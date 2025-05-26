import os
from fastapi import Request
from google.cloud import storage

import logger

bucket_name = os.getenv("BUCKET_NAME")
if not bucket_name:
    raise ValueError("BUCKET_NAME environment variable is not set.")


def _get_cloud_storage_client():
    """Create and return a Google Cloud Storage client."""
    try:
        client = storage.Client()
        return client
    except Exception as e:
        raise RuntimeError(f"Failed to create Google Cloud Storage client: {e}")


def upload_file_to_bucket(file_path: str, file: bytes, request: Request):
    """Uploads a file to the specified Google Cloud Storage bucket."""
    client = _get_cloud_storage_client()
    try:
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(file_path)
        blob.upload_from_string(file, content_type="application/octet-stream")
        logger.info(f"File uploaded to {file_path} in bucket {bucket_name}", request)
    except Exception as e:
        raise RuntimeError(f"Failed to upload file: {e}")


def get_bucket_file_url(file_path: str) -> str:
    """Returns the public URL of a file in the Google Cloud Storage bucket."""
    client = _get_cloud_storage_client()
    try:
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(file_path)
        if not blob.exists():
            raise FileNotFoundError(
                f"File {file_path} does not exist in bucket {bucket_name}."
            )
        return blob.public_url
    except Exception as e:
        raise RuntimeError(f"Failed to get file URL: {e}")
