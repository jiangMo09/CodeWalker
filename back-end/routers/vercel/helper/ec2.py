import requests


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
