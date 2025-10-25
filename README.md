# RoomWaves

**RoomWaves** is a comprehensive web application for acoustic analysis and impulse response (IR) processing. It provides tools for analyzing room acoustics, processing audio signals, calculating acoustic parameters, and performing convolution operations.


https://github.com/user-attachments/assets/6a89f296-ffe3-4edf-9c1c-b2bd4a1a685e


## Features

- ** Acoustic Analysis**: Calculate key acoustic parameters (RT60, EDT, C50, C80, D50, Ts, etc.)
- ** Signal Processing**: Upload and analyze audio files with advanced signal processing
- ** Visualization**: Interactive 3D surface plots and spectrograms using ECharts
- ** Impulse Response**: Calculate and analyze room impulse responses
- ** SNR Analysis**: Signal-to-noise ratio calculation and visualization
- ** Convolution**: Convolve dry audio with impulse responses
- ** PDF Reports**: Generate comprehensive acoustic analysis reports

## Quick Start

### Prerequisites

- **Backend**: Python 3.9+
- **Frontend**: Node.js 20.19+ or 22.12+

### Local Development

#### 1. Backend Setup

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend API will be available at `http://localhost:8000`  
API documentation at `http://localhost:8000/docs`

#### 2. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend will be available at `http://localhost:5173`

### Docker Deployment

#### Backend
```bash
cd backend
docker build -t roomwaves-backend .
docker run -p 8080:8080 roomwaves-backend
```

#### Frontend
```bash
cd frontend
docker build -t roomwaves-frontend .
docker run -p 80:80 roomwaves-frontend
```

## API Endpoints

- `POST /api/upload` - Upload audio files
- `POST /api/plot` - Generate plots and spectrograms
- `POST /api/parameters` - Calculate acoustic parameters
- `POST /api/signal` - Process audio signals
- `POST /api/snr` - Calculate signal-to-noise ratio
- `POST /api/calculate-ir` - Calculate impulse response

## Configuration

Backend configuration is managed through environment variables. See `backend/app/core/config.py` for available settings.

## License

See [LICENSE](LICENSE) file for details.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Documentation

- **Backend README**: [backend/README.md](backend/README.md)
- **Frontend README**: [frontend/README.md](frontend/README.md)
- **API Documentation**: Available at `/docs` when running the backend
