# Example Audio Files

This folder contains example audio files used in the convolution tool.

## Required Files

### Dry Audio (Anechoic)
Place these files in this folder:
- `drums.wav` - Anechoic drum sample
- `trumpet.wav` - Anechoic trumpet sample

You can add up to 5 dry audio examples total.

### Impulse Responses
Place these files in this folder:
- `clifford_tower_ir.wav` - Clifford Tower impulse response
- `1a_marble_hall.mp3` - Marble Hall impulse response

You can add up to 5 impulse response examples total.

## File Requirements
- **Format**: WAV, MP3, or other web-compatible audio formats
- **Size**: Keep files under 10MB for best performance
- **Naming**: Use descriptive names without spaces (use underscores or hyphens)

## How to Add New Examples

1. Place your audio file in this folder
2. Update `/frontend/src/views/ConvolveView.vue`:
   - For dry audio: Add to the `exampleAudios` array
   - For IR: Add to the `exampleIRs` array

Example:
```javascript
const exampleAudios = ref([
  { name: 'Drums', filename: 'drums.wav' },
  { name: 'Trumpet', filename: 'trumpet.wav' },
  { name: 'Your Audio', filename: 'your_audio.wav' } // Add here
]);
```

## Notes
- These files are served directly from your frontend
- No backend upload required for example files
- Files are loaded on-demand when selected by the user
