"""
UIDAI Analytics - Project Structure Migration Script
Migrates from numbered folders to industry-standard structure

Author: Senior Software Architect
Date: January 17, 2026
"""

import os
import shutil
from pathlib import Path
from typing import Dict, List
import json

# Color output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header(text: str):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'=' * 70}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'=' * 70}{Colors.ENDC}\n")

def print_success(text: str):
    print(f"{Colors.OKGREEN}✓ {text}{Colors.ENDC}")

def print_info(text: str):
    print(f"{Colors.OKCYAN}ℹ {text}{Colors.ENDC}")

def print_warning(text: str):
    print(f"{Colors.WARNING}⚠ {text}{Colors.ENDC}")

def print_error(text: str):
    print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")


class ProjectMigrator:
    def __init__(self, root_path: str, dry_run: bool = True):
        self.root = Path(root_path)
        self.dry_run = dry_run
        self.migration_log = []
        
    def create_directory_structure(self):
        """Create new directory structure"""
        print_header("Creating New Directory Structure")
        
        directories = [
            # Config
            "config",
            
            # Data
            "data/raw/biometric",
            "data/raw/demographic",
            "data/raw/enrollment",
            "data/interim",
            "data/processed",
            "data/external",
            "data/outputs/predictions",
            
            # Docs
            "docs/architecture",
            "docs/user-guides",
            "docs/technical",
            "docs/reports",
            
            # Notebooks
            "notebooks/01-exploratory",
            "notebooks/02-experiments",
            "notebooks/03-reports",
            
            # Source code
            "src/core",
            "src/data",
            "src/features",
            "src/models",
            "src/analytics",
            "src/visualization",
            "src/utils",
            
            # Backend (reorganize existing)
            "backend/app/api/v1",
            "backend/app/core",
            "backend/app/schemas",
            "backend/app/services",
            "backend/app/utils",
            "backend/tests/test_api",
            "backend/tests/test_services",
            
            # Models
            "models/demand",
            "models/biometric",
            "models/demographic",
            "models/enrollment",
            
            # Visualizations
            "visualizations/anomalies",
            "visualizations/heatmaps",
            "visualizations/lifecycle",
            "visualizations/trends",
            
            # Tests
            "tests/integration",
            "tests/e2e",
            "tests/fixtures",
            
            # Scripts
            "scripts/setup",
            "scripts/data",
            "scripts/training",
            "scripts/deployment",
            "scripts/debugging",
            "scripts/utilities",
            
            # Docker
            "docker",
        ]
        
        for directory in directories:
            dir_path = self.root / directory
            if not self.dry_run:
                dir_path.mkdir(parents=True, exist_ok=True)
                # Create __init__.py for Python packages
                if directory.startswith("src/") or directory.startswith("backend/app"):
                    init_file = dir_path / "__init__.py"
                    if not init_file.exists():
                        init_file.write_text('"""Package initialization."""\n')
            print_success(f"Created: {directory}")
        
        self.migration_log.append(("CREATE_DIRS", len(directories)))
    
    def get_migration_map(self) -> Dict[str, str]:
        """Define file migration mapping"""
        return {
            # Data files
            "01_data/raw": "data/raw",
            "01_data/processed": "data/processed",
            
            # Notebooks
            "02_notebooks/Biometric_Analysis_1.ipynb": "notebooks/01-exploratory/biometric_analysis.ipynb",
            "02_notebooks/Demographic_Analysis_EDA.ipynb": "notebooks/01-exploratory/demographic_eda.ipynb",
            "02_notebooks/enrollment_Analysis.ipynb": "notebooks/01-exploratory/enrollment_analysis.ipynb",
            "02_notebooks/feature_importance.csv": "notebooks/02-experiments/feature_importance.csv",
            
            # Models
            "03_models/uidai_demand_model.pkl": "models/demand/uidai_demand_model.pkl",
            "03_models/uidai_enrollment_model.pkl": "models/enrollment/uidai_enrollment_model.pkl",
            "03_models/uidai_biometric_model.pkl": "models/biometric/uidai_biometric_model.pkl",
            "03_models/uidai_biometric_model_info.pkl": "models/biometric/uidai_biometric_model_info.pkl",
            "03_models/uidai_demographic_model.pkl": "models/demographic/uidai_demographic_model.pkl",
            "03_models/uidai_demographic_model_info.pkl": "models/demographic/uidai_demographic_model_info.pkl",
            "03_models/biometric_feature_importance.csv": "models/biometric/feature_importance.csv",
            
            # Training scripts
            "03_models/train_demand_model.py": "scripts/training/train_demand_model.py",
            "03_models/train_biometric_model.py": "scripts/training/train_biometric_model.py",
            "03_models/train_demographic_model.py": "scripts/training/train_demographic_model.py",
            "03_models/train_enrollment_model.py": "scripts/training/train_enrollment_model.py",
            "03_models/train_model.py": "scripts/training/train_model.py",
            
            # Visualizations
            "04_visuals/anomalies": "visualizations/anomalies",
            "04_visuals/heatmaps": "visualizations/heatmaps",
            "04_visuals/lifecycle": "visualizations/lifecycle",
            "04_visuals/trends": "visualizations/trends",
            
            # Documentation - Reports
            "INTEGRATION_STATUS_REPORT.md": "docs/reports/INTEGRATION_STATUS_REPORT.md",
            "SYSTEM_STATUS_REPORT.md": "docs/reports/SYSTEM_STATUS_REPORT.md",
            "MODEL_ANALYSIS_AND_RECOMMENDATIONS.md": "docs/technical/MODEL_ANALYSIS_AND_RECOMMENDATIONS.md",
            "BIOMETRIC_MODEL_UPGRADE_REPORT.md": "docs/technical/BIOMETRIC_MODEL_UPGRADE_REPORT.md",
            "DEMOGRAPHIC_PREDICTION_SYSTEM.md": "docs/technical/DEMOGRAPHIC_PREDICTION_SYSTEM.md",
            "FEATURES_SUMMARY.md": "docs/technical/FEATURES_SUMMARY.md",
            
            # Documentation - User Guides
            "EXPORT_QUICK_GUIDE.md": "docs/user-guides/EXPORT_QUICK_GUIDE.md",
            "VISUALIZATION_QUICK_GUIDE.md": "docs/user-guides/VISUALIZATION_QUICK_GUIDE.md",
            "INTEGRATION_SUMMARY.md": "docs/user-guides/INTEGRATION_SUMMARY.md",
            "SOLUTION_BACKEND_RUNNING.md": "docs/user-guides/SOLUTION_BACKEND_RUNNING.md",
            "EXPORT_FEATURE.md": "docs/user-guides/EXPORT_FEATURE.md",
            "VISUALIZATION_SYSTEM.md": "docs/user-guides/VISUALIZATION_SYSTEM.md",
            "INTEGRATION_DIAGRAM.txt": "docs/architecture/INTEGRATION_DIAGRAM.txt",
            
            # Scripts - Data Processing
            "process_demographic_data.py": "scripts/data/process_demographic_data.py",
            "extract_delhi_centers.py": "scripts/data/extract_delhi_centers.py",
            "extract_delhi_centers_v2.py": "scripts/data/extract_delhi_centers_v2.py",
            
            # Scripts - Debugging
            "debug_anomalies.py": "scripts/debugging/debug_anomalies.py",
            "debug_dashboard.py": "scripts/debugging/debug_dashboard.py",
            "debug_locations.py": "scripts/debugging/debug_locations.py",
            
            # Scripts - Utilities
            "generate_visuals.py": "scripts/utilities/generate_visuals.py",
            "test_integration.py": "tests/integration/test_integration.py",
            "VERIFY_INTEGRATION.bat": "scripts/utilities/verify_integration.bat",
            
            # Scripts - Deployment
            "start_backend.bat": "scripts/deployment/start_backend.bat",
            "start_frontend.bat": "scripts/deployment/start_frontend.bat",
            "start_servers.ps1": "scripts/deployment/start_servers.ps1",
            "run_stack.bat": "scripts/deployment/run_stack.bat",
            "test_system.ps1": "scripts/deployment/test_system.ps1",
            
            # Outputs
            "locations_output.txt": "data/outputs/locations_output.txt",
        }
    
    def migrate_files(self):
        """Migrate files to new locations"""
        print_header("Migrating Files")
        
        migration_map = self.get_migration_map()
        migrated = 0
        skipped = 0
        errors = 0
        
        for source, destination in migration_map.items():
            source_path = self.root / source
            dest_path = self.root / destination
            
            if source_path.exists():
                try:
                    if not self.dry_run:
                        # Create parent directory
                        dest_path.parent.mkdir(parents=True, exist_ok=True)
                        
                        # Copy file or directory
                        if source_path.is_dir():
                            if not dest_path.exists():
                                shutil.copytree(source_path, dest_path)
                            else:
                                print_warning(f"Destination exists: {destination}")
                        else:
                            shutil.copy2(source_path, dest_path)
                    
                    print_success(f"{source} → {destination}")
                    migrated += 1
                    self.migration_log.append(("MIGRATE", source, destination))
                except Exception as e:
                    print_error(f"Failed to migrate {source}: {e}")
                    errors += 1
                    self.migration_log.append(("ERROR", source, str(e)))
            else:
                print_warning(f"Source not found: {source}")
                skipped += 1
        
        print_info(f"\nMigration Summary: {migrated} migrated, {skipped} skipped, {errors} errors")
    
    def reorganize_backend(self):
        """Reorganize backend structure"""
        print_header("Reorganizing Backend")
        
        backend_migrations = {
            "backend/main.py": "backend/app/main.py",
            "backend/model_service.py": "backend/app/services/model_service.py",
            "backend/dashboard_service.py": "backend/app/services/dashboard_service.py",
            "backend/schemas.py": "backend/app/schemas/predictions.py",
            "backend/test_api.py": "backend/tests/test_api/test_endpoints.py",
            "backend/test_api_v2.py": "backend/tests/test_api/test_endpoints_v2.py",
        }
        
        for source, destination in backend_migrations.items():
            source_path = self.root / source
            dest_path = self.root / destination
            
            if source_path.exists():
                if not self.dry_run:
                    dest_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(source_path, dest_path)
                print_success(f"{source} → {destination}")
                self.migration_log.append(("BACKEND_REORG", source, destination))
    
    def create_package_files(self):
        """Create necessary package files"""
        print_header("Creating Package Files")
        
        files_to_create = {
            "setup.py": self._get_setup_py_content(),
            "pyproject.toml": self._get_pyproject_toml_content(),
            "Makefile": self._get_makefile_content(),
            ".env.example": self._get_env_example_content(),
            "src/__init__.py": '"""UIDAI Analytics - Core Package"""\n__version__ = "1.0.0"\n',
            "models/registry.yaml": self._get_model_registry_content(),
            "START_HERE.md": self._get_start_here_content(),
        }
        
        for filepath, content in files_to_create.items():
            file_path = self.root / filepath
            if not self.dry_run:
                file_path.parent.mkdir(parents=True, exist_ok=True)
                file_path.write_text(content)
            print_success(f"Created: {filepath}")
    
    def _get_setup_py_content(self) -> str:
        return '''"""
UIDAI Analytics - Setup Configuration
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="uidai-analytics",
    version="1.0.0",
    author="UIDAI Analytics Team",
    description="AI-powered Aadhaar Analytics & Forecasting Platform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "pandas>=1.5.0",
        "numpy>=1.23.0",
        "scikit-learn>=1.2.0",
        "xgboost>=1.7.0",
        "joblib>=1.2.0",
        "fastapi>=0.100.0",
        "uvicorn[standard]>=0.23.0",
        "pydantic>=2.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
'''
    
    def _get_pyproject_toml_content(self) -> str:
        return '''[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "uidai-analytics"
version = "1.0.0"
description = "AI-powered Aadhaar Analytics & Forecasting Platform"
readme = "README.md"
requires-python = ">=3.9"
license = {text = "MIT"}

[tool.black]
line-length = 100
target-version = ['py39']

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"
python_classes = "Test*"
python_functions = "test_*"

[tool.mypy]
python_version = "3.9"
warn_return_any = true
warn_unused_configs = true
'''
    
    def _get_makefile_content(self) -> str:
        return '''.PHONY: install test lint format run-backend run-frontend docker-up clean

install:
\tpip install -r requirements.txt
\tpip install -e .

install-dev:
\tpip install -r requirements-dev.txt
\tpip install -e .[dev]

test:
\tpytest tests/ -v --cov=src

lint:
\tflake8 src/ backend/
\tmypy src/

format:
\tblack src/ backend/ tests/

run-backend:
\tcd backend && uvicorn app.main:app --reload --port 8002

run-frontend:
\tcd frontend && npm run dev

docker-up:
\tdocker-compose -f docker/docker-compose.yml up -d

docker-down:
\tdocker-compose -f docker/docker-compose.yml down

clean:
\tfind . -type d -name __pycache__ -exec rm -rf {} +
\tfind . -type f -name "*.pyc" -delete
\tfind . -type d -name "*.egg-info" -exec rm -rf {} +
\trm -rf .pytest_cache .coverage htmlcov/

help:
\t@echo "Available commands:"
\t@echo "  make install       - Install dependencies"
\t@echo "  make test          - Run tests"
\t@echo "  make lint          - Run linters"
\t@echo "  make format        - Format code"
\t@echo "  make run-backend   - Start backend server"
\t@echo "  make run-frontend  - Start frontend dev server"
\t@echo "  make docker-up     - Start Docker containers"
\t@echo "  make clean         - Remove cache files"
'''
    
    def _get_env_example_content(self) -> str:
        return '''# Environment Configuration

# Application
APP_NAME=UIDAI Analytics
APP_VERSION=1.0.0
ENVIRONMENT=development

# API
API_HOST=0.0.0.0
API_PORT=8002
API_RELOAD=true

# Database (if using)
# DATABASE_URL=postgresql://user:password@localhost:5432/uidai

# Frontend
FRONTEND_URL=http://localhost:5173

# Security
# SECRET_KEY=your-secret-key-here
# API_KEY=your-api-key-here

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json

# Models
MODEL_PATH=models/
'''
    
    def _get_model_registry_content(self) -> str:
        return '''# ML Model Registry

models:
  demand:
    name: uidai_demand_model
    version: 1.0.0
    type: regression
    framework: sklearn
    status: production
    trained_date: "2026-01-17"
    
  biometric:
    name: uidai_biometric_model
    version: 1.0.0
    type: regression
    framework: xgboost
    status: production
    trained_date: "2026-01-17"
    
  demographic:
    name: uidai_demographic_model
    version: 1.0.0
    type: regression
    framework: sklearn
    status: production
    trained_date: "2026-01-17"
    
  enrollment:
    name: uidai_enrollment_model
    version: 1.0.0
    type: regression
    framework: sklearn
    status: production
    trained_date: "2026-01-17"
'''
    
    def _get_start_here_content(self) -> str:
        return '''# 🚀 UIDAI Analytics - Quick Start Guide

## Prerequisites
- Python 3.9+
- Node.js 16+
- Git

## Setup

### 1. Clone Repository
```bash
git clone <your-repo-url>
cd uidai-analytics
```

### 2. Install Dependencies
```bash
# Python
make install

# Frontend
cd frontend
npm install
```

### 3. Start Services
```bash
# Terminal 1 - Backend
make run-backend

# Terminal 2 - Frontend
make run-frontend
```

### 4. Access Application
- Frontend: http://localhost:5173
- Backend API: http://localhost:8002
- API Docs: http://localhost:8002/docs

## Project Structure
See `PROJECT_RESTRUCTURE_PLAN.md` for detailed folder structure.

## Documentation
- Architecture: `docs/architecture/`
- User Guides: `docs/user-guides/`
- Technical Docs: `docs/technical/`

## Testing
```bash
make test
```

## Support
For issues, see `docs/reports/SYSTEM_STATUS_REPORT.md`
'''
    
    def save_migration_log(self):
        """Save migration log"""
        log_path = self.root / "migration_log.json"
        if not self.dry_run:
            with open(log_path, 'w') as f:
                json.dump(self.migration_log, f, indent=2)
        print_success(f"Migration log saved: {log_path}")
    
    def run(self):
        """Run complete migration"""
        print_header("UIDAI Analytics - Project Structure Migration")
        
        if self.dry_run:
            print_warning("DRY RUN MODE - No files will be modified")
            print_info("Run with --execute flag to perform actual migration\n")
        
        self.create_directory_structure()
        self.migrate_files()
        self.reorganize_backend()
        self.create_package_files()
        self.save_migration_log()
        
        print_header("Migration Complete!")
        
        if self.dry_run:
            print_warning("This was a DRY RUN. To execute migration, run:")
            print_info("python scripts/utilities/migrate_structure.py --execute")
        else:
            print_success("Project structure has been migrated successfully!")
            print_info("\nNext steps:")
            print_info("1. Review migrated files")
            print_info("2. Update import statements")
            print_info("3. Test backend and frontend")
            print_info("4. Commit changes to Git")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Migrate UIDAI project structure")
    parser.add_argument("--execute", action="store_true", help="Execute migration (default is dry run)")
    parser.add_argument("--root", default=".", help="Project root directory")
    
    args = parser.parse_args()
    
    migrator = ProjectMigrator(
        root_path=args.root,
        dry_run=not args.execute
    )
    
    migrator.run()
