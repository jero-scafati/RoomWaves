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
const emit = defineEmits(['update:selectedBands']);

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
  { key: 'C50', label: 'C50 (dB)', description: 'Clarity Index' },
  { key: 'D50', label: 'D50 (%)', description: 'Definition' }
];

// ============================================================================
// METHODS
// ============================================================================
const handleBandsChange = (value) => {
  emit('update:selectedBands', value);
};

const downloadCSV = () => {
  if (!tableData.value.length) return;
  
  // Create CSV header
  const headers = ['Frequency (Hz)', ...parameterNames.map(p => p.label)];
  const csvContent = [
    headers.join(','),
    ...tableData.value.map(row => {
      const values = [
        row.frequency,
        ...parameterNames.map(param => row[param.key]?.toFixed(2) ?? 'N/A')
      ];
      return values.join(',');
    })
  ].join('\n');
  
  // Download the file
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
  const link = document.createElement('a');
  const url = URL.createObjectURL(blob);
  const bandType = props.selectedBands === 1 ? 'octave' : 'third-octave';
  link.setAttribute('href', url);
  link.setAttribute('download', `acoustical-parameters-${bandType}.csv`);
  link.style.visibility = 'hidden';
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};

const downloadPDF = async () => {
  if (!tableData.value.length) return;
  
  try {
    // Dynamically import jsPDF
    const { jsPDF } = await import('jspdf');
    await import('jspdf-autotable');
    
    const doc = new jsPDF();
    const bandType = props.selectedBands === 1 ? 'Octave Band' : '1/3 Octave Band';
    
    // Add title
    doc.setFontSize(16);
    doc.text('Acoustical Parameters', 14, 15);
    doc.setFontSize(11);
    doc.text(`${bandType} Analysis`, 14, 22);
    
    // Prepare table data
    const headers = [['Frequency (Hz)', ...parameterNames.map(p => p.label)]];
    const body = tableData.value.map(row => [
      row.frequency,
      ...parameterNames.map(param => row[param.key]?.toFixed(2) ?? 'N/A')
    ]);
    
    // Add table
    doc.autoTable({
      head: headers,
      body: body,
      startY: 28,
      theme: 'grid',
      styles: { fontSize: 9, cellPadding: 3 },
      headStyles: { fillColor: [59, 130, 246], fontStyle: 'bold' },
      alternateRowStyles: { fillColor: [245, 245, 245] }
    });
    
    // Download the file
    const filename = `acoustical-parameters-${bandType.toLowerCase().replace(' ', '-')}.pdf`;
    doc.save(filename);
  } catch (error) {
    console.error('Error generating PDF:', error);
    alert('Error generating PDF. Please make sure jsPDF is installed.');
  }
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
      
      <div v-if="isVisible" class="download-buttons">
        <button @click="downloadCSV" class="download-btn csv-btn" :disabled="isLoading">
          Download CSV
        </button>
        <button @click="downloadPDF" class="download-btn pdf-btn" :disabled="isLoading">
          Download PDF
        </button>
      </div>
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
            <li><strong>C50:</strong> Clarity Index - Ratio of early (0-50ms) to late energy</li>
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

.download-buttons {
  display: flex;
  gap: var(--space-sm);
  flex-wrap: wrap;
}

.content-container {
  padding: var(--space-md);
  background: transparent;
  border: none;
  border-radius: var(--radius-lg);
  min-height: 420px;
  position: relative;
}

.table-wrapper {
  width: 100%;
  position: relative;
  z-index: 1;
}

.table-container {
  overflow-x: auto;
  margin-bottom: var(--space-xl);
  border-radius: var(--radius-md);
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

.download-btn {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  color: white;
  border: none;
  padding: var(--space-sm) var(--space-lg);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--transition-base);
  font-weight: var(--font-weight-semibold);
  font-size: var(--font-size-sm);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.download-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.download-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}

.csv-btn {
  background: linear-gradient(135deg, #10b981, #059669);
}

.csv-btn:hover:not(:disabled) {
  box-shadow: 0 4px 16px rgba(16, 185, 129, 0.4);
}

.pdf-btn {
  background: linear-gradient(135deg, #ef4444, #dc2626);
}

.pdf-btn:hover:not(:disabled) {
  box-shadow: 0 4px 16px rgba(239, 68, 68, 0.4);
}

.table-header {
  text-align: center;
  margin-bottom: var(--space-xl);
}

.table-header h3 {
  color: var(--color-text-primary);
  font-size: var(--font-size-2xl);
  margin: 0 0 var(--space-sm) 0;
  font-weight: var(--font-weight-bold);
}

.subtitle {
  color: var(--color-text-secondary);
  font-size: var(--font-size-base);
  margin: 0;
  font-weight: var(--font-weight-medium);
}

.status-message {
  color: var(--color-text-secondary);
  font-size: var(--font-size-base);
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  font-weight: var(--font-weight-medium);
}

.error {
  color: var(--color-error);
}

.parameters-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  background: rgba(26, 26, 27, 0.6);
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  border-radius: var(--radius-md);
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.parameters-table thead {
  background: linear-gradient(135deg, rgba(47, 9, 136, 0.15), rgba(69, 16, 184, 0.1));
}

.parameters-table th {
  padding: var(--space-md) var(--space-lg);
  text-align: left;
  color: var(--color-text-primary);
  font-weight: var(--font-weight-semibold);
  font-size: var(--font-size-sm);
  border-bottom: 2px solid rgba(47, 9, 136, 0.3);
  white-space: nowrap;
  position: sticky;
  top: 0;
  background: inherit;
  z-index: 10;
}

.parameters-table td {
  padding: var(--space-md) var(--space-lg);
  color: var(--color-text-secondary);
  font-size: var(--font-size-sm);
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  transition: all var(--transition-fast);
}

.parameters-table tbody tr {
  transition: all var(--transition-fast);
}

.parameters-table tbody tr:hover {
  background: rgba(47, 9, 136, 0.08);
}

.parameters-table tbody tr:hover td {
  color: var(--color-text-primary);
}

.parameters-table tbody tr:last-child td {
  border-bottom: none;
}

.freq-column {
  font-weight: var(--font-weight-semibold);
  color: var(--color-primary-light);
  min-width: 120px;
}

.legend {
  background: rgba(26, 26, 27, 0.6);
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  border-radius: var(--radius-md);
  padding: var(--space-lg);
  border-left: 3px solid var(--color-primary);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  transition: all var(--transition-base);
}

.legend:hover {
  background: rgba(26, 26, 27, 0.7);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.legend h4 {
  color: var(--color-text-primary);
  font-size: var(--font-size-lg);
  margin: 0 0 var(--space-md) 0;
  font-weight: var(--font-weight-semibold);
}

.legend ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.legend li {
  color: var(--color-text-secondary);
  font-size: var(--font-size-sm);
  margin-bottom: var(--space-sm);
  line-height: var(--line-height-relaxed);
  padding-left: var(--space-md);
  position: relative;
}

.legend li::before {
  content: '▸';
  position: absolute;
  left: 0;
  color: var(--color-primary-light);
  font-size: var(--font-size-sm);
}

.legend li:last-child {
  margin-bottom: 0;
}

.legend strong {
  color: var(--color-primary-light);
  font-weight: var(--font-weight-semibold);
}

@media (max-width: 768px) {
  .controls {
    flex-direction: column;
    gap: var(--space-md);
  }
  
  .download-buttons {
    justify-content: center;
    width: 100%;
  }
  
  .download-btn {
    flex: 1;
  }
  
  .table-container {
    font-size: var(--font-size-xs);
  }
  
  .parameters-table th,
  .parameters-table td {
    padding: var(--space-sm) var(--space-md);
  }

  .content-container {
    padding: var(--space-md);
  }
}
</style>
