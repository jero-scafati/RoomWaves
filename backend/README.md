# RoomWaves Backend

Backend API for acoustic analysis and impulse response processing.

## Setup

Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the API

```bash
uvicorn app.main:app --reload
```

## Testing

The project uses pytest for testing. Tests cover the main acoustic processing functions:

### Quick Start

Run all tests:
```bash
pytest
```

Or use the Makefile:
```bash
make test
```

### Test Commands

```bash
pytest                    # Run all tests
pytest -v                # Verbose output
pytest --cov=app         # With coverage
make test-coverage       # Coverage with HTML report
```

### Test Structure

```
tests/
├── conftest.py                    # Fixtures and synthetic RI generator
├── test_snr.py                    # SNR calculation tests
├── test_parameters_pipeline.py    # Acoustic parameters tests
└── test_edge_cases.py             # Edge cases and integration tests
```

### Coverage

Run tests with coverage report:
```bash
pytest --cov=app --cov-report=html
```

View HTML report: `open htmlcov/index.html`

## Project Structure

```
app/
├── core/          # Configuration
├── routers/       # API endpoints
├── schemas/       # Pydantic models
├── services/      # Business logic
└── utils/         # Pipeline processors
    └── pipeline/
        ├── orchestrator.py    # Main pipeline
        └── processor/         # Signal processors
```
