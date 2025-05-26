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
    name = db.Column(db.String(50), unique=True, nullable=False)  # Hosted, Pre-reg, Media, Blogger, Government, Student
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
    name = db.Column(db.String(50), unique=True, nullable=False)  # Homestay, Service Villa, Budget Resort, Premium Resort
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

class BuyerFinancialInfo(db.Model):
    __tablename__ = 'buyer_financial_info'
    
    id = db.Column(db.Integer, primary_key=True)
    buyer_profile_id = db.Column(db.Integer, db.ForeignKey('buyer_profiles.id'), nullable=False)
    deposit_paid = db.Column(db.Boolean, default=False)
    entry_fee_paid = db.Column(db.Boolean, default=False)
    payment_date = db.Column(db.DateTime, nullable=True)
    payment_reference = db.Column(db.String(100), nullable=True)
    
    # Relationships
    buyer_profile = db.relationship('BuyerProfile', backref=db.backref('financial_info', uselist=False))
    
    def to_dict(self):
        return {
            'id': self.id,
            'buyer_profile_id': self.buyer_profile_id,
            'deposit_paid': self.deposit_paid,
            'entry_fee_paid': self.entry_fee_paid,
            'payment_date': self.payment_date.isoformat() if self.payment_date else None,
            'payment_reference': self.payment_reference
        }

class SellerFinancialInfo(db.Model):
    __tablename__ = 'seller_financial_info'
    
    id = db.Column(db.Integer, primary_key=True)
    seller_profile_id = db.Column(db.Integer, db.ForeignKey('seller_profiles.id'), nullable=False)
    total_amt_due = db.Column(db.Numeric(10, 2), default=0.00)
    total_amt_paid = db.Column(db.Numeric(10, 2), default=0.00)
    deposit_paid = db.Column(db.Boolean, default=False)
    subscription_uptodate = db.Column(db.Boolean, default=False)
    
    # Relationships
    seller_profile = db.relationship('SellerProfile', backref=db.backref('financial_info', uselist=False))
    
    def to_dict(self):
        return {
            'id': self.id,
            'seller_profile_id': self.seller_profile_id,
            'total_amt_due': float(self.total_amt_due),
            'total_amt_paid': float(self.total_amt_paid),
            'deposit_paid': self.deposit_paid,
            'subscription_uptodate': self.subscription_uptodate
        }

class BuyerBusinessInfo(db.Model):
    __tablename__ = 'buyer_business_info'
    
    id = db.Column(db.Integer, primary_key=True)
    buyer_profile_id = db.Column(db.Integer, db.ForeignKey('buyer_profiles.id'), nullable=False)
    start_year = db.Column(db.Integer, nullable=True)
    sell_wayanad = db.Column(db.Boolean, default=False)
    sell_wayanad_year = db.Column(db.Integer, nullable=True)
    previous_visit = db.Column(db.Boolean, default=False)
    previous_stay_property = db.Column(db.String(200), nullable=True)
    property_interest_1 = db.Column(db.String(100), nullable=True)
    property_interest_2 = db.Column(db.String(100), nullable=True)
    why_visit = db.Column(db.Text, nullable=True)
    
    # Relationships
    buyer_profile = db.relationship('BuyerProfile', backref=db.backref('business_info', uselist=False))
    
    def to_dict(self):
        return {
            'id': self.id,
            'buyer_profile_id': self.buyer_profile_id,
            'start_year': self.start_year,
            'sell_wayanad': self.sell_wayanad,
            'sell_wayanad_year': self.sell_wayanad_year,
            'previous_visit': self.previous_visit,
            'previous_stay_property': self.previous_stay_property,
            'property_interest_1': self.property_interest_1,
            'property_interest_2': self.property_interest_2,
            'why_visit': self.why_visit
        }

class SellerBusinessInfo(db.Model):
    __tablename__ = 'seller_business_info'
    
    id = db.Column(db.Integer, primary_key=True)
    seller_profile_id = db.Column(db.Integer, db.ForeignKey('seller_profiles.id'), nullable=False)
    start_year = db.Column(db.Integer, nullable=True)
    number_of_rooms = db.Column(db.Integer, nullable=True)
    previous_business = db.Column(db.Boolean, default=False)
    previous_business_year = db.Column(db.Integer, nullable=True)
    
    # Relationships
    seller_profile = db.relationship('SellerProfile', backref=db.backref('business_info', uselist=False))
    
    def to_dict(self):
        return {
            'id': self.id,
            'seller_profile_id': self.seller_profile_id,
            'start_year': self.start_year,
            'number_of_rooms': self.number_of_rooms,
            'previous_business': self.previous_business,
            'previous_business_year': self.previous_business_year
        }

class BuyerReference(db.Model):
    __tablename__ = 'buyer_references'
    
    id = db.Column(db.Integer, primary_key=True)
    buyer_profile_id = db.Column(db.Integer, db.ForeignKey('buyer_profiles.id'), nullable=False)
    reference_1_name = db.Column(db.String(100), nullable=True)
    reference_1_contact = db.Column(db.String(100), nullable=True)
    reference_2_name = db.Column(db.String(100), nullable=True)
    reference_2_contact = db.Column(db.String(100), nullable=True)
    
    # Relationships
    buyer_profile = db.relationship('BuyerProfile', backref=db.backref('references', uselist=False))
    
    def to_dict(self):
        return {
            'id': self.id,
            'buyer_profile_id': self.buyer_profile_id,
            'reference_1_name': self.reference_1_name,
            'reference_1_contact': self.reference_1_contact,
            'reference_2_name': self.reference_2_name,
            'reference_2_contact': self.reference_2_contact
        }

class SellerReference(db.Model):
    __tablename__ = 'seller_references'
    
    id = db.Column(db.Integer, primary_key=True)
    seller_profile_id = db.Column(db.Integer, db.ForeignKey('seller_profiles.id'), nullable=False)
    reference_1_name = db.Column(db.String(100), nullable=True)
    reference_1_contact = db.Column(db.String(100), nullable=True)
    reference_2_name = db.Column(db.String(100), nullable=True)
    reference_2_contact = db.Column(db.String(100), nullable=True)
    
    # Relationships
    seller_profile = db.relationship('SellerProfile', backref=db.backref('references', uselist=False))
    
    def to_dict(self):
        return {
            'id': self.id,
            'seller_profile_id': self.seller_profile_id,
            'reference_1_name': self.reference_1_name,
            'reference_1_contact': self.reference_1_contact,
            'reference_2_name': self.reference_2_name,
            'reference_2_contact': self.reference_2_contact
        }

class SellerAttendee(db.Model):
    __tablename__ = 'seller_attendees'
    
    id = db.Column(db.Integer, primary_key=True)
    seller_profile_id = db.Column(db.Integer, db.ForeignKey('seller_profiles.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    designation = db.Column(db.String(50), nullable=True)
    mobile = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    is_primary = db.Column(db.Boolean, default=False)
    
    # Relationships
    seller_profile = db.relationship('SellerProfile', backref=db.backref('attendees', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'seller_profile_id': self.seller_profile_id,
            'name': self.name,
            'designation': self.designation,
            'mobile': self.mobile,
            'email': self.email,
            'is_primary': self.is_primary
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

class StallInventory(db.Model):
    __tablename__ = 'stall_inventory'
    
    id = db.Column(db.Integer, primary_key=True)
    stall_type_id = db.Column(db.Integer, db.ForeignKey('stall_types.id'), nullable=False)
    total_stalls = db.Column(db.Integer, default=0)
    allocated_stalls = db.Column(db.Integer, default=0)
    available_stalls = db.Column(db.Integer, default=0)
    
    # Relationships
    stall_type = db.relationship('StallType', backref=db.backref('inventory', uselist=False))
    
    def to_dict(self):
        return {
            'id': self.id,
            'stall_type_id': self.stall_type_id,
            'total_stalls': self.total_stalls,
            'allocated_stalls': self.allocated_stalls,
            'available_stalls': self.available_stalls
        }

# Enhanced existing models

class BuyerProfile(db.Model):
    __tablename__ = 'buyer_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    organization = db.Column(db.String(100), nullable=False)
    designation = db.Column(db.String(50), nullable=True)
    operator_type = db.Column(db.String(50), nullable=True)  # Tour Operator, Travel Agent, etc.
    
    # Enhanced fields
    category_id = db.Column(db.Integer, db.ForeignKey('buyer_categories.id'), nullable=True)
    salutation = db.Column(db.String(10), nullable=True)
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    vip = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, rejected
    gst = db.Column(db.String(20), nullable=True)
    pincode = db.Column(db.String(10), nullable=True)
    
    # Keep existing fields for backward compatibility
    interests = db.Column(db.JSON, nullable=True)  # Array of interests - will be migrated to relationships
    properties_of_interest = db.Column(db.JSON, nullable=True)  # Array of property types
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
    
    # Enhanced relationships
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
            'interests': self.interests or [],  # Backward compatibility
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
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'financial_info': self.financial_info.to_dict() if hasattr(self, 'financial_info') and self.financial_info else None,
            'business_info': self.business_info.to_dict() if hasattr(self, 'business_info') and self.business_info else None
        }

class SellerProfile(db.Model):
    __tablename__ = 'seller_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    business_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    seller_type = db.Column(db.String(50), nullable=True)  # e.g., "Resort", "Tour Operator", etc.
    target_market = db.Column(db.String(50), nullable=True)  # e.g., "Domestic", "International", etc.
    
    # Enhanced fields
    property_type_id = db.Column(db.Integer, db.ForeignKey('property_types.id'), nullable=True)
    status = db.Column(db.String(20), default='active')  # active, inactive, pending
    assn_member = db.Column(db.Boolean, default=False)  # Association member
    gst = db.Column(db.String(20), nullable=True)
    pincode = db.Column(db.String(10), nullable=True)
    
    # Keep existing fields
    logo_url = db.Column(db.String(255), nullable=True)
    website = db.Column(db.String(255), nullable=True)
    contact_email = db.Column(db.String(100), nullable=True)
    contact_phone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.Text, nullable=True)
    is_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    # Enhanced relationships
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
            'target_market_relationships': [interest.to_dict() for interest in self.target_market_relationships],
            'attendees': [attendee.to_dict() for attendee in self.attendees] if hasattr(self, 'attendees') else [],
            'financial_info': self.financial_info.to_dict() if hasattr(self, 'financial_info') and self.financial_info else None,
            'business_info': self.business_info.to_dict() if hasattr(self, 'business_info') and self.business_info else None
        }

class Stall(db.Model):
    __tablename__ = 'stalls'
    
    id = db.Column(db.Integer, primary_key=True)
    seller_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # Can be null for unallocated stalls
    stall_type_id = db.Column(db.Integer, db.ForeignKey('stall_types.id'), nullable=False)
    number = db.Column(db.String(20), nullable=False)
    
    # Enhanced fields
    allocated_stall_number = db.Column(db.String(20), nullable=True)
    fascia_name = db.Column(db.String(100), nullable=True)
    microsite_url = db.Column(db.String(255), nullable=True)
    is_allocated = db.Column(db.Boolean, default=False)
    
    # Keep existing fields for backward compatibility
    stall_type = db.Column(db.String(50), nullable=True)  # Will be replaced by stall_type_id
    price = db.Column(db.Float, nullable=True)  # Will come from StallType
    size = db.Column(db.String(50), nullable=True)  # Will come from StallType
    allowed_attendees = db.Column(db.Integer, nullable=True)  # Will come from StallType
    max_meetings_per_attendee = db.Column(db.Integer, nullable=True)  # Will come from StallType
    min_meetings_per_attendee = db.Column(db.Integer, nullable=True)  # Will come from StallType
    inclusions = db.Column(db.Text, nullable=True)  # Will come from StallType
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    # Enhanced relationships
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
            'stall_type': self.stall_type,  # Backward compatibility
            'stall_type_info': self.stall_type_rel.to_dict() if self.stall_type_rel else None,
            'price': self.price or (self.stall_type_rel.price if self.stall_type_rel else None),
            'size': self.size or (self.stall_type_rel.size if self.stall_type_rel else None),
            'allowed_attendees': self.allowed_attendees or (self.stall_type_rel.allowed_attendees if self.stall_type_rel else None),
            'max_meetings_per_attendee': self.max_meetings_per_attendee or (self.stall_type_rel.max_meetings_per_attendee if self.stall_type_rel else None),
            'min_meetings_per_attendee': self.min_meetings_per_attendee or (self.stall_type_rel.min_meetings_per_attendee if self.stall_type_rel else None),
            'inclusions': self.inclusions or (self.stall_type_rel.inclusions if self.stall_type_rel else None),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'seller_business_name': self.seller.seller_profile.business_name if self.seller and self.seller.seller_profile else None
        }

# Keep all existing models unchanged for backward compatibility

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
                'arr
