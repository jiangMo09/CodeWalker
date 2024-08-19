import os
import tempfile
import requests
import uuid
from git import Repo
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, HttpUrl
import boto3
from botocore.exceptions import ClientError
from utils.mysql import get_db, execute_query
from utils.load_env import S3_BUCKET, S3_FOLDER, CLOUDFRONT_URL

router = APIRouter()


class RepoUrl(BaseModel):
    url: HttpUrl


def is_public_repo(repo_url):
    response = requests.get(repo_url)
    return response.status_code == 200


def clone_repo(repo_url, temp_dir):
    Repo.clone_from(repo_url, temp_dir)


def validate_repo_contents(temp_dir):
    allowed_extensions = {".html", ".js", ".css"}
    has_index_html = False

    for root, _, files in os.walk(temp_dir):
        if ".git" in root:
            continue
        for file in files:
            if file == "index.html" and root == temp_dir:
                has_index_html = True
            file_extension = os.path.splitext(file)[1].lower()
            if file_extension not in allowed_extensions:
                return False

    return has_index_html


def upload_to_s3(local_path, s3_prefix):
    s3 = boto3.client("s3")
    for root, _, files in os.walk(local_path):
        for file in files:
            local_file = os.path.join(root, file)
            relative_path = os.path.relpath(local_file, local_path)
            s3_key = os.path.join(S3_FOLDER, s3_prefix, relative_path)
            file_extension = os.path.splitext(file)[1].lower()

            content_type = "text/plain"
            if file_extension == ".html":
                content_type = "text/html"
            elif file_extension == ".js":
                content_type = "application/javascript"
            elif file_extension == ".css":
                content_type = "text/css"

            with open(local_file, "rb") as file_data:
                s3.upload_fileobj(
                    file_data,
                    S3_BUCKET,
                    s3_key,
                    ExtraArgs={"ContentType": content_type},
                )


def save_repo_info(db, repo_url, cloudfront_path):
    query = """
    INSERT INTO repo_info (repo_url, cloudfront_path) 
    VALUES (%s, %s)
    """
    execute_query(db, query, (repo_url, cloudfront_path))


@router.post("/pure_js")
async def post_pure_js(repo_url: RepoUrl, db=Depends(get_db)):
    try:
        if not is_public_repo(repo_url.url):
            raise HTTPException(status_code=400, detail="Repository is not public")

        with tempfile.TemporaryDirectory() as temp_dir:
            clone_repo(repo_url.url, temp_dir)

            if not validate_repo_contents(temp_dir):
                raise HTTPException(
                    status_code=400, detail="Invalid repository contents"
                )

            unique_id = uuid.uuid4()
            s3_prefix = f"{unique_id}"

            upload_to_s3(temp_dir, s3_prefix)

            cloudfront_path = f"{CLOUDFRONT_URL}/pure-js/{s3_prefix}/index.html"
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
