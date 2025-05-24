#!/usr/bin/env python3
"""
Database migration script to create the buyer_profiles table
"""

import os
import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app import create_app
from app.models import db, BuyerProfile

def create_buyer_profile_table():
    """Create the buyer_profiles table"""
    app = create_app()
    
    with app.app_context():
        try:
            # Check if table already exists
            with db.engine.connect() as connection:
                result = connection.execute(text("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_schema = 'public' 
                        AND table_name = 'buyer_profiles'
                    );
                """))
                
                table_exists = result.fetchone()[0]
            
            if table_exists:
                print("✅ buyer_profiles table already exists")
                return True
            
            # Create the table
            print("🔄 Creating buyer_profiles table...")
            BuyerProfile.__table__.create(db.engine)
            
            print("✅ buyer_profiles table created successfully!")
            
            # Verify the table was created
            with db.engine.connect() as connection:
                result = connection.execute(text("""
                    SELECT column_name, data_type 
                    FROM information_schema.columns 
                    WHERE table_name = 'buyer_profiles'
                    ORDER BY ordinal_position;
                """))
                
                columns = result.fetchall()
                print(f"📋 Table created with {len(columns)} columns:")
                for col_name, col_type in columns:
                    print(f"   - {col_name}: {col_type}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error creating buyer_profiles table: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == "__main__":
    print("🚀 Starting buyer_profiles table migration...")
    success = create_buyer_profile_table()
    
    if success:
        print("✅ Migration completed successfully!")
    else:
        print("❌ Migration failed!")
        sys.exit(1)
