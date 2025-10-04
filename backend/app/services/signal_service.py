from app.utils.signals.signals import generar_sweep_inverse, wav_to_b64


def generate_sweep_signals(
    duration: float,
    f_inf: int,
    f_sup: int,
    fs: int
) -> dict:
    """
    Generates sweep and inverse sweep signals with their base64 encoded audio data.
    
    Parameters
    ----------
    duration : int
        Duration of the sweep in seconds.
    f_inf : int
        Lower frequency bound in Hz.
    f_sup : int
        Upper frequency bound in Hz.
    fs : int
        Sampling frequency in Hz.
    
    Returns
    -------
    dict
        Dictionary containing base64 encoded audio data and filenames for both
        sweep and inverse sweep signals.
    """
    sweep, inverse, fs = generar_sweep_inverse(duration, fs, f_inf, f_sup)
    
    sweep_b64 = wav_to_b64(sweep, fs)
    inverse_b64 = wav_to_b64(inverse, fs)

    return {
        "audio_sweep_b64": sweep_b64,
        "audio_inverse_b64": inverse_b64,
        "filename_sweep": f'sweep_{duration:.1f}s_{int(f_inf)}-{int(f_sup)}.wav',
        "filename_inverse": f'inverse_{duration:.1f}s_{int(f_inf)}-{int(f_sup)}.wav'
    }
