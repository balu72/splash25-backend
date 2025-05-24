from app import create_app
from app.models import db, User, UserRole, BuyerProfile

def create_buyer_profiles():
    app = create_app()
    with app.app_context():
        # Find the buyer user
        buyer = User.query.filter_by(username='buyer_new').first()
        if buyer:
            # Check if profile already exists
            profile = BuyerProfile.query.filter_by(user_id=buyer.id).first()
            if not profile:
                # Create buyer profile
                profile = BuyerProfile(
                    user_id=buyer.id,
                    name='John Doe',
                    organization='Global Travel Inc.',
                    designation='Travel Manager',
                    operator_type='Tour Operator',
                    interests=['Wildlife', 'Trekking', 'Photography'],
                    properties_of_interest=['Resorts', 'Hotels', 'Homestays'],
                    country='India',
                    state='Kerala',
                    city='Kochi',
                    address='123 Marine Drive, Kochi, Kerala',
                    mobile='+91 9876543210',
                    website='https://globaltravel.com',
                    instagram='@globaltravel',
                    year_of_starting_business=2015,
                    selling_wayanad=True,
                    since_when=2018,
                    bio='Experienced travel operator specializing in Kerala tourism with focus on sustainable and eco-friendly travel experiences.'
                )
                db.session.add(profile)
                db.session.commit()
                print('Buyer profile created successfully!')
            else:
                print('Buyer profile already exists.')
        else:
            print('Buyer user not found.')

        # Create additional mock buyer profiles for testing
        mock_buyers = [
            {
                'username': 'buyer_test1',
                'email': 'buyer1@test.com',
                'password': 'test123',
                'profile': {
                    'name': 'Jane Smith',
                    'organization': 'Adventure Seekers Ltd.',
                    'designation': 'Operations Manager',
                    'operator_type': 'Travel Agent',
                    'interests': ['Adventure Sports', 'Trekking', 'Nature'],
                    'properties_of_interest': ['Camping', 'Tree Houses', 'Hostels'],
                    'country': 'USA',
                    'state': 'California',
                    'city': 'San Francisco',
                    'address': '456 Market Street, San Francisco, CA',
                    'mobile': '+1 555-123-4567',
                    'website': 'https://adventureseekers.com',
                    'year_of_starting_business': 2012,
                    'selling_wayanad': False,
                    'bio': 'Specializing in adventure travel and outdoor experiences for thrill-seekers.'
                }
            },
            {
                'username': 'buyer_test2',
                'email': 'buyer2@test.com',
                'password': 'test123',
                'profile': {
                    'name': 'Robert Johnson',
                    'organization': 'Cultural Heritage Tours',
                    'designation': 'Director',
                    'operator_type': 'DMC',
                    'interests': ['Cultural Tours', 'Photography', 'Wellness'],
                    'properties_of_interest': ['Hotels', 'Villas', 'Resorts'],
                    'country': 'UK',
                    'state': 'England',
                    'city': 'London',
                    'address': '789 Oxford Street, London',
                    'mobile': '+44 20 7123 4567',
                    'website': 'https://culturalheritage.co.uk',
                    'year_of_starting_business': 2008,
                    'selling_wayanad': True,
                    'since_when': 2020,
                    'bio': 'Focused on cultural immersion and heritage tourism experiences.'
                }
            }
        ]

        for mock_buyer in mock_buyers:
            # Check if user already exists
            existing_user = User.query.filter_by(username=mock_buyer['username']).first()
            if not existing_user:
                # Create user
                user = User(
                    username=mock_buyer['username'],
                    email=mock_buyer['email'],
                    password=mock_buyer['password'],
                    role=UserRole.BUYER
                )
                db.session.add(user)
                db.session.flush()  # Get the user ID
                
                # Create profile
                profile_data = mock_buyer['profile']
                profile = BuyerProfile(
                    user_id=user.id,
                    **profile_data
                )
                db.session.add(profile)
                print(f"Created buyer: {mock_buyer['username']}")
            else:
                print(f"Buyer {mock_buyer['username']} already exists.")
        
        db.session.commit()
        print('All buyer profiles created successfully!')

if __name__ == "__main__":
    create_buyer_profiles()
