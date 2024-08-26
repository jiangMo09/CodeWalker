import tempfile
from typing import List

from botocore.exceptions import ClientError
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
import shortuuid

from utils.mysql import get_db, execute_query

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

router = APIRouter()


class RepoUrl(BaseModel):
    url: str
    deploymentType: str
    storageTypes: List[str]


# def save_repo_info(db, repo_url, cloudfront_path):
#     query = """
#     INSERT INTO repo_info (repo_url, cloudfront_path)
#     VALUES (%s, %s)
#     """
#     execute_query(db, query, (repo_url, cloudfront_path))


def process_req_with_static_s3(local_path, bucket_name):
    create_static_s3(bucket_name)
    create_route53_record_for_s3(bucket_name)
    upload_files_to_s3(local_path, bucket_name)


def process_req_with_cdn_s3(local_path, bucket_name):
    try:
        create_s3(bucket_name)
        upload_files_to_s3(local_path, bucket_name)

        cloudfront_domain, distribution_id = create_cloudfront(bucket_name)
        if not distribution_id:
            raise Exception("Failed to create CloudFront distribution")

        update_bucket_policy(bucket_name, distribution_id)

        deploy_url = create_route53_record_for_cloudfront(
            bucket_name, cloudfront_domain
        )

        print(f"CloudFront URL: {cloudfront_domain}")
        print(f"Distribution ID: {distribution_id}")
        print(f"Bucket Name: {bucket_name}")
        print(f"Deploy URL: {deploy_url}")

        return deploy_url

    except Exception as e:
        print(f"Error in process_req_with_cdn_s3: {str(e)}")
        return None


@router.post("/deploy/pure_js")
async def post_pure_js(repo_url: RepoUrl, db=Depends(get_db)):
    print("repo_url repo_url", repo_url)
    try:

        if not is_public_repo(repo_url.url):
            raise HTTPException(status_code=400, detail="Repository is not public")

        user_name, repo_name = extract_github_info(repo_url.url)

        if not repo_name:
            raise HTTPException(
                status_code=400,
                detail="Repository is not github repo, can't find repo_name",
            )

        with tempfile.TemporaryDirectory() as temp_dir:
            clone_repo(repo_url.url, temp_dir)

            short_id = shortuuid.uuid()[:4]
            s3_prefix = f"{repo_name}-{short_id}".lower()

            if repo_url.deploymentType == "pureJs":
                if not validate_repo_contents(temp_dir):
                    raise HTTPException(
                        status_code=400, detail="Invalid repository contents"
                    )

                if not repo_url.storageTypes:
                    print("process_req_with_static_s3")
                    process_req_with_static_s3(temp_dir, s3_prefix + ".codewalker.cc")
                    deploy_url = f"http://{s3_prefix}.codewalker.cc"
                elif repo_url.storageTypes[0] == "CloudFront":
                    print("process_req_with_cdn_s3")
                    deploy_url = process_req_with_cdn_s3(temp_dir, s3_prefix)

                print("deploy_url", deploy_url)

            # save_repo_info(db, repo_url.url, cloudfront_path)

            return {
                "data": {
                    "success": True,
                    "message": "Repository uploaded successfully",
                    "deploy_url": deploy_url,
                }
            }

    except HTTPException as he:
        return {"data": {"error": f"Error1: {he.detail}"}}
    except ClientError as ce:
        return {"data": {"error": f"Error2: Failed to upload to S3 - {str(ce)}"}}
    except Exception as e:
        return {"data": {"error": f"Error3: {str(e)}"}}
