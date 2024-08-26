import tempfile
from typing import List
import os
import re
from pathlib import Path
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from .helper.github_repo import clone_repo, extract_github_info, is_public_repo
from .helper.docker import deploy_with_docker_compose, delayed_cleanup

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
async def deploy_fast_api(repo_info: RepoInfo):
    try:
        if not is_public_repo(repo_info.url):
            raise HTTPException(status_code=400, detail="Repository is not public")

        user_name, repo_name = extract_github_info(repo_info.url)
        if not repo_name:
            raise HTTPException(
                status_code=400,
                detail="Repository is not github repo, can't find repo_name",
            )

        with tempfile.TemporaryDirectory() as temp_dir:
            clone_repo(repo_info.url, temp_dir)

            if not os.path.exists(os.path.join(temp_dir, "requirements.txt")):
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

            root_dir_path = Path(temp_dir) / repo_info.rootDir
            if not (root_dir_path / f"{main_file}.py").exists():
                raise HTTPException(
                    status_code=400,
                    detail=f"{main_file}.py not found in specified root directory",
                )

            service_name = f"{user_name}-{repo_name}".lower()
            image_tag = f"{user_name}/{repo_name}:latest".lower()

            service_name, image_tag = deploy_with_docker_compose(
                temp_dir,
                service_name,
                image_tag,
                port,
                repo_info.envVars,
                repo_info.buildCommand,
            )

            delayed_cleanup(service_name, image_tag)
            deploy_url = f"http://localhost:{port}"

        return DeploymentResponse(
            data=DeploymentData(
                success=True,
                message="Repository deployed successfully",
                deploy_url=deploy_url,
            )
        )

    except HTTPException as he:
        return {"data": {"error": f"Error1: {he.detail}"}}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
