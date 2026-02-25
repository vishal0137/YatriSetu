# Enhanced Data Import Feature

## Overview

The enhanced data import feature provides a comprehensive solution for importing bus, route, fare, and stop data with automatic duplicate detection, data preview, and editing capabilities before database insertion.

## Key Features

| Feature | Description |
|---------|-------------|
| Duplicate Detection | Automatically identifies existing records in database |
| Data Preview | View all extracted data before importing |
| Inline Editing | Edit data directly in the preview table |
| Action Selection | Choose insert, update, or skip for each record |
| Validation | Real-time validation with error highlighting |
| Statistics | Live statistics showing insert/update/skip counts |
| Filtering | Filter preview by status (all, insert, duplicate, error) |
| Step-by-Step Wizard | Guided 3-step import process |

## Import Workflow

### Step 1: Upload File

1. Navigate to Admin Dashboard → Data Import
2. Drag and drop or browse for CSV/PDF file
3. Select data category (or use auto-detection)
4. Click "Analyze & Preview Data"

**Supported Formats:**
- CSV files (.csv)
- PDF files (.pdf)
- Maximum file size: 10MB

**Supported Categories:**
- Buses
- Routes
- Fares
- Stops

### Step 2: Preview & Edit Data

The preview screen displays:

| Column | Description |
|--------|-------------|
| # | Row number |
| Action | Dropdown to select insert/update/skip |
| Status | Badge showing New or Duplicate |
| Data Columns | All extracted fields (editable) |

**Statistics Panel:**
- Total Records: Total number of extracted records
- To Insert: Records marked for insertion
- Duplicates: Records that already exist in database
- Errors: Records with validation errors

**Filtering Options:**
- All: Show all records
- To Insert: Show only new records
- Duplicates: Show only duplicate records
- Errors: Show only records with validation errors

**Editing Data:**
1. Click on any data cell to edit
2. Type new value
3. Press Enter or click outside to save
4. Changes are stored in preview

**Changing Actions:**
- Use the Action dropdown to select:
  - Insert: Add as new record
  - Update: Update existing record (for duplicates)
  - Skip: Don't import this record

### Step 3: Import to Database

Review the import summary:
- Records to Insert
- Records to Update
- Records to Skip

**Import Process:**
1. Review statistics
2. Check the confirmation checkbox
3. Click "Execute Import"
4. Wait for completion
5. View results

## Duplicate Detection

### How It Works

The system checks for duplicates based on unique identifiers:

| Category | Duplicate Check Field |
|----------|----------------------|
| Buses | bus_number |
| Routes | route_number |
| Stops | route_id + stop_name + sequence |
| Fares | route_id + passenger_type |

### Duplicate Handling Options

| Action | Behavior |
|--------|----------|
| Skip | Don't import the duplicate record |
| Update | Update the existing record with new data |
| Insert | Force insert (may cause database error) |

### Visual Indicators

- Yellow background: Duplicate record
- Green background: New record to insert
- Red background: Validation error

## Data Validation

### Validation Rules

**Buses:**
- bus_number: Required
- bus_type: Must be valid type (AC, Non-AC, Electric, CNG, Diesel)
- capacity: Must be positive number (1-200)
- status: Must be valid status (Active, Inactive, Maintenance, Retired)

**Routes:**
- route_number: Required
- start_location: Required
- end_location: Required
- distance: Must be positive number

**Fares:**
- route_id: Required
- passenger_type: Must be valid type (General, Student, Senior Citizen, Differently Abled, Child)
- fare_amount: Required, must be non-negative

**Stops:**
- stop_name: Required
- latitude: Must be between -90 and 90
- longitude: Must be between -180 and 180
- sequence: Must be positive integer

### Error Handling

Records with validation errors are:
- Highlighted in red
- Marked with error badge
- Listed in validation report
- Can be edited before import

## API Endpoints

### Preview Data

```http
POST /admin/api/data-import/preview
Content-Type: application/json

{
  "filepath": "path/to/uploaded/file.csv",
  "category": "routes"
}
```

**Response:**
```json
{
  "success": true,
  "preview": [
    {
      "id": 0,
      "data": {...},
      "is_duplicate": false,
      "duplicate_info": null,
      "validation_status": "valid",
      "action": "insert"
    }
  ],
  "total_records": 100,
  "duplicates": {
    "duplicates": [...],
    "total_duplicates": 5
  },
  "validation": {
    "total_errors": 0,
    "total_warnings": 2,
    "errors": [],
    "warnings": []
  }
}
```

### Import to Database

```http
POST /admin/api/data-import/import
Content-Type: application/json

{
  "filepath": "path/to/uploaded/file.csv",
  "category": "routes",
  "preview_data": [...]
}
```

**Response:**
```json
{
  "success": true,
  "message": "Successfully processed 95 records",
  "statistics": {
    "inserted": 90,
    "updated": 5,
    "skipped": 5,
    "errors": 0
  },
  "errors": []
}
```

## Database Operations

### Insert Operation

New records are inserted with:
- Automatic timestamp generation
- Default values for optional fields
- Foreign key validation
- Transaction rollback on error

### Update Operation

Existing records are updated with:
- Preservation of primary key
- Selective field updates
- Timestamp updates
- Audit trail (if enabled)

### Skip Operation

Records marked as skip are:
- Not inserted or updated
- Counted in statistics
- Logged for reference

## Best Practices

### Before Import

1. Review file format and structure
2. Ensure data quality
3. Check for required fields
4. Validate data types
5. Remove unnecessary columns

### During Preview

1. Review all duplicate records
2. Decide on action for each duplicate
3. Edit incorrect data
4. Verify validation errors
5. Use filters to focus on specific records

### After Import

1. Review import statistics
2. Check for errors
3. Verify data in database
4. Test with chatbot queries
5. Update related data if needed

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| File upload fails | Check file size (max 10MB) and format |
| Duplicate detection not working | Ensure database connection is active |
| Validation errors | Review error messages and edit data |
| Import fails | Check database connection and permissions |
| Data not appearing | Refresh page or check database directly |

### Error Messages

| Error | Meaning | Solution |
|-------|---------|----------|
| "File not found" | Uploaded file path invalid | Re-upload file |
| "Invalid category" | Category not supported | Select valid category |
| "Validation errors found" | Data doesn't meet requirements | Edit data in preview |
| "Database connection failed" | Cannot connect to database | Check database configuration |
| "Transaction failed" | Database operation error | Check logs and retry |

## Performance Considerations

| Operation | Time | Notes |
|-----------|------|-------|
| File upload | 1-5s | Depends on file size |
| Duplicate check | 2-10s | Depends on database size |
| Preview generation | 1-3s | Limited to 100 records |
| Database import | 5-30s | Depends on record count |

**Optimization Tips:**
- Import in batches for large files
- Use CSV format for faster processing
- Clean data before upload
- Schedule imports during low traffic

## Security

### File Upload Security

- File type validation
- File size limits
- Secure file storage
- Automatic cleanup

### Data Validation

- Input sanitization
- SQL injection prevention
- XSS protection
- CSRF tokens

### Access Control

- Admin-only access
- Session validation
- Audit logging
- Permission checks

## Future Enhancements

Planned features:
- Batch import for multiple files
- Import scheduling
- Data transformation rules
- Custom validation rules
- Import templates
- Export functionality
- Import history
- Rollback capability

## Related Documentation

| Document | Description |
|----------|-------------|
| [DATA_IMPORT_FEATURE.md](DATA_IMPORT_FEATURE.md) | Original data import documentation |
| [app/models/README.md](../app/models/README.md) | Models package documentation |
| [TESTING_GUIDE.md](TESTING_GUIDE.md) | Testing procedures |

---

**Feature Version:** 2.0  
**Last Updated:** February 25, 2026  
**Status:** Production Ready
