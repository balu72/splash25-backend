from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from ..models import db, Meeting, TimeSlot, User, UserRole, MeetingStatus, SystemSetting
from ..utils.auth import buyer_required, seller_required
import logging

meeting = Blueprint('meeting', __name__, url_prefix='/api/meetings')

@meeting.route('', methods=['GET'])
@jwt_required()
def get_meetings():
    """Get meetings for the current user"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({
            'error': 'User not found'
        }), 404
    
    # Get meetings based on user role
    if user.role == UserRole.BUYER.value:
        meetings = Meeting.query.filter_by(buyer_id=user_id).all()
    elif user.role == UserRole.SELLER.value:
        meetings = Meeting.query.filter_by(seller_id=user_id).all()
    elif user.role == UserRole.ADMIN.value:
        # Admins can see all meetings
        meetings = Meeting.query.all()
    else:
        return jsonify({
            'error': 'Invalid user role'
        }), 400
    
    return jsonify({
        'meetings': [m.to_dict() for m in meetings]
    }), 200

@meeting.route('/<int:meeting_id>', methods=['GET'])
@jwt_required()
def get_meeting(meeting_id):
    """Get a specific meeting"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({
            'error': 'User not found'
        }), 404
    
    meeting = Meeting.query.get(meeting_id)
    
    if not meeting:
        return jsonify({
            'error': 'Meeting not found'
        }), 404
    
    # Check if the user has permission to view this meeting
    if user.role == UserRole.BUYER.value and meeting.buyer_id != user_id:
        return jsonify({
            'error': 'You do not have permission to view this meeting'
        }), 403
    
    if user.role == UserRole.SELLER.value and meeting.seller_id != user_id:
        return jsonify({
            'error': 'You do not have permission to view this meeting'
        }), 403
    
    return jsonify({
        'meeting': meeting.to_dict()
    }), 200

@meeting.route('/buyer/request', methods=['POST'])
@jwt_required()
@buyer_required
def create_buyer_meeting_request():
    """Create a new meeting request by the buyer"""
    data = request.get_json()
    buyer_id = get_jwt_identity()
    
    # Validate required fields
    required_fields = ['requested_id']  
    for field in required_fields:
        if field not in data:
            return jsonify({
                'error': f'Missing required field: {field}'
            }), 400
    
    # Check if meetings are enabled
    meetings_enabled = SystemSetting.query.filter_by(key='meetings_enabled').first()
    if not meetings_enabled or meetings_enabled.value != 'true':
        return jsonify({
            'error': 'Meeting requests are currently disabled'
        }), 400
    
    # ✅ FIX: Convert requested_id to integer to fix data type mismatch
    try:
        seller_id = int(data['requested_id'])
    except (ValueError, TypeError):
        return jsonify({
            'error': 'Invalid seller ID format'
        }), 400
    
    # Check if the seller exists
    seller = User.query.get(seller_id)
    if not seller or seller.role != UserRole.SELLER.value:
        return jsonify({
            'error': 'Invalid seller'
        }), 400
    """
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
    """
    # Check for existing meeting
    meeting = Meeting.query.filter_by(buyer_id=buyer_id, seller_id=seller_id).first()
    if meeting:
        # ✅ ENHANCEMENT: Check if existing meeting status allows new request
        # Get status as lowercase string for case-insensitive comparison
        if hasattr(meeting.status, 'value'):
            status_lower = meeting.status.value.lower()
        else:
            status_lower = str(meeting.status).lower()
        
        # Allow new meeting if previous was cancelled or expired
        if status_lower not in ['cancelled', 'expired']:
            return jsonify({
                'error': f'Meeting request already exists with status: {meeting.status.value if hasattr(meeting.status, "value") else meeting.status}'
            }), 400
        
        # If cancelled or expired, we'll create a new meeting (continue with creation)
    
    # Create the meeting
    meeting = Meeting(
        buyer_id=buyer_id,
        seller_id=seller_id,
        requestor_id=buyer_id,  # Set requestor_id to current buyer
        #time_slot_id=data['time_slot_id'],
        notes=data.get('notes', ''),
        status=MeetingStatus.PENDING
    )
    
    # Mark the time slot as unavailable
    #time_slot.is_available = False
    #time_slot.meeting_id = meeting.id
    
    db.session.add(meeting)
    db.session.commit()
    
    return jsonify({
        'message': 'Meeting request created successfully',
        'meeting': meeting.to_dict()
    }), 201

@meeting.route('/seller/request', methods=['POST'])
@jwt_required()
@seller_required
def create_seller_meeting_request():
    """Create a new meeting request by the seller"""
    data = request.get_json()
    seller_id = get_jwt_identity()
    
    # Validate required fields
    required_fields = ['requested_id']  
    for field in required_fields:
        if field not in data:
            return jsonify({
                'error': f'Missing required field: {field}'
            }), 400
    
    # Check if meetings are enabled
    meetings_enabled = SystemSetting.query.filter_by(key='meetings_enabled').first()
    if not meetings_enabled or meetings_enabled.value != 'true':
        return jsonify({
            'error': 'Meeting requests are currently disabled'
        }), 400
    
    # ✅ FIX: Convert requested_id to integer to fix data type mismatch
    try:
        buyer_id = int(data['requested_id'])
    except (ValueError, TypeError):
        return jsonify({
            'error': 'Invalid buyer ID format'
        }), 400
    
    # Check if the buyer exists
    buyer = User.query.get(buyer_id)
    if not buyer or buyer.role != UserRole.BUYER.value:
        return jsonify({
            'error': 'Invalid buyer'
        }), 400

    # Check for existing meeting
    meeting = Meeting.query.filter_by(buyer_id=buyer_id, seller_id=seller_id).first()
    if meeting:
        # ✅ ENHANCEMENT: Check if existing meeting status allows new request
        # Get status as lowercase string for case-insensitive comparison
        if hasattr(meeting.status, 'value'):
            status_lower = meeting.status.value.lower()
        else:
            status_lower = str(meeting.status).lower()
        
        # Allow new meeting if previous was cancelled or expired
        if status_lower not in ['cancelled', 'expired']:
            return jsonify({
                'error': f'Meeting request already exists with status: {meeting.status.value if hasattr(meeting.status, "value") else meeting.status}'
            }), 400
        
        # If cancelled or expired, we'll create a new meeting (continue with creation)
    
    # Create the meeting
    meeting = Meeting(
        buyer_id=buyer_id,
        seller_id=seller_id,
        requestor_id=seller_id,  # Set requestor_id to current seller
        #time_slot_id=data['time_slot_id'],
        notes=data.get('notes', ''),
        status=MeetingStatus.PENDING
    )
    
    # Mark the time slot as unavailable
    #time_slot.is_available = False
    #time_slot.meeting_id = meeting.id
    
    db.session.add(meeting)
    db.session.commit()
    
    return jsonify({
        'message': 'Meeting request created successfully',
        'meeting': meeting.to_dict()
    }), 201


@meeting.route('/<int:meeting_id>/status', methods=['PUT'])
@jwt_required()
def update_meeting_status(meeting_id):
    """Update the status of a meeting (accept/reject) - available to both buyers and sellers"""
    data = request.get_json()
    user_id = int(get_jwt_identity())
    
    # Validate required fields
    if 'status' not in data:
        return jsonify({
            'error': 'Missing required field: status'
        }), 400
    
    # Validate status value
    try:
        new_status = MeetingStatus(data['status'])
        if new_status not in [MeetingStatus.ACCEPTED, MeetingStatus.REJECTED]:
            return jsonify({
                'error': 'Invalid status. Must be "accepted" or "rejected"'
            }), 400
    except ValueError:
        return jsonify({
            'error': 'Invalid status value'
        }), 400
    
    # Get the meeting
    meeting = Meeting.query.get(meeting_id)
    
    if not meeting:
        return jsonify({
            'error': 'Meeting not found'
        }), 404
    
    # Get the user to check role
    user = User.query.get(user_id)
    if not user:
        return jsonify({
            'error': 'User not found'
        }), 404
    
    # Check if the user has permission to update this meeting
    # Admins can update any meeting, others must be participants
    if user.role != UserRole.ADMIN.value:
        if meeting.buyer_id != user_id and meeting.seller_id != user_id:
            logging.debug(f"User {user_id} does not have permission to update meeting {meeting_id}")
            return jsonify({
                'error': 'You do not have permission to update this meeting'
            }), 403
        
        # Check if the user is the requestor (requestors cannot accept/reject their own requests)
        # This restriction doesn't apply to admins
        if meeting.requestor_id == user_id:
            logging.debug(f"User {user_id} cannot accept/reject their own meeting request")
            return jsonify({
                'error': 'You cannot accept or reject your own meeting request'
            }), 403
    
    # Check if the meeting is in a pending state
    if meeting.status != MeetingStatus.PENDING:
        logging.debug(f"Cannot update meeting {meeting_id}. Current status: {meeting.status.value}")
        return jsonify({
            'error': f'Cannot update meeting status. Current status: {meeting.status.value}'
        }), 400
    
    # Update the meeting status
    meeting.status = new_status
    
    # If rejected, free up the time slot
    if new_status == MeetingStatus.REJECTED and meeting.time_slot:
        meeting.time_slot.is_available = True
        meeting.time_slot.meeting_id = None
    
    db.session.commit()
    
    return jsonify({
        'message': f'Meeting {new_status.value} successfully',
        'meeting': meeting.to_dict()
    }), 200

@meeting.route('/<int:meeting_id>', methods=['DELETE'])
@jwt_required()
def cancel_meeting(meeting_id):
    """Cancel a meeting"""
    user_id = get_jwt_identity()
    
    # Get the meeting
    meeting = Meeting.query.get(meeting_id)
    
    if not meeting:
        return jsonify({
            'error': 'Meeting not found'
        }), 404
    
    # Check if the user has permission to cancel this meeting
    if meeting.buyer_id != user_id and meeting.seller_id != user_id:
        return jsonify({
            'error': 'You do not have permission to cancel this meeting'
        }), 403
    
    # Check if the meeting can be cancelled
    if meeting.status not in [MeetingStatus.PENDING, MeetingStatus.ACCEPTED]:
        return jsonify({
            'error': f'Cannot cancel meeting with status: {meeting.status.value}'
        }), 400
    
    # Update the meeting status
    meeting.status = MeetingStatus.CANCELLED
    
    # Free up the time slot
    if meeting.time_slot:
        meeting.time_slot.is_available = True
        meeting.time_slot.meeting_id = None
    
    db.session.commit()
    
    return jsonify({
        'message': 'Meeting cancelled successfully'
    }), 200
