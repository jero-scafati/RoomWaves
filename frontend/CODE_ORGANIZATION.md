# Code Organization Guide

## Overview
This document describes the organization and structure of the FastEQ Frontend codebase.

## File Structure

```
src/
├── components/          # Reusable Vue components
│   ├── charts/         # Chart visualization components
│   │   ├── WaveformChart.vue
│   │   ├── FrequencyChart.vue
│   │   ├── SpectrogramChart.vue
│   │   └── Surface3dChart.vue
│   ├── tabs/           # Tab-specific components
│   │   ├── WaveformTab.vue
│   │   ├── FrequencyTab.vue
│   │   ├── SpectrogramTab.vue
│   │   └── Surface3DTab.vue
│   └── AudioUploader.vue
├── composables/        # Reusable composition functions
│   ├── useWaveform.js
│   ├── useFrequencyResponse.js
│   ├── useSpectrogram.js
│   └── useSurface3D.js
├── views/              # Page-level components
│   ├── HomeView.vue         # NEW: ~220 lines (current)
│   └── HomeView.old.vue     # OLD: 500+ lines (deprecated)
└── services/           # API and business logic
    └── ApiService.js
```

## Architecture Patterns

### 1. Composables Pattern (Recommended)
The new architecture uses **Vue 3 Composables** to extract and reuse logic:

**Benefits:**
- ✅ Separation of concerns
- ✅ Reusable business logic
- ✅ Easier testing
- ✅ Better code organization
- ✅ Smaller file sizes

**Structure:**
```javascript
// composables/useWaveform.js
export function useWaveform() {
  const chartData = ref(null);
  const isLoading = ref(false);
  const error = ref('');
  
  const fetchData = async (filename) => { /* ... */ };
  const toggle = async (filename) => { /* ... */ };
  const clear = () => { /* ... */ };
  
  return { chartData, isLoading, error, fetchData, toggle, clear };
}
```

### 2. Component Composition Pattern
Break down large views into smaller, focused components:

**Tab Components:**
- Each tab is a separate component (`WaveformTab.vue`, `FrequencyTab.vue`, etc.)
- Responsible only for UI rendering
- Emits events to parent
- Receives data via props

**Benefits:**
- ✅ Single Responsibility Principle
- ✅ Easier to understand and maintain
- ✅ Reusable components
- ✅ Better performance (can use v-show efficiently)

### 3. HomeView.new.vue Structure (Recommended)
The new simplified view (~180 lines):

```javascript
// ============================================================================
// IMPORTS
// ============================================================================
// Vue components and composables

// ============================================================================
// STATE
// ============================================================================
// Minimal state: uploadedFilename, activeTab
// Composables handle feature-specific state

// ============================================================================
// EVENT HANDLERS
// ============================================================================
// Simple event handlers that delegate to composables
```

### 4. Old HomeView.vue Structure (Deprecated)
The old monolithic view (500+ lines) - kept for reference:

```javascript
// ============================================================================
// IMPORTS
// ============================================================================
// All imports grouped at the top

// ============================================================================
// STATE - Global
// ============================================================================
// Global state variables (uploadedFilename, activeTab)

// ============================================================================
// STATE - [Feature Name]
// ============================================================================
// Feature-specific state grouped together

// ============================================================================
// COMPUTED PROPERTIES
// ============================================================================
// All computed properties

// ============================================================================
// EVENT HANDLERS
// ============================================================================
// Event handlers grouped by category

// ============================================================================
// API CALLS - [Feature Name]
// ============================================================================
// API calls grouped by feature
```

### 5. Chart Component Structure
All chart components follow a consistent pattern:

```javascript
// ============================================================================
// IMPORTS
// ============================================================================
// Vue and library imports

// ============================================================================
// PROPS
// ============================================================================
// Component props definition

// ============================================================================
// STATE
// ============================================================================
// Local component state (refs, variables)

// ============================================================================
// CHART INITIALIZATION
// ============================================================================
// Chart setup and configuration logic

// ============================================================================
// LIFECYCLE HOOKS
// ============================================================================
// onMounted, watch, onUnmounted
```

## Migration Guide

To switch from the old to the new architecture:

1. **Backup current HomeView.vue** (already done - it's preserved)
2. **Rename files:**
   ```bash
   mv src/views/HomeView.vue src/views/HomeView.old.vue
   mv src/views/HomeView.new.vue src/views/HomeView.vue
   ```
3. **Test all functionality** - everything should work identically
4. **Remove old file** once confident

## Consistent Patterns

#### Resize Handler Pattern
All chart components use the same resize handler pattern:
```javascript
let resizeHandler = null

// In initChart():
resizeHandler = () => {
  if (chartInstance) {
    chartInstance.resize()
  }
}
window.addEventListener('resize', resizeHandler)

// In onUnmounted():
if (resizeHandler) {
  window.removeEventListener('resize', resizeHandler)
}
```

#### Chart Disposal Pattern
```javascript
onUnmounted(() => {
  if (resizeHandler) {
    window.removeEventListener('resize', resizeHandler)
  }
  if (chartInstance) {
    chartInstance.dispose()
  }
})
```

## Features by Component

### HomeView.vue
- **Purpose**: Main application view with tab-based navigation
- **Features**:
  - File upload handling
  - Tab navigation (Waveform, Frequency Response, Spectrogram, 3D Surface)
  - Plot data management
  - API integration
- **Lines**: ~200 (down from 500+ after reorganization)

### Chart Components

#### WaveformChart.vue
- Displays time-domain waveform
- Uses ECharts line chart
- LTTB sampling for performance

#### FrequencyChart.vue
- Displays frequency response
- Logarithmic x-axis (20Hz - 20kHz)
- Interactive zoom and pan
- Smooth line rendering with glow effect

#### SpectrogramChart.vue
- Time-frequency heatmap visualization
- Custom color mapping for power levels
- Interactive tooltips

#### Surface3dChart.vue
- 3D scatter plot visualization
- Configurable data reduction
- Octave smoothing support
- Interactive 3D controls

## Best Practices

1. **Grouping**: Related code is grouped together with clear section headers
2. **Consistency**: All components follow the same organizational pattern
3. **Comments**: Section headers use consistent formatting
4. **Cleanup**: Proper cleanup in onUnmounted hooks
5. **Naming**: Descriptive variable and function names
6. **Separation**: Logic separated by feature/concern

## Maintenance

When adding new features:
1. Follow the established section structure
2. Add new state in the appropriate STATE section
3. Group related functions together
4. Add clear section headers
5. Maintain consistent patterns across components
