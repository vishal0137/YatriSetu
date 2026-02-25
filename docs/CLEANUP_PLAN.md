# YatriSetu Project Cleanup and Reorganization Plan

## Issues Identified

### 1. Misplaced Files
- `docs/test_models.py` - Should be in tests/
- `docs/TESTING_INSTRUCTIONS.md` - Already exists, duplicate
- `tests/process_dtc_data.py` - Should be in root as CLI tool
- `destination_bus_services_nov_2025_1_0.pdf` - Should be in data/ folder

### 2. Duplicate Files
- `TESTING_INSTRUCTIONS.md` exists in both root and docs/
- Multiple similar documentation files

### 3. Empty/Unnecessary Folders
- `.dist/` - Empty
- `env/` - Should use .env in root
- `__pycache__/` - Should be in .gitignore

### 4. Organizational Issues
- PDF file in root directory
- No dedicated data/ folder for input files
- No logs/ folder for application logs
- Uploads folder not properly organized

## Reorganization Plan

### New Folder Structure
```
YatriSetu_Prototype/
├── app/                    # Application code
│   ├── models/            # Data models
│   ├── routes/            # Flask routes
│   ├── static/            # Static files
│   ├── templates/         # HTML templates
│   └── chatbot_modules/   # Chatbot components
├── database/              # Database scripts and SQL
├── docs/                  # Documentation only
├── ml/                    # Machine learning models
├── tests/                 # All test files
├── data/                  # Input data files (NEW)
│   ├── raw/              # Raw input files
│   └── processed/        # Processed CSV files
├── logs/                  # Application logs (NEW)
├── scripts/               # Utility scripts (NEW)
│   ├── setup.bat
│   ├── start_server.bat
│   └── process_dtc_data.py
├── uploads/               # User uploaded files
│   └── data_imports/
├── .env                   # Environment variables
├── .gitignore            # Git ignore rules
├── config.py             # Configuration
├── requirements.txt      # Dependencies
├── run.py                # Application entry
└── README.md             # Main documentation
```

## Actions to Take

### 1. Create New Folders
- data/raw/
- data/processed/
- logs/
- scripts/

### 2. Move Files
- destination_bus_services_nov_2025_1_0.pdf → data/raw/
- processed_data/* → data/processed/
- bats/* → scripts/
- tests/process_dtc_data.py → scripts/
- docs/test_models.py → DELETE (duplicate)
- docs/TESTING_INSTRUCTIONS.md → DELETE (duplicate)

### 3. Delete Files/Folders
- .dist/ (empty)
- env/ (use .env in root)
- __pycache__/ (regenerated)
- docs/test_models.py
- docs/TESTING_INSTRUCTIONS.md

### 4. Update .gitignore
Add:
- __pycache__/
- *.pyc
- .pytest_cache/
- logs/
- uploads/
- data/raw/*.pdf
- .env

### 5. Fix Import Paths
Update imports in files that reference moved files

### 6. Update Documentation
- Update PROJECT_STRUCTURE.md
- Update README.md with new structure
