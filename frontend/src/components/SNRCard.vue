<script setup>
// ============================================================================
// PROPS
// ============================================================================
const props = defineProps({
  snr: Number,
  quality: Object,
  description: String,
  isLoading: Boolean,
  error: String
});
</script>

<template>
  <div v-if="isLoading || snr !== null || error" class="snr-card-wrapper">
    <!-- Loading State -->
    <div v-if="isLoading" class="snr-card loading">
      <div class="snr-header">
        <span class="snr-icon">⏳</span>
        <h4>Calculating SNR...</h4>
      </div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="snr-card error">
      <div class="snr-header">
        <span class="snr-icon">❌</span>
        <h4>SNR Error</h4>
      </div>
      <p class="error-message">{{ error }}</p>
    </div>

    <!-- SNR Display -->
    <div v-else-if="snr !== null" class="snr-card" :class="quality?.class">
      <div class="snr-header">
        <span class="snr-icon">{{ quality?.icon }}</span>
        <h4>Signal Quality (SNR)</h4>
      </div>
      <div class="snr-content">
        <div class="snr-value">{{ snr.toFixed(1) }} dB</div>
        <div class="snr-quality">{{ quality?.label }}</div>
      </div>
      <div class="snr-description">{{ description }}</div>
    </div>
  </div>
</template>

<style scoped>
.snr-card-wrapper {
  margin-top: 1.5rem;
  animation: fadeIn 0.3s ease-in;
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

.snr-card {
  background: linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 100%);
  border-radius: 12px;
  padding: 1.25rem;
  border-left: 4px solid;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
  transition: transform 0.2s ease;
}

.snr-card:hover {
  transform: translateY(-2px);
}

.snr-card.excellent {
  border-left-color: #10b981;
}

.snr-card.good {
  border-left-color: #3b82f6;
}

.snr-card.questionable {
  border-left-color: #f59e0b;
}

.snr-card.poor {
  border-left-color: #ef4444;
}

.snr-card.loading {
  border-left-color: #6b7280;
}

.snr-card.error {
  border-left-color: #ef4444;
}

.snr-header {
  display: flex;
  align-items: center;
  gap: 0.625rem;
  margin-bottom: 0.75rem;
}

.snr-icon {
  font-size: 1.25rem;
}

.snr-header h4 {
  color: #e0e0e0;
  font-size: 0.95rem;
  margin: 0;
  font-weight: 600;
}

.snr-content {
  display: flex;
  align-items: baseline;
  gap: 0.875rem;
  margin-bottom: 0.625rem;
}

.snr-value {
  font-size: 1.75rem;
  font-weight: 700;
  color: #ffffff;
}

.snr-quality {
  font-size: 1rem;
  font-weight: 600;
  padding: 0.2rem 0.625rem;
  border-radius: 6px;
  background-color: rgba(255, 255, 255, 0.1);
}

.excellent .snr-quality {
  color: #10b981;
}

.good .snr-quality {
  color: #3b82f6;
}

.questionable .snr-quality {
  color: #f59e0b;
}

.poor .snr-quality {
  color: #ef4444;
}

.snr-description {
  color: #a0a0a0;
  font-size: 0.85rem;
  line-height: 1.4;
}

.error-message {
  color: #f87171;
  font-size: 0.85rem;
  margin: 0;
}

/* Responsive */
@media (max-width: 768px) {
  .snr-content {
    flex-direction: column;
    gap: 0.5rem;
    align-items: flex-start;
  }
  
  .snr-value {
    font-size: 1.5rem;
  }
}
</style>
