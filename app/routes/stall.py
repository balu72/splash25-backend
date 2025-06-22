from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import db, User, Stall, SellerProfile
from ..utils.auth import seller_required, admin_required

stall = Blueprint('stall', __name__, url_prefix='/api/stalls')

@stall.route('', methods=['GET'])
@jwt_required()
@seller_required
def get_stalls():
    """Get all stalls for the current seller"""
    current_user_id = get_jwt_identity()
    # Convert to int if it's a string
    if isinstance(current_user_id, str):
        try:
            current_user_id = int(current_user_id)
        except ValueError:
            return jsonify({'error': 'Invalid user ID'}), 400
    
    try:
        # Get stalls for the current seller with seller profile info
        stalls = db.session.query(Stall, SellerProfile).join(
            SellerProfile, Stall.seller_id == SellerProfile.user_id
        ).filter(Stall.seller_id == current_user_id).all()
        
        stall_list = []
        for stall, seller_profile in stalls:
            stall_dict = stall.to_dict()
            stall_dict['fascia_name'] = seller_profile.business_name
            # Include complete stall type information for attendee calculations
            if stall.stall_type_rel:
                stall_dict['stall_type_info'] = stall.stall_type_rel.to_dict()
                # Map the stall type fields to the stall for backward compatibility
                stall_dict['allowed_attendees'] = stall.stall_type_rel.attendees
                stall_dict['max_additional_seller_passes'] = stall.stall_type_rel.max_additional_seller_passes
            stall_list.append(stall_dict)
        
        return jsonify({
            'stalls': stall_list
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to fetch stalls',
            'message': str(e)
        }), 500

@stall.route('', methods=['POST'])
@jwt_required()
@seller_required
def create_stall():
    """Create a new stall for the current seller"""
    current_user_id = get_jwt_identity()
    # Convert to int if it's a string
    if isinstance(current_user_id, str):
        try:
            current_user_id = int(current_user_id)
        except ValueError:
            return jsonify({'error': 'Invalid user ID'}), 400
    
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['stall_type_id']
        
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Set default number if not provided
        stall_number = data.get('number', '0')
        
        # Check if stall number already exists for this seller
        existing_stall = Stall.query.filter_by(
            seller_id=current_user_id, 
            number=stall_number
        ).first()
        
        if existing_stall:
            return jsonify({
                'error': 'Stall number already exists for this seller'
            }), 400
        
        # Verify stall type exists
        from ..models import StallType
        stall_type = StallType.query.get(data['stall_type_id'])
        if not stall_type:
            return jsonify({
                'error': 'Invalid stall type ID'
            }), 400
        
        # Create new stall
        new_stall = Stall(
            seller_id=current_user_id,
            stall_type_id=data['stall_type_id'],
            number=stall_number,
            fascia_name=data.get('fascia_name', ''),
            allocated_stall_number=data.get('allocated_stall_number', ''),
            is_allocated=True
        )
        
        db.session.add(new_stall)
        db.session.commit()
        
        # Get the created stall with seller profile info
        stall_with_profile = db.session.query(Stall, SellerProfile).join(
            SellerProfile, Stall.seller_id == SellerProfile.user_id
        ).filter(Stall.id == new_stall.id).first()
        
        if stall_with_profile:
            stall, seller_profile = stall_with_profile
            stall_dict = stall.to_dict()
            stall_dict['fascia_name'] = seller_profile.business_name
        else:
            stall_dict = new_stall.to_dict()
        
        return jsonify({
            'message': 'Stall created successfully',
            'stall': stall_dict
        }), 201
        
    except ValueError as e:
        return jsonify({
            'error': 'Invalid data type',
            'message': str(e)
        }), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Failed to create stall',
            'message': str(e)
        }), 500

@stall.route('/<int:stall_id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_stall(stall_id):
    """Update an existing stall (admin only)"""
    try:
        # Find the stall (admin can update any stall)
        stall = Stall.query.get(stall_id)
        
        if not stall:
            return jsonify({
                'error': 'Stall not found'
            }), 404
        
        data = request.get_json()
        
        # Update fields if provided
        if 'number' in data:
            # Check if new number conflicts with existing stalls for the same seller
            existing_stall = Stall.query.filter_by(
                seller_id=stall.seller_id, 
                number=data['number']
            ).filter(Stall.id != stall_id).first()
            
            if existing_stall:
                return jsonify({
                    'error': 'Stall number already exists for this seller'
                }), 400
            
            stall.number = data['number']
        
        if 'stall_type_id' in data:
            # Verify stall type exists
            from ..models import StallType
            stall_type = StallType.query.get(data['stall_type_id'])
            if not stall_type:
                return jsonify({
                    'error': 'Invalid stall type ID'
                }), 400
            stall.stall_type_id = data['stall_type_id']
        
        if 'fascia_name' in data:
            stall.fascia_name = data['fascia_name']
        
        if 'allocated_stall_number' in data:
            stall.allocated_stall_number = data['allocated_stall_number']
        
        if 'is_allocated' in data:
            stall.is_allocated = bool(data['is_allocated'])
        
        db.session.commit()
        
        # Get the updated stall with seller profile info
        stall_with_profile = db.session.query(Stall, SellerProfile).join(
            SellerProfile, Stall.seller_id == SellerProfile.user_id
        ).filter(Stall.id == stall.id).first()
        
        if stall_with_profile:
            stall, seller_profile = stall_with_profile
            stall_dict = stall.to_dict()
            stall_dict['fascia_name'] = seller_profile.business_name
        else:
            stall_dict = stall.to_dict()
        
        return jsonify({
            'message': 'Stall updated successfully',
            'stall': stall_dict
        }), 200
        
    except ValueError as e:
        return jsonify({
            'error': 'Invalid data type',
            'message': str(e)
        }), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Failed to update stall',
            'message': str(e)
        }), 500

@stall.route('/<int:stall_id>', methods=['DELETE'])
@jwt_required()
@seller_required
def delete_stall(stall_id):
    """Delete a stall"""
    current_user_id = get_jwt_identity()
    # Convert to int if it's a string
    if isinstance(current_user_id, str):
        try:
            current_user_id = int(current_user_id)
        except ValueError:
            return jsonify({'error': 'Invalid user ID'}), 400
    
    try:
        # Find the stall and verify ownership
        stall = Stall.query.filter_by(id=stall_id, seller_id=current_user_id).first()
        
        if not stall:
            return jsonify({
                'error': 'Stall not found or access denied'
            }), 404
        
        db.session.delete(stall)
        db.session.commit()
        
        return jsonify({
            'message': 'Stall deleted successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Failed to delete stall',
            'message': str(e)
        }), 500
