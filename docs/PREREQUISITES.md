# YatriSetu - Prerequisites and Setup Guide

## Prototype Lifecycle Strategy

This project follows a structured prototype lifecycle approach:

1. **Planning Phase** - Requirements gathering and system design
2. **Setup Phase** - Environment configuration and dependency installation
3. **Development Phase** - Iterative development of core features
4. **Testing Phase** - Unit testing and integration testing
5. **Deployment Phase** - Production deployment preparation

## System Requirements

### Hardware Requirements
- Processor: Intel Core i3 or equivalent (minimum)
- RAM: 4GB (minimum), 8GB (recommended)
- Storage: 2GB free space
- Internet connection for package downloads

### Software Requirements

#### 1. Python
- **Version:** Python 3.8 or higher
- **Download:** https://www.python.org/downloads/
- **Installation:**
  - Download the installer for Windows
  - Run the installer
  - Check "Add Python to PATH" during installation
  - Verify installation: `python --version`

#### 2. PostgreSQL
- **Version:** PostgreSQL 14 or higher
- **Download:** https://www.postgresql.org/download/windows/
- **Installation:**
  - Download the Windows installer
  - Run the installer
  - Set password for postgres user (remember this!)
  - Default port: 5432
  - Verify installation: `psql --version`

#### 3. Git (Optional)
- **Version:** Latest stable version
- **Download:** https://git-scm.com/download/win
- **Purpose:** Version control and collaboration

## Environment Setup

### Step 1: Create Project Directory

```cmd
mkdir C:\Project\YatriSetu_Prototype
cd C:\Project\YatriSetu_Prototype
```

### Step 2: Create Virtual Environment

A virtual environment isolates project dependencies from system-wide Python packages.

```cmd
python -m venv venv
```

This creates a `venv` folder containing:
- Python interpreter
- pip package manager
- Isolated package installation directory

### Step 3: Activate Virtual Environment

**Windows Command Prompt:**
```cmd
venv\Scripts\activate
```

**Windows PowerShell:**
```powershell
venv\Scripts\Activate.ps1
```

You should see `(venv)` prefix in your command prompt.

### Step 4: Upgrade pip

```cmd
python -m pip install --upgrade pip
```

### Step 5: Install Python Dependencies

```cmd
pip install -r requirements.txt
```

Required packages:
- Flask (Web framework)
- psycopg2 (PostgreSQL adapter)
- Flask-SQLAlchemy (ORM)
- python-dotenv (Environment variables)
- Werkzeug (Security utilities)

## Database Setup

### Step 1: Create Database

Open PostgreSQL command line (psql):

```cmd
psql -U postgres
```

Enter your postgres password, then:

```sql
CREATE DATABASE yatrisetu;
\q
```

### Step 2: Import Database Schema and Data

Navigate to project directory:

```cmd
cd C:\Project\YatriSetu_Prototype
```

Import the SQL file:

```cmd
psql -U postgres -d yatrisetu < YATRISETU_DB.sql
```

Or if the file is in a different location:

```cmd
psql -U postgres -d yatrisetu < C:\Project\YatriSetu_Prototype\YATRISETU_DB.sql
```

### Step 3: Verify Database Import

```cmd
psql -U postgres -d yatrisetu
```

Check tables:

```sql
\dt
SELECT COUNT(*) FROM users;
SELECT COUNT(*) FROM bookings;
SELECT COUNT(*) FROM routes;
\q
```

## Configuration

### Step 1: Create Environment File

Create `.env` file in project root:

```env
# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=yatrisetu
DB_USER=postgres
DB_PASSWORD=your_postgres_password

# Flask Configuration
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here

# Application Configuration
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123
```

**Important:** Replace `your_postgres_password` with your actual PostgreSQL password.

### Step 2: Update config.py

The `config.py` file reads from `.env` and configures the application.

## Running the Application

### Step 1: Activate Virtual Environment

```cmd
cd C:\Project\YatriSetu_Prototype
venv\Scripts\activate
```

### Step 2: Run Flask Application

```cmd
python run.py
```

You should see:

```
 * Running on http://127.0.0.1:5000
 * Running on http://localhost:5000
```

### Step 3: Access Admin Dashboard

Open browser and navigate to:
- **Admin Dashboard:** http://localhost:5000/admin
- **Login:** Use credentials from `.env` file

## Troubleshooting

### Issue: "python is not recognized"
**Solution:** Add Python to PATH environment variable
1. Search "Environment Variables" in Windows
2. Edit System PATH
3. Add Python installation directory

### Issue: "psql is not recognized"
**Solution:** Add PostgreSQL bin directory to PATH
- Default location: `C:\Program Files\PostgreSQL\14\bin`

### Issue: "Access denied for user postgres"
**Solution:** Check PostgreSQL password in `.env` file

### Issue: "Port 5000 already in use"
**Solution:** Change port in `run.py`:
```python
app.run(debug=True, port=5001)
```

### Issue: Virtual environment activation fails in PowerShell
**Solution:** Enable script execution:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Development Workflow

### Daily Development Routine

1. **Start Development:**
   ```cmd
   cd C:\Project\YatriSetu_Prototype
   venv\Scripts\activate
   python run.py
   ```

2. **Make Changes:**
   - Edit files in `app/` directory
   - Flask auto-reloads on file changes (debug mode)

3. **Test Changes:**
   - Refresh browser
   - Check console for errors

4. **Stop Development:**
   - Press `Ctrl+C` in terminal
   - Deactivate virtual environment: `deactivate`

### Installing New Packages

```cmd
pip install package-name
pip freeze > requirements.txt
```

## Project Phases

### Phase 1: Setup (Current)
- ✓ Environment setup
- ✓ Database configuration
- ✓ Basic project structure

### Phase 2: Admin Dashboard Development
- Dashboard layout
- Real-time statistics
- Data visualization
- User management

### Phase 3: API Development
- RESTful API endpoints
- Authentication & authorization
- Data validation

### Phase 4: Testing
- Unit tests
- Integration tests
- Performance testing

### Phase 5: Deployment
- Production configuration
- Server setup
- Monitoring setup

## Additional Resources

- **Flask Documentation:** https://flask.palletsprojects.com/
- **PostgreSQL Documentation:** https://www.postgresql.org/docs/
- **Bootstrap Documentation:** https://getbootstrap.com/docs/
- **Chart.js Documentation:** https://www.chartjs.org/docs/

## Support

For issues or questions:
1. Check troubleshooting section
2. Review error messages carefully
3. Consult documentation links
4. Check database connection settings

## Next Steps

After completing prerequisites:
1. Verify all installations
2. Test database connection
3. Run the application
4. Explore admin dashboard
5. Review code structure
6. Begin feature development

---

**Note:** This is a prototype environment. For production deployment, additional security measures and optimizations are required.
