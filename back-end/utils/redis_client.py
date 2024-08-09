import os
import redis.asyncio as redis
from utils.load_env import REDIS_URL
from utils.logger_api import setup_logger

logger = setup_logger("redis_client", "app.log")

is_production = os.getenv("ENVIRONMENT") == "production"
if is_production:
    redis_url = REDIS_URL
    if not redis_url.startswith("rediss://"):
        logger.error(
            "Production REDIS_URL must start with 'rediss://' for SSL connection"
        )
        raise ValueError(
            "Production REDIS_URL must start with 'rediss://' for SSL connection"
        )

    redis_options = {
        "encoding": "utf-8",
        "decode_responses": True,
        "ssl_cert_reqs": None,
    }
else:
    redis_url = "redis://localhost"
    redis_options = {"encoding": "utf-8", "decode_responses": True}

try:
    async_redis_client = redis.from_url(redis_url, **redis_options)
    logger.info(
        f"Redis client initialized successfully. URL: {'ElastiCache' if is_production else 'localhost'}"
    )
except redis.RedisError as e:
    logger.error(f"Error initializing Redis client: {e}")
    raise
