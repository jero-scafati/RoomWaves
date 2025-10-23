import { ref, computed } from 'vue';
import ApiService from '@/services/ApiService.js';

export function useEnvelopeDb() {
  const chartData = ref(null);
  const isLoading = ref(false);
  const error = ref('');

  const isVisible = computed(() => chartData.value !== null);

  const fetchData = async (filename) => {
    if (!filename) return;
    
    isLoading.value = true;
    error.value = '';
    
    try {
      const response = await ApiService.getEnvelopeDbData(filename);
      chartData.value = {
        labels: response.data.labels,
        datasets: [{
          label: 'Envelope (dB)',
          backgroundColor: '#8b5cf6',
          borderColor: '#8b5cf6',
          data: response.data.data,
          tension: 0.3
        }]
      };
    } catch (err) {
      error.value = 'Could not load envelope data.';
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
