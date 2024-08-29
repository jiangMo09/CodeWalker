import tempfile
import re
from typing import List
from pathlib import Path
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel

from .helper.github_repo import clone_repo, extract_github_info, is_public_repo
from .helper.docker import deploy_with_docker_compose, delayed_cleanup
from .helper.target_group import (
    create_target_group,
    register_target,
    create_listener_rule,
)
from .helper.route53 import create_route53_record_for_alb
from .helper.ec2 import (
    get_instance_id,
    get_instance_security_group,
    add_security_group_rule,
)

router = APIRouter()


class RepoInfo(BaseModel):
    url: str
    deploymentType: str
    storageTypes: List[str]
    buildCommand: str
    envVars: List[dict]
    rootDir: str


class DeploymentData(BaseModel):
    success: bool
    message: str
    deploy_url: str


class DeploymentResponse(BaseModel):
    data: DeploymentData


class ErrorResponse(BaseModel):
    error: str


@router.post(
    "/deploy/fast_api",
    response_model=DeploymentResponse,
    responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
)
async def deploy_fast_api(repo_info: RepoInfo, background_tasks: BackgroundTasks):
    try:
        if not is_public_repo(repo_info.url):
            raise HTTPException(status_code=400, detail="Repository is not public")

        user_name, repo_name = extract_github_info(repo_info.url)
        if not repo_name:
            raise HTTPException(
                status_code=400,
                detail="Repository is not a GitHub repo, can't find repo_name",
            )

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir_path = Path(temp_dir)
            clone_repo(repo_info.url, temp_dir_path)

            requirements_file = temp_dir_path / "requirements.txt"
            if not requirements_file.exists():
                raise HTTPException(
                    status_code=400,
                    detail="requirements.txt not found in repository root",
                )

            match = re.search(r"uvicorn\s+(\w+):", repo_info.buildCommand)
            if not match:
                raise HTTPException(
                    status_code=400,
                    detail="Invalid build command format. Expected 'uvicorn <module>:app'",
                )
            main_file = match.group(1)

            port_match = re.search(r"--port\s+(\d+)", repo_info.buildCommand)
            if not port_match:
                raise HTTPException(
                    status_code=400, detail="Port not found in build command"
                )
            port = port_match.group(1)

            root_dir_path = temp_dir_path / repo_info.rootDir
            if not (root_dir_path / f"{main_file}.py").exists():
                raise HTTPException(
                    status_code=400,
                    detail=f"{main_file}.py not found in specified root directory",
                )

            service_name = f"{user_name}-{repo_name}".lower()
            image_tag = f"{user_name}/{repo_name}:latest".lower()

            container_id, host_port = await deploy_with_docker_compose(
                temp_dir_path,
                service_name,
                image_tag,
                port,
                repo_info.envVars,
                repo_info.buildCommand,
            )

            instance_id = get_instance_id()
            if not instance_id:
                raise HTTPException(status_code=500, detail="Failed to get EC2 ID.")
            sg_id = get_instance_security_group(instance_id)
            if not sg_id:
                raise HTTPException(status_code=500, detail="Failed to get EC2 sg_id.")
            try:
                print(f"正在為安全組 {sg_id} 添加規則，端口為 {host_port}")
                add_security_group_rule(sg_id, int(host_port))
            except Exception as e:
                print(f"調用 add_security_group_rule 時發生錯誤: {e}")

            subdomain = f"{user_name}-{repo_name}".lower()
            target_group_arn = create_target_group(int(host_port), subdomain)
            register_target(target_group_arn, instance_id, int(host_port))
            create_listener_rule(target_group_arn, subdomain)

            full_domain = create_route53_record_for_alb(subdomain)

            background_tasks.add_task(delayed_cleanup, service_name, image_tag)

        return DeploymentResponse(
            data=DeploymentData(
                success=True,
                message="Repository deployed successfully",
                deploy_url=full_domain,
            )
        )

    except HTTPException as he:
        return {"data": {"error": f"Error: {he.detail}"}}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
