#!/usr/bin/env python3
"""
Script to enable meetings in system settings
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.models import db, SystemSetting

def enable_meetings():
    """Enable meetings in system settings"""
    app = create_app()
    
    with app.app_context():
        # Check if meetings_enabled setting exists
        meetings_setting = SystemSetting.query.filter_by(key='meetings_enabled').first()
        
        if meetings_setting:
            meetings_setting.value = 'true'
            print("Updated existing meetings_enabled setting to 'true'")
        else:
            # Create new setting
            meetings_setting = SystemSetting(
                key='meetings_enabled',
                value='true',
                description='Enable or disable meeting requests functionality'
            )
            db.session.add(meetings_setting)
            print("Created new meetings_enabled setting with value 'true'")
        
        try:
            db.session.commit()
            print("✅ Meetings are now enabled!")
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error enabling meetings: {e}")

if __name__ == "__main__":
    enable_meetings()
