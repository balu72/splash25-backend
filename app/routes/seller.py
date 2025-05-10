from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, date
from ..utils.auth import seller_required
from ..models import db, User, UserRole, TravelPlan, Listing, ListingStatus, ListingDate, Meeting, MeetingStatus

seller = Blueprint('seller', __name__, url_prefix='/api/seller')

@seller.route('/dashboard', methods=['GET'])
@seller_required
def dashboard():
    """
    Endpoint for seller dashboard data
    """
    user_id = get_jwt_identity()
    
    # Get seller's listings
    listings = Listing.query.filter_by(seller_id=user_id).all()
    
    # Calculate stats
    total_listings = len(listings)
    active_listings = sum(1 for listing in listings if listing.status == ListingStatus.ACTIVE)
    total_views = sum(listing.views for listing in listings)
    total_bookings = sum(listing.bookings for listing in listings)
    revenue = sum(listing.price * listing.bookings for listing in listings)
    
    # Get recent bookings (placeholder)
    recent_bookings = [
        {
            'id': 1,
            'customer_name': 'John Doe',
            'event': 'Wayanad Nature Camp',
            'date': '2025-06-15',
            'participants': 2,
            'status': 'confirmed'
        },
        {
            'id': 2,
            'customer_name': 'Jane Smith',
            'event': 'Splash25 Trekking Adventure',
            'date': '2025-07-10',
            'participants': 4,
            'status': 'pending'
        }
    ]
    
    # Get seller's verification status
    user = User.query.get(user_id)
    verification_status = {
        'is_verified': user.is_verified,
        'pending_documents': []
    }
    
    return jsonify({
        'message': 'Welcome to the Seller Dashboard',
        'business_stats': {
            'total_listings': total_listings,
            'active_listings': active_listings,
            'total_views': total_views,
            'total_bookings': total_bookings,
            'revenue': revenue
        },
        'recent_bookings': recent_bookings,
        'verification_status': verification_status
    }), 200

@seller.route('/travel-plans', methods=['GET'])
@seller_required
def get_travel_plans():
    """
    Endpoint to get seller's travel plans
    """
    user_id = get_jwt_identity()
    
    # Fetch travel plans for the user
    travel_plans = TravelPlan.query.filter_by(user_id=user_id).all()
    
    return jsonify({
        'travel_plans': [plan.to_dict() for plan in travel_plans]
    }), 200

@seller.route('/meetings', methods=['GET'])
@seller_required
def get_meetings():
    """
    Endpoint to get seller's meetings
    """
    user_id = get_jwt_identity()
    
    # Get query parameters for filtering
    status = request.args.get('status')
    from_date = request.args.get('from_date')
    to_date = request.args.get('to_date')
    
    # Build query
    query = Meeting.query.filter_by(seller_id=user_id)
    
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
        'meetings': [meeting.to_dict_for_seller() for meeting in meetings]
    }), 200

@seller.route('/meetings/<int:meeting_id>', methods=['PUT'])
@seller_required
def update_meeting(meeting_id):
    """
    Endpoint to update meeting status
    """
    user_id = get_jwt_identity()
    data = request.get_json()
    
    # Validate required fields
    if 'status' not in data:
        return jsonify({'error': 'Missing required field: status'}), 400
    
    # Check if meeting exists and belongs to the user
    meeting = Meeting.query.filter_by(id=meeting_id, seller_id=user_id).first()
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
        'meeting': meeting.to_dict_for_seller()
    }), 200

@seller.route('/buyers', methods=['GET'])
@seller_required
def get_buyers():
    """
    Endpoint to get list of buyers interested in the seller
    """
    user_id = get_jwt_identity()
    
    # Get query parameters for filtering
    search = request.args.get('search', '')
    interest_level = request.args.get('interest_level', '')
    
    # Get buyers who have requested meetings with this seller
    meetings = Meeting.query.filter_by(seller_id=user_id).all()
    buyer_ids = set(meeting.buyer_id for meeting in meetings)
    
    # Get buyer details
    buyers = User.query.filter(User.id.in_(buyer_ids)).all()
    
    # Convert to response format
    buyer_list = []
    for buyer in buyers:
        # In a real application, you would fetch additional data like interest level, etc.
        # For now, we'll use placeholder data
        buyer_data = {
            'id': buyer.id,
            'name': buyer.username,
            'organization': 'Organization',  # Placeholder
            'interestLevel': 'high',  # Placeholder
            'lastContact': date.today().isoformat(),  # Placeholder
            'email': buyer.email,
            'phone': '+1 555-123-4567'  # Placeholder
        }
        
        # Apply search filter if provided
        if search and search.lower() not in buyer.username.lower():
            continue
        
        # Apply interest level filter if provided
        if interest_level and interest_level != buyer_data['interestLevel']:
            continue
        
        buyer_list.append(buyer_data)
    
    return jsonify({
        'buyers': buyer_list
    }), 200

@seller.route('/listings', methods=['GET'])
@seller_required
def get_listings():
    """
    Endpoint to get seller's listings
    """
    user_id = get_jwt_identity()
    
    # Fetch listings from the database
    listings = Listing.query.filter_by(seller_id=user_id).all()
    
    return jsonify({
        'message': 'Seller listings',
        'listings': [listing.to_dict() for listing in listings]
    }), 200

@seller.route('/listings', methods=['POST'])
@seller_required
def create_listing():
    """
    Endpoint to create a new listing
    """
    user_id = get_jwt_identity()
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['name', 'description', 'price', 'duration', 'location', 'max_participants', 'available_dates']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Create new listing
    try:
        listing = Listing(
            seller_id=user_id,
            name=data['name'],
            description=data['description'],
            price=float(data['price']),
            duration=data['duration'],
            location=data['location'],
            max_participants=int(data['max_participants']),
            status=ListingStatus.ACTIVE,
            image_url=data.get('image_url', '/images/listings/default.jpg')
        )
        db.session.add(listing)
        db.session.flush()  # Get the listing ID
        
        # Add available dates
        for date_str in data['available_dates']:
            listing_date = ListingDate(
                listing_id=listing.id,
                date=datetime.fromisoformat(date_str).date()
            )
            db.session.add(listing_date)
        
        db.session.commit()
    except ValueError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
    
    return jsonify({
        'message': 'Listing created successfully',
        'listing': listing.to_dict()
    }), 201

@seller.route('/listings/<int:listing_id>', methods=['PUT'])
@seller_required
def update_listing(listing_id):
    """
    Endpoint to update an existing listing
    """
    user_id = get_jwt_identity()
    data = request.get_json()
    
    # Check if listing exists and belongs to the user
    listing = Listing.query.filter_by(id=listing_id, seller_id=user_id).first()
    if not listing:
        return jsonify({'error': 'Listing not found or access denied'}), 404
    
    # Update listing fields
    if 'name' in data:
        listing.name = data['name']
    if 'description' in data:
        listing.description = data['description']
    if 'price' in data:
        listing.price = float(data['price'])
    if 'duration' in data:
        listing.duration = data['duration']
    if 'location' in data:
        listing.location = data['location']
    if 'max_participants' in data:
        listing.max_participants = int(data['max_participants'])
    if 'status' in data:
        try:
            listing.status = ListingStatus(data['status'])
        except ValueError:
            return jsonify({'error': f'Invalid status: {data["status"]}'}), 400
    if 'image_url' in data:
        listing.image_url = data['image_url']
    
    # Update available dates if provided
    if 'available_dates' in data:
        # Remove existing dates
        ListingDate.query.filter_by(listing_id=listing_id).delete()
        
        # Add new dates
        for date_str in data['available_dates']:
            listing_date = ListingDate(
                listing_id=listing.id,
                date=datetime.fromisoformat(date_str).date()
            )
            db.session.add(listing_date)
    
    db.session.commit()
    
    return jsonify({
        'message': 'Listing updated successfully',
        'listing': listing.to_dict()
    }), 200

@seller.route('/profile', methods=['GET'])
@seller_required
def get_profile():
    """
    Endpoint to get seller profile information
    """
    user_id = get_jwt_identity()
    
    # Fetch user from the database
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({
        'message': 'Seller profile information',
        'profile': {
            'business_name': user.business_name or '',
            'business_description': user.business_description or '',
            'contact_info': {
                'email': user.email,
                'phone': '+91 9496417855',  # Placeholder
                'address': 'Wayanad Tourism Organisation, Vasudeva Edom, Pozhuthana PO, Wayanad, Kerala, India. 673 575'  # Placeholder
            },
            'verification': {
                'status': 'verified' if user.is_verified else 'pending',
                'documents': [
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
                ]
            }
        }
    }), 200

@seller.route('/profile', methods=['PUT'])
@seller_required
def update_profile():
    """
    Endpoint to update seller profile information
    """
    user_id = get_jwt_identity()
    data = request.get_json()
    
    # Fetch user from the database
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Update user fields
    if 'business_name' in data:
        user.business_name = data['business_name']
    if 'business_description' in data:
        user.business_description = data['business_description']
    
    db.session.commit()
    
    return jsonify({
        'message': 'Profile updated successfully',
        'profile': {
            'business_name': user.business_name or '',
            'business_description': user.business_description or '',
            'contact_info': {
                'email': user.email,
                'phone': '+91 9496417855',  # Placeholder
                'address': 'Wayanad Tourism Organisation, Vasudeva Edom, Pozhuthana PO, Wayanad, Kerala, India. 673 575'  # Placeholder
            },
            'verification': {
                'status': 'verified' if user.is_verified else 'pending',
                'documents': [
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
                ]
            }
        }
    }), 200
