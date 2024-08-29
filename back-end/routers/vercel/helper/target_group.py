import boto3
from fastapi import HTTPException
from utils.load_env import AWS_VPC_ID, AWS_ALB_LISTENER_ARN


def create_target_group(docker_port: int, subdomain: str):
    alb_client = boto3.client("elbv2")
    target_group_name = f"tg-{subdomain}"

    try:
        response = alb_client.create_target_group(
            Name=target_group_name,
            Protocol="HTTP",
            Port=docker_port,
            VpcId=AWS_VPC_ID,
            TargetType="ip",
            IpAddressType="ipv4",
        )
        return response["TargetGroups"][0]["TargetGroupArn"]
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to create target group: {str(e)}"
        )


def create_listener_rule(target_group_arn: str, subdomain: str, priority: int):
    alb_client = boto3.client("elbv2")

    try:
        alb_client.create_rule(
            ListenerArn=AWS_ALB_LISTENER_ARN,
            Conditions=[
                {"Field": "host-header", "Values": [f"{subdomain}.codewalker.cc"]}
            ],
            Priority=priority,
            Actions=[{"Type": "forward", "TargetGroupArn": target_group_arn}],
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to create listener rule: {str(e)}"
        )


def register_target(target_group_arn: str, instance_ip: str, docker_port: int):
    alb_client = boto3.client("elbv2")

    try:
        alb_client.register_targets(
            TargetGroupArn=target_group_arn,
            Targets=[{"Id": instance_ip, "Port": docker_port}],
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to register target: {str(e)}"
        )
