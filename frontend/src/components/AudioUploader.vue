<script setup>
import { ref, computed, onMounted } from 'vue';
import ApiService from '@/services/ApiService.js';

// Source selection
const audioSource = ref('example');
const selectedFile = ref(null);
const selectedExampleIR = ref('clifford_tower_ir.wav');
const isLoading = ref(false);
const uploadStatus = ref('');
const uploadError = ref(false);
const emit = defineEmits(['upload-success', 'example-selected']);

// Example IR files
const exampleIRs = ref([
  { name: 'Clifford Tower', filename: 'clifford_tower_ir.wav' },
  { name: 'Marble Hall', filename: '1a_marble_hall.mp3' }
]);

// Audio preview
const audioPreviewUrl = ref('');
const isLoadingPreview = ref(false);


const handleFileChange = (event) => {
  selectedFile.value = event.target.files[0];
  uploadStatus.value = '';
  uploadError.value = false;
  loadPreview();
};

const handleSourceChange = () => {
  selectedFile.value = null;
  selectedExampleIR.value = '';
  uploadStatus.value = '';
  uploadError.value = false;
  clearPreview();
};

const handleExampleSelect = () => {
  uploadStatus.value = '';
  uploadError.value = false;
  loadPreview();
};

const uploadFile = async () => {
  if (!selectedFile.value) return;

  isLoading.value = true;
  uploadStatus.value = 'Uploading file...';
  uploadError.value = false;

  try {
    const response = await ApiService.uploadFile(selectedFile.value);
    uploadStatus.value = `Success! File "${response.data.filename}" uploaded.`;
    emit('upload-success', response.data.path);
  } catch (err) {
    uploadError.value = true;
    uploadStatus.value = 'Error uploading the file.';
    console.error(err);
  } finally {
    isLoading.value = false;
  }
};

const processExample = () => {
  if (!selectedExampleIR.value) return;
  
  uploadStatus.value = `Using example: ${getExampleName()}`;
  emit('example-selected', selectedExampleIR.value);
};

const getExampleName = () => {
  const example = exampleIRs.value.find(ir => ir.filename === selectedExampleIR.value);
  return example ? example.name : selectedExampleIR.value;
};

const loadPreview = () => {
  clearPreview();
  isLoadingPreview.value = true;
  
  try {
    if (audioSource.value === 'example' && selectedExampleIR.value) {
      audioPreviewUrl.value = `/examples/${selectedExampleIR.value}`;
    } else if (selectedFile.value) {
      audioPreviewUrl.value = URL.createObjectURL(selectedFile.value);
    }
  } catch (err) {
    console.error('Failed to load preview:', err);
  } finally {
    isLoadingPreview.value = false;
  }
};

const clearPreview = () => {
  if (audioPreviewUrl.value && audioPreviewUrl.value.startsWith('blob:')) {
    URL.revokeObjectURL(audioPreviewUrl.value);
  }
  audioPreviewUrl.value = '';
};

const canProcess = computed(() => {
  if (audioSource.value === 'example') {
    return selectedExampleIR.value && !isLoading.value;
  } else {
    return selectedFile.value && !isLoading.value;
  }
});

// Load preview on mount for pre-selected example
onMounted(() => {
  if (audioSource.value === 'example' && selectedExampleIR.value) {
    loadPreview();
  }
});
</script>

<template>
  <section class="upload-section">
    <h2>Select Impulse Response</h2>
    
    <!-- Source Selection Radio Buttons -->
    <div class="source-selector">
      <label class="radio-option">
        <input type="radio" value="example" v-model="audioSource" @change="handleSourceChange" />
        <span>Use Example IR</span>
      </label>
      <label class="radio-option">
        <input type="radio" value="upload" v-model="audioSource" @change="handleSourceChange" />
        <span>Upload My IR</span>
      </label>
    </div>
    
    <!-- Example IR Selection -->
    <div v-if="audioSource === 'example'" class="input-group">
      <label for="example-ir" class="input-label">Choose Example</label>
      <select
        id="example-ir"
        v-model="selectedExampleIR"
        @change="handleExampleSelect"
        class="select-input"
      >
        <option value="" disabled>Select an example...</option>
        <option v-for="ir in exampleIRs" :key="ir.filename" :value="ir.filename">
          {{ ir.name }}
        </option>
      </select>
      
      <button @click="processExample" :disabled="!canProcess" class="process-btn">
        Analyze
      </button>
    </div>
    
    <!-- Upload IR -->
    <div v-else class="input-group">
      <label for="file-input" class="input-label">Upload Audio File</label>
      <input
        id="file-input"
        type="file"
        @change="handleFileChange"
        accept="audio/*"
        class="file-input"
      />
      
      <button @click="uploadFile" :disabled="!canProcess" class="process-btn">
        {{ isLoading ? 'Uploading...' : 'Analyze' }}
      </button>
    </div>
    
    <p v-if="uploadStatus" :class="{ 'success': !uploadError, 'error': uploadError }">
      {{ uploadStatus }}
    </p>
  </section>
</template>

<style scoped>
.upload-section {
  background: var(--glass-background);
  backdrop-filter: blur(var(--glass-blur));
  -webkit-backdrop-filter: blur(var(--glass-blur));
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-lg);
  padding: var(--space-md);
  box-shadow: var(--glass-shadow);
  margin-bottom: 0;
  transition: all var(--transition-base);
  position: relative;
}

.upload-section:hover {
  border-color: rgba(255, 255, 255, 0.15);
}

.upload-section h2 {
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-semibold);
  margin-bottom: var(--space-sm);
  color: var(--color-text-primary);
  position: relative;
  z-index: 1;
}

.source-selector {
  display: flex;
  gap: var(--space-md);
  margin-bottom: var(--space-sm);
  padding: var(--space-xs) var(--space-sm);
  background: rgba(31, 33, 35, 0.4);
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  border-radius: var(--radius-md);
  border: 1px solid rgba(255, 255, 255, 0.05);
  position: relative;
  z-index: 1;
}

.radio-option {
  display: flex;
  align-items: center;
  gap: var(--space-xs);
  cursor: pointer;
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  color: var(--color-text-secondary);
  transition: all var(--transition-base);
  padding: var(--space-xs) var(--space-sm);
  border-radius: var(--radius-md);
}

.radio-option:hover {
  color: var(--color-text-primary);
  background: rgba(255, 255, 255, 0.03);
}

.radio-option input[type="radio"] {
  width: 18px;
  height: 18px;
  cursor: pointer;
  accent-color: var(--color-primary);
}

.radio-option:has(input:checked) {
  color: var(--color-primary-light);
  background: rgba(47, 9, 136, 0.1);
}

.input-group {
  animation: fadeIn 0.4s ease;
  position: relative;
  z-index: 1;
}

.input-label {
  display: block;
  font-weight: var(--font-weight-semibold);
  margin-bottom: var(--space-sm);
  color: var(--color-text-primary);
  font-size: var(--font-size-sm);
}

.select-input {
  width: 100%;
  padding: var(--space-sm);
  background: var(--color-surface-elevated);
  color: var(--color-text-primary);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-md);
  font-size: var(--font-size-sm);
  cursor: pointer;
  transition: all var(--transition-base);
  margin-bottom: var(--space-sm);
  font-weight: var(--font-weight-medium);
}

.select-input:hover {
  border-color: var(--color-border-lighter);
  background: var(--color-surface-hover);
}

.select-input:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(47, 9, 136, 0.15);
}

.file-input {
  width: 100%;
  padding: var(--space-sm);
  background: var(--color-surface-elevated);
  color: var(--color-text-primary);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-md);
  font-size: var(--font-size-sm);
  cursor: pointer;
  margin-bottom: var(--space-sm);
  transition: all var(--transition-base);
}

.file-input:hover {
  border-color: var(--color-border-lighter);
}

.file-input::-webkit-file-upload-button {
  background: linear-gradient(135deg, var(--color-primary), var(--color-primary-hover));
  color: white;
  padding: var(--space-sm) var(--space-md);
  border: none;
  border-radius: var(--radius-md);
  cursor: pointer;
  font-weight: var(--font-weight-semibold);
  margin-right: var(--space-md);
  transition: all var(--transition-base);
}

.file-input::-webkit-file-upload-button:hover {
  transform: scale(1.02);
  box-shadow: 0 4px 12px rgba(47, 9, 136, 0.3);
}

.process-btn {
  width: 100%;
  padding: var(--space-sm) var(--space-md);
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-semibold);
  border-radius: var(--radius-md);
  border: none;
  cursor: pointer;
  transition: all var(--transition-base);
  background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-hover) 100%);
  color: white;
  box-shadow: 0 2px 8px rgba(47, 9, 136, 0.3);
  position: relative;
  overflow: hidden;
}

.process-btn::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  transform: translate(-50%, -50%);
  transition: width 0.6s, height 0.6s;
}

.process-btn:hover:not(:disabled)::before {
  width: 300px;
  height: 300px;
}

.process-btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(47, 9, 136, 0.4);
}

.process-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}

.success {
  color: var(--color-success);
  font-weight: var(--font-weight-semibold);
  margin-top: var(--space-md);
  font-size: var(--font-size-sm);
  text-align: center;
  animation: fadeIn 0.3s ease;
}

.error {
  color: var(--color-error);
  font-weight: var(--font-weight-semibold);
  margin-top: var(--space-md);
  font-size: var(--font-size-sm);
  text-align: center;
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes float {
  0%, 100% {
    transform: translate(0, 0) rotate(0deg);
  }
  33% {
    transform: translate(30px, -30px) rotate(120deg);
  }
  66% {
    transform: translate(-20px, 20px) rotate(240deg);
  }
}

@media (max-width: 768px) {
  .source-selector {
    flex-direction: column;
    gap: var(--space-sm);
  }

  .upload-section {
    padding: var(--space-sm);
  }
}
</style>