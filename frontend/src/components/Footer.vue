<script setup>
const currentYear = new Date().getFullYear();
</script>

<template>
  <footer class="footer">
    <div class="footer-container">
      <div class="footer-content">
        <div class="footer-logo">
          <span class="logo-text">Roomwaves</span>
        </div>
        <p class="footer-description">
          Advanced impulse response analysis and signal generation for room acoustics
        </p>
        <a 
          href="https://drive.google.com/file/d/1YLKCTbqL_0Xz0I8lOnpCyhM1cr2EYVEZ/view?usp=sharing" 
          target="_blank" 
          rel="noopener noreferrer"
          class="paper-link"
        >
          Read Paper
        </a>
        <p class="footer-copyright">
          © {{ currentYear }} Roomwaves. All rights reserved.
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
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: var(--space-md);
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

.paper-link {
  display: inline-block;
  color: var(--color-primary-light);
  font-size: var(--font-size-sm);
  text-decoration: none;
  margin-bottom: var(--space-md);
  padding: var(--space-xs) var(--space-md);
  border: 1px solid var(--color-primary);
  border-radius: var(--radius-md);
  font-weight: var(--font-weight-semibold);
  transition: all 0.3s ease;
  background: rgba(47, 9, 136, 0.1);
}

.paper-link:hover {
  background: var(--color-primary);
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(47, 9, 136, 0.3);
}

.footer-copyright {
  color: var(--color-text-tertiary);
  font-size: var(--font-size-xs);
  margin: 0;
}
</style>
