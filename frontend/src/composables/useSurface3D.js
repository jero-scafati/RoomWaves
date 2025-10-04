// ============================================================================
// Composable: useSurface3D
// Manages 3D surface plot state and API calls
// ============================================================================
import { ref, computed } from 'vue';
import ApiService from '@/services/ApiService.js';

export function useSurface3D() {
  // State
  const data = ref(null);
  const isLoading = ref(false);
  const error = ref('');
  const dataReduction = ref(2);
  const bands = ref(48);
  const bandsOptions = [1, 3, 6, 12, 24, 48];

  // Computed
  const isVisible = computed(() => data.value !== null);

  // Methods
  const fetchData = async (filename) => {
    if (!filename) return;
    
    isLoading.value = true;
    error.value = '';
    
    try {
      const response = await ApiService.getCsdData(filename, bands.value);
      data.value = response.data;
    } catch (err) {
      error.value = 'Could not load 3D surface data.';
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
    dataReduction,
    bands,
    bandsOptions,
    fetchData,
    toggle,
    clear
  };
}
