<template>
  <div class="about-view">
    <div class="about-content">
      <h1 class="title">About RoomWaves</h1>
      <p class="description">
        RoomWaves is a powerful, open-source tool designed for acousticians,
        audio engineers, and researchers to analyze room impulse responses (RIRs).
        Our goal is to provide a comprehensive, accessible, and free platform for
        acoustic analysis and signal generation.
      </p>

      <h2 class="section-title">Our Mission</h2>
      <p class="section-text">
        We believe that understanding room acoustics should not be limited by
        expensive software. RoomWaves aims to democratize the field by providing
        professional-grade tools that run directly in your browser. Whether you're
        treating a home studio, designing a concert hall, or conducting research,
        RoomWaves provides the insights you need.
      </p>

      <h2 class="section-title">Technology Stack</h2>
      <p class="section-text">
        RoomWaves is built with a modern technology stack to ensure a fast,
        reliable, and interactive experience:
      </p>
      <ul class="tech-stack">
        <li><strong>Frontend:</strong> Vue.js 3, Vite, Axios, Plotly.js</li>
        <li><strong>Backend:</strong> FastAPI (Python), NumPy, SciPy</li>
        <li><strong>Hosting:</strong> Deployed with Vercel and Netlify</li>
      </ul>

      <h2 class="section-title">Contribute</h2>
      <p class="section-text">
        This project is open-source and community-driven. We welcome contributions
        of all kinds, from bug reports and feature requests to code contributions.
        Check out our GitHub repository to get started!
      </p>
    </div>
  </div>
</template>

<style scoped>
.about-view {
  max-width: 900px;
  margin: 0 auto;
  padding: 3rem 2rem;
  color: #e0e0e0;
}

.about-content {
  background-color: #1a1a1a;
  border: 1px solid #3a3a3a;
  border-radius: 12px;
  padding: 2.5rem;
}

.title {
  font-size: 2.8rem;
  font-weight: 700;
  margin-bottom: 1rem;
  text-align: center;
  background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.description {
  font-size: 1.1rem;
  color: #b0b0b0;
  line-height: 1.7;
  text-align: center;
  margin-bottom: 2.5rem;
}

.section-title {
  font-size: 1.8rem;
  font-weight: 600;
  color: #e0e0e0;
  border-bottom: 2px solid #3b82f6;
  display: inline-block;
  padding-bottom: 0.5rem;
  margin-top: 2rem;
  margin-bottom: 1.5rem;
}

.section-text {
  font-size: 1rem;
  color: #b0b0b0;
  line-height: 1.8;
}

.tech-stack {
  list-style: none;
  padding-left: 0;
}

.tech-stack li {
  background-color: #252525;
  border-radius: 8px;
  padding: 1rem;
  margin-bottom: 0.75rem;
  border-left: 4px solid #3b82f6;
}

.tech-stack strong {
  color: #e0e0e0;
}
</style>
