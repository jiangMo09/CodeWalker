from fastapi import HTTPException

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
        route53.change_resource_record_sets(
            HostedZoneId=ROUTE53_HOSTED_ZONE_ID, ChangeBatch=change_batch
        )
        print(f"成功建立 http://{subdomain}")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to create Route53 record: {str(e)}"
        )


def create_route53_record_for_cloudfront(subdomain, cloudfront_domain_name):
    route53 = boto3.client("route53")

    full_domain = (
        f"{subdomain}.codewalker.cc"
        if not subdomain.endswith(".codewalker.cc")
        else subdomain
    )

    change_batch = {
        "Changes": [
            {
                "Action": "UPSERT",
                "ResourceRecordSet": {
                    "Name": full_domain,
                    "Type": "A",
                    "AliasTarget": {
                        "HostedZoneId": "Z2FDTNDATAQYW2",  # CloudFront 的 HostedZoneId
                        "DNSName": cloudfront_domain_name,  # 這應該是 CloudFront 分配的域名
                        "EvaluateTargetHealth": True,
                    },
                },
            }
        ]
    }

    try:
        route53.change_resource_record_sets(
            HostedZoneId=ROUTE53_HOSTED_ZONE_ID,
            ChangeBatch=change_batch,
        )
        print(f"成功建立/更新記錄 https://{full_domain}")
        return f"https://{full_domain}"
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to create Route53 record: {str(e)}"
        )
