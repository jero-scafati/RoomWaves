from fastapi import APIRouter
import librosa

from app.services.get_snr import calculate_snr
from app.services.s3_service import download_file_from_s3

router = APIRouter()

@router.get("/snr/{filename:path}")
async def get_snr(filename: str):
    """
    Calculate the Signal-to-Noise Ratio (SNR) of an audio file.
    This is a lightweight endpoint that only calculates SNR without full acoustic analysis.
    """
    file_key = filename
    
    file_stream = download_file_from_s3(file_key)
    y, fs = librosa.load(file_stream, sr=None, mono=True)
    
    snr_db = calculate_snr(y)
    
    return {"snr_db": snr_db}
