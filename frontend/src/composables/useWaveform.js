// ============================================================================
// Composable: useWaveform
// Manages waveform plot state and API calls
// ============================================================================
import { ref, computed } from 'vue';
import ApiService from '@/services/ApiService.js';

export function useWaveform() {
  // State
  const chartData = ref(null);
  const isLoading = ref(false);
  const error = ref('');

  // Computed
  const isVisible = computed(() => chartData.value !== null);

  // Methods
  const fetchData = async (filename) => {
    if (!filename) return;
    
    isLoading.value = true;
    error.value = '';
    
    try {
      const response = await ApiService.getPlotData(filename);
      chartData.value = {
        labels: response.data.labels,
        datasets: [{
          label: 'Waveform',
          backgroundColor: '#3b82f6',
          borderColor: '#3b82f6',
          data: response.data.data,
          tension: 0.1
        }]
      };
    } catch (err) {
      error.value = 'Could not load waveform data.';
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
    fetchData,
    toggle,
    clear
  };
}
