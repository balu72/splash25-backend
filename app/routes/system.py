from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..utils.auth import admin_required
from ..models import db, SystemSetting

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
