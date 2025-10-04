<script setup>
// ============================================================================
// IMPORTS
// ============================================================================
import { computed } from 'vue';

// ============================================================================
// PROPS
// ============================================================================
const props = defineProps({
  data: Object,
  isLoading: Boolean,
  error: String,
  isVisible: Boolean,
  selectedBands: Number,
  bandsOptions: Array
});

// ============================================================================
// EMITS
// ============================================================================
const emit = defineEmits(['toggle', 'update:selectedBands', 'refetch']);

// ============================================================================
// COMPUTED
// ============================================================================
const tableData = computed(() => {
  if (!props.data?.parameters) return [];
  
  const params = props.data.parameters;
  return Object.keys(params)
    .sort((a, b) => Number(a) - Number(b)) // Sort frequencies numerically
    .map(freq => ({
      frequency: freq,
      ...params[freq]
    }));
});

const parameterNames = [
  { key: 'EDT', label: 'EDT (s)', description: 'Early Decay Time' },
  { key: 'T60_from_T20', label: 'T20 (s)', description: 'Reverberation Time from T20' },
  { key: 'T60_from_T30', label: 'T30 (s)', description: 'Reverberation Time from T30' },
  { key: 'C80', label: 'C80 (dB)', description: 'Clarity Index' },
  { key: 'D50', label: 'D50 (%)', description: 'Definition' }
];

// ============================================================================
// METHODS
// ============================================================================
const handleBandsChange = (value) => {
  emit('update:selectedBands', value);
  emit('refetch');
};
</script>

<template>
  <div class="tab-content">
    <div class="controls">
      <div class="control-group">
        <label for="bands-select">Band Type:</label>
        <select 
          id="bands-select" 
          :value="selectedBands"
          @change="handleBandsChange(Number($event.target.value))"
        >
          <option v-for="option in bandsOptions" :key="option.value" :value="option.value">
            {{ option.label }}
          </option>
        </select>
      </div>
      <button @click="emit('toggle')" :disabled="isLoading">
        {{ isVisible ? 'Clear' : 'Show Parameters' }}
      </button>
    </div>
    
    <div class="content-container">
      <div v-if="isLoading" class="status-message">
        <p>Loading Acoustical Parameters...</p>
      </div>
      <div v-else-if="error" class="status-message error">
        <p>{{ error }}</p>
      </div>
      <div v-else-if="isVisible" class="table-wrapper">
        <div class="table-header">
          <h3>Acoustical Parameters</h3>
          <p class="subtitle">{{ selectedBands === 1 ? 'Octave Band' : '1/3 Octave Band' }} Analysis</p>
        </div>
        
        <div class="table-container">
          <table class="parameters-table">
            <thead>
              <tr>
                <th class="freq-column">Frequency (Hz)</th>
                <th v-for="param in parameterNames" :key="param.key" :title="param.description">
                  {{ param.label }}
                </th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="row in tableData" :key="row.frequency">
                <td class="freq-column">{{ row.frequency }}</td>
                <td v-for="param in parameterNames" :key="param.key">
                  {{ row[param.key]?.toFixed(2) ?? 'N/A' }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        
        <div class="legend">
          <h4>Parameter Descriptions:</h4>
          <ul>
            <li><strong>EDT:</strong> Early Decay Time - Time for sound to decay 10 dB from initial level</li>
            <li><strong>T20:</strong> Reverberation Time extrapolated from 5-25 dB decay</li>
            <li><strong>T30:</strong> Reverberation Time extrapolated from 5-35 dB decay</li>
            <li><strong>C80:</strong> Clarity Index - Ratio of early (0-80ms) to late energy</li>
            <li><strong>D50:</strong> Definition - Percentage of energy in first 50ms</li>
          </ul>
        </div>
      </div>
      <div v-else class="status-message">
        <p>Click "Show Parameters" to see the acoustical analysis.</p>
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

.content-container {
  padding: 1rem;
  background-color: #242424;
  border-radius: 8px;
  min-height: 420px;
}

.status-message {
  color: #a0a0a0;
  font-size: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 400px;
}

.error {
  color: #f87171;
}

.table-wrapper {
  width: 100%;
}

.table-header {
  text-align: center;
  margin-bottom: 1.5rem;
}

.table-header h3 {
  color: #e0e0e0;
  font-size: 1.5rem;
  margin: 0 0 0.5rem 0;
}

.subtitle {
  color: #a0a0a0;
  font-size: 0.9rem;
  margin: 0;
}

.table-container {
  overflow-x: auto;
  margin-bottom: 2rem;
}

.parameters-table {
  width: 100%;
  border-collapse: collapse;
  background-color: #1a1a1a;
  border-radius: 8px;
  overflow: hidden;
}

.parameters-table thead {
  background-color: #2a2a2a;
}

.parameters-table th {
  padding: 12px 16px;
  text-align: left;
  color: #e0e0e0;
  font-weight: 600;
  font-size: 0.9rem;
  border-bottom: 2px solid #3a3a3a;
  white-space: nowrap;
}

.parameters-table td {
  padding: 10px 16px;
  color: #c0c0c0;
  font-size: 0.9rem;
  border-bottom: 1px solid #2a2a2a;
}

.parameters-table tbody tr:hover {
  background-color: #2a2a2a;
}

.parameters-table tbody tr:last-child td {
  border-bottom: none;
}

.freq-column {
  font-weight: 600;
  color: #3b82f6;
  min-width: 120px;
}

.legend {
  background-color: #1a1a1a;
  border-radius: 8px;
  padding: 1.5rem;
  border-left: 4px solid #3b82f6;
}

.legend h4 {
  color: #e0e0e0;
  font-size: 1rem;
  margin: 0 0 1rem 0;
}

.legend ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.legend li {
  color: #a0a0a0;
  font-size: 0.85rem;
  margin-bottom: 0.5rem;
  line-height: 1.5;
}

.legend li:last-child {
  margin-bottom: 0;
}

.legend strong {
  color: #3b82f6;
  font-weight: 600;
}

/* Responsive design */
@media (max-width: 768px) {
  .table-container {
    font-size: 0.8rem;
  }
  
  .parameters-table th,
  .parameters-table td {
    padding: 8px 10px;
  }
}
</style>
