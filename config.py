import os
from dotenv import load_dotenv
from pathlib import Path
from urllib.parse import quote_plus

# Get the base directory
basedir = Path(__file__).parent

# Load .env file explicitly - check both locations
env_path = basedir / 'env' / '.env'
if not env_path.exists():
    env_path = basedir / '.env'

load_dotenv(dotenv_path=env_path, override=True)

class Config:
    """Application configuration"""
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('FLASK_ENV', 'development') == 'development'
    
    # Database Configuration
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_NAME = os.getenv('DB_NAME', 'yatrisetu_db')
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')
    
    # URL-encode password to handle special characters like @
    DB_PASSWORD_ENCODED = quote_plus(DB_PASSWORD)
    
    # SQLAlchemy Configuration
    SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASSWORD_ENCODED}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = DEBUG
    
    # Admin Credentials
    ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin123')
    
    # Application Settings
    ITEMS_PER_PAGE = 20
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
