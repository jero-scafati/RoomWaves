<script setup>
// ============================================================================
// IMPORTS
// ============================================================================
import { ref, watch, onMounted } from 'vue';
import ApiService from '@/services/ApiService.js';
import AudioUploader from '@/components/AudioUploader.vue';
import SNRCard from '@/components/SNRCard.vue';
import WaveformTab from '@/components/tabs/WaveformTab.vue';
import FrequencyTab from '@/components/tabs/FrequencyTab.vue';
import SpectrogramTab from '@/components/tabs/SpectrogramTab.vue';
import Surface3DTab from '@/components/tabs/Surface3DTab.vue';
import ParametersTab from '@/components/tabs/ParametersTab.vue';
import ConvolutionTab from '@/components/tabs/ConvolutionTab.vue';

// Composables
import { useWaveform } from '@/composables/useWaveform.js';
import { useFrequencyResponse } from '@/composables/useFrequencyResponse.js';
import { useSpectrogram } from '@/composables/useSpectrogram.js';
import { useSurface3D } from '@/composables/useSurface3D.js';
import { useParameters } from '@/composables/useParameters.js';
import { useSNR } from '@/composables/useSNR.js';

// ============================================================================
// STATE
// ============================================================================
const filePath = ref('');
const activeTab = ref('waveform');

// Initialize composables
const waveform = useWaveform();
const frequency = useFrequencyResponse();
const spectrogram = useSpectrogram();
const surface3d = useSurface3D();
const parameters = useParameters();
const snr = useSNR();

onMounted(() => {
  handleExampleSelected('clifford_tower_ir.wav');
});

// ============================================================================
// EVENT HANDLERS
// ============================================================================
const handleUploadSuccess = (path) => {
  filePath.value = path;
  // Clear all plots
  waveform.clear();
  frequency.clear();
  spectrogram.clear();
  surface3d.clear();
  parameters.clear();
  snr.clear();
  // Fetch SNR immediately
  snr.fetchSNR(path);
  // Automatically fetch data for the current active tab
  fetchDataForActiveTab();
};

const handleExampleSelected = (filename) => {
  // For examples, construct the full path directly
  filePath.value = `examples/${filename}`;
  
  // Clear all plots
  waveform.clear();
  frequency.clear();
  spectrogram.clear();
  surface3d.clear();
  parameters.clear();
  snr.clear();
  
  // Fetch SNR immediately
  snr.fetchSNR(filePath.value);
  
  // Automatically fetch data for the current active tab
  fetchDataForActiveTab();
};

// ============================================================================
// WATCHERS
// ============================================================================
// Watch for tab changes and automatically fetch data
watch(activeTab, (newTab, oldTab) => {
  if (!filePath.value) return;
  
  // Clear the previous tab's data
  clearTabData(oldTab);
  
  // Fetch data for the new tab
  fetchDataForActiveTab();
});

// Watch for frequency response bands changes
watch(() => frequency.selectedBands.value, () => {
  if (filePath.value && activeTab.value === 'frequency' && frequency.isVisible.value) {
    frequency.fetchData(filePath.value);
  }
});

// Watch for surface3d bands changes
watch(() => surface3d.bands.value, () => {
  if (filePath.value && activeTab.value === 'surface' && surface3d.isVisible.value) {
    surface3d.fetchData(filePath.value);
  }
});

// Watch for parameters bands changes
watch(() => parameters.selectedBands.value, () => {
  if (filePath.value && activeTab.value === 'parameters' && parameters.isVisible.value) {
    parameters.fetchData(filePath.value);
  }
});

// ============================================================================
// HELPER METHODS
// ============================================================================
const fetchDataForActiveTab = () => {
  if (!filePath.value) return;
  
  switch (activeTab.value) {
    case 'waveform':
      waveform.fetchData(filePath.value);
      break;
    case 'frequency':
      frequency.fetchData(filePath.value);
      break;
    case 'spectrogram':
      spectrogram.fetchData(filePath.value);
      break;
    case 'surface':
      surface3d.fetchData(filePath.value);
      break;
    case 'parameters':
      parameters.fetchData(filePath.value);
      break;
  }
};

const clearTabData = (tab) => {
  switch (tab) {
    case 'waveform':
      waveform.clear();
      break;
    case 'frequency':
      frequency.clear();
      break;
    case 'spectrogram':
      spectrogram.clear();
      break;
    case 'surface':
      surface3d.clear();
      break;
    case 'parameters':
      parameters.clear();
      break;
  }
};
</script>

<template>
  <div class="analysis-view">
    <div class="analysis-header">
      <div class="header-compact">
        <AudioUploader 
          @upload-success="handleUploadSuccess"
          @example-selected="handleExampleSelected"
        />

        <SNRCard 
          :snr="snr.snr.value"
          :quality="snr.quality.value"
          :description="snr.description.value"
          :isLoading="snr.isLoading.value"
          :error="snr.error.value"
        />
      </div>
    </div>

    <div v-if="filePath" class="analysis-workspace">
      <aside class="sidebar-nav">
        <div class="sidebar-header">
          <h3>Analysis</h3>
        </div>
        <nav class="nav-menu">
          <button 
            class="nav-item tooltip-container" 
            :class="{ active: activeTab === 'waveform' }"
            @click="activeTab = 'waveform'"
          >
            <span class="nav-label">Waveform</span>
            <span class="tooltip-icon">?</span>
            <div class="tooltip-text">
              View the time-domain representation of the impulse response signal.
            </div>
          </button>
          <button 
            class="nav-item tooltip-container" 
            :class="{ active: activeTab === 'frequency' }"
            @click="activeTab = 'frequency'"
          >
            <span class="nav-label">Frequency</span>
            <span class="tooltip-icon">?</span>
            <div class="tooltip-text">
              Analyze the frequency response across different octave bands.
            </div>
          </button>
          <button 
            class="nav-item tooltip-container" 
            :class="{ active: activeTab === 'spectrogram' }"
            @click="activeTab = 'spectrogram'"
          >
            <span class="nav-label">Spectrogram</span>
            <span class="tooltip-icon">?</span>
            <div class="tooltip-text">
              View the time-frequency representation showing how energy distributes over time and frequency.
            </div>
          </button>
          <button 
            class="nav-item tooltip-container" 
            :class="{ active: activeTab === 'surface' }"
            @click="activeTab = 'surface'"
          >
            <span class="nav-label">3D Surface</span>
            <span class="tooltip-icon">?</span>
            <div class="tooltip-text">
              Interactive 3D visualization of the spectral decay over time.
            </div>
          </button>
          <button 
            class="nav-item tooltip-container" 
            :class="{ active: activeTab === 'parameters' }"
            @click="activeTab = 'parameters'"
          >
            <span class="nav-label">Parameters</span>
            <span class="tooltip-icon">?</span>
            <div class="tooltip-text">
              View acoustic parameters like RT60, EDT, C50, and D50 according to ISO 3382.
            </div>
          </button>
          <button 
            class="nav-item tooltip-container" 
            :class="{ active: activeTab === 'convolution' }"
            @click="activeTab = 'convolution'"
          >
            <span class="nav-label">Convolution</span>
            <span class="tooltip-icon">?</span>
            <div class="tooltip-text">
              Convolve this IR with your own audio to simulate how it would sound in this space.
            </div>
          </button>
        </nav>
      </aside>

      <main class="content-area">
        <WaveformTab
          v-show="activeTab === 'waveform'"
          :chartData="waveform.chartData.value"
          :isLoading="waveform.isLoading.value"
          :error="waveform.error.value"
          :isVisible="waveform.isVisible.value"
          :filePath="filePath"
        />

        <FrequencyTab
          v-show="activeTab === 'frequency'"
          :chartData="frequency.chartData.value"
          :isLoading="frequency.isLoading.value"
          :error="frequency.error.value"
          :isVisible="frequency.isVisible.value"
          :selectedBands="frequency.selectedBands.value"
          :bandsOptions="frequency.bandsOptions"
          @update:selectedBands="(val) => frequency.selectedBands.value = val"
        />

        <SpectrogramTab
          v-show="activeTab === 'spectrogram'"
          :data="spectrogram.data.value"
          :isLoading="spectrogram.isLoading.value"
          :error="spectrogram.error.value"
          :isVisible="spectrogram.isVisible.value"
        />

        <Surface3DTab
          v-show="activeTab === 'surface'"
          :data="surface3d.data.value"
          :isLoading="surface3d.isLoading.value"
          :error="surface3d.error.value"
          :isVisible="surface3d.isVisible.value"
          :dataReduction="surface3d.dataReduction.value"
          :bands="surface3d.bands.value"
          :bandsOptions="surface3d.bandsOptions"
          @update:dataReduction="(val) => surface3d.dataReduction.value = val"
          @update:bands="(val) => surface3d.bands.value = val"
        />

        <ParametersTab
          v-show="activeTab === 'parameters'"
          :data="parameters.data.value"
          :isLoading="parameters.isLoading.value"
          :error="parameters.error.value"
          :isVisible="parameters.isVisible.value"
          :selectedBands="parameters.selectedBands.value"
          :bandsOptions="parameters.bandsOptions"
          @update:selectedBands="(val) => parameters.selectedBands.value = val"
        />

        <ConvolutionTab
          v-show="activeTab === 'convolution'"
          :currentIRPath="filePath"
        />
      </main>
    </div>
  </div>
</template>

<style scoped>
.analysis-view {
  max-width: 1400px;
  margin: 0 auto;
  padding: var(--space-xl);
  animation: fadeIn 0.4s ease;
}

.analysis-header {
  margin-bottom: var(--space-lg);
}

.header-compact {
  display: grid;
  grid-template-columns: 1fr 320px;
  gap: var(--space-md);
  align-items: start;
}

.analysis-workspace {
  display: grid;
  grid-template-columns: 240px 1fr;
  gap: var(--space-xl);
  animation: slideIn 0.4s ease;
}

.sidebar-nav {
  background: var(--glass-background);
  backdrop-filter: blur(var(--glass-blur));
  -webkit-backdrop-filter: blur(var(--glass-blur));
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-xl);
  padding: var(--space-lg);
  height: fit-content;
  position: sticky;
  top: var(--space-xl);
  box-shadow: var(--glass-shadow);
  transition: all var(--transition-base);
  overflow: visible;
  z-index: var(--z-sticky);
}

.sidebar-nav:hover {
  border-color: rgba(255, 255, 255, 0.15);
  box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.45);
}

.sidebar-header {
  margin-bottom: var(--space-lg);
  padding-bottom: var(--space-md);
  border-bottom: 1px solid var(--glass-border);
}

.sidebar-header h3 {
  margin: 0;
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-bold);
  background: linear-gradient(135deg, var(--color-primary-light), var(--color-primary));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.nav-menu {
  display: flex;
  flex-direction: column;
  gap: var(--space-sm);
  overflow: visible;
  position: relative;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: var(--space-md);
  padding: var(--space-md) var(--space-lg);
  background: transparent;
  border: 1px solid transparent;
  border-radius: var(--radius-lg);
  color: var(--color-text-secondary);
  cursor: pointer;
  transition: all var(--transition-base);
  font-weight: var(--font-weight-medium);
  font-size: var(--font-size-base);
  text-align: left;
  position: relative;
  overflow: visible;
}

.nav-item::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 3px;
  height: 100%;
  background: var(--color-primary);
  transform: scaleY(0);
  transition: transform var(--transition-base);
  border-radius: var(--radius-lg) 0 0 var(--radius-lg);
}

.nav-item:hover {
  background: var(--color-surface-hover);
  border-color: var(--glass-border);
  color: var(--color-text-primary);
  transform: translateX(4px);
}

.nav-item:hover::before {
  transform: scaleY(1);
}

.nav-item.active {
  background: linear-gradient(135deg, rgba(47, 9, 136, 0.2), rgba(69, 16, 184, 0.15));
  border-color: var(--color-primary);
  color: var(--color-primary-light);
  box-shadow: 0 0 20px rgba(47, 9, 136, 0.2);
}

.nav-item.active::before {
  transform: scaleY(1);
}


.nav-label {
  flex: 1;
}

.tooltip-container {
  position: relative;
  z-index: 9999;
}

.tooltip-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 14px;
  height: 14px;
  background: var(--color-primary);
  color: white;
  border-radius: 50%;
  font-size: 10px;
  font-weight: var(--font-weight-bold);
  cursor: help;
  flex-shrink: 0;
  opacity: 0.7;
  transition: opacity var(--transition-base);
}

.tooltip-container:hover .tooltip-icon {
  opacity: 1;
}

.tooltip-text {
  position: absolute;
  left: 100%;
  top: 50%;
  transform: translateY(-50%) translateX(12px);
  background: var(--color-surface-elevated);
  color: var(--color-text-primary);
  padding: var(--space-sm) var(--space-md);
  border-radius: var(--radius-md);
  font-size: var(--font-size-sm);
  white-space: normal;
  width: 220px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
  border: 1px solid var(--glass-border);
  opacity: 0;
  visibility: hidden;
  transition: all var(--transition-base);
  z-index: 10000;
  pointer-events: none;
  line-height: 1.4;
}

.tooltip-text::after {
  content: '';
  position: absolute;
  right: 100%;
  top: 50%;
  transform: translateY(-50%);
  border: 6px solid transparent;
  border-right-color: var(--color-surface-elevated);
}

.tooltip-container:hover .tooltip-text {
  opacity: 1;
  visibility: visible;
}

.content-area {
  background: transparent;
  border: none;
  padding: 0;
  min-height: 600px;
  position: relative;
  overflow-y: auto;
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

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateX(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
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

@media (max-width: 1024px) {
  .analysis-workspace {
    grid-template-columns: 1fr;
  }

  .sidebar-nav {
    position: static;
  }

  .nav-menu {
    flex-direction: row;
    overflow-x: auto;
  }

  .nav-item {
    flex-direction: column;
    min-width: 100px;
    text-align: center;
  }
}

@media (max-width: 768px) {
  .analysis-view {
    padding: var(--space-md);
  }

  .header-compact {
    grid-template-columns: 1fr;
    gap: var(--space-sm);
  }

  .nav-menu {
    gap: var(--space-xs);
  }

  .nav-item {
    padding: var(--space-sm);
    font-size: var(--font-size-sm);
  }

  .tooltip-text {
    left: 50%;
    top: 100%;
    transform: translateX(-50%) translateY(8px);
    width: 200px;
  }

  .tooltip-text::after {
    right: auto;
    bottom: 100%;
    top: auto;
    left: 50%;
    transform: translateX(-50%);
    border-right-color: transparent;
    border-bottom-color: var(--color-surface-elevated);
  }

  .tooltip-icon {
    width: 12px;
    height: 12px;
    font-size: 9px;
  }
}
</style>
