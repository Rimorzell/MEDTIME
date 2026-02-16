import logging
import uuid

import boto3
from botocore.exceptions import BotoCoreError, ClientError

from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


s3_client = boto3.client(
    "s3",
    aws_access_key_id=settings.aws_access_key_id,
    aws_secret_access_key=settings.aws_secret_access_key,
    region_name=settings.s3_region,
)


def generate_presigned_upload_url(file_name: str, file_type: str) -> str:
    file_key = f"uploads/{uuid.uuid4()}-{file_name}"
    return s3_client.generate_presigned_url(
        "put_object",
        Params={"Bucket": settings.s3_bucket_name, "Key": file_key, "ContentType": file_type},
        ExpiresIn=3600,
    )


def generate_presigned_download_url(file_key: str) -> str:
    return s3_client.generate_presigned_url(
        "get_object", Params={"Bucket": settings.s3_bucket_name, "Key": file_key}, ExpiresIn=3600
    )


def delete_file(file_key: str) -> bool:
    try:
        s3_client.delete_object(Bucket=settings.s3_bucket_name, Key=file_key)
        return True
    except (BotoCoreError, ClientError):
        logger.exception("Failed to delete file from S3", extra={"file_key": file_key})
        return False
