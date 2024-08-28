import subprocess
import docker
import yaml
import time
from pathlib import Path
from typing import List
from fastapi import HTTPException


def create_dockerfile(temp_dir: Path, port: str):
    dockerfile_content = f"""
    FROM python:3.12-slim
    WORKDIR /app
    COPY . .
    RUN pip install --no-cache-dir -r requirements.txt
    EXPOSE {port}
    """

    dockerfile_path = temp_dir / "Dockerfile"
    with open(dockerfile_path, "w") as dockerfile:
        dockerfile.write(dockerfile_content)


def create_docker_compose_file(
    temp_dir: Path,
    service_name: str,
    image_tag: str,
    port: str,
    env_vars: List[dict],
    build_command: str,
):
    compose_config = {
        "version": "3",
        "services": {
            service_name: {
                "build": {"context": ".", "dockerfile": "Dockerfile"},
                "image": image_tag,
                "ports": [f"0:{port}"],
                "environment": [
                    f"{var['key']}={var['value']}" for var in env_vars if var["key"]
                ],
                "command": build_command,
                "mem_limit": "192m",
                "cpus": 0.5,
                "labels": ["com.docker.compose.rm=true"],
            }
        },
    }

    with open(temp_dir / "docker-compose.yml", "w") as f:
        yaml.dump(compose_config, f)


def run_docker_compose(temp_dir: Path):
    try:
        subprocess.run(["docker-compose", "up", "-d"], cwd=temp_dir, check=True)
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Docker Compose error: {str(e)}")


async def deploy_with_docker_compose(
    temp_dir: Path,
    service_name: str,
    image_tag: str,
    port: str,
    env_vars: List[dict],
    build_command: str,
):
    create_dockerfile(temp_dir, port)
    create_docker_compose_file(
        temp_dir, service_name, image_tag, port, env_vars, build_command
    )
    run_docker_compose(temp_dir)

    client = docker.from_env()
    try:
        containers = client.containers.list(filters={"name": service_name})
        if containers:
            container = containers[0]
            container_id = container.id
            port_bindings = container.attrs["NetworkSettings"]["Ports"]
            host_port = port_bindings[f"{port}/tcp"][0]["HostPort"]
            return container_id, host_port
        else:
            raise HTTPException(
                status_code=500, detail="No containers found for the service"
            )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error retrieving container ID: {str(e)}"
        )


def delayed_cleanup(service_name: str, image_tag: str, delay_minutes: int = 1):
    time.sleep(delay_minutes * 60)
    client = docker.from_env()

    try:
        containers = client.containers.list(filters={"name": service_name})
        for container in containers:
            container.stop()
            container.remove()

        client.images.remove(image_tag)

        print(f"Cleaned up {service_name} and its image after {delay_minutes} minutes")
    except Exception as e:
        print(f"Error during cleanup: {str(e)}")
