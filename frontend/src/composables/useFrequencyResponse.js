// ============================================================================
// Composable: useFrequencyResponse
// Manages frequency response plot state and API calls
// ============================================================================
import { ref, computed } from 'vue';
import ApiService from '@/services/ApiService.js';

export function useFrequencyResponse() {
  // State
  const chartData = ref(null);
  const isLoading = ref(false);
  const error = ref('');
  const selectedBands = ref(24);
  const bandsOptions = [1, 3, 6, 12, 24, 48];

  // Computed
  const isVisible = computed(() => chartData.value !== null);

  // Methods
  const fetchData = async (filename) => {
    if (!filename) return;
    
    isLoading.value = true;
    error.value = '';
    
    try {
      const response = await ApiService.getFrequencyData(filename, selectedBands.value);
      chartData.value = {
        labels: response.data.frequencies,
        datasets: [{
          label: 'Frequency Response',
          backgroundColor: '#10b981',
          borderColor: '#10b981',
          data: response.data.magnitudes,
          tension: 0.1
        }]
      };
    } catch (err) {
      error.value = 'Could not load frequency data.';
      console.error(err);
    } finally {
      isLoading.value = false;
    }
  };

  const toggle = async (filename) => {
    if (isVisible.value) {
      clear();
    } else {
      await fetchData(filename);
    }
  };

  const clear = () => {
    chartData.value = null;
    error.value = '';
  };

  return {
    chartData,
    isLoading,
    error,
    isVisible,
    selectedBands,
    bandsOptions,
    fetchData,
    toggle,
    clear
  };
}
