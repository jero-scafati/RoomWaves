<script setup>
import { ref, computed } from 'vue';

// ============================================================================
// PROPS
// ============================================================================
const props = defineProps({
  currentIRPath: {
    type: String,
    default: ''
  }
});

// ============================================================================
// STATE
// ============================================================================
const dryAudioSource = ref('example');
const selectedExampleAudio = ref('');
const uploadedDryAudioFile = ref(null);

const isProcessing = ref(false);
const processingStatus = ref('');
const convolvedAudioUrl = ref('');
const error = ref('');

const dryAudioPreviewUrl = ref('');
const irPreviewUrl = ref('');

const exampleAudios = ref([
  { name: 'Drums', filename: 'drums.wav' },
  { name: 'Trumpet', filename: 'trumpet.wav' }
]);

const exampleIRs = ref([
  { name: 'Clifford Tower', filename: 'clifford_tower_ir.wav' },
  { name: 'Marble Hall', filename: '1a_marble_hall.mp3' }
]);

// ============================================================================
// COMPUTED
// ============================================================================
const canConvolve = computed(() => {
  if (isProcessing.value) return false;
  const hasDryAudio = dryAudioSource.value === 'example' ? selectedExampleAudio.value : uploadedDryAudioFile.value;
  const hasIR = props.currentIRPath && props.currentIRPath.length > 0;
  return hasDryAudio && hasIR;
});

const currentIRName = computed(() => {
  if (!props.currentIRPath || props.currentIRPath.length === 0) return 'No IR loaded';
  const filename = props.currentIRPath.split('/').pop();
  if (filename === 'clifford_tower_ir.wav') return 'Clifford Tower';
  if (filename === '1a_marble_hall.mp3') return 'Marble Hall';
  return filename;
});

// ============================================================================
// METHODS
// ============================================================================
const handleDryAudioFileSelect = (event) => {
  const file = event.target.files[0];
  error.value = '';
  
  if (!file) {
    uploadedDryAudioFile.value = null;
    clearDryAudioPreview();
    return;
  }
  
  if (file.size > 50 * 1024 * 1024) {
    error.value = 'Dry audio file exceeds 50MB limit.';
    uploadedDryAudioFile.value = null;
    event.target.value = '';
    return;
  }
  
  uploadedDryAudioFile.value = file;
  loadDryAudioPreview();
};


const loadDryAudioPreview = async () => {
  clearDryAudioPreview();
  try {
    if (dryAudioSource.value === 'example' && selectedExampleAudio.value) {
      dryAudioPreviewUrl.value = `/examples/${selectedExampleAudio.value}`;
    } else if (uploadedDryAudioFile.value) {
      dryAudioPreviewUrl.value = URL.createObjectURL(uploadedDryAudioFile.value);
    }
  } catch (err) {
    console.error('Failed to load dry audio preview:', err);
  }
};


const clearDryAudioPreview = () => {
  if (dryAudioPreviewUrl.value && dryAudioPreviewUrl.value.startsWith('blob:')) {
    URL.revokeObjectURL(dryAudioPreviewUrl.value);
  }
  dryAudioPreviewUrl.value = '';
};


const handleDryAudioSourceChange = () => {
  clearDryAudioPreview();
  selectedExampleAudio.value = '';
  uploadedDryAudioFile.value = null;
};


const loadAudio = async (source, context) => {
  if (typeof source === 'string') {
    const response = await fetch(source);
    if (!response.ok) throw new Error('Failed to load audio file');
    const arrayBuffer = await response.arrayBuffer();
    return await context.decodeAudioData(arrayBuffer);
  } else {
    const arrayBuffer = await source.arrayBuffer();
    return await context.decodeAudioData(arrayBuffer);
  }
};

const audioBufferToWav = (audioBuffer) => {
  const numOfChannels = audioBuffer.numberOfChannels;
  const sampleRate = audioBuffer.sampleRate;
  const length = audioBuffer.length * numOfChannels * 2 + 44;
  const buffer = new ArrayBuffer(length);
  const view = new DataView(buffer);
  const channels = [];
  let pos = 0;

  const setUint16 = (data) => { view.setUint16(pos, data, true); pos += 2; };
  const setUint32 = (data) => { view.setUint32(pos, data, true); pos += 4; };

  setUint32(0x46464952); setUint32(length - 8); setUint32(0x45564157);
  setUint32(0x20746d66); setUint32(16); setUint16(1); setUint16(numOfChannels);
  setUint32(sampleRate); setUint32(sampleRate * numOfChannels * 2);
  setUint16(numOfChannels * 2); setUint16(16);
  setUint32(0x61746164); setUint32(length - pos - 4);

  for (let i = 0; i < audioBuffer.numberOfChannels; i++) {
    channels.push(audioBuffer.getChannelData(i));
  }

  let offset = 0;
  while (pos < length) {
    for (let i = 0; i < numOfChannels; i++) {
      let sample = Math.max(-1, Math.min(1, channels[i][offset]));
      sample = sample < 0 ? sample * 0x8000 : sample * 0x7FFF;
      view.setInt16(pos, sample, true);
      pos += 2;
    }
    offset++;
  }

  return new Blob([buffer], { type: 'audio/wav' });
};

const convolveAudio = async () => {
  if (!canConvolve.value) return;
  
  isProcessing.value = true;
  error.value = '';
  processingStatus.value = 'Processing...';
  
  try {
    const audioContext = new AudioContext();
    
    const drySource = dryAudioSource.value === 'example' 
      ? `/examples/${selectedExampleAudio.value}` 
      : uploadedDryAudioFile.value;
    const irSourceUrl = `/${props.currentIRPath}`;
    
    const dryBuffer = await loadAudio(drySource, audioContext);
    const irBuffer = await loadAudio(irSourceUrl, audioContext);
    
    const offlineContext = new OfflineAudioContext(
      dryBuffer.numberOfChannels,
      dryBuffer.length,
      dryBuffer.sampleRate
    );
    
    const sourceNode = offlineContext.createBufferSource();
    const convolverNode = offlineContext.createConvolver();
    
    sourceNode.buffer = dryBuffer;
    convolverNode.buffer = irBuffer;
    
    sourceNode.connect(convolverNode);
    convolverNode.connect(offlineContext.destination);
    sourceNode.start(0);
    
    const renderedBuffer = await offlineContext.startRendering();
    const wavBlob = audioBufferToWav(renderedBuffer);
    
    if (convolvedAudioUrl.value) {
      URL.revokeObjectURL(convolvedAudioUrl.value);
    }
    convolvedAudioUrl.value = URL.createObjectURL(wavBlob);
    processingStatus.value = 'Complete!';
    
  } catch (err) {
    console.error('Convolution error:', err);
    error.value = err.message || 'An error occurred during processing.';
    processingStatus.value = '';
  } finally {
    isProcessing.value = false;
  }
};

const downloadAudio = () => {
  if (!convolvedAudioUrl.value) return;
  
  const link = document.createElement('a');
  link.href = convolvedAudioUrl.value;
  link.download = 'convolved_audio.wav';
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};
</script>

<template>
  <div class="tab-content">
    <div v-if="!currentIRPath || currentIRPath.length === 0" class="no-ir-message">
      <p>Please load an impulse response first to use convolution.</p>
    </div>
    
    <div v-else class="convolution-grid">
      <!-- Current IR Info -->
      <div class="ir-info-card">
        <h3 class="card-title">Current Impulse Response</h3>
        <p class="ir-name">{{ currentIRName }}</p>
        <audio v-if="currentIRPath" :src="`/${currentIRPath}`" controls class="audio-preview"></audio>
      </div>

      <!-- Dry Audio -->
      <div class="input-card">
        <h3 class="card-title">Select Dry Audio</h3>
        <div class="source-selector">
          <label class="radio-option">
            <input type="radio" value="example" v-model="dryAudioSource" @change="handleDryAudioSourceChange" />
            <span>Example</span>
          </label>
          <label class="radio-option">
            <input type="radio" value="upload" v-model="dryAudioSource" @change="handleDryAudioSourceChange" />
            <span>Upload</span>
          </label>
        </div>
        
        <div v-if="dryAudioSource === 'example'">
          <select v-model="selectedExampleAudio" @change="loadDryAudioPreview" class="select-input">
            <option value="" disabled>Select...</option>
            <option v-for="audio in exampleAudios" :key="audio.filename" :value="audio.filename">
              {{ audio.name }}
            </option>
          </select>
        </div>
        <div v-else>
          <input type="file" @change="handleDryAudioFileSelect" accept="audio/*" class="file-input" />
        </div>
        
        <audio v-if="dryAudioPreviewUrl" :src="dryAudioPreviewUrl" controls class="audio-preview"></audio>
      </div>

      <!-- Process Button -->
      <div class="action-card">
        <button @click="convolveAudio" :disabled="!canConvolve" class="convolve-btn">
          {{ isProcessing ? 'Processing...' : 'Convolve Audio' }}
        </button>
        
        <div v-if="error" class="error-message">{{ error }}</div>
        <div v-if="processingStatus && !error" class="status-message">{{ processingStatus }}</div>
      </div>

      <!-- Result -->
      <div v-if="convolvedAudioUrl" class="result-card">
        <h3 class="card-title">Result</h3>
        <audio :src="convolvedAudioUrl" controls class="audio-preview"></audio>
        <button @click="downloadAudio" class="download-btn">Download</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.tab-content {
  animation: fadeIn 0.4s ease;
  padding: var(--space-md);
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

.no-ir-message {
  text-align: center;
  padding: var(--space-2xl);
  color: var(--color-text-secondary);
  font-size: var(--font-size-lg);
}

.convolution-grid {
  display: grid;
  gap: var(--space-md);
  max-width: 800px;
  margin: 0 auto;
}

.ir-info-card,
.input-card,
.action-card,
.result-card {
  padding: var(--space-lg);
  background: rgba(24, 26, 27, 0.4);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: var(--radius-lg);
  transition: all var(--transition-base);
}

.ir-info-card:hover,
.input-card:hover,
.result-card:hover {
  border-color: rgba(255, 255, 255, 0.12);
  background: rgba(24, 26, 27, 0.5);
}

.ir-name {
  font-size: var(--font-size-lg);
  color: var(--color-primary-text);
  font-weight: var(--font-weight-semibold);
  margin-bottom: var(--space-sm);
}

.card-title {
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-primary);
  margin: 0 0 var(--space-md) 0;
}

.source-selector {
  display: flex;
  gap: var(--space-md);
  margin-bottom: var(--space-sm);
  padding: var(--space-xs) var(--space-sm);
  background: rgba(31, 33, 35, 0.4);
  border-radius: var(--radius-md);
}

.radio-option {
  display: flex;
  align-items: center;
  gap: var(--space-xs);
  cursor: pointer;
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  transition: all var(--transition-base);
}

.radio-option:hover {
  color: var(--color-text-primary);
}

.radio-option input[type="radio"] {
  cursor: pointer;
  accent-color: var(--color-primary);
}

.select-input {
  width: 100%;
  padding: var(--space-sm);
  background: var(--color-surface-elevated);
  color: var(--color-text-primary);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-md);
  font-size: var(--font-size-sm);
  margin-bottom: var(--space-sm);
}

.file-input {
  width: 100%;
  padding: var(--space-sm);
  background: var(--color-surface-elevated);
  color: var(--color-text-primary);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-md);
  font-size: var(--font-size-sm);
  margin-bottom: var(--space-sm);
}

.audio-preview {
  width: 100%;
  margin-top: var(--space-sm);
  border-radius: var(--radius-md);
}

.convolve-btn,
.download-btn {
  width: 100%;
  padding: var(--space-md);
  background: linear-gradient(135deg, var(--color-primary), var(--color-primary-hover));
  color: white;
  border: none;
  border-radius: var(--radius-md);
  font-weight: var(--font-weight-semibold);
  cursor: pointer;
  transition: all var(--transition-base);
}

.convolve-btn:hover:not(:disabled),
.download-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(47, 9, 136, 0.4);
}

.convolve-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}

.download-btn {
  margin-top: var(--space-sm);
  background: linear-gradient(135deg, #10b981, #059669);
}

.error-message {
  margin-top: var(--space-sm);
  color: var(--color-error);
  font-size: var(--font-size-sm);
  text-align: center;
}

.status-message {
  margin-top: var(--space-sm);
  color: var(--color-success);
  font-size: var(--font-size-sm);
  text-align: center;
  font-weight: var(--font-weight-medium);
}
</style>
