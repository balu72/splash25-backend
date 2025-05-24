from app import create_app
from app.models import db, User, TravelPlan, Transportation, Accommodation, GroundTransportation
from datetime import datetime, timedelta

def create_travel_plan_data():
    """Create travel plan data for buyer_new user."""
    app = create_app()
    
    with app.app_context():
        # Find the buyer_new user
        buyer = User.query.filter_by(username="buyer_new").first()
        if not buyer:
            print("Buyer user 'buyer_new' not found. Please run add_buyer.py first.")
            return
        
        # Check if travel plan already exists
        existing_plan = TravelPlan.query.filter_by(user_id=buyer.id).first()
        if existing_plan:
            print("Travel plan for 'buyer_new' already exists.")
            return
        
        # Create travel plan with correct fields
        travel_plan = TravelPlan(
            user_id=buyer.id,
            event_name="Splash25 - Wayanad Tourism Event",
            event_start_date=(datetime.now() + timedelta(days=30)).date(),
            event_end_date=(datetime.now() + timedelta(days=33)).date(),
            venue="Wayanad, Kerala",
            status="confirmed"
        )
        
        db.session.add(travel_plan)
        db.session.flush()  # Get the travel_plan.id
        
        # Create transportation details
        transportation = Transportation(
            travel_plan_id=travel_plan.id,
            type="flight",
            # Outbound journey
            outbound_carrier="Air India",
            outbound_number="AI 644",
            outbound_departure_location="Mumbai (BOM)",
            outbound_departure_datetime=datetime.now() + timedelta(days=30, hours=14, minutes=30),
            outbound_arrival_location="Cochin International Airport (COK)",
            outbound_arrival_datetime=datetime.now() + timedelta(days=30, hours=16, minutes=45),
            outbound_booking_reference="AI644MUM",
            outbound_seat_info="14A",
            # Return journey
            return_carrier="Air India",
            return_number="AI 645",
            return_departure_location="Cochin International Airport (COK)",
            return_departure_datetime=datetime.now() + timedelta(days=33, hours=18, minutes=45),
            return_arrival_location="Mumbai (BOM)",
            return_arrival_datetime=datetime.now() + timedelta(days=33, hours=21, minutes=15),
            return_booking_reference="AI645COK",
            return_seat_info="12B"
        )
        
        db.session.add(transportation)
        
        # Create accommodation details
        accommodation = Accommodation(
            travel_plan_id=travel_plan.id,
            name="Grand Hyatt Kochi Bolgatty",
            address="Bolgatty Island, Mulavukad P.O, Kochi, Kerala 682504",
            check_in_datetime=datetime.now() + timedelta(days=30, hours=17, minutes=30),
            check_out_datetime=datetime.now() + timedelta(days=33, hours=12),
            room_type="Deluxe King Room",
            booking_reference="GH2025WAY001",
            special_notes="Late check-out requested. Vegetarian meals preferred."
        )
        
        db.session.add(accommodation)
        
        # Create ground transportation details
        ground_transportation = GroundTransportation(
            travel_plan_id=travel_plan.id,
            # Pickup details
            pickup_location="Cochin International Airport (COK)",
            pickup_datetime=datetime.now() + timedelta(days=30, hours=17),
            pickup_vehicle_type="Sedan",
            pickup_driver_contact="Ravi Kumar - +91 98765 43210",
            # Dropoff details
            dropoff_location="Grand Hyatt Kochi Bolgatty to Cochin International Airport (COK)",
            dropoff_datetime=datetime.now() + timedelta(days=33, hours=16),
            dropoff_vehicle_type="Sedan",
            dropoff_driver_contact="Ravi Kumar - +91 98765 43210"
        )
        
        db.session.add(ground_transportation)
        
        # Commit all changes
        db.session.commit()
        
        print("Travel plan data created successfully for 'buyer_new'!")
        print(f"Travel Plan ID: {travel_plan.id}")
        print(f"Event: {travel_plan.event_name}")
        print(f"Venue: {travel_plan.venue}")
        print(f"Dates: {travel_plan.event_start_date} to {travel_plan.event_end_date}")
        print("Transportation, accommodation, and ground transportation details added.")

if __name__ == "__main__":
    create_travel_plan_data()
