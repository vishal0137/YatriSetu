# YatriSetu Data Directory

This directory contains all data files used by the YatriSetu application.

## Folder Structure

```
data/
├── raw/              # Raw input files (PDFs, CSVs)
│   ├── .gitkeep
│   └── *.pdf        # DTC PDF files (gitignored)
└── processed/        # Processed, database-ready CSV files
    ├── .gitkeep
    ├── routes_final.csv
    ├── stops_final.csv
    ├── fares_final.csv
    └── README.md
```

## Raw Data (`raw/`)

### Purpose
Stores original, unprocessed data files from DTC or other sources.

### File Types
- PDF files (DTC route schedules, bus information)
- CSV files (raw data exports)
- Excel files (if applicable)

### Git Handling
- Raw PDF and CSV files are gitignored
- Only `.gitkeep` is tracked
- Prevents large files in repository

### Usage
```bash
# Place new DTC PDF here
cp new_dtc_routes.pdf data/raw/

# Process the file
python scripts/process_dtc_data.py data/raw/new_dtc_routes.pdf data/processed
```

## Processed Data (`processed/`)

### Purpose
Stores cleaned, validated, database-ready CSV files.

### File Types
- `routes_final.csv` - Route information
- `stops_final.csv` - Stop sequences
- `fares_final.csv` - Fare structure
- `buses_final.csv` - Bus fleet data (if applicable)

### Git Handling
- Processed CSV files are tracked in git
- These are production-ready data
- Small file sizes suitable for version control

### Usage
```bash
# Import to database via admin panel
# Navigate to: http://localhost:5000/admin/data-import
# Upload files from data/processed/

# Or use direct PostgreSQL import
psql -U postgres -d yatrisetu_db -f data/processed/import_script.sql
```

## Data Processing Workflow

### Step 1: Obtain Raw Data
```bash
# Download DTC PDF from official source
# Save to data/raw/
```

### Step 2: Process Data
```bash
# Run processing script
python scripts/process_dtc_data.py data/raw/input.pdf data/processed

# Output:
# - data/processed/routes_final.csv
# - data/processed/stops_final.csv
# - data/processed/fares_final.csv
```

### Step 3: Validate Data
```bash
# Review processed files
# Check for:
# - Correct column names
# - Valid data types
# - No missing required fields
# - Proper formatting
```

### Step 4: Import to Database
```bash
# Option 1: Admin Panel
# http://localhost:5000/admin/data-import

# Option 2: Direct SQL import
# See data/processed/README.md for SQL commands
```

## Data Quality Standards

### Raw Data
- Original, unmodified files
- Preserve source formatting
- Include metadata (date, source, version)

### Processed Data
- Schema-compliant
- Validated and cleaned
- No duplicates
- Consistent formatting
- Database-ready

## File Naming Conventions

### Raw Files
```
<source>_<type>_<date>_<version>.pdf
Example: dtc_routes_nov_2025_1_0.pdf
```

### Processed Files
```
<category>_final.csv
Example: routes_final.csv
```

## Data Sources

| Source | Type | Update Frequency |
|--------|------|------------------|
| DTC Official | PDF | Monthly |
| Manual Entry | CSV | As needed |
| API Import | JSON | Real-time |

## Data Backup

### Backup Strategy
- Raw files: Keep original sources
- Processed files: Version controlled in git
- Database: Regular PostgreSQL backups

### Backup Schedule
- Raw data: Backup before processing
- Processed data: Committed to git
- Database: Daily automated backups

## Troubleshooting

### Issue: Processing Fails
**Solution:**
- Check PDF file integrity
- Verify file format
- Review error logs in `logs/`

### Issue: Import Fails
**Solution:**
- Validate CSV structure
- Check for duplicates
- Verify database connection

### Issue: Data Mismatch
**Solution:**
- Re-process from raw data
- Compare with source
- Check validation rules

## Security Considerations

- Raw data may contain sensitive information
- Processed data is sanitized
- No personal information in git
- Access control on data folders

## Related Documentation

- [Data Import Feature](../docs/DATA_IMPORT_ENHANCED.md)
- [Duplicate Detection Guide](../docs/DUPLICATE_DETECTION_GUIDE.md)
- [Processed Data README](processed/README.md)

---

**Last Updated:** February 25, 2026  
**Data Version:** 1.0
