#!/usr/bin/env python3
"""
Complete Meeting System Setup Script

This script will:
1. Enable meetings in system settings
2. Create time slots for all sellers
3. Create sample meetings for testing
4. Initialize meeting metadata
"""

import sys
import os
import json
from datetime import datetime, timedelta

# Add the app directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models import db, User, TimeSlot, Meeting, SystemSetting, UserRole, MeetingStatus

def enable_meetings():
    """Enable meetings in system settings"""
    print("1. Enabling meetings...")
    
    # Check if meetings_enabled setting exists
    meetings_setting = SystemSetting.query.filter_by(key='meetings_enabled').first()
    
    if meetings_setting:
        meetings_setting.value = 'true'
        print("   ✅ Updated existing meetings_enabled setting to 'true'")
    else:
        # Create new setting
        meetings_setting = SystemSetting(
            key='meetings_enabled',
            value='true',
            description='Enable or disable meeting requests functionality'
        )
        db.session.add(meetings_setting)
        print("   ✅ Created new meetings_enabled setting with value 'true'")

def initialize_meeting_metadata():
    """Initialize meeting metadata settings"""
    print("2. Initializing meeting metadata...")
    
    # Default meeting metadata
    default_breaks = [
        {
            "id": 1,
            "label": "Lunch Break",
            "startTime": "12:00 PM",
            "endTime": "1:00 PM"
        }
    ]
    
    metadata_settings = [
        {
            'key': 'meeting_duration',
            'value': '30',
            'description': 'Meeting duration in minutes'
        },
        {
            'key': 'meeting_interval',
            'value': '0',
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
    
    for setting_data in metadata_settings:
        existing_setting = SystemSetting.query.filter_by(key=setting_data['key']).first()
        if existing_setting:
            existing_setting.value = setting_data['value']
            existing_setting.description = setting_data['description']
        else:
            setting = SystemSetting(
                key=setting_data['key'],
                value=setting_data['value'],
                description=setting_data['description']
            )
            db.session.add(setting)
        print(f"   ✅ Set {setting_data['key']} = {setting_data['value']}")

def create_time_slots():
    """Create time slots for all sellers"""
    print("3. Creating time slots for sellers...")
    
    # Get all sellers
    sellers = User.query.filter_by(role=UserRole.SELLER.value).all()
    
    if not sellers:
        print("   ⚠️  No sellers found in the database!")
        return []
    
    print(f"   Found {len(sellers)} sellers")
    
    # Create time slots for the next 14 days
    start_date = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
    
    total_slots_created = 0
    all_time_slots = []
    
    for seller in sellers:
        print(f"   Creating time slots for: {seller.username}")
        
        seller_slots_created = 0
        current_date = start_date
        
        # Create slots for 14 days
        for day in range(14):
            day_date = current_date + timedelta(days=day)
            
            # Skip weekends
            if day_date.weekday() >= 5:  # Saturday = 5, Sunday = 6
                continue
            
            # Create slots from 9 AM to 5 PM (every 30 minutes)
            for hour in range(9, 17):  # 9 AM to 5 PM
                for minute in [0, 30]:  # Every 30 minutes
                    # Skip lunch break (12:00 PM - 1:00 PM)
                    if hour == 12:
                        continue
                    
                    slot_start = day_date.replace(hour=hour, minute=minute)
                    slot_end = slot_start + timedelta(minutes=30)
                    
                    # Check if slot already exists
                    existing_slot = TimeSlot.query.filter_by(
                        user_id=seller.id,
                        start_time=slot_start,
                        end_time=slot_end
                    ).first()
                    
                    if not existing_slot:
                        # Create the time slot
                        time_slot = TimeSlot(
                            user_id=seller.id,
                            start_time=slot_start,
                            end_time=slot_end,
                            is_available=True
                        )
                        db.session.add(time_slot)
                        all_time_slots.append(time_slot)
                        seller_slots_created += 1
        
        print(f"     ✅ Created {seller_slots_created} time slots")
        total_slots_created += seller_slots_created
    
    print(f"   ✅ Total time slots created: {total_slots_created}")
    return all_time_slots

def create_sample_meetings():
    """Create sample meetings for testing"""
    print("4. Creating sample meetings...")
    
    # Get buyers and sellers
    buyers = User.query.filter_by(role=UserRole.BUYER.value).limit(5).all()
    sellers = User.query.filter_by(role=UserRole.SELLER.value).limit(5).all()
    
    if not buyers or not sellers:
        print("   ⚠️  Need both buyers and sellers to create sample meetings")
        return
    
    meetings_created = 0
    
    # Create a few sample meetings with different statuses
    for i, buyer in enumerate(buyers[:3]):  # Use first 3 buyers
        for j, seller in enumerate(sellers[:2]):  # Use first 2 sellers
            # Get available time slots for this seller
            available_slots = TimeSlot.query.filter_by(
                user_id=seller.id,
                is_available=True
            ).limit(2).all()
            
            if available_slots:
                for k, time_slot in enumerate(available_slots):
                    # Create meeting with different statuses
                    if meetings_created % 3 == 0:
                        status = MeetingStatus.PENDING
                    elif meetings_created % 3 == 1:
                        status = MeetingStatus.ACCEPTED
                    else:
                        status = MeetingStatus.COMPLETED
                    
                    meeting = Meeting(
                        buyer_id=buyer.id,
                        seller_id=seller.id,
                        time_slot_id=time_slot.id,
                        notes=f"Sample meeting between {buyer.username} and {seller.username}",
                        status=status
                    )
                    
                    # If meeting is not pending, mark time slot as unavailable
                    if status != MeetingStatus.PENDING:
                        time_slot.is_available = False
                        time_slot.meeting_id = meeting.id
                    
                    db.session.add(meeting)
                    meetings_created += 1
                    
                    print(f"   ✅ Created {status.value} meeting: {buyer.username} → {seller.username}")
                    
                    # Limit to 2 meetings per buyer-seller pair
                    if k >= 1:
                        break
    
    print(f"   ✅ Total sample meetings created: {meetings_created}")

def main():
    """Main setup function"""
    print("🚀 Setting up Meeting System for Splash25")
    print("=" * 50)
    
    app = create_app()
    
    with app.app_context():
        try:
            # Step 1: Enable meetings
            enable_meetings()
            
            # Step 2: Initialize meeting metadata
            initialize_meeting_metadata()
            
            # Step 3: Create time slots
            create_time_slots()
            
            # Step 4: Create sample meetings
            create_sample_meetings()
            
            # Commit all changes
            db.session.commit()
            
            print("\n" + "=" * 50)
            print("✅ Meeting system setup completed successfully!")
            print("\nWhat was set up:")
            print("• Meetings enabled in system settings")
            print("• Meeting metadata configured (30-min slots, 9 AM - 5 PM)")
            print("• Time slots created for all sellers (next 14 days, weekdays only)")
            print("• Sample meetings created for testing")
            print("\nYou can now:")
            print("• Log in as a buyer to see sellers and request meetings")
            print("• Log in as a seller to see meeting requests and manage time slots")
            print("• Use the admin panel to manage meeting settings")
            
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ Error setting up meeting system: {str(e)}")
            raise

if __name__ == "__main__":
    main()
