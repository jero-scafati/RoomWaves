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
    <div class="background-pattern"></div>
    
    <section class="hero">
      <div class="hero-card">
        <h1 class="hero-title">Roomwaves</h1>
        <p class="hero-subtitle">Room Impulse Response Analysis</p>
        <p class="hero-description">
          Analyze room acoustics with interactive visualizations and audio convolution
        </p>
        <div class="hero-buttons">
          <button @click="router.push('/analysis')" class="btn btn-primary">
            Start Analysis
          </button>
          <button @click="router.push('/signal')" class="btn btn-secondary">
            Generate Signals
          </button>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.home-view {
  position: relative;
  width: 100%;
  min-height: calc(100vh - 200px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--space-xl);
  overflow: hidden;
}

.background-pattern {
  position: absolute;
  inset: 0;
  background: 
    radial-gradient(circle at 20% 30%, rgba(138, 43, 226, 0.15) 0%, transparent 50%),
    radial-gradient(circle at 80% 70%, rgba(47, 9, 136, 0.15) 0%, transparent 50%),
    radial-gradient(circle at 50% 50%, rgba(59, 130, 246, 0.08) 0%, transparent 70%);
  animation: float 20s ease-in-out infinite;
  z-index: 0;
}

@keyframes float {
  0%, 100% { transform: translate(0, 0) scale(1); }
  50% { transform: translate(-20px, 20px) scale(1.05); }
}

.hero {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 700px;
  margin: 0 auto;
}

.hero-card {
  text-align: center;
  padding: var(--space-2xl);
  background: var(--glass-background);
  backdrop-filter: blur(var(--glass-blur));
  -webkit-backdrop-filter: blur(var(--glass-blur));
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-2xl);
  box-shadow: var(--glass-shadow);
  transition: all var(--transition-base);
  position: relative;
  overflow: hidden;
}

.hero-card::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: var(--radius-2xl);
  padding: 1px;
  background: linear-gradient(135deg, 
    rgba(138, 43, 226, 0.2), 
    transparent 50%, 
    rgba(47, 9, 136, 0.1));
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  pointer-events: none;
}

.hero-card:hover {
  transform: translateY(-4px);
  border-color: rgba(255, 255, 255, 0.15);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
}

.hero-title {
  font-size: var(--font-size-4xl);
  font-weight: var(--font-weight-bold);
  margin-bottom: var(--space-md);
  background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-light) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  position: relative;
  z-index: 1;
}

.hero-subtitle {
  font-size: var(--font-size-lg);
  color: var(--color-text-secondary);
  margin-bottom: var(--space-md);
  font-weight: var(--font-weight-semibold);
  text-transform: uppercase;
  letter-spacing: 1px;
  position: relative;
  z-index: 1;
}

.hero-description {
  font-size: var(--font-size-base);
  color: var(--color-text-secondary);
  line-height: var(--line-height-relaxed);
  margin-bottom: var(--space-xl);
  position: relative;
  z-index: 1;
}

.hero-buttons {
  display: flex;
  gap: var(--space-md);
  justify-content: center;
  flex-wrap: wrap;
  position: relative;
  z-index: 1;
}

.btn {
  padding: var(--space-md) var(--space-xl);
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-semibold);
  border-radius: var(--radius-lg);
  border: none;
  cursor: pointer;
  transition: all var(--transition-base);
  position: relative;
  overflow: hidden;
}

.btn::before {
  content: '';
  position: absolute;
  inset: 0;
  background: rgba(255, 255, 255, 0.1);
  transform: translateX(-100%);
  transition: transform 0.3s ease;
}

.btn:hover::before {
  transform: translateX(0);
}

.btn-primary {
  background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-hover) 100%);
  color: white;
  box-shadow: 0 4px 16px rgba(47, 9, 136, 0.3);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 24px rgba(47, 9, 136, 0.4);
}

.btn-secondary {
  background: transparent;
  color: var(--color-primary-text);
  border: 2px solid var(--color-primary-text);
}

.btn-secondary:hover {
  background: rgba(47, 9, 136, 0.1);
  transform: translateY(-2px);
  border-color: var(--color-primary-light);
}

@media (max-width: 768px) {
  .home-view {
    padding: var(--space-md);
  }

  .hero-card {
    padding: var(--space-xl);
  }

  .hero-title {
    font-size: var(--font-size-3xl);
  }

  .hero-subtitle {
    font-size: var(--font-size-base);
  }

  .hero-description {
    font-size: var(--font-size-sm);
  }
  
  .hero-buttons {
    flex-direction: column;
  }
}
</style>
