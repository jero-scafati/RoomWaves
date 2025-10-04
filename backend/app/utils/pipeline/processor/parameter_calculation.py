import numpy as np

from app.utils.pipeline.abc import SignalProcessor
from app.utils.pipeline.helpers import linear_regression_in_range

class ParameterCalculator(SignalProcessor):
    """
    Final processor to calculate acoustic parameters according to ISO 3382.
    """
    def _calculate_clarity_and_definition(self, p_squared: np.ndarray) -> dict:
        n50 = min(int(0.050 * self.fs), len(p_squared))
        total_energy = np.sum(p_squared)
        early_energy_50 = np.sum(p_squared[:n50])
        d50 = 100.0 * (early_energy_50 / total_energy) if total_energy > 0 else 0

        n80 = min(int(0.080 * self.fs), len(p_squared))
        early_energy_80 = np.sum(p_squared[:n80])
        late_energy_80 = np.sum(p_squared[n80:])
        
        # Avoid log(0)
        c80 = 10.0 * np.log10(early_energy_80 / np.clip(late_energy_80, 1e-10, None))
        
        return {'D50': d50, 'C80': c80}
        
    def process(self, data: dict) -> dict:
        decay_curves_db = data['decay_curves_db']
        decay_curves = data['decay_curves']
        acoustic_parameters = {}
        
        for freq, curve_db in decay_curves_db.items():
            time_vector = np.arange(len(curve_db)) / self.fs
            # Normalize curve to start at 0 dB for consistent regression
            norm_curve_db = curve_db - np.max(curve_db)
            
            p_squared = decay_curves[freq]['p_squared']
            
            edt_reg = linear_regression_in_range(time_vector, norm_curve_db, -1, -11)
            t20_reg = linear_regression_in_range(time_vector, norm_curve_db, -5, -25)
            t30_reg = linear_regression_in_range(time_vector, norm_curve_db, -5, -35)
            
            clarity_def_params = self._calculate_clarity_and_definition(p_squared)

            acoustic_parameters[str(freq)] = {
                'EDT': -60.0 / edt_reg['slope'],
                'T60_from_T20': -60.0 / t20_reg['slope'],
                'T60_from_T30': -60.0 / t30_reg['slope'],
                'C80': clarity_def_params['C80'],
                'D50': clarity_def_params['D50']
            }
        
        data['acoustic_parameters'] = acoustic_parameters
        return data