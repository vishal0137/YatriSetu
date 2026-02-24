"""
Script to create database tables
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db

app = create_app()

def create_tables():
    """Create all database tables"""
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("✅ All tables created successfully!")
        
        # List all tables
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        
        print(f"\n📊 Total tables: {len(tables)}")
        print("\nTables created:")
        for table in sorted(tables):
            print(f"  - {table}")

if __name__ == '__main__':
    create_tables()
