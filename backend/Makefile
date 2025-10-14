.PHONY: test test-verbose test-coverage test-watch clean install help

help:
	@echo "Available commands:"
	@echo "  make install        - Install dependencies"
	@echo "  make test          - Run all tests"
	@echo "  make test-verbose  - Run tests with verbose output"
	@echo "  make test-coverage - Run tests with coverage report"
	@echo "  make test-watch    - Run tests in watch mode"
	@echo "  make clean         - Clean test artifacts"

install:
	pip install -r requirements.txt

test:
	pytest

test-verbose:
	pytest -v

test-coverage:
	pytest --cov=app --cov-report=term-missing --cov-report=html

test-watch:
	pytest --watch

clean:
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete
