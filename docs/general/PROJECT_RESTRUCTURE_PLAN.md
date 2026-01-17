# 🏗️ UIDAI Analytics - Production-Ready Folder Structure

## Executive Summary

This document outlines a **clean, scalable, industry-standard** folder structure for the UIDAI Aadhaar Analytics platform, following best practices from companies like Google, Microsoft, and leading AI/ML organizations.

---

## 📁 Proposed Folder Structure

```
uidai-analytics/
│
├── .github/                          # GitHub Actions, CI/CD workflows
│   ├── workflows/
│   │   ├── ci.yml
│   │   ├── deploy-backend.yml
│   │   └── deploy-frontend.yml
│   └── ISSUE_TEMPLATE/
│
├── .vscode/                          # VS Code settings (optional, gitignore)
│   ├── settings.json
│   ├── launch.json
│   └── extensions.json
│
├── config/                           # Configuration files
│   ├── development.yaml
│   ├── production.yaml
│   ├── logging.yaml
│   └── database.yaml
│
├── data/                             # Data directory (add to .gitignore)
│   ├── raw/                          # Original, immutable data
│   │   ├── biometric/
│   │   ├── demographic/
│   │   └── enrollment/
│   ├── interim/                      # Intermediate transformed data
│   ├── processed/                    # Final datasets ready for modeling
│   │   ├── clean_biometric_data.csv
│   │   ├── clean_demographic_data.csv
│   │   └── merged_clean_aadhaar_enrolment_data.csv
│   ├── external/                     # External reference data
│   └── outputs/                      # Generated outputs, exports
│       └── predictions/
│
├── docs/                             # Documentation
│   ├── architecture/
│   │   ├── system-design.md
│   │   ├── data-flow.md
│   │   └── api-design.md
│   ├── user-guides/
│   │   ├── EXPORT_QUICK_GUIDE.md
│   │   ├── VISUALIZATION_QUICK_GUIDE.md
│   │   └── deployment-guide.md
│   ├── technical/
│   │   ├── MODEL_ANALYSIS_AND_RECOMMENDATIONS.md
│   │   ├── FEATURES_SUMMARY.md
│   │   └── database-schema.md
│   └── reports/
│       ├── INTEGRATION_STATUS_REPORT.md
│       ├── SYSTEM_STATUS_REPORT.md
│       └── quarterly-analysis.md
│
├── notebooks/                        # Jupyter notebooks
│   ├── 01-exploratory/               # EDA and initial analysis
│   │   ├── biometric_analysis.ipynb
│   │   ├── demographic_eda.ipynb
│   │   └── enrollment_analysis.ipynb
│   ├── 02-experiments/               # Model experiments
│   │   └── feature_importance.ipynb
│   ├── 03-reports/                   # Report-ready notebooks
│   └── README.md
│
├── src/                              # Source code (Python package)
│   ├── __init__.py
│   │
│   ├── core/                         # Core business logic
│   │   ├── __init__.py
│   │   ├── constants.py
│   │   ├── exceptions.py
│   │   └── logging_config.py
│   │
│   ├── data/                         # Data processing pipeline
│   │   ├── __init__.py
│   │   ├── loaders.py                # Data loading utilities
│   │   ├── cleaners.py               # Data cleaning
│   │   ├── validators.py             # Data validation
│   │   └── transformers.py           # Data transformation
│   │
│   ├── features/                     # Feature engineering
│   │   ├── __init__.py
│   │   ├── builders.py               # Feature construction
│   │   ├── selectors.py              # Feature selection
│   │   └── encoders.py               # Categorical encoding
│   │
│   ├── models/                       # ML models
│   │   ├── __init__.py
│   │   ├── base.py                   # Base model class
│   │   ├── demand_model.py
│   │   ├── biometric_model.py
│   │   ├── demographic_model.py
│   │   ├── enrollment_model.py
│   │   ├── trainers.py               # Training logic
│   │   ├── predictors.py             # Prediction logic
│   │   └── evaluators.py             # Model evaluation
│   │
│   ├── analytics/                    # Analysis modules
│   │   ├── __init__.py
│   │   ├── anomaly_detector.py
│   │   ├── trend_analyzer.py
│   │   ├── dashboard_aggregator.py
│   │   └── insights_generator.py
│   │
│   ├── visualization/                # Visualization utilities
│   │   ├── __init__.py
│   │   ├── charts.py
│   │   ├── heatmaps.py
│   │   └── plotters.py
│   │
│   └── utils/                        # Utility functions
│       ├── __init__.py
│       ├── file_utils.py
│       ├── date_utils.py
│       └── validators.py
│
├── backend/                          # Backend API (FastAPI)
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                   # FastAPI app entry
│   │   ├── config.py                 # App configuration
│   │   │
│   │   ├── api/                      # API routes
│   │   │   ├── __init__.py
│   │   │   ├── v1/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── health.py
│   │   │   │   ├── predictions.py
│   │   │   │   ├── dashboard.py
│   │   │   │   ├── analytics.py
│   │   │   │   └── exports.py
│   │   │   └── dependencies.py
│   │   │
│   │   ├── core/                     # Core backend logic
│   │   │   ├── __init__.py
│   │   │   ├── security.py
│   │   │   ├── middleware.py
│   │   │   └── exceptions.py
│   │   │
│   │   ├── schemas/                  # Pydantic models
│   │   │   ├── __init__.py
│   │   │   ├── predictions.py
│   │   │   ├── dashboard.py
│   │   │   └── responses.py
│   │   │
│   │   ├── services/                 # Business logic
│   │   │   ├── __init__.py
│   │   │   ├── model_service.py
│   │   │   ├── dashboard_service.py
│   │   │   └── analytics_service.py
│   │   │
│   │   └── utils/
│   │       ├── __init__.py
│   │       └── helpers.py
│   │
│   ├── tests/                        # Backend tests
│   │   ├── __init__.py
│   │   ├── conftest.py
│   │   ├── test_api/
│   │   └── test_services/
│   │
│   ├── alembic/                      # Database migrations (if using DB)
│   ├── requirements.txt
│   ├── Dockerfile
│   └── README.md
│
├── frontend/                         # Frontend (React + TypeScript)
│   ├── public/
│   ├── src/
│   │   ├── assets/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── hooks/
│   │   ├── utils/
│   │   ├── types/
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── tests/
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   ├── Dockerfile
│   └── README.md
│
├── models/                           # Trained ML models & artifacts
│   ├── demand/
│   │   ├── uidai_demand_model.pkl
│   │   └── metadata.json
│   ├── biometric/
│   │   ├── uidai_biometric_model.pkl
│   │   ├── uidai_biometric_model_info.pkl
│   │   └── metadata.json
│   ├── demographic/
│   │   ├── uidai_demographic_model.pkl
│   │   ├── uidai_demographic_model_info.pkl
│   │   └── metadata.json
│   ├── enrollment/
│   │   ├── uidai_enrollment_model.pkl
│   │   └── metadata.json
│   └── registry.yaml                 # Model registry
│
├── visualizations/                   # Generated visualizations
│   ├── anomalies/
│   ├── heatmaps/
│   ├── lifecycle/
│   └── trends/
│
├── tests/                            # Integration & E2E tests
│   ├── __init__.py
│   ├── integration/
│   │   ├── test_api_integration.py
│   │   └── test_ml_pipeline.py
│   ├── e2e/
│   │   └── test_workflows.py
│   └── fixtures/
│
├── scripts/                          # Utility scripts
│   ├── setup/
│   │   ├── setup_environment.sh
│   │   └── install_dependencies.sh
│   ├── data/
│   │   ├── process_demographic_data.py
│   │   ├── extract_delhi_centers.py
│   │   └── validate_data.py
│   ├── training/
│   │   ├── train_all_models.py
│   │   └── retrain_model.py
│   ├── deployment/
│   │   ├── start_backend.bat
│   │   ├── start_frontend.bat
│   │   ├── start_servers.ps1
│   │   └── deploy.sh
│   ├── debugging/
│   │   ├── debug_anomalies.py
│   │   ├── debug_dashboard.py
│   │   └── debug_locations.py
│   └── utilities/
│       ├── generate_visuals.py
│       └── verify_integration.py
│
├── docker/                           # Docker configurations
│   ├── backend.Dockerfile
│   ├── frontend.Dockerfile
│   └── docker-compose.yml
│
├── .env.example                      # Environment variables template
├── .gitignore
├── .dockerignore
├── pyproject.toml                    # Python project metadata
├── setup.py                          # Package installation
├── requirements.txt                  # Python dependencies (root)
├── requirements-dev.txt              # Development dependencies
├── Makefile                          # Common commands
├── README.md                         # Main README
├── CHANGELOG.md                      # Version history
├── LICENSE
└── START_HERE.md                     # Quick start guide

```

---

## 📋 Folder Purpose & Guidelines

### **Root Level**
| File/Folder | Purpose |
|-------------|---------|
| `.github/` | CI/CD workflows, issue templates, GitHub Actions |
| `.vscode/` | Editor settings (add to .gitignore for personal preferences) |
| `config/` | Configuration files for different environments |
| `docs/` | All documentation (architecture, guides, reports) |
| `data/` | **Data storage (add to .gitignore except README)** |
| `notebooks/` | Jupyter notebooks for exploration and experimentation |
| `src/` | **Core Python package - all reusable code** |
| `backend/` | FastAPI application |
| `frontend/` | React TypeScript application |
| `models/` | Trained ML models and artifacts |
| `visualizations/` | Generated charts, graphs, heatmaps |
| `tests/` | Integration and E2E tests |
| `scripts/` | One-off scripts, utilities, startup scripts |
| `docker/` | Docker configurations |

### **`src/` - Core Python Package**
This is your **main codebase** - installable as a Python package.

```python
# Install your package in development mode
pip install -e .
```

**Sub-folders:**
- `core/` - Constants, exceptions, logging config
- `data/` - Data loading, cleaning, validation, transformation
- `features/` - Feature engineering, selection, encoding
- `models/` - ML model classes, training, prediction, evaluation
- `analytics/` - Anomaly detection, trend analysis, insights
- `visualization/` - Chart generation utilities
- `utils/` - Shared utility functions

### **`backend/` - FastAPI Application**
Professional API structure following FastAPI best practices.

**Key principles:**
- **Separation of concerns** (routes, services, schemas)
- **Version control** (`/api/v1/`)
- **Testability** (dependency injection)
- **Scalability** (service layer pattern)

### **`frontend/` - React Application**
Standard React + TypeScript structure.

**Features:**
- Component-based architecture
- Service layer for API calls
- Custom hooks for logic reuse
- TypeScript for type safety

### **`data/` - Data Management**
```
data/
├── raw/          # NEVER modify - immutable source data
├── interim/      # Intermediate transformations
├── processed/    # Final datasets ready for ML
├── external/     # External reference data
└── outputs/      # Generated predictions, exports
```

**Add to `.gitignore`:**
```gitignore
data/raw/*
data/interim/*
data/processed/*
!data/*/README.md
```

### **`models/` - Model Registry**
Organized by model type with metadata.

```
models/
├── demand/
│   ├── uidai_demand_model.pkl
│   └── metadata.json        # Training date, metrics, features
└── registry.yaml            # Centralized model tracking
```

### **`scripts/` - Utility Scripts**
One-off scripts organized by purpose.

**Guidelines:**
- **`setup/`** - Environment setup, installation
- **`data/`** - Data processing scripts
- **`training/`** - Model training scripts
- **`deployment/`** - Startup scripts, deployment
- **`debugging/`** - Debug utilities
- **`utilities/`** - Miscellaneous tools

### **`docs/` - Documentation**
All documentation in one place.

```
docs/
├── architecture/      # System design, data flow
├── user-guides/       # How-to guides for users
├── technical/         # Technical specifications
└── reports/           # Analysis reports, status updates
```

### **`tests/` - Testing**
Organized by test type.

```
tests/
├── integration/       # API integration tests
├── e2e/              # End-to-end workflow tests
└── fixtures/         # Test data and mocks
```

---

## 🔄 Migration Plan

### **Step 1: Create New Structure**
```bash
# Run the migration script
python scripts/utilities/migrate_structure.py
```

### **Step 2: Move Files**

| Current Location | New Location |
|------------------|--------------|
| `01_data/*` | `data/raw/*` and `data/processed/*` |
| `02_notebooks/*` | `notebooks/01-exploratory/*` |
| `03_models/*.pkl` | `models/<model_type>/*.pkl` |
| `04_visuals/*` | `visualizations/*` |
| `05_reports/*` | `docs/reports/*` |
| `*.md` (reports) | `docs/reports/*` |
| `*.md` (guides) | `docs/user-guides/*` |
| `debug_*.py` | `scripts/debugging/*` |
| `process_*.py` | `scripts/data/*` |
| `extract_*.py` | `scripts/data/*` |
| `generate_visuals.py` | `scripts/utilities/*` |
| `test_integration.py` | `tests/integration/*` |
| `start_*.bat` | `scripts/deployment/*` |
| `backend/` | `backend/` (restructure internally) |
| `frontend/` | `frontend/` (no change) |

### **Step 3: Update Imports**
After moving files to `src/`, update imports:

```python
# Old
from model_service import model_service

# New
from src.models.predictors import ModelPredictor
from src.analytics.dashboard_aggregator import DashboardService
```

### **Step 4: Create Package Files**
Add `__init__.py` to make `src/` a package:
```python
# src/__init__.py
__version__ = "1.0.0"
```

### **Step 5: Update Startup Scripts**
Update paths in:
- `start_backend.bat`
- `start_frontend.bat`
- `start_servers.ps1`

---

## 🎯 Best Practices

### **1. Environment Management**
```bash
# Create virtual environment
python -m venv .venv

# Activate
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Install
pip install -r requirements.txt
```

### **2. Configuration Management**
Use environment-specific configs:
```yaml
# config/development.yaml
database:
  host: localhost
  port: 5432

# config/production.yaml
database:
  host: prod-db.example.com
  port: 5432
```

### **3. Secrets Management**
```bash
# .env.example (commit this)
DATABASE_URL=postgresql://localhost/uidai
API_KEY=your_api_key_here

# .env (DO NOT COMMIT)
DATABASE_URL=postgresql://prod-server/uidai
API_KEY=actual_secret_key
```

### **4. Logging**
```python
# Use structured logging
import logging
logger = logging.getLogger(__name__)

logger.info("Processing data", extra={"records": 1000})
```

### **5. Testing**
```bash
# Run tests
pytest tests/

# With coverage
pytest --cov=src tests/
```

---

## 📦 Package Installation

Create `setup.py`:
```python
from setuptools import setup, find_packages

setup(
    name="uidai-analytics",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "pandas>=1.5.0",
        "numpy>=1.23.0",
        "scikit-learn>=1.2.0",
        "fastapi>=0.100.0",
        "uvicorn>=0.23.0",
    ],
)
```

Install in development mode:
```bash
pip install -e .
```

---

## 🚀 Quick Start Commands

Create a `Makefile`:
```makefile
.PHONY: install test lint run-backend run-frontend

install:
	pip install -r requirements.txt
	pip install -e .

test:
	pytest tests/ -v

lint:
	flake8 src/ backend/
	black src/ backend/ --check

run-backend:
	cd backend && uvicorn app.main:app --reload

run-frontend:
	cd frontend && npm run dev

docker-up:
	docker-compose up -d

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
```

Usage:
```bash
make install
make test
make run-backend
```

---

## 📊 Benefits of This Structure

### ✅ **Scalability**
- Easy to add new models, features, or services
- Clear separation of concerns

### ✅ **Maintainability**
- Predictable file locations
- Easier onboarding for new team members

### ✅ **Testability**
- Clear separation of logic and infrastructure
- Easy to mock dependencies

### ✅ **Collaboration**
- Standard structure familiar to developers
- Clear ownership boundaries

### ✅ **CI/CD Ready**
- Docker support
- GitHub Actions workflows
- Automated testing

### ✅ **Production Ready**
- Environment-specific configurations
- Proper logging and monitoring
- Security best practices

---

## 🔧 Next Steps

1. **Review** this structure with your team
2. **Run** the migration script (to be created)
3. **Update** documentation
4. **Test** that everything works
5. **Commit** changes to version control

---

## 📚 References

This structure follows best practices from:
- [Cookiecutter Data Science](https://drivendata.github.io/cookiecutter-data-science/)
- [FastAPI Best Practices](https://github.com/zhanymkanov/fastapi-best-practices)
- [React TypeScript Best Practices](https://react-typescript-cheatsheet.netlify.app/)
- [Google's Python Style Guide](https://google.github.io/styleguide/pyguide.html)

---

**Version:** 1.0  
**Last Updated:** January 17, 2026  
**Author:** Senior Software Architect
