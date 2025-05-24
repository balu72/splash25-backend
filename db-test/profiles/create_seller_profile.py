from app import create_app
from app.models import db, User, UserRole, SellerProfile

def create_seller_profile():
    app = create_app()
    with app.app_context():
        # Find the seller user
        seller = User.query.filter_by(username='seller_new').first()
        if seller:
            # Check if profile already exists
            profile = SellerProfile.query.filter_by(user_id=seller.id).first()
            if not profile:
                # Create seller profile
                profile = SellerProfile(
                    user_id=seller.id,
                    business_name='New Adventure Tours',
                    description='Providing exciting adventure tours in Wayanad with expert guides and safety equipment.',
                    seller_type='Tour Operator',
                    target_market='Domestic',
                    website='https://newadventuretours.com',
                    contact_email='info@newadventuretours.com',
                    contact_phone='+91 9876543210',
                    address='Kalpetta, Wayanad, Kerala',
                    is_verified=True
                )
                db.session.add(profile)
                db.session.commit()
                print('Seller profile created successfully!')
            else:
                print('Seller profile already exists.')
        else:
            print('Seller user not found.')

if __name__ == "__main__":
    create_seller_profile()
