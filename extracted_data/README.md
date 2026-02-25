# Extracted DTC Bus Services Data

## Overview

This directory contains cleaned and formatted data extracted from the DTC (Delhi Transport Corporation) PDF file: `destination_bus_services_nov_2025_1_0.pdf`

## Files

| File | Records | Description |
|------|---------|-------------|
| routes_cleaned.csv | 40 | AC bus routes with origin, destination, and timings |
| stops_cleaned.csv | 204 | Bus stops for all routes with sequence information |
| fares_cleaned.csv | 200 | Fare structure for all passenger categories |

## Data Quality

| Metric | Value |
|--------|-------|
| Total Routes | 40 |
| Unique Stops | 139 |
| Passenger Categories | 5 |
| Data Completeness | 100% |
| Data Source | DTC Official PDF (November 2025) |

## File Descriptions

### 1. routes_cleaned.csv

Contains route information for AC bus services.

**Columns:**
- `route_number` - Route identifier (e.g., DS-1, DS-2)
- `route_name` - Full route name (Origin to Destination)
- `start_location` - Starting point
- `end_location` - Ending point
- `intermediate_stops` - Comma-separated list of stops
- `morning_departure` - Morning departure time from origin
- `evening_departure` - Evening departure time from destination
- `bus_type` - Bus type (AC)
- `status` - Route status (Active)

**Sample Data:**
```csv
route_number,route_name,start_location,end_location,morning_departure,evening_departure
DS-1,Dwarka Sector-6/7 X-ing to Nehru Place(T),Dwarka Sector-6/7 X-ing,Nehru Place(T),8.20,18.05
DS-2,Dwarka Sec-4/5 Xing to CGO Complex,Dwarka Sec-4/5 Xing,CGO Complex (JLN Stadium),8.15,18.05
```

### 2. stops_cleaned.csv

Contains all bus stops for each route with sequence information.

**Columns:**
- `route_id` - Route identifier
- `stop_name` - Name of the bus stop
- `sequence` - Stop sequence number on the route
- `stop_type` - Type of stop (Origin, Intermediate, Destination)

**Sample Data:**
```csv
route_id,stop_name,sequence,stop_type
DS-1,Dwarka Sector-6/7 X-ing,1,Origin
DS-1,Telephone Exchange Dwarka Sec-6,2,Intermediate
DS-1,Nehru Place(T),6,Destination
```

### 3. fares_cleaned.csv

Contains fare information for all passenger categories.

**Columns:**
- `route_id` - Route identifier
- `passenger_type` - Category of passenger
- `fare_amount` - Fare in INR
- `currency` - Currency code (INR)
- `effective_date` - Date from which fare is effective

**Passenger Categories:**
- General
- Student
- Senior Citizen
- Differently Abled
- Child

**Sample Data:**
```csv
route_id,passenger_type,fare_amount,currency,effective_date
DS-1,General,50,INR,2025-11-01
DS-1,Student,25,INR,2025-11-01
DS-1,Senior Citizen,30,INR,2025-11-01
```

## Import Instructions

### Using YatriSetu Admin Panel

1. Navigate to: `http://localhost:5000/admin/data-import`
2. Upload each CSV file:
   - Upload `routes_cleaned.csv` → Select category: **Routes**
   - Upload `stops_cleaned.csv` → Select category: **Stops**
   - Upload `fares_cleaned.csv` → Select category: **Fares**
3. Review the analysis and validation
4. Click "Import to Database"

### Manual Database Import

#### PostgreSQL Commands:

```sql
-- Import Routes
COPY routes(route_number, route_name, start_location, end_location, bus_type, status)
FROM 'C:/Project/YatriSetu_Prototype/extracted_data/routes_cleaned.csv'
DELIMITER ',' CSV HEADER;

-- Import Stops
COPY stops(route_id, stop_name, sequence, stop_type)
FROM 'C:/Project/YatriSetu_Prototype/extracted_data/stops_cleaned.csv'
DELIMITER ',' CSV HEADER;

-- Import Fares
COPY fares(route_id, passenger_type, fare_amount, currency, effective_date)
FROM 'C:/Project/YatriSetu_Prototype/extracted_data/fares_cleaned.csv'
DELIMITER ',' CSV HEADER;
```

## Data Statistics

### Routes Distribution

| Metric | Count |
|--------|-------|
| Total AC Routes | 40 |
| Dwarka Routes | 4 |
| Rohini Routes | 4 |
| Badarpur Routes | 2 |
| Other Routes | 30 |

### Stops Distribution

| Metric | Count |
|--------|-------|
| Total Stops | 204 |
| Unique Locations | 139 |
| Origin Points | 40 |
| Destination Points | 40 |
| Intermediate Stops | 124 |

### Fare Structure

| Passenger Type | Fare (INR) | Discount |
|----------------|------------|----------|
| General | 50 | - |
| Student | 25 | 50% |
| Senior Citizen | 30 | 40% |
| Differently Abled | 25 | 50% |
| Child | 20 | 60% |

## Data Validation

All data has been validated for:

- ✅ Required fields present
- ✅ Data types correct
- ✅ No duplicate routes
- ✅ Sequential stop ordering
- ✅ Valid passenger categories
- ✅ Positive fare amounts
- ✅ Consistent route references

## Notes

1. **Timings:** Morning and evening departure times are in 24-hour format
2. **Stops:** Intermediate stops are listed in sequence order
3. **Fares:** Standard DTC AC bus fare structure applied
4. **Status:** All routes marked as "Active" as per source document
5. **Effective Date:** Fares effective from November 1, 2025

## Source Information

| Property | Value |
|----------|-------|
| Source Document | destination_bus_services_nov_2025_1_0.pdf |
| Document Type | DTC Official Bus Services List |
| Extraction Date | February 25, 2026 |
| Data Period | November 2025 onwards |
| Bus Type | AC Buses |
| Service Type | Destination Bus Service |

## Maintenance

To update this data:

1. Obtain latest DTC PDF document
2. Run extraction script: `python test_pdf_extraction.py`
3. Run cleaning script: `python clean_extracted_data.py`
4. Review and validate cleaned CSV files
5. Import to database using admin panel

## Contact

For questions or issues with the data, please contact the YatriSetu development team.

---

**Last Updated:** February 25, 2026  
**Data Version:** 1.0  
**Status:** Ready for Import
