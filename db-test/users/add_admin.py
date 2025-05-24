from app import create_app
from app.models import db, User, UserRole

def add_admin():
    """Add an admin user with a known password."""
    app = create_app()
    
    with app.app_context():
        # Check if admin already exists
        admin = User.query.filter_by(username="admin_new").first()
        if admin:
            print("Admin user 'admin_new' already exists.")
            return
        
        # Create admin user
        admin = User(
            username="admin_new",
            email="admin_new@splash25.com",
            password="admin123",
            role=UserRole.ADMIN
        )
        
        db.session.add(admin)
        db.session.commit()
        
        print("Admin user 'admin_new' created successfully!")
        print("Username: admin_new")
        print("Password: admin123")

if __name__ == "__main__":
    add_admin()
