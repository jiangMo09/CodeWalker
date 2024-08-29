import boto3
from fastapi import HTTPException
from utils.load_env import AWS_VPC_ID, AWS_ALB_LISTENER_ARN, AWS_BUCKET_REGION


def create_target_group(docker_port: int, subdomain: str):
    print(f"Creating target group for subdomain: {subdomain} on port: {docker_port}")
    print(f"Using AWS region: {AWS_BUCKET_REGION}")
    alb_client = boto3.client("elbv2", region_name=AWS_BUCKET_REGION)
    target_group_name = f"tg-{subdomain}"

    try:
        print(f"Sending request to create target group: {target_group_name}")
        response = alb_client.create_target_group(
            Name=target_group_name,
            Protocol="HTTP",
            Port=docker_port,
            VpcId=AWS_VPC_ID,
            TargetType="instance",
            IpAddressType="ipv4",
        )
        target_group_arn = response["TargetGroups"][0]["TargetGroupArn"]
        print(f"Target group created successfully. ARN: {target_group_arn}")
        return target_group_arn
    except Exception as e:
        print(f"Error creating target group: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Failed to create target group: {str(e)}"
        )


def create_listener_rule(target_group_arn: str, subdomain: str):
    priority = get_available_priority(AWS_ALB_LISTENER_ARN)
    print(
        f"Creating listener rule for subdomain: {subdomain} with priority: {priority}"
    )
    print(f"Using AWS region: {AWS_BUCKET_REGION}")
    alb_client = boto3.client("elbv2", region_name=AWS_BUCKET_REGION)

    try:
        print(f"Sending request to create listener rule for {subdomain}.codewalker.cc")
        response = alb_client.create_rule(
            ListenerArn=AWS_ALB_LISTENER_ARN,
            Conditions=[
                {"Field": "host-header", "Values": [f"{subdomain}.codewalker.cc"]}
            ],
            Priority=priority,
            Actions=[{"Type": "forward", "TargetGroupArn": target_group_arn}],
        )
        print(f"Listener rule created successfully for {subdomain}.codewalker.cc")
    except Exception as e:
        print(f"Error creating listener rule: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Failed to create listener rule: {str(e)}"
        )


def register_target(target_group_arn: str, instance_id: str, docker_port: int):
    print(f"Registering target with Instance ID: {instance_id} and port: {docker_port}")
    print(f"Using AWS region: {AWS_BUCKET_REGION}")
    alb_client = boto3.client("elbv2", region_name=AWS_BUCKET_REGION)

    try:
        print(f"Sending request to register target to group: {target_group_arn}")
        response = alb_client.register_targets(
            TargetGroupArn=target_group_arn,
            Targets=[{"Id": instance_id, "Port": docker_port}],
        )
        print(f"Target registered successfully to target group: {target_group_arn}")
    except Exception as e:
        print(f"Error registering target: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Failed to register target: {str(e)}"
        )


def get_available_priority(listener_arn):
    alb_client = boto3.client("elbv2", region_name=AWS_BUCKET_REGION)

    response = alb_client.describe_rules(ListenerArn=listener_arn)
    existing_priorities = [
        rule["Priority"] for rule in response["Rules"] if rule["Priority"] != "default"
    ]

    existing_priorities = sorted([int(p) for p in existing_priorities])

    for i in range(1, 50001):
        if i not in existing_priorities:
            return i

    raise Exception("No available priorities")
