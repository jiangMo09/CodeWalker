import os
import tempfile
import time
import shortuuid
from git import Repo
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, HttpUrl
import boto3
from botocore.exceptions import ClientError
from utils.mysql import get_db, execute_query
from utils.load_env import S3_BUCKET, S3_FOLDER, CLOUDFRONT_URL

from .helper.github_repo import clone_repo, extract_github_info, is_public_repo
from .helper.s3 import create_s3, upload_files_to_s3, update_bucket_policy
from .helper.cloudfront import create_cloudfront

router = APIRouter()


class RepoUrl(BaseModel):
    url: str


def validate_repo_contents(temp_dir):
    allowed_extensions = {".html", ".js", ".css"}
    has_index_html = False

    for root, _, files in os.walk(temp_dir):
        for file in files:
            if file == "index.html" and root == temp_dir:
                has_index_html = True
            file_extension = os.path.splitext(file)[1].lower()
            if file_extension not in allowed_extensions:
                return False

    return has_index_html


# def save_repo_info(db, repo_url, cloudfront_path):
#     query = """
#     INSERT INTO repo_info (repo_url, cloudfront_path)
#     VALUES (%s, %s)
#     """
#     execute_query(db, query, (repo_url, cloudfront_path))


def process_new_request(local_path, bucket_name):
    create_s3(bucket_name)
    upload_files_to_s3(local_path, bucket_name)

    cloudfront_url, distribution_id = create_cloudfront(bucket_name)

    if distribution_id:
        print("update_bucket_policy", distribution_id)
        update_bucket_policy(bucket_name, distribution_id)

    else:
        print(
            "Failed to create CloudFront distribution. Skipping bucket policy update."
        )
    full_cloudfront_url = f"https://{cloudfront_url}"

    return full_cloudfront_url


@router.post("/pure_js")
async def post_pure_js(repo_url: RepoUrl, db=Depends(get_db)):
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

            if not validate_repo_contents(temp_dir):
                raise HTTPException(
                    status_code=400, detail="Invalid repository contents"
                )

            short_id = shortuuid.uuid()[:4]
            s3_prefix = f"{repo_name}-{short_id}".lower()

            cloudfront_path = process_new_request(temp_dir, s3_prefix)

            print(cloudfront_path)
            # save_repo_info(db, repo_url.url, cloudfront_path)

            return {
                "data": {
                    "message": "Repository uploaded successfully",
                    "cloudfront_path": cloudfront_path,
                }
            }

    except HTTPException as he:
        return {"data": {"error": f"Error: {he.detail}"}}
    except ClientError as ce:
        return {"data": {"error": f"Error: Failed to upload to S3 - {str(ce)}"}}
    except Exception as e:
        return {"data": {"error": f"Error: {str(e)}"}}
