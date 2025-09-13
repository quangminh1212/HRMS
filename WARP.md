# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

XLAB HRMS - Modern Human Resource Management System built with Python using multiple UI frameworks (Streamlit, Flet, NiceGUI). The system features a professional Material Design 3 interface with comprehensive HR management capabilities.

## Architecture

### Core Structure
- **Main App**: `app.py` (Modern UI) and `app_optimized.py` (Optimized version)
- **Launcher**: `run.py` - Configurable launcher with port 3000
- **Database**: SQLite with SQLAlchemy ORM (`src/models/`)
- **UI Components**: Modular design system in `src/components/`
- **Features**: Separated feature modules in `src/features/`

### Design System
- Material Design 3 implementation
- XLAB Design tokens (Teal primary: #14B8A6)
- Glassmorphism effects
- Component-based architecture with clean white theme

## Development Commands

### Setup & Run
```bash
# Initial setup
setup.bat                   # Windows setup script
pip install -r requirements.txt  # Manual dependency installation

# Run application
run.bat                     # Windows launcher with menu
python run.py              # Direct Python launcher (port 3000)
python app_optimized.py    # Run optimized version directly

# Alternative launchers
python app.py              # Main modern UI
python app_hrms_simple.py  # Simplified version
python app_minimal.py      # Minimal version
```

### Development Workflow
```bash
# Code quality
make format               # Format code with Black & isort
make lint                # Run code quality checks
make security            # Run security analysis
make quality             # Run all quality checks

# Testing
make test                # Run all tests
make test-cov            # Run tests with coverage
python test_all_features.py  # Test all features
python feature_checklist.py  # Generate feature checklist

# Cleanup & Optimization
python cleanup.py            # Clean project files
python optimize_imports.py   # Optimize imports
python format_code.py        # Format code
```

### Git Workflow
```bash
# Automated commit workflow
git add .
git commit -m "feat: <description>"  # Use conventional commits
git push

# Or use Make
make commit              # Auto quality check & commit
make push               # Commit and push
```

## Key Components

### Authentication
- Default credentials: `admin` / `admin123`
- Session management in `st.session_state`
- Authentication handled in `app.py:authenticate_user()`

### Database Models (`src/models/`)
- `models.py`: Basic models (User, Employee, Department)
- `models_enhanced.py`: Enhanced models with additional features
- Auto-initialization on startup via `init_enhanced_database()`

### Feature Modules (`src/features/`)
- `hr_search.py`: Employee search functionality
- `salary_management.py`: Salary increase management
- `retirement_management.py`: Retirement tracking
- `additional_features.py`: Planning, contracts, rewards, etc.

### UI Components (`src/components/`)
- `design.py`: Design tokens and base CSS
- `components.py`: Reusable UI components (metric cards, hero headers)
- `pages.py`: Additional page components

## Port Configuration
- Default port: **3000** (HRMS Modern)
- Alternative ports used by different versions
- Port configuration in `run.py` and launcher scripts

## Testing Strategy
- Unit tests in `tests/` directory
- Feature testing with `test_all_features.py`
- UI testing with `auto_test_ui_options.py`
- Sample query testing with `test_sample_queries.py`

## Code Standards
- PEP 8 compliance enforced
- Type hints where applicable
- Comprehensive docstrings
- Clean architecture principles
- Error handling with proper logging
- International commit message standards

## Performance Optimization
- Optimized version available (`app_optimized.py`)
- Database query optimization
- Caching strategies implemented
- Component lazy loading

## Deployment Notes
- Windows batch scripts for easy deployment
- Auto keep-alive functionality built-in
- Responsive design for all screen sizes
- Support for multiple UI frameworks

## Common Issues & Solutions

### Port Already in Use
```bash
# Check if port 3000 is occupied
netstat -an | findstr :3000
# Kill the process or use alternative port
```

### Database Initialization
```bash
# Reset database
python -c "from src.models.models_enhanced import init_enhanced_database; init_enhanced_database()"
```

### Module Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

## Development Tips
- Always run `make quality` before committing
- Use the modern UI version (`app.py`) for best user experience
- Test features with `feature_checklist.py` after major changes
- Keep database backups before schema changes
- Follow the established component pattern when adding new features