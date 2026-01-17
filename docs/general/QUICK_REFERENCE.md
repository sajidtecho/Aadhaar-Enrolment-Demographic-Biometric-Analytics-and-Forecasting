# 🎯 Quick Reference - Project Restructure

## Run Migration

### Dry Run (Preview Only)
```bash
python migrate_structure.py
```

### Execute Migration
```bash
python migrate_structure.py --execute
```

---

## New Structure Quick Reference

```
📁 config/          → Configuration files
📁 data/            → All data (gitignored)
  ├── raw/          → Original data
  ├── processed/    → Clean data
  └── outputs/      → Results
📁 docs/            → ALL documentation
  ├── architecture/ → System design
  ├── user-guides/  → How-to guides
  ├── technical/    → Specs & analysis
  └── reports/      → Status reports
📁 notebooks/       → Jupyter notebooks
📁 src/             → **PYTHON PACKAGE** (pip install -e .)
  ├── core/         → Constants, exceptions
  ├── data/         → Data pipeline
  ├── features/     → Feature engineering
  ├── models/       → ML models
  ├── analytics/    → Analysis logic
  └── utils/        → Utilities
📁 backend/         → FastAPI app
  └── app/
      ├── api/v1/   → API routes
      ├── services/ → Business logic
      └── schemas/  → Pydantic models
📁 frontend/        → React app (unchanged)
📁 models/          → Trained .pkl files
📁 visualizations/  → Generated charts
📁 tests/           → All tests
📁 scripts/         → Utility scripts
  ├── data/         → Data processing
  ├── training/     → Model training
  ├── deployment/   → Start scripts
  └── utilities/    → Tools
```

---

## Common Commands (After Migration)

### Installation
```bash
make install          # Install dependencies
make install-dev      # Install dev dependencies
```

### Development
```bash
make run-backend      # Start backend (port 8002)
make run-frontend     # Start frontend (port 5173)
```

### Testing
```bash
make test             # Run all tests
make lint             # Check code quality
make format           # Format code
```

### Docker
```bash
make docker-up        # Start containers
make docker-down      # Stop containers
```

### Cleanup
```bash
make clean            # Remove cache files
```

---

## File Location Guide

| Looking for... | New location |
|----------------|--------------|
| Training scripts | `scripts/training/` |
| Data processing | `scripts/data/` |
| Debug scripts | `scripts/debugging/` |
| Start scripts | `scripts/deployment/` |
| ML models (.pkl) | `models/<model_type>/` |
| Documentation | `docs/<category>/` |
| Notebooks | `notebooks/01-exploratory/` |
| Tests | `tests/integration/` |
| Generated charts | `visualizations/` |
| Config files | `config/` |

---

## Import Changes

### Before
```python
from model_service import model_service
import dashboard_service
```

### After
```python
from src.models.predictors import ModelPredictor
from src.analytics.dashboard_aggregator import DashboardService
```

---

## Backend Changes

### Before
```
backend/
├── main.py
├── model_service.py
└── schemas.py
```

### After
```
backend/app/
├── main.py
├── api/v1/
│   ├── predictions.py
│   └── dashboard.py
├── services/
│   ├── model_service.py
│   └── dashboard_service.py
└── schemas/
    └── predictions.py
```

---

## Key Benefits

✅ **Installable Package**
```bash
pip install -e .
# Now use: from src.models import ...
```

✅ **Clean Root**
```
Only 8 files instead of 30+
```

✅ **Make Commands**
```bash
make install
make test
make run-backend
```

✅ **Docker Support**
```bash
docker-compose up
```

✅ **CI/CD Ready**
```
.github/workflows/ci.yml
```

---

## Migration Checklist

- [ ] Review `PROJECT_RESTRUCTURE_PLAN.md`
- [ ] Run dry-run: `python migrate_structure.py`
- [ ] Execute: `python migrate_structure.py --execute`
- [ ] Update import statements
- [ ] Update path references
- [ ] Test backend: `make run-backend`
- [ ] Test frontend: `make run-frontend`
- [ ] Run tests: `make test`
- [ ] Commit changes to Git
- [ ] Update team documentation

---

## Rollback Plan

If something goes wrong:
1. Migration creates copies, not moves
2. Check `migration_log.json`
3. Original files still in place
4. Use Git to revert if needed

---

## Support Files

- **Full Plan:** `PROJECT_RESTRUCTURE_PLAN.md`
- **Comparison:** `BEFORE_AFTER_COMPARISON.md`
- **Migration Script:** `migrate_structure.py`
- **Migration Log:** `migration_log.json` (after execution)

---

**Quick Start:** `python migrate_structure.py`  
**Questions:** Check `docs/user-guides/`  
**Issues:** See `docs/reports/SYSTEM_STATUS_REPORT.md`
