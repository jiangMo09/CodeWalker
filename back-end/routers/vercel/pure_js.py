import tempfile
from typing import List
from botocore.exceptions import ClientError
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Request
from pydantic import BaseModel
import shortuuid
import jwt

from utils.mysql import get_db, execute_query, get_db_connection
from utils.load_env import JWT_SECRET_KEY
from .helper.github_repo import (
    clone_repo,
    extract_github_info,
    is_public_repo,
    validate_repo_contents,
)
from .helper.s3 import (
    create_s3,
    create_static_s3,
    upload_files_to_s3,
    update_bucket_policy,
)
from .helper.cloudfront import create_cloudfront
from .helper.route53 import (
    create_route53_record_for_s3,
    create_route53_record_for_cloudfront,
)
from .helper.get_deployment_status import get_deployment_status

router = APIRouter()


class RepoInfo(BaseModel):
    url: str
    deploymentType: str
    storageTypes: List[str]


def process_req_with_static_s3(local_path: str, bucket_name: str) -> str:
    create_static_s3(bucket_name)
    create_route53_record_for_s3(bucket_name)
    upload_files_to_s3(local_path, bucket_name)
    return f"http://{bucket_name}"


def process_req_with_cdn_s3(local_path: str, bucket_name: str) -> str:
    create_s3(bucket_name)
    upload_files_to_s3(local_path, bucket_name)
    cloudfront_domain, distribution_id = create_cloudfront(bucket_name)
    if not distribution_id:
        raise HTTPException(
            status_code=500, detail="Failed to create CloudFront distribution"
        )
    update_bucket_policy(bucket_name, distribution_id)
    url = create_route53_record_for_cloudfront(bucket_name, cloudfront_domain)
    return url, distribution_id, cloudfront_domain


def deploy_process(deployment_id: int, repo_url: RepoInfo):
    connection = None
    try:
        connection = get_db_connection()

        execute_query(
            connection,
            "UPDATE deployments SET status = %s WHERE id = %s",
            ("deploying", deployment_id),
        )

        user_name, repo_name = extract_github_info(repo_url.url)
        with tempfile.TemporaryDirectory() as temp_dir:
            clone_repo(repo_url.url, temp_dir)
            if not validate_repo_contents(temp_dir):
                raise HTTPException(
                    status_code=400,
                    detail="Invalid repository contents, repository should only contain HTML, JS, CSS and MD files.",
                )

            short_id = shortuuid.uuid()[:4]
            s3_prefix = f"{repo_name}-{short_id}".lower()
            bucket_name = f"{s3_prefix}.codewalker.cc"

            if not repo_url.storageTypes:
                deploy_url = process_req_with_static_s3(temp_dir, bucket_name)
                s3_url = deploy_url
                cloudfront_id = None
                cloudfront_url = None
            elif repo_url.storageTypes[0] == "CloudFront":
                deploy_url, cloudfront_id, cloudfront_url = process_req_with_cdn_s3(
                    temp_dir, s3_prefix
                )
                s3_url = f"http://{bucket_name}.s3-website-us-east-1.amazonaws.com"
            else:
                raise HTTPException(status_code=400, detail="Invalid storage type")

        execute_query(
            connection,
            """
            UPDATE deployments 
            SET status = %s, route53_url = %s, s3_bucketname = %s, s3_url = %s, cloudfront_id = %s, cloudfront_url = %s
            WHERE id = %s
            """,
            (
                "pending",
                deploy_url,
                bucket_name,
                s3_url,
                cloudfront_id,
                cloudfront_url,
                deployment_id,
            ),
        )

    except HTTPException as he:
        if connection:
            execute_query(
                connection,
                "UPDATE deployments SET status = %s WHERE id = %s",
                ("failed", deployment_id),
            )
        print(f"Deployment failed: {he.detail}")
        raise
    except Exception as e:
        if connection:
            execute_query(
                connection,
                "UPDATE deployments SET status = %s WHERE id = %s",
                ("failed", deployment_id),
            )
        print(f"Deployment failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    finally:
        if connection:
            connection.close()


@router.post("/deploy/pure_js")
async def post_pure_js(
    request: Request,
    repo_url: RepoInfo,
    background_tasks: BackgroundTasks,
    db=Depends(get_db),
):
    print(repo_url)
    try:
        auth_token = request.headers.get("authToken")
        payload = jwt.decode(auth_token, JWT_SECRET_KEY, algorithms=["HS256"])

        if not payload:
            raise HTTPException(status_code=403, detail="Please Login")
        user_id = payload["id"]

        if not is_public_repo(repo_url.url):
            raise HTTPException(status_code=400, detail="Repository is not public")

        if repo_url.deploymentType != "pureJs":
            raise HTTPException(status_code=400, detail="Invalid deployment type")

        user_name, repo_name = extract_github_info(repo_url.url)
        if not repo_name:
            raise HTTPException(
                status_code=400,
                detail="Invalid GitHub repository URL, can't find repo_name.",
            )

        # TODO:here will have race condition

        execute_query(
            db,
            """
            INSERT INTO deployments 
            (user_id, deployment_type, github_repo_url, github_repo_name, github_repo_owner,status) 
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                user_id,
                repo_url.deploymentType,
                repo_url.url,
                repo_name,
                user_name,
                "validating",
            ),
        )

        result = execute_query(db, "SELECT LAST_INSERT_ID()", fetch_method="fetchone")

        deployment_id = result["LAST_INSERT_ID()"]
        if not deployment_id:
            raise HTTPException(
                status_code=500, detail="Failed to create deployment record"
            )

        background_tasks.add_task(deploy_process, deployment_id, repo_url)

        return {
            "data": {
                "success": True,
                "message": "Deployment process started",
                "deployment_id": deployment_id,
            }
        }

    except HTTPException:
        raise
    except ClientError as ce:
        raise HTTPException(status_code=500, detail=f"AWS Error: {str(ce)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@router.get("/deploy/status/{deployment_id}")
async def get_deployment_status_route(deployment_id: int, db=Depends(get_db)):
    return await get_deployment_status(deployment_id, db)
