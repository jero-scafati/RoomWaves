<script setup>
import { ref } from 'vue';
import ApiService from '@/services/ApiService.js';

const selectedFile = ref(null);
const isLoading = ref(false);
const uploadStatus = ref('');
const uploadError = ref(false);
const emit = defineEmits(['upload-success']);


const handleFileChange = (event) => {
  selectedFile.value = event.target.files[0];
  uploadStatus.value = '';
  uploadError.value = false;
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
</script>

<template>
  <section class="upload-section">
    <h2>Upload an Audio File</h2>
    <input type="file" @change="handleFileChange" accept="audio/*" />
    <button @click="uploadFile" :disabled="!selectedFile || isLoading">
      {{ isLoading ? 'Uploading...' : 'Upload and Process' }}
    </button>
    <p v-if="uploadStatus" :class="{ 'success': !uploadError, 'error': uploadError }">
      {{ uploadStatus }}
    </p>
  </section>
</template>

<style scoped>
.upload-section {
  /* You can add component-specific styles here */
}
.success {
  color: #34d399; /* A more modern green */
}
.error {
  color: #f87171; /* A softer red */
}
</style>