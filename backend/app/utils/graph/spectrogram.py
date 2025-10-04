import numpy as np
from scipy import signal
from scipy.interpolate import interp1d, RectBivariateSpline
from scipy.ndimage import gaussian_filter

def get_spectrogram_data(y: np.ndarray, sr: int) -> dict:
    """
    Calculates and resamples the spectrogram data onto a logarithmic frequency scale.

    Args:
        y (np.ndarray): The time-domain audio signal.
        sr (int): The sample rate.

    Returns:
        dict: A dictionary containing the log-resampled spectrogram data.
    """
    # 1. Calculate the original linear spectrogram
    nperseg = int(0.046 * sr)  # Use a larger window for better frequency resolution (e.g., 46ms)
    noverlap = nperseg // 2     # 50% overlap

    f_linear, t, Sxx = signal.spectrogram(
        y, 
        fs=sr, 
        nperseg=nperseg, 
        noverlap=noverlap
    )

    # 2. Define the target logarithmic frequency scale
    min_freq = 20
    max_freq = 20000
    # Create a logarithmically spaced grid of frequencies
    num_log_bins = 512 # More bins for a smoother visual result
    f_log = np.logspace(np.log10(min_freq), np.log10(max_freq), num=num_log_bins)

    # 3. Resample the spectrogram data for each time slice
    Sxx_log = np.zeros((num_log_bins, len(t)))

    for i in range(len(t)):
        # Create an interpolation function for the current time slice
        # This maps linear frequencies to their power values
        interp_func = interp1d(
            f_linear,           # Original X-values (linear frequencies)
            Sxx[:, i],          # Original Y-values (power at this time slice)
            kind='linear',      # Use linear interpolation
            bounds_error=False, # Don't throw errors for out-of-bounds values
            fill_value=0.0      # Fill out-of-bounds with 0
        )
        
        # Apply the interpolation to our new log-frequency axis
        Sxx_log[:, i] = interp_func(f_log)

    # 4. Convert power to dB, clip, and normalize
    Sxx_db = 10 * np.log10(Sxx_log + 1e-10)
    Sxx_db -= np.max(Sxx_db) 
    Sxx_clipped = np.clip(Sxx_db, -80, None)

    # 5. UPSAMPLE VIA 2D INTERPOLATION
    # Define the desired final resolution. A factor of 3-4x is usually great.
    time_upsample_factor = 2
    freq_upsample_factor = 2 

    num_hires_t = len(t) * time_upsample_factor
    t_hires = np.linspace(t.min(), t.max(), num_hires_t)

    num_hires_f = len(f_log) * freq_upsample_factor
    f_hires = np.logspace(np.log10(f_log.min()), np.log10(f_log.max()), num_hires_f)

    # Create the interpolation function. Note that Sxx is (freq, time),
    # so we use f_log and t as the axes.
    # We must transpose Sxx_clipped to match the (t, f) axis order.
    interpolator = RectBivariateSpline(t, f_log, Sxx_clipped.T)

    # Evaluate the interpolator on the new high-resolution time axis.
    # The result will be (t_hires, f_log), so we transpose it back.
    Sxx_hires = interpolator(t_hires, f_hires).T

    # 6. (Optional) APPLY FINAL GENTLE SMOOTHING
    # A small sigma on the high-res data gives a polished look.
    Sxx_smoothed = gaussian_filter(Sxx_clipped, sigma=1.5)

    # Get final min/max for the color axis
    max_db = np.max(Sxx_smoothed)
    min_db = np.min(Sxx_smoothed)

    return {
        "Sxx": Sxx_smoothed.tolist(),
        "f": f_log.tolist(), # Send the new log frequencies
        "t": t.tolist(),
        "min_db": min_db,
        "max_db": max_db
    }