from enum import Enum

from fastapi import APIRouter
import librosa

from app.services.get_parameters import process_impulse_response
from app.services.s3_service import download_file_from_s3

router = APIRouter()

class BandsPerOctave(int, Enum):
    one = 1
    three = 3

from app.services.get_parameters import process_impulse_response


router = APIRouter()

@router.get("/parameters/{filename}")
async def get_acoustic_parameters(
    filename: str,
    bands: BandsPerOctave = BandsPerOctave.one):
    
    file_key = f"uploads/{filename}"
    
    file_stream = download_file_from_s3(file_key)
    y, fs = librosa.load(file_stream, sr=None, mono=True)
    
    results = process_impulse_response(
        ri=y,
        fs=fs,
        filter_type=bands,
        smoothing_window_ms=10
    )
    
    return results