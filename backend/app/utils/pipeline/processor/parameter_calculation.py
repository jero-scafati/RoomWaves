import numpy as np

from app.utils.pipeline.abc import SignalProcessor
from app.utils.pipeline.helpers import linear_regression_in_range

class ParameterCalculator(SignalProcessor):
    """
    Final processor to calculate acoustic parameters according to ISO 3382.
    """
    def _calculate_clarity_and_definition(self, p_squared: np.ndarray, noise_start_index: int) -> dict:
        # Validate noise_start_index to prevent empty slice warnings
        if noise_start_index >= len(p_squared) or noise_start_index < 0:
            noise_start_index = max(0, len(p_squared) - 1)
        
        # Calculate noise power, handling edge cases
        noise_slice = p_squared[noise_start_index:]
        if len(noise_slice) == 0:
            noise_power_per_sample = 0.0
        else:
            noise_power_per_sample = np.mean(noise_slice)

        peak_index = np.argmax(p_squared)

        samples_50ms = int(0.050 * self.fs)

        t0 = peak_index
        t50 = min(t0 + samples_50ms, len(p_squared))

        total_len = len(p_squared)
        total_energy_raw = np.sum(p_squared)
        total_energy_corrected = total_energy_raw - (total_len * noise_power_per_sample)

        early_50_len = t50 - t0
        early_energy_50_raw = np.sum(p_squared[t0:t50])
        early_energy_50_corrected = early_energy_50_raw - (early_50_len * noise_power_per_sample)

        late_energy_50_corrected = total_energy_corrected - early_energy_50_corrected

        # Ensure all values are valid and positive to prevent NaN/inf
        total_energy_corrected = max(total_energy_corrected, 1e-12)
        early_energy_50_corrected = max(early_energy_50_corrected, 1e-12)
        late_energy_50_corrected = max(late_energy_50_corrected, 1e-12)

        d50 = 100.0 * (early_energy_50_corrected / total_energy_corrected)
        c50 = 10.0 * np.log10(early_energy_50_corrected / late_energy_50_corrected)

        return {'D50': d50, 'C50': c50}
        
    def process(self, data: dict) -> dict:
        decay_curves_db = data['decay_curves_db']
        filtered_signals = data['filtered_signals']
        lundeby_data = data['lundeby_data']
        acoustic_parameters = {}
        
        for freq, curve_db in decay_curves_db.items():
            time_vector = np.arange(len(curve_db)) / self.fs
            norm_curve_db = curve_db - np.max(curve_db)
            
            edt_reg = linear_regression_in_range(time_vector, norm_curve_db, -1, -11)
            t20_reg = linear_regression_in_range(time_vector, norm_curve_db, -5, -25)
            t30_reg = linear_regression_in_range(time_vector, norm_curve_db, -5, -35)
            
            original_filtered_signal = filtered_signals[freq]
            p_squared_for_clarity = original_filtered_signal ** 2
            noise_start_index = lundeby_data[freq]['noise_start_index']
            clarity_def_params = self._calculate_clarity_and_definition(p_squared_for_clarity, noise_start_index)

            acoustic_parameters[str(freq)] = {
                'EDT': -60.0 / edt_reg['slope'],
                'T60_from_T20': -60.0 / t20_reg['slope'],
                'T60_from_T30': -60.0 / t30_reg['slope'],
                'C50': clarity_def_params['C50'],
                'D50': clarity_def_params['D50']
            }
        
        data['acoustic_parameters'] = acoustic_parameters
        return data