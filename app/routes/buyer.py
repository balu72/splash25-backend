from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from nc_py_api import Nextcloud, NextcloudException
from io import BytesIO
from PIL import Image
import base64
import requests
from urllib.parse import urlparse
from werkzeug.utils import secure_filename
import os
import logging
from ..utils.auth import buyer_required
from ..models import db, User, TravelPlan, Transportation, Accommodation, GroundTransportation, Meeting, MeetingStatus, UserRole, TimeSlot, SystemSetting, BuyerProfile, BuyerCategory, PropertyType, Interest, StallType

buyer = Blueprint('buyer', __name__, url_prefix='/api/buyer')

@buyer.route('/dashboard', methods=['GET'])
@buyer_required
def dashboard():
    """
    Endpoint for buyer dashboard data
    """
    user_id = get_jwt_identity()
    
    # Convert to int if it's a string
    if isinstance(user_id, str):
        try:
            user_id = int(user_id)
        except ValueError:
            return jsonify({'error': 'Invalid user ID'}), 400
    
    # Get featured destinations from verified sellers
    try:
        from ..models.models import SellerProfile
        featured_sellers = SellerProfile.query.join(User).filter(
            User.role == UserRole.SELLER.value,
            SellerProfile.is_verified == True,
            SellerProfile.status == 'active'
        ).limit(3).all()
        
        featured_destinations = []
        for seller in featured_sellers:
            featured_destinations.append({
                'id': seller.id,
                'name': seller.business_name or 'Kerala Experience',
                'description': seller.description or 'Experience authentic Kerala hospitality',
                'image_url': seller.logo_url or '/images/destinations/default.jpg'
            })
        
        # Fallback if no sellers found
        if not featured_destinations:
            featured_destinations = [
                {
                    'id': 1,
                    'name': 'Discover Kerala',
                    'description': 'Connect with local businesses and experiences',
                    'image_url': '/images/destinations/kerala-default.jpg'
                }
            ]
    except Exception as e:
        # Fallback in case of database error
        featured_destinations = []
    
    # Get upcoming events from buyer's meetings
    try:
        upcoming_meetings = Meeting.query.filter_by(
            buyer_id=user_id,
            status=MeetingStatus.ACCEPTED
        ).join(TimeSlot).filter(
            TimeSlot.start_time > datetime.now()
        ).order_by(TimeSlot.start_time).limit(2).all()
        
        upcoming_events = []
        for meeting in upcoming_meetings:
            seller_name = 'Business Partner'
            if meeting.seller and meeting.seller.seller_profile:
                seller_name = meeting.seller.seller_profile.business_name
            elif meeting.seller:
                seller_name = meeting.seller.business_name or meeting.seller.username
            
            upcoming_events.append({
                'id': meeting.id,
                'name': f'Meeting with {seller_name}',
                'date': meeting.time_slot.start_time.strftime('%Y-%m-%d'),
                'location': 'Event Venue'
            })
        
        # If no upcoming meetings, show general event info
        if not upcoming_events:
            # Check system settings for event info
            event_start = SystemSetting.query.filter_by(key='event_start_date').first()
            venue_name = SystemSetting.query.filter_by(key='venue_name').first()
            
            if event_start and venue_name:
                upcoming_events.append({
                    'id': 1,
                    'name': 'Splash25 Event',
                    'date': event_start.value,
                    'location': venue_name.value
                })
    except Exception as e:
        # Fallback in case of database error
        upcoming_events = []
    
    return jsonify({
        'message': 'Welcome to the Buyer Dashboard',
        'featured_destinations': featured_destinations,
        'upcoming_events': upcoming_events
    }), 200

@buyer.route('/profile', methods=['GET'])
@buyer_required
def get_profile():
    """
    Endpoint to get buyer profile information
    """
    user_id = get_jwt_identity()
    
    # Convert to int if it's a string
    if isinstance(user_id, str):
        try:
            user_id = int(user_id)
        except ValueError:
            return jsonify({'error': 'Invalid user ID'}), 400
    
    # Get buyer profile
    buyer_profile = BuyerProfile.query.filter_by(user_id=user_id).first()
    
    if not buyer_profile:
        return jsonify({
            'error': 'Buyer profile not found'
        }), 404
    
    return jsonify({
        'profile': buyer_profile.to_dict()
    }), 200

@buyer.route('/profile', methods=['PUT'])
@buyer_required
def update_profile():
    """
    Endpoint to update buyer profile information
    """
    user_id = get_jwt_identity()
    
    # Convert to int if it's a string
    if isinstance(user_id, str):
        try:
            user_id = int(user_id)
        except ValueError:
            return jsonify({'error': 'Invalid user ID'}), 400
    
    data = request.get_json()
    
    # Get or create buyer profile
    buyer_profile = BuyerProfile.query.filter_by(user_id=user_id).first()
    
    if not buyer_profile:
        # Create new profile
        buyer_profile = BuyerProfile(user_id=user_id)
        db.session.add(buyer_profile)
    
    # Update profile fields (including enhanced fields)
    updatable_fields = [
        # Legacy fields
        'name', 'organization', 'designation', 'operator_type', 
        'interests', 'properties_of_interest', 'country', 'state', 
        'city', 'address', 'mobile', 'website', 'instagram', 
        'year_of_starting_business', 'bio', 'profile_image',
        # Enhanced fields
        'category_id', 'salutation', 'first_name', 'last_name', 
        'vip', 'status', 'gst', 'pincode'
    ]
    
    for field in updatable_fields:
        if field in data:
            setattr(buyer_profile, field, data[field])
    
    try:
        db.session.commit()
        return jsonify({
            'message': 'Profile updated successfully',
            'profile': buyer_profile.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': f'Failed to update profile: {str(e)}'
        }), 500

@buyer.route('/profile', methods=['POST'])
@buyer_required
def create_profile():
    """
    Endpoint to create buyer profile information
    """
    user_id = get_jwt_identity()
    
    # Convert to int if it's a string
    if isinstance(user_id, str):
        try:
            user_id = int(user_id)
        except ValueError:
            return jsonify({'error': 'Invalid user ID'}), 400
    
    data = request.get_json()
    
    # Check if profile already exists
    existing_profile = BuyerProfile.query.filter_by(user_id=user_id).first()
    if existing_profile:
        return jsonify({
            'error': 'Profile already exists. Use PUT to update.'
        }), 400
    
    # Validate required fields
    required_fields = ['name', 'organization']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Create new profile with enhanced fields support
    buyer_profile = BuyerProfile(
        user_id=user_id,
        # Legacy fields
        name=data['name'],
        organization=data['organization'],
        designation=data.get('designation'),
        operator_type=data.get('operator_type'),
        interests=data.get('interests', []),
        properties_of_interest=data.get('properties_of_interest', []),
        country=data.get('country'),
        state=data.get('state'),
        city=data.get('city'),
        address=data.get('address'),
        mobile=data.get('mobile'),
        website=data.get('website'),
        instagram=data.get('instagram'),
        year_of_starting_business=data.get('year_of_starting_business'),
        bio=data.get('bio'),
        profile_image=data.get('profile_image'),
        # Enhanced fields
        category_id=data.get('category_id'),
        salutation=data.get('salutation'),
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        vip=data.get('vip', False),
        status=data.get('status', 'pending'),
        gst=data.get('gst'),
        pincode=data.get('pincode')
    )
    
    try:
        db.session.add(buyer_profile)
        db.session.commit()
        return jsonify({
            'message': 'Profile created successfully',
            'profile': buyer_profile.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': f'Failed to create profile: {str(e)}'
        }), 500

# Enhanced Model Endpoints

@buyer.route('/categories', methods=['GET'])
@buyer_required
def get_buyer_categories():
    """
    Endpoint to get all buyer categories
    """
    try:
        categories = BuyerCategory.query.all()
        return jsonify({
            'categories': [category.to_dict() for category in categories]
        }), 200
    except Exception as e:
        return jsonify({
            'error': f'Failed to fetch categories: {str(e)}'
        }), 500

@buyer.route('/categories/<int:category_id>', methods=['GET'])
@buyer_required
def get_buyer_category(category_id):
    """
    Endpoint to get a specific buyer category
    """
    try:
        category = BuyerCategory.query.get(category_id)
        if not category:
            return jsonify({'error': 'Category not found'}), 404
        
        return jsonify({
            'category': category.to_dict()
        }), 200
    except Exception as e:
        return jsonify({
            'error': f'Failed to fetch category: {str(e)}'
        }), 500

@buyer.route('/interests', methods=['GET'])
@buyer_required
def get_interests():
    """
    Endpoint to get all available interests
    """
    try:
        interests = Interest.query.all()
        return jsonify({
            'interests': [interest.to_dict() for interest in interests]
        }), 200
    except Exception as e:
        return jsonify({
            'error': f'Failed to fetch interests: {str(e)}'
        }), 500

@buyer.route('/travel-plans', methods=['GET'])
@buyer_required
def get_travel_plans():
    """
    Endpoint to get buyer's travel plans
    """
    user_id = get_jwt_identity()
    
    # Convert to int if it's a string
    if isinstance(user_id, str):
        try:
            user_id = int(user_id)
        except ValueError:
            return jsonify({'error': 'Invalid user ID'}), 400
    
    # Fetch travel plans for the user
    travel_plans = TravelPlan.query.filter_by(user_id=user_id).all()
    
    if not travel_plans:
        # if no travel plan found, create a new one 
        travel_plan = TravelPlan(
            user_id = user_id,
            event_name = 'Wayanad Splash 2025',
            event_start_date = datetime(2025, 7, 11),
            event_end_date = datetime(2025, 7, 13),
            venue = "Wayanad Tourism organization",
            status = "Planned",
            created_at = datetime.now()
        )
        db.session.add(travel_plan);
        db.session.commit()

        # Refetch the details
        travel_plans = TravelPlan.query.filter_by(user_id=user_id).all()
    
    return jsonify({
        'travel_plans': [plan.to_dict() for plan in travel_plans]
    }), 200

@buyer.route('/travel-plans/<int:plan_id>/outbound', methods=['PUT'])
@buyer_required
def update_outbound(plan_id):
    """
    Endpoint to update outbound journey details
    """
    user_id = get_jwt_identity()
    
    # Convert to int if it's a string
    if isinstance(user_id, str):
        try:
            user_id = int(user_id)
        except ValueError:
            return jsonify({'error': 'Invalid user ID'}), 400
    
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['carrier', 'number', 'departureLocation', 'departureDateTime', 
                       'arrivalLocation', 'arrivalDateTime', 'bookingReference']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Fetch travel plan
    travel_plan = TravelPlan.query.filter_by(id=plan_id, user_id=user_id).first()
    if not travel_plan:
        return jsonify({'error': 'Travel plan not found or access denied'}), 404
    
    # Determine transportation type from data - preserve existing type if not provided
    transport_type = data.get('type', travel_plan.transportation.type if travel_plan.transportation else 'flight').lower()
    outbound_type = data.get('outbound_type', transport_type).lower()  # Individual outbound type
    
    # Update outbound journey details
    if not travel_plan.transportation:
        # Create new transportation record if it doesn't exist
        transportation = Transportation(
            travel_plan_id=plan_id,
            type=transport_type,
            outbound_type=outbound_type,  # Set individual outbound type
            outbound_carrier=data['carrier'],
            outbound_number=data['number'],
            outbound_departure_location=data['departureLocation'],
            outbound_departure_datetime=datetime.fromisoformat(data['departureDateTime']),
            outbound_arrival_location=data['arrivalLocation'],
            outbound_arrival_datetime=datetime.fromisoformat(data['arrivalDateTime']),
            outbound_booking_reference=data['bookingReference'],
            outbound_seat_info=data.get('seatInfo', ''),
            # Set default values for return journey
            return_carrier='',
            return_number='',
            return_departure_location='',
            return_departure_datetime=datetime.now(),
            return_arrival_location='',
            return_arrival_datetime=datetime.now(),
            return_booking_reference=''
        )
        db.session.add(transportation)
    else:
        # Update existing transportation record
        travel_plan.transportation.type = transport_type
        travel_plan.transportation.outbound_type = outbound_type  # Update individual outbound type
        travel_plan.transportation.outbound_carrier = data['carrier']
        travel_plan.transportation.outbound_number = data['number']
        travel_plan.transportation.outbound_departure_location = data['departureLocation']
        travel_plan.transportation.outbound_departure_datetime = datetime.fromisoformat(data['departureDateTime'])
        travel_plan.transportation.outbound_arrival_location = data['arrivalLocation']
        travel_plan.transportation.outbound_arrival_datetime = datetime.fromisoformat(data['arrivalDateTime'])
        travel_plan.transportation.outbound_booking_reference = data['bookingReference']
        travel_plan.transportation.outbound_seat_info = data.get('seatInfo', '')
    
    db.session.commit()
    
    return jsonify({
        'message': 'Outbound journey updated successfully',
        'travel_plan': travel_plan.to_dict()
    }), 200

@buyer.route('/travel-plans/<int:plan_id>/return', methods=['PUT'])
@buyer_required
def update_return(plan_id):
    """
    Endpoint to update return journey details
    """
    user_id = get_jwt_identity()
    
    # Convert to int if it's a string
    if isinstance(user_id, str):
        try:
            user_id = int(user_id)
        except ValueError:
            return jsonify({'error': 'Invalid user ID'}), 400
    
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['carrier', 'number', 'departureLocation', 'departureDateTime', 
                       'arrivalLocation', 'arrivalDateTime', 'bookingReference']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Fetch travel plan
    travel_plan = TravelPlan.query.filter_by(id=plan_id, user_id=user_id).first()
    if not travel_plan:
        return jsonify({'error': 'Travel plan not found or access denied'}), 404
    
    # Determine transportation type from data - preserve existing type if not provided
    transport_type = data.get('type', travel_plan.transportation.type if travel_plan.transportation else 'flight').lower()
    
    # Update return journey details
    if not travel_plan.transportation:
        # Create new transportation record if it doesn't exist
        transportation = Transportation(
            travel_plan_id=plan_id,
            type=transport_type,
            # Set default values for outbound journey
            outbound_carrier='',
            outbound_number='',
            outbound_departure_location='',
            outbound_departure_datetime=datetime.now(),
            outbound_arrival_location='',
            outbound_arrival_datetime=datetime.now(),
            outbound_booking_reference='',
            # Return journey details
            return_carrier=data['carrier'],
            return_number=data['number'],
            return_departure_location=data['departureLocation'],
            return_departure_datetime=datetime.fromisoformat(data['departureDateTime']),
            return_arrival_location=data['arrivalLocation'],
            return_arrival_datetime=datetime.fromisoformat(data['arrivalDateTime']),
            return_booking_reference=data['bookingReference'],
            return_seat_info=data.get('seatInfo', '')
        )
        db.session.add(transportation)
    else:
        # Update existing transportation record
        travel_plan.transportation.type = transport_type
        travel_plan.transportation.return_carrier = data['carrier']
        travel_plan.transportation.return_number = data['number']
        travel_plan.transportation.return_departure_location = data['departureLocation']
        travel_plan.transportation.return_departure_datetime = datetime.fromisoformat(data['departureDateTime'])
        travel_plan.transportation.return_arrival_location = data['arrivalLocation']
        travel_plan.transportation.return_arrival_datetime = datetime.fromisoformat(data['arrivalDateTime'])
        travel_plan.transportation.return_booking_reference = data['bookingReference']
        travel_plan.transportation.return_seat_info = data.get('seatInfo', '')
    
    db.session.commit()
    
    return jsonify({
        'message': 'Return journey updated successfully',
        'travel_plan': travel_plan.to_dict()
    }), 200

@buyer.route('/travel-plans/<int:plan_id>/transportation', methods=['PUT'])
@buyer_required
def update_transportation(plan_id):
    """
    Endpoint to update both outbound and return transportation details in a single transaction
    """
    user_id = get_jwt_identity()
    
    # Convert to int if it's a string
    if isinstance(user_id, str):
        try:
            user_id = int(user_id)
        except ValueError:
            return jsonify({'error': 'Invalid user ID'}), 400
    
    data = request.get_json()
    
    # Validate required fields for both outbound and return
    required_outbound_fields = ['outbound.carrier', 'outbound.number', 'outbound.departureLocation', 
                               'outbound.departureDateTime', 'outbound.arrivalLocation', 
                               'outbound.arrivalDateTime', 'outbound.bookingReference']
    required_return_fields = ['return.carrier', 'return.number', 'return.departureLocation', 
                             'return.departureDateTime', 'return.arrivalLocation', 
                             'return.arrivalDateTime', 'return.bookingReference']
    
    # Check outbound fields
    for field in required_outbound_fields:
        keys = field.split('.')
        if keys[0] not in data or keys[1] not in data[keys[0]]:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Check return fields
    for field in required_return_fields:
        keys = field.split('.')
        if keys[0] not in data or keys[1] not in data[keys[0]]:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Fetch travel plan
    travel_plan = TravelPlan.query.filter_by(id=plan_id, user_id=user_id).first()
    if not travel_plan:
        return jsonify({'error': 'Travel plan not found or access denied'}), 404
    
    # Get transportation type from data
    transport_type = data.get('type', 'flight').lower()
    
    try:
        # Update transportation details in a single transaction
        if not travel_plan.transportation:
            # Create new transportation record if it doesn't exist
            transportation = Transportation(
                travel_plan_id=plan_id,
                type=transport_type,
                # Individual transportation types
                outbound_type=data['outbound'].get('type', transport_type).lower(),
                return_type=data['return'].get('type', transport_type).lower(),
                # Outbound journey
                outbound_carrier=data['outbound']['carrier'],
                outbound_number=data['outbound']['number'],
                outbound_departure_location=data['outbound']['departureLocation'],
                outbound_departure_datetime=datetime.fromisoformat(data['outbound']['departureDateTime']),
                outbound_arrival_location=data['outbound']['arrivalLocation'],
                outbound_arrival_datetime=datetime.fromisoformat(data['outbound']['arrivalDateTime']),
                outbound_booking_reference=data['outbound']['bookingReference'],
                outbound_seat_info=data['outbound'].get('seatInfo', ''),
                # Return journey
                return_carrier=data['return']['carrier'],
                return_number=data['return']['number'],
                return_departure_location=data['return']['departureLocation'],
                return_departure_datetime=datetime.fromisoformat(data['return']['departureDateTime']),
                return_arrival_location=data['return']['arrivalLocation'],
                return_arrival_datetime=datetime.fromisoformat(data['return']['arrivalDateTime']),
                return_booking_reference=data['return']['bookingReference'],
                return_seat_info=data['return'].get('seatInfo', '')
            )
            db.session.add(transportation)
        else:
            # Update existing transportation record (SINGLE UPDATE - FIXES DUPLICATE ISSUE)
            travel_plan.transportation.type = transport_type
            # Individual transportation types
            travel_plan.transportation.outbound_type = data['outbound'].get('type', transport_type).lower()
            travel_plan.transportation.return_type = data['return'].get('type', transport_type).lower()
            # Outbound journey
            travel_plan.transportation.outbound_carrier = data['outbound']['carrier']
            travel_plan.transportation.outbound_number = data['outbound']['number']
            travel_plan.transportation.outbound_departure_location = data['outbound']['departureLocation']
            travel_plan.transportation.outbound_departure_datetime = datetime.fromisoformat(data['outbound']['departureDateTime'])
            travel_plan.transportation.outbound_arrival_location = data['outbound']['arrivalLocation']
            travel_plan.transportation.outbound_arrival_datetime = datetime.fromisoformat(data['outbound']['arrivalDateTime'])
            travel_plan.transportation.outbound_booking_reference = data['outbound']['bookingReference']
            travel_plan.transportation.outbound_seat_info = data['outbound'].get('seatInfo', '')
            # Return journey
            travel_plan.transportation.return_carrier = data['return']['carrier']
            travel_plan.transportation.return_number = data['return']['number']
            travel_plan.transportation.return_departure_location = data['return']['departureLocation']
            travel_plan.transportation.return_departure_datetime = datetime.fromisoformat(data['return']['departureDateTime'])
            travel_plan.transportation.return_arrival_location = data['return']['arrivalLocation']
            travel_plan.transportation.return_arrival_datetime = datetime.fromisoformat(data['return']['arrivalDateTime'])
            travel_plan.transportation.return_booking_reference = data['return']['bookingReference']
            travel_plan.transportation.return_seat_info = data['return'].get('seatInfo', '')
        
        db.session.commit()
        
        return jsonify({
            'message': 'Transportation updated successfully',
            'travel_plan': travel_plan.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': f'Failed to update transportation: {str(e)}'
        }), 500

@buyer.route('/travel-plans/<int:plan_id>/accommodation', methods=['PUT'])
@buyer_required
def update_accommodation(plan_id):
    """
    Endpoint to update accommodation details
    """
    user_id = get_jwt_identity()
    
    # Convert to int if it's a string
    if isinstance(user_id, str):
        try:
            user_id = int(user_id)
        except ValueError:
            return jsonify({'error': 'Invalid user ID'}), 400
    
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['name', 'address', 'checkInDateTime', 'checkOutDateTime', 
                       'roomType', 'bookingReference']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Fetch travel plan
    travel_plan = TravelPlan.query.filter_by(id=plan_id, user_id=user_id).first()
    if not travel_plan:
        return jsonify({'error': 'Travel plan not found or access denied'}), 404
    
    # Update accommodation details
    if not travel_plan.accommodation:
        # Create new accommodation record if it doesn't exist
        accommodation = Accommodation(
            travel_plan_id=plan_id,
            name=data['name'],
            address=data['address'],
            check_in_datetime=datetime.fromisoformat(data['checkInDateTime']),
            check_out_datetime=datetime.fromisoformat(data['checkOutDateTime']),
            room_type=data['roomType'],
            booking_reference=data['bookingReference'],
            special_notes=data.get('specialNotes', '')
        )
        db.session.add(accommodation)
    else:
        # Update existing accommodation record
        travel_plan.accommodation.name = data['name']
        travel_plan.accommodation.address = data['address']
        travel_plan.accommodation.check_in_datetime = datetime.fromisoformat(data['checkInDateTime'])
        travel_plan.accommodation.check_out_datetime = datetime.fromisoformat(data['checkOutDateTime'])
        travel_plan.accommodation.room_type = data['roomType']
        travel_plan.accommodation.booking_reference = data['bookingReference']
        travel_plan.accommodation.special_notes = data.get('specialNotes', '')
    
    db.session.commit()
    
    return jsonify({
        'message': 'Accommodation updated successfully',
        'travel_plan': travel_plan.to_dict()
    }), 200

@buyer.route('/travel-plans/<int:plan_id>/pickup', methods=['PUT'])
@buyer_required
def update_pickup(plan_id):
    """
    Endpoint to update pickup details
    """
    user_id = get_jwt_identity()
    
    # Convert to int if it's a string
    if isinstance(user_id, str):
        try:
            user_id = int(user_id)
        except ValueError:
            return jsonify({'error': 'Invalid user ID'}), 400
    
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['location', 'dateTime']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Fetch travel plan
    travel_plan = TravelPlan.query.filter_by(id=plan_id, user_id=user_id).first()
    if not travel_plan:
        return jsonify({'error': 'Travel plan not found or access denied'}), 404
    
    # Update pickup details
    if not travel_plan.ground_transportation:
        # Create new ground transportation record if it doesn't exist
        ground_transportation = GroundTransportation(
            travel_plan_id=plan_id,
            pickup_location=data['location'],
            pickup_datetime=datetime.fromisoformat(data['dateTime']),
            pickup_vehicle_type=data.get('vehicleType', ''),
            pickup_driver_contact=data.get('driverContact', ''),
            # Set default values for dropoff
            dropoff_location='',
            dropoff_datetime=datetime.now(),
            dropoff_vehicle_type='',
            dropoff_driver_contact=''
        )
        db.session.add(ground_transportation)
    else:
        # Update existing ground transportation record
        travel_plan.ground_transportation.pickup_location = data['location']
        travel_plan.ground_transportation.pickup_datetime = datetime.fromisoformat(data['dateTime'])
        travel_plan.ground_transportation.pickup_vehicle_type = data.get('vehicleTypeId', None)
        travel_plan.ground_transportation.pickup_driver_contact = data.get('driverContact', '')
    
    db.session.commit()
    
    return jsonify({
        'message': 'Pickup details updated successfully',
        'travel_plan': travel_plan.to_dict()
    }), 200

@buyer.route('/travel-plans/<int:plan_id>/dropoff', methods=['PUT'])
@buyer_required
def update_dropoff(plan_id):
    """
    Endpoint to update dropoff details
    """
    user_id = get_jwt_identity()
    
    # Convert to int if it's a string
    if isinstance(user_id, str):
        try:
            user_id = int(user_id)
        except ValueError:
            return jsonify({'error': 'Invalid user ID'}), 400
    
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['location', 'dateTime']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Fetch travel plan
    travel_plan = TravelPlan.query.filter_by(id=plan_id, user_id=user_id).first()
    if not travel_plan:
        return jsonify({'error': 'Travel plan not found or access denied'}), 404
    
    # Update dropoff details
    if not travel_plan.ground_transportation:
        # Create new ground transportation record if it doesn't exist
        ground_transportation = GroundTransportation(
            travel_plan_id=plan_id,
            # Set default values for pickup
            pickup_location='',
            pickup_datetime=datetime.now(),
            pickup_vehicle_type='',
            pickup_driver_contact='',
            # Dropoff details
            dropoff_location=data['location'],
            dropoff_datetime=datetime.fromisoformat(data['dateTime']),
            dropoff_vehicle_type=data.get('vehicleType', ''),
            dropoff_driver_contact=data.get('driverContact', '')
        )
        db.session.add(ground_transportation)
    else:
        # Update existing ground transportation record
        travel_plan.ground_transportation.dropoff_location = data['location']
        travel_plan.ground_transportation.dropoff_datetime = datetime.fromisoformat(data['dateTime'])
        travel_plan.ground_transportation.dropoff_vehicle_type = data.get('vehicleTypeId', None)
        travel_plan.ground_transportation.dropoff_driver_contact = data.get('driverContact', '')
    
    db.session.commit()
    
    return jsonify({
        'message': 'Dropoff details updated successfully',
        'travel_plan': travel_plan.to_dict()
    }), 200

@buyer.route('/meetings', methods=['GET'])
@buyer_required
def get_meetings():
    """
    Endpoint to get buyer's meetings
    """
    user_id = get_jwt_identity()
    
    # Convert to int if it's a string
    if isinstance(user_id, str):
        try:
            user_id = int(user_id)
        except ValueError:
            return jsonify({'error': 'Invalid user ID'}), 400
    
    # Get query parameters for filtering
    status = request.args.get('status')
    from_date = request.args.get('from_date')
    to_date = request.args.get('to_date')
    
    # Build query
    query = Meeting.query.filter_by(buyer_id=user_id)
    
    # Apply filters if provided
    if status:
        try:
            meeting_status = MeetingStatus(status)
            query = query.filter_by(status=meeting_status)
        except ValueError:
            return jsonify({'error': f'Invalid status: {status}'}), 400
    
    # Execute query
    meetings = query.all()
    
    return jsonify({
        'meetings': [meeting.to_dict() for meeting in meetings]
    }), 200

@buyer.route('/meetings', methods=['POST'])
@buyer_required
def create_meeting():
    """
    Endpoint to create a new meeting request
    """
    user_id = get_jwt_identity()
    
    # Convert to int if it's a string
    if isinstance(user_id, str):
        try:
            user_id = int(user_id)
        except ValueError:
            return jsonify({'error': 'Invalid user ID'}), 400
    
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['seller_id', 'time_slot_id']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Check if meetings are enabled
    meetings_enabled = SystemSetting.query.filter_by(key='meetings_enabled').first()
    if not meetings_enabled or meetings_enabled.value != 'true':
        return jsonify({
            'error': 'Meeting requests are currently disabled'
        }), 400

    # Check if the seller exists
    seller = User.query.get(data['seller_id'])
    if not seller or seller.role != UserRole.SELLER:
        return jsonify({
            'error': 'Invalid seller'
        }), 400
    
    # Check if the time slot exists and is available
    time_slot = TimeSlot.query.get(data['time_slot_id'])
    if not time_slot:
        return jsonify({
            'error': 'Time slot not found'
        }), 404
    
    if not time_slot.is_available:
        return jsonify({
            'error': 'Time slot is not available'
        }), 400
    
    # Check if the time slot belongs to the seller
    if time_slot.user_id != data['seller_id']:
        return jsonify({
            'error': 'Time slot does not belong to the specified seller'
        }), 400

    # Create the meeting
    meeting = Meeting(
        buyer_id=user_id,
        seller_id=data['seller_id'],
        time_slot_id=data['time_slot_id'],
        notes=data.get('notes', ''),
        status=MeetingStatus.PENDING
    )
    
    # Mark the time slot as unavailable
    time_slot.is_available = False
    
    db.session.add(meeting)
    db.session.commit()

    # Link meeting_id to time_slot if supported
    if hasattr(time_slot, 'meeting_id'):
        time_slot.meeting_id = meeting.id
        db.session.commit()
    
    return jsonify({
        'message': 'Meeting request created successfully',
        'meeting': meeting.to_dict()
    }), 201

@buyer.route('/meetings/<int:meeting_id>', methods=['PUT'])
@buyer_required
def update_meeting(meeting_id):
    """
    Endpoint to update meeting status
    """
    user_id = get_jwt_identity()
    
    # Convert to int if it's a string
    if isinstance(user_id, str):
        try:
            user_id = int(user_id)
        except ValueError:
            return jsonify({'error': 'Invalid user ID'}), 400
    
    data = request.get_json()
    
    # Validate required fields
    if 'status' not in data:
        return jsonify({'error': 'Missing required field: status'}), 400
    
    # Check if meeting exists and belongs to the user
    meeting = Meeting.query.filter_by(id=meeting_id, buyer_id=user_id).first()
    if not meeting:
        return jsonify({'error': 'Meeting not found or access denied'}), 404
    
    # Update meeting status
    try:
        meeting.status = MeetingStatus(data['status'])
        db.session.commit()
    except ValueError:
        return jsonify({'error': f'Invalid status: {data["status"]}'}), 400
    
    return jsonify({
        'message': 'Meeting updated successfully',
        'meeting': meeting.to_dict()
    }), 200

@buyer.route('/profile/image', methods=['POST'])
@buyer_required
def upload_profile_image():
    """
    Endpoint to upload buyer profile image
    """
    user_id = get_jwt_identity()
    
    # Convert to int if it's a string
    if isinstance(user_id, str):
        try:
            user_id = int(user_id)
        except ValueError:
            return jsonify({'error': 'Invalid user ID'}), 400
    
    # Check if file was uploaded
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    # Validate file
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Check file type
    allowed_extensions = {'jpg', 'jpeg', 'png'}
    if not '.' in file.filename or file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
        return jsonify({'error': 'Invalid file type. Only JPG, JPEG, and PNG files are allowed'}), 400
    
    # Check file size (1MB limit)
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)  # Reset file pointer
    
    if file_size > 1 * 1024 * 1024:  # 1MB
        return jsonify({'error': 'File size exceeds 1MB limit'}), 400
    
    try:
        # Get buyer profile
        buyer_profile = BuyerProfile.query.filter_by(user_id=user_id).first()
        if not buyer_profile:
            return jsonify({'error': 'Buyer profile not found'}), 404
        
        # Get external storage credentials from environment
        storage_url = os.getenv('EXTERNAL_STORAGE_URL')+"index.php"
        storage_user = os.getenv('EXTERNAL_STORAGE_USER')
        storage_password = os.getenv('EXTERNAL_STORAGE_PASSWORD')
        ocs_url = os.getenv("EXTERNAL_STORAGE_URL")+'ocs/v2.php/apps/files_sharing/api/v1/shares'
        ocs_headers = {'OCS-APIRequest': 'true',"Accept": "application/json"}
        ocs_auth = (storage_user, storage_password)  # Use app password or user/pass
        
        if not all([storage_url, storage_user, storage_password]):
            return jsonify({'error': 'External storage configuration missing'}), 500
        
        nc = Nextcloud(nextcloud_url=storage_url, nc_auth_user=storage_user, nc_auth_pass=storage_password)

        # Save file to uploads directory
        # upload_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], 'profile_images')
        buyer_base_dir_available = False
        buyer_image_profile_dir_available = False
        buyer_dir = f"buyer_{user_id}/"
        remote_dir_path = f"/Photos/{buyer_dir}"
        remote_base_profile_images_path = f"/Photos/{buyer_dir}/profile"
        # Make base dir for buyer
        try:
            nc.files.listdir(remote_dir_path)
            logging.debug(f"Found remote path:: {remote_dir_path}")
            buyer_base_dir_available = True
        except NextcloudException as e:
            if e.status_code != 404:
                raise e
            else:
                try:
                    logging.info(f"Could not locate remote directory::: {remote_dir_path}::: Proceeding to create")
                    nc.files.mkdir(remote_dir_path)
                    logging.debug(f"Created remote directory {remote_dir_path} successfully")
                    logging.debug("Now setting sharing permissions...")
                    dir_sharing_data = {
                        'path': remote_dir_path,         # Folder you created
                        'shareType': 3,                  # Public link
                        'permissions': 1                 # Read-only
                    }
                    response = requests.post(ocs_url, headers=ocs_headers, data=dir_sharing_data, auth=ocs_auth)

                    if response.status_code == 200:
                        logging.info(f"Response Text is:: {response}")
                        share_info = response.json()
                        link = share_info['ocs']['data']['url']
                        logging.debug(f"Public Share URL: {link}")
                        buyer_base_dir_available = True
                    else:
                        logging.debug("Failed to create share:", response.text)
                except Exception as e:
                    logging.debug(f"Exception while creating buyer base directory:{str(e)}")
                    return jsonify({"Exception": f"Failed to create buyer base directory -- {remote_dir_path} - the error is ::::{str(e)}"}), 500

        # If we have buyer base directory, check if we have buyer profile image directory
        if buyer_base_dir_available: 
            try:
                nc.files.listdir(remote_base_profile_images_path)
                logging.debug(f"Found remote path:: {remote_dir_path}")
                buyer_image_profile_dir_available = True
            except NextcloudException as e:
                if e.status_code != 404:
                    raise e
                else:
                    try:
                        logging.info(f"Could not locate buyer profile image directory::: {remote_base_profile_images_path}::: Proceeding to create")
                        nc.files.mkdir(remote_base_profile_images_path)
                        logging.debug(f"Created remote directory {remote_dir_path} successfully")
                        logging.debug("Now setting sharing permissions...")
                        dir_sharing_data = {
                            'path': remote_base_profile_images_path,         # Folder you created
                            'shareType': 3,                  # Public link
                            'permissions': 1                 # Read-only
                        }
                        response = requests.post(ocs_url, headers=ocs_headers, data=dir_sharing_data, auth=ocs_auth)
                        if response.status_code == 200:
                            logging.info(f"Response Text is:: {response}")
                            share_info = response.json()
                            link = share_info['ocs']['data']['url']
                            logging.debug(f"Public Share URL: {link}")
                            buyer_image_profile_dir_available = True
                        else:
                            logging.debug("Failed to create buyer profile image directtory:", response.text)
                    except Exception as e:
                        logging.debug(f"Exception while creating buyer buyer profile images directory:{str(e)}")
                        return jsonify({"Exception": f"Failed to create buyer bprofile imagesase directory -- {remote_base_profile_images_path} - the error is ::::{str(e)}"}), 500


        # Generate unique filename
        filename = secure_filename(f"buyer_{user_id}_{int(datetime.now().timestamp())}.{file.filename.rsplit('.', 1)[1].lower()}")

        # Prepare file data for upload
        file_data = file.read()
        file.seek(0)  # Reset for potential retry
            
        # Create basic auth header
        auth_string = f"{storage_user}:{storage_password}"
        auth_bytes = auth_string.encode('ascii')
        auth_b64 = base64.b64encode(auth_bytes).decode('ascii')

        # File upload URL
        upload_url = f"{remote_base_profile_images_path}/{filename}"
        
        # Public URL for storage and reading
        file_public_url=""
        
        # Upload file
        try:        
            buf = BytesIO(file_data)  
            buf.seek(0)
            logging.info(f"Uploading file :::: {upload_url}")
            uploaded_file = nc.files.upload_stream(upload_url, buf)
            logging.info(f"The uploaded file data is::: {(uploaded_file.name)}")
            # Now give it a publicly available link 
            seller_file_sharing_data = {
                'path': upload_url,              # Uploaded file
                'shareType': 3,                  # Public link
                'permissions': 1                 # Read-only
            }
            response = requests.post(ocs_url, headers=ocs_headers, data=seller_file_sharing_data, auth=ocs_auth)
            if response.status_code == 200:
                result = response.json()
                if result["ocs"]["meta"]["status"] == "ok":
                    file_public_url = result["ocs"]["data"]["url"]
                    logging.debug(f"Public share URL: {file_public_url}")
                else:
                    logging.error(f"Share API error: {result['ocs']['meta']['message']}")
            else:
                print("HTTP error:", response.status_code, response.text)
        except Exception as e:
            logging.debug(f"Exception while uploading file:{e}")
            return jsonify({'Exception': f'Failed to upload file {upload_url}:::{str(e)}'}), 500
        
        # Update profile with image URL
        image_url = file_public_url
        buyer_profile.profile_image = image_url
        
        db.session.commit()
        
        return jsonify({
            'message': 'Profile image uploaded successfully',
            'profile': buyer_profile.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': f'Failed to upload profile image: {str(e)}'
        }), 500

@buyer.route('/sellers', methods=['GET'])
@buyer_required
def get_sellers():
    """
    Endpoint to get list of sellers with proper profile data including state and country
    """
    import os
    from ..models.models import SellerProfile
    
    # Get query parameters for filtering
    search = request.args.get('search', '')
    specialty = request.args.get('specialty', '')
    
    # Build query to join users with seller_profiles
    query = db.session.query(User, SellerProfile).join(
        SellerProfile, User.id == SellerProfile.user_id
    ).filter(User.role == UserRole.SELLER.value)
    
    # Apply search filter if provided
    if search:
        query = query.filter(
            (User.username.ilike(f'%{search}%')) | 
            (User.business_name.ilike(f'%{search}%')) |
            (SellerProfile.business_name.ilike(f'%{search}%'))
        )
    
    # Execute query
    results = query.all()
    
    # Get PUBLIC_SITE_URL from environment
    public_site_url = os.getenv('PUBLIC_SITE_URL', 'http://localhost:3000')
    
    # Convert to response format
    seller_list = []
    for user, profile in results:
        # Handle microsite_url - prepend PUBLIC_SITE_URL if it's a relative path
        microsite_url = profile.microsite_url or ''
        if microsite_url and not microsite_url.startswith('http'):
            microsite_url = f"{public_site_url}{microsite_url}"
        
        seller_data = {
            'id': user.id,
            'name': user.username,
            'businessName': profile.business_name or user.business_name or '',
            'description': profile.description or user.business_description or '',
            'location': profile.state or 'Unknown',  # Display state instead of pincode
            'country': profile.country or 'Unknown',
            'address': profile.address or '',
            'pincode': profile.pincode or '',
            'seller_type': profile.seller_type or 'Not Specified',  # Include seller type
            'rating': 4.8,  # Placeholder - could be calculated from reviews
            'specialties': [interest.name for interest in profile.target_market_relationships],  # Dynamic specialties from database
            'image_url': profile.logo_url or '/images/sellers/default.jpg',
            'isVerified': profile.is_verified,
            'stallNo': f"A{user.id:02d}",  # Placeholder
            'website': profile.website or '',
            'microsite_url': microsite_url,
            'contactEmail': profile.contact_email or user.email,
            'contactPhone': profile.contact_phone or ''
        }
        
        # Filter by specialty if provided (placeholder logic)
        if specialty and specialty not in seller_data['specialties']:
            continue
        
        # Check meeting status
        user_id = get_jwt_identity()
        if isinstance(user_id, str):
            try:
                user_id = int(user_id)
            except ValueError:
                user_id = None
        
        if user_id:
            meeting = Meeting.query.filter_by(buyer_id=user_id, seller_id=user.id).order_by(Meeting.created_at.desc()).first()
            if meeting:
                seller_data['meetingStatus'] = meeting.status.value
            else:
                seller_data['meetingStatus'] = 'none'
        else:
            seller_data['meetingStatus'] = 'none'
        
        seller_list.append(seller_data)
    
    return jsonify({
        'sellers': seller_list
    }), 200
