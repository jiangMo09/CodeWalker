import boto3
import os
import mimetypes
import json
from botocore.exceptions import ClientError
from fastapi import HTTPException
from utils.load_env import AWS_ACCOUNT_ID, AWS_BUCKET_REGION


def update_bucket_policy(bucket_name: str, distribution_id: str):
    s3 = boto3.client("s3")
    policy = {
        "Version": "2008-10-17",
        "Id": "PolicyForCloudFrontPrivateContent",
        "Statement": [
            {
                "Sid": "AllowCloudFrontServicePrincipal",
                "Effect": "Allow",
                "Principal": {"Service": "cloudfront.amazonaws.com"},
                "Action": "s3:GetObject",
                "Resource": f"arn:aws:s3:::{bucket_name}/*",
                "Condition": {
                    "StringEquals": {
                        "AWS:SourceArn": f"arn:aws:cloudfront::{AWS_ACCOUNT_ID}:distribution/{distribution_id}"
                    }
                },
            }
        ],
    }
    try:
        s3.put_bucket_policy(Bucket=bucket_name, Policy=json.dumps(policy))
        print(f"Bucket policy updated for '{bucket_name}'")
    except ClientError as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to update bucket policy: {str(e)}"
        )


def create_static_s3(
    bucket_name: str,
    region: str = AWS_BUCKET_REGION,
    index_document: str = "index.html",
    error_document: str = "error.html",
):
    s3 = boto3.client("s3", region_name=region)
    try:
        s3.create_bucket(
            Bucket=bucket_name, CreateBucketConfiguration={"LocationConstraint": region}
        )
        s3.put_public_access_block(
            Bucket=bucket_name,
            PublicAccessBlockConfiguration={
                "BlockPublicAcls": False,
                "IgnorePublicAcls": False,
                "BlockPublicPolicy": False,
                "RestrictPublicBuckets": False,
            },
        )
        bucket_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "PublicReadGetObject",
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": "s3:GetObject",
                    "Resource": f"arn:aws:s3:::{bucket_name}/*",
                }
            ],
        }
        s3.put_bucket_policy(Bucket=bucket_name, Policy=json.dumps(bucket_policy))
        s3.put_bucket_website(
            Bucket=bucket_name,
            WebsiteConfiguration={
                "ErrorDocument": {"Key": error_document},
                "IndexDocument": {"Suffix": index_document},
            },
        )
        print(f"Static website hosting enabled for bucket {bucket_name}")
    except ClientError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create static S3 bucket or set website: {str(e)}",
        )


def create_s3(bucket_name: str, region: str = AWS_BUCKET_REGION):
    s3 = boto3.client("s3")
    try:
        s3.create_bucket(
            Bucket=bucket_name, CreateBucketConfiguration={"LocationConstraint": region}
        )
        s3.head_bucket(Bucket=bucket_name)
        print(f"S3 bucket '{bucket_name}' created and accessible.")
    except ClientError as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to create or access S3 bucket: {str(e)}"
        )


def upload_files_to_s3(local_path: str, bucket_name: str):
    s3 = boto3.client("s3")
    try:
        for root, _, files in os.walk(local_path):
            for file in files:
                local_file = os.path.join(root, file)
                s3_key = os.path.relpath(local_file, local_path).replace("\\", "/")
                content_type, _ = mimetypes.guess_type(local_file)
                s3.upload_file(
                    local_file,
                    bucket_name,
                    s3_key,
                    ExtraArgs={
                        "ContentType": content_type or "application/octet-stream"
                    },
                )
        print(f"Files uploaded to S3 bucket '{bucket_name}' successfully.")
    except ClientError as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to upload files to S3: {str(e)}"
        )
