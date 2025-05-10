from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime
import enum

db = SQLAlchemy()
bcrypt = Bcrypt()

class UserRole(enum.Enum):
    BUYER = "buyer"
    SELLER = "seller"
    ADMIN = "admin"

class MeetingStatus(enum.Enum):
    REQUESTED = "requested"
    CONFIRMED = "confirmed"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class ListingStatus(enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"

class TravelPlan(db.Model):
    __tablename__ = 'travel_plans'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_name = db.Column(db.String(120), nullable=False)
    event_start_date = db.Column(db.Date, nullable=False)
    event_end_date = db.Column(db.Date, nullable=False)
    venue = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(20), nullable=False)  # confirmed, pending, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('travel_plans', lazy=True))
    transportation = db.relationship('Transportation', backref='travel_plan', uselist=False, cascade='all, delete-orphan')
    accommodation = db.relationship('Accommodation', backref='travel_plan', uselist=False, cascade='all, delete-orphan')
    ground_transportation = db.relationship('GroundTransportation', backref='travel_plan', uselist=False, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'eventName': self.event_name,
            'eventDates': {
                'start': self.event_start_date.isoformat(),
                'end': self.event_end_date.isoformat()
            },
            'venue': self.venue,
            'status': self.status,
            'transportation': self.transportation.to_dict() if self.transportation else None,
            'accommodation': self.accommodation.to_dict() if self.accommodation else None,
            'groundTransportation': self.ground_transportation.to_dict() if self.ground_transportation else None
        }

class Transportation(db.Model):
    __tablename__ = 'transportation'
    
    id = db.Column(db.Integer, primary_key=True)
    travel_plan_id = db.Column(db.Integer, db.ForeignKey('travel_plans.id'), nullable=False)
    type = db.Column(db.String(20), nullable=False)  # flight, train, bus, other
    
    # Outbound journey
    outbound_carrier = db.Column(db.String(100), nullable=False)
    outbound_number = db.Column(db.String(20), nullable=False)
    outbound_departure_location = db.Column(db.String(200), nullable=False)
    outbound_departure_datetime = db.Column(db.DateTime, nullable=False)
    outbound_arrival_location = db.Column(db.String(200), nullable=False)
    outbound_arrival_datetime = db.Column(db.DateTime, nullable=False)
    outbound_booking_reference = db.Column(db.String(50), nullable=False)
    outbound_seat_info = db.Column(db.String(50), nullable=True)
    
    # Return journey
    return_carrier = db.Column(db.String(100), nullable=False)
    return_number = db.Column(db.String(20), nullable=False)
    return_departure_location = db.Column(db.String(200), nullable=False)
    return_departure_datetime = db.Column(db.DateTime, nullable=False)
    return_arrival_location = db.Column(db.String(200), nullable=False)
    return_arrival_datetime = db.Column(db.DateTime, nullable=False)
    return_booking_reference = db.Column(db.String(50), nullable=False)
    return_seat_info = db.Column(db.String(50), nullable=True)
    
    def to_dict(self):
        return {
            'type': self.type,
            'outbound': {
                'carrier': self.outbound_carrier,
                'number': self.outbound_number,
                'departureLocation': self.outbound_departure_location,
                'departureDateTime': self.outbound_departure_datetime.isoformat(),
                'arrivalLocation': self.outbound_arrival_location,
                'arrivalDateTime': self.outbound_arrival_datetime.isoformat(),
                'bookingReference': self.outbound_booking_reference,
                'seatInfo': self.outbound_seat_info
            },
            'return': {
                'carrier': self.return_carrier,
                'number': self.return_number,
                'departureLocation': self.return_departure_location,
                'departureDateTime': self.return_departure_datetime.isoformat(),
                'arrivalLocation': self.return_arrival_location,
                'arrivalDateTime': self.return_arrival_datetime.isoformat(),
                'bookingReference': self.return_booking_reference,
                'seatInfo': self.return_seat_info
            }
        }

class Accommodation(db.Model):
    __tablename__ = 'accommodations'
    
    id = db.Column(db.Integer, primary_key=True)
    travel_plan_id = db.Column(db.Integer, db.ForeignKey('travel_plans.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    address = db.Column(db.Text, nullable=False)
    check_in_datetime = db.Column(db.DateTime, nullable=False)
    check_out_datetime = db.Column(db.DateTime, nullable=False)
    room_type = db.Column(db.String(100), nullable=False)
    booking_reference = db.Column(db.String(50), nullable=False)
    special_notes = db.Column(db.Text, nullable=True)
    
    def to_dict(self):
        return {
            'name': self.name,
            'address': self.address,
            'checkInDateTime': self.check_in_datetime.isoformat(),
            'checkOutDateTime': self.check_out_datetime.isoformat(),
            'roomType': self.room_type,
            'bookingReference': self.booking_reference,
            'specialNotes': self.special_notes
        }

class GroundTransportation(db.Model):
    __tablename__ = 'ground_transportation'
    
    id = db.Column(db.Integer, primary_key=True)
    travel_plan_id = db.Column(db.Integer, db.ForeignKey('travel_plans.id'), nullable=False)
    
    # Pickup details
    pickup_location = db.Column(db.String(200), nullable=False)
    pickup_datetime = db.Column(db.DateTime, nullable=False)
    pickup_vehicle_type = db.Column(db.String(50), nullable=True)
    pickup_driver_contact = db.Column(db.String(50), nullable=True)
    
    # Dropoff details
    dropoff_location = db.Column(db.String(200), nullable=False)
    dropoff_datetime = db.Column(db.DateTime, nullable=False)
    dropoff_vehicle_type = db.Column(db.String(50), nullable=True)
    dropoff_driver_contact = db.Column(db.String(50), nullable=True)
    
    def to_dict(self):
        return {
            'pickup': {
                'location': self.pickup_location,
                'dateTime': self.pickup_datetime.isoformat(),
                'vehicleType': self.pickup_vehicle_type,
                'driverContact': self.pickup_driver_contact
            },
            'dropoff': {
                'location': self.dropoff_location,
                'dateTime': self.dropoff_datetime.isoformat(),
                'vehicleType': self.dropoff_vehicle_type,
                'driverContact': self.dropoff_driver_contact
            }
        }

class Meeting(db.Model):
    __tablename__ = 'meetings'
    
    id = db.Column(db.Integer, primary_key=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    from_time = db.Column(db.DateTime, nullable=False)
    to_time = db.Column(db.DateTime, nullable=False)
    topic = db.Column(db.String(200), nullable=True)
    status = db.Column(db.Enum(MeetingStatus), nullable=False, default=MeetingStatus.REQUESTED)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    buyer = db.relationship('User', foreign_keys=[buyer_id], backref=db.backref('buyer_meetings', lazy=True))
    seller = db.relationship('User', foreign_keys=[seller_id], backref=db.backref('seller_meetings', lazy=True))
    
    def to_dict_for_buyer(self):
        return {
            'id': self.id,
            'fromTime': self.from_time.isoformat(),
            'toTime': self.to_time.isoformat(),
            'sellerEntity': self.seller.business_name,
            'sellerName': self.seller.username,
            'stallNo': f"A{self.seller_id:02d}",  # Placeholder for actual stall number
            'status': self.status.value,
            'topic': self.topic
        }
    
    def to_dict_for_seller(self):
        return {
            'id': self.id,
            'fromTime': self.from_time.isoformat(),
            'toTime': self.to_time.isoformat(),
            'buyerName': self.buyer.username,
            'buyerOrganization': "Organization",  # Placeholder for actual organization
            'status': self.status.value,
            'topic': self.topic
        }

class Listing(db.Model):
    __tablename__ = 'listings'
    
    id = db.Column(db.Integer, primary_key=True)
    seller_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    duration = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    max_participants = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Enum(ListingStatus), nullable=False, default=ListingStatus.ACTIVE)
    image_url = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    views = db.Column(db.Integer, default=0)
    bookings = db.Column(db.Integer, default=0)
    
    # Relationships
    seller = db.relationship('User', backref=db.backref('listings', lazy=True))
    available_dates = db.relationship('ListingDate', backref='listing', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'duration': self.duration,
            'location': self.location,
            'max_participants': self.max_participants,
            'status': self.status.value,
            'image_url': self.image_url,
            'available_dates': [date.date.isoformat() for date in self.available_dates],
            'views': self.views,
            'bookings': self.bookings
        }

class ListingDate(db.Model):
    __tablename__ = 'listing_dates'
    
    id = db.Column(db.Integer, primary_key=True)
    listing_id = db.Column(db.Integer, db.ForeignKey('listings.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.Enum(UserRole), nullable=False, default=UserRole.BUYER)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Additional fields based on role
    # For sellers
    business_name = db.Column(db.String(120), nullable=True)
    business_description = db.Column(db.Text, nullable=True)
    is_verified = db.Column(db.Boolean, default=False)
    
    def __init__(self, username, email, password, role=UserRole.BUYER, **kwargs):
        self.username = username
        self.email = email
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        self.role = role
        
        # Set additional fields if provided
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
    
    def is_buyer(self):
        return self.role == UserRole.BUYER
    
    def is_seller(self):
        return self.role == UserRole.SELLER
    
    def is_admin(self):
        return self.role == UserRole.ADMIN
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role.value,
            'created_at': self.created_at.isoformat(),
            'business_name': self.business_name if self.is_seller() else None,
            'is_verified': self.is_verified if self.is_seller() else None
        }
