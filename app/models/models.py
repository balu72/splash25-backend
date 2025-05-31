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

# Enhanced Models for the new schema

# Association tables for many-to-many relationships
buyer_profile_interests = db.Table('buyer_profile_interests',
    db.Column('buyer_profile_id', db.Integer, db.ForeignKey('buyer_profiles.id'), primary_key=True),
    db.Column('interest_id', db.Integer, db.ForeignKey('interests.id'), primary_key=True)
)

seller_target_markets = db.Table('seller_target_markets',
    db.Column('seller_profile_id', db.Integer, db.ForeignKey('seller_profiles.id'), primary_key=True),
    db.Column('interest_id', db.Integer, db.ForeignKey('interests.id'), primary_key=True)
)

class BuyerCategory(db.Model):
    __tablename__ = 'buyer_categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    deposit_amount = db.Column(db.Numeric(10, 2), default=0.00)
    entry_fee = db.Column(db.Numeric(10, 2), default=0.00)
    description = db.Column(db.Text, nullable=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'deposit_amount': float(self.deposit_amount),
            'entry_fee': float(self.entry_fee),
            'description': self.description
        }

class PropertyType(db.Model):
    __tablename__ = 'property_types'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }

class Interest(db.Model):
    __tablename__ = 'interests'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }

class StallType(db.Model):
    __tablename__ = 'stall_types'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    size = db.Column(db.String(50), nullable=True)
    allowed_attendees = db.Column(db.Integer, default=2)
    max_meetings_per_attendee = db.Column(db.Integer, default=20)
    min_meetings_per_attendee = db.Column(db.Integer, default=5)
    inclusions = db.Column(db.Text, nullable=True)
    saleable = db.Column(db.Boolean, default=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': float(self.price),
            'size': self.size,
            'allowed_attendees': self.allowed_attendees,
            'max_meetings_per_attendee': self.max_meetings_per_attendee,
            'min_meetings_per_attendee': self.min_meetings_per_attendee,
            'inclusions': self.inclusions,
            'saleable': self.saleable
        }

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(10), nullable=False, default=UserRole.BUYER.value)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    business_name = db.Column(db.String(120), nullable=True)
    business_description = db.Column(db.Text, nullable=True)
    is_verified = db.Column(db.Boolean, default=False)
    
    def __init__(self, username, email, password, role=UserRole.BUYER, **kwargs):
        self.username = username
        self.email = email
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        self.role = role.value if isinstance(role, UserRole) else role
        
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
    
    def is_buyer(self):
        return self.role == UserRole.BUYER.value
    
    def is_seller(self):
        return self.role == UserRole.SELLER.value
    
    def is_admin(self):
        return self.role == UserRole.ADMIN.value
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'created_at': self.created_at.isoformat()
        }

class BuyerProfile(db.Model):
    __tablename__ = 'buyer_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    organization = db.Column(db.String(100), nullable=False)
    designation = db.Column(db.String(50), nullable=True)
    operator_type = db.Column(db.String(50), nullable=True)
    
    # Enhanced fields
    category_id = db.Column(db.Integer, db.ForeignKey('buyer_categories.id'), nullable=True)
    salutation = db.Column(db.String(10), nullable=True)
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    vip = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(20), default='pending')
    gst = db.Column(db.String(20), nullable=True)
    pincode = db.Column(db.String(10), nullable=True)
    
    # Existing fields for backward compatibility
    interests = db.Column(db.JSON, nullable=True)
    properties_of_interest = db.Column(db.JSON, nullable=True)
    country = db.Column(db.String(50), nullable=True)
    state = db.Column(db.String(50), nullable=True)
    city = db.Column(db.String(50), nullable=True)
    address = db.Column(db.Text, nullable=True)
    mobile = db.Column(db.String(20), nullable=True)
    website = db.Column(db.String(255), nullable=True)
    instagram = db.Column(db.String(100), nullable=True)
    year_of_starting_business = db.Column(db.Integer, nullable=True)
    selling_wayanad = db.Column(db.Boolean, default=False)
    since_when = db.Column(db.Integer, nullable=True)
    bio = db.Column(db.Text, nullable=True)
    profile_image = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('buyer_profile', uselist=False))
    category = db.relationship('BuyerCategory', backref=db.backref('buyers', lazy=True))
    interest_relationships = db.relationship('Interest', secondary=buyer_profile_interests, 
                                           backref=db.backref('buyer_profiles', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'organization': self.organization,
            'designation': self.designation,
            'operator_type': self.operator_type,
            'category': self.category.to_dict() if self.category else None,
            'salutation': self.salutation,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'vip': self.vip,
            'status': self.status,
            'gst': self.gst,
            'pincode': self.pincode,
            'interests': self.interests or [],
            'interest_relationships': [interest.to_dict() for interest in self.interest_relationships],
            'properties_of_interest': self.properties_of_interest or [],
            'country': self.country,
            'state': self.state,
            'city': self.city,
            'address': self.address,
            'mobile': self.mobile,
            'website': self.website,
            'instagram': self.instagram,
            'year_of_starting_business': self.year_of_starting_business,
            'selling_wayanad': self.selling_wayanad,
            'since_when': self.since_when,
            'bio': self.bio,
            'profile_image': self.profile_image,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class SellerProfile(db.Model):
    __tablename__ = 'seller_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    business_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    seller_type = db.Column(db.String(50), nullable=True)
    target_market = db.Column(db.String(50), nullable=True)
    
    # Enhanced fields
    property_type_id = db.Column(db.Integer, db.ForeignKey('property_types.id'), nullable=True)
    status = db.Column(db.String(20), default='active')
    assn_member = db.Column(db.Boolean, default=False)
    gst = db.Column(db.String(20), nullable=True)
    pincode = db.Column(db.String(10), nullable=True)
    
    # Existing fields
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
    property_type = db.relationship('PropertyType', backref=db.backref('sellers', lazy=True))
    target_market_relationships = db.relationship('Interest', secondary=seller_target_markets,
                                                 backref=db.backref('seller_profiles', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'business_name': self.business_name,
            'description': self.description,
            'seller_type': self.seller_type,
            'target_market': self.target_market,
            'property_type': self.property_type.to_dict() if self.property_type else None,
            'status': self.status,
            'assn_member': self.assn_member,
            'gst': self.gst,
            'pincode': self.pincode,
            'logo_url': self.logo_url,
            'website': self.website,
            'contact_email': self.contact_email,
            'contact_phone': self.contact_phone,
            'address': self.address,
            'is_verified': self.is_verified,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'target_market_relationships': [interest.to_dict() for interest in self.target_market_relationships]
        }

class Stall(db.Model):
    __tablename__ = 'stalls'
    
    id = db.Column(db.Integer, primary_key=True)
    seller_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    stall_type_id = db.Column(db.Integer, db.ForeignKey('stall_types.id'), nullable=False)
    number = db.Column(db.String(20), nullable=False)
    
    # Enhanced fields
    allocated_stall_number = db.Column(db.String(20), nullable=True)
    fascia_name = db.Column(db.String(100), nullable=True)
    microsite_url = db.Column(db.String(255), nullable=True)
    is_allocated = db.Column(db.Boolean, default=False)
    
    # Backward compatibility fields
    stall_type = db.Column(db.String(50), nullable=True)
    price = db.Column(db.Float, nullable=True)
    size = db.Column(db.String(50), nullable=True)
    allowed_attendees = db.Column(db.Integer, nullable=True)
    max_meetings_per_attendee = db.Column(db.Integer, nullable=True)
    min_meetings_per_attendee = db.Column(db.Integer, nullable=True)
    inclusions = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    # Relationships
    seller = db.relationship('User', backref=db.backref('stalls', lazy=True))
    stall_type_rel = db.relationship('StallType', backref=db.backref('stalls', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'seller_id': self.seller_id,
            'number': self.number,
            'allocated_stall_number': self.allocated_stall_number,
            'fascia_name': self.fascia_name,
            'microsite_url': self.microsite_url,
            'is_allocated': self.is_allocated,
            'stall_type': self.stall_type,
            'stall_type_info': self.stall_type_rel.to_dict() if self.stall_type_rel else None,
            'price': self.price or (float(self.stall_type_rel.price) if self.stall_type_rel else None),
            'size': self.size or (self.stall_type_rel.size if self.stall_type_rel else None),
            'allowed_attendees': self.allowed_attendees or (self.stall_type_rel.allowed_attendees if self.stall_type_rel else None),
            'max_meetings_per_attendee': self.max_meetings_per_attendee or (self.stall_type_rel.max_meetings_per_attendee if self.stall_type_rel else None),
            'min_meetings_per_attendee': self.min_meetings_per_attendee or (self.stall_type_rel.min_meetings_per_attendee if self.stall_type_rel else None),
            'inclusions': self.inclusions or (self.stall_type_rel.inclusions if self.stall_type_rel else None),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'seller_business_name': self.seller.seller_profile.business_name if self.seller and self.seller.seller_profile else None
        }

# Keep all existing models for backward compatibility

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
                'email': self.seller.email,
                'business_name': self.seller.seller_profile.business_name if self.seller.seller_profile else self.seller.business_name
            },
            'time_slot': self.time_slot.to_dict() if self.time_slot else None
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

class TravelPlan(db.Model):
    __tablename__ = 'travel_plans'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_name = db.Column(db.String(120), nullable=False)
    event_start_date = db.Column(db.Date, nullable=False)
    event_end_date = db.Column(db.Date, nullable=False)
    venue = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref=db.backref('travel_plans', lazy=True))
    transportation = db.relationship('Transportation', backref='travel_plan', uselist=False, cascade='all, delete-orphan')
    accommodation = db.relationship('Accommodation', backref='travel_plan', uselist=False, cascade='all, delete-orphan')
    ground_transportation = db.relationship('GroundTransportation', backref='travel_plan', uselist=False, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'event_name': self.event_name,
            'event_start_date': self.event_start_date.isoformat() if self.event_start_date else None,
            'event_end_date': self.event_end_date.isoformat() if self.event_end_date else None,
            'venue': self.venue,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'transportation': self.transportation.to_dict() if self.transportation else None,
            'accommodation': self.accommodation.to_dict() if self.accommodation else None,
            'ground_transportation': self.ground_transportation.to_dict() if self.ground_transportation else None
        }

class Transportation(db.Model):
    __tablename__ = 'transportation'
    
    id = db.Column(db.Integer, primary_key=True)
    travel_plan_id = db.Column(db.Integer, db.ForeignKey('travel_plans.id'), nullable=False)
    type = db.Column(db.String(20), nullable=False)  # Primary transportation type
    
    # Individual transportation types for outbound and return journeys
    outbound_type = db.Column(db.String(20), nullable=True)  # Can be different from main type
    return_type = db.Column(db.String(20), nullable=True)    # Can be different from main type
    
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
            'id': self.id,
            'travel_plan_id': self.travel_plan_id,
            'type': self.type,
            'outbound': {
                'type': self.outbound_type or self.type,  # Use individual type or fall back to main type
                'carrier': self.outbound_carrier,
                'number': self.outbound_number,
                'departure_location': self.outbound_departure_location,
                'departure_datetime': self.outbound_departure_datetime.isoformat() if self.outbound_departure_datetime else None,
                'arrival_location': self.outbound_arrival_location,
                'arrival_datetime': self.outbound_arrival_datetime.isoformat() if self.outbound_arrival_datetime else None,
                'booking_reference': self.outbound_booking_reference,
                'seat_info': self.outbound_seat_info
            },
            'return': {
                'type': self.return_type or self.type,  # Use individual type or fall back to main type
                'carrier': self.return_carrier,
                'number': self.return_number,
                'departure_location': self.return_departure_location,
                'departure_datetime': self.return_departure_datetime.isoformat() if self.return_departure_datetime else None,
                'arrival_location': self.return_arrival_location,
                'arrival_datetime': self.return_arrival_datetime.isoformat() if self.return_arrival_datetime else None,
                'booking_reference': self.return_booking_reference,
                'seat_info': self.return_seat_info
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
            'id': self.id,
            'travel_plan_id': self.travel_plan_id,
            'name': self.name,
            'address': self.address,
            'check_in_datetime': self.check_in_datetime.isoformat() if self.check_in_datetime else None,
            'check_out_datetime': self.check_out_datetime.isoformat() if self.check_out_datetime else None,
            'room_type': self.room_type,
            'booking_reference': self.booking_reference,
            'special_notes': self.special_notes
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
            'id': self.id,
            'travel_plan_id': self.travel_plan_id,
            'pickup': {
                'location': self.pickup_location,
                'datetime': self.pickup_datetime.isoformat() if self.pickup_datetime else None,
                'vehicle_type': self.pickup_vehicle_type,
                'driver_contact': self.pickup_driver_contact
            },
            'dropoff': {
                'location': self.dropoff_location,
                'datetime': self.dropoff_datetime.isoformat() if self.dropoff_datetime else None,
                'vehicle_type': self.dropoff_vehicle_type,
                'driver_contact': self.dropoff_driver_contact
            }
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
    
    seller = db.relationship('User', backref=db.backref('listings', lazy=True))
    available_dates = db.relationship('ListingDate', backref='listing', lazy=True, cascade='all, delete-orphan')

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
    
    admin = db.relationship('User', backref=db.backref('invited_buyers', lazy=True))

class PendingBuyer(db.Model):
    __tablename__ = 'pending_buyers'
    
    id = db.Column(db.Integer, primary_key=True)
    invited_buyer_id = db.Column(db.Integer, db.ForeignKey('invited_buyers.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    designation = db.Column(db.String(30), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    invited_buyer = db.relationship('InvitedBuyer', backref=db.backref('pending_registration', uselist=False))

class DomainRestriction(db.Model):
    __tablename__ = 'domain_restrictions'
    
    id = db.Column(db.Integer, primary_key=True)
    domain = db.Column(db.String(100), unique=True, nullable=False)
    is_enabled = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
