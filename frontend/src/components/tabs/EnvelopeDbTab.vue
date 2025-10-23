<script setup>
import WaveformChart from '@/components/charts/WaveformChart.vue';

defineProps({
  chartData: Object,
  isLoading: Boolean,
  error: String,
  isVisible: Boolean
});
</script>

<template>
  <div class="tab-content">
    <div class="chart-container">
      <div v-if="isLoading" class="status-message">
        <p>Loading Envelope Decay...</p>
      </div>
      <div v-else-if="error" class="status-message error">
        <p>{{ error }}</p>
      </div>
      <WaveformChart v-else-if="isVisible" :chartData="chartData" />
      <div v-else class="status-message">
        <p>Loading envelope data...</p>
      </div>
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
</style>
