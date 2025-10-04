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

// Parameters from query string with defaults
const duration = ref(parseFloat(route.query.duration) || 10);
const f_inf = ref(parseInt(route.query.f_inf) || 20);
const f_sup = ref(parseInt(route.query.f_sup) || 20000);
const fs = ref(parseInt(route.query.fs) || 44100);

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
    <!-- Header -->
    <header class="text-center mb-4">
      <h1 class="title">Signal Generator</h1>
      <p class="subtitle">Generate and download sweep and inverse sweep signals</p>
    </header>

    <hr class="separator" />

    <!-- Parameters Form -->
    <section class="parameters-section">
      <div class="card">
        <div class="card-header">
          <h5 class="mb-0">
            <i class="icon">⚙️</i> Signal Parameters
          </h5>
        </div>
        <div class="card-body">
          <div class="parameters-grid">
            <div class="param-field">
              <label for="duration">Duration (s)</label>
              <input
                id="duration"
                v-model.number="duration"
                type="number"
                step="0.1"
                min="0.1"
                max="60"
                class="form-control"
              />
            </div>
            <div class="param-field">
              <label for="f_inf">Lower Frequency (Hz)</label>
              <input
                id="f_inf"
                v-model.number="f_inf"
                type="number"
                step="1"
                min="1"
                max="24000"
                class="form-control"
              />
            </div>
            <div class="param-field">
              <label for="f_sup">Upper Frequency (Hz)</label>
              <input
                id="f_sup"
                v-model.number="f_sup"
                type="number"
                step="1"
                min="1"
                max="48000"
                class="form-control"
              />
            </div>
            <div class="param-field">
              <label for="fs">Sample Rate (Hz)</label>
              <input
                id="fs"
                v-model.number="fs"
                type="number"
                step="1"
                min="8000"
                max="96000"
                class="form-control"
              />
            </div>
          </div>
          <div class="button-container">
            <button
              @click="generateNewSignals"
              :disabled="isLoading"
              class="btn btn-primary"
            >
              <span v-if="isLoading">⏳ Generating...</span>
              <span v-else>🔄 Generate Signals</span>
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- Error Display -->
    <div v-if="error" class="alert alert-error">
      <strong>Error:</strong> {{ error }}
    </div>

    <!-- Loading Indicator -->
    <div v-if="isLoading && !signalData" class="loading-container">
      <div class="spinner"></div>
      <p>Generating signals...</p>
    </div>

    <!-- Signal Results -->
    <section v-if="signalData && !isLoading" class="results-section">
      <div class="signals-grid">
        <!-- Sweep Card -->
        <div class="signal-card">
          <div class="card-header-signal">
            <div class="header-content">
              <h5 class="mb-0">
                <i class="icon">📈</i> Direct Sweep
              </h5>
              <span class="badge">Sweep</span>
            </div>
          </div>
          <div class="card-body-signal">
            <div class="audio-player">
              <audio controls class="audio-control">
                <source
                  :src="`data:audio/wav;base64,${signalData.audio_sweep_b64}`"
                  type="audio/wav"
                />
                Your browser does not support the audio element.
              </audio>
            </div>
            <a
              :href="`data:audio/wav;base64,${signalData.audio_sweep_b64}`"
              :download="signalData.filename_sweep"
              class="btn btn-download"
            >
              <i class="icon">⬇️</i> Download Sweep
            </a>
          </div>
        </div>

        <!-- Inverse Sweep Card -->
        <div class="signal-card">
          <div class="card-header-signal">
            <div class="header-content">
              <h5 class="mb-0">
                <i class="icon">📉</i> Inverse Sweep
              </h5>
              <span class="badge">Inverse</span>
            </div>
          </div>
          <div class="card-body-signal">
            <div class="audio-player">
              <audio controls class="audio-control">
                <source
                  :src="`data:audio/wav;base64,${signalData.audio_inverse_b64}`"
                  type="audio/wav"
                />
                Your browser does not support the audio element.
              </audio>
            </div>
            <a
              :href="`data:audio/wav;base64,${signalData.audio_inverse_b64}`"
              :download="signalData.filename_inverse"
              class="btn btn-download"
            >
              <i class="icon">⬇️</i> Download Inverse
            </a>
          </div>
        </div>
      </div>

      <!-- Info Card -->
      <div class="info-card">
        <div class="info-content">
          <div class="info-icon">ℹ️</div>
          <div class="info-text">
            <strong>How to use these signals?</strong>
            <p class="mb-0">
              The direct sweep measures the impulse response of a room.
              The inverse sweep processes the recording to obtain the impulse response.
            </p>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.signal-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.title {
  font-size: 2.5rem;
  font-weight: bold;
  color: #e0e0e0;
  margin-bottom: 0.5rem;
}

.subtitle {
  color: #a0a0a0;
  font-size: 1.1rem;
}

.separator {
  border: none;
  border-top: 1px solid #3a3a3a;
  margin: 2rem 0;
}

/* Parameters Section */
.parameters-section {
  margin-bottom: 2rem;
}

.card {
  background-color: #1a1a1a;
  border-radius: 12px;
  border: 1px solid #3a3a3a;
  overflow: hidden;
}

.card-header {
  background-color: #252525;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #3a3a3a;
}

.card-header h5 {
  color: #e0e0e0;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.card-body {
  padding: 1.5rem;
}

.parameters-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.param-field label {
  display: block;
  color: #b0b0b0;
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.form-control {
  width: 100%;
  padding: 0.75rem;
  background-color: #2a2a2a;
  border: 1px solid #3a3a3a;
  border-radius: 6px;
  color: #e0e0e0;
  font-size: 1rem;
  transition: border-color 0.3s ease;
}

.form-control:focus {
  outline: none;
  border-color: #3b82f6;
}

.button-container {
  display: flex;
  justify-content: center;
}

.btn {
  padding: 0.75rem 2rem;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
  font-size: 1rem;
}

.btn-primary {
  background-color: #3b82f6;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background-color: #2563eb;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Alert */
.alert {
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 1.5rem;
}

.alert-error {
  background-color: rgba(239, 68, 68, 0.1);
  border: 1px solid #ef4444;
  color: #fca5a5;
}

/* Loading */
.loading-container {
  text-align: center;
  padding: 3rem;
}

.spinner {
  border: 4px solid #3a3a3a;
  border-top: 4px solid #3b82f6;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Results Section */
.results-section {
  margin-top: 2rem;
}

.signals-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(450px, 1fr));
  gap: 2rem;
  margin-bottom: 2rem;
}

.signal-card {
  background-color: #1a1a1a;
  border-radius: 12px;
  border: 1px solid #3a3a3a;
  overflow: hidden;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.signal-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
}

.card-header-signal {
  background-color: #252525;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #3a3a3a;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-content h5 {
  color: #e0e0e0;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.badge {
  background-color: #3b82f6;
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.85rem;
  font-weight: 600;
}

.card-body-signal {
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.audio-player {
  background-color: #252525;
  border-radius: 8px;
  padding: 1rem;
  border: 1px solid #3a3a3a;
}

.audio-control {
  width: 100%;
  height: 40px;
}

.btn-download {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background-color: transparent;
  border: 2px solid #3b82f6;
  color: #3b82f6;
  text-decoration: none;
  border-radius: 8px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-download:hover {
  background-color: #3b82f6;
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

/* Info Card */
.info-card {
  background-color: #1a1a1a;
  border: 1px solid #3a3a3a;
  border-radius: 8px;
  padding: 1rem;
}

.info-content {
  display: flex;
  gap: 1rem;
  align-items: flex-start;
}

.info-icon {
  font-size: 1.5rem;
  flex-shrink: 0;
}

.info-text {
  color: #b0b0b0;
  font-size: 0.95rem;
}

.info-text strong {
  color: #e0e0e0;
  display: block;
  margin-bottom: 0.5rem;
}

.info-text p {
  margin: 0;
  line-height: 1.5;
}

.icon {
  font-style: normal;
}

.mb-0 {
  margin-bottom: 0;
}

.mb-4 {
  margin-bottom: 1.5rem;
}

/* Responsive Design */
@media (max-width: 768px) {
  .signals-grid {
    grid-template-columns: 1fr;
  }

  .parameters-grid {
    grid-template-columns: 1fr;
  }
}
</style>
