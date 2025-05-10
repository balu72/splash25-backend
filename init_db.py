from app import create_app
from app.models import db, User, UserRole

def init_db():
    """Initialize the database with test users."""
    app = create_app()
    
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        
        # Check if we already have users
        if User.query.count() > 0:
            print("Database already contains users. Skipping initialization.")
            return
        
        # Create test users
        test_users = [
            # Admin user
            User(
                username="admin",
                email="admin@splash25.com",
                password="admin123",
                role=UserRole.ADMIN
            ),
            
            # Seller user
            User(
                username="seller",
                email="seller@example.com",
                password="seller123",
                role=UserRole.SELLER,
                business_name="Wayanad Adventures",
                business_description="Providing authentic experiences in the heart of Wayanad",
                is_verified=True
            ),
            
            # Buyer user
            User(
                username="buyer",
                email="buyer@example.com",
                password="buyer123",
                role=UserRole.BUYER
            )
        ]
        
        # Add users to the database
        for user in test_users:
            db.session.add(user)
        
        # Commit the changes
        db.session.commit()
        
        print(f"Database initialized with {len(test_users)} test users:")
        print("- Admin: username='admin', password='admin123'")
        print("- Seller: username='seller', password='seller123'")
        print("- Buyer: username='buyer', password='buyer123'")

if __name__ == "__main__":
    init_db()
