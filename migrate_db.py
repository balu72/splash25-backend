from app import create_app
from app.models import db

def migrate_db():
    """Create all tables in the database."""
    app = create_app()
    
    with app.app_context():
        # Create all tables
        db.create_all()
        print("Database schema updated successfully.")

if __name__ == "__main__":
    migrate_db()
