"""
Test configuration and fixtures for Splash25 API tests
"""
import pytest
import os
from flask import Flask
from app import create_app
from app.models import db, User, UserRole, BuyerProfile, SellerProfile


@pytest.fixture(scope='session')
def app():
    """Create application for the tests."""
    # Use the existing test database
    test_config = {
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': os.getenv('DATABASE_URI', 'postgresql://splash25user:splash25pass@localhost:5433/test_migration_db'),
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'JWT_SECRET_KEY': 'test-secret-key',
        'WTF_CSRF_ENABLED': False
    }
    
    app = create_app()
    app.config.update(test_config)
    
    with app.app_context():
        # Don't create tables - use existing enhanced database
        # Just ensure we have some test users
        ensure_test_users()
        
        yield app
        
        # Cleanup - just remove session, don't drop tables
        db.session.remove()


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()


def ensure_test_users():
    """Ensure test users exist in the database."""
    # Check if test users already exist
    admin_user = User.query.filter_by(username='test_admin').first()
    if not admin_user:
        admin_user = User(
            username='test_admin',
            email='admin@test.com',
            password='admin123',
            role=UserRole.ADMIN
        )
        db.session.add(admin_user)
    
    buyer_user = User.query.filter_by(username='test_buyer').first()
    if not buyer_user:
        buyer_user = User(
            username='test_buyer',
            email='buyer@test.com',
            password='buyer123',
            role=UserRole.BUYER
        )
        db.session.add(buyer_user)
    
    seller_user = User.query.filter_by(username='test_seller').first()
    if not seller_user:
        seller_user = User(
            username='test_seller',
            email='seller@test.com',
            password='seller123',
            role=UserRole.SELLER,
            business_name='Test Resort',
            business_description='A test resort for testing'
        )
        db.session.add(seller_user)
    
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Warning: Could not create test users: {e}")


# Authentication helpers
@pytest.fixture
def admin_token(client):
    """Get admin authentication token."""
    response = client.post('/api/auth/login', json={
        'username': 'test_admin',
        'password': 'admin123'
    })
    if response.status_code == 200:
        return response.json['access_token']
    else:
        # If test admin doesn't exist, try with existing admin
        # Check if there are any existing admin users
        return None


@pytest.fixture
def buyer_token(client):
    """Get buyer authentication token."""
    response = client.post('/api/auth/login', json={
        'username': 'test_buyer',
        'password': 'buyer123'
    })
    if response.status_code == 200:
        return response.json['access_token']
    else:
        return None


@pytest.fixture
def seller_token(client):
    """Get seller authentication token."""
    response = client.post('/api/auth/login', json={
        'username': 'test_seller',
        'password': 'seller123'
    })
    if response.status_code == 200:
        return response.json['access_token']
    else:
        return None


@pytest.fixture
def auth_headers():
    """Helper function to create authorization headers."""
    def _auth_headers(token):
        return {'Authorization': f'Bearer {token}'}
    return _auth_headers
