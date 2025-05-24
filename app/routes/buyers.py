from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from ..utils.auth import seller_required, admin_required
from ..models import db, User, UserRole, BuyerProfile

buyers = Blueprint('buyers', __name__, url_prefix='/api/buyers')

@buyers.route('', methods=['GET'])
@jwt_required()
def get_buyers():
    """Get all buyers with optional filtering"""
    # Get query parameters
    name = request.args.get('name', '')
    operator_type = request.args.get('operator_type', '')
    interest = request.args.get('interest', '')
    property_type = request.args.get('property_type', '')
    country = request.args.get('country', '')
    state = request.args.get('state', '')
    selling_wayanad = request.args.get('selling_wayanad', '')
    
    # Start with a query for all buyers
    query = BuyerProfile.query.join(User).filter(User.role == UserRole.BUYER)
    
    # Apply filters if provided
    if name:
        query = query.filter(
            (BuyerProfile.name.ilike(f'%{name}%')) | 
            (BuyerProfile.organization.ilike(f'%{name}%'))
        )
    
    if operator_type:
        query = query.filter(BuyerProfile.operator_type == operator_type)
    
    if interest:
        # For JSON array fields, use contains
        query = query.filter(BuyerProfile.interests.contains([interest]))
    
    if property_type:
        query = query.filter(BuyerProfile.properties_of_interest.contains([property_type]))
    
    if country:
        query = query.filter(BuyerProfile.country == country)
    
    if state:
        query = query.filter(BuyerProfile.state == state)
    
    if selling_wayanad:
        selling_wayanad_bool = selling_wayanad.lower() == 'true'
        query = query.filter(BuyerProfile.selling_wayanad == selling_wayanad_bool)
    
    # Execute the query
    buyer_profiles = query.all()
    
    return jsonify({
        'buyers': [b.to_dict() for b in buyer_profiles]
    }), 200

@buyers.route('/<int:buyer_id>', methods=['GET'])
@jwt_required()
def get_buyer(buyer_id):
    """Get a specific buyer's details"""
    # Find the buyer profile
    buyer_profile = BuyerProfile.query.filter_by(user_id=buyer_id).first()
    
    if not buyer_profile:
        return jsonify({
            'error': 'Buyer not found'
        }), 404
    
    # Check if the associated user is actually a buyer
    user = User.query.get(buyer_id)
    if not user or user.role != UserRole.BUYER:
        return jsonify({
            'error': 'User is not a buyer'
        }), 400
    
    return jsonify({
        'buyer': buyer_profile.to_dict()
    }), 200

@buyers.route('/operator-types', methods=['GET'])
@jwt_required()
def get_operator_types():
    """Get all unique operator types"""
    operator_types = db.session.query(BuyerProfile.operator_type).distinct().all()
    # Filter out None values and extract from tuples
    types = [t[0] for t in operator_types if t[0]]
    
    # If no data exists, return default types
    if not types:
        types = ['Tour Operator', 'Travel Agent', 'Hotel Chain', 'Resort Owner', 'DMC']
    
    return jsonify({
        'operator_types': types
    }), 200

@buyers.route('/interests', methods=['GET'])
@jwt_required()
def get_interests():
    """Get all unique interests"""
    # Get all buyer profiles and extract unique interests
    buyer_profiles = BuyerProfile.query.all()
    interests = set()
    
    for profile in buyer_profiles:
        if profile.interests:
            interests.update(profile.interests)
    
    # If no data exists, return default interests
    if not interests:
        interests = {'Wildlife', 'Trekking', 'Photography', 'Nature', 'Cultural Tours', 'Adventure Sports', 'Wellness', 'Backpacking'}
    
    return jsonify({
        'interests': list(interests)
    }), 200

@buyers.route('/property-types', methods=['GET'])
@jwt_required()
def get_property_types():
    """Get all unique property types"""
    # Get all buyer profiles and extract unique property types
    buyer_profiles = BuyerProfile.query.all()
    property_types = set()
    
    for profile in buyer_profiles:
        if profile.properties_of_interest:
            property_types.update(profile.properties_of_interest)
    
    # If no data exists, return default property types
    if not property_types:
        property_types = {'Resorts', 'Hotels', 'Homestays', 'Camping', 'Tree Houses', 'Villas', 'Hostels'}
    
    return jsonify({
        'property_types': list(property_types)
    }), 200

@buyers.route('/countries', methods=['GET'])
@jwt_required()
def get_countries():
    """Get all unique countries"""
    countries = db.session.query(BuyerProfile.country).distinct().all()
    # Filter out None values and extract from tuples
    country_list = [c[0] for c in countries if c[0]]
    
    # If no data exists, return default countries
    if not country_list:
        country_list = ['India', 'USA', 'UK', 'Germany', 'France', 'Australia', 'Canada', 'Singapore']
    
    return jsonify({
        'countries': country_list
    }), 200

@buyers.route('/states', methods=['GET'])
@jwt_required()
def get_states():
    """Get all unique states for a specific country"""
    country = request.args.get('country')
    
    if not country:
        return jsonify({
            'error': 'Country parameter is required'
        }), 400
    
    states = db.session.query(BuyerProfile.state).filter_by(country=country).distinct().all()
    # Filter out None values and extract from tuples
    state_list = [s[0] for s in states if s[0]]
    
    # If no data exists, return default states based on country
    if not state_list:
        mock_states = {
            'India': ['Kerala', 'Karnataka', 'Tamil Nadu', 'Goa', 'Maharashtra'],
            'USA': ['California', 'New York', 'Florida', 'Texas', 'Nevada'],
            'UK': ['England', 'Scotland', 'Wales', 'Northern Ireland'],
            'Germany': ['Bavaria', 'Berlin', 'Hamburg', 'Saxony'],
            'France': ['Île-de-France', 'Provence', 'Normandy', 'Brittany'],
            'Australia': ['New South Wales', 'Victoria', 'Queensland', 'Western Australia'],
            'Canada': ['Ontario', 'Quebec', 'British Columbia', 'Alberta'],
            'Singapore': ['Central', 'North', 'South', 'East', 'West']
        }
        state_list = mock_states.get(country, [])
    
    return jsonify({
        'states': state_list
    }), 200
