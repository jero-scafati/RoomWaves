# RoomWaves Frontend

Modern Vue.js web interface for acoustic analysis and impulse response processing. Provides an intuitive UI for uploading audio files, visualizing acoustic data, and generating analysis reports.

## Features

- **📤 File Upload**: Drag-and-drop audio file upload with format validation
- **📊 Interactive Visualizations**: 3D surface plots, spectrograms, and frequency response charts
- **🎵 Audio Playback**: Built-in audio player for uploaded files
- **📈 Real-time Analysis**: Live acoustic parameter calculations
- **🔄 Convolution Tool**: Convolve dry audio with impulse responses
- **📄 PDF Export**: Generate and download comprehensive analysis reports
- **🎨 Modern UI**: Clean, responsive design with smooth animations
- **🌐 Multi-view Navigation**: Home, RIR Analysis, and Convolution views

## Requirements

- Node.js 20.19+ or 22.12+
- npm (Node package manager)

## Setup

### 1. Install Dependencies

```bash
npm install
```

### 2. Configuration (Optional)

The frontend automatically connects to the backend at `http://localhost:8000`. To change this, update the API base URL in `src/services/ApiService.js`:

```javascript
const API_BASE_URL = 'http://localhost:8000';
```

## Run

### Development Mode

```bash
npm run dev
```

App available at `http://localhost:5173`

The development server includes:
- Hot Module Replacement (HMR)
- Vue DevTools integration
- Fast refresh on file changes

### Preview Production Build

```bash
npm run build
npm run preview
```

## Build

### Production Build

```bash
npm run build
```

The optimized production files will be generated in the `dist/` directory.

Build features:
- Minified JavaScript and CSS
- Tree-shaking for smaller bundle size
- Asset optimization
- Source maps for debugging

## Docker

### Build Image

```bash
docker build -t roomwaves-frontend .
```

### Run Container

```bash
docker run -p 80:80 roomwaves-frontend
```

### Custom Port

```bash
docker run -p 8080:80 roomwaves-frontend
```

## Project Structure

```
frontend/
├── public/
│   ├── examples/           # Example audio files
│   │   └── README.md       # Instructions for adding examples
│   └── roomwaves.svg       # App logo
├── src/
│   ├── assets/
│   │   ├── design-tokens.css  # Design system variables
│   │   └── main.css           # Global styles
│   ├── components/
│   │   ├── AudioUploader.vue  # File upload component
│   │   ├── Footer.vue         # App footer
│   │   └── Navbar.vue         # Navigation bar
│   ├── composables/
│   │   └── useSurface3D.js    # 3D surface plot logic
│   ├── services/
│   │   └── ApiService.js      # Backend API client
│   ├── views/
│   │   ├── HomeView.vue       # Main analysis view
│   │   ├── RIRView.vue        # RIR calculation view
│   │   └── ConvolveView.vue   # Convolution view
│   ├── router/
│   │   └── index.js           # Vue Router configuration
│   ├── App.vue                # Root component
│   └── main.js                # Application entry point
├── index.html                 # HTML template
├── package.json               # Dependencies and scripts
├── vite.config.js             # Vite configuration
└── Dockerfile                 # Docker configuration
```

## Tech Stack

### Core
- **Vue 3** (3.5.18) - Progressive JavaScript framework
- **Vue Router** (4.5.1) - Official router for Vue.js
- **Vite** (7.0.6) - Next-generation frontend build tool

### Visualization
- **ECharts** (5.6.0) - Powerful charting library
- **ECharts GL** (2.0.9) - 3D visualization extension
- **vue-echarts** (6.7.3) - Vue integration for ECharts

### Utilities
- **Axios** (1.12.2) - HTTP client for API requests
- **jsPDF** (2.5.2) - PDF generation
- **jspdf-autotable** (3.8.4) - Table generation for PDFs

### Development
- **@vitejs/plugin-vue** (6.0.1) - Vue 3 plugin for Vite
- **vite-plugin-vue-devtools** (8.0.0) - Vue DevTools integration

## Development

### Adding New Views

1. Create a new view component in `src/views/`
2. Add the route in `src/router/index.js`
3. Update navigation in `src/components/Navbar.vue`

Example:
```javascript
// src/router/index.js
import MyNewView from '../views/MyNewView.vue'

const routes = [
  // ... existing routes
  {
    path: '/my-view',
    name: 'MyView',
    component: MyNewView
  }
]
```

### Adding New Components

1. Create component in `src/components/`
2. Import and use in your views

```vue
<script setup>
import MyComponent from '@/components/MyComponent.vue'
</script>

<template>
  <MyComponent />
</template>
```

### Working with the API

The `ApiService.js` provides methods for all backend endpoints:

```javascript
import ApiService from '@/services/ApiService'

// Upload file
const response = await ApiService.uploadAudio(file)

// Calculate parameters
const params = await ApiService.calculateParameters(audioData, sampleRate)

// Generate plot
const plotData = await ApiService.generatePlot(audioData, plotType)
```

### Styling

The project uses a design token system defined in `src/assets/design-tokens.css`:

```css
/* Use design tokens in your components */
.my-element {
  color: var(--color-primary);
  padding: var(--spacing-md);
  border-radius: var(--radius-md);
}
```

## Example Audio Files

Example audio files for the convolution tool are located in `public/examples/`. See [public/examples/README.md](public/examples/README.md) for instructions on adding new examples.

**Note**: Large audio files (*.wav, *.mp3) in the examples directory are excluded from git. You'll need to add your own example files locally.

## Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build locally

## Environment Variables

Create a `.env` file for environment-specific configuration:

```env
VITE_API_BASE_URL=http://localhost:8000
```

Access in code:
```javascript
const apiUrl = import.meta.env.VITE_API_BASE_URL
```

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)

## Troubleshooting

### Port Already in Use

If port 5173 is already in use, Vite will automatically try the next available port. You can also specify a custom port:

```bash
npm run dev -- --port 3000
```

### Build Errors

Clear the cache and rebuild:
```bash
rm -rf node_modules dist
npm install
npm run build
```

### API Connection Issues

Ensure the backend is running at `http://localhost:8000` and CORS is properly configured.

## License

See [LICENSE](../LICENSE) file for details.
