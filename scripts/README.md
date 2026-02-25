# YatriSetu Scripts

This folder contains utility scripts for managing the YatriSetu application.

## Available Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| setup.bat | Initial project setup | `scripts\setup.bat` |
| start_server.bat | Start development server | `scripts\start_server.bat` |
| start_production.bat | Start production server | `scripts\start_production.bat` |
| quick_start.bat | Quick development start | `scripts\quick_start.bat` |
| restart_server.bat | Restart server | `scripts\restart_server.bat` |
| force_restart.bat | Force restart server | `scripts\force_restart.bat` |
| process_dtc_data.py | Process DTC PDF files | `python scripts\process_dtc_data.py <input> <output>` |

## Script Descriptions

### setup.bat
Performs initial project setup:
- Creates virtual environment
- Installs dependencies
- Sets up database
- Creates necessary folders

### start_server.bat
Starts the development server with:
- Debug mode enabled
- Auto-reload on code changes
- Detailed error messages

### start_production.bat
Starts the production server with:
- Production configuration
- Logging enabled
- Database connection check
- Error handling

### process_dtc_data.py
CLI tool for processing DTC PDF files:
```bash
python scripts/process_dtc_data.py data/raw/input.pdf data/processed
```

Options:
- `--category`: Specify data category (routes, buses, stops, fares)
- `--verbose`: Show detailed processing information

## Usage Examples

### First Time Setup
```bash
# Run setup script
scripts\setup.bat

# Start development server
scripts\start_server.bat
```

### Daily Development
```bash
# Quick start (skips checks)
scripts\quick_start.bat
```

### Production Deployment
```bash
# Start production server
scripts\start_production.bat
```

### Data Processing
```bash
# Process new DTC data
python scripts\process_dtc_data.py data/raw/new_routes.pdf data/processed

# With specific category
python scripts\process_dtc_data.py data/raw/buses.csv data/processed --category buses

# Verbose output
python scripts\process_dtc_data.py data/raw/routes.pdf data/processed --verbose
```

## Troubleshooting

### Script Won't Run
- Ensure you're in the project root directory
- Check file permissions
- Run as administrator if needed

### Virtual Environment Issues
- Delete `venv` folder
- Run `scripts\setup.bat` again

### Database Connection Errors
- Check `.env` file configuration
- Verify PostgreSQL is running
- Check database credentials

## Notes

- All scripts should be run from the project root directory
- Scripts automatically activate the virtual environment
- Logs are stored in `logs/` directory
- Use `Ctrl+C` to stop the server

---

**Last Updated:** February 25, 2026
