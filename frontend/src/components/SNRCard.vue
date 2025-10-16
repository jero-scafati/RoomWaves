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
        <h4>Calculating SNR...</h4>
      </div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="snr-card error">
      <div class="snr-header">
        <h4>SNR Error</h4>
      </div>
      <p class="error-message">{{ error }}</p>
    </div>

    <!-- SNR Display -->
    <div v-else-if="snr !== null" class="snr-card" :class="quality?.class">
      <div class="snr-header">
        <h4>Signal Quality</h4>
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
  margin-top: 0;
  animation: fadeIn 0.4s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-15px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.snr-card {
  background: var(--glass-background);
  backdrop-filter: blur(var(--glass-blur));
  -webkit-backdrop-filter: blur(var(--glass-blur));
  border-radius: var(--radius-lg);
  padding: var(--space-md);
  border: 1px solid var(--glass-border);
  border-left: 3px solid;
  box-shadow: var(--glass-shadow);
  transition: all var(--transition-base);
  position: relative;
}

.snr-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 4px;
  height: 100%;
  background: currentColor;
  filter: brightness(1.2);
}

.snr-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
  border-color: rgba(255, 255, 255, 0.15);
}

.snr-card.excellent {
  color: #10b981;
}

.snr-card.good {
  color: var(--color-primary-light);
}

.snr-card.questionable {
  color: #f59e0b;
}

.snr-card.poor {
  color: #ef4444;
}

.snr-card.loading {
  color: #6b7280;
}

.snr-card.error {
  color: #ef4444;
}

.snr-header {
  display: flex;
  align-items: center;
  gap: var(--space-xs);
  margin-bottom: var(--space-sm);
}

.snr-header h4 {
  color: var(--color-text-secondary);
  font-size: var(--font-size-sm);
  margin: 0;
  font-weight: var(--font-weight-medium);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.snr-content {
  display: flex;
  align-items: baseline;
  gap: var(--space-sm);
  margin-bottom: var(--space-xs);
}

.snr-value {
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-bold);
  color: var(--color-text-primary);
}

.snr-quality {
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
  padding: 2px var(--space-sm);
  border-radius: var(--radius-sm);
  background: rgba(255, 255, 255, 0.08);
  color: currentColor;
  border: 1px solid currentColor;
  transition: all var(--transition-base);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.snr-description {
  color: var(--color-text-secondary);
  font-size: var(--font-size-xs);
  line-height: var(--line-height-relaxed);
  font-weight: var(--font-weight-normal);
}

.error-message {
  color: var(--color-error);
  font-size: var(--font-size-sm);
  margin: 0;
  font-weight: var(--font-weight-medium);
}

@media (max-width: 768px) {
  .snr-content {
    flex-direction: column;
    gap: var(--space-xs);
    align-items: flex-start;
  }
  
  .snr-value {
    font-size: var(--font-size-lg);
  }

  .snr-card {
    padding: var(--space-sm);
  }
}
</style>
