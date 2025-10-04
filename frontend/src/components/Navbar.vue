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
          <span class="logo-icon">🌊</span>
          <span class="logo-text">RoomWaves</span>
        </div>
        <div class="nav-links">
          <button @click="navigateTo('/analysis')" class="nav-button">
            Analysis
          </button>
          <button @click="navigateTo('/signal')" class="nav-button">
            Signals
          </button>
          <button @click="navigateTo('/about')" class="nav-button">
            About
          </button>
        </div>
      </div>

      <!-- Right Side: GitHub Link -->
      <div class="navbar-right">
        <a
          href="https://github.com/jero-scafati/FastEQ"
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
  background: rgba(26, 26, 26, 0.95);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  position: sticky;
  top: 0;
  z-index: 1000;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
}

.navbar-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.navbar-left {
  display: flex;
  align-items: center;
  gap: 2rem;
}

.logo {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  transition: transform 0.2s ease;
}

.logo:hover {
  transform: scale(1.05);
}

.logo-icon {
  font-size: 1.8rem;
}

.logo-text {
  font-size: 1.5rem;
  font-weight: 700;
  background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.nav-links {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.nav-button {
  background: transparent;
  color: #b0b0b0;
  border: none;
  padding: 0.5rem 1rem;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  border-radius: 6px;
  transition: all 0.3s ease;
}

.nav-button:hover {
  background: rgba(59, 130, 246, 0.1);
  color: #3b82f6;
}

.navbar-right {
  display: flex;
  align-items: center;
}

.github-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: transparent;
  color: #b0b0b0;
  text-decoration: none;
  border-radius: 6px;
  transition: all 0.3s ease;
  border: 1px solid transparent;
}

.github-link:hover {
  background: rgba(255, 255, 255, 0.05);
  color: #e0e0e0;
  border-color: rgba(255, 255, 255, 0.1);
}

.github-icon {
  width: 20px;
  height: 20px;
}

.github-text {
  font-weight: 500;
}

/* Responsive Design */
@media (max-width: 768px) {
  .navbar-container {
    padding: 1rem;
  }

  .navbar-left {
    gap: 1rem;
  }

  .logo-text {
    font-size: 1.2rem;
  }

  .nav-links {
    gap: 0.25rem;
  }

  .nav-button {
    padding: 0.4rem 0.7rem;
    font-size: 0.9rem;
  }

  .github-text {
    display: none;
  }
}

@media (max-width: 480px) {
  .logo-icon {
    font-size: 1.5rem;
  }

  .logo-text {
    font-size: 1rem;
  }

  .nav-button {
    padding: 0.3rem 0.5rem;
    font-size: 0.85rem;
  }
}
</style>
