import requests


def get_instance_private_ip():
    try:
        response = requests.get(
            "http://169.254.169.254/latest/meta-data/local-ipv4", timeout=2
        )
        return response.text
    except requests.RequestException:
        print("無法獲取實例元數據。確保這段代碼在EC2實例上運行。")
        return None
