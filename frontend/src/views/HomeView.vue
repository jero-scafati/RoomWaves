<script setup>
import { onMounted } from 'vue';
import { useRouter } from 'vue-router';
import ApiService from '@/services/ApiService.js';

const router = useRouter();

onMounted(async () => {
  try {
    await fetch(`${import.meta.env.VITE_API_BASE_URL}/warmup`);
  } catch (err) {
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
          Professional acoustic analysis and signal generation for room impulse responses
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

    <section class="features">
      <div class="feature-card">
        <h3>What is a Room Impulse Response?</h3>
        <p>
          A Room Impulse Response (RIR) captures how a room responds to sound. It contains all acoustic information about the space: 
          early reflections, reverberation, and frequency response. Think of it as an acoustic fingerprint of a room.
        </p>
      </div>

      <div class="feature-card">
        <h3>Analysis Tools</h3>
        <p>
          Visualize impulse responses through multiple perspectives: time-domain waveforms, frequency response curves, 
          spectrograms, and 3D surface plots. Extract acoustic parameters like RT60, EDT, and clarity indices.
        </p>
      </div>

      <div class="feature-card">
        <h3>Convolution</h3>
        <p>
          Apply room acoustics to any audio. Convolve your recordings with impulse responses to simulate how they would 
          sound in different spaces—from small rooms to concert halls.
        </p>
      </div>

      <div class="feature-card">
        <h3>Signal Generation</h3>
        <p>
          Generate exponential sine sweeps for measuring impulse responses in real spaces. Create both direct and 
          inverse sweeps at custom sample rates and frequency ranges for professional acoustic measurements.
        </p>
      </div>
    </section>

    <section class="workflow">
      <div class="workflow-card">
        <h2>How It Works</h2>
        <div class="workflow-steps">
          <div class="workflow-step">
            <div class="step-number">1</div>
            <div class="step-content">
              <h4>Generate Sweep Signal</h4>
              <p>Create an exponential sine sweep signal covering your desired frequency range</p>
            </div>
          </div>
          <div class="workflow-step">
            <div class="step-number">2</div>
            <div class="step-content">
              <h4>Record in Space</h4>
              <p>Play the sweep through a speaker and record it in the room you want to measure</p>
            </div>
          </div>
          <div class="workflow-step">
            <div class="step-number">3</div>
            <div class="step-content">
              <h4>Extract Impulse Response</h4>
              <p>Convolve the recording with the inverse sweep to obtain the room's impulse response</p>
            </div>
          </div>
          <div class="workflow-step">
            <div class="step-number">4</div>
            <div class="step-content">
              <h4>Analyze & Apply</h4>
              <p>Visualize acoustic properties and apply the IR to your audio recordings</p>
            </div>
          </div>
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
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  padding: var(--space-xl);
  overflow: hidden;
  gap: var(--space-3xl);
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

.features {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 1200px;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: var(--space-lg);
}

.feature-card {
  background: var(--glass-background);
  backdrop-filter: blur(var(--glass-blur));
  -webkit-backdrop-filter: blur(var(--glass-blur));
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-xl);
  padding: var(--space-xl);
  box-shadow: var(--glass-shadow);
  transition: all var(--transition-base);
}

.feature-card:hover {
  transform: translateY(-4px);
  border-color: rgba(255, 255, 255, 0.15);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
}

.feature-card h3 {
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-primary);
  margin-bottom: var(--space-sm);
}

.feature-card p {
  color: var(--color-text-secondary);
  line-height: var(--line-height-relaxed);
  font-size: var(--font-size-sm);
}

.workflow {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 900px;
}

.workflow-card {
  background: var(--glass-background);
  backdrop-filter: blur(var(--glass-blur));
  -webkit-backdrop-filter: blur(var(--glass-blur));
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-xl);
  padding: var(--space-2xl);
  box-shadow: var(--glass-shadow);
}

.workflow-card h2 {
  font-size: var(--font-size-2xl);
  font-weight: var(--font-weight-bold);
  color: var(--color-text-primary);
  text-align: center;
  margin-bottom: var(--space-xl);
  background: linear-gradient(135deg, var(--color-primary-light), var(--color-primary));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.workflow-steps {
  display: flex;
  flex-direction: column;
  gap: var(--space-lg);
}

.workflow-step {
  display: flex;
  gap: var(--space-lg);
  align-items: flex-start;
}

.step-number {
  flex-shrink: 0;
  width: 48px;
  height: 48px;
  border-radius: var(--radius-full);
  background: linear-gradient(135deg, var(--color-primary), var(--color-primary-hover));
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-bold);
  box-shadow: 0 4px 16px rgba(47, 9, 136, 0.3);
}

.step-content h4 {
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-primary);
  margin-bottom: var(--space-xs);
}

.step-content p {
  color: var(--color-text-secondary);
  line-height: var(--line-height-relaxed);
  font-size: var(--font-size-sm);
  margin: 0;
}

@media (max-width: 768px) {
  .home-view {
    padding: var(--space-md);
    gap: var(--space-xl);
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

  .features {
    grid-template-columns: 1fr;
  }

  .workflow-card {
    padding: var(--space-lg);
  }

  .workflow-step {
    gap: var(--space-md);
  }

  .step-number {
    width: 40px;
    height: 40px;
    font-size: var(--font-size-base);
  }
}
</style>
