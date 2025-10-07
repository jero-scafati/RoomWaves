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
// No emits needed - automatic loading
</script>

<template>
  <div class="tab-content">
    <div class="chart-container">
      <div v-if="isLoading" class="status-message">
        <p>Loading Waveform...</p>
      </div>
      <div v-else-if="error" class="status-message error">
        <p>{{ error }}</p>
      </div>
      <WaveformChart v-else-if="isVisible" :chartData="chartData" />
      <div v-else class="status-message">
        <p>Loading waveform data...</p>
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
