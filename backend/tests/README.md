# Backend Tests

## Setup

Install test dependencies:
```bash
pip install -r requirements.txt
```

## Running Tests

Run all tests:
```bash
pytest
```

Run specific test file:
```bash
pytest tests/test_snr.py
pytest tests/test_parameters_pipeline.py
```

Run with coverage:
```bash
pytest --cov=app --cov-report=html
```

Run specific test:
```bash
pytest tests/test_snr.py::TestSNRCalculation::test_snr_with_synthetic_signal
```

## Test Structure

- `conftest.py` - Shared fixtures including synthetic RI generator
- `test_snr.py` - Tests for SNR calculation
- `test_parameters_pipeline.py` - Tests for acoustic parameters pipeline

## Fixtures

- `synthetic_ri_single_band` - Single frequency band RI for basic tests
- `synthetic_ri_multi_band` - Multi-band RI with known T60 values
- `known_t60_values` - Expected T60 values for validation
- `known_snr_synthetic` - RI with known SNR for validation
