from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from ..models import db, Meeting, TimeSlot, User, UserRole, MeetingStatus, SystemSetting
from ..utils.auth import buyer_required, seller_required

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
    if user.role == UserRole.BUYER:
        meetings = Meeting.query.filter_by(buyer_id=user_id).all()
    elif user.role == UserRole.SELLER:
        meetings = Meeting.query.filter_by(seller_id=user_id).all()
    elif user.role == UserRole.ADMIN:
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
    if user.role == UserRole.BUYER and meeting.buyer_id != user_id:
        return jsonify({
            'error': 'You do not have permission to view this meeting'
        }), 403
    
    if user.role == UserRole.SELLER and meeting.seller_id != user_id:
        return jsonify({
            'error': 'You do not have permission to view this meeting'
        }), 403
    
    return jsonify({
        'meeting': meeting.to_dict()
    }), 200

@meeting.route('', methods=['POST'])
@jwt_required()
@buyer_required
def create_meeting():
    """Create a new meeting request"""
    data = request.get_json()
    buyer_id = get_jwt_identity()
    
    # Validate required fields
    required_fields = ['seller_id', 'time_slot_id']
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
        buyer_id=buyer_id,
        seller_id=data['seller_id'],
        time_slot_id=data['time_slot_id'],
        notes=data.get('notes', ''),
        status=MeetingStatus.PENDING
    )
    
    # Mark the time slot as unavailable
    time_slot.is_available = False
    time_slot.meeting_id = meeting.id
    
    db.session.add(meeting)
    db.session.commit()
    
    return jsonify({
        'message': 'Meeting request created successfully',
        'meeting': meeting.to_dict()
    }), 201

@meeting.route('/<int:meeting_id>/status', methods=['PUT'])
@jwt_required()
@seller_required
def update_meeting_status(meeting_id):
    """Update the status of a meeting (accept/reject)"""
    data = request.get_json()
    seller_id = get_jwt_identity()
    
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
    
    # Check if the meeting belongs to the seller
    if meeting.seller_id != seller_id:
        return jsonify({
            'error': 'You do not have permission to update this meeting'
        }), 403
    
    # Check if the meeting is in a pending state
    if meeting.status != MeetingStatus.PENDING:
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
