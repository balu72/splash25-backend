from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timedelta
from ..models import db, TimeSlot, User, UserRole
from ..utils.auth import seller_required

timeslot = Blueprint('timeslot', __name__, url_prefix='/api/timeslots')

@timeslot.route('', methods=['GET'])
@jwt_required()
def get_timeslots():
    """Get time slots with optional filtering"""
    user_id = request.args.get('user_id')
    date_str = request.args.get('date')
    
    query = TimeSlot.query
    
    # Filter by user_id if provided
    if user_id:
        query = query.filter_by(user_id=user_id)
    
    # Filter by date if provided
    if date_str:
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            next_day = date_obj + timedelta(days=1)
            query = query.filter(TimeSlot.start_time >= date_obj, TimeSlot.start_time < next_day)
        except ValueError:
            return jsonify({
                'error': 'Invalid date format. Use YYYY-MM-DD'
            }), 400
    
    # Get the current user
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    
    # If the user is a seller, only show their own time slots
    if current_user.role == UserRole.SELLER and not user_id:
        query = query.filter_by(user_id=current_user_id)
    
    # Execute the query
    timeslots = query.all()
    
    return jsonify({
        'timeslots': [t.to_dict() for t in timeslots]
    }), 200

@timeslot.route('', methods=['POST'])
@jwt_required()
@seller_required
def create_timeslots():
    """Create time slots for a seller"""
    data = request.get_json()
    user_id = get_jwt_identity()
    
    # Validate required fields
    required_fields = ['start_date', 'end_date']
    for field in required_fields:
        if field not in data:
            return jsonify({
                'error': f'Missing required field: {field}'
            }), 400
    
    try:
        # Parse dates
        start_date = datetime.strptime(data['start_date'], '%Y-%m-%d')
        end_date = datetime.strptime(data['end_date'], '%Y-%m-%d')
        
        # Validate date range
        if start_date > end_date:
            return jsonify({
                'error': 'Start date must be before end date'
            }), 400
        
        if start_date < datetime.now():
            return jsonify({
                'error': 'Start date cannot be in the past'
            }), 400
        
        # Limit to 90 days in the future
        max_date = datetime.now() + timedelta(days=90)
        if end_date > max_date:
            return jsonify({
                'error': 'End date cannot be more than 90 days in the future'
            }), 400
        
        # Create time slots for each day in the range
        current_date = start_date
        created_slots = 0
        
        while current_date <= end_date:
            # Start at 9 AM
            start_hour = 9
            
            # Create slots until 5 PM (17:00)
            while start_hour < 17:
                for minute in [0, 15, 30, 45]:
                    # Create the start and end times for this slot
                    slot_start = datetime.combine(current_date.date(), datetime.min.time().replace(hour=start_hour, minute=minute))
                    slot_end = slot_start + timedelta(minutes=15)
                    
                    # Skip if this slot is in the past
                    if slot_start < datetime.now():
                        continue
                    
                    # Check if this slot already exists
                    existing_slot = TimeSlot.query.filter_by(
                        user_id=user_id,
                        start_time=slot_start,
                        end_time=slot_end
                    ).first()
                    
                    if not existing_slot:
                        # Create the time slot
                        time_slot = TimeSlot(
                            user_id=user_id,
                            start_time=slot_start,
                            end_time=slot_end,
                            is_available=True
                        )
                        db.session.add(time_slot)
                        created_slots += 1
                
                # Move to the next hour
                start_hour += 1
            
            # Move to the next day
            current_date += timedelta(days=1)
        
        db.session.commit()
        
        return jsonify({
            'message': f'Successfully created {created_slots} time slots',
            'created_slots': created_slots
        }), 201
        
    except ValueError as e:
        return jsonify({
            'error': f'Invalid date format: {str(e)}'
        }), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': f'Error creating time slots: {str(e)}'
        }), 500

@timeslot.route('/<int:timeslot_id>', methods=['DELETE'])
@jwt_required()
@seller_required
def delete_timeslot(timeslot_id):
    """Delete a time slot"""
    user_id = get_jwt_identity()
    
    # Find the time slot
    time_slot = TimeSlot.query.get(timeslot_id)
    
    if not time_slot:
        return jsonify({
            'error': 'Time slot not found'
        }), 404
    
    # Check if the time slot belongs to the current user
    if time_slot.user_id != user_id:
        return jsonify({
            'error': 'You do not have permission to delete this time slot'
        }), 403
    
    # Check if the time slot is already booked
    if not time_slot.is_available:
        return jsonify({
            'error': 'Cannot delete a booked time slot'
        }), 400
    
    # Delete the time slot
    db.session.delete(time_slot)
    db.session.commit()
    
    return jsonify({
        'message': 'Time slot deleted successfully'
    }), 200

@timeslot.route('/bulk-delete', methods=['POST'])
@jwt_required()
@seller_required
def bulk_delete_timeslots():
    """Delete multiple time slots for a date range"""
    data = request.get_json()
    user_id = get_jwt_identity()
    
    # Validate required fields
    required_fields = ['start_date', 'end_date']
    for field in required_fields:
        if field not in data:
            return jsonify({
                'error': f'Missing required field: {field}'
            }), 400
    
    try:
        # Parse dates
        start_date = datetime.strptime(data['start_date'], '%Y-%m-%d')
        end_date = datetime.strptime(data['end_date'], '%Y-%m-%d')
        
        # Validate date range
        if start_date > end_date:
            return jsonify({
                'error': 'Start date must be before end date'
            }), 400
        
        # Find all available time slots in the date range
        next_day = end_date + timedelta(days=1)
        time_slots = TimeSlot.query.filter(
            TimeSlot.user_id == user_id,
            TimeSlot.start_time >= start_date,
            TimeSlot.start_time < next_day,
            TimeSlot.is_available == True
        ).all()
        
        # Delete the time slots
        for time_slot in time_slots:
            db.session.delete(time_slot)
        
        db.session.commit()
        
        return jsonify({
            'message': f'Successfully deleted {len(time_slots)} time slots',
            'deleted_slots': len(time_slots)
        }), 200
        
    except ValueError as e:
        return jsonify({
            'error': f'Invalid date format: {str(e)}'
        }), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': f'Error deleting time slots: {str(e)}'
        }), 500
