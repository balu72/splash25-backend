from app import create_app
from app.models import db, User, UserRole

def add_users():
    app = create_app()
    
    with app.app_context():
        # Check if users already exist
        if User.query.filter_by(username='buyer').first():
            print("User 'buyer' already exists. Skipping...")
        else:
            buyer = User(
                username="buyer",
                email="buyer@example.com",
                password="buyer123",
                role=UserRole.BUYER
            )
            db.session.add(buyer)
            print("User 'buyer' created successfully")
        
        if User.query.filter_by(username='seller').first():
            print("User 'seller' already exists. Skipping...")
        else:
            seller = User(
                username="seller",
                email="seller@example.com",
                password="seller123",
                role=UserRole.SELLER,
                business_name="Test Business",
                business_description="A test business for the seller account",
                is_verified=True
            )
            db.session.add(seller)
            print("User 'seller' created successfully")
        
        db.session.commit()
        
        # Print all users
        users = User.query.all()
        print("\nAll users in the database:")
        for user in users:
            print(f"- {user.username} ({user.role.value})")

if __name__ == "__main__":
    add_users()
