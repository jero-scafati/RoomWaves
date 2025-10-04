<script setup>
// ============================================================================
// IMPORTS
// ============================================================================
import { ref } from 'vue';
import AudioUploader from '@/components/AudioUploader.vue';
import WaveformTab from '@/components/tabs/WaveformTab.vue';
import FrequencyTab from '@/components/tabs/FrequencyTab.vue';
import SpectrogramTab from '@/components/tabs/SpectrogramTab.vue';
import Surface3DTab from '@/components/tabs/Surface3DTab.vue';
import ParametersTab from '@/components/tabs/ParametersTab.vue';

// Composables
import { useWaveform } from '@/composables/useWaveform.js';
import { useFrequencyResponse } from '@/composables/useFrequencyResponse.js';
import { useSpectrogram } from '@/composables/useSpectrogram.js';
import { useSurface3D } from '@/composables/useSurface3D.js';
import { useParameters } from '@/composables/useParameters.js';

// ============================================================================
// STATE
// ============================================================================
const uploadedFilename = ref('');
const activeTab = ref('waveform');

// Initialize composables
const waveform = useWaveform();
const frequency = useFrequencyResponse();
const spectrogram = useSpectrogram();
const surface3d = useSurface3D();
const parameters = useParameters();

// ============================================================================
// EVENT HANDLERS
// ============================================================================
const handleUploadSuccess = (filename) => {
  uploadedFilename.value = filename;
  // Clear all plots
  waveform.clear();
  frequency.clear();
  spectrogram.clear();
  surface3d.clear();
  parameters.clear();
};

const handleWaveformToggle = () => {
  waveform.toggle(uploadedFilename.value);
};

const handleFrequencyToggle = () => {
  frequency.toggle(uploadedFilename.value);
};

const handleSpectrogramToggle = () => {
  spectrogram.toggle(uploadedFilename.value);
};

const handleSurface3DToggle = () => {
  surface3d.toggle(uploadedFilename.value);
};

const handleSurface3DRefetch = () => {
  surface3d.fetchData(uploadedFilename.value);
};

const handleParametersToggle = () => {
  parameters.toggle(uploadedFilename.value);
};

const handleParametersRefetch = () => {
  parameters.fetchData(uploadedFilename.value);
};
</script>

<template>
  <div class="home-view">
    <!-- Header -->
    <header class="text-center">
      <h1>IR Analyzer</h1>
      <p>Upload your impulse response file to get started.</p>
    </header>

    <hr class="separator" />

    <!-- File Uploader -->
    <AudioUploader @upload-success="handleUploadSuccess" />

    <!-- Navigation Tabs -->
    <nav v-if="uploadedFilename" class="plot-navbar">
      <button 
        class="nav-tab" 
        :class="{ active: activeTab === 'waveform' }"
        @click="activeTab = 'waveform'"
      >
        Waveform
      </button>
      <button 
        class="nav-tab" 
        :class="{ active: activeTab === 'frequency' }"
        @click="activeTab = 'frequency'"
      >
        Frequency Response
      </button>
      <button 
        class="nav-tab" 
        :class="{ active: activeTab === 'spectrogram' }"
        @click="activeTab = 'spectrogram'"
      >
        Spectrogram
      </button>
      <button 
        class="nav-tab" 
        :class="{ active: activeTab === 'surface' }"
        @click="activeTab = 'surface'"
      >
        3D Surface
      </button>
      <button 
        class="nav-tab" 
        :class="{ active: activeTab === 'parameters' }"
        @click="activeTab = 'parameters'"
      >
        Parameters
      </button>
    </nav>

    <!-- Plot Content Area -->
    <section v-if="uploadedFilename" class="plot-section">
      
      <!-- Waveform Tab -->
      <WaveformTab
        v-show="activeTab === 'waveform'"
        :chartData="waveform.chartData.value"
        :isLoading="waveform.isLoading.value"
        :error="waveform.error.value"
        :isVisible="waveform.isVisible.value"
        @toggle="handleWaveformToggle"
      />

      <!-- Frequency Response Tab -->
      <FrequencyTab
        v-show="activeTab === 'frequency'"
        :chartData="frequency.chartData.value"
        :isLoading="frequency.isLoading.value"
        :error="frequency.error.value"
        :isVisible="frequency.isVisible.value"
        :selectedBands="frequency.selectedBands.value"
        :bandsOptions="frequency.bandsOptions"
        @toggle="handleFrequencyToggle"
        @update:selectedBands="(val) => frequency.selectedBands.value = val"
      />

      <!-- Spectrogram Tab -->
      <SpectrogramTab
        v-show="activeTab === 'spectrogram'"
        :data="spectrogram.data.value"
        :isLoading="spectrogram.isLoading.value"
        :error="spectrogram.error.value"
        :isVisible="spectrogram.isVisible.value"
        @toggle="handleSpectrogramToggle"
      />

      <!-- 3D Surface Tab -->
      <Surface3DTab
        v-show="activeTab === 'surface'"
        :data="surface3d.data.value"
        :isLoading="surface3d.isLoading.value"
        :error="surface3d.error.value"
        :isVisible="surface3d.isVisible.value"
        :dataReduction="surface3d.dataReduction.value"
        :bands="surface3d.bands.value"
        :bandsOptions="surface3d.bandsOptions"
        @toggle="handleSurface3DToggle"
        @update:dataReduction="(val) => surface3d.dataReduction.value = val"
        @update:bands="(val) => surface3d.bands.value = val"
        @refetch="handleSurface3DRefetch"
      />

      <!-- Parameters Tab -->
      <ParametersTab
        v-show="activeTab === 'parameters'"
        :data="parameters.data.value"
        :isLoading="parameters.isLoading.value"
        :error="parameters.error.value"
        :isVisible="parameters.isVisible.value"
        :selectedBands="parameters.selectedBands.value"
        :bandsOptions="parameters.bandsOptions"
        @toggle="handleParametersToggle"
        @update:selectedBands="(val) => parameters.selectedBands.value = val"
        @refetch="handleParametersRefetch"
      />

    </section>
  </div>
</template>

<style scoped>
.home-view {
  max-width: 1000px;
  margin: 0 auto;
  padding: 2rem;
  text-align: center;
}

.separator {
  border: none;
  border-top: 1px solid #3a3a3a;
  margin: 2rem 0;
}

/* Navigation Tabs */
.plot-navbar {
  display: flex;
  justify-content: center;
  gap: 0;
  margin: 2rem 0 0 0;
  background-color: #1a1a1a;
  border-radius: 8px 8px 0 0;
  padding: 0.5rem;
  border-bottom: 2px solid #3a3a3a;
}

.nav-tab {
  background-color: transparent;
  color: #a0a0a0;
  border: none;
  padding: 12px 24px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;
  font-size: 0.95rem;
  border-radius: 6px;
}

.nav-tab:hover {
  background-color: #2a2a2a;
  color: #e0e0e0;
}

.nav-tab.active {
  background-color: #3b82f6;
  color: white;
}

/* Plot Section */
.plot-section {
  background-color: #1a1a1a;
  border-radius: 0 0 8px 8px;
  padding: 1.5rem;
  min-height: 500px;
}
</style>
