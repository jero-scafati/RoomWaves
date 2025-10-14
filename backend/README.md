# RoomWaves Backend

FastAPI backend for acoustic analysis and impulse response processing.

## Setup

```bash
pip install -r requirements.txt
```

## Run

```bash
uvicorn app.main:app --reload
```

API available at `http://localhost:8000`

## Testing

```bash
pytest              # Run all tests
pytest -v           # Verbose output
pytest --cov=app    # With coverage
```

## Docker

```bash
docker build -t roomwaves-backend .
docker run -p 8080:8080 roomwaves-backend
```

## Project Structure

```
app/
├── routers/       # API endpoints
├── services/      # Business logic
└── utils/         # Signal processing pipeline
```
