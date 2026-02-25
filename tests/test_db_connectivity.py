"""
PostgreSQL Database Connectivity Test
Tests database connection and basic operations
"""

import sys
import os
import pytest

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def test_database_connection():
    """Test basic database connection"""
    print("\n" + "=" * 70)
    print("PostgreSQL Database Connectivity Test")
    print("=" * 70)
    
    try:
        import psycopg2
        from config import Config
        
        print("\n1. Configuration Check")
        print("-" * 70)
        print(f"Host: {Config.DB_HOST}")
        print(f"Port: {Config.DB_PORT}")
        print(f"Database: {Config.DB_NAME}")
        print(f"User: {Config.DB_USER}")
        print(f"Password: {'*' * len(Config.DB_PASSWORD)}")
        print(f"Connection String: postgresql://{Config.DB_USER}:***@{Config.DB_HOST}:{Config.DB_PORT}/{Config.DB_NAME}")
        
        print("\n2. Testing Connection")
        print("-" * 70)
        
        # Try to connect
        conn = psycopg2.connect(
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            database=Config.DB_NAME,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD
        )
        
        print("✓ Connection successful!")
        
        # Test query
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"✓ PostgreSQL version: {version[0][:50]}...")
        
        # Check if database exists
        cursor.execute("SELECT current_database();")
        db_name = cursor.fetchone()
        print(f"✓ Connected to database: {db_name[0]}")
        
        # List tables
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        tables = cursor.fetchall()
        
        if tables:
            print(f"\n✓ Found {len(tables)} tables:")
            for table in tables:
                print(f"  - {table[0]}")
        else:
            print("\n⚠ No tables found in database")
            print("  Run database migrations to create tables")
        
        cursor.close()
        conn.close()
        
        print("\n" + "=" * 70)
        print("✓ All database connectivity tests passed!")
        print("=" * 70)
        
        return True
        
    except ImportError as e:
        print(f"\n✗ Error: psycopg2 not installed")
        print(f"  Install with: pip install psycopg2-binary")
        return False
        
    except psycopg2.OperationalError as e:
        print(f"\n✗ Connection failed!")
        print(f"  Error: {str(e)}")
        print("\nTroubleshooting:")
        print("  1. Check if PostgreSQL is running")
        print("  2. Verify credentials in .env file")
        print("  3. Ensure database 'yatrisetu_db' exists")
        print("  4. Check PostgreSQL is listening on localhost:5432")
        print("\nQuick fixes:")
        print("  - Update DB_PASSWORD in .env file")
        print("  - Create database: createdb yatrisetu_db")
        print("  - Check pg_hba.conf for authentication settings")
        return False
        
    except Exception as e:
        print(f"\n✗ Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_sqlalchemy_connection():
    """Test SQLAlchemy connection"""
    print("\n" + "=" * 70)
    print("SQLAlchemy Database Connection Test")
    print("=" * 70)
    
    try:
        from flask import Flask
        from flask_sqlalchemy import SQLAlchemy
        from config import Config
        
        print("\n1. Creating Flask app with SQLAlchemy")
        print("-" * 70)
        
        app = Flask(__name__)
        app.config.from_object(Config)
        db = SQLAlchemy(app)
        
        print("✓ Flask app created")
        print("✓ SQLAlchemy initialized")
        
        print("\n2. Testing database connection")
        print("-" * 70)
        
        with app.app_context():
            # Test connection
            result = db.session.execute(db.text("SELECT 1"))
            print("✓ Database query successful")
            
            # Get database info
            result = db.session.execute(db.text("SELECT current_database(), current_user"))
            db_info = result.fetchone()
            print(f"✓ Database: {db_info[0]}")
            print(f"✓ User: {db_info[1]}")
            
            # Check tables
            result = db.session.execute(db.text("""
                SELECT COUNT(*) 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """))
            table_count = result.fetchone()[0]
            print(f"✓ Tables in database: {table_count}")
        
        print("\n" + "=" * 70)
        print("✓ SQLAlchemy connection test passed!")
        print("=" * 70)
        
        return True
        
    except Exception as e:
        print(f"\n✗ SQLAlchemy connection failed!")
        print(f"  Error: {str(e)}")
        return False


def test_database_models():
    """Test if database models can be imported"""
    print("\n" + "=" * 70)
    print("Database Models Import Test")
    print("=" * 70)
    
    try:
        from app.models import User, Bus, Route, Booking, Stop
        
        print("\n✓ Successfully imported models:")
        print("  - User")
        print("  - Bus")
        print("  - Route")
        print("  - Booking")
        print("  - Stop")
        
        print("\n" + "=" * 70)
        print("✓ Models import test passed!")
        print("=" * 70)
        
        return True
        
    except Exception as e:
        print(f"\n✗ Failed to import models: {str(e)}")
        return False


def run_all_tests():
    """Run all database connectivity tests"""
    print("\n" + "=" * 70)
    print("YATRISETU DATABASE CONNECTIVITY TEST SUITE")
    print("=" * 70)
    
    results = []
    
    # Test 1: Basic psycopg2 connection
    results.append(("PostgreSQL Connection", test_database_connection()))
    
    # Test 2: SQLAlchemy connection
    results.append(("SQLAlchemy Connection", test_sqlalchemy_connection()))
    
    # Test 3: Models import
    results.append(("Database Models", test_database_models()))
    
    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    for test_name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{test_name:.<50} {status}")
    
    total = len(results)
    passed = sum(1 for _, p in results if p)
    
    print("-" * 70)
    print(f"Total: {passed}/{total} tests passed")
    print("=" * 70)
    
    return all(p for _, p in results)


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
