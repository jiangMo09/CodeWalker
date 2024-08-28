import tempfile
from typing import List
from botocore.exceptions import ClientError
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
import shortuuid

from utils.mysql import get_db
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
    return create_route53_record_for_cloudfront(bucket_name, cloudfront_domain)


@router.post("/deploy/pure_js")
async def post_pure_js(repo_url: RepoInfo, db=Depends(get_db)):
    try:
        if not is_public_repo(repo_url.url):
            raise HTTPException(status_code=400, detail="Repository is not public")
        if repo_url.deploymentType != "pureJs":
            raise HTTPException(status_code=400, detail="Invalid deployment type")

        user_name, repo_name = extract_github_info(repo_url.url)
        if not repo_name:
            raise HTTPException(status_code=400, detail="Invalid GitHub repository URL, can't find repo_name.")

        with tempfile.TemporaryDirectory() as temp_dir:
            clone_repo(repo_url.url, temp_dir)
            if not validate_repo_contents(temp_dir):
                raise HTTPException(
                    status_code=400, detail="Invalid repository contents"
                )

            short_id = shortuuid.uuid()[:4]
            s3_prefix = f"{repo_name}-{short_id}".lower()
            bucket_name = f"{s3_prefix}.codewalker.cc"

            if not repo_url.storageTypes:
                deploy_url = process_req_with_static_s3(temp_dir, bucket_name)
            elif repo_url.storageTypes[0] == "CloudFront":
                deploy_url = process_req_with_cdn_s3(temp_dir, s3_prefix)
            else:
                raise HTTPException(status_code=400, detail="Invalid storage type")

        return {
            "data": {
                "success": True,
                "message": "Repository deployed successfully",
                "deploy_url": deploy_url,
            }
        }

    except HTTPException as he:
        return {"data": {"error": f"Error: {he.detail}"}}
    except ClientError as ce:
        return {"data": {"error": f"AWS Error: {str(ce)}"}}
    except Exception as e:
        return {"data": {"error": f"Unexpected error: {str(e)}"}}
