# RoomWaves Backend

FastAPI backend for acoustic analysis and impulse response processing. Provides REST API endpoints for audio signal processing, acoustic parameter calculation, and visualization.

## Features

- **Audio Processing**: Upload and process WAV/MP3 audio files
- **Acoustic Parameters**: Calculate RT60, EDT, C50, C80, D50, Ts, and more
- **Signal Analysis**: FFT, spectrograms, and frequency analysis
- **Impulse Response**: Calculate and analyze room impulse responses
- **SNR Calculation**: Signal-to-noise ratio analysis
- **Visualization**: Generate plots and 3D surface data
- **CORS Support**: Configured for frontend integration

## Requirements

- Python 3.9+
- pip (Python package manager)

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configuration (Optional)

Create a `.env` file in the backend directory for custom configuration:

```env
APP_NAME=RoomWaves
APP_VERSION=1.0.0
ALLOWED_ORIGINS=["http://localhost:5173"]
```

## Run

### Development Mode

```bash
uvicorn app.main:app --reload
```

API available at `http://localhost:8000`  
Interactive API documentation at `http://localhost:8000/docs`  
Alternative docs at `http://localhost:8000/redoc`

### Production Mode

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8080
```

## Testing

```bash
# Run all tests
pytest

# Verbose output
pytest -v

# With coverage report
pytest --cov=app

# Generate HTML coverage report
pytest --cov=app --cov-report=html
```

## Docker

### Build Image

```bash
docker build -t roomwaves-backend .
```

### Run Container

```bash
docker run -p 8080:8080 roomwaves-backend
```

### With Environment Variables

```bash
docker run -p 8080:8080 -e ALLOWED_ORIGINS='["http://localhost:5173"]' roomwaves-backend
```

## Project Structure

```
backend/
├── app/
│   ├── core/
│   │   └── config.py          # Application configuration
│   ├── routers/
│   │   ├── upload.py          # File upload endpoint
│   │   ├── plot.py            # Plot generation
│   │   ├── parameters.py      # Acoustic parameters
│   │   ├── signal.py          # Signal processing
│   │   ├── snr.py             # SNR calculation
│   │   └── calculate_ir.py    # Impulse response
│   ├── services/
│   │   └── plot_service.py    # Plotting business logic
│   ├── utils/
│   │   ├── signals/
│   │   │   └── signals.py     # Signal processing utilities
│   │   └── parameters/
│   │       └── parameters.py  # Acoustic parameter calculations
│   └── main.py                # FastAPI application entry point
├── tests/
│   ├── test_parameters.py     # Parameter calculation tests
│   └── test_signals.py        # Signal processing tests
├── requirements.txt           # Python dependencies
└── Dockerfile                 # Docker configuration
```

## API Endpoints

### Core Endpoints

- `GET /` - API welcome message
- `GET /warmup` - Warmup endpoint for cold starts
- `GET /docs` - Interactive API documentation (Swagger UI)
- `GET /redoc` - Alternative API documentation (ReDoc)

### Processing Endpoints

- `POST /api/upload` - Upload audio files
  - Accepts: WAV, MP3 files
  - Returns: File metadata and audio data

- `POST /api/plot` - Generate plots and spectrograms
  - Accepts: Audio data, plot type
  - Returns: Plot data for visualization

- `POST /api/parameters` - Calculate acoustic parameters
  - Accepts: Audio data, sample rate
  - Returns: RT60, EDT, C50, C80, D50, Ts, etc.

- `POST /api/signal` - Process audio signals
  - Accepts: Audio data, processing parameters
  - Returns: Processed signal data

- `POST /api/snr` - Calculate signal-to-noise ratio
  - Accepts: Audio data, analysis parameters
  - Returns: SNR values and analysis

- `POST /api/calculate-ir` - Calculate impulse response
  - Accepts: Recorded signal, excitation signal
  - Returns: Impulse response data

## Key Dependencies

- **FastAPI** (0.116.2) - Web framework
- **Uvicorn** (0.35.0) - ASGI server
- **NumPy** - Numerical computing
- **SciPy** - Scientific computing
- **Librosa** (0.11.0) - Audio analysis
- **Matplotlib** (3.8.2) - Plotting
- **Pydantic** (2.11.9) - Data validation
- **python-multipart** (0.0.20) - File upload support

## Development

### Adding New Endpoints

1. Create a new router in `app/routers/`
2. Define your endpoint logic
3. Include the router in `app/main.py`

Example:
```python
# app/routers/my_endpoint.py
from fastapi import APIRouter

router = APIRouter()

@router.post("/my-endpoint")
def my_endpoint():
    return {"message": "Hello"}
```

```python
# app/main.py
from app.routers import my_endpoint
app.include_router(my_endpoint.router, prefix="/api", tags=["my-endpoint"])
```

### Running Tests During Development

```bash
# Watch mode (requires pytest-watch)
ptw

# Run specific test file
pytest tests/test_parameters.py

# Run specific test function
pytest tests/test_parameters.py::test_calculate_rt60
```

## Troubleshooting

### Import Errors

If you encounter import errors, ensure you're running commands from the backend directory and have installed all dependencies.

### Port Already in Use

If port 8000 is already in use, specify a different port:
```bash
uvicorn app.main:app --reload --port 8001
```

### CORS Issues

Update `ALLOWED_ORIGINS` in `app/core/config.py` to include your frontend URL.

## License

See [LICENSE](../LICENSE) file for details.
