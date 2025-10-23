def get_csd_data(signal, sr: int, bands_per_oct: int) -> dict:
    import numpy as np
    from scipy.interpolate import interp1d
    from scipy.signal import windows
    from scipy.ndimage import gaussian_filter
    """
    Performs Cumulative Spectral Decay (CSD) analysis on an impulse response.
    
    Args:
        signal: The impulse response signal
        sr: Sample rate in Hz
        
    Returns:
        Dictionary containing waterfall plot data
    """
    # Configuration Parameters
    fft_size = 8192  # Power of 2 for FFT
    time_step_ms = 1.0  # Time resolution for each slice in milliseconds
    num_slices = 150  # Total number of decay slices
    dynamic_range_db = 60  # Visual depth of the plot in dB
    min_freq = 20
    max_freq = 20000
    

    hop_length = fft_size // 4 
    # Create Hann window
    window = windows.hann(fft_size)
    
    # Core CSD Loop
    num_slices = (len(signal) - fft_size) // hop_length + 1
    slices = []
    for i in range(num_slices):
        start_index = i * hop_length
        
        # Check if we have enough samples
        if start_index + fft_size > len(signal):
            break
            
        # Extract current chunk
        chunk = signal[start_index:start_index + fft_size]
        
        # Apply window
        windowed_chunk = chunk * window
        
        # Compute FFT
        fft_result = np.fft.rfft(windowed_chunk, n=fft_size)
        
        # Calculate magnitude in dB
        magnitude = np.abs(fft_result)
        # Avoid log of zero
        magnitude[magnitude == 0] = 1e-10
        magnitude_db = 20 * np.log10(magnitude)
        
        slices.append(magnitude_db)
    
    # Update num_slices to actual number of slices computed
    num_slices_actual = len(slices)
    
    # Frequency Axis Generation
    f_linear = np.fft.rfftfreq(fft_size, 1 / sr)
    f_log = np.logspace(np.log10(min_freq), np.log10(max_freq), num=1024)
    
    # Post-Processing (Smoothing and Resampling)
    Sxx_log_smoothed = np.zeros((num_slices_actual, len(f_log)))
    
    for slice_idx, db_slice in enumerate(slices):
        # Apply Fractional-Octave Smoothing
        smoothed_slice = fractional_octave_smoothing(
            db_slice, f_linear, bands_per_oct
        )
        
        # Resample to logarithmic axis
        # Create interpolation function
        interp_func = interp1d(
            f_linear,
            smoothed_slice,
            kind='linear',
            bounds_error=False,
            fill_value=smoothed_slice[0]  # Use first value for out-of-bounds
        )
        
        # Apply interpolation to log frequency axis
        Sxx_log_smoothed[slice_idx, :] = interp_func(f_log)
    
    # Normalization and Clipping
    # Find absolute maximum
    max_value = np.max(Sxx_log_smoothed)
    
    # Normalize so highest peak is at 0 dB
    Sxx_normalized = Sxx_log_smoothed - max_value
    
    # Clip to dynamic range
    Sxx_clipped = np.clip(Sxx_normalized, -dynamic_range_db, 0)
    Sxx_gaussian = gaussian_filter(Sxx_clipped, sigma=1.5)
    # Create time axis (in seconds)
    t = np.arange(num_slices_actual) * time_step_ms / 1000.0
    
    
    # Return data structure
    return {
        "Sxx": Sxx_gaussian.T.tolist(),  # Transpose to have frequency as first dimension
        "f": f_log.tolist(),
        "t": t.tolist(),
        "min_db": -dynamic_range_db,
        "max_db": 0
    }


def fractional_octave_smoothing(spectrum_db, frequencies, fraction):
    import numpy as np
    
    octave_ratio = 2 ** (1 / fraction)
    
    # Initialize smoothed spectrum
    smoothed = np.zeros_like(spectrum_db)
    
    # Skip DC and very low frequencies
    start_idx = np.where(frequencies >= 20)[0]
    if len(start_idx) == 0:
        return spectrum_db
    start_idx = start_idx[0]
    
    # Apply smoothing
    for i in range(start_idx, len(frequencies)):
        f_center = frequencies[i]
        
        # Calculate band edges
        f_lower = f_center / np.sqrt(octave_ratio)
        f_upper = f_center * np.sqrt(octave_ratio)
        
        # Find indices within band
        band_mask = (frequencies >= f_lower) & (frequencies <= f_upper)
        
        if np.any(band_mask):
            # Average values within the band
            smoothed[i] = np.mean(spectrum_db[band_mask])
        else:
            smoothed[i] = spectrum_db[i]
    
    # Copy unsmoothed low frequencies
    smoothed[:start_idx] = spectrum_db[:start_idx]
    
    return smoothed