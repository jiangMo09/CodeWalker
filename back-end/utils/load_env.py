from dotenv import load_dotenv
import os

load_dotenv()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
MY_IPS = os.getenv("MY_IPS")
HOST = os.getenv("DB_HOST")
USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")
NAME = os.getenv("DB_NAME")
SQS_URL = os.getenv("SQS_URL")
REDIS_URL = os.getenv("REDIS_URL")
ECR_REGISTRY = os.getenv("ECR_REGISTRY")
ENVIRONMENT = os.getenv("ENVIRONMENT")
S3_BUCKET = os.getenv("S3_BUCKET")
S3_FOLDER = os.getenv("S3_FOLDER")
CLOUDFRONT_URL = os.getenv("CLOUDFRONT_URL")
