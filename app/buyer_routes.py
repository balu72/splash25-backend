from flask import Blueprint, jsonify
from .auth_utils import buyer_required
from .models import User

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
