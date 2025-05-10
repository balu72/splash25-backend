from flask import Blueprint, jsonify, request
from .auth_utils import admin_required
from .models import User, UserRole, db

admin = Blueprint('admin', __name__, url_prefix='/api/admin')

@admin.route('/dashboard', methods=['GET'])
@admin_required
def dashboard():
    """
    Endpoint for admin dashboard data
    """
    # This is a placeholder for actual dashboard data
    # In a real application, you would fetch relevant data from the database
    return jsonify({
        'message': 'Welcome to the Admin Dashboard',
        'system_stats': {
            'total_users': 150,
            'users_by_role': {
                'buyer': 120,
                'seller': 29,
                'admin': 1
            },
            'total_listings': 45,
            'total_bookings': 230,
            'pending_verifications': 3
        },
        'recent_activities': [
            {
                'type': 'new_user',
                'details': 'New seller registered: Wayanad Eco Tours',
                'timestamp': '2025-05-09T10:15:00Z'
            },
            {
                'type': 'verification_request',
                'details': 'Seller verification requested: Kerala Adventures',
                'timestamp': '2025-05-08T14:30:00Z'
            },
            {
                'type': 'new_listing',
                'details': 'New listing created: Banasura Hill Trek',
                'timestamp': '2025-05-08T09:45:00Z'
            }
        ]
    }), 200

@admin.route('/users', methods=['GET'])
@admin_required
def get_users():
    """
    Endpoint to get all users
    """
    # In a real application, you would fetch users from the database
    # with pagination and filtering
    return jsonify({
        'message': 'All users',
        'users': [
            {
                'id': 1,
                'username': 'admin',
                'email': 'admin@splash25.com',
                'role': 'admin',
                'created_at': '2025-01-01T00:00:00Z'
            },
            {
                'id': 2,
                'username': 'seller1',
                'email': 'seller1@example.com',
                'role': 'seller',
                'created_at': '2025-01-15T10:30:00Z',
                'business_name': 'Wayanad Adventures',
                'is_verified': True
            },
            {
                'id': 3,
                'username': 'buyer1',
                'email': 'buyer1@example.com',
                'role': 'buyer',
                'created_at': '2025-02-10T15:45:00Z'
            }
        ]
    }), 200

@admin.route('/users/<int:user_id>', methods=['GET'])
@admin_required
def get_user(user_id):
    """
    Endpoint to get a specific user
    """
    # In a real application, you would fetch the user from the database
    return jsonify({
        'message': f'User details for ID: {user_id}',
        'user': {
            'id': user_id,
            'username': 'seller1',
            'email': 'seller1@example.com',
            'role': 'seller',
            'created_at': '2025-01-15T10:30:00Z',
            'business_name': 'Wayanad Adventures',
            'business_description': 'Providing authentic experiences in the heart of Wayanad',
            'is_verified': True,
            'verification_documents': [
                {
                    'type': 'Business Registration',
                    'status': 'approved',
                    'uploaded_at': '2025-01-15T10:30:00Z'
                },
                {
                    'type': 'ID Proof',
                    'status': 'approved',
                    'uploaded_at': '2025-01-15T10:35:00Z'
                }
            ],
            'listings': [
                {
                    'id': 1,
                    'name': 'Wayanad Nature Camp',
                    'status': 'active'
                },
                {
                    'id': 2,
                    'name': 'Splash25 Trekking Adventure',
                    'status': 'active'
                }
            ]
        }
    }), 200

@admin.route('/users/<int:user_id>', methods=['PUT'])
@admin_required
def update_user(user_id):
    """
    Endpoint to update a user
    """
    data = request.get_json()
    
    # In a real application, you would update the user in the database
    
    return jsonify({
        'message': f'User {user_id} updated successfully',
        'user': {
            'id': user_id,
            'username': data.get('username', 'seller1'),
            'email': data.get('email', 'seller1@example.com'),
            'role': data.get('role', 'seller'),
            'is_verified': data.get('is_verified', True)
        }
    }), 200

@admin.route('/verifications', methods=['GET'])
@admin_required
def get_verifications():
    """
    Endpoint to get pending seller verifications
    """
    # In a real application, you would fetch pending verifications from the database
    return jsonify({
        'message': 'Pending seller verifications',
        'verifications': [
            {
                'id': 1,
                'user_id': 4,
                'username': 'seller2',
                'business_name': 'Kerala Adventures',
                'documents': [
                    {
                        'type': 'Business Registration',
                        'url': '/documents/seller2/business-reg.pdf',
                        'uploaded_at': '2025-05-08T14:30:00Z'
                    },
                    {
                        'type': 'ID Proof',
                        'url': '/documents/seller2/id-proof.pdf',
                        'uploaded_at': '2025-05-08T14:35:00Z'
                    }
                ]
            },
            {
                'id': 2,
                'user_id': 5,
                'username': 'seller3',
                'business_name': 'Wayanad Eco Tours',
                'documents': [
                    {
                        'type': 'Business Registration',
                        'url': '/documents/seller3/business-reg.pdf',
                        'uploaded_at': '2025-05-09T10:15:00Z'
                    }
                ]
            }
        ]
    }), 200

@admin.route('/verifications/<int:verification_id>', methods=['PUT'])
@admin_required
def update_verification(verification_id):
    """
    Endpoint to approve or reject a seller verification
    """
    data = request.get_json()
    
    if 'status' not in data or data['status'] not in ['approved', 'rejected']:
        return jsonify({'error': 'Status must be either "approved" or "rejected"'}), 400
    
    # In a real application, you would update the verification status in the database
    
    return jsonify({
        'message': f'Verification {verification_id} {data["status"]}',
        'verification': {
            'id': verification_id,
            'user_id': 4,
            'username': 'seller2',
            'business_name': 'Kerala Adventures',
            'status': data['status'],
            'updated_at': '2025-05-10T15:30:00Z'
        }
    }), 200

@admin.route('/create-admin', methods=['POST'])
@admin_required
def create_admin():
    """
    Endpoint to create a new admin user
    """
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['username', 'email', 'password']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # In a real application, you would check if the username or email already exists
    # and create the new admin user in the database
    
    return jsonify({
        'message': 'Admin user created successfully',
        'user': {
            'id': 6,  # This would be generated by the database
            'username': data['username'],
            'email': data['email'],
            'role': 'admin',
            'created_at': '2025-05-10T15:35:00Z'
        }
    }), 201
