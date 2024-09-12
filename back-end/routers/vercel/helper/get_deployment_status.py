from datetime import datetime, timedelta
import requests
from fastapi import HTTPException
from utils.mysql import execute_query


def check_deployment_status(deployment):
    if deployment["status"] == "pending":
        url = deployment["route53_url"]
        if not url:
            return False

        return True

        # TODO:response.status_code == 200
        # try:
        #     response = requests.get(url, timeout=10)
        #     if response.status_code == 200:
        #         return True
        #     else:
        #         print(
        #             f"Deployment not ready yet. HTTP status code: {response.status_code}"
        #         )
        #         return False
        # except requests.RequestException as e:
        #     print(f"Error checking deployment status: {str(e)}")
        #     return False

    return False


async def get_deployment_status(deployment_id: int, db):
    deployment = execute_query(
        db,
        """
        SELECT id, status, route53_url, s3_url, cloudfront_url, s3_bucketname, 
               cloudfront_id, created_at
        FROM deployments WHERE id = %s
        """,
        (deployment_id,),
        fetch_method="fetchone",
    )

    if not deployment:
        raise HTTPException(status_code=404, detail="Deployment not found")

    if deployment["status"] == "pending":
        if check_deployment_status(deployment):
            execute_query(
                db,
                "UPDATE deployments SET status = %s WHERE id = %s",
                ("completed", deployment_id),
            )
            deployment["status"] = "completed"
        else:
            created_at = deployment["created_at"]
            if datetime.now() - created_at > timedelta(minutes=10):
                execute_query(
                    db,
                    "UPDATE deployments SET status = %s WHERE id = %s",
                    ("failed", deployment_id),
                )
                deployment["status"] = "failed"

    status_messages = {
        "validating": "Project validation passed, cloud deployment in progress",
        "deploying": "Cloud deployment in progress",
        "pending": "Cloud deployment completed, waiting for URL to take effect",
        "completed": "URL is effective, please visit",
        "failed": "Deployment failed or timed out",
    }

    response_data = {
        "status": deployment["status"],
        "message": status_messages.get(deployment["status"], "Unknown status"),
        "deploy_url": deployment["route53_url"],
        "s3_url": deployment["s3_url"],
        "cloudfront_url": deployment["cloudfront_url"],
        "s3_bucketname": deployment["s3_bucketname"],
        "cloudfront_id": deployment["cloudfront_id"],
        "created_at": deployment["created_at"].isoformat(),
        "elapsed_time": (datetime.now() - deployment["created_at"]).total_seconds(),
    }

    return {"data": response_data}
