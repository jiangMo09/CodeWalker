import boto3
import uuid

OAC_ID = "E19EEGSWNVXGMG"


def create_cloudfront(bucket_name):
    cloudfront = boto3.client("cloudfront")

    distribution_config = {
        "CallerReference": str(uuid.uuid4()),
        "DefaultRootObject": "index.html",
        "Origins": {
            "Quantity": 1,
            "Items": [
                {
                    "Id": bucket_name,
                    "DomainName": f"{bucket_name}.s3.ap-northeast-1.amazonaws.com",
                    "OriginPath": "",
                    "S3OriginConfig": {"OriginAccessIdentity": ""},
                    "OriginAccessControlId": OAC_ID,
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
            # 使用推薦的 Cache Policy 和 Origin Request Policy
            "CachePolicyId": "658327ea-f89d-4fab-a63d-7e88639e58f6",  # CachingOptimized Policy ID (S3 優化)
        },
        "Enabled": True,
        "PriceClass": "PriceClass_200",
        "HttpVersion": "http2",
        "Comment": bucket_name,
    }

    distribution = cloudfront.create_distribution(
        DistributionConfig=distribution_config
    )
    distribution_id = distribution["Distribution"]["Id"]
    cloudfront_domain = distribution["Distribution"]["DomainName"]
    return cloudfront_domain, distribution_id
