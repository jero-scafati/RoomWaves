<script setup>
// ============================================================================
// IMPORTS
// ============================================================================
import { ref, watch } from 'vue';
import ApiService from '@/services/ApiService.js';
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
  // Automatically fetch data for the current active tab
  fetchDataForActiveTab();
};

const handleExampleSelected = async (filename) => {
  // For examples, we need to fetch the file and upload it to backend for analysis
  try {
    // Fetch the example file from public folder
    const response = await fetch(`/examples/${filename}`);
    if (!response.ok) {
      console.error('Failed to fetch example file');
      return;
    }
    
    // Convert to File object
    const blob = await response.blob();
    const file = new File([blob], filename, { type: blob.type });
    
    // Upload to backend
    const uploadResponse = await ApiService.uploadFile(file);
    
    // Use the uploaded filename
    uploadedFilename.value = uploadResponse.data.filename;
    
    // Clear all plots
    waveform.clear();
    frequency.clear();
    spectrogram.clear();
    surface3d.clear();
    parameters.clear();
    
    // Automatically fetch data for the current active tab
    fetchDataForActiveTab();
  } catch (err) {
    console.error('Failed to process example file:', err);
  }
};

// ============================================================================
// WATCHERS
// ============================================================================
// Watch for tab changes and automatically fetch data
watch(activeTab, (newTab, oldTab) => {
  if (!uploadedFilename.value) return;
  
  // Clear the previous tab's data
  clearTabData(oldTab);
  
  // Fetch data for the new tab
  fetchDataForActiveTab();
});

// Watch for frequency response bands changes
watch(() => frequency.selectedBands.value, () => {
  if (uploadedFilename.value && activeTab.value === 'frequency' && frequency.isVisible.value) {
    frequency.fetchData(uploadedFilename.value);
  }
});

// Watch for surface3d bands changes
watch(() => surface3d.bands.value, () => {
  if (uploadedFilename.value && activeTab.value === 'surface' && surface3d.isVisible.value) {
    surface3d.fetchData(uploadedFilename.value);
  }
});

// Watch for parameters bands changes
watch(() => parameters.selectedBands.value, () => {
  if (uploadedFilename.value && activeTab.value === 'parameters' && parameters.isVisible.value) {
    parameters.fetchData(uploadedFilename.value);
  }
});

// ============================================================================
// HELPER METHODS
// ============================================================================
const fetchDataForActiveTab = () => {
  if (!uploadedFilename.value) return;
  
  switch (activeTab.value) {
    case 'waveform':
      waveform.fetchData(uploadedFilename.value);
      break;
    case 'frequency':
      frequency.fetchData(uploadedFilename.value);
      break;
    case 'spectrogram':
      spectrogram.fetchData(uploadedFilename.value);
      break;
    case 'surface':
      surface3d.fetchData(uploadedFilename.value);
      break;
    case 'parameters':
      parameters.fetchData(uploadedFilename.value);
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
  <div class="home-view">
    <!-- Header -->
    <!-- File Uploader -->
    <AudioUploader 
      @upload-success="handleUploadSuccess"
      @example-selected="handleExampleSelected"
    />

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
        @update:selectedBands="(val) => frequency.selectedBands.value = val"
      />

      <!-- Spectrogram Tab -->
      <SpectrogramTab
        v-show="activeTab === 'spectrogram'"
        :data="spectrogram.data.value"
        :isLoading="spectrogram.isLoading.value"
        :error="spectrogram.error.value"
        :isVisible="spectrogram.isVisible.value"
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
        @update:dataReduction="(val) => surface3d.dataReduction.value = val"
        @update:bands="(val) => surface3d.bands.value = val"
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
        @update:selectedBands="(val) => parameters.selectedBands.value = val"
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
