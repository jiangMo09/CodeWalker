import docker
import re
import threading
import sys


def sanitize_repo_url(repo_url):
    repo_name = repo_url.rstrip(".git").split("/")[-1]
    return re.sub(r"[^a-zA-Z0-9]", "-", repo_name)


def stop_container(container):
    container.stop()
    print(f"Container {container.name} has been stopped after 30 seconds.")


def run_docker(repo_url):
    client = docker.from_env()
    container_name = sanitize_repo_url(repo_url)

    try:
        container = client.containers.run(
            "pure-js-docker",
            command=repo_url,
            detach=True,
            ports={"8000/tcp": 8000},
            name=container_name,
            cpu_quota=50000,
            mem_limit="128m",
        )
        print(
            f"Container {container.name} is running. Access the website at http://localhost:8000"
        )

        timer = threading.Timer(30.0, stop_container, [container])
        timer.start()

    except docker.errors.APIError as e:
        print(f"Failed to start container: {e.explanation}")


def main(repo_url):
    run_docker(repo_url)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python docker-manager-project.py <github_repo_url>")
        sys.exit(1)

    repo_url = sys.argv[1]
    main(repo_url)
