#!/usr/bin/env python3
"""
Initialize Meeting Metadata Settings

This script initializes the default meeting metadata settings in the system_settings table.
Run this script to set up the default meeting configuration for the event.
"""

import sys
import os
import json
from datetime import datetime

# Add the parent directory to the path to import the app
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app import create_app
from app.models import db, SystemSetting

def initialize_meeting_metadata():
    """Initialize default meeting metadata settings"""
    
    app = create_app()
    
    with app.app_context():
        try:
            print("Initializing meeting metadata settings...")
            
            # Check if meeting metadata already exists
            existing_keys = ['meeting_duration', 'meeting_interval', 'day_start_time', 'day_end_time', 'meeting_breaks']
            existing_settings = SystemSetting.query.filter(SystemSetting.key.in_(existing_keys)).all()
            
            if existing_settings:
                print(f"Found {len(existing_settings)} existing meeting metadata settings:")
                for setting in existing_settings:
                    print(f"  - {setting.key}: {setting.value}")
                
                response = input("Do you want to overwrite existing settings? (y/N): ")
                if response.lower() != 'y':
                    print("Aborted. No changes made.")
                    return
                
                # Delete existing settings
                for setting in existing_settings:
                    db.session.delete(setting)
                print("Deleted existing meeting metadata settings.")
            
            # Default meeting metadata
            default_breaks = [
                {
                    "id": 1,
                    "label": "Lunch Break",
                    "startTime": "12:00 PM",
                    "endTime": "1:00 PM"
                }
            ]
            
            default_metadata = [
                {
                    'key': 'meeting_duration',
                    'value': '10',
                    'description': 'Meeting duration in minutes'
                },
                {
                    'key': 'meeting_interval',
                    'value': '5',
                    'description': 'Interval between meeting slots in minutes'
                },
                {
                    'key': 'day_start_time',
                    'value': '9:00 AM',
                    'description': 'Day start time for meetings'
                },
                {
                    'key': 'day_end_time',
                    'value': '5:00 PM',
                    'description': 'Day end time for meetings'
                },
                {
                    'key': 'meeting_breaks',
                    'value': json.dumps(default_breaks),
                    'description': 'Meeting breaks configuration (JSON)'
                }
            ]
            
            # Create new settings
            for setting_data in default_metadata:
                setting = SystemSetting(
                    key=setting_data['key'],
                    value=setting_data['value'],
                    description=setting_data['description']
                )
                db.session.add(setting)
                print(f"Added setting: {setting_data['key']} = {setting_data['value']}")
            
            db.session.commit()
            
            print("\n✅ Meeting metadata initialized successfully!")
            print("\nDefault configuration:")
            print("  - Meeting Duration: 10 minutes")
            print("  - Interval Between Slots: 5 minutes")
            print("  - Day Start Time: 9:00 AM")
            print("  - Day End Time: 5:00 PM")
            print("  - Breaks: Lunch Break (12:00 PM - 1:00 PM)")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error initializing meeting metadata: {str(e)}")
            raise

def verify_meeting_metadata():
    """Verify that meeting metadata settings exist and display them"""
    
    app = create_app()
    
    with app.app_context():
        try:
            print("Verifying meeting metadata settings...")
            
            meeting_keys = ['meeting_duration', 'meeting_interval', 'day_start_time', 'day_end_time', 'meeting_breaks']
            settings = SystemSetting.query.filter(SystemSetting.key.in_(meeting_keys)).all()
            
            if not settings:
                print("❌ No meeting metadata settings found.")
                return False
            
            print(f"\n✅ Found {len(settings)} meeting metadata settings:")
            for setting in settings:
                if setting.key == 'meeting_breaks':
                    try:
                        breaks = json.loads(setting.value)
                        print(f"  - {setting.key}: {len(breaks)} break(s)")
                        for break_item in breaks:
                            print(f"    * {break_item['label']}: {break_item['startTime']} - {break_item['endTime']}")
                    except json.JSONDecodeError:
                        print(f"  - {setting.key}: Invalid JSON")
                else:
                    print(f"  - {setting.key}: {setting.value}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error verifying meeting metadata: {str(e)}")
            return False

def main():
    """Main function"""
    if len(sys.argv) > 1 and sys.argv[1] == 'verify':
        verify_meeting_metadata()
    else:
        initialize_meeting_metadata()

if __name__ == '__main__':
    main()
