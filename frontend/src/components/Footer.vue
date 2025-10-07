<script setup>
const currentYear = new Date().getFullYear();
</script>

<template>
  <footer class="footer">
    <div class="footer-container">
      <div class="footer-content">
        <div class="footer-logo">
          <span class="logo-icon">🌊</span>
          <span class="logo-text">RoomWaves</span>
        </div>
        <p class="footer-description">
          Advanced impulse response analysis and signal generation for room acoustics
        </p>
        <p class="footer-copyright">
          © {{ currentYear }} RoomWaves. All rights reserved.
        </p>
      </div>
    </div>
  </footer>
</template>

<style scoped>
.footer {
  background-color: var(--color-background-secondary);
  border-top: 1px solid var(--color-border);
  margin-top: auto;
}

.footer-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: var(--space-xl);
}

.footer-content {
  text-align: center;
}

.footer-logo {
  display: inline-flex;
  align-items: center;
  gap: var(--space-sm);
  margin-bottom: var(--space-md);
}

.logo-icon {
  font-size: var(--font-size-2xl);
}

.logo-text {
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-bold);
  background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-light) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.footer-description {
  color: var(--color-text-secondary);
  margin-bottom: var(--space-md);
  font-size: var(--font-size-sm);
}

.footer-copyright {
  color: var(--color-text-tertiary);
  font-size: var(--font-size-xs);
  margin: 0;
}
</style>
