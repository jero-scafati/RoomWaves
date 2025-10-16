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
const emit = defineEmits(['update:dataReduction', 'update:bands']);
</script>

<template>
  <div class="tab-content">
    
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
                @change="emit('update:bands', Number($event.target.value))"
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
        <p>Loading 3D surface data...</p>
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

.control-group {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
}

label {
  color: var(--color-text-secondary);
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  white-space: nowrap;
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

.control-panel {
  display: flex;
  gap: var(--space-md);
  flex-wrap: wrap;
  position: absolute;
  top: var(--space-md);
  left: var(--space-md);
  background: rgba(5, 14, 20, 0.85);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  padding: var(--space-md);
  border-radius: var(--radius-lg);
  border: 1px solid rgba(255, 255, 255, 0.1);
  z-index: 10;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4);
  transition: all var(--transition-base);
}

.control-panel:hover {
  background: rgba(5, 14, 20, 0.95);
  border-color: rgba(255, 255, 255, 0.15);
}
</style>
