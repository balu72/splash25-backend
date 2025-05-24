from app import create_app
from app.models import db, User, UserRole, Stall, SellerProfile

def create_stall_data():
    app = create_app()
    with app.app_context():
        # Find the seller user
        seller = User.query.filter_by(username='seller_new').first()
        if seller:
            # Check if seller has a profile
            seller_profile = SellerProfile.query.filter_by(user_id=seller.id).first()
            if not seller_profile:
                print('Seller profile not found. Please create seller profile first.')
                return
            
            # Create sample stalls
            sample_stalls = [
                {
                    'number': 'S001',
                    'stall_type': 'Standard',
                    'price': 25000.0,
                    'size': '3m X 3m',
                    'allowed_attendees': 2,
                    'max_meetings_per_attendee': 8,
                    'min_meetings_per_attendee': 4,
                    'inclusions': 'Table, 2 chairs, power outlet, WiFi, welcome kit'
                },
                {
                    'number': 'S002',
                    'stall_type': 'Premium',
                    'price': 45000.0,
                    'size': '4m X 4m',
                    'allowed_attendees': 3,
                    'max_meetings_per_attendee': 12,
                    'min_meetings_per_attendee': 6,
                    'inclusions': 'Large table, 4 chairs, power outlets, WiFi, welcome kit, refreshments, branding space'
                },
                {
                    'number': 'S003',
                    'stall_type': 'Executive',
                    'price': 75000.0,
                    'size': '5m X 5m',
                    'allowed_attendees': 5,
                    'max_meetings_per_attendee': 15,
                    'min_meetings_per_attendee': 8,
                    'inclusions': 'Executive table, 6 chairs, multiple power outlets, premium WiFi, welcome kit, refreshments, large branding space, storage area'
                }
            ]
            
            for stall_data in sample_stalls:
                # Check if stall already exists
                existing_stall = Stall.query.filter_by(
                    seller_id=seller.id,
                    number=stall_data['number']
                ).first()
                
                if not existing_stall:
                    stall = Stall(
                        seller_id=seller.id,
                        **stall_data
                    )
                    db.session.add(stall)
                    print(f"Created stall: {stall_data['number']}")
                else:
                    print(f"Stall {stall_data['number']} already exists.")
            
            db.session.commit()
            print('Sample stall data created successfully!')
        else:
            print('Seller user not found.')

if __name__ == "__main__":
    create_stall_data()
