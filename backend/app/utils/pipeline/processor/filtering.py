import numpy as np
from scipy import signal

from app.utils.pipeline.abc import SignalProcessor
from app.utils.pipeline.constants import (
    OCTAVE_FREQUENCIES,
    THIRD_OCTAVE_FREQUENCIES,
    BANDWIDTH_FACTOR_OCTAVE,
    BANDWIDTH_FACTOR_THIRD_OCTAVE
)

class BandpassFilter(SignalProcessor):
    """
    Processor to filter the impulse response signal into frequency bands.
    """
    def __init__(self, fs: int, filter_type: int = 1, filter_order: int = 4):
        super().__init__(fs)
        self.filter_type = filter_type
        self.filter_order = filter_order

    def process(self, data: dict) -> dict:
        """
        Expects 'ri' in the data dictionary.
        Adds 'filtered_signals' (a dict of signals filtered by frequency) to the data.
        """
        impulse_response = data['ri']
        
        if self.filter_type == 1:
            bandwidth_factor = BANDWIDTH_FACTOR_OCTAVE
            center_frequencies = OCTAVE_FREQUENCIES
        elif self.filter_type == 3:
            bandwidth_factor = BANDWIDTH_FACTOR_THIRD_OCTAVE
            center_frequencies = THIRD_OCTAVE_FREQUENCIES
        else:
            raise ValueError("Filter type must be 'octava' or 'tercio_octava'")

        ratio = np.power(2, bandwidth_factor)
        filtered_signals = {}
        
        for center_freq in center_frequencies:
            low_cutoff = center_freq / ratio
            high_cutoff = center_freq * ratio
            
            sos = signal.iirfilter(
                self.filter_order,
                [low_cutoff, high_cutoff],
                btype='band',
                ftype='butter',
                fs=self.fs,
                output='sos'
            )
            
            filtered_signal = signal.sosfiltfilt(sos, impulse_response)
            filtered_signals[center_freq] = filtered_signal
            
        data['filtered_signals'] = filtered_signals
        return data