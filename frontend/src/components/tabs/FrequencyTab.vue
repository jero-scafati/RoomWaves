<script setup>
// ============================================================================
// IMPORTS
// ============================================================================
import FrequencyChart from '@/components/charts/FrequencyChart.vue';

// ============================================================================
// PROPS
// ============================================================================
const props = defineProps({
  chartData: Object,
  isLoading: Boolean,
  error: String,
  isVisible: Boolean,
  selectedBands: Number,
  bandsOptions: Array
});

// ============================================================================
// EMITS
// ============================================================================
const emit = defineEmits(['update:selectedBands']);
</script>

<template>
  <div class="tab-content">
    <div class="controls">
      <div class="control-group">
        <label for="bands-select">Bands per Octave:</label>
        <select 
          id="bands-select" 
          :value="selectedBands"
          @change="emit('update:selectedBands', Number($event.target.value))"
        >
          <option v-for="band in bandsOptions" :key="band" :value="band">
            1/{{ band }}
          </option>
        </select>
      </div>
    </div>
    
    <div class="chart-container">
      <div v-if="isLoading" class="status-message">
        <p>Loading Frequency Response...</p>
      </div>
      <div v-else-if="error" class="status-message error">
        <p>{{ error }}</p>
      </div>
      <FrequencyChart v-else-if="isVisible" :chartData="chartData" />
      <div v-else class="status-message">
        <p>Loading frequency response data...</p>
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

.controls {
  margin-bottom: var(--space-lg);
  display: flex;
  justify-content: center;
  align-items: center;
  gap: var(--space-lg);
  flex-wrap: wrap;
}

.control-group {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  padding: var(--space-sm) var(--space-md);
  background: rgba(24, 26, 27, 0.4);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: var(--radius-lg);
  transition: all var(--transition-base);
}

.control-group:hover {
  border-color: rgba(255, 255, 255, 0.12);
  background: rgba(24, 26, 27, 0.5);
}

label {
  color: var(--color-text-secondary);
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
}

select {
  background: var(--color-surface-elevated);
  color: var(--color-text-primary);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-md);
  padding: var(--space-sm) var(--space-md);
  cursor: pointer;
  transition: all var(--transition-base);
  font-weight: var(--font-weight-medium);
}

select:hover {
  border-color: var(--color-border-lighter);
  background: var(--color-surface-hover);
}

select:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(47, 9, 136, 0.1);
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
