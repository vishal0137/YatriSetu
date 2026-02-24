# YatriSetu - Quick Start Guide

## For Windows Users

### Prerequisites Check

Before starting, ensure you have:
- ✓ Python 3.8+ installed
- ✓ PostgreSQL 14+ installed
- ✓ Database file: `YATRISETU_DB.sql` in project root

### Quick Setup (5 Minutes)

#### Option 1: Automated Setup (Recommended)

1. Open Command Prompt in project directory
2. Run the setup script:
   ```cmd
   setup.bat
   ```
3. Follow the on-screen instructions

#### Option 2: Manual Setup

1. **Create Virtual Environment**
   ```cmd
   python -m venv venv
   ```

2. **Activate Virtual Environment**
   ```cmd
   venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```cmd
   pip install -r requirements.txt
   ```

4. **Configure Environment**
   ```cmd
   copy .env.example .env
   ```
   Edit `.env` and update database credentials

5. **Setup Database**
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

6. **Run Application**
   ```cmd
   python run.py
   ```

7. **Access Dashboard**
   Open browser: http://localhost:5000/admin

### Default Credentials

- Username: `admin`
- Password: `admin123`

(Change these in `.env` file)

### Troubleshooting

#### "Python not found"
Add Python to PATH:
1. Search "Environment Variables"
2. Edit System PATH
3. Add Python directory

#### "psql not found"
Add PostgreSQL to PATH:
- Default: `C:\Program Files\PostgreSQL\14\bin`

#### "Connection refused"
Check PostgreSQL service:
```cmd
services.msc
```
Ensure "postgresql-x64-14" is running

#### Port 5000 in use
Change port in `run.py`:
```python
app.run(debug=True, port=5001)
```

### Project Structure

```
YatriSetu_Prototype/
├── app/
│   ├── __init__.py          # App initialization
│   ├── models.py            # Database models
│   ├── routes/
│   │   └── admin.py         # Admin routes
│   └── templates/
│       ├── base.html        # Base template
│       └── admin/
│           └── dashboard.html  # Dashboard
├── venv/                     # Virtual environment
├── config.py                 # Configuration
├── run.py                    # Entry point
├── requirements.txt          # Dependencies
├── .env                      # Environment variables
└── YATRISETU_DB.sql         # Database dump
```

### Development Workflow

1. **Start Development**
   ```cmd
   cd C:\Project\YatriSetu_Prototype
   venv\Scripts\activate
   python run.py
   ```

2. **Make Changes**
   - Edit files in `app/` directory
   - Flask auto-reloads on save

3. **Stop Server**
   - Press `Ctrl+C`
   - Deactivate: `deactivate`

### API Endpoints

- `GET /admin` - Dashboard
- `GET /admin/api/stats` - Statistics
- `GET /admin/api/bookings/recent` - Recent bookings
- `GET /admin/api/revenue/monthly` - Monthly revenue
- `GET /admin/api/buses/active` - Active buses

### Database Schema

Key tables:
- `users` - User accounts
- `buses` - Bus fleet
- `routes` - Bus routes
- `bookings` - Ticket bookings
- `payments` - Payment transactions
- `live_bus_locations` - GPS tracking
- `wallets` - Digital wallets

### Features Implemented

✓ Dashboard with real-time statistics
✓ Revenue analytics with charts
✓ Booking status visualization
✓ Recent bookings table
✓ Active bus monitoring
✓ Responsive design

### Next Steps

1. Explore the dashboard
2. Review code structure
3. Check API responses
4. Customize as needed
5. Add new features

### Support

For detailed documentation, see:
- [README.md](README.md) - Project overview
- [PREREQUISITES.md](PREREQUISITES.md) - Detailed setup

### Common Commands

```cmd
# Activate environment
venv\Scripts\activate

# Install new package
pip install package-name
pip freeze > requirements.txt

# Database backup
pg_dump -U postgres yatrisetu > backup.sql

# Database restore
psql -U postgres -d yatrisetu < backup.sql

# Check Python packages
pip list

# Run tests (when implemented)
python -m pytest
```

### Performance Tips

- Use database indexes for queries
- Enable caching for static data
- Optimize chart data queries
- Use pagination for large datasets

### Security Notes

- Change default admin credentials
- Use strong SECRET_KEY in production
- Enable HTTPS in production
- Implement rate limiting
- Validate all user inputs

---

**Ready to start?** Run `setup.bat` and you'll be up in 5 minutes!
