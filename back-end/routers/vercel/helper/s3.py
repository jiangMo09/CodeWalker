import boto3
import os
import mimetypes
import json

account_id = 767397801164

def update_bucket_policy_OAI(bucket_name, oai_id):
    s3 = boto3.client("s3")

    policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "1",
                "Effect": "Allow",
                "Principal": {
                    "AWS": f"arn:aws:iam::cloudfront:user/CloudFront Origin Access Identity {oai_id}"
                },
                "Action": "s3:GetObject",
                "Resource": f"arn:aws:s3:::{bucket_name}/*"
            }
        ]
    }

    s3.put_bucket_policy(Bucket=bucket_name, Policy=json.dumps(policy))
    print(f"Bucket policy updated for '{bucket_name}'")

def update_bucket_policy(bucket_name, distribution_id):
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
                        "AWS:SourceArn": f"arn:aws:cloudfront::{account_id}:distribution/{distribution_id}"
                    }
                },
            }
        ],
    }

    s3.put_bucket_policy(Bucket=bucket_name, Policy=json.dumps(policy))
    print(f"Bucket policy updated for '{bucket_name}'")


def create_s3(bucket_name, region="ap-northeast-1"):
    s3 = boto3.client("s3")
    try:
        s3.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={"LocationConstraint": region},
        )
        print(f"S3 bucket '{bucket_name}' created successfully.")

        s3.head_bucket(Bucket=bucket_name)
        print(f"Confirmed that bucket '{bucket_name}' exists and is accessible.")
    except Exception as e:
        print(f"Error creating or confirming S3 bucket: {str(e)}")
        raise


def upload_files_to_s3(local_path, bucket_name):
    s3 = boto3.client("s3")
    for root, _, files in os.walk(local_path):
        for file in files:
            local_file = os.path.join(root, file)
            relative_path = os.path.relpath(local_file, local_path)
            s3_key = relative_path.replace("\\", "/")

            content_type, _ = mimetypes.guess_type(local_file)
            if content_type is None:
                content_type = "application/octet-stream"

            s3.upload_file(
                local_file,
                bucket_name,
                s3_key,
                ExtraArgs={"ContentType": content_type},
            )
    print(f"Files uploaded to S3 bucket '{bucket_name}' successfully.")
