from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import db, User, UserRole, SellerProfile
from ..utils.auth import seller_required, admin_required

seller = Blueprint('seller', __name__, url_prefix='/api/sellers')

@seller.route('', methods=['GET'])
@jwt_required()
def get_sellers():
    """Get all sellers with optional filtering"""
    # Get query parameters
    name = request.args.get('name', '')
    seller_type = request.args.get('seller_type', '')
    target_market = request.args.get('target_market', '')
    
    # Start with a query for all sellers
    query = SellerProfile.query.join(User).filter(User.role == UserRole.SELLER)
    
    # Apply filters if provided
    if name:
        query = query.filter(SellerProfile.business_name.ilike(f'%{name}%'))
    
    if seller_type:
        query = query.filter(SellerProfile.seller_type == seller_type)
    
    if target_market:
        query = query.filter(SellerProfile.target_market == target_market)
    
    # Execute the query
    seller_profiles = query.all()
    
    return jsonify({
        'sellers': [s.to_dict() for s in seller_profiles]
    }), 200

@seller.route('/<int:seller_id>', methods=['GET'])
@jwt_required()
def get_seller(seller_id):
    """Get a specific seller's details"""
    # Find the seller profile
    seller_profile = SellerProfile.query.filter_by(user_id=seller_id).first()
    
    if not seller_profile:
        return jsonify({
            'error': 'Seller not found'
        }), 404
    
    # Check if the associated user is actually a seller
    user = User.query.get(seller_id)
    if not user or user.role != UserRole.SELLER:
        return jsonify({
            'error': 'User is not a seller'
        }), 400
    
    return jsonify({
        'seller': seller_profile.to_dict()
    }), 200

@seller.route('/profile', methods=['GET'])
@jwt_required()
@seller_required
def get_own_profile():
    """Get the current seller's profile"""
    user_id = get_jwt_identity()
    
    # Find the seller profile
    seller_profile = SellerProfile.query.filter_by(user_id=user_id).first()
    
    if not seller_profile:
        return jsonify({
            'error': 'Seller profile not found'
        }), 404
    
    return jsonify({
        'seller': seller_profile.to_dict()
    }), 200

@seller.route('/profile', methods=['PUT'])
@jwt_required()
@seller_required
def update_profile():
    """Update the current seller's profile"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    # Validate business name if provided
    if 'business_name' in data:
        business_name = data['business_name'].strip() if data['business_name'] else ''
        if len(business_name) < 5:
            return jsonify({
                'error': 'Business name must be at least 5 characters long'
            }), 400
        data['business_name'] = business_name
    
    # Find the seller profile
    seller_profile = SellerProfile.query.filter_by(user_id=user_id).first()
    
    if not seller_profile:
        # Create a new profile if it doesn't exist
        seller_profile = SellerProfile(user_id=user_id)
        db.session.add(seller_profile)
    
    # Update fields
    updatable_fields = [
        'business_name', 'description', 'seller_type', 'target_market',
        'logo_url', 'website', 'contact_email', 'contact_phone', 'address'
    ]
    
    for field in updatable_fields:
        if field in data:
            setattr(seller_profile, field, data[field])
    
    try:
        db.session.commit()
        return jsonify({
            'message': 'Profile updated successfully',
            'seller': seller_profile.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Failed to update profile',
            'message': str(e)
        }), 500

@seller.route('/types', methods=['GET'])
@jwt_required()
def get_seller_types():
    """Get all unique seller types"""
    seller_types = db.session.query(SellerProfile.seller_type).distinct().all()
    # Filter out None values and extract from tuples
    types = [t[0] for t in seller_types if t[0]]
    
    return jsonify({
        'seller_types': types
    }), 200

@seller.route('/target-markets', methods=['GET'])
@jwt_required()
def get_target_markets():
    """Get all unique target markets"""
    target_markets = db.session.query(SellerProfile.target_market).distinct().all()
    # Filter out None values and extract from tuples
    markets = [m[0] for m in target_markets if m[0]]
    
    return jsonify({
        'target_markets': markets
    }), 200

@seller.route('/<int:seller_id>/verify', methods=['PUT'])
@jwt_required()
@admin_required
def verify_seller(seller_id):
    """Verify a seller (admin only)"""
    # Find the seller profile
    seller_profile = SellerProfile.query.filter_by(user_id=seller_id).first()
    
    if not seller_profile:
        return jsonify({
            'error': 'Seller profile not found'
        }), 404
    
    # Check if the associated user is actually a seller
    user = User.query.get(seller_id)
    if not user or user.role != UserRole.SELLER:
        return jsonify({
            'error': 'User is not a seller'
        }), 400
    
    # Update verification status
    seller_profile.is_verified = True
    db.session.commit()
    
    return jsonify({
        'message': 'Seller verified successfully',
        'seller': seller_profile.to_dict()
    }), 200
