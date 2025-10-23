from app.utils.pipeline.orchestrator import AcousticPipeline

def process_impulse_response(
    ri,
    fs: int,
    filter_type: int,
    smoothing_window_ms: int
) -> dict:
    """
    Processes an impulse response using the acoustic pipeline.
    """
    pipeline = AcousticPipeline(
        fs=fs,
        filter_type=filter_type,
        smoothing_window_ms=smoothing_window_ms
    )

    pipeline.run(ri)

    final_parameters = pipeline.get_final_parameters()
    
    return {"parameters": final_parameters}