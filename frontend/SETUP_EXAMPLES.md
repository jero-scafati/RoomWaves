# Setting Up Example Audio Files

## Quick Setup

Place your example audio files in: `/frontend/public/examples/`

### Required Files (based on current configuration):

**Dry Audio (Anechoic):**
- `drums.wav`
- `trumpet.wav`

**Impulse Responses:**
- `clifford_tower_ir.wav`
- `1a_marble_hall.mp3`

## Where to Find Example Files

### Free Impulse Response Sources:
1. **OpenAIR** - http://www.openairlib.net/
   - High-quality IRs from real spaces
   - Free for non-commercial use

2. **Voxengo** - https://www.voxengo.com/impulses/
   - Free convolution impulse responses

3. **EchoThief** - http://www.echothief.com/
   - Professional IRs (some free)

### Free Anechoic Audio Sources:
1. **Freesound** - https://freesound.org/
   - Search for "anechoic" or "dry"
   
2. **University of Iowa Musical Instrument Samples**
   - http://theremin.music.uiowa.edu/

## How to Convert Audio Files

If you need to convert files to WAV format:

```bash
# Using ffmpeg (install with: brew install ffmpeg or apt-get install ffmpeg)
ffmpeg -i input.mp3 output.wav

# Convert to 16-bit WAV for smaller size
ffmpeg -i input.mp3 -acodec pcm_s16le output.wav
```

## Adding More Examples

To add more examples beyond the current 4:

1. Place the file in `/frontend/public/examples/`
2. Edit `/frontend/src/views/ConvolveView.vue`
3. Add to the appropriate array:

```javascript
// For dry audio
const exampleAudios = ref([
  { name: 'Drums', filename: 'drums.wav' },
  { name: 'Trumpet', filename: 'trumpet.wav' },
  { name: 'Your Audio', filename: 'your_file.wav' } // Add here
]);

// For impulse responses
const exampleIRs = ref([
  { name: 'Clifford Tower', filename: 'clifford_tower_ir.wav' },
  { name: 'Marble Hall', filename: '1a_marble_hall.mp3' },
  { name: 'Your IR', filename: 'your_ir.wav' } // Add here
]);
```

## Testing

1. Place files in `/frontend/public/examples/`
2. Start the dev server: `npm run dev`
3. Go to the Convolve page
4. Select an example from the dropdown
5. You should see the audio player with the file ready to play

## File Size Recommendations

- **Dry Audio**: < 5 MB each
- **Impulse Responses**: < 2 MB each
- Keep total size under 50MB for all examples combined

This ensures fast loading times for users!
