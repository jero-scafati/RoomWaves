def get_envelope_db_data(signal, sr: int, num_points: int = 2000, min_db: float = -70.0) -> dict[str, list[object]]:
    import librosa
    import numpy as np
    from app.utils.pipeline.helpers import to_db_scale
    
    envelope = np.abs(signal)
    
    envelope_db = to_db_scale(envelope)
    envelope_db_clipped = np.clip(envelope_db, min_db, None)
    
    if len(envelope_db_clipped) > num_points:
        step = len(envelope_db_clipped) // num_points
        envelope_plot = envelope_db_clipped[::step]
    else:
        envelope_plot = envelope_db_clipped
    
    duration = librosa.get_duration(y=signal, sr=sr)
    time_labels = np.linspace(0, duration, len(envelope_plot)).tolist()
    
    amplitude_data = envelope_plot.tolist()
    
    return {"labels": time_labels, "data": amplitude_data}
