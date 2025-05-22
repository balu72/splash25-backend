from app import create_app
from app.models import db, User, UserRole, TravelPlan, Transportation, Accommodation, GroundTransportation, Meeting, MeetingStatus, Listing, ListingStatus, ListingDate, TimeSlot
from datetime import datetime, timedelta, date

def init_db():
    """Initialize the database with sample data."""
    app = create_app()
    
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Check if users already exist
        if User.query.count() > 0:
            print("Database already initialized. Skipping...")
            return
        
        print("Initializing database with sample data...")
        
        # Create users
        admin = User(
            username="admin",
            email="admin@splash25.com",
            password="password123",
            role=UserRole.ADMIN
        )
        
        buyer1 = User(
            username="john_doe",
            email="john@example.com",
            password="password123",
            role=UserRole.BUYER
        )
        
        buyer2 = User(
            username="jane_smith",
            email="jane@example.com",
            password="password123",
            role=UserRole.BUYER
        )
        
        seller1 = User(
            username="rahul_sharma",
            email="rahul@wayanadadventures.com",
            password="password123",
            role=UserRole.SELLER,
            business_name="Wayanad Adventures",
            business_description="Specialized in wildlife tours and nature experiences",
            is_verified=True
        )
        
        seller2 = User(
            username="priya_nair",
            email="priya@keralatrekking.com",
            password="password123",
            role=UserRole.SELLER,
            business_name="Kerala Trekking Co.",
            business_description="Expert trekking guides for all major peaks in Kerala",
            is_verified=True
        )
        
        db.session.add_all([admin, buyer1, buyer2, seller1, seller2])
        db.session.commit()
        
        # Create travel plans
        travel_plan1 = TravelPlan(
            user_id=buyer1.id,
            event_name="Splash25",
            event_start_date=date(2025, 5, 25),
            event_end_date=date(2025, 5, 28),
            venue="Wayanad Convention Center, Kerala, India",
            status="confirmed"
        )
        
        travel_plan2 = TravelPlan(
            user_id=seller1.id,
            event_name="Splash25",
            event_start_date=date(2025, 5, 25),
            event_end_date=date(2025, 5, 28),
            venue="Wayanad Convention Center, Kerala, India",
            status="confirmed"
        )
        
        db.session.add_all([travel_plan1, travel_plan2])
        db.session.commit()
        
        # Create transportation details
        transportation1 = Transportation(
            travel_plan_id=travel_plan1.id,
            type="flight",
            outbound_carrier="Air India",
            outbound_number="AI-462",
            outbound_departure_location="Bengaluru International Airport (BLR)",
            outbound_departure_datetime=datetime(2025, 5, 24, 10, 30),
            outbound_arrival_location="Calicut International Airport (CCJ)",
            outbound_arrival_datetime=datetime(2025, 5, 24, 11, 45),
            outbound_booking_reference="AIBNG24587",
            outbound_seat_info="14A (Window)",
            return_carrier="Air India",
            return_number="AI-475",
            return_departure_location="Calicut International Airport (CCJ)",
            return_departure_datetime=datetime(2025, 5, 29, 16, 15),
            return_arrival_location="Bengaluru International Airport (BLR)",
            return_arrival_datetime=datetime(2025, 5, 29, 17, 30),
            return_booking_reference="AIBNG24587",
            return_seat_info="12C (Aisle)"
        )
        
        transportation2 = Transportation(
            travel_plan_id=travel_plan2.id,
            type="flight",
            outbound_carrier="Air India",
            outbound_number="AI-462",
            outbound_departure_location="Bengaluru International Airport (BLR)",
            outbound_departure_datetime=datetime(2025, 5, 24, 10, 30),
            outbound_arrival_location="Calicut International Airport (CCJ)",
            outbound_arrival_datetime=datetime(2025, 5, 24, 11, 45),
            outbound_booking_reference="AIBNG24587",
            outbound_seat_info="14A (Window)",
            return_carrier="Air India",
            return_number="AI-475",
            return_departure_location="Calicut International Airport (CCJ)",
            return_departure_datetime=datetime(2025, 5, 29, 16, 15),
            return_arrival_location="Bengaluru International Airport (BLR)",
            return_arrival_datetime=datetime(2025, 5, 29, 17, 30),
            return_booking_reference="AIBNG24587",
            return_seat_info="12C (Aisle)"
        )
        
        db.session.add_all([transportation1, transportation2])
        db.session.commit()
        
        # Create accommodation details
        accommodation1 = Accommodation(
            travel_plan_id=travel_plan1.id,
            name="Wayanad Blooms Resort",
            address="123 Forest Road, Kalpetta, Wayanad, Kerala 673121",
            check_in_datetime=datetime(2025, 5, 24, 14, 0),
            check_out_datetime=datetime(2025, 5, 29, 11, 0),
            room_type="Deluxe Room with Forest View",
            booking_reference="WBR25052405",
            special_notes="Late check-in arranged. Breakfast included."
        )
        
        accommodation2 = Accommodation(
            travel_plan_id=travel_plan2.id,
            name="Wayanad Blooms Resort",
            address="123 Forest Road, Kalpetta, Wayanad, Kerala 673121",
            check_in_datetime=datetime(2025, 5, 24, 14, 0),
            check_out_datetime=datetime(2025, 5, 29, 11, 0),
            room_type="Deluxe Room with Forest View",
            booking_reference="WBR25052405",
            special_notes="Late check-in arranged. Breakfast included."
        )
        
        db.session.add_all([accommodation1, accommodation2])
        db.session.commit()
        
        # Create ground transportation details
        ground_transportation1 = GroundTransportation(
            travel_plan_id=travel_plan1.id,
            pickup_location="Calicut International Airport (CCJ)",
            pickup_datetime=datetime(2025, 5, 24, 12, 0),
            pickup_vehicle_type="SUV",
            pickup_driver_contact="+91 9876543210",
            dropoff_location="Calicut International Airport (CCJ)",
            dropoff_datetime=datetime(2025, 5, 29, 13, 30),
            dropoff_vehicle_type="SUV",
            dropoff_driver_contact="+91 9876543210"
        )
        
        ground_transportation2 = GroundTransportation(
            travel_plan_id=travel_plan2.id,
            pickup_location="Calicut International Airport (CCJ)",
            pickup_datetime=datetime(2025, 5, 24, 12, 0),
            pickup_vehicle_type="SUV",
            pickup_driver_contact="+91 9876543210",
            dropoff_location="Calicut International Airport (CCJ)",
            dropoff_datetime=datetime(2025, 5, 29, 13, 30),
            dropoff_vehicle_type="SUV",
            dropoff_driver_contact="+91 9876543210"
        )
        
        db.session.add_all([ground_transportation1, ground_transportation2])
        db.session.commit()
        
        # Create meetings
        meeting1 = Meeting(
            buyer_id=buyer1.id,
            seller_id=seller1.id,
            from_time=datetime(2025, 5, 26, 10, 0),
            to_time=datetime(2025, 5, 26, 10, 30),
            topic="Wildlife Sanctuary Tour Planning",
            status=MeetingStatus.CONFIRMED
        )
        
        meeting2 = Meeting(
            buyer_id=buyer1.id,
            seller_id=seller2.id,
            from_time=datetime(2025, 5, 27, 14, 30),
            to_time=datetime(2025, 5, 27, 15, 0),
            topic="Chembra Peak Trek Preparation",
            status=MeetingStatus.REQUESTED
        )
        
        meeting3 = Meeting(
            buyer_id=buyer2.id,
            seller_id=seller1.id,
            from_time=datetime(2025, 5, 28, 9, 15),
            to_time=datetime(2025, 5, 28, 9, 45),
            topic="Historical Sites Tour Discussion",
            status=MeetingStatus.COMPLETED
        )
        
        meeting4 = Meeting(
            buyer_id=buyer2.id,
            seller_id=seller2.id,
            from_time=datetime(2025, 5, 28, 11, 0),
            to_time=datetime(2025, 5, 28, 11, 30),
            topic="Spice Plantation Tour Planning",
            status=MeetingStatus.CANCELLED
        )
        
        db.session.add_all([meeting1, meeting2, meeting3, meeting4])
        db.session.commit()
        
        # Create listings
        listing1 = Listing(
            seller_id=seller1.id,
            name="Wayanad Nature Camp",
            description="Experience the rich biodiversity of Wayanad with our expert guides",
            price=2500,
            duration="2 days",
            location="Muthanga Wildlife Sanctuary",
            max_participants=20,
            status=ListingStatus.ACTIVE,
            image_url="/images/listings/nature-camp.jpg",
            views=450,
            bookings=12
        )
        
        listing2 = Listing(
            seller_id=seller1.id,
            name="Splash25 Trekking Adventure",
            description="Trek to the heart-shaped lake at the summit of Chembra Peak",
            price=1800,
            duration="1 day",
            location="Chembra Peak",
            max_participants=15,
            status=ListingStatus.ACTIVE,
            image_url="/images/listings/trekking-adventure.jpg",
            views=320,
            bookings=8
        )
        
        listing3 = Listing(
            seller_id=seller2.id,
            name="Cultural Heritage Tour",
            description="Explore the rich cultural heritage of Wayanad",
            price=1500,
            duration="1 day",
            location="Various locations in Wayanad",
            max_participants=25,
            status=ListingStatus.ACTIVE,
            image_url="/images/listings/heritage-tour.jpg",
            views=280,
            bookings=5
        )
        
        db.session.add_all([listing1, listing2, listing3])
        db.session.commit()
        
        # Create listing dates
        today = date.today()
        for i in range(10):
            listing_date1 = ListingDate(
                listing_id=listing1.id,
                date=today + timedelta(days=i*7)
            )
            listing_date2 = ListingDate(
                listing_id=listing2.id,
                date=today + timedelta(days=i*7+1)
            )
            listing_date3 = ListingDate(
                listing_id=listing3.id,
                date=today + timedelta(days=i*7+2)
            )
            db.session.add_all([listing_date1, listing_date2, listing_date3])
        
        db.session.commit()
        
        print("Database initialized successfully!")

if __name__ == "__main__":
    init_db()
