# 🎚️ Audio Convolution Feature - Complete Guide

## 🔒 Critical Security Note

**NEVER PUT R2 CREDENTIALS IN THE FRONTEND!**

This application uses **presigned URLs** for secure file access:
- ✅ Frontend has NO R2 credentials
- ✅ Frontend requests temporary URLs from backend
- ✅ Backend generates presigned URLs (valid 10 minutes)
- ✅ Frontend uses presigned URLs to download files
- ✅ Credentials stay secure on the server

If you accidentally committed R2 credentials to the frontend:
1. **Immediately rotate your R2 keys** in Cloudflare dashboard
2. Remove credentials from `.env` file
3. Remove from git history using `git filter-branch` or BFG Repo-Cleaner
4. Never commit `.env` files (add to `.gitignore`)

## Overview

The `/convolve` page allows users to apply impulse responses to audio files using Web Audio API convolution. Users can choose from example files or upload their own.

## Architecture

### Key Features
✅ **Example Files from R2** - Pre-loaded drums, trumpet, and IR samples  
✅ **Custom Uploads** - Users can upload their own audio and IRs  
✅ **Smart Upload Logic** - Dry audio stays local, IRs go to R2 for reuse  
✅ **Browser Processing** - All convolution happens client-side  
✅ **No Backend Convolution** - Backend only stores IRs

## File Flow

```
Example Files (R2):
  /examples/drums.wav
  /examples/trumpet.wav
  /examples/clifford_tower_ir.wav
  /examples/1a_marble_hall.mp3

User Uploads (R2):
  /uploads/{filename}  ← Custom IRs uploaded here

Dry Audio (Local):
  Stays in browser, never uploaded to R2
```

## User Workflow

### Option 1: Use Examples
```
1. Select "Use Example Audio" → Choose drums or trumpet
2. Select "Use Example IR" → Choose Clifford Tower or Marble Hall
3. Click "Convolve Audio"
4. Listen and download result
```

### Option 2: Upload Custom Dry Audio
```
1. Select "Upload My Audio" → Choose local file (stays in browser)
2. Select "Use Example IR" → Choose Clifford Tower or Marble Hall
3. Click "Convolve Audio"
4. Listen and download result
```

### Option 3: Upload Custom IR
```
1. Select "Use Example Audio" → Choose drums or trumpet
2. Select "Upload My IR" → Choose IR file
3. Click "Upload IR to R2" → IR is stored in /uploads/
4. Click "Convolve Audio"
5. Listen and download result
```

### Option 4: Full Custom
```
1. Select "Upload My Audio" → Choose local file
2. Select "Upload My IR" → Choose IR file → Upload to R2
3. Click "Convolve Audio"
4. Listen and download result
```

## Environment Configuration

### Frontend (.env)
```env
VITE_API_BASE_URL=http://localhost:8000
```

**🔒 SECURITY NOTE:** The frontend does NOT have R2 credentials or direct bucket URLs. All file access goes through presigned URLs from the backend.

### Backend
The backend securely stores R2 credentials and generates presigned URLs:
```env
R2_ACCESS_KEY_ID=your-access-key
R2_SECRET_ACCESS_KEY=your-secret-key
R2_ACCOUNT_ID=your-account-id
R2_BUCKET_NAME=your-bucket-name
R2_ENDPOINT_URL=https://<account-id>.r2.cloudflarestorage.com
```

**⚠️ NEVER put these credentials in the frontend!**

### Backend
The backend needs R2 credentials to handle `/api/upload` for custom IRs.

## R2 Bucket Structure

```
your-bucket/
├── examples/           ← Public, read-only example files
│   ├── drums.wav
│   ├── trumpet.wav
│   ├── clifford_tower_ir.wav
│   └── 1a_marble_hall.mp3
│
└── uploads/           ← User-uploaded IRs (via /api/upload)
    └── {various IR files}
```

### CORS Configuration

Your R2 bucket must allow browser access:

```json
[
  {
    "AllowedOrigins": [
      "http://localhost:5173",
      "https://yourdomain.com"
    ],
    "AllowedMethods": ["GET", "HEAD"],
    "AllowedHeaders": ["*"],
    "ExposeHeaders": ["Content-Length"],
    "MaxAgeSeconds": 3600
  }
]
```

## Example Files

Make sure these files exist in your R2 bucket at `/examples/`:

1. **drums.wav** - Anechoic drum sample
2. **trumpet.wav** - Anechoic trumpet sample  
3. **clifford_tower_ir.wav** - Clifford Tower impulse response
4. **1a_marble_hall.mp3** - Marble Hall impulse response

## Backend API Endpoints

Two endpoints are needed:

### 1. POST `/api/upload`

Already exists! Used by `/analysis` page. Now also used for uploading custom IRs.

**Request:**
```
Content-Type: multipart/form-data
file: [binary audio file]
```

**Response:**
```json
{
  "filename": "my-ir.wav",
  "url": "https://presigned-url-valid-for-10-min.r2.dev/..."
}
```

The presigned URL is stored in the frontend to use for convolution.

### 2. GET `/api/files/{filename}` ⭐ NEW

Generates a temporary, secure presigned URL for accessing files in R2.

**Request:**
```
GET /api/files/examples/drums.wav
```

**Response:**
```json
{
  "url": "https://presigned-url-valid-for-10-min.r2.dev/..."
}
```

**Implementation:**
```python
@router.get("/files/{filename:path}")
async def get_file_download_link(filename: str):
    """
    Provides a temporary, direct download link for a file in the bucket.
    """
    file_key = filename  # Already includes 'examples/' or 'uploads/'

    # Check if file exists
    try:
        s3_client.head_object(Bucket=settings.R2_BUCKET_NAME, Key=file_key)
    except s3_client.exceptions.ClientError as e:
        if e.response['Error']['Code'] == '404':
            raise HTTPException(status_code=404, detail="File not found")
        else:
            raise HTTPException(status_code=500, detail="Error accessing file")
    
    url = generate_presigned_url(file_key, expiration=600)  # Valid for 10 minutes

    return {"url": url}
```

**Why Presigned URLs?**
- ✅ Frontend never sees R2 credentials
- ✅ URLs expire after 10 minutes (secure)
- ✅ Direct download from R2 (fast)
- ✅ Backend controls access (you can add auth checks here)

## Technical Details

### Dry Audio Handling
- **Example**: 
  1. Frontend calls `GET /api/files/examples/drums.wav`
  2. Backend generates presigned URL (valid 10 min)
  3. Frontend uses presigned URL to fetch file from R2
- **Upload**: Stays in browser as File object, never sent to R2

### IR Handling
- **Example**: 
  1. Frontend calls `GET /api/files/examples/clifford_tower_ir.wav`
  2. Backend generates presigned URL (valid 10 min)
  3. Frontend uses presigned URL to fetch file from R2
- **Upload**: 
  1. Sent to `POST /api/upload`
  2. Backend stores in R2 at `/uploads/`
  3. Backend returns presigned URL
  4. Frontend saves URL for convolution

### Convolution Process
```javascript
1. Create AudioContext
2. Get presigned URLs (if using examples)
   → Call backend: GET /api/files/examples/drums.wav
   → Backend returns: { url: "presigned-url" }
3. Load dry audio (from presigned URL or local File)
4. Load IR (from presigned URL)
5. Decode both to AudioBuffers
6. Create OfflineAudioContext
7. Build chain: Source → Convolver → Destination
8. Render to final AudioBuffer
9. Convert to WAV Blob
10. Create download URL
```

## Component State

```javascript
// Dry audio
dryAudioSource: 'example' | 'upload'
selectedExampleAudio: 'drums.wav' | 'trumpet.wav'
uploadedDryAudioFile: File | null

// Impulse response
irSource: 'example' | 'upload'
selectedExampleIR: 'clifford_tower_ir.wav' | '1a_marble_hall.mp3'
uploadedIRFile: File | null
uploadedIRUrl: string  // R2 URL after upload

// Processing
isProcessing: boolean
isUploadingIR: boolean
convolvedAudioUrl: string
```

## Validation

### Dry Audio File
- Max size: 50MB
- Type: audio/*
- Not uploaded to server

### IR File
- Max size: 20MB
- Type: audio/*
- Must upload to R2 before convolution

## UI/UX Features

### Radio Button Selection
- Clear choice between example/upload
- Visual feedback when selected
- Disabled during processing

### Smart Upload Flow
1. User selects IR file
2. Shows file size
3. "Upload IR to R2" button appears
4. After upload: "✅ IR uploaded successfully!"
5. Convolve button becomes enabled

### Status Messages
- "Initializing..."
- "Loading dry audio..."
- "Loading impulse response..."
- "Convolving audio..."
- "Rendering final audio..."
- "Creating download file..."
- "Complete! Your audio is ready."

### Error Handling
- File size validation
- File type validation
- Network errors (fetch fails)
- R2 upload failures
- Decode errors

## Testing Checklist

### Example Files
- [ ] Verify all 4 example files exist in R2 at `/examples/`
- [ ] Test drums + Clifford Tower
- [ ] Test trumpet + Marble Hall
- [ ] Test drums + Marble Hall
- [ ] Test trumpet + Clifford Tower

### Custom Dry Audio
- [ ] Upload MP3 file
- [ ] Upload WAV file
- [ ] Upload FLAC file
- [ ] Test with example IR
- [ ] Verify file stays local (check network tab)

### Custom IR
- [ ] Select IR file
- [ ] Click upload
- [ ] Verify uploaded to R2
- [ ] Use uploaded IR with example audio
- [ ] Use uploaded IR with custom audio

### Edge Cases
- [ ] Try >50MB dry audio (should fail)
- [ ] Try >20MB IR (should fail)
- [ ] Try non-audio file (should fail)
- [ ] Test with slow network
- [ ] Test CORS errors
- [ ] Test with missing R2 files

### Browser Compatibility
- [ ] Chrome
- [ ] Firefox
- [ ] Safari
- [ ] Edge
- [ ] Mobile Safari
- [ ] Mobile Chrome

## Troubleshooting

### "Failed to fetch audio file"
- Verify backend endpoint `GET /api/files/{filename}` is working
- Check backend has correct R2 credentials
- Verify file exists in R2 at `/examples/`
- Check backend logs for presigned URL generation errors
- Verify presigned URL hasn't expired (valid 10 min)
- Check browser console for network errors

### "Failed to upload IR"
- Check backend `/api/upload` endpoint is working
- Verify R2 credentials in backend
- Check file size < 20MB
- Check network tab for error details

### Convolution produces silence
- Verify both audio files loaded correctly
- Check console for decode errors
- Try with example files first
- Check audio file isn't corrupted

### Download doesn't work
- Check browser popup blocker
- Try different browser
- Check console for errors
- Verify Blob creation succeeded

## Performance

### Typical Processing Times
- Small files (30s): 2-5 seconds
- Medium files (3 min): 10-20 seconds  
- Large files (10 min): 30-60 seconds

### Memory Usage
- Large files may use significant RAM
- Browser may show memory warnings
- Consider adding file length warnings

## Future Enhancements

### Potential Features
1. **Progress bar** during rendering
2. **Wet/dry mix slider**
3. **Preview playback** of dry audio and IR
4. **Multiple IR uploads** at once
5. **IR library management** (list, delete)
6. **Waveform visualization**
7. **Format selection** (WAV/MP3 output)
8. **Batch processing**

## Summary

✅ **Simple**: 2 options for audio, 2 options for IR  
✅ **Fast**: Try examples immediately  
✅ **Flexible**: Upload custom files  
✅ **Efficient**: Only IRs are uploaded, dry audio stays local  
✅ **Reusable**: Uploaded IRs stored in R2 for future use  

The feature is production-ready once you:
1. Add the 4 example files to R2
2. Set `VITE_R2_PUBLIC_URL` in frontend .env
3. Configure R2 CORS
4. Test with examples! 🎉
