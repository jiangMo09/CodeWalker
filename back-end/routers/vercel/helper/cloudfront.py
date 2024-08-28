import boto3
import uuid
from fastapi import HTTPException
from utils.load_env import (
    CLOUDFRONT_OAC_ID,
    AWS_BUCKET_REGION,
    AWS_ACCOUNT_ID,
    AWS_ACM_ID,
)


def create_cloudfront(bucket_name: str):
    try:
        cloudfront = boto3.client("cloudfront")
        distribution_config = {
            "CallerReference": str(uuid.uuid4()),
            "Aliases": {
                "Quantity": 1,
                "Items": [f"{bucket_name}.codewalker.cc"],
            },
            "DefaultRootObject": "index.html",
            "Origins": {
                "Quantity": 1,
                "Items": [
                    {
                        "Id": bucket_name,
                        "DomainName": f"{bucket_name}.s3.{AWS_BUCKET_REGION}.amazonaws.com",
                        "OriginPath": "",
                        "S3OriginConfig": {"OriginAccessIdentity": ""},
                        "OriginAccessControlId": CLOUDFRONT_OAC_ID,
                    },
                ],
            },
            "DefaultCacheBehavior": {
                "TargetOriginId": bucket_name,
                "ViewerProtocolPolicy": "allow-all",
                "AllowedMethods": {
                    "Quantity": 2,
                    "Items": ["GET", "HEAD"],
                    "CachedMethods": {"Quantity": 2, "Items": ["GET", "HEAD"]},
                },
                "CachePolicyId": "658327ea-f89d-4fab-a63d-7e88639e58f6",  # CachingOptimized Policy ID (S3 optimized)
            },
            "ViewerCertificate": {
                "ACMCertificateArn": f"arn:aws:acm:us-east-1:{AWS_ACCOUNT_ID}:certificate/{AWS_ACM_ID}",
                "SSLSupportMethod": "sni-only",
                "MinimumProtocolVersion": "TLSv1.2_2021",
            },
            "Enabled": True,
            "PriceClass": "PriceClass_200",
            "HttpVersion": "http2",
            "Comment": bucket_name,
        }
        distribution = cloudfront.create_distribution(
            DistributionConfig=distribution_config
        )
        return (
            distribution["Distribution"]["DomainName"],
            distribution["Distribution"]["Id"],
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create CloudFront distribution: {str(e)}",
        )
