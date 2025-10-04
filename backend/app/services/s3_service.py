import io

import boto3
from fastapi import HTTPException

from app.core.config import settings

s3_client = boto3.client(
    's3',
    endpoint_url=settings.R2_ENDPOINT_URL,
    aws_access_key_id=settings.R2_ACCESS_KEY_ID,
    aws_secret_access_key=settings.R2_SECRET_ACCESS_KEY,
    region_name='auto'
)

def upload_file_to_s3(file: io.BytesIO, file_key: str):
    try:
        s3_client.upload_fileobj(
            file,
            settings.R2_BUCKET_NAME,
            file_key
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not upload file: {e}")

def download_file_from_s3(file_key: str) -> io.BytesIO:
    try:
        in_memory_file = io.BytesIO()
        s3_client.download_fileobj(settings.R2_BUCKET_NAME, file_key, in_memory_file)
        in_memory_file.seek(0)
        return in_memory_file
    except s3_client.exceptions.NoSuchKey:
        raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error downloading file: {e}")