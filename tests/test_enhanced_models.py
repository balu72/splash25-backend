"""
Enhanced models API tests - Testing new database features
"""
import pytest
from app.models import BuyerCategory, PropertyType, Interest, StallType, BuyerProfile, SellerProfile


@pytest.mark.enhanced
class TestEnhancedModelsAPI:
    """Test enhanced model functionality with new database features"""
    
    def test_buyer_profile_enhanced_fields(self, client, buyer_token, auth_headers):
        """Test buyer profile with enhanced fields"""
        response = client.get('/api/buyer/profile',
                            headers=auth_headers(buyer_token))
        
        assert response.status_code == 200
        data = response.get_json()
        profile = data['profile']
        
        # Test enhanced fields are present
        assert 'category' in profile
        assert 'salutation' in profile
        assert 'first_name' in profile
        assert 'last_name' in profile
        assert 'vip' in profile
        assert 'status' in profile
        assert 'gst' in profile
        assert 'pincode' in profile
        
        # Test enhanced field values
        assert profile['salutation'] == 'Mr.'
        assert profile['first_name'] == 'Test'
        assert profile['last_name'] == 'Buyer'
        assert profile['vip'] is True
        assert profile['status'] == 'active'
        assert profile['gst'] == 'GST123456789'
        assert profile['pincode'] == '123456'
        
        # Test category relationship
        assert profile['category'] is not None
        assert profile['category']['name'] == 'Premium'
        assert profile['category']['deposit_amount'] == 5000.0
        assert profile['category']['entry_fee'] == 1000.0
    
    def test_buyer_profile_update_enhanced_fields(self, client, buyer_token, auth_headers):
        """Test updating buyer profile with enhanced fields"""
        update_data = {
            'salutation': 'Ms.',
            'first_name': 'Updated',
            'last_name': 'Name',
            'vip': False,
            'gst': 'GST999888777',
            'pincode': '654321'
        }
        
        response = client.put('/api/buyer/profile',
                            headers=auth_headers(buyer_token),
                            json=update_data)
        
        assert response.status_code == 200
        data = response.get_json()
        profile = data['profile']
        
        # Verify updates
        assert profile['salutation'] == 'Ms.'
        assert profile['first_name'] == 'Updated'
        assert profile['last_name'] == 'Name'
        assert profile['vip'] is False
        assert profile['gst'] == 'GST999888777'
        assert profile['pincode'] == '654321'
    
    def test_seller_profile_enhanced_fields(self, client, seller_token, auth_headers):
        """Test seller profile with enhanced fields"""
        # First, we need to check if there's a seller profile endpoint
        # Since we don't have one in the current routes, let's test through admin
        pass  # Will implement when seller profile endpoint is available
    
    def test_buyer_categories_data(self, client, admin_token, auth_headers):
        """Test buyer categories are properly loaded"""
        # This would require a buyer categories endpoint
        # For now, we'll test through the database directly in the fixture
        pass
    
    def test_property_types_data(self, client, admin_token, auth_headers):
        """Test property types are properly loaded"""
        # This would require a property types endpoint
        pass
    
    def test_interests_data(self, client, admin_token, auth_headers):
        """Test interests are properly loaded"""
        # This would require an interests endpoint
        pass
    
    def test_stall_types_data(self, client, admin_token, auth_headers):
        """Test stall types are properly loaded"""
        # This would require a stall types endpoint
        pass
    
    def test_backward_compatibility_json_fields(self, client, buyer_token, auth_headers):
        """Test that legacy JSON fields still work"""
        response = client.get('/api/buyer/profile',
                            headers=auth_headers(buyer_token))
        
        assert response.status_code == 200
        data = response.get_json()
        profile = data['profile']
        
        # Test legacy JSON fields are still present
        assert 'interests' in profile
        assert 'properties_of_interest' in profile
        
        # Test they contain expected data
        assert isinstance(profile['interests'], list)
        assert isinstance(profile['properties_of_interest'], list)
        assert 'Wildlife' in profile['interests']
        assert 'Adventure' in profile['interests']
        assert 'Resort' in profile['properties_of_interest']
        assert 'Hotel' in profile['properties_of_interest']
    
    def test_buyer_profile_create_with_enhanced_fields(self, client):
        """Test creating a new buyer profile with enhanced fields"""
        # First register a new buyer
        register_response = client.post('/api/auth/register', json={
            'username': 'enhanced_buyer',
            'email': 'enhanced@test.com',
            'password': 'password123',
            'role': 'buyer'
        })
        assert register_response.status_code == 201
        
        # Login to get token
        login_response = client.post('/api/auth/login', json={
            'username': 'enhanced_buyer',
            'password': 'password123'
        })
        token = login_response.get_json()['access_token']
        headers = {'Authorization': f'Bearer {token}'}
        
        # Create profile with enhanced fields
        profile_data = {
            'name': 'Enhanced Buyer',
            'organization': 'Enhanced Org',
            'designation': 'Manager',
            'operator_type': 'Tour Operator',
            'salutation': 'Dr.',
            'first_name': 'Enhanced',
            'last_name': 'Buyer',
            'vip': True,
            'gst': 'GST111222333',
            'pincode': '111222',
            'interests': ['Wildlife', 'Culture'],
            'properties_of_interest': ['Resort', 'Homestay'],
            'country': 'India',
            'state': 'Kerala',
            'city': 'Wayanad',
            'mobile': '+919999888877',
            'website': 'https://enhanced.com'
        }
        
        response = client.post('/api/buyer/profile',
                             headers=headers,
                             json=profile_data)
        
        assert response.status_code == 201
        data = response.get_json()
        profile = data['profile']
        
        # Verify enhanced fields
        assert profile['salutation'] == 'Dr.'
        assert profile['first_name'] == 'Enhanced'
        assert profile['last_name'] == 'Buyer'
        assert profile['vip'] is True
        assert profile['gst'] == 'GST111222333'
        assert profile['pincode'] == '111222'
        
        # Verify legacy fields still work
        assert profile['interests'] == ['Wildlife', 'Culture']
        assert profile['properties_of_interest'] == ['Resort', 'Homestay']


@pytest.mark.enhanced
@pytest.mark.integration
class TestEnhancedRelationships:
    """Test enhanced model relationships"""
    
    def test_buyer_category_relationship(self, client, buyer_token, auth_headers):
        """Test buyer-category relationship"""
        response = client.get('/api/buyer/profile',
                            headers=auth_headers(buyer_token))
        
        assert response.status_code == 200
        data = response.get_json()
        profile = data['profile']
        
        # Test category relationship is properly loaded
        assert 'category' in profile
        category = profile['category']
        assert category is not None
        assert 'id' in category
        assert 'name' in category
        assert 'deposit_amount' in category
        assert 'entry_fee' in category
        assert 'description' in category
    
    def test_interest_relationships(self, client, buyer_token, auth_headers):
        """Test interest relationships (many-to-many)"""
        response = client.get('/api/buyer/profile',
                            headers=auth_headers(buyer_token))
        
        assert response.status_code == 200
        data = response.get_json()
        profile = data['profile']
        
        # Test interest relationships
        assert 'interest_relationships' in profile
        interest_relationships = profile['interest_relationships']
        assert isinstance(interest_relationships, list)
        
        # Should have some interests from test data
        # Note: This depends on the relationship being properly set up in test data


@pytest.mark.enhanced
@pytest.mark.backward_compat
class TestBackwardCompatibility:
    """Test backward compatibility with existing functionality"""
    
    def test_existing_api_responses_unchanged(self, client, buyer_token, auth_headers):
        """Test that existing API responses maintain their structure"""
        response = client.get('/api/buyer/profile',
                            headers=auth_headers(buyer_token))
        
        assert response.status_code == 200
        data = response.get_json()
        profile = data['profile']
        
        # Test all original fields are still present
        original_fields = [
            'id', 'user_id', 'name', 'organization', 'designation', 
            'operator_type', 'interests', 'properties_of_interest',
            'country', 'state', 'city', 'address', 'mobile', 'website',
            'instagram', 'year_of_starting_business', 'selling_wayanad',
            'since_when', 'bio', 'profile_image', 'created_at', 'updated_at'
        ]
        
        for field in original_fields:
            assert field in profile, f"Original field '{field}' missing from response"
    
    def test_json_fields_still_functional(self, client, buyer_token, auth_headers):
        """Test that JSON fields (interests, properties_of_interest) still work"""
        # Update with JSON data
        update_data = {
            'interests': ['Wildlife', 'Adventure', 'Photography'],
            'properties_of_interest': ['Resort', 'Hotel', 'Homestay']
        }
        
        response = client.put('/api/buyer/profile',
                            headers=auth_headers(buyer_token),
                            json=update_data)
        
        assert response.status_code == 200
        data = response.get_json()
        profile = data['profile']
        
        # Verify JSON fields updated correctly
        assert profile['interests'] == ['Wildlife', 'Adventure', 'Photography']
        assert profile['properties_of_interest'] == ['Resort', 'Hotel', 'Homestay']
    
    def test_enhanced_fields_optional(self, client):
        """Test that enhanced fields are optional for backward compatibility"""
        # Register new buyer
        register_response = client.post('/api/auth/register', json={
            'username': 'legacy_buyer',
            'email': 'legacy@test.com',
            'password': 'password123',
            'role': 'buyer'
        })
        assert register_response.status_code == 201
        
        # Login
        login_response = client.post('/api/auth/login', json={
            'username': 'legacy_buyer',
            'password': 'password123'
        })
        token = login_response.get_json()['access_token']
        headers = {'Authorization': f'Bearer {token}'}
        
        # Create profile with only legacy fields
        legacy_profile_data = {
            'name': 'Legacy Buyer',
            'organization': 'Legacy Org',
            'interests': ['Wildlife'],
            'properties_of_interest': ['Resort'],
            'country': 'India',
            'state': 'Kerala'
        }
        
        response = client.post('/api/buyer/profile',
                             headers=headers,
                             json=legacy_profile_data)
        
        assert response.status_code == 201
        data = response.get_json()
        profile = data['profile']
        
        # Verify legacy fields work
        assert profile['name'] == 'Legacy Buyer'
        assert profile['organization'] == 'Legacy Org'
        assert profile['interests'] == ['Wildlife']
        assert profile['properties_of_interest'] == ['Resort']
        
        # Verify enhanced fields have default values or are None
        assert profile['vip'] is False  # Default value
        assert profile['status'] == 'pending'  # Default value
        assert profile['salutation'] is None
        assert profile['gst'] is None
