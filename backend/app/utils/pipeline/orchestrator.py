import numpy as np

from .abc import SignalProcessor
from .processor import (
    BandpassFilter,
    EnvelopeSmoother,
    DecayAnalyzer,
    ParameterCalculator
)

class AcousticPipeline:
    """Orchestrates the execution of the signal processing chain."""
    def __init__(self, fs: int, filter_type: int, smoothing_window_ms: int):
        self.fs = fs
        
        self.processors: list[SignalProcessor] = [
            BandpassFilter(fs, filter_type=filter_type),
            EnvelopeSmoother(fs, smoothing_window_ms=smoothing_window_ms),
            DecayAnalyzer(fs),
            ParameterCalculator(fs)
        ]
        self.processing_data: dict[str, object] = {}

    def run(self, impulse_response: np.ndarray) -> None:
        """
        Executes the full processing pipeline on an impulse response.
        The results are stored internally.
        """
        self.processing_data = {'ri': impulse_response, 'fs': self.fs}
        for processor in self.processors:
            self.processing_data = processor.process(self.processing_data)

    def get_final_parameters(self) -> dict[str, object]:
        """
        Returns the essential acoustic parameters calculated by the pipeline.
        This should be called after run().
        """
        return self.processing_data.get('acoustic_parameters', {})