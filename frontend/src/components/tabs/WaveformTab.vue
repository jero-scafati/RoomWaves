<script setup>
// ============================================================================
// IMPORTS
// ============================================================================
import WaveformChart from '@/components/charts/WaveformChart.vue';

// ============================================================================
// PROPS
// ============================================================================
const props = defineProps({
  chartData: Object,
  isLoading: Boolean,
  error: String,
  isVisible: Boolean
});

// ============================================================================
// EMITS
// ============================================================================
const emit = defineEmits(['toggle']);
</script>

<template>
  <div class="tab-content">
    <div class="controls">
      <button @click="emit('toggle')" :disabled="isLoading">
        {{ isVisible ? 'Clear' : 'Plot' }}
      </button>
    </div>
    
    <div class="chart-container">
      <div v-if="isLoading" class="status-message">
        <p>Loading Waveform...</p>
      </div>
      <div v-else-if="error" class="status-message error">
        <p>{{ error }}</p>
      </div>
      <WaveformChart v-else-if="isVisible" :chartData="chartData" />
      <div v-else class="status-message">
        <p>Click "Plot" to visualize the waveform.</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.tab-content {
  animation: fadeIn 0.3s ease-in;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.controls {
  margin-bottom: 1.5rem;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1.5rem;
  flex-wrap: wrap;
}

button {
  background-color: #3b82f6;
  color: white;
  border: none;
  padding: 10px 24px;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.2s ease;
  font-weight: 500;
  font-size: 0.95rem;
}

button:hover {
  background-color: #2563eb;
}

button:disabled {
  background-color: #4a4a4a;
  cursor: not-allowed;
}

.chart-container {
  padding: 1rem;
  background-color: #242424;
  border-radius: 8px;
  min-height: 420px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.status-message {
  color: #a0a0a0;
  font-size: 1rem;
}

.error {
  color: #f87171;
}
</style>
