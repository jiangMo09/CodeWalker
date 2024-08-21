import boto3

from utils.load_env import (
    ROUTE53_HOSTED_ZONE_ID,
    S3_HOSTED_ZONE_ID,
    S3_WEBSITE_ENDPOINT,
)


def create_route53_record_for_s3(subdomain):
    route53 = boto3.client("route53")

    change_batch = {
        "Changes": [
            {
                "Action": "UPSERT",
                "ResourceRecordSet": {
                    "Name": subdomain,
                    "Type": "A",
                    "AliasTarget": {
                        "HostedZoneId": S3_HOSTED_ZONE_ID,
                        "DNSName": S3_WEBSITE_ENDPOINT,
                        "EvaluateTargetHealth": True,
                    },
                },
            }
        ]
    }

    try:
        response = route53.change_resource_record_sets(
            HostedZoneId=ROUTE53_HOSTED_ZONE_ID, ChangeBatch=change_batch
        )
        print(f"成功創建/更新記錄 http://{subdomain}")
        return response
    except Exception as e:
        print(f"創建/更新記錄時發生錯誤: {str(e)}")
        return None
