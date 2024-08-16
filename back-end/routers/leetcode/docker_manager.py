import docker
import sys
import json
import time
from utils.load_env import ENVIRONMENT, ECR_REGISTRY

client = docker.from_env()


def measure_resources():
    return {"time": time.perf_counter()}


async def run_container(image_name, data):
    environment = {
        "js-docker": {"DATA_INPUT": json.dumps(data)},
        "python-docker": {"DATA_INPUT": json.dumps(data)},
        "java-docker": {"DATA_INPUT": json.dumps(data)},
        "cpp-docker": {"DATA_INPUT": json.dumps(data)},
    }

    if ENVIRONMENT == "production":
        full_image_name = f"{ECR_REGISTRY}/codewalker:{image_name}"
    else:
        full_image_name = image_name

    try:
        start = measure_resources()

        container = client.containers.run(
            full_image_name,
            environment=environment[image_name],
            detach=True,
            cpu_quota=50000,
            mem_limit="128m",
        )
        timeout = 15
        container.wait(timeout=timeout)

        end = measure_resources()

        logs = (
            container.logs(stdout=True, stderr=True).decode("utf-8").strip().split("\n")
        )
        log_data = None
        error_message = None

        for line in logs:
            try:
                log_data = json.loads(line)
            except json.JSONDecodeError:
                if "Error:" in line:
                    error_message = line.strip()
                print(f"無法解析的日誌行: {line}")

        execution_time = end["time"] - start["time"]

        if log_data:
            result = {
                "container_run_success": True,
                "run_result": log_data.get("run_result", []),
                "total_correct": log_data.get("total_correct", 0),
                "total_testcases": log_data.get("total_testcases", 0),
                "total_run_time": log_data.get("total_run_time", "0 ms"),
                "total_run_memory": log_data.get("total_run_memory", "0 MB"),
                "all_passed": log_data.get("all_passed", False),
                "is_infinite_loop": execution_time >= timeout,
            }
        else:
            result = {
                "container_run_success": False,
                "error": error_message or "Unknown error occurred",
            }

        return result
    except Exception as e:
        print(f"發生錯誤: {str(e)}")
        return {"container_run_success": False, "error": str(e)}
    finally:
        container.remove()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("用法: python docker-manage.py <json_data>")
        sys.exit(1)

    data = json.loads(sys.argv[1])
    language = data.get("lang", "").lower()

    language_to_image = {
        "javascript": "js-docker",
        "python3": "python-docker",
        "java": "java-docker",
        "cpp": "cpp-docker",
    }

    if language not in language_to_image:
        print(f"不支援的語言: {language}")
        sys.exit(1)

    image_name = language_to_image[language]
    run_container(image_name, data)
