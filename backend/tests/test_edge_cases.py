import numpy as np
import pytest
from app.services.get_parameters import process_impulse_response
from app.services.get_snr import calculate_snr


class TestEdgeCases:
    
    def test_very_short_impulse_response(self):
        ri = np.random.randn(1000)
        fs = 44100
        
        params = process_impulse_response(
            ri=ri,
            fs=fs,
            filter_type=1,
            smoothing_window_ms=50
        )
        
        assert 'parameters' in params
        assert isinstance(params['parameters'], dict)
    
    def test_very_low_snr_signal(self):
        np.random.seed(42)
        signal_clean = np.exp(-np.linspace(0, 5, 10000))
        noise = 0.5 * np.random.randn(10000)
        ri = signal_clean + noise
        
        snr = calculate_snr(ri)
        assert snr is not None
        assert snr > 0
    
    def test_normalized_vs_unnormalized_signal(self):
        np.random.seed(42)
        ri_base = np.exp(-np.linspace(0, 3, 20000))
        
        ri_normalized = ri_base / np.max(np.abs(ri_base))
        ri_scaled = ri_base * 100
        
        snr1 = calculate_snr(ri_normalized)
        snr2 = calculate_snr(ri_scaled)
        
        assert abs(snr1 - snr2) < 1.0
    
    def test_pipeline_consistency_multiple_runs(self, synthetic_ri_multi_band):
        result = synthetic_ri_multi_band
        ri = result['audio_data']
        fs = result['fs']
        
        params1 = process_impulse_response(
            ri=ri,
            fs=fs,
            filter_type=1,
            smoothing_window_ms=50
        )
        
        params2 = process_impulse_response(
            ri=ri,
            fs=fs,
            filter_type=1,
            smoothing_window_ms=50
        )
        
        for freq in params1['parameters'].keys():
            for param_name in ['EDT', 'T60_from_T20', 'T60_from_T30', 'C50', 'D50']:
                val1 = params1['parameters'][freq][param_name]
                val2 = params2['parameters'][freq][param_name]
                assert val1 == val2, f"Inconsistent {param_name} at {freq}Hz"
    
    def test_high_sampling_rate(self):
        np.random.seed(42)
        fs = 96000
        t = np.arange(0, 1.0, 1/fs)
        ri = np.exp(-3 * t) * np.cos(2 * np.pi * 1000 * t)
        
        params = process_impulse_response(
            ri=ri,
            fs=fs,
            filter_type=1,
            smoothing_window_ms=50
        )
        
        assert 'parameters' in params
        assert len(params['parameters']) > 0
    
    def test_signal_with_silence_at_start(self):
        np.random.seed(42)
        silence = np.zeros(5000)
        signal = np.exp(-np.linspace(0, 3, 15000))
        ri = np.concatenate([silence, signal])
        
        snr = calculate_snr(ri)
        assert snr is not None
