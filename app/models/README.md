# YatriSetu Models Package

## Overview

The models package contains all core business logic, data processing, and database models for the YatriSetu Smart Transit Platform. This package is organized into two primary categories: Database Models and Processing Models.

## Package Structure

```
app/models/
├── __init__.py                    # Package initialization and exports
├── database_models.py             # SQLAlchemy ORM models
├── chatbot.py                     # AI chatbot processing model
├── data_extractor.py              # Data extraction and validation model
├── unified_data_processor.py     # Unified data processing pipeline
└── README.md                      # This file
```

## Models Classification

### Database Models (ORM)

Database models define the schema and relationships for PostgreSQL database tables using SQLAlchemy ORM.

| Model | Table | Purpose |
|-------|-------|---------|
| User | users | User account management |
| Bus | buses | Bus fleet information |
| Route | routes | Route definitions and details |
| Booking | bookings | Ticket booking records |

### Processing Models

Processing models handle business logic, data transformation, and external data integration.

| Model | Purpose | Input | Output |
|-------|---------|-------|--------|
| Chatbot | Natural language query processing | Text messages | Structured responses |
| DataExtractor | File data extraction and validation | CSV/PDF files | Validated data objects |
| UnifiedDataProcessor | Complete data processing pipeline | PDF files | Database-ready CSV files |

## Database Models

### User Model

Manages user accounts and authentication.

**Schema:**
```python
class User(db.Model):
    id: Integer (Primary Key)
    email: String(255) (Unique, Required)
    phone: String(20)
    full_name: String(255) (Required)
    hashed_password: String(255) (Required)
    role: String(20)
    is_active: Boolean (Default: True)
    created_at: DateTime
    updated_at: DateTime
```

**Usage:**
```python
from app.models import User

# Create new user
user = User(
    email='user@example.com',
    full_name='John Doe',
    hashed_password=hash_password('password'),
    role='passenger'
)
db.session.add(user)
db.session.commit()

# Query user
user = User.query.filter_by(email='user@example.com').first()
```

### Bus Model

Manages bus fleet information.

**Schema:**
```python
class Bus(db.Model):
    id: Integer (Primary Key)
    bus_number: String(50) (Unique, Required)
    registration_number: String(50) (Unique, Required)
    capacity: Integer (Required)
    bus_type: String(50)
    is_active: Boolean (Default: True)
    created_at: DateTime
    updated_at: DateTime
```

**Usage:**
```python
from app.models import Bus

# Create new bus
bus = Bus(
    bus_number='DL-1234',
    registration_number='DL01AB1234',
    capacity=50,
    bus_type='AC'
)
db.session.add(bus)
db.session.commit()
```

### Route Model

Manages route definitions and details.

**Schema:**
```python
class Route(db.Model):
    id: Integer (Primary Key)
    route_number: String(50) (Unique, Required)
    route_name: String(255) (Required)
    bus_id: Integer (Foreign Key → buses.id)
    start_location: String(255) (Required)
    end_location: String(255) (Required)
    distance_km: Numeric(5,2)
    estimated_duration_minutes: Integer
    fare: Numeric(10,2) (Required)
    is_active: Boolean (Default: True)
    created_at: DateTime
    updated_at: DateTime
```

**Usage:**
```python
from app.models import Route

# Create new route
route = Route(
    route_number='DS-1',
    route_name='Dwarka to Nehru Place',
    start_location='Dwarka Sector-6',
    end_location='Nehru Place',
    distance_km=25.5,
    estimated_duration_minutes=45,
    fare=50.00
)
db.session.add(route)
db.session.commit()
```

### Booking Model

Manages ticket booking records.

**Schema:**
```python
class Booking(db.Model):
    id: Integer (Primary Key)
    user_id: Integer (Foreign Key → users.id)
    route_id: Integer (Foreign Key → routes.id)
    booking_reference: String(50) (Unique)
    journey_date: Date
    passenger_count: Integer
    total_fare: Numeric(10,2)
    status: String(20)
    created_at: DateTime
    updated_at: DateTime
```

## Processing Models

### Chatbot Model

Processes natural language queries and provides intelligent responses.

**Capabilities:**
- Route search and recommendations
- Fare calculations
- Bus information retrieval
- Location matching with fuzzy search
- Context-aware multi-turn conversations

**API:**
```python
from app.models import Chatbot

chatbot = Chatbot()

# Process user message
response = chatbot.process_message("Route from Connaught Place to Dwarka")

# Response structure
{
    'message': str,           # Response text
    'type': str,             # Response type
    'routes': list,          # Route data (if applicable)
    'suggestions': list      # Quick action suggestions
}
```

**Key Methods:**

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| process_message | message: str | dict | Process user query and return response |
| find_route | source: str, destination: str | list | Find routes between locations |
| calculate_fare | route_id: str, passenger_type: str | float | Calculate fare for route |
| get_bus_info | bus_number: str | dict | Retrieve bus information |

### DataExtractor Model

Extracts and validates data from CSV and PDF files.

**Capabilities:**
- CSV file parsing and analysis
- PDF table extraction
- Automatic category detection
- Data structure validation
- Schema compliance checking
- Export to standardized CSV format

**API:**
```python
from app.models import DataExtractor

extractor = DataExtractor()

# Analyze file structure
analysis = extractor.analyze_csv_structure('routes.csv')

# Extract data by category
routes = extractor.extract_routes_from_csv('routes.csv')
buses = extractor.extract_buses_from_csv('buses.csv')
fares = extractor.extract_fares_from_csv('fares.csv')
stops = extractor.extract_stops_from_csv('stops.csv')

# Get validation report
report = extractor.get_validation_report()
```

**Key Methods:**

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| analyze_csv_structure | file_path: str | dict | Analyze CSV file structure |
| extract_routes_from_csv | file_path: str | list | Extract route data |
| extract_buses_from_csv | file_path: str | list | Extract bus data |
| extract_fares_from_csv | file_path: str | list | Extract fare data |
| extract_stops_from_csv | file_path: str | list | Extract stop data |
| extract_from_pdf | file_path: str | dict | Extract tables from PDF |
| get_validation_report | - | dict | Get validation results |
| export_to_csv | category: str, output_path: str | None | Export data to CSV |

### UnifiedDataProcessor Model

Complete data processing pipeline from PDF extraction to database-ready CSV files.

**Capabilities:**
- Unified PDF extraction and cleaning
- Automatic category detection
- Database schema alignment
- Comprehensive data validation
- Automatic generation of related data (stops and fares from routes)
- Multi-format export with statistics

**API:**
```python
from app.models import UnifiedDataProcessor

processor = UnifiedDataProcessor()

# Process PDF file
result = processor.process_pdf('dtc_data.pdf', category='routes')

# Check result
if result['success']:
    # Export processed data
    processor.export_to_csv('routes', 'output_routes.csv')
    processor.export_to_csv('stops', 'output_stops.csv')
    processor.export_to_csv('fares', 'output_fares.csv')
    
    # Get all data
    all_data = processor.get_all_data()
```

**Key Methods:**

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| process_pdf | pdf_path: str, category: str | dict | Complete PDF processing pipeline |
| export_to_csv | category: str, output_path: str | None | Export to CSV format |
| get_all_data | - | dict | Retrieve all extracted data |
| get_validation_report | - | dict | Get validation statistics |

**Processing Pipeline:**
```
PDF File Input
    ↓
Table Extraction
    ↓
Data Parsing
    ↓
Data Cleaning
    ↓
Schema Alignment
    ↓
Data Validation
    ↓
Related Data Generation
    ↓
CSV Export
```

## Integration Patterns

### With Flask Routes

```python
from flask import Blueprint, request, jsonify
from app.models import Chatbot, DataExtractor

# Chatbot integration
@chatbot_bp.route('/api/message', methods=['POST'])
def process_message():
    chatbot = Chatbot()
    response = chatbot.process_message(request.json['message'])
    return jsonify(response)

# Data import integration
@data_import_bp.route('/api/analyze', methods=['POST'])
def analyze_file():
    extractor = DataExtractor()
    analysis = extractor.analyze_csv_structure(file_path)
    return jsonify(analysis)
```

### With CLI Tools

```python
from app.models import UnifiedDataProcessor

def main():
    processor = UnifiedDataProcessor()
    result = processor.process_pdf(pdf_path, category='routes')
    
    if result['success']:
        processor.export_to_csv('routes', 'output.csv')
```

## Data Validation

All processing models implement comprehensive validation:

### Validation Rules

| Category | Rules |
|----------|-------|
| Routes | Required fields, valid locations, positive distances |
| Stops | Required fields, valid coordinates, positive sequences |
| Fares | Required fields, valid passenger types, non-negative amounts |
| Buses | Required fields, valid types, positive capacity |

### Validation Response

```python
{
    'is_valid': bool,
    'total_errors': int,
    'total_warnings': int,
    'errors': list,
    'warnings': list
}
```

## Error Handling

All models implement standardized error handling:

```python
import logging

logger = logging.getLogger(__name__)

try:
    result = processor.process_pdf(pdf_path)
except FileNotFoundError:
    logger.error("File not found")
except ValidationError as e:
    logger.error(f"Validation failed: {e}")
except Exception as e:
    logger.error(f"Unexpected error: {e}")
```

## Performance Metrics

| Model | Operation | Time | Memory |
|-------|-----------|------|--------|
| Chatbot | Query processing | <100ms | ~50MB |
| DataExtractor | CSV extraction (1000 rows) | ~2-5s | ~100MB |
| UnifiedDataProcessor | PDF processing | ~5-10s | ~200MB |
| Database Models | CRUD operations | <50ms | ~20MB |

## Dependencies

### Required Packages

```txt
Flask>=3.0.0
Flask-SQLAlchemy>=3.1.1
psycopg2-binary>=2.9.9
pandas>=1.5.3
pdfplumber>=0.9.0
PyPDF2>=3.0.1
scikit-learn>=1.3.0
numpy>=1.24.3
```

### Installation

```bash
pip install -r requirements.txt
```

## Testing

### Unit Tests

```python
# tests/test_models.py
from app.models import Chatbot, DataExtractor, UnifiedDataProcessor

def test_chatbot_processing():
    chatbot = Chatbot()
    response = chatbot.process_message("Hello")
    assert response is not None
    assert 'message' in response

def test_data_extraction():
    extractor = DataExtractor()
    analysis = extractor.analyze_csv_structure('test_data.csv')
    assert analysis['total_rows'] > 0

def test_unified_processing():
    processor = UnifiedDataProcessor()
    result = processor.process_pdf('test.pdf')
    assert result['success'] == True
```

## Configuration

### Environment Variables

```env
# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=yatrisetu_db
DB_USER=postgres
DB_PASSWORD=your_password

# Model Configuration
CHATBOT_CONFIDENCE_THRESHOLD=0.7
DATA_VALIDATION_STRICT=true
MAX_FILE_SIZE_MB=10
```

## Best Practices

### Database Models

1. Always use transactions for data modifications
2. Implement proper indexing for frequently queried fields
3. Use lazy loading for relationships
4. Validate data before database insertion
5. Handle database exceptions gracefully

### Processing Models

1. Validate input data before processing
2. Implement comprehensive error handling
3. Log all operations for debugging
4. Use appropriate data types
5. Generate detailed processing reports

## Maintenance

### Regular Tasks

| Task | Frequency | Description |
|------|-----------|-------------|
| Database backup | Daily | Backup all database tables |
| Log review | Weekly | Review error and warning logs |
| Performance monitoring | Weekly | Monitor query and processing times |
| Validation rule updates | Monthly | Update validation rules as needed |
| Documentation updates | As needed | Keep documentation current |

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | February 2026 | Initial release with all core models |

## CLI Tools

### process_dtc_data.py

Command-line interface for processing DTC PDF files and generating database-ready CSV files.

**Location:** `process_dtc_data.py` (project root)

**Usage:**

```bash
# Basic usage
python process_dtc_data.py input.pdf output_directory

# With specific category
python process_dtc_data.py input.pdf output_dir --category routes

# Verbose output
python process_dtc_data.py input.pdf output_dir --verbose
```

**Arguments:**

| Argument | Type | Description |
|----------|------|-------------|
| pdf_path | Required | Path to PDF file to process |
| output_dir | Required | Directory for output CSV files |
| --category | Optional | Data category (routes, buses, stops, fares) |
| --verbose | Flag | Show detailed processing information |

**Output Files:**

- `routes_final.csv` - Route information
- `stops_final.csv` - Stop sequences
- `fares_final.csv` - Fare structure

**Example:**

```bash
python process_dtc_data.py destination_bus_services_nov_2025_1_0.pdf processed_data
```

## Support

For issues or questions regarding models:

1. Review model documentation
2. Check error logs in `logs/` directory
3. Consult API documentation
4. Contact development team

## Related Documentation

| Document | Description |
|----------|-------------|
| [DATA_IMPORT_FEATURE.md](../../docs/DATA_IMPORT_FEATURE.md) | Data import feature documentation |
| [CHATBOT_QUICK_REFERENCE.md](../../docs/CHATBOT_QUICK_REFERENCE.md) | Chatbot API reference |
| [PROJECT_STRUCTURE.md](../../docs/PROJECT_STRUCTURE.md) | Overall project structure |
| [processed_data/README.md](../../processed_data/README.md) | Processed data specifications |

---

**Package Version:** 1.0.0  
**Last Updated:** February 25, 2026  
**Maintained By:** YatriSetu Development Team
