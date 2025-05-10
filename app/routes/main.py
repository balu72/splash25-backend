from flask import Blueprint, jsonify

main = Blueprint("main", __name__)

@main.route("/")
def home():
    return jsonify({
        "name": "Splash25 API",
        "version": "1.0.0",
        "description": "API for Splash25 tourism application",
        "endpoints": {
            "auth": {
                "register": "/api/auth/register",
                "login": "/api/auth/login",
                "refresh": "/api/auth/refresh",
                "me": "/api/auth/me",
                "logout": "/api/auth/logout"
            },
            "buyer": {
                "dashboard": "/api/buyer/dashboard",
                "profile": "/api/buyer/profile"
            },
            "seller": {
                "dashboard": "/api/seller/dashboard",
                "listings": "/api/seller/listings",
                "profile": "/api/seller/profile"
            },
            "admin": {
                "dashboard": "/api/admin/dashboard",
                "users": "/api/admin/users",
                "verifications": "/api/admin/verifications"
            }
        }
    })

@main.route("/health")
def health_check():
    return jsonify({
        "status": "healthy",
        "message": "Splash25 API is running"
    })
