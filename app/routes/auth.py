from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token,
    jwt_required, 
    get_jwt_identity,
    get_jwt
)
from datetime import datetime, timedelta
import re
from ..models import db, User, UserRole, InvitedBuyer, PendingBuyer, DomainRestriction
from ..utils.email_service import send_registration_confirmation_email

auth = Blueprint('auth', __name__, url_prefix='/api/auth')

# Token blacklist for logout functionality
# In a production environment, this should be stored in Redis or another persistent store
token_blacklist = set()

@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['username', 'email', 'password', 'role']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Check if username or email already exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 409
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 409
    
    # Validate role
    try:
        role = UserRole(data['role'])
    except ValueError:
        return jsonify({'error': f'Invalid role. Must be one of: {[r.value for r in UserRole]}'}), 400
    
    # Don't allow direct registration as admin
    if role == UserRole.ADMIN:
        return jsonify({'error': 'Cannot register as admin'}), 403
    
    # Additional fields for sellers
    kwargs = {}
    if role == UserRole.SELLER:
        if 'business_name' not in data:
            return jsonify({'error': 'Business name is required for sellers'}), 400
        kwargs['business_name'] = data['business_name']
        kwargs['business_description'] = data.get('business_description', '')
    
    # Create new user
    user = User(
        username=data['username'],
        email=data['email'],
        password=data['password'],
        role=role,
        **kwargs
    )
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({
        'message': 'User registered successfully',
        'user': user.to_dict()
    }), 201

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    # Validate required fields
    if not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Username and password are required'}), 400
    
    # Find user by username
    user = User.query.filter_by(username=data['username']).first()
    
    # Check if user exists and password is correct
    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'Invalid username or password'}), 401
    
    # Create tokens
    access_token = create_access_token(
        identity=str(user.id),  # Convert to string to avoid JWT issues
        additional_claims={'role': user.role.value},
        expires_delta=timedelta(hours=1)
    )
    refresh_token = create_refresh_token(
        identity=str(user.id),  # Convert to string to avoid JWT issues
        additional_claims={'role': user.role.value},
        expires_delta=timedelta(days=30)
    )
    
    return jsonify({
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': user.to_dict()
    }), 200

@auth.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user_id = get_jwt_identity()
    # Convert to int if it's a string
    if isinstance(current_user_id, str):
        try:
            current_user_id = int(current_user_id)
        except ValueError:
            return jsonify({'error': 'Invalid user ID'}), 400
    
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Create new access token
    access_token = create_access_token(
        identity=str(user.id),  # Convert to string to avoid JWT issues
        additional_claims={'role': user.role.value},
        expires_delta=timedelta(hours=1)
    )
    
    return jsonify({
        'access_token': access_token,
        'user': user.to_dict()
    }), 200

@auth.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    current_user_id = get_jwt_identity()
    # Convert to int if it's a string
    if isinstance(current_user_id, str):
        try:
            current_user_id = int(current_user_id)
        except ValueError:
            return jsonify({'error': 'Invalid user ID'}), 400
    
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify(user.to_dict()), 200

@auth.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()['jti']
    token_blacklist.add(jti)
    return jsonify({'message': 'Successfully logged out'}), 200

# Helper function to check if a token is blacklisted
def is_token_blacklisted(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    return jti in token_blacklist

@auth.route('/validate-invite/<token>', methods=['GET'])
def validate_invite(token):
    """Validate an invitation token"""
    invited_buyer = InvitedBuyer.query.filter_by(invitation_token=token).first()
    
    if not invited_buyer:
        return jsonify({'error': 'Invalid invitation token'}), 404
    
    if invited_buyer.is_registered:
        return jsonify({'error': 'Invitation already used'}), 400
    
    if invited_buyer.expires_at < datetime.utcnow():
        return jsonify({'error': 'Invitation expired'}), 400
    
    return jsonify({
        'message': 'Invitation valid',
        'invited_buyer': {
            'name': invited_buyer.name,
            'email': invited_buyer.email
        }
    }), 200

@auth.route('/register-invited', methods=['POST'])
def register_invited():
    """Register an invited buyer"""
    data = request.get_json()
    
    # Validate required fields
    required_fields = [
        'token', 'name', 'designation', 'company', 'address', 'city', 'state', 
        'pin', 'mobile', 'email', 'year_of_starting_business', 'type_of_operator',
        'already_sell_wayanad', 'opinion_about_previous_splash', 
        'reference_property1_name', 'reference_property1_address',
        'interests', 'properties_of_interest', 'why_attend_splash2025'
    ]
    
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Validate invitation token
    invited_buyer = InvitedBuyer.query.filter_by(invitation_token=data['token']).first()
    
    if not invited_buyer:
        return jsonify({'error': 'Invalid invitation token'}), 404
    
    if invited_buyer.is_registered:
        return jsonify({'error': 'Invitation already used'}), 400
    
    if invited_buyer.expires_at < datetime.utcnow():
        return jsonify({'error': 'Invitation expired'}), 400
    
    # Validate email matches invitation
    if data['email'].lower() != invited_buyer.email.lower():
        return jsonify({'error': 'Email does not match invitation'}), 400
    
    # Check domain restriction if enabled
    domain_restrictions = DomainRestriction.query.filter_by(is_enabled=True).all()
    if domain_restrictions:
        email_domain = data['email'].split('@')[-1].lower()
        allowed_domains = [r.domain.lower() for r in domain_restrictions]
        
        if email_domain not in allowed_domains:
            return jsonify({'error': 'Email domain not allowed'}), 400
    
    # Validate mobile number format
    if not re.match(r'^\+\d{12}$', data['mobile']):
        return jsonify({'error': 'Invalid mobile number format. Must be in format: +XXXXXXXXXXXX (12 digits after +)'}), 400
    
    # Create pending buyer
    pending_buyer = PendingBuyer(
        invited_buyer_id=invited_buyer.id,
        name=data['name'],
        designation=data['designation'],
        company=data['company'],
        gst=data.get('gst'),
        address=data['address'],
        city=data['city'],
        state=data['state'],
        pin=data['pin'],
        mobile=data['mobile'],
        email=data['email'],
        website=data.get('website'),
        instagram=data.get('instagram'),
        year_of_starting_business=data['year_of_starting_business'],
        type_of_operator=data['type_of_operator'],
        already_sell_wayanad=data['already_sell_wayanad'],
        since_when=data.get('since_when'),
        opinion_about_previous_splash=data['opinion_about_previous_splash'],
        property_stayed_in=data.get('property_stayed_in'),
        reference_property1_name=data['reference_property1_name'],
        reference_property1_address=data['reference_property1_address'],
        reference_property2_name=data.get('reference_property2_name'),
        reference_property2_address=data.get('reference_property2_address'),
        interests=','.join(data['interests']),
        properties_of_interest=','.join(data['properties_of_interest']),
        why_attend_splash2025=data['why_attend_splash2025']
    )
    
    db.session.add(pending_buyer)
    db.session.commit()
    
    # Send confirmation email
    send_registration_confirmation_email(pending_buyer)
    
    return jsonify({
        'message': 'Registration submitted successfully',
        'pending_buyer': pending_buyer.to_dict()
    }), 201
