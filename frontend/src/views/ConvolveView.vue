<script setup>
import { ref, computed, onMounted } from 'vue';
import ApiService from '@/services/ApiService.js';

// ============================================================================
// STATE
// ============================================================================
// Dry audio (source)
const dryAudioSource = ref('example'); // 'example' or 'upload'
const selectedExampleAudio = ref('');
const uploadedDryAudioFile = ref(null);

// Impulse response
const irSource = ref('example'); // 'example' or 'upload'
const selectedExampleIR = ref('');
const uploadedIRFile = ref(null);

// Processing
const isProcessing = ref(false);
const processingStatus = ref('');
const convolvedAudioUrl = ref('');
const audioContext = ref(null);
const error = ref('');

// Preview URLs for audio players
const dryAudioPreviewUrl = ref('');
const irPreviewUrl = ref('');
const isLoadingDryPreview = ref(false);
const isLoadingIRPreview = ref(false);

// Example files from R2 bucket
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
  
  // Check dry audio
  const hasDryAudio = dryAudioSource.value === 'example' 
    ? selectedExampleAudio.value 
    : uploadedDryAudioFile.value;
  
  // Check IR
  const hasIR = irSource.value === 'example'
    ? selectedExampleIR.value
    : uploadedIRFile.value;
  
  return hasDryAudio && hasIR;
});

const dryAudioFileSize = computed(() => {
  if (!uploadedDryAudioFile.value) return '';
  const sizeMB = (uploadedDryAudioFile.value.size / (1024 * 1024)).toFixed(2);
  return `${sizeMB} MB`;
});

const irFileSize = computed(() => {
  if (!uploadedIRFile.value) return '';
  const sizeMB = (uploadedIRFile.value.size / (1024 * 1024)).toFixed(2);
  return `${sizeMB} MB`;
});

// ============================================================================
// METHODS - FILE HANDLING
// ============================================================================

/**
 * Handle dry audio file selection (local only, not uploaded)
 */
const handleDryAudioFileSelect = (event) => {
  const file = event.target.files[0];
  error.value = '';
  
  if (!file) {
    uploadedDryAudioFile.value = null;
    clearDryAudioPreview();
    return;
  }
  
  // Validate file size (max 50MB)
  const maxSize = 50 * 1024 * 1024;
  if (file.size > maxSize) {
    error.value = 'Dry audio file exceeds 50MB limit.';
    uploadedDryAudioFile.value = null;
    event.target.value = '';
    return;
  }
  
  // Validate file type
  if (!file.type.startsWith('audio/')) {
    error.value = 'Please select a valid audio file.';
    uploadedDryAudioFile.value = null;
    event.target.value = '';
    return;
  }
  
  uploadedDryAudioFile.value = file;
  // Create preview URL for uploaded file
  loadDryAudioPreview();
};

/**
 * Handle IR file selection
 */
const handleIRFileSelect = (event) => {
  const file = event.target.files[0];
  error.value = '';
  
  if (!file) {
    uploadedIRFile.value = null;
    clearIRPreview();
    return;
  }
  
  // Validate file size (max 20MB for IRs)
  const maxSize = 20 * 1024 * 1024;
  if (file.size > maxSize) {
    error.value = 'IR file exceeds 20MB limit.';
    uploadedIRFile.value = null;
    event.target.value = '';
    return;
  }
  
  // Validate file type
  if (!file.type.startsWith('audio/')) {
    error.value = 'Please select a valid audio file for the IR.';
    uploadedIRFile.value = null;
    event.target.value = '';
    return;
  }
  
  uploadedIRFile.value = file;
  // Create preview URL for uploaded file
  loadIRPreview();
};


// ============================================================================
// METHODS - AUDIO PREVIEW
// ============================================================================

/**
 * Load preview for dry audio (example or uploaded)
 */
const loadDryAudioPreview = async () => {
  clearDryAudioPreview();
  isLoadingDryPreview.value = true;
  
  try {
    if (dryAudioSource.value === 'example' && selectedExampleAudio.value) {
      // Use local example file from public folder
      dryAudioPreviewUrl.value = `/examples/${selectedExampleAudio.value}`;
    } else if (uploadedDryAudioFile.value) {
      // Create object URL for uploaded file
      dryAudioPreviewUrl.value = URL.createObjectURL(uploadedDryAudioFile.value);
    }
  } catch (err) {
    console.error('Failed to load dry audio preview:', err);
    error.value = 'Failed to load audio preview';
  } finally {
    isLoadingDryPreview.value = false;
  }
};

/**
 * Load preview for IR (example or uploaded)
 */
const loadIRPreview = async () => {
  clearIRPreview();
  isLoadingIRPreview.value = true;
  
  try {
    if (irSource.value === 'example' && selectedExampleIR.value) {
      // Use local example file from public folder
      irPreviewUrl.value = `/examples/${selectedExampleIR.value}`;
    } else if (uploadedIRFile.value) {
      // Create object URL for uploaded file
      irPreviewUrl.value = URL.createObjectURL(uploadedIRFile.value);
    }
  } catch (err) {
    console.error('Failed to load IR preview:', err);
    error.value = 'Failed to load IR preview';
  } finally {
    isLoadingIRPreview.value = false;
  }
};

/**
 * Clear dry audio preview URL
 */
const clearDryAudioPreview = () => {
  // Only revoke blob URLs (not local file paths)
  if (dryAudioPreviewUrl.value && dryAudioPreviewUrl.value.startsWith('blob:')) {
    URL.revokeObjectURL(dryAudioPreviewUrl.value);
  }
  dryAudioPreviewUrl.value = '';
};

/**
 * Clear IR preview URL
 */
const clearIRPreview = () => {
  // Only revoke blob URLs (not local file paths)
  if (irPreviewUrl.value && irPreviewUrl.value.startsWith('blob:')) {
    URL.revokeObjectURL(irPreviewUrl.value);
  }
  irPreviewUrl.value = '';
};

/**
 * Handle dry audio source change (example/upload toggle)
 */
const handleDryAudioSourceChange = () => {
  clearDryAudioPreview();
  selectedExampleAudio.value = '';
  uploadedDryAudioFile.value = null;
};

/**
 * Handle IR source change (example/upload toggle)
 */
const handleIRSourceChange = () => {
  clearIRPreview();
  selectedExampleIR.value = '';
  uploadedIRFile.value = null;
};

// ============================================================================
// METHODS - AUDIO PROCESSING
// ============================================================================


/**
 * Get the dry audio source (file path or File object)
 */
const getDryAudioSource = () => {
  if (dryAudioSource.value === 'example') {
    // Return path to local example file
    return `/examples/${selectedExampleAudio.value}`;
  } else {
    // Return uploaded File object
    return uploadedDryAudioFile.value;
  }
};

/**
 * Get the IR source (file path or File object)
 */
const getIRSource = () => {
  if (irSource.value === 'example') {
    // Return path to local example file
    return `/examples/${selectedExampleIR.value}`;
  } else {
    // Return uploaded File object
    return uploadedIRFile.value;
  }
};

/**
 * Load audio from file path or File object
 */
const loadAudio = async (source, context) => {
  if (typeof source === 'string') {
    // It's a URL/path - fetch it
    processingStatus.value = 'Loading example audio...';
    const response = await fetch(source);
    if (!response.ok) {
      throw new Error('Failed to load audio file');
    }
    const arrayBuffer = await response.arrayBuffer();
    return await context.decodeAudioData(arrayBuffer);
  } else {
    // It's a local File object
    processingStatus.value = 'Loading uploaded audio...';
    const arrayBuffer = await source.arrayBuffer();
    return await context.decodeAudioData(arrayBuffer);
  }
};

/**
 * Convert AudioBuffer to WAV file
 */
const audioBufferToWav = (audioBuffer) => {
  const numOfChannels = audioBuffer.numberOfChannels;
  const sampleRate = audioBuffer.sampleRate;
  const length = audioBuffer.length * numOfChannels * 2 + 44;
  const buffer = new ArrayBuffer(length);
  const view = new DataView(buffer);
  const channels = [];
  let offset = 0;
  let pos = 0;

  // Write WAVE header
  const setUint16 = (data) => {
    view.setUint16(pos, data, true);
    pos += 2;
  };
  
  const setUint32 = (data) => {
    view.setUint32(pos, data, true);
    pos += 4;
  };

  // "RIFF" chunk descriptor
  setUint32(0x46464952); // "RIFF"
  setUint32(length - 8); // file length - 8
  setUint32(0x45564157); // "WAVE"

  // "fmt " sub-chunk
  setUint32(0x20746d66); // "fmt "
  setUint32(16); // subchunk1size
  setUint16(1); // audio format (1 = PCM)
  setUint16(numOfChannels);
  setUint32(sampleRate);
  setUint32(sampleRate * numOfChannels * 2); // byte rate
  setUint16(numOfChannels * 2); // block align
  setUint16(16); // bits per sample

  // "data" sub-chunk
  setUint32(0x61746164); // "data"
  setUint32(length - pos - 4); // subchunk2size

  // Write interleaved data
  for (let i = 0; i < audioBuffer.numberOfChannels; i++) {
    channels.push(audioBuffer.getChannelData(i));
  }

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

/**
 * Main convolution process
 */
const convolveAudio = async () => {
  if (!canConvolve.value) return;
  
  isProcessing.value = true;
  error.value = '';
  processingStatus.value = 'Initializing...';
  
  try {
    // Create audio context
    audioContext.value = new AudioContext();
    
    // Get sources (file paths or File objects)
    processingStatus.value = 'Preparing audio sources...';
    const drySource = getDryAudioSource();
    const irSourceUrl = getIRSource();
    
    // Load dry audio
    processingStatus.value = 'Loading dry audio...';
    const dryBuffer = await loadAudio(drySource, audioContext.value);
    
    // Load impulse response
    processingStatus.value = 'Loading impulse response...';
    const irBuffer = await loadAudio(irSourceUrl, audioContext.value);
    
    // Create offline context for rendering
    processingStatus.value = 'Convolving audio...';
    const offlineContext = new OfflineAudioContext(
      dryBuffer.numberOfChannels,
      dryBuffer.length,
      dryBuffer.sampleRate
    );
    
    // Create nodes in offline context
    const sourceNode = offlineContext.createBufferSource();
    const convolverNode = offlineContext.createConvolver();
    
    // Set up the audio processing chain
    sourceNode.buffer = dryBuffer;
    convolverNode.buffer = irBuffer;
    
    // Connect: Source -> Convolver -> Destination
    sourceNode.connect(convolverNode);
    convolverNode.connect(offlineContext.destination);
    
    // Start the source
    sourceNode.start(0);
    
    // Render the audio
    processingStatus.value = 'Rendering final audio...';
    const renderedBuffer = await offlineContext.startRendering();
    
    // Convert to WAV
    processingStatus.value = 'Creating download file...';
    const wavBlob = audioBufferToWav(renderedBuffer);
    
    // Create download URL
    if (convolvedAudioUrl.value) {
      URL.revokeObjectURL(convolvedAudioUrl.value);
    }
    convolvedAudioUrl.value = URL.createObjectURL(wavBlob);
    
    processingStatus.value = 'Complete! Your audio is ready.';
    
  } catch (err) {
    console.error('Convolution error:', err);
    error.value = err.message || 'An error occurred during processing. Please try again.';
    processingStatus.value = '';
  } finally {
    isProcessing.value = false;
  }
};

/**
 * Download the convolved audio
 */
const downloadAudio = () => {
  if (!convolvedAudioUrl.value) return;
  
  const link = document.createElement('a');
  link.href = convolvedAudioUrl.value;
  
  // Generate filename based on source
  let filename = 'convolved_audio.wav';
  if (dryAudioSource.value === 'example' && selectedExampleAudio.value) {
    filename = `convolved_${selectedExampleAudio.value}`;
  } else if (uploadedDryAudioFile.value) {
    filename = `convolved_${uploadedDryAudioFile.value.name}`;
  }
  
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};

/**
 * Reset the form
 */
const reset = () => {
  dryAudioSource.value = 'example';
  selectedExampleAudio.value = '';
  uploadedDryAudioFile.value = null;
  clearDryAudioPreview();
  
  irSource.value = 'example';
  selectedExampleIR.value = '';
  uploadedIRFile.value = null;
  clearIRPreview();
  
  if (convolvedAudioUrl.value) {
    URL.revokeObjectURL(convolvedAudioUrl.value);
  }
  convolvedAudioUrl.value = '';
  processingStatus.value = '';
  error.value = '';
  
  // Clear file inputs
  const fileInputs = document.querySelectorAll('input[type="file"]');
  fileInputs.forEach(input => input.value = '');
};
</script>

<template>
  <div class="convolve-view">
    <div class="container">
      <!-- Header -->
      <header class="header">
        <h1>🎚️ Audio Convolution</h1>
        <p class="subtitle">
          Apply impulse responses to your audio files using real-time convolution
        </p>
      </header>

      <!-- Main Content -->
      <div class="content-grid">
        
        <!-- Dry Audio Section -->
        <section class="card input-section">
          <h2 class="section-title">1. Select Dry Audio</h2>
          
          <!-- Source Selection -->
          <div class="source-selector">
            <label class="radio-option">
              <input type="radio" value="example" v-model="dryAudioSource" :disabled="isProcessing" @change="handleDryAudioSourceChange" />
              <span>Use Example Audio</span>
            </label>
            <label class="radio-option">
              <input type="radio" value="upload" v-model="dryAudioSource" :disabled="isProcessing" @change="handleDryAudioSourceChange" />
              <span>Upload My Audio</span>
            </label>
          </div>
          
          <!-- Example Audio Selection -->
          <div v-if="dryAudioSource === 'example'" class="option-content">
            <label for="example-audio" class="input-label">Choose Example</label>
            <select
              id="example-audio"
              v-model="selectedExampleAudio"
              :disabled="isProcessing"
              class="select-input"
              @change="loadDryAudioPreview"
            >
              <option value="" disabled>Select an example...</option>
              <option v-for="audio in exampleAudios" :key="audio.filename" :value="audio.filename">
                {{ audio.name }}
              </option>
            </select>
            
            <!-- Audio Preview -->
            <div v-if="dryAudioPreviewUrl" class="audio-preview">
              <label class="preview-label">🎵 Preview:</label>
              <audio :src="dryAudioPreviewUrl" controls class="preview-audio"></audio>
            </div>
            <div v-else-if="isLoadingDryPreview" class="loading-preview">
              <span class="spinner-small"></span> Loading preview...
            </div>
          </div>
          
          <!-- Upload Audio -->
          <div v-else class="option-content">
            <div class="file-input-wrapper">
              <input
                type="file"
                id="dry-audio-file"
                accept="audio/*"
                @change="handleDryAudioFileSelect"
                :disabled="isProcessing"
              />
              <label for="dry-audio-file" class="file-input-label">
                <span class="file-icon">📁</span>
                <span v-if="!uploadedDryAudioFile">Choose Audio File</span>
                <span v-else class="file-name">{{ uploadedDryAudioFile.name }}</span>
              </label>
            </div>
            <p v-if="uploadedDryAudioFile" class="file-info">
              Size: {{ dryAudioFileSize }} | Max: 50 MB
            </p>
            
            <!-- Audio Preview -->
            <div v-if="dryAudioPreviewUrl" class="audio-preview">
              <label class="preview-label">🎵 Preview:</label>
              <audio :src="dryAudioPreviewUrl" controls class="preview-audio"></audio>
            </div>
          </div>
        </section>

        <!-- Impulse Response Section -->
        <section class="card input-section">
          <h2 class="section-title">2. Select Impulse Response</h2>
          
          <!-- Source Selection -->
          <div class="source-selector">
            <label class="radio-option">
              <input type="radio" value="example" v-model="irSource" :disabled="isProcessing" @change="handleIRSourceChange" />
              <span>Use Example IR</span>
            </label>
            <label class="radio-option">
              <input type="radio" value="upload" v-model="irSource" :disabled="isProcessing" @change="handleIRSourceChange" />
              <span>Upload My IR</span>
            </label>
          </div>
          
          <!-- Example IR Selection -->
          <div v-if="irSource === 'example'" class="option-content">
            <label for="example-ir" class="input-label">Choose Example</label>
            <select
              id="example-ir"
              v-model="selectedExampleIR"
              :disabled="isProcessing"
              class="select-input"
              @change="loadIRPreview"
            >
              <option value="" disabled>Select an example...</option>
              <option v-for="ir in exampleIRs" :key="ir.filename" :value="ir.filename">
                {{ ir.name }}
              </option>
            </select>
            
            <!-- Audio Preview -->
            <div v-if="irPreviewUrl" class="audio-preview">
              <label class="preview-label">🎵 Preview:</label>
              <audio :src="irPreviewUrl" controls class="preview-audio"></audio>
            </div>
            <div v-else-if="isLoadingIRPreview" class="loading-preview">
              <span class="spinner-small"></span> Loading preview...
            </div>
          </div>
          
          <!-- Upload IR -->
          <div v-else class="option-content">
            <div class="file-input-wrapper">
              <input
                type="file"
                id="ir-file"
                accept="audio/*"
                @change="handleIRFileSelect"
                :disabled="isProcessing"
              />
              <label for="ir-file" class="file-input-label">
                <span class="file-icon">📁</span>
                <span v-if="!uploadedIRFile">Choose IR File</span>
                <span v-else class="file-name">{{ uploadedIRFile.name }}</span>
              </label>
            </div>
            <p v-if="uploadedIRFile" class="file-info">
              Size: {{ irFileSize }} | Max: 20 MB
            </p>
            
            <!-- Audio Preview -->
            <div v-if="irPreviewUrl" class="audio-preview">
              <label class="preview-label">🎵 Preview:</label>
              <audio :src="irPreviewUrl" controls class="preview-audio"></audio>
            </div>
          </div>
        </section>

        <!-- Convolve Button -->
        <section class="card">
          <button
            @click="convolveAudio"
            :disabled="!canConvolve"
            class="btn btn-primary btn-large"
          >
            <span class="btn-icon">🎛️</span>
            {{ isProcessing ? 'Processing...' : 'Convolve Audio' }}
          </button>
        </section>

        <!-- Status Section -->
        <section class="card status-section">
          <h2 class="section-title">Status</h2>
          
          <!-- Processing Indicator -->
          <div v-if="isProcessing" class="processing-indicator">
            <div class="spinner"></div>
            <p class="status-text">{{ processingStatus }}</p>
          </div>
          
          <!-- Error Message -->
          <div v-else-if="error" class="error-message">
            <span class="error-icon">⚠️</span>
            <p>{{ error }}</p>
          </div>
          
          <!-- Success Message -->
          <div v-else-if="convolvedAudioUrl" class="success-message">
            <span class="success-icon">✅</span>
            <p>{{ processingStatus }}</p>
          </div>
          
          <!-- Idle State -->
          <div v-else class="idle-state">
            <span class="idle-icon">🎵</span>
            <p>Select an audio file and impulse response to begin</p>
          </div>
        </section>

        <!-- Result Section -->
        <section v-if="convolvedAudioUrl" class="card result-section">
          <h2 class="section-title">Result</h2>
          
          <!-- Audio Player -->
          <div class="audio-player">
            <audio :src="convolvedAudioUrl" controls class="audio-element"></audio>
          </div>
          
          <!-- Download Button -->
          <div class="action-buttons">
            <button @click="downloadAudio" class="btn btn-success">
              <span class="btn-icon">💾</span>
              Download Convolved Audio
            </button>
            <button @click="reset" class="btn btn-secondary">
              <span class="btn-icon">🔄</span>
              Process Another
            </button>
          </div>
        </section>

        <!-- Info Section -->
        <section class="card info-section">
          <h3 class="info-title">ℹ️ How it Works</h3>
          <ul class="info-list">
            <li>Select dry audio (predetermined or upload your own)</li>
            <li>Select impulse response (predetermined or upload your own)</li>
            <li>Click "Convolve" to apply the IR to your audio</li>
            <li>Listen to the result and download the processed file</li>
          </ul>
          
          <div class="tech-note">
            <strong>Technical Note:</strong> All convolution processing happens in your browser using the Web Audio API. Both example and uploaded files are processed entirely in your browser - nothing is sent to the backend.
          </div>
          
          <div class="tech-note" style="margin-top: var(--space-md);">
            <strong>Example Files:</strong> Try the example drums or trumpet with the Clifford Tower or Marble Hall impulse responses to hear the effect!
          </div>
        </section>
      </div>

    </div>
  </div>
</template>

<style scoped>
/* ============================================================================
   LAYOUT
   ============================================================================ */
.convolve-view {
  min-height: calc(100vh - 200px);
  padding: var(--space-xl) 0;
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.05) 0%, rgba(37, 99, 235, 0.02) 100%);
}

.container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 0 var(--space-lg);
}

.content-grid {
  display: grid;
  gap: var(--space-lg);
}

/* ============================================================================
   HEADER
   ============================================================================ */
.header {
  text-align: center;
  margin-bottom: var(--space-2xl);
}

.header h1 {
  font-size: var(--font-size-4xl);
  font-weight: var(--font-weight-bold);
  margin-bottom: var(--space-md);
  background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-light) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.subtitle {
  font-size: var(--font-size-lg);
  color: var(--color-text-secondary);
}

/* ============================================================================
   CARDS
   ============================================================================ */
.card {
  background-color: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  padding: var(--space-xl);
  box-shadow: var(--shadow-md);
}

.section-title {
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-semibold);
  margin-bottom: var(--space-lg);
  color: var(--color-text-primary);
}

/* ============================================================================
   FILE INPUT
   ============================================================================ */
.file-input-wrapper {
  position: relative;
  margin-bottom: var(--space-md);
}

.file-input-wrapper input[type="file"] {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
}

.file-input-label {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-md);
  padding: var(--space-lg);
  background-color: var(--color-surface-elevated);
  border: 2px dashed var(--color-border-light);
  border-radius: var(--radius-lg);
  cursor: pointer;
  transition: all var(--transition-base);
  font-weight: var(--font-weight-medium);
}

.file-input-label:hover {
  border-color: var(--color-primary);
  background-color: rgba(59, 130, 246, 0.05);
}

.file-input-wrapper input:disabled + .file-input-label {
  opacity: 0.5;
  cursor: not-allowed;
}

.file-icon {
  font-size: var(--font-size-2xl);
}

.file-name {
  color: var(--color-primary);
  font-weight: var(--font-weight-semibold);
}

.file-info {
  font-size: var(--font-size-sm);
  color: var(--color-text-tertiary);
  margin-bottom: var(--space-lg);
}

/* ============================================================================
   FORM ELEMENTS
   ============================================================================ */
.ir-selector {
  margin-bottom: var(--space-xl);
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
}

.select-input:hover {
  border-color: var(--color-border-lighter);
}

.select-input:focus {
  outline: none;
  border-color: var(--color-primary);
}

.select-input:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* ============================================================================
   BUTTONS
   ============================================================================ */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-sm);
  padding: var(--space-md) var(--space-xl);
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-semibold);
  border-radius: var(--radius-lg);
  border: none;
  cursor: pointer;
  transition: all var(--transition-base);
  width: 100%;
}

.btn-icon {
  font-size: var(--font-size-lg);
}

.btn-primary {
  background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-hover) 100%);
  color: white;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: var(--shadow-glow);
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}

.btn-success {
  background-color: var(--color-success);
  color: white;
}

.btn-success:hover {
  background-color: var(--color-success-hover);
  transform: translateY(-2px);
}

.btn-secondary {
  background-color: transparent;
  border: 2px solid var(--color-border-light);
  color: var(--color-text-primary);
}

.btn-secondary:hover {
  border-color: var(--color-primary);
  background-color: rgba(59, 130, 246, 0.1);
}

/* ============================================================================
   STATUS INDICATORS
   ============================================================================ */
.processing-indicator,
.error-message,
.success-message,
.idle-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--space-2xl);
  text-align: center;
  min-height: 150px;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 4px solid var(--color-surface-elevated);
  border-top: 4px solid var(--color-primary);
  border-radius: var(--radius-full);
  animation: spin 1s linear infinite;
  margin-bottom: var(--space-md);
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.status-text {
  font-size: var(--font-size-lg);
  color: var(--color-primary);
  font-weight: var(--font-weight-medium);
}

.error-icon,
.success-icon,
.idle-icon {
  font-size: 3rem;
  margin-bottom: var(--space-md);
}

.error-message {
  color: var(--color-error);
}

.success-message {
  color: var(--color-success);
}

.idle-state {
  color: var(--color-text-tertiary);
}

/* ============================================================================
   RESULT SECTION
   ============================================================================ */
.audio-player {
  margin-bottom: var(--space-xl);
  text-align: center;
}

.audio-element {
  width: 100%;
  max-width: 500px;
  border-radius: var(--radius-md);
  background-color: var(--color-surface-elevated);
}

.action-buttons {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-md);
}

/* ============================================================================
   INFO SECTION
   ============================================================================ */
.info-title {
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-semibold);
  margin-bottom: var(--space-md);
}

.info-list {
  list-style: none;
  padding: 0;
  margin: 0 0 var(--space-lg) 0;
}

.info-list li {
  padding: var(--space-sm) 0;
  padding-left: var(--space-lg);
  position: relative;
  line-height: var(--line-height-relaxed);
  color: var(--color-text-secondary);
}

.info-list li::before {
  content: '▸';
  position: absolute;
  left: 0;
  color: var(--color-primary);
  font-weight: var(--font-weight-bold);
}

.tech-note {
  padding: var(--space-md);
  background-color: rgba(59, 130, 246, 0.1);
  border-left: 4px solid var(--color-primary);
  border-radius: var(--radius-md);
  font-size: var(--font-size-sm);
  line-height: var(--line-height-relaxed);
  color: var(--color-text-secondary);
}

.tech-note strong {
  color: var(--color-primary);
}

/* ============================================================================
   SOURCE SELECTOR (RADIO BUTTONS)
   ============================================================================ */
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

.radio-option input:disabled {
  cursor: not-allowed;
  opacity: 0.5;
}

.radio-option:has(input:disabled) {
  cursor: not-allowed;
  opacity: 0.5;
}

/* ============================================================================
   OPTION CONTENT
   ============================================================================ */
.option-content {
  animation: fadeIn var(--transition-base);
}

.success-text {
  margin-top: var(--space-sm);
  padding: var(--space-sm);
  color: var(--color-success);
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  background-color: rgba(16, 185, 129, 0.1);
  border-radius: var(--radius-md);
  text-align: center;
}

/* ============================================================================
   BUTTON VARIANTS
   ============================================================================ */
.btn-large {
  font-size: var(--font-size-lg);
  padding: var(--space-lg) var(--space-2xl);
}

.spinner-small {
  display: inline-block;
  width: 14px;
  height: 14px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top: 2px solid white;
  border-radius: var(--radius-full);
  animation: spin 0.8s linear infinite;
  margin-right: var(--space-xs);
}

/* ============================================================================
   AUDIO PREVIEW
   ============================================================================ */
.audio-preview {
  margin-top: var(--space-lg);
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

.loading-preview {
  margin-top: var(--space-lg);
  padding: var(--space-md);
  text-align: center;
  color: var(--color-text-tertiary);
  font-size: var(--font-size-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-sm);
}

.loading-preview .spinner-small {
  border: 2px solid var(--color-border-light);
  border-top: 2px solid var(--color-primary);
}

/* ============================================================================
   RESPONSIVE DESIGN
   ============================================================================ */
@media (max-width: 768px) {
  .convolve-view {
    padding: var(--space-lg) 0;
  }

  .header h1 {
    font-size: var(--font-size-3xl);
  }

  .subtitle {
    font-size: var(--font-size-base);
  }

  .card {
    padding: var(--space-lg);
  }

  .action-buttons {
    grid-template-columns: 1fr;
  }

  .source-selector {
    flex-direction: column;
    gap: var(--space-md);
  }
}
</style>
