# Data Import Feature - YatriSetu

## Overview

The Data Import feature allows administrators to import buses, routes, fares, and stops data from CSV or PDF files into the YatriSetu database. The system automatically detects data categories, validates data structure, and ensures data integrity before insertion.

## Features

| Feature | Description |
|---------|-------------|
| File Upload | Drag-and-drop or browse to upload CSV/PDF files |
| Automatic Detection | Automatically detects data category (buses, routes, fares, stops) |
| Structure Analysis | Analyzes file structure and displays column information |
| Data Validation | Validates data types, required fields, and categorical values |
| Preview | Shows sample data before import |
| Error Reporting | Detailed validation error messages |
| Database Import | Imports validated data into database |
| Export | Exports extracted data to CSV format |

## Supported File Formats

| Format | Extension | Max Size | Notes |
|--------|-----------|----------|-------|
| CSV | .csv | 10MB | Comma-separated values |
| PDF | .pdf | 10MB | Requires table extraction |

## Data Categories

### 1. Buses

| Field | Type | Required | Valid Values |
|-------|------|----------|--------------|
| bus_number | String | Yes | Unique identifier |
| bus_type | String | No | AC, Non-AC, Electric, CNG, Diesel |
| capacity | Integer | No | 1-200 |
| status | String | No | Active, Inactive, Maintenance, Retired |
| manufacturer | String | No | Any |
| model | String | No | Any |
| year | Integer | No | Valid year |

**Example CSV:**
```csv
bus_number,bus_type,capacity,status,manufacturer,model,year
DL-1234,AC,50,Active,Tata,Starbus,2023
DL-5678,Non-AC,60,Active,Ashok Leyland,Viking,2022
```

### 2. Routes

| Field | Type | Required | Valid Values |
|-------|------|----------|--------------|
| route_number | String | Yes | Unique identifier |
| route_name | String | No | Any |
| start_location | String | Yes | Location name |
| end_location | String | Yes | Location name |
| distance | Float | No | Positive number (km) |
| duration | Integer | No | Minutes |
| frequency | Integer | No | Buses per hour |

**Example CSV:**
```csv
route_number,route_name,start_location,end_location,distance,duration
101,Central-Airport,Connaught Place,IGI Airport,25.5,45
102,Tech Park Express,Dwarka,Cyber City,18.2,35
```

### 3. Fares

| Field | Type | Required | Valid Values |
|-------|------|----------|--------------|
| route_id | String | Yes | Valid route number |
| passenger_type | String | Yes | General, Student, Senior Citizen, Differently Abled, Child |
| fare_amount | Float | Yes | Non-negative number |
| distance_range | String | No | Distance range |
| effective_date | Date | No | Valid date |

**Example CSV:**
```csv
route_id,passenger_type,fare_amount,distance_range
101,General,50,0-25km
101,Student,25,0-25km
101,Senior Citizen,30,0-25km
```

### 4. Stops

| Field | Type | Required | Valid Values |
|-------|------|----------|--------------|
| stop_name | String | Yes | Location name |
| latitude | Float | No | -90 to 90 |
| longitude | Float | No | -180 to 180 |
| route_id | String | No | Valid route number |
| sequence | Integer | No | Positive number |
| arrival_time | Time | No | HH:MM format |

**Example CSV:**
```csv
stop_name,latitude,longitude,route_id,sequence
Connaught Place,28.6304,77.2177,101,1
Kashmere Gate,28.6692,77.2289,101,2
IGI Airport,28.5562,77.1000,101,3
```

## Usage Guide

### Step 1: Access Data Import

1. Navigate to Admin Panel
2. Click "Data Import" in the sidebar
3. Or go to: `http://localhost:5000/admin/data-import`

### Step 2: Upload File

**Method A: Drag and Drop**
1. Drag CSV or PDF file to upload area
2. File will be automatically uploaded and analyzed

**Method B: Browse**
1. Click "Browse Files" button
2. Select CSV or PDF file
3. Click "Open"

### Step 3: Review Analysis

The system automatically analyzes the file and displays:

| Information | Description |
|-------------|-------------|
| Total Rows | Number of data rows |
| Total Columns | Number of columns |
| Detected Category | Auto-detected data type |
| Confidence | Detection confidence percentage |
| Columns List | All column names |
| Sample Data | First 3 rows preview |

### Step 4: Select Category

1. Review the detected category
2. Confirm or change category from dropdown
3. Options: Buses, Routes, Fares, Stops

### Step 5: Extract Data

1. Click "Extract Data" button
2. System extracts and validates data
3. Review extraction results
4. Check validation warnings if any

### Step 6: Validate (Optional)

1. Click "Validate Data" button
2. System performs comprehensive validation
3. Review validation report
4. Fix errors in source file if needed

### Step 7: Import to Database

1. Review extracted data preview
2. Click "Import to Database" button
3. Confirm import action
4. System inserts data into database
5. Success message displayed

### Step 8: Export (Optional)

1. Click "Export to CSV" button
2. System exports extracted data
3. Download exported file

## Validation Rules

### Buses Validation

| Rule | Description |
|------|-------------|
| Required Fields | bus_number must be present |
| Bus Type | Must be one of: AC, Non-AC, Electric, CNG, Diesel |
| Capacity | Must be integer between 1-200 |
| Status | Must be one of: Active, Inactive, Maintenance, Retired |

### Routes Validation

| Rule | Description |
|------|-------------|
| Required Fields | route_number, start_location, end_location |
| Distance | Must be positive number |
| Duration | Must be positive integer |
| Locations | Cannot be empty |

### Fares Validation

| Rule | Description |
|------|-------------|
| Required Fields | route_id, passenger_type, fare_amount |
| Passenger Type | Must be valid category |
| Fare Amount | Must be non-negative number |
| Route ID | Must reference existing route |

### Stops Validation

| Rule | Description |
|------|-------------|
| Required Fields | stop_name |
| Latitude | Must be between -90 and 90 |
| Longitude | Must be between -180 and 180 |
| Sequence | Must be positive integer |

## Error Handling

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| Missing required field | Required column not found | Add missing column to CSV |
| Invalid data type | Wrong data type in field | Correct data type in CSV |
| Invalid category value | Value not in allowed list | Use valid category value |
| Duplicate entry | Record already exists | Remove duplicate or update |
| File too large | File exceeds 10MB | Split file or compress |
| Invalid file format | Unsupported file type | Use CSV or PDF format |

### Validation Error Format

```
Row 5: Missing bus_number
Row 12: Invalid bus_type 'Hybrid'
Row 23: Capacity must be a number
```

## Installation

### Required Dependencies

Add to `requirements.txt`:

```txt
pandas>=1.5.0
pdfplumber>=0.9.0
PyPDF2>=3.0.0
```

### Install Dependencies

```bash
pip install pandas pdfplumber PyPDF2
```

### Register Blueprint

In `app/__init__.py`:

```python
from app.routes.data_import import data_import_bp

app.register_blueprint(data_import_bp)
```

### Update Sidebar

Add to `app/templates/admin/_sidebar.html`:

```html
<a href="/admin/data-import" class="sidebar-item {% if active_page == 'data_import' %}active{% endif %}">
    <i class="fas fa-file-import"></i>
    <span>Data Import</span>
</a>
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| /admin/data-import | GET | Render data import page |
| /admin/api/data-import/analyze | POST | Analyze uploaded file |
| /admin/api/data-import/extract | POST | Extract data from file |
| /admin/api/data-import/validate | POST | Validate extracted data |
| /admin/api/data-import/import | POST | Import data to database |
| /admin/api/data-import/export | POST | Export data to CSV |

## Technical Architecture

### Components

| Component | File | Purpose |
|-----------|------|---------|
| Data Extractor | app/data_extractor.py | Core extraction logic |
| Route Handler | app/routes/data_import.py | API endpoints |
| Frontend Template | app/templates/admin/data_import.html | User interface |
| JavaScript | app/static/js/data-import.js | Client-side logic |

### Data Flow

```
File Upload
    ↓
File Analysis (detect category, structure)
    ↓
Data Extraction (parse and normalize)
    ↓
Data Validation (check rules)
    ↓
Database Import (insert records)
```

## Best Practices

### For Administrators

| Practice | Recommendation |
|----------|----------------|
| File Preparation | Ensure CSV has proper headers |
| Data Quality | Verify data before upload |
| Backup | Backup database before import |
| Testing | Test with small file first |
| Validation | Always validate before import |

### For Developers

| Practice | Recommendation |
|----------|----------------|
| Error Handling | Implement comprehensive error handling |
| Logging | Log all import operations |
| Transactions | Use database transactions |
| Validation | Add custom validation rules |
| Testing | Write unit tests for extractors |

## Security Considerations

| Aspect | Implementation |
|--------|----------------|
| File Upload | Validate file type and size |
| File Storage | Store in secure directory |
| SQL Injection | Use parameterized queries |
| Access Control | Admin-only access |
| File Cleanup | Delete uploaded files after processing |

## Performance

| Metric | Value |
|--------|-------|
| Max File Size | 10MB |
| Processing Time | ~2-5 seconds for 1000 rows |
| Memory Usage | ~50MB for typical file |
| Concurrent Uploads | Supported |

## Troubleshooting

### Issue: File Upload Fails

**Solution:**
- Check file size (max 10MB)
- Verify file format (CSV or PDF)
- Check server upload directory permissions

### Issue: Category Not Detected

**Solution:**
- Ensure CSV has proper column headers
- Match column names to expected schema
- Manually select category from dropdown

### Issue: Validation Errors

**Solution:**
- Review error messages
- Fix data in source file
- Re-upload corrected file

### Issue: Import Fails

**Solution:**
- Check database connection
- Verify database schema
- Review validation errors
- Check for duplicate entries

## Future Enhancements

| Enhancement | Description |
|-------------|-------------|
| Excel Support | Support .xlsx files |
| Batch Import | Import multiple files at once |
| Scheduled Import | Automatic periodic imports |
| Data Mapping | Custom column mapping interface |
| Duplicate Detection | Advanced duplicate checking |
| Data Transformation | Custom data transformation rules |
| Import History | Track all import operations |
| Rollback | Undo import operations |

## Related Documentation

| Document | Description |
|----------|-------------|
| [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) | System architecture |
| [TESTING_GUIDE.md](TESTING_GUIDE.md) | Testing procedures |
| [USE_CASE_DIAGRAM.md](USE_CASE_DIAGRAM.md) | System use cases |

---

**Status:** Implemented  
**Version:** 1.0  
**Last Updated:** February 2026
