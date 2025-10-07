import io

import boto3
from fastapi import HTTPException

from app.core.config import settings

from botocore.config import Config

s3_client = boto3.client(
    's3',
    endpoint_url=settings.R2_ENDPOINT_URL,
    aws_access_key_id=settings.R2_ACCESS_KEY_ID,
    aws_secret_access_key=settings.R2_SECRET_ACCESS_KEY,
    region_name='auto',
    config=Config(signature_version='s3v4')
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

def generate_presigned_url(file_key: str, expiration: int = 3600) -> str:
    """
    Generate a presigned URL for downloading a file from S3/R2.
    
    Args:
        file_key: The S3 key of the file
        expiration: URL expiration time in seconds (default: 1 hour)
    
    Returns:
        A presigned URL string
    """
    try:
        # First check if file exists
        s3_client.head_object(Bucket=settings.R2_BUCKET_NAME, Key=file_key)
        
        # Generate presigned URL
        presigned_url = s3_client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': settings.R2_BUCKET_NAME,
                'Key': file_key
            },
            ExpiresIn=expiration
        )
        return presigned_url
    except s3_client.exceptions.NoSuchKey:
        raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating presigned URL: {e}")