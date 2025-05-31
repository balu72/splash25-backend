#!/usr/bin/env python3
"""
Script to create test time slots for sellers to test the meeting request functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.models import db, User, TimeSlot, UserRole
from datetime import datetime, timedelta

def create_test_timeslots():
    """Create test time slots for all sellers"""
    app = create_app()
    
    with app.app_context():
        # Get all sellers
        sellers = User.query.filter_by(role=UserRole.SELLER.value).all()
        
        if not sellers:
            print("No sellers found in the database!")
            return
        
        print(f"Found {len(sellers)} sellers. Creating time slots...")
        
        # Create time slots for the next 7 days
        start_date = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
        
        total_slots_created = 0
        
        for seller in sellers:
            print(f"Creating time slots for seller: {seller.username} (ID: {seller.id})")
            
            seller_slots_created = 0
            current_date = start_date
            
            # Create slots for 7 days
            for day in range(7):
                day_date = current_date + timedelta(days=day)
                
                # Skip weekends for this example
                if day_date.weekday() >= 5:  # Saturday = 5, Sunday = 6
                    continue
                
                # Create slots from 9 AM to 5 PM (every 30 minutes)
                for hour in range(9, 17):  # 9 AM to 5 PM
                    for minute in [0, 30]:  # Every 30 minutes
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
                            seller_slots_created += 1
            
            print(f"  Created {seller_slots_created} time slots for {seller.username}")
            total_slots_created += seller_slots_created
        
        # Commit all changes
        try:
            db.session.commit()
            print(f"\n✅ Successfully created {total_slots_created} time slots for {len(sellers)} sellers!")
            print("Time slots are available from 9 AM to 5 PM (weekdays only) for the next 7 days.")
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error creating time slots: {e}")

if __name__ == "__main__":
    create_test_timeslots()
