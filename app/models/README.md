# YatriSetu Models Package

## Overview

The models package contains all core business logic and database models for the YatriSetu Smart Transit Platform.

## Package Structure

```
app/models/
├── __init__.py                    # Package initialization and exports
├── database_models.py             # SQLAlchemy ORM models
├── chatbot.py                     # AI chatbot processing model
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
| Stop | stops | Bus stop information |
| Driver | drivers | Driver information |
| Conductor | conductors | Conductor information |
| Payment | payments | Payment transactions |
| Wallet | wallets | User wallet management |
| LiveBusLocation | live_bus_locations | Real-time bus tracking |

### Processing Models

Processing models handle business logic and natural language processing.

| Model | Purpose | Input | Output |
|-------|---------|-------|--------|
| Chatbot | Natural language query processing | Text messages | Structured responses |

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

## Integration Patterns

### With Flask Routes

```python
from flask import Blueprint, request, jsonify
from app.models import Chatbot

# Chatbot integration
@chatbot_bp.route('/api/message', methods=['POST'])
def process_message():
    chatbot = Chatbot()
    response = chatbot.process_message(request.json['message'])
    return jsonify(response)
```

## Error Handling

All models implement standardized error handling:

```python
import logging

logger = logging.getLogger(__name__)

try:
    response = chatbot.process_message(message)
except Exception as e:
    logger.error(f"Unexpected error: {e}")
```

## Dependencies

### Required Packages

```txt
Flask>=3.0.0
Flask-SQLAlchemy>=3.1.1
psycopg2-binary>=2.9.9
scikit-learn>=1.3.0
numpy>=1.24.3
```

## Testing

### Unit Tests

```python
# tests/test_models_comprehensive.py
from app.models import Chatbot

def test_chatbot_processing():
    chatbot = Chatbot()
    response = chatbot.process_message("Hello")
    assert response is not None
    assert 'message' in response
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

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | February 2026 | Core models with chatbot functionality |

## Related Documentation

| Document | Description |
|----------|-------------|
| [CHATBOT_QUICK_REFERENCE.md](../../docs/CHATBOT_QUICK_REFERENCE.md) | Chatbot API reference |
| [PROJECT_STRUCTURE.md](../../docs/PROJECT_STRUCTURE.md) | Overall project structure |

---

**Package Version:** 1.0.0  
**Last Updated:** February 25, 2026  
**Maintained By:** YatriSetu Development Team
