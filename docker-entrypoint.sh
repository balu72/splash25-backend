#!/bin/sh

# Exit on any error
set -e

echo "Starting Splash25 Backend..."

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to be ready..."
while ! pg_isready -h ${DB_HOST:-postgres} -p ${DB_PORT:-5432} -U ${DB_USER:-splash25user}; do
  echo "PostgreSQL is unavailable - sleeping"
  sleep 2
done

echo "PostgreSQL is ready!"

# Run database migrations if needed
echo "Running database setup..."
python -c "
from app import create_app
from app.models import db
app = create_app()
with app.app_context():
    db.create_all()
    print('Database tables created/verified')
"

# Initialize default users if needed
echo "Setting up default users..."
python -c "
from app import create_app
from app.models import db, User, UserRole
app = create_app()
with app.app_context():
    # Check if admin user exists
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(
            username='admin',
            email='admin@splash25.com',
            password='admin123',
            role=UserRole.ADMIN
        )
        db.session.add(admin)
        print('Created admin user')
    
    # Check if test buyer exists
    buyer = User.query.filter_by(username='buyer').first()
    if not buyer:
        buyer = User(
            username='buyer',
            email='buyer@example.com',
            password='buyer123',
            role=UserRole.BUYER
        )
        db.session.add(buyer)
        print('Created test buyer user')
    
    # Check if test seller exists
    seller = User.query.filter_by(username='seller').first()
    if not seller:
        seller = User(
            username='seller',
            email='seller@example.com',
            password='seller123',
            role=UserRole.SELLER
        )
        db.session.add(seller)
        print('Created test seller user')
    
    db.session.commit()
    print('Default users setup complete')
"

echo "Database setup complete!"

# Execute the main command
echo "Starting Flask application..."
exec "$@"
