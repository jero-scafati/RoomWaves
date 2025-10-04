# Architecture Overview

## Layer Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        HomeView.vue                         │
│                    (Orchestrator Layer)                     │
│                         ~180 lines                          │
│                                                             │
│  • Manages global state (uploadedFilename, activeTab)      │
│  • Coordinates composables                                 │
│  • Renders tab components                                  │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ uses
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     Composables Layer                       │
│                   (Business Logic)                          │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ useWaveform  │  │useFrequency  │  │useSpectrogram│     │
│  │   ~65 lines  │  │  Response    │  │   ~60 lines  │     │
│  │              │  │  ~70 lines   │  │              │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│                                                             │
│  ┌──────────────┐                                          │
│  │ useSurface3D │                                          │
│  │   ~65 lines  │                                          │
│  └──────────────┘                                          │
│                                                             │
│  Each composable provides:                                 │
│  • State (data, isLoading, error)                          │
│  • Methods (fetchData, toggle, clear)                      │
│  • Computed properties (isVisible)                         │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ calls
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      Services Layer                         │
│                                                             │
│                    ┌──────────────┐                         │
│                    │  ApiService  │                         │
│                    │              │                         │
│                    │ • getPlotData│                         │
│                    │ • getFreqData│                         │
│                    │ • getSpecData│                         │
│                    │ • getCsdData │                         │
│                    └──────────────┘                         │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ HTTP requests
                              ▼
                         Backend API
```

## Component Hierarchy

```
HomeView.vue
├── AudioUploader.vue
├── Navigation Tabs (buttons)
└── Tab Components (conditional rendering)
    ├── tabs/WaveformTab.vue
    │   └── charts/WaveformChart.vue
    ├── tabs/FrequencyTab.vue
    │   └── charts/FrequencyChart.vue
    ├── tabs/SpectrogramTab.vue
    │   └── charts/SpectrogramChart.vue
    └── tabs/Surface3DTab.vue
        └── charts/Surface3dChart.vue
```

## Data Flow

### 1. File Upload Flow
```
User uploads file
    ↓
AudioUploader emits 'upload-success'
    ↓
HomeView.handleUploadSuccess()
    ↓
Sets uploadedFilename
    ↓
Calls clear() on all composables
    ↓
All plots reset
```

### 2. Plot Data Flow (Example: Waveform)
```
User clicks "Plot" button
    ↓
WaveformTab emits 'toggle' event
    ↓
HomeView.handleWaveformToggle()
    ↓
waveform.toggle(uploadedFilename)
    ↓
useWaveform.fetchData()
    ↓
ApiService.getPlotData()
    ↓
HTTP request to backend
    ↓
Response data stored in composable
    ↓
WaveformTab receives updated props
    ↓
WaveformChart renders data
```

### 3. Tab Switching Flow
```
User clicks tab button
    ↓
activeTab ref updated
    ↓
v-show conditionally displays tab component
    ↓
Tab component and its data remain in memory
    ↓
Instant switching (no re-rendering)
```

## Responsibility Matrix

| Layer | Responsibilities | Does NOT Handle |
|-------|-----------------|-----------------|
| **HomeView.vue** | • Tab navigation<br>• File upload coordination<br>• Composable initialization<br>• Event delegation | • API calls<br>• Data transformation<br>• Plot rendering<br>• Styling details |
| **Composables** | • State management<br>• API calls<br>• Data transformation<br>• Business logic | • UI rendering<br>• User events<br>• Styling |
| **Tab Components** | • UI layout<br>• User interactions<br>• Event emission<br>• Props handling | • API calls<br>• Data fetching<br>• Business logic |
| **Chart Components** | • Chart rendering<br>• Chart configuration<br>• ECharts integration | • Data fetching<br>• State management<br>• Parent coordination |

## Communication Patterns

### Props Down, Events Up
```
HomeView.vue
    │
    │ Props ↓
    ├─→ chartData
    ├─→ isLoading
    ├─→ error
    ├─→ isVisible
    │
    │ Events ↑
    ├─← toggle
    ├─← update:selectedBands
    └─← refetch
    │
    ▼
WaveformTab.vue
```

### Composable Pattern
```javascript
// In HomeView.vue
const waveform = useWaveform();

// Access state
waveform.chartData.value
waveform.isLoading.value
waveform.error.value

// Call methods
waveform.toggle(filename)
waveform.clear()
waveform.fetchData(filename)
```

## File Organization Principles

### 1. Separation of Concerns
- **Composables**: Business logic and state
- **Tab Components**: UI and user interaction
- **Chart Components**: Visualization
- **Services**: API communication

### 2. Single Responsibility
Each file has ONE clear purpose:
- `useWaveform.js` - Waveform data management
- `WaveformTab.vue` - Waveform UI
- `WaveformChart.vue` - Waveform visualization

### 3. Dependency Direction
```
Views → Tab Components → Chart Components
  ↓
Composables → Services → Backend API
```

Dependencies flow in one direction (no circular dependencies).

### 4. Reusability
- Composables can be used in any component
- Tab components can be used in different views
- Chart components are completely independent

## Scalability

### Adding a New Plot Type

1. **Create composable** (`composables/useNewPlot.js`)
   ```javascript
   export function useNewPlot() {
     const data = ref(null);
     const isLoading = ref(false);
     const error = ref('');
     
     const fetchData = async (filename) => { /* ... */ };
     const toggle = async (filename) => { /* ... */ };
     const clear = () => { /* ... */ };
     
     return { data, isLoading, error, fetchData, toggle, clear };
   }
   ```

2. **Create tab component** (`components/tabs/NewPlotTab.vue`)
   ```vue
   <template>
     <div class="tab-content">
       <div class="controls">...</div>
       <div class="chart-container">
         <NewPlotChart :data="data" />
       </div>
     </div>
   </template>
   ```

3. **Create chart component** (`components/NewPlotChart.vue`)
   ```vue
   <template>
     <div ref="chartRef"></div>
   </template>
   ```

4. **Add to HomeView.vue**
   ```javascript
   import { useNewPlot } from '@/composables/useNewPlot.js';
   import NewPlotTab from '@/components/tabs/NewPlotTab.vue';
   
   const newPlot = useNewPlot();
   ```

5. **Add tab button and content**
   ```vue
   <button @click="activeTab = 'newplot'">New Plot</button>
   <NewPlotTab v-show="activeTab === 'newplot'" ... />
   ```

**Total changes:** 3 new files + minor updates to HomeView.vue

## Performance Considerations

### 1. Lazy Loading
Tab components can be lazy-loaded:
```javascript
const WaveformTab = defineAsyncComponent(() => 
  import('@/components/tabs/WaveformTab.vue')
);
```

### 2. v-show vs v-if
Using `v-show` keeps components in memory for instant tab switching.

### 3. Composable Efficiency
Each composable manages its own state independently, preventing unnecessary re-renders.

### 4. Chart Instances
Chart instances are properly disposed when components unmount, preventing memory leaks.

## Testing Strategy

### Unit Tests
- **Composables**: Test business logic in isolation
- **Tab Components**: Test UI rendering and events
- **Chart Components**: Test chart configuration

### Integration Tests
- **HomeView**: Test tab navigation and coordination
- **Data Flow**: Test complete user workflows

### Example Test
```javascript
// tests/composables/useWaveform.spec.js
import { useWaveform } from '@/composables/useWaveform';

describe('useWaveform', () => {
  it('should fetch waveform data', async () => {
    const { fetchData, chartData, isLoading } = useWaveform();
    
    await fetchData('test.wav');
    
    expect(isLoading.value).toBe(false);
    expect(chartData.value).toBeDefined();
  });
});
```

## Conclusion

This architecture provides:
- ✅ Clear separation of concerns
- ✅ High modularity and reusability
- ✅ Easy testing
- ✅ Excellent scalability
- ✅ Maintainable codebase
- ✅ Industry best practices

It follows the **Vue 3 Composition API** patterns and modern frontend architecture principles.
