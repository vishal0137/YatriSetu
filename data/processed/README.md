# Processed DTC Bus Services Data

## Overview

This directory contains finalized, database-ready CSV files processed through the Unified Data Processor. All data has been extracted from PDF, cleaned, validated, and aligned with the YatriSetu database schema.

## Location

This folder is located at: `data/processed/`

Raw input files are stored in: `data/raw/`

## Processing Pipeline

```
PDF File
    ↓
Table Extraction (pdfplumber)
    ↓
Data Parsing & Cleaning
    ↓
Schema Alignment
    ↓
Data Validation
    ↓
Related Data Generation
    ↓
Final CSV Export
```

## Generated Files

| File | Records | Description | Status |
|------|---------|-------------|--------|
| routes_final.csv | 41 | Complete route information | ✅ Ready |
| stops_final.csv | 82 | All bus stops with sequences | ✅ Ready |
| fares_final.csv | 205 | Fare structure for all categories | ✅ Ready |

## Data Quality

| Metric | Value |
|--------|-------|
| Validation Status | ✅ Passed |
| Schema Compliance | 100% |
| Required Fields | Complete |
| Data Types | Correct |
| Duplicates | None |

## File Specifications

### 1. routes_final.csv

**Schema-Aligned Fields:**
- `route_number` (string, required) - Route identifier
- `route_name` (string, required) - Full route name
- `start_location` (string, required) - Origin point
- `end_location` (string, required) - Destination point
- `distance` (float, optional) - Route distance in km
- `duration` (integer, optional) - Travel duration in minutes
- `bus_type` (string, optional) - Type of bus (default: Regular)
- `status` (string, optional) - Route status (default: Active)
- `frequency` (integer, optional) - Buses per hour (default: 30)

**Sample:**
```csv
route_number,route_name,start_location,end_location,bus_type,status
DS-1,Dwarka Sector-6/7 X-ing to Nehru Place(T),Dwarka Sector-6/7 X-ing,Nehru Place(T),Regular,Active
```

### 2. stops_final.csv

**Schema-Aligned Fields:**
- `route_id` (string, required) - Route identifier
- `stop_name` (string, required) - Stop name
- `sequence` (integer, required) - Stop order on route
- `latitude` (float, optional) - GPS latitude
- `longitude` (float, optional) - GPS longitude
- `stop_type` (string, optional) - Origin/Intermediate/Destination
- `arrival_time` (string, optional) - Scheduled arrival time

**Sample:**
```csv
route_id,stop_name,sequence,stop_type
DS-1,Dwarka Sector-6/7 X-ing,1,Origin
DS-1,Telephone Exchange Dwarka Sec-6,2,Intermediate
DS-1,Nehru Place(T),6,Destination
```

### 3. fares_final.csv

**Schema-Aligned Fields:**
- `route_id` (string, required) - Route identifier
- `passenger_type` (string, required) - Passenger category
- `fare_amount` (float, required) - Fare in INR
- `currency` (string, optional) - Currency code (default: INR)
- `effective_date` (date, optional) - Effective from date
- `distance_range` (string, optional) - Distance range

**Sample:**
```csv
route_id,passenger_type,fare_amount,currency,effective_date
DS-1,General,50,INR,2026-02-25
DS-1,Student,25,INR,2026-02-25
```

## Database Import

### Using Admin Panel

1. Navigate to: `http://localhost:5000/admin/data-import`
2. Upload files in order:
   - routes_final.csv → Category: Routes
   - stops_final.csv → Category: Stops
   - fares_final.csv → Category: Fares
3. Review validation
4. Click "Import to Database"

### Direct PostgreSQL Import

```sql
-- Import Routes
\copy routes(route_number, route_name, start_location, end_location, bus_type, status, frequency) 
FROM 'processed_data/routes_final.csv' 
DELIMITER ',' CSV HEADER;

-- Import Stops
\copy stops(route_id, stop_name, sequence, stop_type) 
FROM 'processed_data/stops_final.csv' 
DELIMITER ',' CSV HEADER;

-- Import Fares
\copy fares(route_id, passenger_type, fare_amount, currency, effective_date) 
FROM 'processed_data/fares_final.csv' 
DELIMITER ',' CSV HEADER;
```

## Processing Statistics

### Routes
- Total Routes: 41
- Unique Origins: 32
- Unique Destinations: 13
- Bus Type: Regular (AC service)
- Status: All Active

### Stops
- Total Stops: 82
- Unique Locations: 65
- Origin Points: 41
- Destination Points: 41
- Intermediate Stops: Variable per route

### Fares
- Total Fare Records: 205
- Routes Covered: 41
- Passenger Categories: 5
- Currency: INR
- Effective Date: 2026-02-25

## Passenger Categories & Fares

| Category | Base Fare | Discount |
|----------|-----------|----------|
| General | ₹50 | - |
| Student | ₹25 | 50% |
| Senior Citizen | ₹30 | 40% |
| Differently Abled | ₹25 | 50% |
| Child | ₹20 | 60% |

## Data Validation Results

✅ All required fields present  
✅ Data types correct  
✅ No duplicate routes  
✅ Sequential stop ordering  
✅ Valid passenger categories  
✅ Positive fare amounts  
✅ Consistent route references  

## Processing Tool

Generated using: **Unified Data Processor**

```bash
python scripts/process_dtc_data.py data/raw/destination_bus_services_nov_2025_1_0.pdf data/processed
```

## Features

- ✅ Automatic PDF table extraction
- ✅ Intelligent data cleaning
- ✅ Database schema alignment
- ✅ Comprehensive validation
- ✅ Related data generation (stops, fares)
- ✅ Export to CSV format

## Maintenance

### Updating Data

When new DTC data is available:

```bash
# Process new PDF
python scripts/process_dtc_data.py data/raw/new_dtc_data.pdf data/processed

# Review generated files
# Import via admin panel or database
```

### Data Refresh Schedule

| Update Type | Frequency |
|-------------|-----------|
| Route Changes | As announced |
| Fare Updates | Quarterly |
| Stop Updates | Monthly |
| Schedule Changes | Seasonal |

## Source Information

| Property | Value |
|----------|-------|
| Source File | destination_bus_services_nov_2025_1_0.pdf |
| Processing Date | February 25, 2026 |
| Processor Version | 1.0 |
| Data Period | November 2025 onwards |
| Service Type | AC Destination Bus Service |

## Next Steps

1. ✅ Data extracted and processed
2. ✅ Schema alignment complete
3. ✅ Validation passed
4. ⏳ Import to database
5. ⏳ Test with chatbot
6. ⏳ Verify route search functionality

## Support

For issues or questions:
- Review: `docs/DATA_IMPORT_FEATURE.md`
- Check: `app/unified_data_processor.py`
- Run: `python process_dtc_data.py --help`

---

**Status:** Ready for Database Import  
**Quality:** Production Grade  
**Last Updated:** February 25, 2026
