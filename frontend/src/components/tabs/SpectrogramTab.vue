<script setup>
// ============================================================================
// IMPORTS
// ============================================================================
import SpectrogramChart from '@/components/charts/SpectrogramChart.vue';

// ============================================================================
// PROPS
// ============================================================================
const props = defineProps({
  data: Object,
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
        <p>Loading Spectrogram...</p>
      </div>
      <div v-else-if="error" class="status-message error">
        <p>{{ error }}</p>
      </div>
      <SpectrogramChart v-else-if="isVisible" :spectrogramData="data" />
      <div v-else class="status-message">
        <p>Loading spectrogram data...</p>
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
}

.status-message p {
  margin: 0;
}

.error {
  color: var(--color-error);
}
</style>
