from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
import pandas as pd
import re
import secrets
from datetime import datetime, timedelta
from ..utils.auth import admin_required
from ..models import db, User, UserRole, InvitedBuyer, PendingBuyer, DomainRestriction, Meeting, Listing, SellerProfile, BuyerProfile
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
            'properties_of_interest', 'status'
        ]
        
        for field in updatable_fields:
            if field in data:
                if field == 'vip':
                    # Handle boolean fields
                    setattr(buyer_profile, field, bool(data[field]))
                elif field == 'year_of_starting_business' or field == 'since_when':
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
