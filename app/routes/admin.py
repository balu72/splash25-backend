from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
import pandas as pd
import re
import secrets
from datetime import datetime, timedelta
from ..utils.auth import admin_required
from ..models import db, User, UserRole, InvitedBuyer, PendingBuyer, DomainRestriction
from ..utils.email_service import send_invitation_email, send_approval_email, send_rejection_email

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
    
    # Check if username or email already exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 409
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 409
    
    # Create new admin user
    user = User(
        username=data['username'],
        email=data['email'],
        password=data['password'],
        role=UserRole.ADMIN
    )
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({
        'message': 'Admin user created successfully',
        'user': user.to_dict()
    }), 201

@admin.route('/domain-restrictions', methods=['GET'])
@admin_required
def get_domain_restrictions():
    """Get all domain restrictions"""
    restrictions = DomainRestriction.query.all()
    return jsonify({
        'domain_restrictions': [r.to_dict() for r in restrictions]
    }), 200

@admin.route('/domain-restrictions', methods=['POST'])
@admin_required
def add_domain_restriction():
    """Add a new domain restriction"""
    data = request.get_json()
    
    if 'domain' not in data:
        return jsonify({'error': 'Domain is required'}), 400
    
    # Validate domain format
    domain = data['domain'].strip().lower()
    if not re.match(r'^[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,}$', domain):
        return jsonify({'error': 'Invalid domain format'}), 400
    
    # Check if domain already exists
    if DomainRestriction.query.filter_by(domain=domain).first():
        return jsonify({'error': 'Domain already exists'}), 409
    
    # Create new domain restriction
    restriction = DomainRestriction(
        domain=domain,
        is_enabled=data.get('is_enabled', True)
    )
    
    db.session.add(restriction)
    db.session.commit()
    
    return jsonify({
        'message': 'Domain restriction added successfully',
        'domain_restriction': restriction.to_dict()
    }), 201

@admin.route('/domain-restrictions/<int:restriction_id>', methods=['PUT'])
@admin_required
def update_domain_restriction(restriction_id):
    """Update a domain restriction"""
    data = request.get_json()
    
    restriction = DomainRestriction.query.get(restriction_id)
    if not restriction:
        return jsonify({'error': 'Domain restriction not found'}), 404
    
    if 'is_enabled' in data:
        restriction.is_enabled = data['is_enabled']
    
    db.session.commit()
    
    return jsonify({
        'message': 'Domain restriction updated successfully',
        'domain_restriction': restriction.to_dict()
    }), 200

@admin.route('/domain-restrictions/<int:restriction_id>', methods=['DELETE'])
@admin_required
def delete_domain_restriction(restriction_id):
    """Delete a domain restriction"""
    restriction = DomainRestriction.query.get(restriction_id)
    if not restriction:
        return jsonify({'error': 'Domain restriction not found'}), 404
    
    db.session.delete(restriction)
    db.session.commit()
    
    return jsonify({
        'message': 'Domain restriction deleted successfully'
    }), 200

@admin.route('/upload-invites', methods=['POST'])
@admin_required
def upload_invites():
    """Upload Excel file with buyer invites"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not file.filename.endswith(('.xlsx', '.xls')):
        return jsonify({'error': 'File must be an Excel file (.xlsx or .xls)'}), 400
    
    try:
        # Read Excel file
        df = pd.read_excel(file)
        
        # Validate Excel structure
        required_columns = ['Name', 'Email']
        for column in required_columns:
            if column not in df.columns:
                return jsonify({'error': f'Missing required column: {column}'}), 400
        
        # Process each row
        admin_id = get_jwt_identity()
        processed = 0
        skipped = 0
        errors = []
        
        for index, row in df.iterrows():
            name = row['Name']
            email = row['Email']
            
            # Validate email format
            if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
                errors.append({
                    'row': index + 2,  # +2 because Excel is 1-indexed and has a header row
                    'email': email,
                    'error': 'Invalid email format'
                })
                continue
            
            # Check if email already exists in invited_buyers
            if InvitedBuyer.query.filter_by(email=email).first():
                skipped += 1
                continue
            
            # Check if email already exists in users
            if User.query.filter_by(email=email).first():
                skipped += 1
                continue
            
            # Generate invitation token
            token = secrets.token_urlsafe(32)
            
            # Create invited buyer
            invited_buyer = InvitedBuyer(
                name=name,
                email=email,
                invitation_token=token,
                invited_by=admin_id,
                expires_at=datetime.utcnow() + timedelta(days=7)  # Token expires in 7 days
            )
            
            db.session.add(invited_buyer)
            processed += 1
        
        db.session.commit()
        
        # Send invitation emails
        for invited_buyer in InvitedBuyer.query.filter_by(invited_by=admin_id, is_registered=False).all():
            send_invitation_email(invited_buyer)
        
        return jsonify({
            'message': 'Invites processed successfully',
            'processed': processed,
            'skipped': skipped,
            'errors': errors
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin.route('/invited-buyers', methods=['GET'])
@admin_required
def get_invited_buyers():
    """Get all invited buyers"""
    invited_buyers = InvitedBuyer.query.all()
    return jsonify({
        'invited_buyers': [b.to_dict() for b in invited_buyers]
    }), 200

@admin.route('/invited-buyers/<int:buyer_id>/resend', methods=['POST'])
@admin_required
def resend_invitation(buyer_id):
    """Resend invitation email to buyer"""
    invited_buyer = InvitedBuyer.query.get(buyer_id)
    if not invited_buyer:
        return jsonify({'error': 'Invited buyer not found'}), 404
    
    if invited_buyer.is_registered:
        return jsonify({'error': 'Buyer has already registered'}), 400
    
    # Update expiration date
    invited_buyer.expires_at = datetime.utcnow() + timedelta(days=7)
    db.session.commit()
    
    # Send invitation email
    send_invitation_email(invited_buyer)
    
    return jsonify({
        'message': 'Invitation resent successfully',
        'invited_buyer': invited_buyer.to_dict()
    }), 200

@admin.route('/invited-buyers/<int:buyer_id>', methods=['DELETE'])
@admin_required
def delete_invited_buyer(buyer_id):
    """Delete an invited buyer"""
    invited_buyer = InvitedBuyer.query.get(buyer_id)
    if not invited_buyer:
        return jsonify({'error': 'Invited buyer not found'}), 404
    
    if invited_buyer.is_registered:
        return jsonify({'error': 'Cannot delete a buyer who has already registered'}), 400
    
    db.session.delete(invited_buyer)
    db.session.commit()
    
    return jsonify({
        'message': 'Invited buyer deleted successfully'
    }), 200

@admin.route('/pending-buyers', methods=['GET'])
@admin_required
def get_pending_buyers():
    """Get all pending buyers"""
    pending_buyers = PendingBuyer.query.all()
    return jsonify({
        'pending_buyers': [b.to_dict() for b in pending_buyers]
    }), 200

@admin.route('/pending-buyers/<int:buyer_id>', methods=['GET'])
@admin_required
def get_pending_buyer(buyer_id):
    """Get a specific pending buyer"""
    pending_buyer = PendingBuyer.query.get(buyer_id)
    if not pending_buyer:
        return jsonify({'error': 'Pending buyer not found'}), 404
    
    return jsonify({
        'pending_buyer': pending_buyer.to_dict()
    }), 200

@admin.route('/pending-buyers/<int:buyer_id>/approve', methods=['POST'])
@admin_required
def approve_buyer(buyer_id):
    """Approve a pending buyer"""
    pending_buyer = PendingBuyer.query.get(buyer_id)
    if not pending_buyer:
        return jsonify({'error': 'Pending buyer not found'}), 404
    
    if pending_buyer.status != 'pending':
        return jsonify({'error': f'Buyer is already {pending_buyer.status}'}), 400
    
    # Generate a random password
    password = secrets.token_urlsafe(10)
    
    # Create a new user
    user = User(
        username=pending_buyer.email.split('@')[0],  # Use part of email as username
        email=pending_buyer.email,
        password=password,
        role=UserRole.BUYER
    )
    
    db.session.add(user)
    
    # Update pending buyer status
    pending_buyer.status = 'approved'
    
    # Update invited buyer status
    pending_buyer.invited_buyer.is_registered = True
    
    db.session.commit()
    
    # Send approval email with login details
    send_approval_email(user, password)
    
    return jsonify({
        'message': 'Buyer approved successfully',
        'user': user.to_dict()
    }), 200

@admin.route('/pending-buyers/<int:buyer_id>/reject', methods=['POST'])
@admin_required
def reject_buyer(buyer_id):
    """Reject a pending buyer"""
    pending_buyer = PendingBuyer.query.get(buyer_id)
    if not pending_buyer:
        return jsonify({'error': 'Pending buyer not found'}), 404
    
    if pending_buyer.status != 'pending':
        return jsonify({'error': f'Buyer is already {pending_buyer.status}'}), 400
    
    # Update pending buyer status
    pending_buyer.status = 'rejected'
    db.session.commit()
    
    # Send rejection email
    send_rejection_email(pending_buyer)
    
    return jsonify({
        'message': 'Buyer rejected successfully'
    }), 200
