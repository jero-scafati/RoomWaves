import numpy as np
import warnings

def calculate_snr(
    ri: np.ndarray,
    noise_tail_percentage: float = 0.2
) -> float:
    """
    Calculate the Signal-to-Noise Ratio (SNR) of an impulse response.
    
    Args:
        ri: Impulse response array
        noise_tail_percentage: Percentage of signal tail to consider as noise (default 0.2 = 20%)
    
    Returns:
        SNR in dB, or None if calculation fails
    """
    if ri is None or len(ri) == 0:
        warnings.warn("Empty impulse response. Cannot calculate SNR.")
        return None

    peak_signal_amplitude = np.max(np.abs(ri))

    if peak_signal_amplitude == 0:
        return None

    num_samples = len(ri)
    noise_start_index = int(num_samples * (1 - noise_tail_percentage))
    noise_tail = ri[noise_start_index:]

    if len(noise_tail) == 0:
        warnings.warn("Signal too short to estimate noise tail. Cannot calculate SNR.")
        return None

    noise_level_rms = np.sqrt(np.mean(noise_tail**2))

    if noise_level_rms == 0:
        return float('inf')
    
    snr_db = float(20 * np.log10(peak_signal_amplitude / noise_level_rms))
    return snr_db
