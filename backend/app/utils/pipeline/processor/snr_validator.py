import numpy as np
import warnings
from app.utils.pipeline.abc import SignalProcessor

class SNRValidator(SignalProcessor):
    def __init__(self, fs: int, noise_tail_percentage: float = 0.2):
        super().__init__(fs)
        if not 0 < noise_tail_percentage < 1:
            raise ValueError("El 'noise_tail_percentage' debe estar entre 0 y 1.")
        self.noise_tail_percentage = noise_tail_percentage

    def process(self, data: dict) -> dict:
        impulse_response = data.get('ri')

        if impulse_response is None or len(impulse_response) == 0:
            warnings.warn("La respuesta al impulso está vacía. No se puede calcular el SNR.")
            data['snr_db'] = None
            return data

        peak_signal_amplitude = np.max(np.abs(impulse_response))

        if peak_signal_amplitude == 0:
            data['snr_db'] = None
            return data

        num_samples = len(impulse_response)
        noise_start_index = int(num_samples * (1 - self.noise_tail_percentage))
        noise_tail = impulse_response[noise_start_index:]

        if len(noise_tail) == 0:
            warnings.warn("La señal es demasiado corta para estimar la cola de ruido. No se puede calcular el SNR.")
            data['snr_db'] = None
            return data

        noise_level_rms = np.sqrt(np.mean(noise_tail**2))

        if noise_level_rms == 0:
            snr_db = float('inf')
        else:
            snr_db = float(20 * np.log10(peak_signal_amplitude / noise_level_rms))

        data['snr_db'] = snr_db
        return data
