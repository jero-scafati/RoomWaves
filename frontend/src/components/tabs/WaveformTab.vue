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
  isVisible: Boolean,
  filePath: String
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
    
    <!-- Audio Player -->
    <div v-if="isVisible && !isLoading && !error && filePath" class="audio-player-container">
      <audio :src="`/${filePath}`" controls class="audio-player"></audio>
    </div>
  </div>
</template>

<style scoped>
.tab-content {
  animation: fadeIn 0.4s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(15px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.chart-container {
  padding: var(--space-md);
  background: transparent;
  border: none;
  border-radius: var(--radius-lg);
  min-height: 420px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.status-message {
  color: var(--color-text-secondary);
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-medium);
  display: flex;
  align-items: center;
  gap: var(--space-sm);
}

.status-message p {
  margin: 0;
}

.error {
  color: var(--color-error);
}

.audio-player-container {
  margin-top: var(--space-lg);
  padding: var(--space-lg);
  background: rgba(24, 26, 27, 0.4);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: var(--radius-lg);
  display: flex;
  justify-content: center;
  transition: all var(--transition-base);
}

.audio-player-container:hover {
  border-color: rgba(255, 255, 255, 0.12);
  background: rgba(24, 26, 27, 0.5);
}

.audio-player {
  width: 100%;
  max-width: 600px;
  border-radius: var(--radius-md);
}
</style>
