from fastapi import APIRouter

from app.services.signal_service import generate_sweep_signals

router = APIRouter()

@router.get("/signal")
async def get_signal(duration: float = 10,
                     f_inf: int = 20,
                     f_sup: int = 20000,
                     fs: int = 44100):
    return generate_sweep_signals(
        duration=duration,
        f_inf=f_inf,
        f_sup=f_sup,
        fs=fs
    )
