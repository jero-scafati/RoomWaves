<script setup>
import { onMounted } from 'vue';
import { useRouter } from 'vue-router';
import ApiService from '@/services/ApiService.js';

const router = useRouter();

// Warmup API on mount to avoid coldstarts
onMounted(async () => {
  try {
    // Make a simple request to warm up the backend
    await fetch(import.meta.env.VITE_API_BASE_URL);
  } catch (err) {
    // Silently fail - this is just for warmup
    console.log('API warmup attempted');
  }
});
</script>

<template>
  <div class="home-view">
    <!-- Hero Section -->
    <section class="hero">
      <div class="hero-content">
        <h1 class="hero-title">Roomwaves</h1>
        <p class="hero-subtitle">
          Room Impulse Response Analysis
        </p>
        <p class="hero-description">
          Analyze room acoustics, generate signals, and apply convolution effects.
        </p>
        <div class="hero-buttons">
          <button @click="router.push('/analysis')" class="btn btn-primary">
            Start Analysis
          </button>
          <button @click="router.push('/signal')" class="btn btn-secondary">
            Generate Signals
          </button>
          <button @click="router.push('/convolve')" class="btn btn-secondary">
            Convolve Audio
          </button>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.home-view {
  width: 100%;
  min-height: calc(100vh - 200px);
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Hero Section */
.hero {
  text-align: center;
  padding: 4rem 2rem;
  width: 100%;
}

.hero-content {
  max-width: 800px;
  margin: 0 auto;
}

.hero-title {
  font-size: 4rem;
  font-weight: 800;
  margin-bottom: 1rem;
  background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-subtitle {
  font-size: 1.5rem;
  color: #e0e0e0;
  margin-bottom: 1rem;
  font-weight: 500;
}

.hero-description {
  font-size: 1.1rem;
  color: #b0b0b0;
  line-height: 1.8;
  margin-bottom: 2.5rem;
}

.hero-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem 2rem;
  font-size: 1.1rem;
  font-weight: 600;
  border-radius: 10px;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-primary {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
}

.btn-primary:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4);
}

.btn-secondary {
  background: transparent;
  color: #3b82f6;
  border: 2px solid #3b82f6;
}

.btn-secondary:hover {
  background: rgba(59, 130, 246, 0.1);
  transform: translateY(-3px);
}

/* Responsive Design */
@media (max-width: 768px) {
  .hero-title {
    font-size: 2.5rem;
  }

  .hero-subtitle {
    font-size: 1.2rem;
  }

  .hero-description {
    font-size: 1rem;
  }
  
  .hero-buttons {
    flex-direction: column;
    align-items: stretch;
  }
}
</style>
