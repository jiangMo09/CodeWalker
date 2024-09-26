import os
import asyncio
from typing import Dict, Any
import redis.asyncio as redis
from utils.load_env import ELASTI_CACHE_URL
from utils.logger_api import setup_logger
from redis.asyncio.retry import Retry
from redis.backoff import ExponentialBackoff
from redis.exceptions import ConnectionError, TimeoutError, RedisError

logger = setup_logger("redis_client", "app.log")


def get_redis_config() -> tuple[str, Dict[str, Any]]:
    is_production = os.getenv("ENVIRONMENT") == "production"

    if is_production:
        redis_url = ELASTI_CACHE_URL
        if not redis_url.startswith("rediss://"):
            raise ValueError(
                "Production ELASTI_CACHE_URL must start with 'rediss://' for SSL connection"
            )

        return redis_url, {
            "encoding": "utf-8",
            "decode_responses": True,
            "ssl_cert_reqs": None,
            "socket_timeout": 5,
            "socket_connect_timeout": 5,
            "health_check_interval": 10,
            "retry_on_timeout": True,
            "max_connections": 10000,
        }

    return "redis://localhost", {
        "encoding": "utf-8",
        "decode_responses": True,
        "socket_timeout": 5,
        "socket_connect_timeout": 5,
    }


def initialize_redis_client() -> redis.Redis:
    redis_url, redis_options = get_redis_config()

    retry = Retry(ExponentialBackoff(), 3)

    try:
        client = redis.from_url(redis_url, **redis_options, retry=retry)
        logger.info(
            f"Redis client initialized successfully. URL: {'ElastiCache' if 'rediss://' in redis_url else 'localhost'}"
        )
        return client
    except redis.RedisError as e:
        logger.error(f"Error initializing Redis client: {e}")
        raise


async_redis_client = initialize_redis_client()


# https://github.com/redis/redis-py/issues/2773#issuecomment-1687671504
# when request is high, error "Connection closed by server." may happens.
# solved by setting retry & reinitializing client.
async def execute_redis_command(command, *args, **kwargs):
    max_retries = 3
    for attempt in range(max_retries):
        try:
            result = await command(*args, **kwargs)
            if result is None:
                raise ValueError("Command returned None")
            return result
        except (ConnectionError, TimeoutError, ValueError) as e:
            logger.error(
                f"Redis command failed (attempt {attempt + 1}/{max_retries}): {e}"
            )
            if attempt == max_retries - 1:
                logger.error("Max retries reached. Reinitializing Redis client.")
                global async_redis_client
                async_redis_client = initialize_redis_client()
                raise
            await asyncio.sleep(0.1 * (attempt + 1))
        except Exception as e:
            logger.error(f"Unexpected error during Redis operation: {e}")
            raise


async def get_redis_client():
    global async_redis_client
    try:
        await async_redis_client.ping()
    except RedisError:
        logger.info("Redis connection lost. Reinitializing.")
        async_redis_client = initialize_redis_client()
    return async_redis_client
