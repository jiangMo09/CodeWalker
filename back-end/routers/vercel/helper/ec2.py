import requests
import boto3
from botocore.exceptions import ClientError
from utils.load_env import AWS_ALB_SECURITY_GROUP_ID


def get_instance_id():
    try:
        token_response = requests.put(
            "http://169.254.169.254/latest/api/token",
            headers={"X-aws-ec2-metadata-token-ttl-seconds": "21600"},
            timeout=2,
        )
        if token_response.status_code == 200:
            token = token_response.text
            response = requests.get(
                "http://169.254.169.254/latest/meta-data/instance-id",
                headers={"X-aws-ec2-metadata-token": token},
                timeout=2,
            )
            if response.status_code == 200:
                return response.text
            else:
                print(f"無法獲取實例ID，狀態碼: {response.status_code}")
                return None
        else:
            print(f"無法獲取IMDSv2令牌，狀態碼: {token_response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"無法獲取實例ID: {e}")
        return None


def get_instance_security_group(instance_id):
    ec2 = boto3.client("ec2")
    try:
        response = ec2.describe_instances(InstanceIds=[instance_id])
        security_groups = response["Reservations"][0]["Instances"][0]["SecurityGroups"]
        return security_groups[0]["GroupId"]
    except ClientError as e:
        print(f"無法獲取安全組ID: {e}")
        return None


def add_security_group_rule(group_id, port):
    ec2 = boto3.client("ec2")
    try:
        ec2.authorize_security_group_ingress(
            GroupId=group_id,
            IpPermissions=[
                {
                    "IpProtocol": "tcp",
                    "FromPort": port,
                    "ToPort": port,
                    "UserIdGroupPairs": [{"GroupId": AWS_ALB_SECURITY_GROUP_ID}],
                }
            ],
        )
        print(f"已成功添加安全組規則：允許來自ALB的流量通過端口 {port}")
    except ClientError as e:
        print(f"添加安全組規則失敗: {e}")
