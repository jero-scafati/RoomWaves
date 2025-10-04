from fastapi import APIRouter
from enum import Enum
import librosa

from app.services.s3_service import download_file_from_s3
from app.services.plotting import plot_waveform, plot_frequency_response, plot_spectrogram, plot_csd

router = APIRouter()

class BandsPerOctave(int, Enum):
    one = 1
    three = 3
    six = 6
    twelve = 12
    twenty_four = 24
    forty_eight = 48

@router.get("/plot/{filename}")
async def get_plot_data(filename: str):
    file_key = f"uploads/{filename}"
    
    file_stream = download_file_from_s3(file_key)
    y, sr = librosa.load(file_stream, sr=None, mono=True)
    plot_data = plot_waveform(y, sr)
    
    return plot_data

@router.get("/spectrogram/{filename}")
async def get_spectrogram_data(filename: str):
    file_key = f"uploads/{filename}"
    file_stream = download_file_from_s3(file_key)

    y, sr = librosa.load(file_stream, sr=None, mono=True)
    plot_data = plot_spectrogram(y, sr)
    
    return plot_data

@router.get("/csd/{filename}")
async def get_csd_data(
    filename: str,
    bands: BandsPerOctave = BandsPerOctave.twenty_four):
    file_key = f"uploads/{filename}"
    file_stream = download_file_from_s3(file_key)

    y, sr = librosa.load(file_stream, sr=None, mono=True)
    plot_data = plot_csd(y, sr, bands_per_oct=bands.value)

    return plot_data

@router.get("/frequency-response/{filename}")
async def get_frequency_response_data(
    filename: str,
    bands: BandsPerOctave = BandsPerOctave.twenty_four):
    """
    Provides data for frequency response plot.
    - **filename**: The name of the uploaded audio file.
    - **bands**: The number of bands per octave for smoothing.
    """
    file_key = f"uploads/{filename}"
    file_stream = download_file_from_s3(file_key)

    y, sr = librosa.load(file_stream, sr=None, mono=True)

    frequency_data = plot_frequency_response(y, sr, bands_per_oct=bands.value)

    return frequency_data