.PHONY: install test lint format run-backend run-frontend docker-up clean

install:
	pip install -r requirements.txt
	pip install -e .

install-dev:
	pip install -r requirements-dev.txt
	pip install -e .[dev]

test:
	pytest tests/ -v --cov=src

lint:
	flake8 src/ backend/
	mypy src/

format:
	black src/ backend/ tests/

run-backend:
	cd backend && uvicorn app.main:app --reload --port 8002

run-frontend:
	cd frontend && npm run dev

docker-up:
	docker-compose -f docker/docker-compose.yml up -d

docker-down:
	docker-compose -f docker/docker-compose.yml down

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache .coverage htmlcov/

help:
	@echo "Available commands:"
	@echo "  make install       - Install dependencies"
	@echo "  make test          - Run tests"
	@echo "  make lint          - Run linters"
	@echo "  make format        - Format code"
	@echo "  make run-backend   - Start backend server"
	@echo "  make run-frontend  - Start frontend dev server"
	@echo "  make docker-up     - Start Docker containers"
	@echo "  make clean         - Remove cache files"
