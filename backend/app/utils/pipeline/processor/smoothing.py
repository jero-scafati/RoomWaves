from app.utils.pipeline .abc import SignalProcessor

class EnvelopeSmoother(SignalProcessor):
    """
    Processor to calculate the smoothed envelope for each filtered signal.
    """
    def __init__(self, fs: int, smoothing_window_ms: int = 5):
        super().__init__(fs)
        self.window_samples = int(smoothing_window_ms * 1e-3 * fs)

    def _hilbert_transform(self, time_signal):
        import numpy as np
        
        signal_length = len(time_signal)
        if signal_length == 0:
            return np.array([])
            
        freq_domain_signal = np.fft.fft(time_signal)
        
        h = np.zeros(signal_length)
        if signal_length > 1:
            h[0] = 1
            h[1:signal_length // 2] = 2
            if signal_length % 2 == 0:
                h[signal_length // 2] = 1
        
        analytic_signal = np.fft.ifft(freq_domain_signal * h)
        return np.abs(analytic_signal)

    def _moving_average_filter(self, signal_to_smooth, window_length: int):
        import numpy as np
        
        if window_length < 1:
            raise ValueError("Window length must be at least 1.")
        if window_length == 1 or len(signal_to_smooth) == 0:
            return signal_to_smooth

        kernel = np.ones(window_length) / window_length
        return np.convolve(signal_to_smooth, kernel, mode='same')

    def process(self, data: dict) -> dict:
        """
        Expects 'filtered_signals' in the data dictionary.
        Adds 'envelopes' to the data.
        """
        filtered_signals = data['filtered_signals']
        envelopes = {}
        
        for freq, signal_data in filtered_signals.items():
            hilbert_envelope = self._hilbert_transform(signal_data)
            smoothed_envelope = self._moving_average_filter(hilbert_envelope, self.window_samples)
            envelopes[freq] = smoothed_envelope
            
        data['envelopes'] = envelopes
        return data