import subprocess
import docker
import yaml
import time
from pathlib import Path
from typing import List
from fastapi import HTTPException


def create_dockerfile(temp_dir: Path, port: str):
    print(f"Creating Dockerfile in {temp_dir} with port {port}")
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
    print("Dockerfile created successfully")


def create_docker_compose_file(
    temp_dir: Path,
    service_name: str,
    image_tag: str,
    port: str,
    env_vars: List[dict],
    build_command: str,
):
    print(f"Creating docker-compose.yml in {temp_dir} for service {service_name}")
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
    print("docker-compose.yml created successfully")


def run_docker_compose(temp_dir: Path):
    print(f"Running docker-compose up in {temp_dir}")
    try:
        subprocess.run(["docker-compose", "up", "-d"], cwd=temp_dir, check=True)
        print("docker-compose up completed successfully")
    except subprocess.CalledProcessError as e:
        print(f"Error running docker-compose: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Docker Compose error: {str(e)}")


async def deploy_with_docker_compose(
    temp_dir: Path,
    service_name: str,
    image_tag: str,
    port: str,
    env_vars: List[dict],
    build_command: str,
):
    print(f"Deploying service {service_name} with Docker Compose")
    create_dockerfile(temp_dir, port)
    create_docker_compose_file(
        temp_dir, service_name, image_tag, port, env_vars, build_command
    )
    run_docker_compose(temp_dir)

    client = docker.from_env()
    try:
        print(f"Retrieving container information for service {service_name}")
        containers = client.containers.list(filters={"name": service_name})
        if containers:
            container = containers[0]
            container_id = container.id
            port_bindings = container.attrs["NetworkSettings"]["Ports"]
            host_port = port_bindings[f"{port}/tcp"][0]["HostPort"]
            print(f"Container ID: {container_id}, Host Port: {host_port}")
            return container_id, host_port
        else:
            print("No containers found for the service")
            raise HTTPException(
                status_code=500, detail="No containers found for the service"
            )
    except Exception as e:
        print(f"Error retrieving container ID: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error retrieving container ID: {str(e)}"
        )
    finally:
        client.close()


def delayed_cleanup(service_name: str, image_tag: str, delay_minutes: int = 60):
    print(f"Scheduling cleanup for {service_name} after {delay_minutes} minutes")
    time.sleep(delay_minutes * 60)
    client = docker.from_env()

    try:
        print(f"Starting cleanup for {service_name}")

        containers = client.containers.list(filters={"name": service_name})
        for container in containers:
            print(f"Stopping and removing container {container.id}")
            container.stop()
            container.remove()

        print(f"Removing image {image_tag}")
        client.images.remove(image_tag)

        print(f"Cleaning up build cache for {service_name}")
        build_cache_result = client.images.prune(
            filters={"label": f"service={service_name}", "dangling": True}
        )
        print(
            f"Cleaned up {build_cache_result['SpaceReclaimed']} bytes of build cache for {service_name}"
        )

        print(f"Cleaning up unused networks for {service_name}")
        networks = client.networks.list(filters={"label": f"service={service_name}"})
        removed_networks = 0
        for network in networks:
            if not network.containers:
                print(f"Removing unused network: {network.name}")
                network.remove()
                removed_networks += 1
        print(f"Removed {removed_networks} unused networks for {service_name}")

        print(
            f"Cleaned up containers, image, build cache, and unused networks for {service_name} after {delay_minutes} minutes"
        )
    except Exception as e:
        print(f"Error during cleanup: {str(e)}")
    finally:
        client.close()
