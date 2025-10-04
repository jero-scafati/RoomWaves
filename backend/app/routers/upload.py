import os
import uuid

from fastapi import APIRouter, UploadFile, File, HTTPException

from app.core.config import settings
from app.services.s3_service import upload_file_to_s3

router = APIRouter()

@router.post("/upload")
async def upload_audio_file(file: UploadFile = File(...)):
    if file.content_type not in settings.ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"File type not allowed. Please upload one of: {', '.join(settings.ALLOWED_MIME_TYPES)}"
        )

    file.file.seek(0, os.SEEK_END)
    file_size = file.file.tell()
    if file_size > settings.MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=413,
            detail=f"File size exceeds the {settings.MAX_FILE_SIZE_MB}MB limit."
        )
    file.file.seek(0)

    _, extension = os.path.splitext(file.filename)
    unique_filename = f"{uuid.uuid4()}{extension}"
    file_key = f"uploads/{unique_filename}"
    
    upload_file_to_s3(file.file, file_key)
    
    return {
        "status": "upload successful",
        "filename": unique_filename,
        "path": file_key
    }