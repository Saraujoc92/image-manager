from datetime import datetime
import os
from fastapi import Request
from google.cloud import storage

import logger

image_bucket_name_env = os.getenv("IMAGE_UPLOAD_BUCKET_NAME")
if not image_bucket_name_env:
    raise ValueError("IMAGE_UPLOAD_BUCKET_NAME environment variable is not set.")
image_bucket_name: str = image_bucket_name_env


def _get_cloud_storage_client():
    """Create and return a Google Cloud Storage client."""
    try:
        client = storage.Client()
        return client
    except Exception as e:
        raise RuntimeError(f"Failed to create Google Cloud Storage client: {e}")


def _upload_file_to_bucket(
    file_path: str, file: bytes, request: Request, bucket_name: str
):
    """Uploads a file to the specified Google Cloud Storage bucket."""
    client = _get_cloud_storage_client()
    try:
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(file_path)
        blob.upload_from_string(file, content_type="application/octet-stream")
        logger.info(f"File uploaded to {file_path} in bucket {bucket_name}", request)
    except Exception as e:
        raise RuntimeError(f"Failed to upload file: {e}")


def upload_image_to_bucket(file_path: str, file: bytes, request: Request):
    return _upload_file_to_bucket(file_path, file, request, image_bucket_name)


def get_bucket_file_url(file_path: str) -> str:
    """Returns the public URL of a file in the Google Cloud Storage bucket."""
    client = _get_cloud_storage_client()
    try:
        bucket = client.bucket(image_bucket_name)
        blob = bucket.blob(file_path)
        if not blob.exists():
            raise FileNotFoundError(
                f"File {file_path} does not exist in bucket {image_bucket_name}."
            )
        return blob.public_url
    except Exception as e:
        raise RuntimeError(f"Failed to get file URL: {e}")


def upload_log(log: str, request: Request):
    logger_bucket_name = os.getenv("LOGGER_BUCKET_NAME")
    if not logger_bucket_name:
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = f"logs/{timestamp}.log"
    try:
        _upload_file_to_bucket(
            file_path, log.encode("utf-8"), request, logger_bucket_name
        )
    except Exception as e:
        raise RuntimeError(f"Failed to upload log file: {e}")
