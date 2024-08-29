import requests


def get_instance_id():
    try:
        response = requests.get(
            "http://169.254.169.254/latest/meta-data/instance-id", timeout=2
        )
        if response.status_code == 200:
            return response.text
        else:
            print(f"無法獲取實例ID，狀態碼: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"無法獲取實例ID: {e}")
        return None
