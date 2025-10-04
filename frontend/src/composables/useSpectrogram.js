// ============================================================================
// Composable: useSpectrogram
// Manages spectrogram plot state and API calls
// ============================================================================
import { ref, computed } from 'vue';
import ApiService from '@/services/ApiService.js';

export function useSpectrogram() {
  // State
  const data = ref(null);
  const isLoading = ref(false);
  const error = ref('');

  // Computed
  const isVisible = computed(() => data.value !== null);

  // Methods
  const fetchData = async (filename) => {
    if (!filename) return;
    
    isLoading.value = true;
    error.value = '';
    
    try {
      const response = await ApiService.getSpectrogramData(filename);
      data.value = response.data;
    } catch (err) {
      error.value = 'Could not load spectrogram data.';
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
    data.value = null;
    error.value = '';
  };

  return {
    data,
    isLoading,
    error,
    isVisible,
    fetchData,
    toggle,
    clear
  };
}
