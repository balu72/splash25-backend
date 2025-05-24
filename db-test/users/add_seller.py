from app import create_app
from app.models import db, User, UserRole

def add_seller():
    """Add a seller user with a known password."""
    app = create_app()
    
    with app.app_context():
        # Check if seller already exists
        seller = User.query.filter_by(username="seller_new").first()
        if seller:
            print("Seller user 'seller_new' already exists.")
            return
        
        # Create seller user
        seller = User(
            username="seller_new",
            email="seller_new@example.com",
            password="seller123",
            role=UserRole.SELLER,
            business_name="New Adventure Tours",
            business_description="Providing exciting adventure tours in Wayanad",
            is_verified=True
        )
        
        db.session.add(seller)
        db.session.commit()
        
        print("Seller user 'seller_new' created successfully!")
        print("Username: seller_new")
        print("Password: seller123")

if __name__ == "__main__":
    add_seller()
