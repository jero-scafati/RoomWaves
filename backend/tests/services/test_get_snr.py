import numpy as np
import pytest
from app.services.get_snr import calculate_snr


class TestSNRCalculation:
    
    def test_snr_with_synthetic_signal(self, known_snr_synthetic):
        result, expected_snr, tolerance = known_snr_synthetic
        ri = result['audio_data']
        
        calculated_snr = calculate_snr(ri, noise_tail_percentage=0.2)
        
        assert calculated_snr is not None
        assert abs(calculated_snr - expected_snr) < tolerance
    
    def test_snr_empty_signal(self):
        ri = np.array([])
        snr = calculate_snr(ri)
        assert snr is None
    
    def test_snr_zero_signal(self):
        ri = np.zeros(1000)
        snr = calculate_snr(ri)
        assert snr is None
    
    def test_snr_no_noise(self):
        ri = np.ones(1000)
        ri[-200:] = 0
        snr = calculate_snr(ri, noise_tail_percentage=0.2)
        assert snr == float('inf')
    
    def test_snr_different_tail_percentages(self, synthetic_ri_single_band):
        ri = synthetic_ri_single_band['audio_data']
        
        snr_10 = calculate_snr(ri, noise_tail_percentage=0.1)
        snr_20 = calculate_snr(ri, noise_tail_percentage=0.2)
        snr_30 = calculate_snr(ri, noise_tail_percentage=0.3)
        
        assert snr_10 is not None
        assert snr_20 is not None
        assert snr_30 is not None
        assert isinstance(snr_10, float)
        assert isinstance(snr_20, float)
        assert isinstance(snr_30, float)
    
    def test_snr_realistic_range(self, synthetic_ri_multi_band):
        ri = synthetic_ri_multi_band['audio_data']
        snr = calculate_snr(ri)
        
        assert snr is not None
        assert 20 < snr < 100
    
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
    
    def test_signal_with_silence_at_start(self):
        np.random.seed(42)
        silence = np.zeros(5000)
        signal = np.exp(-np.linspace(0, 3, 15000))
        ri = np.concatenate([silence, signal])
        
        snr = calculate_snr(ri)
        assert snr is not None
