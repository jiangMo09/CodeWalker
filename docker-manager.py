import docker
import sys
import time

client = docker.from_env()


def measure_resources():
    return {"time": time.perf_counter()}


def run_container(image_name, function_code):
    environment = {
        "python-docker": {"GREET_FUNCTION": function_code},
        "js-docker": {"GREET_FUNCTION": function_code},
        "java-docker": {"GREET_FUNCTION": function_code},
        "cpp-docker": {"GREET_FUNCTION": function_code},
    }

    try:
        start = measure_resources()

        container = client.containers.run(
            image_name, environment=environment[image_name], detach=True
        )

        timeout = 15
        container.wait(timeout=timeout)

        end = measure_resources()

        output = container.logs().decode("utf-8").strip()
        print(output)

        # 計算並輸出結果
        execution_time = end["time"] - start["time"]

        print(f"是否為無窮迴圈: {'否' if execution_time < timeout else '可能是'}")

        container.remove()
    except docker.errors.ImageNotFound:
        print(f"錯誤: 找不到映像 {image_name}")
    except Exception as e:
        print(f"發生錯誤: {str(e)}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("用法: python docker-manage.py <language> <function_code>")
        sys.exit(1)

    language = sys.argv[1].lower()
    function_code = sys.argv[2]

    language_to_image = {
        "js": "js-docker",
        "python": "python-docker",
        "java": "java-docker",
        "cpp": "cpp-docker",
    }

    if language not in language_to_image:
        print(f"不支援的語言: {language}")
        sys.exit(1)

    image_name = language_to_image[language]
    run_container(image_name, function_code)
