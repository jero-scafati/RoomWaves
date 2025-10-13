// ============================================================================
// Composable: useSNR
// Manages SNR (Signal-to-Noise Ratio) state and API calls
// ============================================================================
import { ref, computed } from 'vue';
import ApiService from '@/services/ApiService.js';

export function useSNR() {
  // State
  const snr = ref(null);
  const isLoading = ref(false);
  const error = ref('');

  // Computed
  const quality = computed(() => {
    if (snr.value === null || snr.value === undefined) return null;
    
    if (snr.value > 50) return { label: 'Excellent', class: 'excellent', icon: '✅' };
    if (snr.value > 35) return { label: 'Good', class: 'good', icon: '👍' };
    if (snr.value > 20) return { label: 'Questionable', class: 'questionable', icon: '⚠️' };
    return { label: 'Poor', class: 'poor', icon: '❌' };
  });

  const description = computed(() => {
    if (!quality.value) return '';
    
    switch (quality.value.class) {
      case 'excellent':
        return 'Very clean signal. Parameters are highly reliable.';
      case 'good':
        return 'Good signal quality. Sufficient for most analyses.';
      case 'questionable':
        return 'Caution: Results may show variability due to noise.';
      case 'poor':
        return 'Warning: High noise level. Results may not be reliable.';
      default:
        return '';
    }
  });

  // Methods
  const fetchSNR = async (filename) => {
    if (!filename) return;
    
    isLoading.value = true;
    error.value = '';
    
    try {
      const response = await ApiService.getSNR(filename);
      snr.value = response.data.snr_db;
      console.log('SNR received:', snr.value);
    } catch (err) {
      error.value = 'Could not calculate SNR.';
      console.error(err);
    } finally {
      isLoading.value = false;
    }
  };

  const clear = () => {
    snr.value = null;
    error.value = '';
  };

  return {
    snr,
    isLoading,
    error,
    quality,
    description,
    fetchSNR,
    clear
  };
}
