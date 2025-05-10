from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from ..models import UserRole

def role_required(allowed_roles):
    """
    Decorator to check if the current user has one of the allowed roles.
    
    Args:
        allowed_roles: A list of UserRole enum values
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            # Verify JWT is present and valid
            verify_jwt_in_request()
            
            # Get claims from JWT
            claims = get_jwt()
            
            # Check if role is in allowed roles
            if 'role' not in claims or claims['role'] not in [role.value for role in allowed_roles]:
                return jsonify({'error': 'Access denied: insufficient permissions'}), 403
            
            return fn(*args, **kwargs)
        return wrapper
    return decorator

# Specific role decorators
def admin_required(fn):
    """Decorator to check if the current user is an admin."""
    return role_required([UserRole.ADMIN])(fn)

def seller_required(fn):
    """Decorator to check if the current user is a seller."""
    return role_required([UserRole.SELLER])(fn)

def buyer_required(fn):
    """Decorator to check if the current user is a buyer."""
    return role_required([UserRole.BUYER])(fn)

def admin_or_seller_required(fn):
    """Decorator to check if the current user is an admin or seller."""
    return role_required([UserRole.ADMIN, UserRole.SELLER])(fn)

def auth_required(fn):
    """Decorator to check if the user is authenticated (any role)."""
    return role_required([UserRole.ADMIN, UserRole.SELLER, UserRole.BUYER])(fn)
