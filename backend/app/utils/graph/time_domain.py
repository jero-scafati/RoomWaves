def get_waveform_data(signal, sr: int, num_points: int = 2000) -> dict[str, list[object]]:
    import librosa
    import numpy as np
    """
    Downsamples a signal and prepares its time-domain data (labels and amplitude)
    for plotting in a JSON-compatible format.

    Args:
        signal (np.ndarray): The time-domain audio signal (impulse response).
        sr (int): The sample rate of the signal.
        num_points (int): The maximum number of data points to return for plotting.

    Returns:
        dict[str, list[object]]: A dictionary with 'labels' (time in seconds) and
                              'data' (amplitude values).
    """
    if len(signal) > num_points:
        step = len(signal) // num_points
        signal_plot = signal[::step]
    else:
        signal_plot = signal

    duration = librosa.get_duration(y=signal, sr=sr)
    time_labels = np.linspace(0, duration, len(signal_plot)).tolist()

    amplitude_data = signal_plot.tolist()

    return {"labels": time_labels, "data": amplitude_data}