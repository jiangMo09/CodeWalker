import docker
import sys
import json
import time

client = docker.from_env()


def measure_resources():
    return {"time": time.perf_counter()}


def run_container(image_name, data):
    environment = {
        "js-docker": {"DATA_INPUT": json.dumps(data)},
        "python-docker": {"DATA_INPUT": json.dumps(data)},
        "java-docker": {"DATA_INPUT": json.dumps(data)},
        # 可以為其他語言添加類似的配置
    }

    try:
        start = measure_resources()
        container = client.containers.run(
            image_name, environment=environment[image_name], detach=True
        )
        timeout = 15
        container.wait(timeout=timeout)

        end = measure_resources()

        logs = container.logs(stream=True)
        for line in logs:
            print(line.decode("utf-8").strip())

        execution_time = end["time"] - start["time"]

        print(f"是否為無窮迴圈: {'否' if execution_time < timeout else '可能是'}")

        container.remove()
    except Exception as e:
        print(f"發生錯誤: {str(e)}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("用法: python docker-manage.py <json_data>")
        sys.exit(1)

    data = json.loads(sys.argv[1])
    language = data.get("lang", "").lower()

    language_to_image = {
        "javascript": "js-docker",
        "python": "python-docker",
        "java": "java-docker",
        # 可以為其他語言添加映射
    }

    if language not in language_to_image:
        print(f"不支援的語言: {language}")
        sys.exit(1)

    image_name = language_to_image[language]
    run_container(image_name, data)
