<script setup>
// ============================================================================
// IMPORTS
// ============================================================================
import Surface3dChart from '@/components/charts/Surface3dChart.vue';

// ============================================================================
// PROPS
// ============================================================================
const props = defineProps({
  data: Object,
  isLoading: Boolean,
  error: String,
  isVisible: Boolean,
  dataReduction: Number,
  bands: Number,
  bandsOptions: Array
});

// ============================================================================
// EMITS
// ============================================================================
const emit = defineEmits(['toggle', 'update:dataReduction', 'update:bands', 'refetch']);
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
        <p>Loading 3D Surface...</p>
      </div>
      <div v-else-if="error" class="status-message error">
        <p>{{ error }}</p>
      </div>
      <Surface3dChart 
        v-else-if="isVisible" 
        :surface-data="data"
        :data-reduction="dataReduction"
      >
        <template #controls>
          <div class="control-panel">
            <div class="control-group">
              <label>Octave Smoother:</label>
              <select 
                :value="bands"
                @change="emit('update:bands', Number($event.target.value)); emit('refetch')"
              >
                <option v-for="band in bandsOptions" :key="band" :value="band">
                  1/{{ band }}
                </option>
              </select>
            </div>
            <div class="control-group">
              <label>Data Reduction:</label>
              <select 
                :value="dataReduction"
                @change="emit('update:dataReduction', Number($event.target.value))"
              >
                <option :value="1">Full Resolution</option>
                <option :value="2">1/2 Resolution</option>
                <option :value="3">1/3 Resolution</option>
                <option :value="4">1/4 Resolution</option>
              </select>
            </div>
          </div>
        </template>
      </Surface3dChart>
      <div v-else class="status-message">
        <p>Click "Plot" to see the 3D waterfall visualization.</p>
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

.control-panel {
  display: flex;
  gap: 15px;
  flex-wrap: wrap;
  position: absolute;
  top: 10px;
  left: 10px;
  background: rgba(40, 40, 40, 0.9);
  padding: 10px;
  border-radius: 6px;
  z-index: 10;
  backdrop-filter: blur(5px);
}
</style>
