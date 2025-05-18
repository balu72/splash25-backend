from app import create_app
from app.models import db, User, TravelPlan
from datetime import date

def create_travel_plan():
    """Create a travel plan for user1."""
    app = create_app()
    
    with app.app_context():
        # Find user1
        user = User.query.filter_by(username="user1").first()
        if not user:
            print("User 'user1' not found.")
            return
        
        # Check if user already has a travel plan
        existing_plan = TravelPlan.query.filter_by(user_id=user.id).first()
        if existing_plan:
            print("User 'user1' already has a travel plan.")
            return
        
        # Create travel plan
        travel_plan = TravelPlan(
            user_id=user.id,
            event_name="Splash25",
            event_start_date=date(2025, 5, 25),
            event_end_date=date(2025, 5, 28),
            venue="Wayanad Convention Center, Kerala, India",
            status="confirmed"
        )
        
        db.session.add(travel_plan)
        db.session.commit()
        
        print("Travel plan created successfully for user 'user1'!")

if __name__ == "__main__":
    create_travel_plan()
