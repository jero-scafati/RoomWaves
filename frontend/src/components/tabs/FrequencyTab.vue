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
const emit = defineEmits(['toggle', 'update:selectedBands']);
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
      <button @click="emit('toggle')" :disabled="isLoading">
        {{ isVisible ? 'Clear' : 'Plot' }}
      </button>
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
        <p>Select bands and click "Plot" to see the frequency response.</p>
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

.control-group {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

label {
  color: #a0a0a0;
  font-size: 0.9rem;
  font-weight: 500;
}

select {
  background-color: #3a3a3a;
  color: white;
  border: 1px solid #5a5a5a;
  border-radius: 6px;
  padding: 8px 12px;
  cursor: pointer;
  transition: border-color 0.2s ease;
}

select:hover {
  border-color: #7a7a7a;
}

select:focus {
  outline: none;
  border-color: #3b82f6;
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
