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
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
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

class TimeSlot(db.Model):
    __tablename__ = 'time_slots'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    is_available = db.Column(db.Boolean, default=True)
    meeting_id = db.Column(db.Integer, db.ForeignKey('meetings.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('time_slots', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat(),
            'is_available': self.is_available,
            'meeting_id': self.meeting_id
        }

class SystemSetting(db.Model):
    __tablename__ = 'system_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(50), unique=True, nullable=False)
    value = db.Column(db.String(255))
    description = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'key': self.key,
            'value': self.value,
            'description': self.description
        }

class Meeting(db.Model):
    __tablename__ = 'meetings'
    
    id = db.Column(db.Integer, primary_key=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    time_slot_id = db.Column(db.Integer, db.ForeignKey('time_slots.id'), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    status = db.Column(db.Enum(MeetingStatus), nullable=False, default=MeetingStatus.PENDING)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    # Relationships
    buyer = db.relationship('User', foreign_keys=[buyer_id], backref=db.backref('buyer_meetings', lazy=True))
    seller = db.relationship('User', foreign_keys=[seller_id], backref=db.backref('seller_meetings', lazy=True))
    time_slot = db.relationship('TimeSlot', foreign_keys=[time_slot_id], backref=db.backref('meeting', uselist=False))
    
    def to_dict(self):
        return {
            'id': self.id,
            'buyer_id': self.buyer_id,
            'seller_id': self.seller_id,
            'time_slot_id': self.time_slot_id,
            'notes': self.notes,
            'status': self.status.value,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'buyer': {
                'id': self.buyer.id,
                'username': self.buyer.username,
                'email': self.buyer.email
            },
            'seller': {
                'id': self.seller.id,
                'username': self.seller.username,
                'email': self.seller.email
            },
            'time_slot': self.time_slot.to_dict() if self.time_slot else None
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

class InvitedBuyer(db.Model):
    __tablename__ = 'invited_buyers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    invitation_token = db.Column(db.String(255), unique=True, nullable=False)
    is_registered = db.Column(db.Boolean, default=False)
    invited_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)
    
    # Relationships
    admin = db.relationship('User', backref=db.backref('invited_buyers', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'is_registered': self.is_registered,
            'created_at': self.created_at.isoformat(),
            'expires_at': self.expires_at.isoformat()
        }

class PendingBuyer(db.Model):
    __tablename__ = 'pending_buyers'
    
    id = db.Column(db.Integer, primary_key=True)
    invited_buyer_id = db.Column(db.Integer, db.ForeignKey('invited_buyers.id'), nullable=False)
    
    # Form fields
    name = db.Column(db.String(100), nullable=False)
    designation = db.Column(db.String(30), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    gst = db.Column(db.String(15), nullable=True)
    address = db.Column(db.String(150), nullable=False)
    city = db.Column(db.String(30), nullable=False)
    state = db.Column(db.String(30), nullable=False)
    pin = db.Column(db.String(10), nullable=False)
    mobile = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    website = db.Column(db.String(100), nullable=True)
    instagram = db.Column(db.String(30), nullable=True)
    year_of_starting_business = db.Column(db.Integer, nullable=False)
    type_of_operator = db.Column(db.String(20), nullable=False)
    already_sell_wayanad = db.Column(db.String(3), nullable=False)
    since_when = db.Column(db.Integer, nullable=True)
    opinion_about_previous_splash = db.Column(db.String(50), nullable=False)
    property_stayed_in = db.Column(db.String(100), nullable=True)
    reference_property1_name = db.Column(db.String(100), nullable=False)
    reference_property1_address = db.Column(db.String(200), nullable=False)
    reference_property2_name = db.Column(db.String(100), nullable=True)
    reference_property2_address = db.Column(db.String(200), nullable=True)
    interests = db.Column(db.String(255), nullable=False)  # Comma-separated values
    properties_of_interest = db.Column(db.String(100), nullable=False)  # Comma-separated values
    why_attend_splash2025 = db.Column(db.Text, nullable=False)
    
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    invited_buyer = db.relationship('InvitedBuyer', backref=db.backref('pending_registration', uselist=False))
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'company': self.company,
            'designation': self.designation,
            'mobile': self.mobile,
            'status': self.status,
            'created_at': self.created_at.isoformat()
            # Add other fields as needed
        }

class DomainRestriction(db.Model):
    __tablename__ = 'domain_restrictions'
    
    id = db.Column(db.Integer, primary_key=True)
    domain = db.Column(db.String(100), unique=True, nullable=False)
    is_enabled = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'domain': self.domain,
            'is_enabled': self.is_enabled,
            'created_at': self.created_at.isoformat()
        }

class SellerProfile(db.Model):
    __tablename__ = 'seller_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    business_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    seller_type = db.Column(db.String(50), nullable=True)  # e.g., "Resort", "Tour Operator", etc.
    target_market = db.Column(db.String(50), nullable=True)  # e.g., "Domestic", "International", etc.
    logo_url = db.Column(db.String(255), nullable=True)
    website = db.Column(db.String(255), nullable=True)
    contact_email = db.Column(db.String(100), nullable=True)
    contact_phone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.Text, nullable=True)
    is_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('seller_profile', uselist=False))
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'business_name': self.business_name,
            'description': self.description,
            'seller_type': self.seller_type,
            'target_market': self.target_market,
            'logo_url': self.logo_url,
            'website': self.website,
            'contact_email': self.contact_email,
            'contact_phone': self.contact_phone,
            'address': self.address,
            'is_verified': self.is_verified
        }

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.Enum(UserRole), nullable=False, default=UserRole.BUYER)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
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
            'created_at': self.created_at.isoformat()
        }
