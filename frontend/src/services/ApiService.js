import axios from 'axios';

// 1. Create and configure an Axios instance.
// This is where you can set the base URL and any default headers.
const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 2. Define and export a function for each API endpoint.
export default {
  uploadFile(file) {
    const formData = new FormData();
    formData.append('file', file);

    // The component doesn't need to know any of this.
    // It just calls the function and gives it a file.
    return apiClient.post('/api/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },

  getPlotData(filePath) {
    return apiClient.get(`/api/plot/${filePath}`);
  },

  getFrequencyData(filePath, bands) {
    return apiClient.get(`/api/frequency-response/${filePath}`, {
      params: { bands }
    });
  },
  
  getSpectrogramData(filePath) {
    return apiClient.get(`/api/spectrogram/${filePath}`);
  },
  getCsdData(filePath, bands) {
    return apiClient.get(`/api/csd/${filePath}`, {
      params: { bands }
    });
  },
  
  getParameters(filePath, bands) {
    return apiClient.get(`/api/parameters/${filePath}`, {
      params: { bands }
    });
  },

  getSNR(filePath) {
    return apiClient.get(`/api/snr/${filePath}`);
  },

  getSignalData(params) {
    return apiClient.get('/api/signal', {
      params: {
        duration: params.duration,
        f_inf: params.f_inf,
        f_sup: params.f_sup,
        fs: params.fs
      }
    });
  },

  getFileUrl(filePath) {
    return apiClient.get(`/api/file-url/${filePath}`);
  },

  calculateIR(recordedSweep, inverseFilter, durationFactor = 4.0) {
    const formData = new FormData();
    formData.append('recorded_sweep', recordedSweep);
    formData.append('inverse_filter', inverseFilter);
    formData.append('duration_factor', durationFactor);

    return apiClient.post('/api/calculate-ir', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
};