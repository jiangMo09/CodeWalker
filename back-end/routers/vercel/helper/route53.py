from fastapi import HTTPException
import boto3
from utils.load_env import (
    ROUTE53_HOSTED_ZONE_ID,
    S3_HOSTED_ZONE_ID,
    S3_WEBSITE_ENDPOINT,
    AWS_ALB_DNS_NAME,
    AWS_ALB_HOSTED_ZONE_ID,
)


def create_route53_record_for_s3(subdomain: str):
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
        print(f"Successfully created http://{subdomain}")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to create Route53 record: {str(e)}"
        )


def create_route53_record_for_cloudfront(subdomain: str, cloudfront_domain_name: str):
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
                        "HostedZoneId": "Z2FDTNDATAQYW2",  # CloudFront's HostedZoneId
                        "DNSName": cloudfront_domain_name,
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
        print(f"Successfully created/updated record https://{full_domain}")
        return f"https://{full_domain}"
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to create Route53 record: {str(e)}"
        )


def create_route53_record_for_alb(subdomain: str):
    route53_client = boto3.client("route53")

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
                        "HostedZoneId": AWS_ALB_HOSTED_ZONE_ID,
                        "DNSName": f"dualstack.{AWS_ALB_DNS_NAME}",
                        "EvaluateTargetHealth": True,
                    },
                },
            }
        ]
    }

    try:
        route53_client.change_resource_record_sets(
            HostedZoneId=ROUTE53_HOSTED_ZONE_ID, ChangeBatch=change_batch
        )
        print(f"Successfully created/updated record https://{full_domain}")
        return f"https://{full_domain}"
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to create Route53 record: {str(e)}"
        )
