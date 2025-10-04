<script setup>
import { useRouter } from 'vue-router';

const router = useRouter();

const features = [
  {
    icon: '📊',
    title: 'IR Analysis',
    description: 'Comprehensive impulse response analysis with waveform, frequency response, spectrogram, and 3D visualization.'
  },
  {
    icon: '🔊',
    title: 'Signal Generation',
    description: 'Generate exponential sweep and inverse sweep signals for room impulse response measurements.'
  },
  {
    icon: '📈',
    title: 'Advanced Parameters',
    description: 'Extract acoustic parameters like RT60, EDT, Clarity, and Definition from your impulse responses.'
  },
  {
    icon: '🎨',
    title: 'Interactive Visualizations',
    description: 'Beautiful, interactive plots powered by Plotly for in-depth analysis and exploration.'
  }
];
</script>

<template>
  <div class="home-view">
    <!-- Hero Section -->
    <section class="hero">
      <div class="hero-content">
        <div class="hero-icon">🌊</div>
        <h1 class="hero-title">RoomWaves</h1>
        <p class="hero-subtitle">
          Professional Room Impulse Response Analysis & Signal Generation
        </p>
        <p class="hero-description">
          A powerful web-based tool for analyzing room acoustics through impulse response measurements.
          Upload your IR files or generate sweep signals for acoustic measurements.
        </p>
        <div class="hero-buttons">
          <button @click="router.push('/rir')" class="btn btn-primary">
            <span class="btn-icon">📊</span>
            Start Analysis
          </button>
          <button @click="router.push('/signal')" class="btn btn-secondary">
            <span class="btn-icon">🔊</span>
            Generate Signals
          </button>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="features">
      <h2 class="section-title">Features</h2>
      <div class="features-grid">
        <div
          v-for="(feature, index) in features"
          :key="index"
          class="feature-card"
        >
          <div class="feature-icon">{{ feature.icon }}</div>
          <h3 class="feature-title">{{ feature.title }}</h3>
          <p class="feature-description">{{ feature.description }}</p>
        </div>
      </div>
    </section>

    <!-- How It Works Section -->
    <section class="how-it-works">
      <h2 class="section-title">How It Works</h2>
      <div class="steps">
        <div class="step">
          <div class="step-number">1</div>
          <h3 class="step-title">Generate or Upload</h3>
          <p class="step-description">
            Generate sweep signals or upload your pre-recorded impulse response file
          </p>
        </div>
        <div class="step-arrow">→</div>
        <div class="step">
          <div class="step-number">2</div>
          <h3 class="step-title">Analyze</h3>
          <p class="step-description">
            View waveforms, frequency response, spectrograms, and 3D visualizations
          </p>
        </div>
        <div class="step-arrow">→</div>
        <div class="step">
          <div class="step-number">3</div>
          <h3 class="step-title">Extract Parameters</h3>
          <p class="step-description">
            Get acoustic parameters like RT60, EDT, Clarity, and more
          </p>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="cta">
      <h2 class="cta-title">Ready to analyze your room acoustics?</h2>
      <button @click="router.push('/rir')" class="btn btn-cta">
        Get Started Now
      </button>
    </section>
  </div>
</template>

<style scoped>
.home-view {
  width: 100%;
  min-height: calc(100vh - 200px);
}

/* Hero Section */
.hero {
  text-align: center;
  padding: 4rem 2rem;
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(37, 99, 235, 0.05) 100%);
}

.hero-content {
  max-width: 900px;
  margin: 0 auto;
}

.hero-icon {
  font-size: 5rem;
  margin-bottom: 1rem;
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-10px);
  }
}

.hero-title {
  font-size: 3.5rem;
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
  margin-bottom: 1.5rem;
  font-weight: 500;
}

.hero-description {
  font-size: 1.1rem;
  color: #b0b0b0;
  line-height: 1.8;
  margin-bottom: 2.5rem;
  max-width: 700px;
  margin-left: auto;
  margin-right: auto;
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

.btn-icon {
  font-size: 1.3rem;
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

/* Features Section */
.features {
  padding: 4rem 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.section-title {
  text-align: center;
  font-size: 2.5rem;
  font-weight: 700;
  color: #e0e0e0;
  margin-bottom: 3rem;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
}

.feature-card {
  background: #1a1a1a;
  border: 1px solid #3a3a3a;
  border-radius: 12px;
  padding: 2rem;
  text-align: center;
  transition: all 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-5px);
  border-color: #3b82f6;
  box-shadow: 0 8px 25px rgba(59, 130, 246, 0.2);
}

.feature-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.feature-title {
  font-size: 1.3rem;
  font-weight: 600;
  color: #e0e0e0;
  margin-bottom: 1rem;
}

.feature-description {
  color: #b0b0b0;
  line-height: 1.6;
}

/* How It Works Section */
.how-it-works {
  padding: 4rem 2rem;
  background: rgba(26, 26, 26, 0.5);
}

.steps {
  max-width: 1000px;
  margin: 0 auto;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 2rem;
  flex-wrap: wrap;
}

.step {
  flex: 1;
  min-width: 200px;
  text-align: center;
}

.step-number {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  font-size: 1.8rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1rem;
  box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
}

.step-title {
  font-size: 1.3rem;
  font-weight: 600;
  color: #e0e0e0;
  margin-bottom: 0.5rem;
}

.step-description {
  color: #b0b0b0;
  line-height: 1.6;
}

.step-arrow {
  font-size: 2rem;
  color: #3b82f6;
  flex-shrink: 0;
}

/* CTA Section */
.cta {
  padding: 4rem 2rem;
  text-align: center;
}

.cta-title {
  font-size: 2rem;
  font-weight: 700;
  color: #e0e0e0;
  margin-bottom: 2rem;
}

.btn-cta {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  padding: 1.2rem 3rem;
  font-size: 1.2rem;
  box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
}

.btn-cta:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4);
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

  .section-title {
    font-size: 2rem;
  }

  .step-arrow {
    display: none;
  }

  .steps {
    flex-direction: column;
  }
}
</style>
