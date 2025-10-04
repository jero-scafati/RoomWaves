// ============================================================================
// Composable: useParameters
// Manages acoustical parameters state and API calls
// ============================================================================
import { ref, computed } from 'vue';
import ApiService from '@/services/ApiService.js';

export function useParameters() {
  // State
  const data = ref(null);
  const isLoading = ref(false);
  const error = ref('');
  const selectedBands = ref(1); // 1 = octave, 3 = 1/3 octave
  const bandsOptions = [
    { value: 1, label: 'Octave Band' },
    { value: 3, label: '1/3 Octave Band' }
  ];

  // Computed
  const isVisible = computed(() => data.value !== null);

  // Methods
  const fetchData = async (filename) => {
    if (!filename) return;
    
    isLoading.value = true;
    error.value = '';
    
    try {
      const response = await ApiService.getParameters(filename, selectedBands.value);
      data.value = response.data;
    } catch (err) {
      error.value = 'Could not load acoustical parameters.';
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
    selectedBands,
    bandsOptions,
    fetchData,
    toggle,
    clear
  };
}
