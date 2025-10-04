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
  background-color: #1a1a1a;
  border-top: 1px solid #3a3a3a;
  margin-top: auto;
}

.footer-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem;
}

.footer-content {
  text-align: center;
}

.footer-logo {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.logo-icon {
  font-size: 1.5rem;
}

.logo-text {
  font-size: 1.3rem;
  font-weight: 700;
  background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.footer-description {
  color: #b0b0b0;
  margin-bottom: 1rem;
  font-size: 0.95rem;
}

.footer-copyright {
  color: #808080;
  font-size: 0.85rem;
  margin: 0;
}
</style>
