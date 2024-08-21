from dotenv import load_dotenv
import os

load_dotenv()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
MY_IPS = os.getenv("MY_IPS")
HOST = os.getenv("DB_HOST")
USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")
NAME = os.getenv("DB_NAME")

ENVIRONMENT = os.getenv("ENVIRONMENT")

AWS_ACCOUNT_ID = os.getenv("AWS_ACCOUNT_ID")
AWS_BUCKET_REGION = os.getenv("AWS_BUCKET_REGION")

ECR_REGISTRY = os.getenv("ECR_REGISTRY")

SQS_URL = os.getenv("SQS_URL")

S3_BUCKET = os.getenv("S3_BUCKET")
S3_FOLDER = os.getenv("S3_FOLDER")
S3_WEBSITE_ENDPOINT = os.getenv("S3_WEBSITE_ENDPOINT")
S3_HOSTED_ZONE_ID = os.getenv("S3_HOSTED_ZONE_ID")

ROUTE53_HOSTED_ZONE_ID = os.getenv("ROUTE53_HOSTED_ZONE_ID")

CLOUDFRONT_URL = os.getenv("CLOUDFRONT_URL")
CLOUDFRONT_OAC_ID = os.getenv("CLOUDFRONT_OAC_ID")

ELASTI_CACHE_URL = os.getenv("ELASTI_CACHE_URL")
