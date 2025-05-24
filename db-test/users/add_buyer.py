from app import create_app
from app.models import db, User, UserRole

def add_buyer():
    """Add a buyer user with a known password."""
    app = create_app()
    
    with app.app_context():
        # Check if buyer already exists
        buyer = User.query.filter_by(username="buyer_new").first()
        if buyer:
            print("Buyer user 'buyer_new' already exists.")
            return
        
        # Create buyer user
        buyer = User(
            username="buyer_new",
            email="buyer_new@example.com",
            password="buyer123",
            role=UserRole.BUYER
        )
        
        db.session.add(buyer)
        db.session.commit()
        
        print("Buyer user 'buyer_new' created successfully!")
        print("Username: buyer_new")
        print("Password: buyer123")

if __name__ == "__main__":
    add_buyer()
