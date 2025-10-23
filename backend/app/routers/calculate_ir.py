import os
import uuid
import io

from fastapi import APIRouter, UploadFile, File, HTTPException
import librosa
import soundfile as sf

from app.core.config import settings
from app.services.s3_service import upload_file_to_s3
from app.utils.signals.signals import get_ir_from_deconvolution

router = APIRouter()

@router.post("/calculate-ir")
async def calculate_ir(
    recorded_sweep: UploadFile = File(...),
    inverse_filter: UploadFile = File(...),
    start_margin_ms: float = 20.0,
    duration_factor: float = 4.0
):
    """
    Calculate an Impulse Response from a recorded sweep and inverse filter.
    
    Args:
        recorded_sweep: The recorded sweep signal (audio file)
        inverse_filter: The inverse filter signal (audio file)
        start_margin_ms: Milliseconds before peak to start trimming (default: 20.0)
        duration_factor: IR duration as multiple of estimated T60 (default: 4.0)
    
    Returns:
        A dictionary with the path to the uploaded IR file
    """
    # Validate file types
    if recorded_sweep.content_type not in settings.ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Recorded sweep file type not allowed. Please upload one of: {', '.join(settings.ALLOWED_MIME_TYPES)}"
        )
    
    if inverse_filter.content_type not in settings.ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Inverse filter file type not allowed. Please upload one of: {', '.join(settings.ALLOWED_MIME_TYPES)}"
        )
    
    try:
        # Load audio files
        sweep_audio, sweep_fs = librosa.load(recorded_sweep.file, sr=None, mono=True)
        filter_audio, filter_fs = librosa.load(inverse_filter.file, sr=None, mono=True)
        
        # Check if sample rates match
        if sweep_fs != filter_fs:
            raise HTTPException(
                status_code=400,
                detail=f"Sample rates must match. Recorded sweep: {sweep_fs} Hz, Inverse filter: {filter_fs} Hz"
            )
        
        ir_result = get_ir_from_deconvolution(
            recording=sweep_audio,
            inverse_filter=filter_audio,
            fs=sweep_fs,
            start_margin_ms=start_margin_ms,
            duration_factor=duration_factor
        )
        
        if ir_result is None:
            raise HTTPException(
                status_code=500,
                detail="Failed to calculate IR. Please check your input files."
            )
        
        # Convert to WAV in memory
        wav_buffer = io.BytesIO()
        sf.write(
            wav_buffer,
            ir_result['audio_data'],
            ir_result['fs'],
            format='WAV',
            subtype='PCM_16'
        )
        wav_buffer.seek(0)
        
        # Generate S3 key and upload
        unique_filename = f"calculated_ir_{uuid.uuid4()}.wav"
        file_key = f"uploads/{unique_filename}"
        
        upload_file_to_s3(wav_buffer, file_key)
        
        return {
            "status": "IR calculation successful",
            "filename": unique_filename,
            "path": file_key,
            "sample_rate": ir_result['fs'],
            "duration_samples": len(ir_result['audio_data'])
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing files: {str(e)}"
        )
