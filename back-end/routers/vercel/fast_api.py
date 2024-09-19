import tempfile
import re
from typing import List
from pathlib import Path
from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends, Request
from pydantic import BaseModel
import shortuuid
import jwt

from utils.mysql import get_db, execute_query, get_db_connection
from utils.load_env import JWT_SECRET_KEY
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
from .helper.get_deployment_status import get_deployment_status

router = APIRouter()


class RepoInfo(BaseModel):
    url: str
    deploymentType: str
    storageTypes: List[str]
    buildCommand: str
    envVars: List[dict]
    rootDir: str


async def deploy_process(
    deployment_id: int, repo_info: RepoInfo, background_tasks: BackgroundTasks
):
    connection = None
    try:
        connection = get_db_connection()

        execute_query(
            connection,
            "UPDATE deployments SET status = %s WHERE id = %s",
            ("deploying", deployment_id),
        )

        user_name, repo_name = extract_github_info(repo_info.url)
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
                raise ValueError("Port not found in build command")
            port = port_match.group(1)

            root_dir_path = temp_dir_path / repo_info.rootDir
            if not (root_dir_path / f"{main_file}.py").exists():
                raise ValueError(
                    f"{main_file}.py not found in specified root directory"
                )

            short_id = shortuuid.uuid()[:4]
            service_name = f"{repo_name}-{short_id}".lower()
            image_tag = f"{repo_name}/{short_id}:latest".lower()

            container_id, host_port = await deploy_with_docker_compose(
                temp_dir_path,
                service_name,
                image_tag,
                port,
                repo_info.envVars,
                repo_info.buildCommand,
                repo_info.storageTypes,
            )

            instance_id = get_instance_id()
            if not instance_id:
                raise HTTPException(status_code=500, detail="Failed to get EC2 ID.")

            sg_id = get_instance_security_group(instance_id)
            if not sg_id:
                raise HTTPException(status_code=500, detail="Failed to get EC2 sg_id.")

            add_security_group_rule(sg_id, int(host_port))

            subdomain = f"{repo_name}-{short_id}".lower()
            target_group_arn = create_target_group(int(host_port), subdomain)
            register_target(target_group_arn, instance_id, int(host_port))
            create_listener_rule(target_group_arn, subdomain)

            deploy_url = create_route53_record_for_alb(subdomain)

        execute_query(
            connection,
            """
            UPDATE deployments 
            SET status = %s, route53_url = %s
            WHERE id = %s
            """,
            (
                "pending",
                deploy_url,
                deployment_id,
            ),
        )

        background_tasks.add_task(
            delayed_cleanup, service_name, image_tag, delay_minutes=60
        )

    except HTTPException as he:
        if connection:
            execute_query(
                connection,
                "UPDATE deployments SET status = %s WHERE id = %s",
                ("failed", deployment_id),
            )
        print(f"Deployment failed: {he.detail}")
        raise
    except Exception as e:
        if connection:
            execute_query(
                connection,
                "UPDATE deployments SET status = %s WHERE id = %s",
                ("failed", deployment_id),
            )
        print(f"Deployment failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    finally:
        if connection:
            connection.close()


@router.post("/deploy/fast_api")
async def post_fast_api(
    request: Request,
    repo_info: RepoInfo,
    background_tasks: BackgroundTasks,
    db=Depends(get_db),
):
    try:
        auth_token = request.headers.get("authToken")
        payload = jwt.decode(auth_token, JWT_SECRET_KEY, algorithms=["HS256"])

        if not payload:
            raise HTTPException(status_code=403, detail="Please Login")
        user_id = payload["id"]

        if not is_public_repo(repo_info.url):
            raise HTTPException(status_code=400, detail="Repository is not public")

        if repo_info.deploymentType != "fastApi":
            raise HTTPException(status_code=400, detail="Invalid deployment type")

        user_name, repo_name = extract_github_info(repo_info.url)
        if not repo_name:
            raise HTTPException(
                status_code=400,
                detail="Invalid GitHub repository URL, can't find repo_name.",
            )

        execute_query(
            db,
            """
            INSERT INTO deployments 
            (user_id, deployment_type, github_repo_url, github_repo_name, github_repo_owner, status) 
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                user_id,
                repo_info.deploymentType,
                repo_info.url,
                repo_name,
                user_name,
                "validating",
            ),
        )

        result = execute_query(db, "SELECT LAST_INSERT_ID()", fetch_method="fetchone")

        deployment_id = result["LAST_INSERT_ID()"]
        if not deployment_id:
            raise HTTPException(
                status_code=500, detail="Failed to create deployment record"
            )

        background_tasks.add_task(
            deploy_process, deployment_id, repo_info, background_tasks
        )

        return {
            "data": {
                "success": True,
                "message": "Deployment process started",
                "deployment_id": deployment_id,
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@router.get("/deploy/status/{deployment_id}")
async def get_deployment_status_route(deployment_id: int, db=Depends(get_db)):
    return await get_deployment_status(deployment_id, db)
