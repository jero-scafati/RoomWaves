<script setup>
import { useRouter } from 'vue-router';

const router = useRouter();

const navigateTo = (path) => {
  router.push(path);
};
</script>

<template>
  <nav class="navbar">
    <div class="navbar-container">
      <!-- Left Side: Logo and Navigation -->
      <div class="navbar-left">
        <div class="logo" @click="navigateTo('/')">
          <span class="logo-text">Roomwaves</span>
        </div>
        <div class="nav-links">
          <button @click="navigateTo('/analysis')" class="nav-button">
            Analysis
          </button>
          <button @click="navigateTo('/signal')" class="nav-button">
            Signals
          </button>
        </div>
      </div>

      <!-- Right Side: GitHub Link -->
      <div class="navbar-right">
        <a
          href="https://github.com/jero-scafati/RoomWaves"
          target="_blank"
          rel="noopener noreferrer"
          class="github-link"
        >
          <svg
            class="github-icon"
            viewBox="0 0 24 24"
            fill="currentColor"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
          </svg>
          <span class="github-text">GitHub</span>
        </a>
      </div>
    </div>
  </nav>
</template>

<style scoped>
.navbar {
  background: var(--glass-background);
  backdrop-filter: blur(var(--glass-blur));
  -webkit-backdrop-filter: blur(var(--glass-blur));
  border-bottom: 1px solid var(--glass-border);
  position: sticky;
  top: 0;
  z-index: var(--z-navbar);
  box-shadow: var(--glass-shadow);
}

.navbar-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: var(--space-md) var(--space-xl);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.navbar-left {
  display: flex;
  align-items: center;
  gap: var(--space-xl);
}

.logo {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.logo-text {
  font-size: var(--font-size-2xl);
  font-weight: var(--font-weight-bold);
  color: var(--color-text-primary);
}

.nav-links {
  display: flex;
  gap: var(--space-sm);
  align-items: center;
}

.nav-button {
  background: transparent;
  color: var(--color-text-secondary);
  border: none;
  padding: var(--space-sm) var(--space-md);
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-medium);
  cursor: pointer;
  border-radius: var(--radius-md);
  transition: color var(--transition-base);
  position: relative;
}

.nav-button::after {
  content: '';
  position: absolute;
  bottom: 6px;
  left: var(--space-md);
  width: calc(100% - var(--space-xl));
  height: 2px;
  background-color: var(--color-text-primary);
  transform: scaleX(0);
  transform-origin: right;
  transition: transform 0.3s ease;
}

.nav-button:hover {
  color: var(--color-text-primary);
}

.nav-button:hover::after {
  transform: scaleX(1);
  transform-origin: left;
}

.navbar-right {
  display: flex;
  align-items: center;
}

.github-link {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  padding: var(--space-sm) var(--space-md);
  background: transparent;
  color: var(--color-text-secondary);
  text-decoration: none;
  border-radius: var(--radius-md);
  transition: color var(--transition-base);
  border: 1px solid transparent;
  position: relative;
}

.github-link::after {
  content: '';
  position: absolute;
  bottom: 6px;
  left: var(--space-md);
  width: calc(100% - var(--space-xl));
  height: 2px;
  background-color: var(--color-text-primary);
  transform: scaleX(0);
  transform-origin: right;
  transition: transform 0.3s ease;
}

.github-link:hover {
  color: var(--color-text-primary);
}

.github-link:hover::after {
  transform: scaleX(1);
  transform-origin: left;
}

.github-icon {
  width: 20px;
  height: 20px;
}

.github-text {
  font-weight: var(--font-weight-medium);
}

/* Responsive Design */
@media (max-width: 768px) {
  .navbar-container {
    padding: var(--space-md);
  }

  .navbar-left {
    gap: var(--space-md);
  }

  .logo-text {
    font-size: var(--font-size-xl);
  }

  .nav-links {
    gap: var(--space-xs);
  }

  .nav-button {
    padding: var(--space-xs) var(--space-sm);
    font-size: var(--font-size-sm);
  }

  .github-text {
    display: none;
  }
}

@media (max-width: 480px) {
  .logo-text {
    font-size: var(--font-size-base);
  }

  .nav-button {
    padding: var(--space-xs) var(--space-sm);
    font-size: var(--font-size-sm);
  }
}
</style>
