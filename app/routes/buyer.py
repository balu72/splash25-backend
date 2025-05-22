from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from ..utils.auth import buyer_required
from ..models import db, User, TravelPlan, Transportation, Accommodation, GroundTransportation, Meeting, MeetingStatus, UserRole, TimeSlot, SystemSetting

buyer = Blueprint('buyer', __name__, url_prefix='/api/buyer')

@buyer.route('/dashboard', methods=['GET'])
@buyer_required
def dashboard():
    """
    Endpoint for buyer dashboard data
    """
    # This is a placeholder for actual dashboard data
    # In a real application, you would fetch relevant data for the buyer
    return jsonify({
        'message': 'Welcome to the Buyer Dashboard',
        'featured_destinations': [
            {
                'id': 1,
                'name': 'Wayanad Wildlife Sanctuary',
                'description': 'Experience the rich biodiversity of Wayanad',
                'image_url': '/images/destinations/wayanad-wildlife.jpg'
            },
            {
                'id': 2,
                'name': 'Chembra Peak',
                'description': 'Trek to the heart-shaped lake at the summit',
                'image_url': '/images/destinations/chembra-peak.jpg'
            },
            {
                'id': 3,
                'name': 'Edakkal Caves',
                'description': 'Explore ancient petroglyphs dating back to 6000 BCE',
                'image_url': '/images/destinations/edakkal-caves.jpg'
            }
        ],
        'upcoming_events': [
            {
                'id': 1,
                'name': 'Wayanad Nature Camp',
                'date': '2025-06-15',
                'location': 'Muthanga Wildlife Sanctuary'
            },
            {
                'id': 2,
                'name': 'Splash25 Trekking Adventure',
                'date': '2025-07-10',
                'location': 'Chembra Peak'
            }
        ]
    }), 200

@buyer.route('/profile', methods=['GET'])
@buyer_required
def profile():
    """
    Endpoint to get buyer profile information
    """
    # In a real application, you would fetch the user from the database
    # based on the JWT identity
    return jsonify({
        'message': 'Buyer profile information',
        'profile': {
            'preferences': {
                'interests': ['Wildlife', 'Trekking', 'Cultural Experiences'],
                'notification_settings': {
                    'email': True,
                    'sms': False
                }
            },
            'recent_activity': [
                {
                    'type': 'viewed',
                    'item': 'Wayanad Wildlife Sanctuary',
                    'timestamp': '2025-05-08T14:30:00Z'
                },
                {
                    'type': 'saved',
                    'item': 'Chembra Peak Trek',
                    'timestamp': '2025-05-07T09:15:00Z'
                }
            ]
        }
    }), 200

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
    
    # Update outbound journey details
    if not travel_plan.transportation:
        # Create new transportation record if it doesn't exist
        transportation = Transportation(
            travel_plan_id=plan_id,
            type='flight',  # Default type
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
    
    # Update return journey details
    if not travel_plan.transportation:
        # Create new transportation record if it doesn't exist
        transportation = Transportation(
            travel_plan_id=plan_id,
            type='flight',  # Default type
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
        travel_plan.ground_transportation.pickup_vehicle_type = data.get('vehicleType', '')
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
        travel_plan.ground_transportation.dropoff_vehicle_type = data.get('vehicleType', '')
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
    
    if from_date:
        try:
            from_datetime = datetime.fromisoformat(from_date)
            query = query.filter(Meeting.from_time >= from_datetime)
        except ValueError:
            return jsonify({'error': f'Invalid from_date format: {from_date}'}), 400
    
    if to_date:
        try:
            to_datetime = datetime.fromisoformat(to_date)
            query = query.filter(Meeting.from_time <= to_datetime)
        except ValueError:
            return jsonify({'error': f'Invalid to_date format: {to_date}'}), 400
    
    # Execute query
    meetings = query.all()
    
    return jsonify({
        'meetings': [meeting.to_dict_for_buyer() for meeting in meetings]
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
    
    # Validate required fields - aligning with meeting.py structure
    required_fields = ['seller_id', 'time_slot_id']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Check if meetings are enabled (similar to meeting.py)
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
        notes=data.get('notes', ''), # Assuming 'topic' might become 'notes'
        status=MeetingStatus.PENDING # PENDING is used in meeting.py
    )
    
    # Mark the time slot as unavailable (similar to meeting.py)
    time_slot.is_available = False
    # time_slot.meeting_id = meeting.id # This needs meeting.id, so commit meeting first or handle differently
    
    db.session.add(meeting)
    db.session.commit() # Commit to get meeting.id

    # Now link meeting_id to time_slot if your model supports it and it's desired here
    if hasattr(time_slot, 'meeting_id'):
        time_slot.meeting_id = meeting.id
        db.session.commit()
    
    return jsonify({
        'message': 'Meeting request created successfully',
        'meeting': meeting.to_dict_for_buyer() # Ensure to_dict_for_buyer is consistent
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
        'meeting': meeting.to_dict_for_buyer()
    }), 200

@buyer.route('/sellers', methods=['GET'])
@buyer_required
def get_sellers():
    """
    Endpoint to get list of sellers
    """
    # Get query parameters for filtering
    search = request.args.get('search', '')
    specialty = request.args.get('specialty', '')
    
    # Build query
    query = User.query.filter_by(role=UserRole.SELLER)
    
    # Apply filters if provided
    if search:
        query = query.filter(
            (User.username.ilike(f'%{search}%')) | 
            (User.business_name.ilike(f'%{search}%'))
        )
    
    # Execute query
    sellers = query.all()
    
    # Convert to response format
    seller_list = []
    for seller in sellers:
        # In a real application, you would fetch additional data like ratings, specialties, etc.
        seller_data = {
            'id': seller.id,
            'name': seller.username,
            'businessName': seller.business_name or '',
            'description': seller.business_description or '',
            'rating': 4.8,  # Placeholder
            'specialties': ['Wildlife Tours', 'Camping', 'Nature Photography'],  # Placeholder
            'image_url': '/images/sellers/default.jpg',  # Placeholder
            'isVerified': seller.is_verified,
            'stallNo': f"A{seller.id:02d}"  # Placeholder
        }
        
        # Filter by specialty if provided
        if specialty and specialty not in seller_data['specialties']:
            continue
        
        # Check meeting status
        user_id = get_jwt_identity()
        meeting = Meeting.query.filter_by(buyer_id=user_id, seller_id=seller.id).order_by(Meeting.created_at.desc()).first()
        if meeting:
            seller_data['meetingStatus'] = meeting.status.value
        else:
            seller_data['meetingStatus'] = 'none'
        
        seller_list.append(seller_data)
    
    return jsonify({
        'sellers': seller_list
    }), 200
