# Backend Tests

## Setup

```bash
pip install -r requirements.txt
```

## Running Tests

```bash
pytest                          # Run all tests
pytest tests/services/          # Run service tests
pytest tests/services/test_get_snr.py  # Run SNR tests only
```

Run with coverage:
```bash
pytest --cov=app --cov-report=html
```

## Test Structure

```
tests/
├── conftest.py                      # Shared fixtures
└── services/
    ├── test_get_snr.py              # SNR calculation tests
    └── test_get_parameters.py       # Parameters pipeline tests
```

Tests mirror the `app/` structure for easy navigation.

## Fixtures (conftest.py)

- `synthetic_ri_single_band` - Single frequency band RI
- `synthetic_ri_multi_band` - Multi-band RI with known T60 values
- `known_t60_values` - Expected T60 values
- `known_snr_synthetic` - RI with known SNR
