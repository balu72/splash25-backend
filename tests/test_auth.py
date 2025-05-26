"""
Authentication API tests
"""
import pytest
from app.models import User, UserRole


@pytest.mark.auth
class TestAuthenticationAPI:
    """Test authentication endpoints"""
    
    def test_login_success(self, client):
        """Test successful login"""
        response = client.post('/api/auth/login', json={
            'username': 'test_buyer',
            'password': 'buyer123'
        })
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'access_token' in data
        assert 'refresh_token' in data
        assert 'user' in data
        assert data['user']['username'] == 'test_buyer'
        assert data['user']['role'] == 'buyer'
    
    def test_login_invalid_credentials(self, client):
        """Test login with invalid credentials"""
        response = client.post('/api/auth/login', json={
            'username': 'test_buyer',
            'password': 'wrong_password'
        })
        
        assert response.status_code == 401
        data = response.get_json()
        assert 'error' in data
        assert 'Invalid username or password' in data['error']
    
    def test_login_missing_fields(self, client):
        """Test login with missing fields"""
        response = client.post('/api/auth/login', json={
            'username': 'test_buyer'
        })
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'Username and password are required' in data['error']
    
    def test_register_buyer_success(self, client):
        """Test successful buyer registration"""
        response = client.post('/api/auth/register', json={
            'username': 'new_buyer',
            'email': 'newbuyer@test.com',
            'password': 'password123',
            'role': 'buyer'
        })
        
        assert response.status_code == 201
        data = response.get_json()
        assert 'message' in data
        assert 'user' in data
        assert data['user']['username'] == 'new_buyer'
        assert data['user']['role'] == 'buyer'
    
    def test_register_seller_success(self, client):
        """Test successful seller registration"""
        response = client.post('/api/auth/register', json={
            'username': 'new_seller',
            'email': 'newseller@test.com',
            'password': 'password123',
            'role': 'seller',
            'business_name': 'New Resort'
        })
        
        assert response.status_code == 201
        data = response.get_json()
        assert 'message' in data
        assert 'user' in data
        assert data['user']['username'] == 'new_seller'
        assert data['user']['role'] == 'seller'
    
    def test_register_seller_missing_business_name(self, client):
        """Test seller registration without business name"""
        response = client.post('/api/auth/register', json={
            'username': 'new_seller2',
            'email': 'newseller2@test.com',
            'password': 'password123',
            'role': 'seller'
        })
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'Business name is required for sellers' in data['error']
    
    def test_register_duplicate_username(self, client):
        """Test registration with duplicate username"""
        response = client.post('/api/auth/register', json={
            'username': 'test_buyer',
            'email': 'duplicate@test.com',
            'password': 'password123',
            'role': 'buyer'
        })
        
        assert response.status_code == 409
        data = response.get_json()
        assert 'error' in data
        assert 'Username already exists' in data['error']
    
    def test_register_duplicate_email(self, client):
        """Test registration with duplicate email"""
        response = client.post('/api/auth/register', json={
            'username': 'duplicate_user',
            'email': 'buyer@test.com',
            'password': 'password123',
            'role': 'buyer'
        })
        
        assert response.status_code == 409
        data = response.get_json()
        assert 'error' in data
        assert 'Email already exists' in data['error']
    
    def test_register_admin_forbidden(self, client):
        """Test that admin registration is forbidden"""
        response = client.post('/api/auth/register', json={
            'username': 'new_admin',
            'email': 'newadmin@test.com',
            'password': 'password123',
            'role': 'admin'
        })
        
        assert response.status_code == 403
        data = response.get_json()
        assert 'error' in data
        assert 'Cannot register as admin' in data['error']
    
    def test_register_invalid_role(self, client):
        """Test registration with invalid role"""
        response = client.post('/api/auth/register', json={
            'username': 'invalid_role_user',
            'email': 'invalid@test.com',
            'password': 'password123',
            'role': 'invalid_role'
        })
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'Invalid role' in data['error']
    
    def test_get_current_user(self, client, buyer_token, auth_headers):
        """Test getting current user information"""
        response = client.get('/api/auth/me', 
                            headers=auth_headers(buyer_token))
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['username'] == 'test_buyer'
        assert data['role'] == 'buyer'
        assert data['email'] == 'buyer@test.com'
    
    def test_get_current_user_unauthorized(self, client):
        """Test getting current user without token"""
        response = client.get('/api/auth/me')
        
        assert response.status_code == 401
    
    def test_refresh_token(self, client, buyer_token):
        """Test token refresh"""
        # First login to get refresh token
        login_response = client.post('/api/auth/login', json={
            'username': 'test_buyer',
            'password': 'buyer123'
        })
        refresh_token = login_response.get_json()['refresh_token']
        
        # Use refresh token to get new access token
        response = client.post('/api/auth/refresh',
                             headers={'Authorization': f'Bearer {refresh_token}'})
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'access_token' in data
        assert 'user' in data
    
    def test_logout(self, client, buyer_token, auth_headers):
        """Test logout functionality"""
        response = client.post('/api/auth/logout',
                             headers=auth_headers(buyer_token))
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'message' in data
        assert 'Successfully logged out' in data['message']
    
    def test_logout_unauthorized(self, client):
        """Test logout without token"""
        response = client.post('/api/auth/logout')
        
        assert response.status_code == 401


@pytest.mark.auth
class TestRoleBasedAccess:
    """Test role-based access control"""
    
    def test_admin_access_admin_endpoint(self, client, admin_token, auth_headers):
        """Test admin can access admin endpoints"""
        response = client.get('/api/admin/dashboard',
                            headers=auth_headers(admin_token))
        
        assert response.status_code == 200
    
    def test_buyer_cannot_access_admin_endpoint(self, client, buyer_token, auth_headers):
        """Test buyer cannot access admin endpoints"""
        response = client.get('/api/admin/dashboard',
                            headers=auth_headers(buyer_token))
        
        assert response.status_code == 403
    
    def test_seller_cannot_access_admin_endpoint(self, client, seller_token, auth_headers):
        """Test seller cannot access admin endpoints"""
        response = client.get('/api/admin/dashboard',
                            headers=auth_headers(seller_token))
        
        assert response.status_code == 403
    
    def test_buyer_access_buyer_endpoint(self, client, buyer_token, auth_headers):
        """Test buyer can access buyer endpoints"""
        response = client.get('/api/buyer/dashboard',
                            headers=auth_headers(buyer_token))
        
        assert response.status_code == 200
    
    def test_seller_cannot_access_buyer_endpoint(self, client, seller_token, auth_headers):
        """Test seller cannot access buyer endpoints"""
        response = client.get('/api/buyer/dashboard',
                            headers=auth_headers(seller_token))
        
        assert response.status_code == 403
