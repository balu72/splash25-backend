from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..utils.auth import admin_required
from ..models import db, SystemSetting
import json

system = Blueprint('system', __name__, url_prefix='/api/system')

@system.route('/settings', methods=['GET'])
@jwt_required()
def get_system_settings():
    """Get all system settings"""
    settings = SystemSetting.query.all()
    return jsonify({
        'settings': [s.to_dict() for s in settings]
    }), 200

@system.route('/settings', methods=['PUT'])
@admin_required
def update_system_settings():
    """Update system settings (admin only)"""
    data = request.get_json()
    
    for key, value in data.items():
        setting = SystemSetting.query.filter_by(key=key).first()
        if setting:
            setting.value = value
        else:
            setting = SystemSetting(
                key=key,
                value=value,
                description=f"Setting for {key}"
            )
            db.session.add(setting)
    
    db.session.commit()
    
    return jsonify({
        'message': 'Settings updated successfully',
        'settings': [s.to_dict() for s in SystemSetting.query.all()]
    }), 200

@system.route('/settings/initialize', methods=['POST'])
@admin_required
def initialize_system_settings():
    """Initialize default system settings (admin only)"""
    # Check if settings already exist
    if SystemSetting.query.count() > 0:
        return jsonify({
            'message': 'Settings already initialized'
        }), 400
    
    # Default settings
    default_settings = [
        {
            'key': 'meetings_enabled',
            'value': 'true',
            'description': 'Enable/disable meeting requests globally'
        },
        {
            'key': 'registration_enabled',
            'value': 'true',
            'description': 'Enable/disable user registration'
        },
        {
            'key': 'maintenance_mode',
            'value': 'false',
            'description': 'Enable/disable maintenance mode'
        }
    ]
    
    for setting_data in default_settings:
        setting = SystemSetting(**setting_data)
        db.session.add(setting)
    
    db.session.commit()
    
    return jsonify({
        'message': 'Default settings initialized successfully',
        'settings': [s.to_dict() for s in SystemSetting.query.all()]
    }), 201

@system.route('/settings/<string:key>', methods=['GET'])
@jwt_required()
def get_system_setting(key):
    """Get a specific system setting by key"""
    setting = SystemSetting.query.filter_by(key=key).first()
    
    if not setting:
        return jsonify({
            'error': f'Setting with key {key} not found'
        }), 404
    
    return jsonify({
        'setting': setting.to_dict()
    }), 200

@system.route('/meeting-metadata', methods=['GET'])
@jwt_required()
def get_meeting_metadata():
    """Get meeting metadata configuration"""
    try:
        # Get all meeting-related settings
        meeting_keys = [
            'meeting_duration',
            'meeting_interval', 
            'day_start_time',
            'day_end_time',
            'meeting_breaks',
            'max_seller_attendees_per_day',
            'max_buyer_meetings_per_day'
        ]
        
        metadata = {}
        for key in meeting_keys:
            setting = SystemSetting.query.filter_by(key=key).first()
            if setting:
                if key == 'meeting_breaks':
                    # Parse JSON for breaks
                    try:
                        metadata[key] = json.loads(setting.value)
                    except (json.JSONDecodeError, TypeError):
                        metadata[key] = []
                elif key in ['meeting_duration', 'meeting_interval', 'max_seller_attendees_per_day', 'max_buyer_meetings_per_day']:
                    # Convert to integer
                    try:
                        metadata[key] = int(setting.value)
                    except (ValueError, TypeError):
                        if key == 'meeting_duration':
                            metadata[key] = 10
                        elif key == 'meeting_interval':
                            metadata[key] = 5
                        elif key == 'max_seller_attendees_per_day':
                            metadata[key] = 230
                        elif key == 'max_buyer_meetings_per_day':
                            metadata[key] = 30
                else:
                    metadata[key] = setting.value
            else:
                # Set defaults if not found
                if key == 'meeting_duration':
                    metadata[key] = 10
                elif key == 'meeting_interval':
                    metadata[key] = 5
                elif key == 'day_start_time':
                    metadata[key] = "9:00 AM"
                elif key == 'day_end_time':
                    metadata[key] = "5:00 PM"
                elif key == 'meeting_breaks':
                    metadata[key] = [
                        {
                            "id": 1,
                            "label": "Lunch Break",
                            "startTime": "12:00 PM",
                            "endTime": "1:00 PM"
                        }
                    ]
                elif key == 'max_seller_attendees_per_day':
                    metadata[key] = 230
                elif key == 'max_buyer_meetings_per_day':
                    metadata[key] = 30
        
        return jsonify({
            'metadata': metadata
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Failed to retrieve meeting metadata: {str(e)}'
        }), 500

@system.route('/meeting-metadata', methods=['PUT'])
@admin_required
def update_meeting_metadata():
    """Update meeting metadata configuration (admin only)"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'error': 'No data provided'
            }), 400
        
        # Validate required fields
        required_fields = ['meetingDuration', 'intervalBetweenSlots', 'dayStartTime', 'dayEndTime', 'breaks']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Validate meeting duration
        if not isinstance(data['meetingDuration'], int) or data['meetingDuration'] < 10 or data['meetingDuration'] > 60:
            return jsonify({
                'error': 'Meeting duration must be between 10 and 60 minutes'
            }), 400
        
        # Validate interval
        if not isinstance(data['intervalBetweenSlots'], int) or data['intervalBetweenSlots'] < 0 or data['intervalBetweenSlots'] > 30:
            return jsonify({
                'error': 'Interval must be between 0 and 30 minutes'
            }), 400
        
        # Validate breaks
        if not isinstance(data['breaks'], list):
            return jsonify({
                'error': 'Breaks must be an array'
            }), 400
        
        # Validate meeting limits (optional fields)
        if 'maxSellerAttendees' in data:
            if not isinstance(data['maxSellerAttendees'], int) or data['maxSellerAttendees'] < 1:
                return jsonify({
                    'error': 'Max seller attendees must be a positive integer'
                }), 400
        
        if 'maxBuyerMeetings' in data:
            if not isinstance(data['maxBuyerMeetings'], int) or data['maxBuyerMeetings'] < 1:
                return jsonify({
                    'error': 'Max buyer meetings must be a positive integer'
                }), 400
        
        # Convert frontend format to backend format
        day_start_time = f"{data['dayStartTime']} {data['dayStartPeriod']}"
        day_end_time = f"{data['dayEndTime']} {data['dayEndPeriod']}"
        
        # Convert breaks to proper format
        breaks_data = []
        for break_item in data['breaks']:
            breaks_data.append({
                'id': break_item['id'],
                'label': break_item['label'],
                'startTime': f"{break_item['startTime']} {break_item['startPeriod']}",
                'endTime': f"{break_item['endTime']} {break_item['endPeriod']}"
            })
        
        # Update or create settings
        settings_to_update = [
            ('meeting_duration', str(data['meetingDuration']), 'Meeting duration in minutes'),
            ('meeting_interval', str(data['intervalBetweenSlots']), 'Interval between meeting slots in minutes'),
            ('day_start_time', day_start_time, 'Day start time for meetings'),
            ('day_end_time', day_end_time, 'Day end time for meetings'),
            ('meeting_breaks', json.dumps(breaks_data), 'Meeting breaks configuration')
        ]
        
        # Add meeting limits if provided
        if 'maxSellerAttendees' in data:
            settings_to_update.append(('max_seller_attendees_per_day', str(data['maxSellerAttendees']), 'Maximum seller attendees per day'))
        
        if 'maxBuyerMeetings' in data:
            settings_to_update.append(('max_buyer_meetings_per_day', str(data['maxBuyerMeetings']), 'Maximum buyer meetings per day'))
        
        for key, value, description in settings_to_update:
            setting = SystemSetting.query.filter_by(key=key).first()
            if setting:
                setting.value = value
                setting.updated_at = db.func.now()
            else:
                setting = SystemSetting(
                    key=key,
                    value=value,
                    description=description
                )
                db.session.add(setting)
        
        db.session.commit()
        
        # Prepare response metadata
        response_metadata = {
            'meetingDuration': data['meetingDuration'],
            'intervalBetweenSlots': data['intervalBetweenSlots'],
            'dayStartTime': day_start_time,
            'dayEndTime': day_end_time,
            'breaks': breaks_data
        }
        
        # Add meeting limits to response if they were provided
        if 'maxSellerAttendees' in data:
            response_metadata['maxSellerAttendees'] = data['maxSellerAttendees']
        
        if 'maxBuyerMeetings' in data:
            response_metadata['maxBuyerMeetings'] = data['maxBuyerMeetings']
        
        return jsonify({
            'message': 'Meeting metadata updated successfully',
            'metadata': response_metadata
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': f'Failed to update meeting metadata: {str(e)}'
        }), 500

@system.route('/meeting-metadata/initialize', methods=['POST'])
@admin_required
def initialize_meeting_metadata():
    """Initialize default meeting metadata settings (admin only)"""
    try:
        # Check if meeting metadata already exists
        existing_keys = ['meeting_duration', 'meeting_interval', 'day_start_time', 'day_end_time', 'meeting_breaks', 'max_seller_attendees_per_day', 'max_buyer_meetings_per_day']
        existing_settings = SystemSetting.query.filter(SystemSetting.key.in_(existing_keys)).count()
        
        if existing_settings > 0:
            return jsonify({
                'message': 'Meeting metadata already initialized'
            }), 400
        
        # Default meeting metadata
        default_breaks = [
            {
                "id": 1,
                "label": "Lunch Break",
                "startTime": "12:00 PM",
                "endTime": "1:00 PM"
            }
        ]
        
        default_metadata = [
            ('meeting_duration', '10', 'Meeting duration in minutes'),
            ('meeting_interval', '5', 'Interval between meeting slots in minutes'),
            ('day_start_time', '9:00 AM', 'Day start time for meetings'),
            ('day_end_time', '5:00 PM', 'Day end time for meetings'),
            ('meeting_breaks', json.dumps(default_breaks), 'Meeting breaks configuration'),
            ('max_seller_attendees_per_day', '230', 'Maximum seller attendees per day'),
            ('max_buyer_meetings_per_day', '30', 'Maximum buyer meetings per day')
        ]
        
        for key, value, description in default_metadata:
            setting = SystemSetting(
                key=key,
                value=value,
                description=description
            )
            db.session.add(setting)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Meeting metadata initialized successfully',
            'metadata': {
                'meetingDuration': 10,
                'intervalBetweenSlots': 5,
                'dayStartTime': '9:00 AM',
                'dayEndTime': '5:00 PM',
                'breaks': default_breaks,
                'maxSellerAttendees': 230,
                'maxBuyerMeetings': 30
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': f'Failed to initialize meeting metadata: {str(e)}'
        }), 500

@system.route('/meetings-toggle', methods=['PUT'])
@admin_required
def toggle_meetings():
    """Toggle meeting requests on/off and handle pending meetings"""
    try:
        data = request.get_json()
        
        if 'enabled' not in data:
            return jsonify({
                'error': 'Missing required field: enabled'
            }), 400
        
        enabled = data['enabled']
        if not isinstance(enabled, bool):
            return jsonify({
                'error': 'enabled field must be a boolean'
            }), 400
        
        # Update the meetings_enabled setting
        setting = SystemSetting.query.filter_by(key='meetings_enabled').first()
        if setting:
            setting.value = 'true' if enabled else 'false'
            setting.updated_at = db.func.now()
        else:
            setting = SystemSetting(
                key='meetings_enabled',
                value='true' if enabled else 'false',
                description='Enable/disable meeting requests globally'
            )
            db.session.add(setting)
        
        # If meetings are being disabled, expire all pending meetings
        if not enabled:
            from ..models import Meeting, MeetingStatus, TimeSlot
            
            # Get all pending meetings
            pending_meetings = Meeting.query.filter_by(status=MeetingStatus.PENDING).all()
            
            expired_count = 0
            for meeting in pending_meetings:
                # Change status to cancelled (we'll use this as "expired")
                meeting.status = MeetingStatus.CANCELLED
                
                # Free up the associated time slot
                if meeting.time_slot:
                    meeting.time_slot.is_available = True
                    meeting.time_slot.meeting_id = None
                
                expired_count += 1
        
        db.session.commit()
        
        response_data = {
            'message': f'Meeting requests {"enabled" if enabled else "disabled"} successfully',
            'meetings_enabled': enabled
        }
        
        if not enabled and 'expired_count' in locals():
            response_data['expired_meetings'] = expired_count
        
        return jsonify(response_data), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': f'Failed to toggle meetings: {str(e)}'
        }), 500

@system.route('/meetings-status', methods=['GET'])
@jwt_required()
def get_meetings_status():
    """Get the current status of meeting requests"""
    try:
        setting = SystemSetting.query.filter_by(key='meetings_enabled').first()
        
        if not setting:
            # Default to enabled if setting doesn't exist
            enabled = True
        else:
            enabled = setting.value == 'true'
        
        return jsonify({
            'meetings_enabled': enabled
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Failed to get meetings status: {str(e)}'
        }), 500
