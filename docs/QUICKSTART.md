# YatriSetu Quick Start Guide

## Prerequisites Verification

Before proceeding, ensure the following software is installed:

| Requirement | Minimum Version | Verification Command |
|-------------|----------------|---------------------|
| Python | 3.8+ | `python --version` |
| PostgreSQL | 14+ | `psql --version` |
| Database File | YATRISETU_DB.sql | Check project root |

## Installation Methods

### Method 1: Automated Setup (Recommended)

1. Open Command Prompt in project directory
2. Execute setup script:

```cmd
setup.bat
```

3. Follow on-screen instructions

### Method 2: Manual Setup

#### Step 1: Create Virtual Environment

```cmd
python -m venv venv
```

#### Step 2: Activate Virtual Environment

```cmd
venv\Scripts\activate
```

#### Step 3: Install Dependencies

```cmd
pip install -r requirements.txt
```

#### Step 4: Configure Environment

```cmd
copy .env.example .env
```

Edit `.env` file and update database credentials.

#### Step 5: Database Setup

```cmd
psql -U postgres
```

```sql
CREATE DATABASE yatrisetu;
\q
```

```cmd
psql -U postgres -d yatrisetu < YATRISETU_DB.sql
```

#### Step 6: Run Application

```cmd
python run.py
```

#### Step 7: Access Dashboard

Navigate to: http://localhost:5000/admin

## Default Credentials

| Field | Value |
|-------|-------|
| Username | admin |
| Password | admin123 |

**Note:** Update credentials in `.env` file for production use.

## Troubleshooting

### Python Not Found

**Solution:** Add Python to system PATH

1. Open System Properties
2. Navigate to Environment Variables
3. Edit System PATH variable
4. Add Python installation directory

### PostgreSQL Command Not Found

**Solution:** Add PostgreSQL to system PATH

Default PostgreSQL location: `C:\Program Files\PostgreSQL\14\bin`

### Database Connection Refused

**Solution:** Verify PostgreSQL service status

```cmd
services.msc
```

Ensure "postgresql-x64-14" service is running.

### Port 5000 Already in Use

**Solution:** Modify port in `run.py`

```python
app.run(debug=True, port=5001)
```

## Project Structure

```
YatriSetu_Prototype/
├── app/
│   ├── __init__.py          # Application initialization
│   ├── models.py            # Database models
│   ├── routes/
│   │   └── admin.py         # Admin route handlers
│   └── templates/
│       ├── base.html        # Base template
│       └── admin/
│           └── dashboard.html  # Dashboard interface
├── venv/                     # Virtual environment
├── config.py                 # Configuration settings
├── run.py                    # Application entry point
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables
└── YATRISETU_DB.sql         # Database schema and data
```

## Development Workflow

### Starting Development

```cmd
cd C:\Project\YatriSetu_Prototype
venv\Scripts\activate
python run.py
```

### Making Changes

- Edit files in `app/` directory
- Flask automatically reloads on file save (development mode)

### Stopping Server

- Press `Ctrl+C` in terminal
- Deactivate environment: `deactivate`

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /admin | Dashboard interface |
| GET | /admin/api/stats | System statistics |
| GET | /admin/api/bookings/recent | Recent bookings |
| GET | /admin/api/revenue/monthly | Monthly revenue data |
| GET | /admin/api/buses/active | Active bus information |

## Database Schema

### Core Tables

| Table | Description |
|-------|-------------|
| users | User account information |
| buses | Bus fleet data |
| routes | Bus route definitions |
| bookings | Ticket booking records |
| payments | Payment transactions |
| live_bus_locations | GPS tracking data |
| wallets | Digital wallet balances |

## Implemented Features

| Feature | Status |
|---------|--------|
| Real-time statistics dashboard | Implemented |
| Revenue analytics with charts | Implemented |
| Booking status visualization | Implemented |
| Recent bookings table | Implemented |
| Active bus monitoring | Implemented |
| Responsive design | Implemented |

## Next Steps

1. Explore dashboard interface
2. Review code structure
3. Test API endpoints
4. Customize configuration
5. Implement additional features

## Common Commands

### Environment Management

```cmd
# Activate virtual environment
venv\Scripts\activate

# Install new package
pip install package-name

# Update requirements file
pip freeze > requirements.txt
```

### Database Operations

```cmd
# Create database backup
pg_dump -U postgres yatrisetu > backup.sql

# Restore database from backup
psql -U postgres -d yatrisetu < backup.sql

# List installed packages
pip list
```

### Testing

```cmd
# Run test suite (when implemented)
python -m pytest
```

## Performance Optimization

| Optimization | Implementation |
|--------------|----------------|
| Database indexes | Use for frequently queried columns |
| Static data caching | Enable for reference data |
| Chart data queries | Optimize with aggregation |
| Large datasets | Implement pagination |

## Security Considerations

| Security Measure | Priority |
|-----------------|----------|
| Change default credentials | Critical |
| Use strong SECRET_KEY | Critical |
| Enable HTTPS | Required for production |
| Implement rate limiting | Recommended |
| Validate user inputs | Critical |

## Additional Resources

| Resource | Location |
|----------|----------|
| Project overview | README.md |
| Detailed setup guide | PREREQUISITES.md |
| Architecture documentation | docs/PROJECT_STRUCTURE.md |

## Quick Reference

### Application URLs

| Interface | URL |
|-----------|-----|
| Home | http://localhost:5000 |
| Admin Dashboard | http://localhost:5000/admin |
| AI Chatbot | http://localhost:5000/chatbot |

### Configuration Files

| File | Purpose |
|------|---------|
| .env | Environment variables |
| config.py | Application configuration |
| requirements.txt | Python dependencies |

## Support

For detailed documentation, refer to:

- README.md - Project overview and features
- PREREQUISITES.md - Comprehensive setup instructions
- docs/ - Complete documentation library
