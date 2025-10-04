import numpy as np

from app.utils.pipeline.abc import SignalProcessor
from app.utils.pipeline.helpers import to_db_scale, linear_regression_in_range

class DecayAnalyzer(SignalProcessor):
    """
    Processor to run the Lundeby algorithm and calculate the Schroeder integral.
    """
    def _calculate_rms_by_block(self, impulse_response: np.ndarray, block_ms: int = 20) -> dict:
        block_size = int(self.fs * block_ms / 1000)
        num_blocks = len(impulse_response) // block_size
        trimmed_ir = impulse_response[:num_blocks * block_size]
        ir_blocks = trimmed_ir.reshape(num_blocks, block_size)
        rms_per_block = np.sqrt(np.mean(ir_blocks**2, axis=1))
        return {'rms_values': rms_per_block, 'block_size': block_size}

    def _schroeder_integral(self, power_signal: np.ndarray, fs: float, crossover_index: int = None) -> dict:
        dt = 1.0 / fs
        p2 = power_signal**2
        if crossover_index is None:
            crossover_index = len(p2)
        
        total_energy = np.sum(p2[:crossover_index]) * dt
        cumulative_energy = np.cumsum(p2[:crossover_index]) * dt
        schroeder_curve = total_energy - cumulative_energy
        
        # Pad with zeros if necessary
        if len(schroeder_curve) < len(p2):
            padding = np.zeros(len(p2) - len(schroeder_curve))
            schroeder_curve = np.concatenate((schroeder_curve, padding))

        schroeder_curve[crossover_index:] = 0.0
        return {'schroeder_curve': schroeder_curve, 'p_squared': p2}

    def _lundeby_crossover(self, impulse_response: np.ndarray) -> dict:
        rms_data = self._calculate_rms_by_block(impulse_response)
        rms_values, block_size = rms_data['rms_values'], rms_data['block_size']
        time_vector_rms = np.arange(len(rms_values)) * block_size / self.fs
        
        fs_rms = self.fs / block_size
        sch_data = self._schroeder_integral(rms_values, fs_rms)
        sch_db = to_db_scale(sch_data['schroeder_curve'])
        
        noise_level = np.mean(sch_db[int(len(sch_db) * 0.9):])
        
        reg = linear_regression_in_range(time_vector_rms, sch_db, 0, noise_level + 7.5)
        slope, intercept = reg['slope'], reg['intercept']
        
        crossover_time = (noise_level - intercept) / slope if slope != 0 else float('inf')
        prev_crossover = crossover_time
        
        for _ in range(10): # Max 6 iterations
            noise_start_time = (noise_level + 7.5 - intercept) / slope if slope != 0 else float('inf')
            noise_start_index = max(0, min(len(impulse_response), int(noise_start_time * self.fs)))
            
            if len(impulse_response) - noise_start_index < int(0.1 * len(impulse_response)):
                noise_start_index = len(impulse_response) - int(0.1 * len(impulse_response))
            
            noise_level = np.mean(sch_db[int(noise_start_index / block_size):])
            
            upper_db, lower_db = -5.0, noise_level + 10.0
            if lower_db >= upper_db: break

            reg = linear_regression_in_range(time_vector_rms, sch_db, upper_db, lower_db)
            slope, intercept = reg['slope'], reg['intercept']
            
            crossover_time = (noise_level - intercept) / slope if slope != 0 else float('inf')
            if abs(crossover_time - prev_crossover) < 1e-3: break
            prev_crossover = crossover_time
            
        crossover_index = int(round(crossover_time * self.fs))
        return {'crossover_index': crossover_index}

    def process(self, data: dict) -> dict:
        envelopes = data['envelopes']
        decay_curves = {}
        decay_curves_db = {}
        
        for freq, envelope in envelopes.items():
            crossover_data = self._lundeby_crossover(envelope)
            crossover_index = crossover_data['crossover_index']
            
            schroeder_data = self._schroeder_integral(envelope, self.fs, crossover_index)
            decay_curves[freq] = schroeder_data
            decay_curves_db[freq] = to_db_scale(schroeder_data['schroeder_curve'])

        data['decay_curves'] = decay_curves
        data['decay_curves_db'] = decay_curves_db
        return data