from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from ..utils.auth import seller_required, admin_required
from ..models import db, User, UserRole

buyers = Blueprint('buyers', __name__, url_prefix='/api/buyers')

@buyers.route('', methods=['GET'])
@jwt_required()
def get_buyers():
    """Get all buyers with optional filtering"""
    # Mock data for now until BuyerProfile model is created
    mock_buyers = [
        {
            'id': 1,
            'user_id': 1,
            'name': 'John Smith',
            'organization': 'Adventure Tours Ltd',
            'operator_type': 'Tour Operator',
            'interests': ['Wildlife', 'Trekking', 'Photography'],
            'properties_of_interest': ['Resorts', 'Homestays'],
            'country': 'India',
            'state': 'Kerala',
            'selling_wayanad': True,
            'bio': 'Experienced tour operator specializing in eco-tourism'
        },
        {
            'id': 2,
            'user_id': 2,
            'name': 'Sarah Johnson',
            'organization': 'Nature Expeditions',
            'operator_type': 'Travel Agent',
            'interests': ['Nature', 'Cultural Tours'],
            'properties_of_interest': ['Hotels', 'Camping'],
            'country': 'USA',
            'state': 'California',
            'selling_wayanad': False,
            'bio': 'Travel agent focused on sustainable tourism'
        }
    ]
    
    return jsonify({
        'buyers': mock_buyers
    }), 200

@buyers.route('/<int:buyer_id>', methods=['GET'])
@jwt_required()
def get_buyer(buyer_id):
    """Get a specific buyer's details"""
    # Mock data for specific buyer
    mock_buyer = {
        'id': buyer_id,
        'user_id': buyer_id,
        'name': 'John Smith',
        'organization': 'Adventure Tours Ltd',
        'operator_type': 'Tour Operator',
        'interests': ['Wildlife', 'Trekking', 'Photography'],
        'properties_of_interest': ['Resorts', 'Homestays'],
        'country': 'India',
        'state': 'Kerala',
        'selling_wayanad': True,
        'bio': 'Experienced tour operator specializing in eco-tourism'
    }
    
    return jsonify({
        'buyer': mock_buyer
    }), 200

@buyers.route('/operator-types', methods=['GET'])
@jwt_required()
def get_operator_types():
    """Get all unique operator types"""
    mock_types = ['Tour Operator', 'Travel Agent', 'Hotel Chain', 'Resort Owner', 'DMC']
    
    return jsonify({
        'operator_types': mock_types
    }), 200

@buyers.route('/interests', methods=['GET'])
@jwt_required()
def get_interests():
    """Get all unique interests"""
    mock_interests = ['Wildlife', 'Trekking', 'Photography', 'Nature', 'Cultural Tours', 'Adventure Sports', 'Wellness', 'Backpacking']
    
    return jsonify({
        'interests': mock_interests
    }), 200

@buyers.route('/property-types', methods=['GET'])
@jwt_required()
def get_property_types():
    """Get all unique property types"""
    mock_property_types = ['Resorts', 'Hotels', 'Homestays', 'Camping', 'Tree Houses', 'Villas', 'Hostels']
    
    return jsonify({
        'property_types': mock_property_types
    }), 200

@buyers.route('/countries', methods=['GET'])
@jwt_required()
def get_countries():
    """Get all unique countries"""
    mock_countries = ['India', 'USA', 'UK', 'Germany', 'France', 'Australia', 'Canada', 'Singapore']
    
    return jsonify({
        'countries': mock_countries
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
    
    # Mock states based on country
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
    
    states = mock_states.get(country, [])
    
    return jsonify({
        'states': states
    }), 200
