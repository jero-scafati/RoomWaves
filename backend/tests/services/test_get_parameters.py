import numpy as np
import pytest
from app.services.get_parameters import process_impulse_response


class TestParametersPipeline:
    
    def test_pipeline_with_synthetic_multiband(self, synthetic_ri_multi_band, known_t60_values):
        result = synthetic_ri_multi_band
        ri = result['audio_data']
        fs = result['fs']
        
        params = process_impulse_response(
            ri=ri,
            fs=fs,
            filter_type=1,
            smoothing_window_ms=50
        )
        
        assert 'parameters' in params
        parameters = params['parameters']
        
        for freq_str in known_t60_values.keys():
            assert freq_str in parameters
            assert 'EDT' in parameters[freq_str]
            assert 'T60_from_T20' in parameters[freq_str]
            assert 'T60_from_T30' in parameters[freq_str]
            assert 'C50' in parameters[freq_str]
            assert 'D50' in parameters[freq_str]
    
    def test_t60_accuracy_with_known_values(self, synthetic_ri_multi_band, known_t60_values):
        result = synthetic_ri_multi_band
        ri = result['audio_data']
        fs = result['fs']
        
        params = process_impulse_response(
            ri=ri,
            fs=fs,
            filter_type=1,
            smoothing_window_ms=50
        )
        
        parameters = params['parameters']
        tolerance_percentage = 20
        
        for freq_str, expected_t60 in known_t60_values.items():
            if freq_str in parameters:
                calculated_t30 = parameters[freq_str]['T60_from_T30']
                
                lower_bound = expected_t60 * (1 - tolerance_percentage / 100)
                upper_bound = expected_t60 * (1 + tolerance_percentage / 100)
                
                assert lower_bound <= calculated_t30 <= upper_bound, \
                    f"T60 at {freq_str}Hz: expected ~{expected_t60}s, got {calculated_t30:.2f}s"
    
    def test_edt_reasonable_values(self, synthetic_ri_multi_band, known_t60_values):
        result = synthetic_ri_multi_band
        ri = result['audio_data']
        fs = result['fs']
        
        params = process_impulse_response(
            ri=ri,
            fs=fs,
            filter_type=1,
            smoothing_window_ms=50
        )
        
        parameters = params['parameters']
        
        for freq_str in known_t60_values.keys():
            if freq_str in parameters:
                edt = parameters[freq_str]['EDT']
                assert 0.1 < edt < 10.0, f"EDT at {freq_str}Hz out of reasonable range: {edt}"
    
    def test_clarity_c50_range(self, synthetic_ri_multi_band):
        result = synthetic_ri_multi_band
        ri = result['audio_data']
        fs = result['fs']
        
        params = process_impulse_response(
            ri=ri,
            fs=fs,
            filter_type=1,
            smoothing_window_ms=50
        )
        
        parameters = params['parameters']
        
        for freq_str, values in parameters.items():
            c50 = values['C50']
            assert -10 < c50 < 20, f"C50 at {freq_str}Hz out of typical range: {c50}"
    
    def test_definition_d50_range(self, synthetic_ri_multi_band):
        result = synthetic_ri_multi_band
        ri = result['audio_data']
        fs = result['fs']
        
        params = process_impulse_response(
            ri=ri,
            fs=fs,
            filter_type=1,
            smoothing_window_ms=50
        )
        
        parameters = params['parameters']
        
        for freq_str, values in parameters.items():
            d50 = values['D50']
            assert 0 <= d50 <= 100, f"D50 at {freq_str}Hz out of range [0,100]: {d50}"
    
    def test_different_filter_types(self, synthetic_ri_single_band):
        result = synthetic_ri_single_band
        ri = result['audio_data']
        fs = result['fs']
        
        for filter_type in [1, 3]:
            params = process_impulse_response(
                ri=ri,
                fs=fs,
                filter_type=filter_type,
                smoothing_window_ms=50
            )
            
            assert 'parameters' in params
            assert len(params['parameters']) > 0
    
    def test_different_smoothing_windows(self, synthetic_ri_single_band):
        result = synthetic_ri_single_band
        ri = result['audio_data']
        fs = result['fs']
        
        for window_ms in [10, 50, 100]:
            params = process_impulse_response(
                ri=ri,
                fs=fs,
                filter_type=1,
                smoothing_window_ms=window_ms
            )
            
            assert 'parameters' in params
            assert len(params['parameters']) > 0
    
    def test_t20_vs_t30_consistency(self, synthetic_ri_multi_band):
        result = synthetic_ri_multi_band
        ri = result['audio_data']
        fs = result['fs']
        
        params = process_impulse_response(
            ri=ri,
            fs=fs,
            filter_type=1,
            smoothing_window_ms=50
        )
        
        parameters = params['parameters']
        
        for freq_str, values in parameters.items():
            t20 = values['T60_from_T20']
            t30 = values['T60_from_T30']
            
            ratio = t20 / t30 if t30 != 0 else 1
            assert 0.5 < ratio < 2.0, \
                f"T20/T30 ratio at {freq_str}Hz inconsistent: T20={t20:.2f}, T30={t30:.2f}"
    
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
