from app.utils.graph import get_waveform_data, get_spectrogram_data, get_frequency_data, get_csd_data 
from app.utils.pipeline.processor import DecayAnalyzer, EnvelopeSmoother

def plot_waveform(signal, sr: int, num_points: int = 2000) -> dict[str, list[object]]:
    return get_waveform_data(signal, sr, num_points)

def plot_frequency_response(signal, sr: int, bands_per_oct: int) -> dict:
    return get_frequency_data(signal, sr, bands_per_oct)

def plot_spectrogram(signal, sr: int) -> dict:
    """
    Creates a spectrogram from a signal, intelligently truncating it first
    by analyzing its energy decay curve.

    This function implements a processing pipeline:
    1.  Calculates the smoothed energy envelope of the whole signal.
    2.  Uses the Lundeby algorithm to find the point where the signal's decay
        meets the noise floor (the crossover point).
    3.  Truncates the original signal at this crossover point.
    4.  Generates the spectrogram only for the acoustically relevant part of the signal.
    """
    # If the signal is too short to be processed, return an empty spectrogram
    if len(signal) < sr * 0.1:  # Example: require at least 100ms
        return get_spectrogram_data(signal, sr)

    # --- 1. SETUP THE PROCESSING PIPELINE ---
    smoother = EnvelopeSmoother(fs=sr)
    decay_analyzer = DecayAnalyzer(fs=sr)

    # --- 2. PREPARE DATA FOR THE PIPELINE ---
    pipeline_data = {'filtered_signals': {'broadband': signal}}

    # --- 3. EXECUTE THE PIPELINE ---
    try:
        pipeline_data = smoother.process(pipeline_data)

        pipeline_data = decay_analyzer._lundeby_crossover(pipeline_data['envelopes']['broadband'])

    except Exception:
        return get_spectrogram_data(signal, sr)


    # --- 4. EXTRACT THE TRUNCATION POINT ---
    try:
        crossover_index = pipeline_data['crossover_index']

        if not (0 < crossover_index <= len(signal)):
            crossover_index = len(signal)

    except (KeyError, IndexError):
        crossover_index = len(signal)

    # --- 5. TRUNCATE SIGNAL AND GENERATE SPECTROGRAM ---
    truncated_signal = signal[:crossover_index]

    return get_spectrogram_data(truncated_signal, sr)

def plot_csd(signal, sr: int, bands_per_oct: int) -> dict:
    """
    Creates a Cumulative Spectral Decay (CSD) plot from a signal.
    """
    if len(signal) < sr * 0.1:  
        return get_csd_data(signal, sr, bands_per_oct=bands_per_oct)

    # If the signal is too short to be processed, return an empty CSD
    if len(signal) < sr * 0.1:  # Example: require at least 100ms
        return get_csd_data(signal, sr, bands_per_oct=bands_per_oct)

    # --- 1. SETUP THE PROCESSING PIPELINE ---
    smoother = EnvelopeSmoother(fs=sr)
    decay_analyzer = DecayAnalyzer(fs=sr)

    # --- 2. PREPARE DATA FOR THE PIPELINE ---
    pipeline_data = {'filtered_signals': {'broadband': signal}}

    # --- 3. EXECUTE THE PIPELINE ---

    # --- 1. SETUP THE PROCESSING PIPELINE ---
    smoother = EnvelopeSmoother(fs=sr)
    decay_analyzer = DecayAnalyzer(fs=sr)

    # --- 2. PREPARE DATA FOR THE PIPELINE ---
    pipeline_data = {'filtered_signals': {'broadband': signal}}

    # --- 3. EXECUTE THE PIPELINE ---
    try:
        pipeline_data = smoother.process(pipeline_data)

        pipeline_data = decay_analyzer._lundeby_crossover(pipeline_data['envelopes']['broadband'])

    except Exception:
        return get_csd_data(signal, sr, bands_per_oct=bands_per_oct)


    # --- 4. EXTRACT THE TRUNCATION POINT ---
    try:
        crossover_index = pipeline_data['crossover_index']

        if not (0 < crossover_index <= len(signal)):
            crossover_index = len(signal)

    except (KeyError, IndexError):
        crossover_index = len(signal)

    # --- 5. TRUNCATE SIGNAL AND GENERATE CSD ---
    truncated_signal = signal[:crossover_index]

    return get_csd_data(truncated_signal, sr, bands_per_oct=bands_per_oct)