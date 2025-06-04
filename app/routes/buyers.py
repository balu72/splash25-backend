from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from ..utils.auth import seller_required, admin_required
from ..models import db, User, UserRole, BuyerProfile, Interest, PropertyType

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
    query = BuyerProfile.query.join(User).filter(User.role == 'buyer')
    
    # Apply filters if provided
    if name:
        query = query.filter(
            (BuyerProfile.name.ilike(f'%{name}%')) | 
            (BuyerProfile.organization.ilike(f'%{name}%'))
        )
    
    if operator_type:
        query = query.filter(BuyerProfile.operator_type == operator_type)
    
    if interest:
        # For JSONB array fields, use the @> operator to check if array contains element
        query = query.filter(BuyerProfile.interests.op('@>')(f'["{interest}"]'))
    
    if property_type:
        # For JSONB array fields, use the @> operator to check if array contains element
        query = query.filter(BuyerProfile.properties_of_interest.op('@>')(f'["{property_type}"]'))
    
    if country:
        query = query.filter(BuyerProfile.country == country)
    
    if state:
        query = query.filter(BuyerProfile.state == state)
    
    if selling_wayanad:
        selling_wayanad_bool = selling_wayanad.lower() == 'true'
        query = query.filter(BuyerProfile.selling_wayanad == selling_wayanad_bool)
    
    # Execute the query
    buyer_profiles = query.all()
    
    # Convert to dict format without problematic relationships

    buyers_data = []
    for b in buyer_profiles:
        buyer_dict = {
            'id': b.id,
            'user_id': b.user_id,
            'name': b.name,
            'organization': b.organization,
            'designation': b.designation,
            'operator_type': b.operator_type,
            'category_id': b.category_id,
            'salutation': b.salutation,
            'first_name': b.first_name,
            'last_name': b.last_name,
            'vip': b.vip,
            'status': b.status,
            'gst': b.gst,
            'pincode': b.pincode,
            'interests': [interest.name for interest in b.interest_relationships] if b.interest_relationships else [],
            'properties_of_interest': b.properties_of_interest or [],
            'country': b.country,
            'state': b.state,
            'city': b.city,
            'address': b.address,
            'mobile': b.mobile,
            'website': b.website,
            'instagram': b.instagram,
            'year_of_starting_business': b.year_of_starting_business,
            'selling_wayanad': b.selling_wayanad,
            'since_when': b.since_when,
            'bio': b.bio,
            'profile_image': b.profile_image,
            'created_at': b.created_at.isoformat() if b.created_at else None,
            'updated_at': b.updated_at.isoformat() if b.updated_at else None,
            'user': {
                'id': b.user.id,
                'username': b.user.username,
                'email': b.user.email,
                'role': b.user.role,
                'created_at': b.user.created_at.isoformat() if b.user.created_at else None
            }
        }
        buyers_data.append(buyer_dict)
 
    
    return jsonify({
       'buyers': buyers_data
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
    if not user or user.role != 'buyer':
        return jsonify({
            'error': 'User is not a buyer'
        }), 400
    
    # Convert to dict format without problematic relationships
    buyer_dict = {
        'id': buyer_profile.id,
        'user_id': buyer_profile.user_id,
        'name': buyer_profile.name,
        'organization': buyer_profile.organization,
        'designation': buyer_profile.designation,
        'operator_type': buyer_profile.operator_type,
        'category_id': buyer_profile.category_id,
        'salutation': buyer_profile.salutation,
        'first_name': buyer_profile.first_name,
        'last_name': buyer_profile.last_name,
        'vip': buyer_profile.vip,
        'status': buyer_profile.status,
        'gst': buyer_profile.gst,
        'pincode': buyer_profile.pincode,
        'interests': [interest.name for interest in buyer_profile.interest_relationships] if buyer_profile.interest_relationships else [],
        'properties_of_interest': buyer_profile.properties_of_interest or [],
        'country': buyer_profile.country,
        'state': buyer_profile.state,
        'city': buyer_profile.city,
        'address': buyer_profile.address,
        'mobile': buyer_profile.mobile,
        'website': buyer_profile.website,
        'instagram': buyer_profile.instagram,
        'year_of_starting_business': buyer_profile.year_of_starting_business,
        'selling_wayanad': buyer_profile.selling_wayanad,
        'since_when': buyer_profile.since_when,
        'bio': buyer_profile.bio,
        'profile_image': buyer_profile.profile_image,
        'created_at': buyer_profile.created_at.isoformat() if buyer_profile.created_at else None,
        'updated_at': buyer_profile.updated_at.isoformat() if buyer_profile.updated_at else None,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'created_at': user.created_at.isoformat() if user.created_at else None
        }
    }
    
    return jsonify({
        'buyer': buyer_dict
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
    """Read all  interests"""
    # Get all buyer profiles and extract unique interests
    all_interests = Interest.query.all()
    interests = []
    
    for interest in all_interests:
        if (interest.name):
            interests.append(interest.name)

    return jsonify({
        'interests': interests
    }), 200

@buyers.route('/property-types', methods=['GET'])
@jwt_required()
def get_property_types():
    """Get all unique property types"""
    # Get all buyer profiles and extract unique property types
    all_property_types = PropertyType.query.all()
    property_types = []
    
    for property_type in all_property_types:
        if (property_type.name):
            property_types.append(property_type.name)
    
    return jsonify({
        'property_types': property_types
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
