<script setup>
import { ref, computed } from 'vue';
import ApiService from '@/services/ApiService.js';

// Source selection
const audioSource = ref('upload');
const selectedFile = ref(null);
const selectedExampleIR = ref('');
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
    emit('upload-success', response.data.filename);
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
      
      <!-- Audio Preview -->
      <div v-if="audioPreviewUrl" class="audio-preview">
        <label class="preview-label">🎵 Preview:</label>
        <audio :src="audioPreviewUrl" controls class="preview-audio"></audio>
      </div>
      
      <button @click="processExample" :disabled="!canProcess" class="process-btn">
        Analyze Example
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
      
      <!-- Audio Preview -->
      <div v-if="audioPreviewUrl" class="audio-preview">
        <label class="preview-label">🎵 Preview:</label>
        <audio :src="audioPreviewUrl" controls class="preview-audio"></audio>
      </div>
      
      <button @click="uploadFile" :disabled="!canProcess" class="process-btn">
        {{ isLoading ? 'Uploading...' : 'Upload and Analyze' }}
      </button>
    </div>
    
    <p v-if="uploadStatus" :class="{ 'success': !uploadError, 'error': uploadError }">
      {{ uploadStatus }}
    </p>
  </section>
</template>

<style scoped>
.upload-section {
  background-color: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  padding: var(--space-xl);
  box-shadow: var(--shadow-md);
  margin-bottom: var(--space-xl);
}

.upload-section h2 {
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-semibold);
  margin-bottom: var(--space-lg);
  color: var(--color-text-primary);
}

.source-selector {
  display: flex;
  gap: var(--space-lg);
  margin-bottom: var(--space-lg);
  padding: var(--space-md);
  background-color: var(--color-surface-elevated);
  border-radius: var(--radius-lg);
}

.radio-option {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  cursor: pointer;
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-medium);
  color: var(--color-text-primary);
  transition: color var(--transition-base);
}

.radio-option input[type="radio"] {
  width: 18px;
  height: 18px;
  cursor: pointer;
  accent-color: var(--color-primary);
}

.radio-option:has(input:checked) {
  color: var(--color-primary);
}

.input-group {
  animation: fadeIn var(--transition-base);
}

.input-label {
  display: block;
  font-weight: var(--font-weight-medium);
  margin-bottom: var(--space-sm);
  color: var(--color-text-primary);
}

.select-input {
  width: 100%;
  padding: var(--space-md);
  background-color: var(--color-surface-elevated);
  color: var(--color-text-primary);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-md);
  font-size: var(--font-size-base);
  cursor: pointer;
  transition: border-color var(--transition-base);
  margin-bottom: var(--space-md);
}

.select-input:hover {
  border-color: var(--color-border-lighter);
}

.select-input:focus {
  outline: none;
  border-color: var(--color-primary);
}

.file-input {
  width: 100%;
  padding: var(--space-md);
  background-color: var(--color-surface-elevated);
  color: var(--color-text-primary);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-md);
  font-size: var(--font-size-base);
  cursor: pointer;
  margin-bottom: var(--space-md);
}

.file-input::-webkit-file-upload-button {
  background-color: var(--color-primary);
  color: white;
  padding: var(--space-sm) var(--space-md);
  border: none;
  border-radius: var(--radius-md);
  cursor: pointer;
  font-weight: var(--font-weight-medium);
  margin-right: var(--space-md);
}

.file-input::-webkit-file-upload-button:hover {
  background-color: var(--color-primary-hover);
}

.audio-preview {
  margin-bottom: var(--space-md);
  padding: var(--space-md);
  background-color: var(--color-surface-elevated);
  border-radius: var(--radius-md);
  border: 1px solid var(--color-border-light);
}

.preview-label {
  display: block;
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  color: var(--color-text-secondary);
  margin-bottom: var(--space-sm);
}

.preview-audio {
  width: 100%;
  height: 40px;
  border-radius: var(--radius-md);
  background-color: var(--color-surface);
}

.process-btn {
  width: 100%;
  padding: var(--space-md) var(--space-xl);
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-semibold);
  border-radius: var(--radius-lg);
  border: none;
  cursor: pointer;
  transition: all var(--transition-base);
  background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-hover) 100%);
  color: white;
}

.process-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: var(--shadow-glow);
}

.process-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}

.success {
  color: var(--color-success);
  font-weight: var(--font-weight-medium);
  margin-top: var(--space-md);
}

.error {
  color: var(--color-error);
  font-weight: var(--font-weight-medium);
  margin-top: var(--space-md);
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

@media (max-width: 768px) {
  .source-selector {
    flex-direction: column;
    gap: var(--space-md);
  }
}
</style>