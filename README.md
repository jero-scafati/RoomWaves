# RoomWaves

Web application for acoustic analysis and impulse response processing.

## Project Structure

- **backend/** - FastAPI REST API for acoustic processing
- **frontend/** - Vue.js web interface

## Quick Start

### Docker

### Backend
```bash
cd backend
docker build -t roomwaves-backend .
docker run -p 8080:8080 roomwaves-backend
```

### Frontend
```bash
cd frontend
docker build -t roomwaves-frontend .
docker run -p 80:80 roomwaves-frontend
```

## Testing

```bash
cd backend
pytest
```

## Tech Stack

- **Backend:** Python, FastAPI
- **Frontend:** Vue 3, Vite
