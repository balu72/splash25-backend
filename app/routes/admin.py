from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
import pandas as pd
import re
import secrets
from datetime import datetime, timedelta
from ..utils.auth import admin_required
from ..models import db, User, UserRole, InvitedBuyer, PendingBuyer, DomainRestriction, Meeting, Listing, SellerProfile, BuyerProfile, BuyerCategory, HostProperty, TravelPlan, Accommodation
from sqlalchemy import func
from ..utils.email_service import send_invitation_email, send_approval_email, send_rejection_email

admin = Blueprint('admin', __name__, url_prefix='/api/admin')

@admin.route('/dashboard', methods=['GET'])
@admin_required
def dashboard():
    """
    Endpoint for admin dashboard data with real database queries
    """
    try:
        # Get real user statistics
        total_users = User.query.count()
        
        # Count users by role
        buyer_count = User.query.filter_by(role=UserRole.BUYER.value).count()
        seller_count = User.query.filter_by(role=UserRole.SELLER.value).count()
        admin_count = User.query.filter_by(role=UserRole.ADMIN.value).count()
        
        # Get real listing statistics
        total_listings = Listing.query.filter_by(status='active').count() if hasattr(Listing, 'status') else Listing.query.count()
        
        # Get real meeting statistics (total bookings)
        total_bookings = Meeting.query.count()
        
        # Get pending verifications (sellers not verified)
        pending_verifications = SellerProfile.query.filter_by(is_verified=False).count()
        
        # Get recent activities (last 10 users registered)
        recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
        recent_activities = []
        
        for user in recent_users:
            activity_type = 'new_user'
            if user.role == UserRole.SELLER.value:
                business_name = user.seller_profile.business_name if user.seller_profile else user.business_name or 'Unknown Business'
                details = f'New seller registered: {business_name}'
            elif user.role == UserRole.BUYER.value:
                organization = user.buyer_profile.organization if user.buyer_profile else 'Unknown Organization'
                details = f'New buyer registered: {organization}'
            else:
                details = f'New {user.role} registered: {user.username}'
            
            recent_activities.append({
                'type': activity_type,
                'details': details,
                'timestamp': user.created_at.isoformat() + 'Z'
            })
        
        # Add recent listings if available
        if hasattr(Listing, 'created_at'):
            recent_listings = Listing.query.order_by(Listing.created_at.desc()).limit(3).all()
            for listing in recent_listings:
                recent_activities.append({
                    'type': 'new_listing',
                    'details': f'New listing created: {listing.name}',
                    'timestamp': listing.created_at.isoformat() + 'Z'
                })
        
        # Sort activities by timestamp (newest first)
        recent_activities.sort(key=lambda x: x['timestamp'], reverse=True)
        recent_activities = recent_activities[:10]  # Limit to 10 most recent
        
        return jsonify({
            'message': 'Welcome to the Admin Dashboard',
            'system_stats': {
                'total_users': total_users,
                'users_by_role': {
                    'buyer': buyer_count,
                    'seller': seller_count,
                    'admin': admin_count
                },
                'total_listings': total_listings,
                'total_bookings': total_bookings,
                'pending_verifications': pending_verifications
            },
            'recent_activities': recent_activities
        }), 200
        
    except Exception as e:
        # Fallback to basic stats if there's an error
        return jsonify({
            'message': 'Welcome to the Admin Dashboard',
            'system_stats': {
                'total_users': User.query.count(),
                'users_by_role': {
                    'buyer': User.query.filter_by(role='buyer').count(),
                    'seller': User.query.filter_by(role='seller').count(),
                    'admin': User.query.filter_by(role='admin').count()
                },
                'total_listings': 0,
                'total_bookings': 0,
                'pending_verifications': 0
            },
            'recent_activities': []
        }), 200

@admin.route('/users', methods=['GET'])
@admin_required
def get_users():
    """
    Endpoint to get all users with real database queries
    """
    try:
        # Get pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        role_filter = request.args.get('role', None)
        search = request.args.get('search', None)
        
        # Build query
        query = User.query
        
        # Apply role filter
        if role_filter and role_filter in ['buyer', 'seller', 'admin']:
            query = query.filter_by(role=role_filter)
        
        # Apply search filter
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                db.or_(
                    User.username.ilike(search_term),
                    User.email.ilike(search_term),
                    User.business_name.ilike(search_term)
                )
            )
        
        # Order by creation date (newest first)
        query = query.order_by(User.created_at.desc())
        
        # Paginate results
        users_pagination = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        # Build user list with profile information
        users_list = []
        for user in users_pagination.items:
            user_data = user.to_dict()
            
            # Add profile-specific information
            if user.is_seller() and user.seller_profile:
                user_data.update({
                    'business_name': user.seller_profile.business_name,
                    'business_description': user.seller_profile.description,
                    'is_verified': user.seller_profile.is_verified,
                    'contact_email': user.seller_profile.contact_email,
                    'contact_phone': user.seller_profile.contact_phone,
                    'status': user.seller_profile.status
                })
            elif user.is_buyer() and user.buyer_profile:
                user_data.update({
                    'organization': user.buyer_profile.organization,
                    'designation': user.buyer_profile.designation,
                    'name': user.buyer_profile.name,
                    'status': user.buyer_profile.status
                })
            
            # Add legacy fields for backward compatibility
            if user.business_name:
                user_data['business_name'] = user.business_name
            if user.business_description:
                user_data['business_description'] = user.business_description
            user_data['is_verified'] = user.is_verified
            
            users_list.append(user_data)
        
        return jsonify({
            'message': 'All users retrieved successfully',
            'users': users_list,
            'pagination': {
                'page': users_pagination.page,
                'pages': users_pagination.pages,
                'per_page': users_pagination.per_page,
                'total': users_pagination.total,
                'has_next': users_pagination.has_next,
                'has_prev': users_pagination.has_prev
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Failed to retrieve users: {str(e)}',
            'users': [],
            'pagination': {
                'page': 1,
                'pages': 0,
                'per_page': 50,
                'total': 0,
                'has_next': False,
                'has_prev': False
            }
        }), 500

@admin.route('/users/<int:user_id>', methods=['GET'])
@admin_required
def get_user(user_id):
    """
    Endpoint to get a specific user with real database queries
    """
    try:
        # Find the user
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Get basic user data
        user_data = user.to_dict()
        
        # Add profile-specific information
        if user.is_seller() and user.seller_profile:
            user_data.update({
                'business_name': user.seller_profile.business_name,
                'business_description': user.seller_profile.description,
                'is_verified': user.seller_profile.is_verified,
                'contact_email': user.seller_profile.contact_email,
                'contact_phone': user.seller_profile.contact_phone,
                'status': user.seller_profile.status,
                'seller_type': user.seller_profile.seller_type,
                'target_market': user.seller_profile.target_market,
                'website': user.seller_profile.website,
                'instagram': user.seller_profile.instagram,
                'address': user.seller_profile.address,
                'state': user.seller_profile.state,
                'country': user.seller_profile.country,
                'gst': user.seller_profile.gst
            })
            
            # Add listings for sellers
            if hasattr(user, 'listings'):
                user_data['listings'] = [listing.to_dict() for listing in user.listings]
            else:
                user_data['listings'] = []
                
            # Add stalls for sellers
            if hasattr(user, 'stalls'):
                user_data['stalls'] = [stall.to_dict() for stall in user.stalls]
            else:
                user_data['stalls'] = []
                
        elif user.is_buyer() and user.buyer_profile:
            user_data.update({
                'organization': user.buyer_profile.organization,
                'designation': user.buyer_profile.designation,
                'name': user.buyer_profile.name,
                'status': user.buyer_profile.status,
                'operator_type': user.buyer_profile.operator_type,
                'country': user.buyer_profile.country,
                'state': user.buyer_profile.state,
                'city': user.buyer_profile.city,
                'address': user.buyer_profile.address,
                'mobile': user.buyer_profile.mobile,
                'website': user.buyer_profile.website,
                'instagram': user.buyer_profile.instagram,
                'year_of_starting_business': user.buyer_profile.year_of_starting_business,
                'selling_wayanad': user.buyer_profile.selling_wayanad,
                'since_when': user.buyer_profile.since_when,
                'bio': user.buyer_profile.bio,
                'vip': user.buyer_profile.vip,
                'gst': user.buyer_profile.gst,
                'interests': user.buyer_profile.interests or [],
                'properties_of_interest': user.buyer_profile.properties_of_interest or []
            })
            
            # Add category information if available
            if user.buyer_profile.category:
                user_data['category'] = user.buyer_profile.category.to_dict()
        
        # Add legacy fields for backward compatibility
        if user.business_name:
            user_data['business_name'] = user.business_name
        if user.business_description:
            user_data['business_description'] = user.business_description
        user_data['is_verified'] = user.is_verified
        
        # Add meeting statistics
        if hasattr(user, 'buyer_meetings'):
            user_data['buyer_meetings_count'] = len(user.buyer_meetings)
        if hasattr(user, 'seller_meetings'):
            user_data['seller_meetings_count'] = len(user.seller_meetings)
        
        # Add travel plans for buyers
        if user.is_buyer() and hasattr(user, 'travel_plans'):
            user_data['travel_plans'] = [plan.to_dict() for plan in user.travel_plans]
        
        return jsonify({
            'message': f'User details for ID: {user_id}',
            'user': user_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Failed to retrieve user: {str(e)}'
        }), 500

@admin.route('/users/<int:user_id>', methods=['PUT'])
@admin_required
def update_user(user_id):
    """
    Endpoint to update a user with real database operations
    """
    data = request.get_json()
    
    # Validate input data
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    try:
        # Find the user
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Validate and update basic user fields
        if 'username' in data:
            # Check if username is already taken by another user
            existing_user = User.query.filter(
                User.username == data['username'],
                User.id != user_id
            ).first()
            if existing_user:
                return jsonify({'error': 'Username already exists'}), 409
            user.username = data['username']
        
        if 'email' in data:
            # Validate email format
            import re
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, data['email']):
                return jsonify({'error': 'Invalid email format'}), 400
            
            # Check if email is already taken by another user
            existing_user = User.query.filter(
                User.email == data['email'],
                User.id != user_id
            ).first()
            if existing_user:
                return jsonify({'error': 'Email already exists'}), 409
            user.email = data['email']
        
        if 'role' in data:
            # Validate role
            valid_roles = ['buyer', 'seller', 'admin']
            if data['role'] not in valid_roles:
                return jsonify({'error': f'Invalid role. Must be one of: {valid_roles}'}), 400
            user.role = data['role']
        
        # Update profile-specific fields based on user role
        if user.is_seller() and user.seller_profile:
            if 'business_name' in data:
                user.seller_profile.business_name = data['business_name']
            if 'business_description' in data:
                user.seller_profile.description = data['business_description']
            if 'is_verified' in data:
                user.seller_profile.is_verified = bool(data['is_verified'])
            if 'contact_email' in data:
                user.seller_profile.contact_email = data['contact_email']
            if 'contact_phone' in data:
                user.seller_profile.contact_phone = data['contact_phone']
            if 'status' in data:
                user.seller_profile.status = data['status']
            if 'seller_type' in data:
                user.seller_profile.seller_type = data['seller_type']
            if 'target_market' in data:
                user.seller_profile.target_market = data['target_market']
            if 'website' in data:
                user.seller_profile.website = data['website']
            if 'instagram' in data:
                user.seller_profile.instagram = data['instagram']
            if 'address' in data:
                user.seller_profile.address = data['address']
            if 'state' in data:
                user.seller_profile.state = data['state']
            if 'country' in data:
                user.seller_profile.country = data['country']
            if 'gst' in data:
                user.seller_profile.gst = data['gst']
        
        elif user.is_buyer() and user.buyer_profile:
            if 'organization' in data:
                user.buyer_profile.organization = data['organization']
            if 'designation' in data:
                user.buyer_profile.designation = data['designation']
            if 'name' in data:
                user.buyer_profile.name = data['name']
            if 'status' in data:
                user.buyer_profile.status = data['status']
            if 'operator_type' in data:
                user.buyer_profile.operator_type = data['operator_type']
            if 'mobile' in data:
                user.buyer_profile.mobile = data['mobile']
            if 'website' in data:
                user.buyer_profile.website = data['website']
            if 'instagram' in data:
                user.buyer_profile.instagram = data['instagram']
            if 'address' in data:
                user.buyer_profile.address = data['address']
            if 'city' in data:
                user.buyer_profile.city = data['city']
            if 'state' in data:
                user.buyer_profile.state = data['state']
            if 'country' in data:
                user.buyer_profile.country = data['country']
            if 'gst' in data:
                user.buyer_profile.gst = data['gst']
            if 'vip' in data:
                user.buyer_profile.vip = bool(data['vip'])
        
        # Update legacy fields for backward compatibility
        if 'business_name' in data:
            user.business_name = data['business_name']
        if 'business_description' in data:
            user.business_description = data['business_description']
        if 'is_verified' in data:
            user.is_verified = bool(data['is_verified'])
        
        # Commit changes
        db.session.commit()
        
        # Return updated user data
        user_data = user.to_dict()
        
        # Add profile information to response
        if user.is_seller() and user.seller_profile:
            user_data.update({
                'business_name': user.seller_profile.business_name,
                'business_description': user.seller_profile.description,
                'is_verified': user.seller_profile.is_verified,
                'contact_email': user.seller_profile.contact_email,
                'contact_phone': user.seller_profile.contact_phone,
                'status': user.seller_profile.status
            })
        elif user.is_buyer() and user.buyer_profile:
            user_data.update({
                'organization': user.buyer_profile.organization,
                'designation': user.buyer_profile.designation,
                'name': user.buyer_profile.name,
                'status': user.buyer_profile.status
            })
        
        # Add legacy fields
        if user.business_name:
            user_data['business_name'] = user.business_name
        if user.business_description:
            user_data['business_description'] = user.business_description
        user_data['is_verified'] = user.is_verified
        
        return jsonify({
            'message': f'User {user_id} updated successfully',
            'user': user_data
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to update user: {str(e)}'}), 500

@admin.route('/verifications', methods=['GET'])
@admin_required
def get_verifications():
    """
    Endpoint to get pending seller verifications with real database queries
    """
    try:
        # Get pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        status_filter = request.args.get('status', 'pending')
        
        # Query for sellers with pending verification
        query = db.session.query(User, SellerProfile).join(
            SellerProfile, User.id == SellerProfile.user_id
        ).filter(
            User.role == UserRole.SELLER.value,
            SellerProfile.is_verified == False
        )
        
        # Apply status filter if needed
        if status_filter == 'pending':
            query = query.filter(SellerProfile.status.in_(['pending', 'active']))
        elif status_filter == 'all':
            pass  # No additional filter
        
        # Order by creation date (newest first)
        query = query.order_by(SellerProfile.created_at.desc())
        
        # Get all results for now (can add pagination later)
        results = query.all()
        
        # Build verification list
        verifications = []
        for user, seller_profile in results:
            verification_data = {
                'id': seller_profile.id,  # Use seller_profile.id as verification ID
                'user_id': user.id,
                'username': user.username,
                'email': user.email,
                'business_name': seller_profile.business_name,
                'status': 'pending' if not seller_profile.is_verified else 'verified',
                'created_at': seller_profile.created_at.isoformat() + 'Z' if seller_profile.created_at else None,
                'contact_email': seller_profile.contact_email,
                'contact_phone': seller_profile.contact_phone,
                'seller_type': seller_profile.seller_type,
                'target_market': seller_profile.target_market,
                'website': seller_profile.website,
                'address': seller_profile.address,
                'state': seller_profile.state,
                'country': seller_profile.country,
                'gst': seller_profile.gst,
                'documents': []  # Placeholder for document system
            }
            
            # Add mock documents structure for now
            # In a real system, you would have a separate documents table
            if seller_profile.business_name:
                verification_data['documents'].append({
                    'type': 'Business Registration',
                    'status': 'pending',
                    'uploaded_at': seller_profile.created_at.isoformat() + 'Z' if seller_profile.created_at else None
                })
            
            verifications.append(verification_data)
        
        return jsonify({
            'message': 'Pending seller verifications retrieved successfully',
            'verifications': verifications,
            'total': len(verifications),
            'pending_count': len([v for v in verifications if v['status'] == 'pending'])
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Failed to retrieve verifications: {str(e)}',
            'verifications': [],
            'total': 0,
            'pending_count': 0
        }), 500

@admin.route('/verifications/<int:verification_id>', methods=['PUT'])
@admin_required
def update_verification(verification_id):
    """
    Endpoint to approve or reject a seller verification with real database operations
    """
    data = request.get_json()
    
    if 'status' not in data or data['status'] not in ['approved', 'rejected']:
        return jsonify({'error': 'Status must be either "approved" or "rejected"'}), 400
    
    try:
        # Find the seller profile by verification_id (which is seller_profile.id)
        seller_profile = SellerProfile.query.get(verification_id)
        if not seller_profile:
            return jsonify({'error': 'Verification not found'}), 404
        
        # Get the associated user
        user = User.query.get(seller_profile.user_id)
        if not user:
            return jsonify({'error': 'Associated user not found'}), 404
        
        # Update verification status
        if data['status'] == 'approved':
            seller_profile.is_verified = True
            seller_profile.status = 'active'
            # Also update legacy field for backward compatibility
            user.is_verified = True
            
            message = f'Seller {seller_profile.business_name} verification approved'
        else:  # rejected
            seller_profile.is_verified = False
            seller_profile.status = 'rejected'
            # Also update legacy field for backward compatibility
            user.is_verified = False
            
            message = f'Seller {seller_profile.business_name} verification rejected'
        
        # Update timestamp
        seller_profile.updated_at = datetime.utcnow()
        
        # Add notes if provided
        if 'notes' in data:
            # In a real system, you might have a separate notes field or verification_notes table
            pass
        
        # Commit changes
        db.session.commit()
        
        # Prepare response data
        verification_data = {
            'id': verification_id,
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'business_name': seller_profile.business_name,
            'status': 'approved' if seller_profile.is_verified else 'rejected',
            'updated_at': seller_profile.updated_at.isoformat() + 'Z',
            'contact_email': seller_profile.contact_email,
            'contact_phone': seller_profile.contact_phone,
            'seller_type': seller_profile.seller_type,
            'target_market': seller_profile.target_market,
            'website': seller_profile.website,
            'address': seller_profile.address,
            'state': seller_profile.state,
            'country': seller_profile.country,
            'gst': seller_profile.gst
        }
        
        return jsonify({
            'message': message,
            'verification': verification_data
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to update verification: {str(e)}'}), 500

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

@admin.route('/buyers/<int:buyer_id>', methods=['PUT'])
@admin_required
def update_buyer_profile(buyer_id):
    """
    Update buyer profile (admin only)
    """
    data = request.get_json()
    
    # Validate input data
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    try:
        # Find the buyer profile by user_id (buyer_id is actually user_id)
        buyer_profile = BuyerProfile.query.filter_by(user_id=buyer_id).first()
        if not buyer_profile:
            return jsonify({'error': 'Buyer profile not found'}), 404
        
        # Get the associated user
        user = User.query.get(buyer_id)
        if not user or not user.is_buyer():
            return jsonify({'error': 'User not found or not a buyer'}), 404
        
        # Update buyer profile fields
        updatable_fields = [
            'name', 'organization', 'designation', 'operator_type',
            'country', 'state', 'city', 'address', 'mobile', 'website', 
            'instagram', 'year_of_starting_business', 
            'since_when', 'bio', 'vip', 'gst', 'interests', 
            'properties_of_interest', 'status', 'category_id'
        ]
        
        for field in updatable_fields:
            if field in data:
                if field == 'vip':
                    # Handle boolean fields
                    setattr(buyer_profile, field, bool(data[field]))
                elif field in ['year_of_starting_business', 'since_when', 'category_id']:
                    # Handle integer fields
                    if data[field] is not None:
                        setattr(buyer_profile, field, int(data[field]))
                    else:
                        setattr(buyer_profile, field, None)
                elif field in ['interests', 'properties_of_interest']:
                    # Handle JSON array fields
                    if isinstance(data[field], list):
                        setattr(buyer_profile, field, data[field])
                    else:
                        setattr(buyer_profile, field, [])
                else:
                    # Handle string fields
                    setattr(buyer_profile, field, data[field])
        
        # Update timestamp
        buyer_profile.updated_at = datetime.utcnow()
        
        # Commit changes
        db.session.commit()
        
        # Return updated buyer profile data
        buyer_data = buyer_profile.to_dict()
        
        return jsonify({
            'message': f'Buyer profile {buyer_id} updated successfully',
            'buyer': buyer_data
        }), 200
        
    except ValueError as e:
        db.session.rollback()
        return jsonify({'error': f'Invalid data format: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to update buyer profile: {str(e)}'}), 500

@admin.route('/sellers/<int:seller_id>', methods=['PUT'])
@admin_required
def update_seller_profile(seller_id):
    """
    Update seller profile (admin only)
    """
    data = request.get_json()
    
    # Validate input data
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    try:
        # Find the seller profile by user_id (seller_id is actually user_id)
        seller_profile = SellerProfile.query.filter_by(user_id=seller_id).first()
        if not seller_profile:
            return jsonify({'error': 'Seller profile not found'}), 404
        
        # Get the associated user
        user = User.query.get(seller_id)
        if not user or not user.is_seller():
            return jsonify({'error': 'User not found or not a seller'}), 404
        
        # Update seller profile fields
        updatable_fields = [
            'business_name', 'description', 'seller_type', 'target_market',
            'website', 'contact_email', 'contact_phone', 'address', 
            'state', 'country', 'gst', 'status'
        ]
        
        for field in updatable_fields:
            if field in data:
                # Handle string fields
                setattr(seller_profile, field, data[field])
        
        # Handle boolean fields separately
        if 'is_verified' in data:
            seller_profile.is_verified = bool(data['is_verified'])
        
        # Update timestamp
        seller_profile.updated_at = datetime.utcnow()
        
        # Commit changes
        db.session.commit()
        
        # Return updated seller profile data
        seller_data = seller_profile.to_dict()
        
        return jsonify({
            'message': f'Seller profile {seller_id} updated successfully',
            'seller': seller_data
        }), 200
        
    except ValueError as e:
        db.session.rollback()
        return jsonify({'error': f'Invalid data format: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to update seller profile: {str(e)}'}), 500

# Buyer Category Management Endpoints

@admin.route('/buyer-categories', methods=['GET'])
@admin_required
def get_buyer_categories():
    """
    Get all buyer categories (admin only)
    """
    try:
        categories = BuyerCategory.query.all()
        return jsonify({
            'buyer_categories': [category.to_dict() for category in categories]
        }), 200
    except Exception as e:
        return jsonify({
            'error': f'Failed to fetch buyer categories: {str(e)}'
        }), 500

@admin.route('/buyer-categories', methods=['POST'])
@admin_required
def create_buyer_category():
    """
    Create new buyer category (admin only)
    """
    data = request.get_json()
    
    # Validate input data
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Validate required fields
    if 'name' not in data:
        return jsonify({'error': 'Missing required field: name'}), 400
    
    # Check if category name already exists
    existing_category = BuyerCategory.query.filter_by(name=data['name']).first()
    if existing_category:
        return jsonify({'error': 'Category name already exists'}), 409
    
    try:
        # Create new buyer category
        category = BuyerCategory(
            name=data['name'],
            deposit_amount=data.get('deposit_amount'),
            entry_fee=data.get('entry_fee'),
            accommodation_hosted=data.get('accommodation_hosted', False),
            transfers_hosted=data.get('transfers_hosted', False),
            max_meetings=data.get('max_meetings'),
            min_meetings=data.get('min_meetings')
        )
        
        db.session.add(category)
        db.session.commit()
        
        return jsonify({
            'message': 'Buyer category created successfully',
            'buyer_category': category.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': f'Failed to create buyer category: {str(e)}'
        }), 500

@admin.route('/buyer-categories/<int:category_id>', methods=['PUT'])
@admin_required
def update_buyer_category(category_id):
    """
    Update buyer category (admin only)
    """
    data = request.get_json()
    
    # Validate input data
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    try:
        # Find the category
        category = BuyerCategory.query.get(category_id)
        if not category:
            return jsonify({'error': 'Buyer category not found'}), 404
        
        # Check if new name conflicts with existing category
        if 'name' in data and data['name'] != category.name:
            existing_category = BuyerCategory.query.filter_by(name=data['name']).first()
            if existing_category:
                return jsonify({'error': 'Category name already exists'}), 409
        
        # Update category fields
        updatable_fields = [
            'name', 'deposit_amount', 'entry_fee', 
            'accommodation_hosted', 'transfers_hosted',
            'max_meetings', 'min_meetings'
        ]
        
        for field in updatable_fields:
            if field in data:
                if field in ['accommodation_hosted', 'transfers_hosted']:
                    # Handle boolean fields
                    setattr(category, field, bool(data[field]))
                elif field in ['max_meetings', 'min_meetings']:
                    # Handle integer fields
                    if data[field] is not None:
                        setattr(category, field, int(data[field]))
                    else:
                        setattr(category, field, None)
                elif field in ['deposit_amount', 'entry_fee']:
                    # Handle decimal fields
                    if data[field] is not None:
                        setattr(category, field, float(data[field]))
                    else:
                        setattr(category, field, None)
                else:
                    # Handle string fields
                    setattr(category, field, data[field])
        
        # Commit changes
        db.session.commit()
        
        return jsonify({
            'message': f'Buyer category {category_id} updated successfully',
            'buyer_category': category.to_dict()
        }), 200
        
    except ValueError as e:
        db.session.rollback()
        return jsonify({'error': f'Invalid data format: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to update buyer category: {str(e)}'}), 500

@admin.route('/buyer-categories/<int:category_id>', methods=['DELETE'])
@admin_required
def delete_buyer_category(category_id):
    """
    Delete buyer category (admin only)
    """
    try:
        # Find the category
        category = BuyerCategory.query.get(category_id)
        if not category:
            return jsonify({'error': 'Buyer category not found'}), 404
        
        # Check if category is being used by any buyers
        buyers_using_category = BuyerProfile.query.filter_by(category_id=category_id).count()
        if buyers_using_category > 0:
            return jsonify({
                'error': f'Cannot delete category. {buyers_using_category} buyers are currently using this category.'
            }), 400
        
        # Delete the category
        db.session.delete(category)
        db.session.commit()
        
        return jsonify({
            'message': f'Buyer category {category_id} deleted successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to delete buyer category: {str(e)}'}), 500

@admin.route('/buyer-categories/<int:category_id>', methods=['GET'])
@admin_required
def get_buyer_category(category_id):
    """
    Get specific buyer category (admin only)
    """
    try:
        category = BuyerCategory.query.get(category_id)
        if not category:
            return jsonify({'error': 'Buyer category not found'}), 404
        
        # Get buyers count for this category
        buyers_count = BuyerProfile.query.filter_by(category_id=category_id).count()
        
        category_data = category.to_dict()
        category_data['buyers_count'] = buyers_count
        
        return jsonify({
            'buyer_category': category_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Failed to fetch buyer category: {str(e)}'
        }), 500

# Stall Allocation Management Endpoints

@admin.route('/sellers/<int:seller_id>/allocate-stall', methods=['POST'])
@admin_required
def allocate_stall_to_seller(seller_id):
    """
    Allocate a stall type to a seller (admin only)
    """
    data = request.get_json()
    
    # Validate input data
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Validate required fields
    if 'stall_type_id' not in data:
        return jsonify({'error': 'Missing required field: stall_type_id'}), 400
    
    try:
        # Find the seller
        seller = User.query.get(seller_id)
        if not seller or not seller.is_seller():
            return jsonify({'error': 'Seller not found'}), 404
        
        # Verify stall type exists
        from ..models import StallType, Stall
        stall_type = StallType.query.get(data['stall_type_id'])
        if not stall_type:
            return jsonify({'error': 'Invalid stall type ID'}), 400
        
        # Set default values
        stall_number = data.get('number', '0')
        fascia_name = data.get('fascia_name', '')
        
        # Use seller's business name as default fascia name if not provided
        if not fascia_name and seller.seller_profile:
            fascia_name = seller.seller_profile.business_name
        
        # Check if stall number already exists for this seller (if not using default '0')
        if stall_number != '0':
            existing_stall = Stall.query.filter_by(
                seller_id=seller_id, 
                number=stall_number
            ).first()
            
            if existing_stall:
                return jsonify({
                    'error': 'Stall number already exists for this seller'
                }), 400
        
        # Create new stall allocation
        new_stall = Stall(
            seller_id=seller_id,
            stall_type_id=data['stall_type_id'],
            number=stall_number,
            fascia_name=fascia_name,
            allocated_stall_number=data.get('allocated_stall_number', ''),
            is_allocated=True
        )
        
        db.session.add(new_stall)
        db.session.commit()
        
        return jsonify({
            'message': 'Stall allocated successfully',
            'stall': new_stall.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to allocate stall: {str(e)}'}), 500

@admin.route('/sellers/<int:seller_id>/stalls', methods=['GET'])
@admin_required
def get_seller_stalls(seller_id):
    """
    Get all stalls allocated to a specific seller (admin only)
    """
    try:
        # Find the seller
        seller = User.query.get(seller_id)
        if not seller or not seller.is_seller():
            return jsonify({'error': 'Seller not found'}), 404
        
        # Get all stalls for this seller
        from ..models import Stall
        stalls = Stall.query.filter_by(seller_id=seller_id).all()
        
        return jsonify({
            'seller_id': seller_id,
            'seller_name': seller.seller_profile.business_name if seller.seller_profile else seller.username,
            'stalls': [stall.to_dict() for stall in stalls]
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to fetch seller stalls: {str(e)}'}), 500

@admin.route('/stalls/<int:stall_id>/deallocate', methods=['DELETE'])
@admin_required
def deallocate_stall(stall_id):
    """
    Deallocate a stall from a seller (admin only)
    """
    try:
        # Find the stall
        from ..models import Stall
        stall = Stall.query.get(stall_id)
        if not stall:
            return jsonify({'error': 'Stall not found'}), 404
        
        # Store seller info for response
        seller_id = stall.seller_id
        seller_name = stall.seller.seller_profile.business_name if stall.seller and stall.seller.seller_profile else 'Unknown'
        
        # Delete the stall allocation
        db.session.delete(stall)
        db.session.commit()
        
        return jsonify({
            'message': f'Stall deallocated successfully from {seller_name}',
            'seller_id': seller_id
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to deallocate stall: {str(e)}'}), 500

@admin.route('/stalls', methods=['GET'])
@admin_required
def get_all_stalls():
    """
    Get all stall allocations (admin only)
    """
    try:
        from ..models import Stall
        stalls = Stall.query.all()
        
        stalls_data = []
        for stall in stalls:
            stall_dict = stall.to_dict()
            # Add seller information
            if stall.seller and stall.seller.seller_profile:
                stall_dict['seller_info'] = {
                    'id': stall.seller.id,
                    'business_name': stall.seller.seller_profile.business_name,
                    'contact_email': stall.seller.seller_profile.contact_email,
                    'is_verified': stall.seller.seller_profile.is_verified
                }
            stalls_data.append(stall_dict)
        
        return jsonify({
            'stalls': stalls_data,
            'total_count': len(stalls_data)
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to fetch stalls: {str(e)}'}), 500

# Host Properties Management Endpoints

@admin.route('/host-properties', methods=['GET'])
@admin_required
def get_host_properties():
    """
    Get all host properties (admin only)
    """
    try:
        properties = HostProperty.query.all()
        
        # Build properties list with calculated fields
        properties_data = []
        for property in properties:
            property_dict = property.to_dict()
            
            # Calculate additional properties
            number_rooms_allocated = property.number_rooms_allocated or 0
            number_current_guests = property.number_current_guests or 0
            
            # 1. Number of rooms available = rooms_allotted - number_rooms_allocated
            property_dict['number_rooms_available'] = property.rooms_allotted - number_rooms_allocated
            
            # 2. isAvailable = True if number_current_guests < 2*rooms_allotted, else False
            property_dict['isAvailable'] = number_current_guests < (2 * property.rooms_allotted)
            
            properties_data.append(property_dict)
        
        return jsonify({
            'host_properties': properties_data,
            'total_count': len(properties_data)
        }), 200
    except Exception as e:
        return jsonify({
            'error': f'Failed to fetch host properties: {str(e)}'
        }), 500

@admin.route('/host-properties', methods=['POST'])
@admin_required
def create_host_property():
    """
    Create new host property (admin only)
    """
    data = request.get_json()
    
    # Validate input data
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Validate required fields
    required_fields = ['property_name', 'rooms_allotted']
    for field in required_fields:
        if field not in data or data[field] is None:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Validate property_name length
    if len(data['property_name'].strip()) == 0:
        return jsonify({'error': 'Property name cannot be empty'}), 400
    
    if len(data['property_name']) > 100:
        return jsonify({'error': 'Property name cannot exceed 100 characters'}), 400
    
    # Validate rooms_allotted is positive integer
    try:
        rooms_allotted = int(data['rooms_allotted'])
        if rooms_allotted <= 0:
            return jsonify({'error': 'Rooms allotted must be a positive number'}), 400
    except (ValueError, TypeError):
        return jsonify({'error': 'Rooms allotted must be a valid number'}), 400
    
    # Validate email format if provided
    if 'contact_email' in data and data['contact_email']:
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, data['contact_email']):
            return jsonify({'error': 'Invalid email format'}), 400
    
    # Validate field lengths
    field_limits = {
        'contact_person_name': 100,
        'contact_phone': 50,
        'contact_email': 100,
        'property_address': 200
    }
    
    for field, max_length in field_limits.items():
        if field in data and data[field] and len(data[field]) > max_length:
            return jsonify({'error': f'{field} cannot exceed {max_length} characters'}), 400
    
    try:
        # Create new host property
        property = HostProperty(
            property_name=data['property_name'].strip(),
            rooms_allotted=rooms_allotted,
            contact_person_name=data.get('contact_person_name', '').strip() if data.get('contact_person_name') else None,
            contact_phone=data.get('contact_phone', '').strip() if data.get('contact_phone') else None,
            contact_email=data.get('contact_email', '').strip() if data.get('contact_email') else None,
            property_address=data.get('property_address', '').strip() if data.get('property_address') else None,
            number_current_guests=int(data['number_current_guests']) if data.get('number_current_guests') is not None else None
        )
        
        db.session.add(property)
        db.session.commit()
        
        return jsonify({
            'message': 'Host property created successfully',
            'host_property': property.to_dict()
        }), 201
        
    except ValueError as e:
        db.session.rollback()
        return jsonify({'error': f'Invalid data format: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': f'Failed to create host property: {str(e)}'
        }), 500

@admin.route('/host-properties/<int:property_id>', methods=['GET'])
@admin_required
def get_host_property(property_id):
    """
    Get specific host property (admin only)
    """
    try:
        property = HostProperty.query.get(property_id)
        if not property:
            return jsonify({'error': 'Host property not found'}), 404
        
        return jsonify({
            'host_property': property.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Failed to fetch host property: {str(e)}'
        }), 500

@admin.route('/host-properties/<int:property_id>', methods=['PUT'])
@admin_required
def update_host_property(property_id):
    """
    Update host property (admin only)
    """
    data = request.get_json()
    
    # Validate input data
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    try:
        # Find the property
        property = HostProperty.query.get(property_id)
        if not property:
            return jsonify({'error': 'Host property not found'}), 404
        
        # Validate property_name if provided
        if 'property_name' in data:
            if not data['property_name'] or len(data['property_name'].strip()) == 0:
                return jsonify({'error': 'Property name cannot be empty'}), 400
            if len(data['property_name']) > 100:
                return jsonify({'error': 'Property name cannot exceed 100 characters'}), 400
        
        # Validate rooms_allotted if provided
        if 'rooms_allotted' in data:
            try:
                rooms_allotted = int(data['rooms_allotted'])
                if rooms_allotted <= 0:
                    return jsonify({'error': 'Rooms allotted must be a positive number'}), 400
            except (ValueError, TypeError):
                return jsonify({'error': 'Rooms allotted must be a valid number'}), 400
        
        # Validate email format if provided
        if 'contact_email' in data and data['contact_email']:
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, data['contact_email']):
                return jsonify({'error': 'Invalid email format'}), 400
        
        # Validate field lengths
        field_limits = {
            'contact_person_name': 100,
            'contact_phone': 50,
            'contact_email': 100,
            'property_address': 200
        }
        
        for field, max_length in field_limits.items():
            if field in data and data[field] and len(data[field]) > max_length:
                return jsonify({'error': f'{field} cannot exceed {max_length} characters'}), 400
        
        # Update property fields
        updatable_fields = [
            'property_name', 'rooms_allotted', 'contact_person_name',
            'contact_phone', 'contact_email', 'property_address', 'number_current_guests'
        ]
        
        for field in updatable_fields:
            if field in data:
                if field == 'property_name':
                    # Handle required string field
                    setattr(property, field, data[field].strip())
                elif field in ['rooms_allotted', 'number_current_guests']:
                    # Handle integer fields
                    if data[field] is not None:
                        setattr(property, field, int(data[field]))
                    else:
                        setattr(property, field, None)
                else:
                    # Handle optional string fields
                    if data[field] is not None:
                        setattr(property, field, data[field].strip() if data[field] else None)
                    else:
                        setattr(property, field, None)
        
        # Commit changes
        db.session.commit()
        
        return jsonify({
            'message': f'Host property {property_id} updated successfully',
            'host_property': property.to_dict()
        }), 200
        
    except ValueError as e:
        db.session.rollback()
        return jsonify({'error': f'Invalid data format: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to update host property: {str(e)}'}), 500

@admin.route('/host-properties/<int:property_id>', methods=['DELETE'])
@admin_required
def delete_host_property(property_id):
    """
    Delete host property (admin only)
    """
    try:
        # Find the property
        property = HostProperty.query.get(property_id)
        if not property:
            return jsonify({'error': 'Host property not found'}), 404
        
        # Store property name for response
        property_name = property.property_name
        
        # Delete the property
        db.session.delete(property)
        db.session.commit()
        
        return jsonify({
            'message': f'Host property "{property_name}" deleted successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to delete host property: {str(e)}'}), 500

# Accommodation Allocation Management Endpoints

@admin.route('/buyers/<int:buyer_id>/allocate-accommodation', methods=['POST'])
@admin_required
def allocate_accommodation_to_buyer(buyer_id):
    """
    Allocate accommodation to a buyer using their first available travel plan (admin only)
    """
    data = request.get_json()
    
    # Validate input data
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Validate required fields
    required_fields = ['host_property_id', 'room_type', 'check_in_datetime', 'check_out_datetime']
    for field in required_fields:
        if field not in data or data[field] is None:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    try:
        # Find the buyer
        buyer = User.query.get(buyer_id)
        if not buyer:
            return jsonify({'error': f'User with ID {buyer_id} not found'}), 404
        
        if not buyer.is_buyer():
            return jsonify({'error': f'User with ID {buyer_id} is not a buyer (role: {buyer.role})'}), 404
        
        # Verify host property exists
        host_property = HostProperty.query.get(data['host_property_id'])
        if not host_property:
            return jsonify({'error': f'Host property with ID {data["host_property_id"]} not found'}), 404
        
        # Validate room type
        valid_room_types = ['single', 'shared']
        if data['room_type'] not in valid_room_types:
            return jsonify({'error': f'Invalid room type. Must be one of: {valid_room_types}'}), 400
        
        # Parse and validate datetime fields
        try:
            from datetime import datetime as dt
            check_in_datetime = dt.fromisoformat(data['check_in_datetime'].replace('Z', '+00:00'))
            check_out_datetime = dt.fromisoformat(data['check_out_datetime'].replace('Z', '+00:00'))
            
            # Validate check_out is after check_in
            if check_out_datetime <= check_in_datetime:
                return jsonify({'error': 'Check-out datetime must be after check-in datetime'}), 400
                
        except (ValueError, AttributeError) as e:
            return jsonify({'error': f'Invalid datetime format. Use ISO format (e.g., 2025-06-25T15:00:00Z): {str(e)}'}), 400
        
        # Find the first available travel plan for this buyer, or create a default one
        travel_plan = TravelPlan.query.filter_by(user_id=buyer_id).order_by(TravelPlan.created_at.asc()).first()
        
        if not travel_plan:
            # Helper function to get system setting
            def get_system_setting(key, default_value=None):
                from ..models import SystemSetting
                setting = SystemSetting.query.filter_by(key=key).first()
                return setting.value if setting and setting.value else default_value
            
            # Helper function to parse date from setting
            def parse_date_from_setting(key, fallback_date):
                date_str = get_system_setting(key)
                if date_str:
                    try:
                        return datetime.strptime(date_str, '%Y-%m-%d').date()
                    except ValueError:
                        pass
                return fallback_date
            
            # Get dynamic event configuration from system settings
            from datetime import date
            event_start_date = parse_date_from_setting('event_start_date', date(2025, 6, 25))
            event_end_date = parse_date_from_setting('event_end_date', date(2025, 6, 28))
            event_name = get_system_setting('event_name', 'Splash25 Event')
            event_venue = get_system_setting('event_venue', 'Wayanad, Kerala')
            
            # Create a default travel plan using system settings
            travel_plan = TravelPlan(
                user_id=buyer_id,
                event_name=event_name,
                event_start_date=event_start_date,
                event_end_date=event_end_date,
                venue=event_venue,
                status="active",
                created_at=datetime.utcnow()
            )
            db.session.add(travel_plan)
            db.session.flush()  # Get the ID without committing yet
        
        # Check if buyer already has accommodation for this travel plan
        existing_accommodation = Accommodation.query.filter_by(
            travel_plan_id=travel_plan.id,
            buyer_id=buyer_id
        ).first()
        
        if existing_accommodation:
            return jsonify({
                'error': f'Buyer already has accommodation allocated for travel plan "{travel_plan.event_name}"'
            }), 400
        
        # Create new accommodation allocation
        new_accommodation = Accommodation(
            travel_plan_id=travel_plan.id,
            host_property_id=data['host_property_id'],
            buyer_id=buyer_id,
            check_in_datetime=check_in_datetime,
            check_out_datetime=check_out_datetime,
            room_type=data['room_type'],
            booking_reference='',  # Empty as requested
            special_notes=data.get('special_notes', ''),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        db.session.add(new_accommodation)
        db.session.commit()
        
        # Update host property statistics
        try:
            # Count accommodations by room type for this property
            shared_count = Accommodation.query.filter_by(
                host_property_id=data['host_property_id'],
                room_type='shared'
            ).count()
            
            single_count = Accommodation.query.filter_by(
                host_property_id=data['host_property_id'],
                room_type='single'
            ).count()
            
            # Calculate number_rooms_allocated using new formula
            # Formula: (shared_count // 2) + single_count
            host_property.number_rooms_allocated = (shared_count // 2) + single_count
            
            # Validation: Check if allocated rooms exceed available rooms
            if host_property.number_rooms_allocated > host_property.rooms_allotted:
                db.session.rollback()
                return jsonify({
                    'error': 'Cannot allocate room: exceeds available room capacity'
                }), 400
            
            # Update number_current_guests using the specified formula
            # Formula: (1 * shared_count) + (2 * single_count)
            host_property.number_current_guests = (1 * shared_count) + (2 * single_count)
            
            # Commit the host property updates
            db.session.commit()
            
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'error': f'Failed to update host property statistics: {str(e)}'
            }), 500
        
        # Return success response with accommodation details
        return jsonify({
            'message': f'Accommodation allocated successfully for {buyer.buyer_profile.name if buyer.buyer_profile else buyer.username}',
            'accommodation': new_accommodation.to_dict()
        }), 201
        
    except ValueError as e:
        db.session.rollback()
        return jsonify({'error': f'Invalid data format: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to allocate accommodation: {str(e)}'}), 500

@admin.route('/buyers/<int:buyer_id>/accommodations', methods=['GET'])
@admin_required
def get_buyer_accommodations(buyer_id):
    """
    Get all accommodations allocated to a specific buyer (admin only)
    """
    try:
        # Find the buyer
        buyer = User.query.get(buyer_id)
        if not buyer or not buyer.is_buyer():
            return jsonify({'error': 'Buyer not found or user is not a buyer'}), 404
        
        # Get all accommodations for this buyer
        accommodations = Accommodation.query.filter_by(buyer_id=buyer_id).all()
        
        return jsonify({
            'buyer_id': buyer_id,
            'buyer_name': buyer.buyer_profile.name if buyer.buyer_profile else buyer.username,
            'buyer_organization': buyer.buyer_profile.organization if buyer.buyer_profile else 'Unknown Organization',
            'accommodations': [accommodation.to_dict() for accommodation in accommodations],
            'total_count': len(accommodations)
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to fetch buyer accommodations: {str(e)}'}), 500

@admin.route('/accommodations/<int:accommodation_id>/deallocate', methods=['DELETE'])
@admin_required
def deallocate_accommodation(accommodation_id):
    """
    Deallocate accommodation from a buyer (admin only)
    """
    try:
        # Find the accommodation
        accommodation = Accommodation.query.get(accommodation_id)
        if not accommodation:
            return jsonify({'error': 'Accommodation not found'}), 404
        
        # Store buyer and property info for response
        buyer_name = accommodation.buyer.buyer_profile.name if accommodation.buyer and accommodation.buyer.buyer_profile else 'Unknown Buyer'
        property_name = accommodation.host_property.property_name if accommodation.host_property else 'Unknown Property'
        
        # Delete the accommodation allocation
        db.session.delete(accommodation)
        db.session.commit()
        
        return jsonify({
            'message': f'Accommodation at "{property_name}" deallocated successfully from {buyer_name}'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to deallocate accommodation: {str(e)}'}), 500

@admin.route('/accommodations', methods=['GET'])
@admin_required
def get_all_accommodations():
    """
    Get all accommodation allocations (admin only)
    """
    try:
        accommodations = Accommodation.query.all()
        
        accommodations_data = []
        for accommodation in accommodations:
            accommodation_dict = accommodation.to_dict()
            # Add additional summary information
            if accommodation.buyer and accommodation.buyer.buyer_profile:
                accommodation_dict['buyer_summary'] = {
                    'id': accommodation.buyer.id,
                    'name': accommodation.buyer.buyer_profile.name,
                    'organization': accommodation.buyer.buyer_profile.organization,
                    'email': accommodation.buyer.email
                }
            if accommodation.host_property:
                accommodation_dict['property_summary'] = {
                    'id': accommodation.host_property.property_id,
                    'name': accommodation.host_property.property_name,
                    'total_rooms': accommodation.host_property.rooms_allotted
                }
            accommodations_data.append(accommodation_dict)
        
        return jsonify({
            'accommodations': accommodations_data,
            'total_count': len(accommodations_data)
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to fetch accommodations: {str(e)}'}), 500
