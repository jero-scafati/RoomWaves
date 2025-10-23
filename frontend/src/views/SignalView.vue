<script setup>
import { ref, onMounted, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import ApiService from '@/services/ApiService.js';

// ============================================================================
// STATE
// ============================================================================
const route = useRoute();
const router = useRouter();

const isLoading = ref(false);
const error = ref(null);
const signalData = ref(null);

// Preset configurations
const presets = [
  { name: 'Standard Quality (44.1kHz)', duration: 10, f_inf: 20, f_sup: 20000, fs: 44100 },
  { name: 'High Quality (48kHz)', duration: 10, f_inf: 20, f_sup: 24000, fs: 48000 },
  { name: 'Quick Test (5s)', duration: 5, f_inf: 20, f_sup: 20000, fs: 44100 },
  { name: 'Ultra High Quality (96kHz)', duration: 10, f_inf: 20, f_sup: 40000, fs: 96000 },
  { name: 'Custom', duration: 10, f_inf: 20, f_sup: 20000, fs: 44100 }
];

const selectedPreset = ref(0);
const showAdvancedSettings = ref(false);

// Parameters from query string with defaults
const duration = ref(parseFloat(route.query.duration) || 10);
const f_inf = ref(parseInt(route.query.f_inf) || 20);
const f_sup = ref(parseInt(route.query.f_sup) || 20000);
const fs = ref(parseInt(route.query.fs) || 44100);

const applyPreset = () => {
  if (selectedPreset.value === presets.length - 1) {
    // Custom option selected - show advanced settings
    showAdvancedSettings.value = true;
    return;
  }
  
  const preset = presets[selectedPreset.value];
  duration.value = preset.duration;
  f_inf.value = preset.f_inf;
  f_sup.value = preset.f_sup;
  fs.value = preset.fs;
  showAdvancedSettings.value = false;
  generateNewSignals();
};

// ============================================================================
// METHODS
// ============================================================================
const fetchSignalData = async () => {
  isLoading.value = true;
  error.value = null;

  try {
    const response = await ApiService.getSignalData({
      duration: duration.value,
      f_inf: f_inf.value,
      f_sup: f_sup.value,
      fs: fs.value
    });

    signalData.value = response.data;
  } catch (err) {
    error.value = err.message || 'Failed to generate signals';
    console.error('Error fetching signal data:', err);
  } finally {
    isLoading.value = false;
  }
};

const generateNewSignals = () => {
  // Update query parameters and fetch new data
  router.push({
    path: '/signal',
    query: {
      duration: duration.value,
      f_inf: f_inf.value,
      f_sup: f_sup.value,
      fs: fs.value
    }
  });
  fetchSignalData();
};

// ============================================================================
// LIFECYCLE
// ============================================================================
onMounted(() => {
  fetchSignalData();
});

// Watch for route query changes (e.g., browser back/forward)
watch(
  () => route.query,
  (newQuery) => {
    duration.value = parseFloat(newQuery.duration) || 10;
    f_inf.value = parseInt(newQuery.f_inf) || 20;
    f_sup.value = parseInt(newQuery.f_sup) || 20000;
    fs.value = parseInt(newQuery.fs) || 44100;
    fetchSignalData();
  }
);
</script>

<template>
  <div class="signal-view">
    <div class="background-pattern"></div>
    <header class="signal-header">
      <h1 class="title">Signal Generator</h1>
      <p class="subtitle">Generate sweep and inverse sweep signals for room acoustics measurement</p>
    </header>

    <section class="config-section">
      <div class="glass-card">
        <div class="card-header">
          <h2>Configuration</h2>
        </div>
        <div class="card-content">
          <div class="preset-group">
            <label for="preset-select" class="input-label">Preset</label>
            <select 
              id="preset-select"
              v-model="selectedPreset" 
              @change="applyPreset"
              class="select-input"
              :disabled="isLoading"
            >
              <option v-for="(preset, index) in presets" :key="index" :value="index">
                {{ preset.name }}
              </option>
            </select>
          </div>

          <div v-if="showAdvancedSettings" class="advanced-settings">
            <div class="params-grid">
              <div class="input-group">
                <label for="duration">Duration (s)</label>
                <input
                  id="duration"
                  v-model.number="duration"
                  type="number"
                  step="0.1"
                  min="0.1"
                  max="60"
                  class="text-input"
                />
              </div>
              <div class="input-group">
                <label for="f_inf">Lower Frequency (Hz)</label>
                <input
                  id="f_inf"
                  v-model.number="f_inf"
                  type="number"
                  step="1"
                  min="1"
                  max="24000"
                  class="text-input"
                />
              </div>
              <div class="input-group">
                <label for="f_sup">Upper Frequency (Hz)</label>
                <input
                  id="f_sup"
                  v-model.number="f_sup"
                  type="number"
                  step="1"
                  min="1"
                  max="48000"
                  class="text-input"
                />
              </div>
              <div class="input-group">
                <label for="fs">Sample Rate (Hz)</label>
                <input
                  id="fs"
                  v-model.number="fs"
                  type="number"
                  step="1"
                  min="8000"
                  max="96000"
                  class="text-input"
                />
              </div>
            </div>
            <button
              @click="generateNewSignals"
              :disabled="isLoading"
              class="generate-btn"
            >
              <span v-if="isLoading">Generating...</span>
              <span v-else>Generate Signals</span>
            </button>
          </div>
        </div>
      </div>
    </section>

    <div v-if="error" class="error-message">
      {{ error }}
    </div>

    <div v-if="isLoading && !signalData" class="loading-state">
      <div class="spinner"></div>
      <p>Generating signals...</p>
    </div>

    <section v-if="signalData && !isLoading" class="results-section">
      <div class="signals-grid">
        <div class="signal-card glass-card">
          <div class="signal-header">
            <h3>Direct Sweep</h3>
            <span class="signal-badge">Sweep</span>
          </div>
          <div class="signal-content">
            <div class="audio-wrapper">
              <audio controls class="audio-player">
                <source
                  :src="`data:audio/wav;base64,${signalData.audio_sweep_b64}`"
                  type="audio/wav"
                />
              </audio>
            </div>
            <a
              :href="`data:audio/wav;base64,${signalData.audio_sweep_b64}`"
              :download="signalData.filename_sweep"
              class="download-btn"
            >
              Download Sweep
            </a>
          </div>
        </div>

        <div class="signal-card glass-card">
          <div class="signal-header">
            <h3>Inverse Sweep</h3>
            <span class="signal-badge inverse">Inverse</span>
          </div>
          <div class="signal-content">
            <div class="audio-wrapper">
              <audio controls class="audio-player">
                <source
                  :src="`data:audio/wav;base64,${signalData.audio_inverse_b64}`"
                  type="audio/wav"
                />
              </audio>
            </div>
            <a
              :href="`data:audio/wav;base64,${signalData.audio_inverse_b64}`"
              :download="signalData.filename_inverse"
              class="download-btn"
            >
              Download Inverse
            </a>
          </div>
        </div>
      </div>

      <div class="info-card glass-card">
        <h4>How to use</h4>
        <p>
          The direct sweep measures the impulse response of a room.
          The inverse sweep processes the recording to obtain the impulse response.
        </p>
      </div>
    </section>
  </div>
</template>

<style scoped>
.signal-view {
  position: relative;
  max-width: 1400px;
  margin: 0 auto;
  padding: var(--space-xl);
  overflow: hidden;
  animation: fadeIn 0.4s ease;
}

.background-pattern {
  position: absolute;
  inset: 0;
  background:
    radial-gradient(circle at 20% 30%, rgba(41, 79, 82, 0.28) 0%, transparent 50%),
    radial-gradient(circle at 80% 70%, rgba(27, 38, 85, 0.466) 0%, transparent 50%),
    radial-gradient(circle at 50% 50%, rgba(29, 130, 155, 0.068) 0%, transparent 70%);
  z-index: 0;
}

.signal-header {
  position: relative;
  z-index: 1;
  text-align: center;
  margin-bottom: var(--space-2xl);
}

.title {
  font-size: var(--font-size-3xl);
  font-weight: var(--font-weight-bold);
  color: var(--color-text-primary);
  margin-bottom: var(--space-sm);
}

.subtitle {
  color: var(--color-text-secondary);
  font-size: var(--font-size-base);
}

.config-section {
  position: relative;
  z-index: 1;
  margin-bottom: var(--space-xl);
}

.glass-card {
  background: var(--glass-background);
  backdrop-filter: blur(var(--glass-blur));
  -webkit-backdrop-filter: blur(var(--glass-blur));
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-xl);
  box-shadow: var(--glass-shadow);
  transition: all var(--transition-base);
  overflow: hidden;
}

.glass-card:hover {
  border-color: rgba(255, 255, 255, 0.15);
  box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.45);
}

.card-header {
  padding: var(--space-lg);
  border-bottom: 1px solid var(--glass-border);
}

.card-header h2 {
  margin: 0;
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-primary);
}

.card-content {
  padding: var(--space-lg);
}

.preset-group {
  margin-bottom: var(--space-md);
}

.input-label {
  display: block;
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-primary);
  margin-bottom: var(--space-sm);
}

.select-input {
  width: 100%;
  padding: var(--space-sm) var(--space-md);
  background: var(--color-surface-elevated);
  color: var(--color-text-primary);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-md);
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  cursor: pointer;
  transition: all var(--transition-base);
}

.select-input:hover:not(:disabled) {
  border-color: var(--color-border-lighter);
  background: var(--color-surface-hover);
}

.select-input:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(47, 9, 136, 0.15);
}

.select-input:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.advanced-settings {
  margin-top: var(--space-lg);
  padding-top: var(--space-lg);
  border-top: 1px solid var(--glass-border);
  animation: slideDown 0.3s ease;
}

.params-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--space-md);
  margin-bottom: var(--space-lg);
}

.input-group label {
  display: block;
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  color: var(--color-text-secondary);
  margin-bottom: var(--space-xs);
}

.text-input {
  width: 100%;
  padding: var(--space-sm);
  background: var(--color-surface-elevated);
  color: var(--color-text-primary);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-md);
  font-size: var(--font-size-sm);
  transition: all var(--transition-base);
}

.text-input:hover {
  border-color: var(--color-border-lighter);
}

.text-input:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(47, 9, 136, 0.15);
}

.generate-btn {
  width: 100%;
  padding: var(--space-md);
  background: linear-gradient(135deg, var(--color-primary), var(--color-primary-hover));
  color: white;
  border: none;
  border-radius: var(--radius-md);
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-semibold);
  cursor: pointer;
  transition: all var(--transition-base);
  box-shadow: 0 2px 8px rgba(47, 9, 136, 0.3);
}

.generate-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(47, 9, 136, 0.4);
}

.generate-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}

.error-message {
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid var(--color-error);
  border-radius: var(--radius-lg);
  padding: var(--space-md);
  color: var(--color-error);
  margin-bottom: var(--space-lg);
  animation: fadeIn 0.3s ease;
}

.loading-state {
  text-align: center;
  padding: var(--space-3xl);
  color: var(--color-text-secondary);
}

.spinner {
  border: 4px solid var(--color-border);
  border-top: 4px solid var(--color-primary);
  border-radius: 50%;
  width: 50px;
  height: 50px;
  animation: spin 1s linear infinite;
  margin: 0 auto var(--space-md);
}

.results-section {
  position: relative;
  z-index: 1;
  animation: fadeIn 0.4s ease;
}

.signals-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: var(--space-xl);
  margin-bottom: var(--space-xl);
}

.signal-card {
  transition: all var(--transition-base);
}

.signal-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 16px 48px 0 rgba(0, 0, 0, 0.5);
}

.signal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--space-lg);
  border-bottom: 1px solid var(--glass-border);
}

.signal-header h3 {
  margin: 0;
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-primary);
}

.signal-badge {
  padding: var(--space-xs) var(--space-md);
  background: linear-gradient(135deg, var(--color-primary), var(--color-primary-hover));
  color: white;
  border-radius: var(--radius-full);
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.signal-badge.inverse {
  background: linear-gradient(135deg, #8b5cf6, #7c3aed);
}

.signal-content {
  padding: var(--space-lg);
  display: flex;
  flex-direction: column;
  gap: var(--space-md);
}

.audio-wrapper {
  background: var(--color-surface-elevated);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-lg);
  padding: var(--space-md);
}

.audio-player {
  width: 100%;
  height: 40px;
}

.download-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--space-sm) var(--space-lg);
  background: transparent;
  border: 2px solid var(--color-primary);
  color: var(--color-primary-light);
  text-decoration: none;
  border-radius: var(--radius-md);
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-semibold);
  transition: all var(--transition-base);
}

.download-btn:hover {
  background: var(--color-primary);
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(47, 9, 136, 0.3);
}

.info-card {
  padding: var(--space-lg);
}

.info-card h4 {
  margin: 0 0 var(--space-sm) 0;
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-primary);
}

.info-card p {
  margin: 0;
  color: var(--color-text-secondary);
  line-height: 1.6;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@media (max-width: 768px) {
  .signal-view {
    padding: var(--space-md);
  }

  .signals-grid {
    grid-template-columns: 1fr;
  }

  .params-grid {
    grid-template-columns: 1fr;
  }
}
</style>
