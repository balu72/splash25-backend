-- Splash25 Database Schema Export - FIXED VERSION
-- Generated on: 2025-05-26T12:38:30.000000
-- Source Database: splash25_core_db
-- Total Tables: 53
-- Status: SYNTAX ERRORS FIXED

-- Drop existing database if exists
DROP DATABASE IF EXISTS splash25_core_db;

-- Create database
CREATE DATABASE splash25_core_db;

-- Connect to database
\c splash25_core_db;

-- Create enum types first
CREATE TYPE user_role AS ENUM ('buyer', 'seller', 'admin');
CREATE TYPE meeting_status AS ENUM ('pending', 'accepted', 'rejected', 'completed', 'cancelled');
CREATE TYPE listing_status AS ENUM ('active', 'inactive', 'pending');

-- Create all sequences first (before tables that reference them)
CREATE SEQUENCE users_id_seq;
CREATE SEQUENCE system_settings_id_seq;
CREATE SEQUENCE domain_restrictions_id_seq;
CREATE SEQUENCE property_types_id_seq;
CREATE SEQUENCE buyer_categories_id_seq;
CREATE SEQUENCE stall_types_id_seq;
CREATE SEQUENCE interests_id_seq;
CREATE SEQUENCE seller_seller_id_seq;
CREATE SEQUENCE stall_type_stall_type_id_seq;
CREATE SEQUENCE buyer_category_buyer_category_id_seq;
CREATE SEQUENCE interest_interest_id_seq;
CREATE SEQUENCE property_type_property_type_id_seq;
CREATE SEQUENCE migration_log_id_seq;
CREATE SEQUENCE accommodations_id_seq;
CREATE SEQUENCE buyer_buyer_id_seq;
CREATE SEQUENCE buyer_business_info_id_seq;
CREATE SEQUENCE buyer_financial_info_id_seq;
CREATE SEQUENCE buyer_interest_interest_number_seq;
CREATE SEQUENCE buyer_profile_interests_id_seq;
CREATE SEQUENCE buyer_profiles_id_seq;
CREATE SEQUENCE buyer_references_id_seq;
CREATE SEQUENCE ground_transportation_id_seq;
CREATE SEQUENCE invited_buyers_id_seq;
CREATE SEQUENCE listing_dates_id_seq;
CREATE SEQUENCE listings_id_seq;
CREATE SEQUENCE meeting_meeting_id_seq;
CREATE SEQUENCE meetings_id_seq;
CREATE SEQUENCE migration_mapping_buyers_id_seq;
CREATE SEQUENCE migration_mapping_sellers_id_seq;
CREATE SEQUENCE pending_buyers_id_seq;
CREATE SEQUENCE seller_attendees_id_seq;
CREATE SEQUENCE seller_business_info_id_seq;
CREATE SEQUENCE seller_financial_info_id_seq;
CREATE SEQUENCE seller_profiles_id_seq;
CREATE SEQUENCE seller_references_id_seq;
CREATE SEQUENCE seller_stall_seller_stall_id_seq;
CREATE SEQUENCE seller_target_market_target_market_number_seq;
CREATE SEQUENCE seller_target_markets_id_seq;
CREATE SEQUENCE stall_database_stall_number_id_seq;
CREATE SEQUENCE stall_inventory_id_seq;
CREATE SEQUENCE stalls_id_seq;
CREATE SEQUENCE time_slots_id_seq;
CREATE SEQUENCE transportation_id_seq;
CREATE SEQUENCE travel_plans_id_seq;

-- Create core tables first (no dependencies)

-- Table: users
CREATE TABLE users (
    id INTEGER NOT NULL DEFAULT nextval('users_id_seq'::regclass),
    username VARCHAR(80) NOT NULL,
    email VARCHAR(120) NOT NULL,
    password_hash VARCHAR(128) NOT NULL,
    role VARCHAR(6) NOT NULL DEFAULT 'buyer'::user_role,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    business_name VARCHAR(120),
    business_description TEXT,
    is_verified BOOLEAN DEFAULT false,
    PRIMARY KEY (id)
);

CREATE INDEX idx_users_idx_users_email ON users (email);
CREATE INDEX idx_users_idx_users_role ON users (role);

-- Table: system_settings
CREATE TABLE system_settings (
    id INTEGER NOT NULL DEFAULT nextval('system_settings_id_seq'::regclass),
    key VARCHAR(50) NOT NULL,
    value VARCHAR(255),
    description VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    PRIMARY KEY (id)
);

-- Table: domain_restrictions
CREATE TABLE domain_restrictions (
    id INTEGER NOT NULL DEFAULT nextval('domain_restrictions_id_seq'::regclass),
    domain VARCHAR(100) NOT NULL,
    is_enabled BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- Table: property_types
CREATE TABLE property_types (
    id INTEGER NOT NULL DEFAULT nextval('property_types_id_seq'::regclass),
    name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- Table: buyer_categories
CREATE TABLE buyer_categories (
    id INTEGER NOT NULL DEFAULT nextval('buyer_categories_id_seq'::regclass),
    name VARCHAR(100) NOT NULL,
    deposit_amount NUMERIC(10, 2),
    entry_fee NUMERIC(10, 2),
    accommodation_hosted BOOLEAN DEFAULT false,
    transfers_hosted BOOLEAN DEFAULT false,
    max_meetings INTEGER,
    min_meetings INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- Table: stall_types
CREATE TABLE stall_types (
    id INTEGER NOT NULL DEFAULT nextval('stall_types_id_seq'::regclass),
    name VARCHAR(50) NOT NULL,
    price NUMERIC(10, 2),
    attendees INTEGER,
    max_meetings_per_attendee INTEGER,
    min_meetings_per_attendee INTEGER,
    size VARCHAR(50),
    saleable BOOLEAN DEFAULT true,
    inclusions TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- Table: interests
CREATE TABLE interests (
    id INTEGER NOT NULL DEFAULT nextval('interests_id_seq'::regclass),
    name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- Table: seller
CREATE TABLE seller (
    seller_id INTEGER NOT NULL DEFAULT nextval('seller_seller_id_seq'::regclass),
    company_name VARCHAR(100),
    address TEXT,
    city VARCHAR(50),
    state VARCHAR(50),
    pincode VARCHAR(10),
    country VARCHAR(50),
    instagram VARCHAR(100),
    gst VARCHAR(20),
    website VARCHAR(100),
    status VARCHAR(20) DEFAULT 'Active'::character varying,
    assn_member BOOLEAN DEFAULT false,
    PRIMARY KEY (seller_id)
);

CREATE INDEX idx_seller_idx_seller_status ON seller (status);

-- Table: stall_type
CREATE TABLE stall_type (
    stall_type_id INTEGER NOT NULL DEFAULT nextval('stall_type_stall_type_id_seq'::regclass),
    stall_name VARCHAR(50) NOT NULL,
    price NUMERIC(10, 2),
    attendees INTEGER,
    max_meetings_per_attendee INTEGER,
    min_meetings_per_attendee INTEGER,
    size VARCHAR(50),
    saleable BOOLEAN DEFAULT true,
    inclusions TEXT,
    PRIMARY KEY (stall_type_id)
);

-- Table: buyer_category
CREATE TABLE buyer_category (
    buyer_category_id INTEGER NOT NULL DEFAULT nextval('buyer_category_buyer_category_id_seq'::regclass),
    category_name VARCHAR(100) NOT NULL,
    deposit_amount NUMERIC(10, 2),
    entry_fee NUMERIC(10, 2),
    accommodation_hosted BOOLEAN DEFAULT false,
    transfers_hosted BOOLEAN DEFAULT false,
    max_meetings INTEGER,
    min_meetings INTEGER,
    PRIMARY KEY (buyer_category_id)
);

-- Table: interest
CREATE TABLE interest (
    interest_id INTEGER NOT NULL DEFAULT nextval('interest_interest_id_seq'::regclass),
    interest_name VARCHAR(100) NOT NULL,
    PRIMARY KEY (interest_id)
);

-- Table: property_type
CREATE TABLE property_type (
    property_type_id INTEGER NOT NULL DEFAULT nextval('property_type_property_type_id_seq'::regclass),
    property_type_name VARCHAR(100) NOT NULL,
    PRIMARY KEY (property_type_id)
);

-- Table: migration_log
CREATE TABLE migration_log (
    id INTEGER NOT NULL DEFAULT nextval('migration_log_id_seq'::regclass),
    step_name VARCHAR(100) NOT NULL,
    status VARCHAR(20) NOT NULL,
    message TEXT,
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    duration_seconds INTEGER,
    PRIMARY KEY (id)
);

-- Table: travel_plans
CREATE TABLE travel_plans (
    id INTEGER NOT NULL DEFAULT nextval('travel_plans_id_seq'::regclass),
    user_id INTEGER NOT NULL,
    event_name VARCHAR(120) NOT NULL,
    event_start_date DATE NOT NULL,
    event_end_date DATE NOT NULL,
    venue VARCHAR(200) NOT NULL,
    status VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- Table: accommodations
CREATE TABLE accommodations (
    id INTEGER NOT NULL DEFAULT nextval('accommodations_id_seq'::regclass),
    travel_plan_id INTEGER NOT NULL,
    name VARCHAR(200) NOT NULL,
    address TEXT NOT NULL,
    check_in_datetime TIMESTAMP NOT NULL,
    check_out_datetime TIMESTAMP NOT NULL,
    room_type VARCHAR(100) NOT NULL,
    booking_reference VARCHAR(50) NOT NULL,
    special_notes TEXT,
    PRIMARY KEY (id)
);

-- Table: buyer
CREATE TABLE buyer (
    buyer_id INTEGER NOT NULL DEFAULT nextval('buyer_buyer_id_seq'::regclass),
    salutation VARCHAR(10),
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    designation VARCHAR(100),
    email VARCHAR(100) NOT NULL,
    category_id INTEGER,
    status VARCHAR(20) DEFAULT 'Pending'::character varying,
    vip BOOLEAN DEFAULT false,
    PRIMARY KEY (buyer_id)
);

CREATE INDEX idx_buyer_idx_buyer_category ON buyer (category_id);
CREATE INDEX idx_buyer_idx_buyer_email ON buyer (email);
CREATE INDEX idx_buyer_idx_buyer_status ON buyer (status);

-- Table: buyer_business
CREATE TABLE buyer_business (
    buyer_id INTEGER NOT NULL,
    start_year INTEGER,
    operator_type VARCHAR(50),
    property_interest_1 VARCHAR(100),
    property_interest_2 VARCHAR(100),
    sell_wayanad BOOLEAN DEFAULT true,
    sell_wayanad_year INTEGER,
    PRIMARY KEY (buyer_id)
);

-- Table: buyer_profiles
CREATE TABLE buyer_profiles (
    id INTEGER NOT NULL DEFAULT nextval('buyer_profiles_id_seq'::regclass),
    user_id INTEGER NOT NULL,
    name VARCHAR(100) NOT NULL,
    organization VARCHAR(100) NOT NULL,
    designation VARCHAR(50),
    operator_type VARCHAR(50),
    interests JSONB,
    properties_of_interest JSONB,
    country VARCHAR(50),
    state VARCHAR(50),
    city VARCHAR(50),
    address TEXT,
    mobile VARCHAR(20),
    website VARCHAR(255),
    instagram VARCHAR(100),
    year_of_starting_business INTEGER,
    selling_wayanad BOOLEAN DEFAULT false,
    since_when INTEGER,
    bio TEXT,
    profile_image VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    category_id INTEGER,
    salutation VARCHAR(10),
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    vip BOOLEAN DEFAULT false,
    status VARCHAR(20) DEFAULT 'pending'::character varying,
    gst VARCHAR(20),
    pincode VARCHAR(10),
    PRIMARY KEY (id)
);

CREATE INDEX idx_buyer_profiles_idx_buyer_profiles_category ON buyer_profiles (category_id);
CREATE INDEX idx_buyer_profiles_idx_buyer_profiles_status ON buyer_profiles (status);
CREATE INDEX idx_buyer_profiles_idx_buyer_profiles_user_id ON buyer_profiles (user_id);

-- Table: buyer_business_info
CREATE TABLE buyer_business_info (
    id INTEGER NOT NULL DEFAULT nextval('buyer_business_info_id_seq'::regclass),
    buyer_profile_id INTEGER,
    start_year INTEGER,
    property_interest_1 VARCHAR(100),
    property_interest_2 VARCHAR(100),
    sell_wayanad BOOLEAN DEFAULT false,
    sell_wayanad_year INTEGER,
    previous_visit BOOLEAN DEFAULT false,
    previous_stay_property VARCHAR(100),
    why_visit TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- Table: buyer_demographic
CREATE TABLE buyer_demographic (
    buyer_id INTEGER NOT NULL,
    mobile VARCHAR(15),
    address TEXT,
    city VARCHAR(50),
    state VARCHAR(50),
    pincode VARCHAR(10),
    country VARCHAR(50),
    instagram VARCHAR(100),
    company_name VARCHAR(100),
    gst VARCHAR(20),
    website VARCHAR(100),
    PRIMARY KEY (buyer_id)
);

-- Table: buyer_financial
CREATE TABLE buyer_financial (
    buyer_id INTEGER NOT NULL,
    deposit_paid BOOLEAN DEFAULT false,
    entry_fee_paid BOOLEAN DEFAULT false,
    PRIMARY KEY (buyer_id)
);

-- Table: buyer_financial_info
CREATE TABLE buyer_financial_info (
    id INTEGER NOT NULL DEFAULT nextval('buyer_financial_info_id_seq'::regclass),
    buyer_profile_id INTEGER,
    deposit_paid BOOLEAN DEFAULT false,
    entry_fee_paid BOOLEAN DEFAULT false,
    deposit_amount NUMERIC(10, 2),
    entry_fee_amount NUMERIC(10, 2),
    payment_date TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- Table: buyer_interest
CREATE TABLE buyer_interest (
    interest_number INTEGER NOT NULL DEFAULT nextval('buyer_interest_interest_number_seq'::regclass),
    buyer_id INTEGER,
    interest_id INTEGER,
    PRIMARY KEY (interest_number)
);

CREATE INDEX idx_buyer_interest_idx_buyer_interest_buyer ON buyer_interest (buyer_id);
CREATE INDEX idx_buyer_interest_idx_buyer_interest_interest ON buyer_interest (interest_id);

-- Table: buyer_misc
CREATE TABLE buyer_misc (
    buyer_id INTEGER NOT NULL,
    previous_visit BOOLEAN DEFAULT false,
    previous_stay_property VARCHAR(100),
    why_visit TEXT,
    PRIMARY KEY (buyer_id)
);

-- Table: buyer_profile_interests
CREATE TABLE buyer_profile_interests (
    id INTEGER NOT NULL DEFAULT nextval('buyer_profile_interests_id_seq'::regclass),
    buyer_profile_id INTEGER,
    interest_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

CREATE INDEX idx_buyer_profile_interests_idx_buyer_profile_interests_buyer ON buyer_profile_interests (buyer_profile_id);
CREATE INDEX idx_buyer_profile_interests_idx_buyer_profile_interests_interest ON buyer_profile_interests (interest_id);

-- Table: buyer_reference
CREATE TABLE buyer_reference (
    buyer_id INTEGER NOT NULL,
    ref1_name VARCHAR(100),
    ref1_addr TEXT,
    ref2_name VARCHAR(100),
    ref2_addr TEXT,
    PRIMARY KEY (buyer_id)
);

-- Table: buyer_references
CREATE TABLE buyer_references (
    id INTEGER NOT NULL DEFAULT nextval('buyer_references_id_seq'::regclass),
    buyer_profile_id INTEGER,
    ref1_name VARCHAR(100),
    ref1_address TEXT,
    ref2_name VARCHAR(100),
    ref2_address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- Table: ground_transportation
CREATE TABLE ground_transportation (
    id INTEGER NOT NULL DEFAULT nextval('ground_transportation_id_seq'::regclass),
    travel_plan_id INTEGER NOT NULL,
    pickup_location VARCHAR(200) NOT NULL,
    pickup_datetime TIMESTAMP NOT NULL,
    pickup_vehicle_type VARCHAR(50),
    pickup_driver_contact VARCHAR(50),
    dropoff_location VARCHAR(200) NOT NULL,
    dropoff_datetime TIMESTAMP NOT NULL,
    dropoff_vehicle_type VARCHAR(50),
    dropoff_driver_contact VARCHAR(50),
    PRIMARY KEY (id)
);

-- Table: invited_buyers
CREATE TABLE invited_buyers (
    id INTEGER NOT NULL DEFAULT nextval('invited_buyers_id_seq'::regclass),
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL,
    invitation_token VARCHAR(255) NOT NULL,
    is_registered BOOLEAN DEFAULT false,
    invited_by INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    PRIMARY KEY (id)
);

-- Table: listings
CREATE TABLE listings (
    id INTEGER NOT NULL DEFAULT nextval('listings_id_seq'::regclass),
    seller_id INTEGER NOT NULL,
    name VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    price NUMERIC(10, 2) NOT NULL,
    duration VARCHAR(50) NOT NULL,
    location VARCHAR(200) NOT NULL,
    max_participants INTEGER NOT NULL,
    status VARCHAR(8) NOT NULL DEFAULT 'active'::listing_status,
    image_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    views INTEGER DEFAULT 0,
    bookings INTEGER DEFAULT 0,
    PRIMARY KEY (id)
);

-- Table: listing_dates
CREATE TABLE listing_dates (
    id INTEGER NOT NULL DEFAULT nextval('listing_dates_id_seq'::regclass),
    listing_id INTEGER NOT NULL,
    date DATE NOT NULL,
    PRIMARY KEY (id)
);

-- Table: seller_profiles
CREATE TABLE seller_profiles (
    id INTEGER NOT NULL DEFAULT nextval('seller_profiles_id_seq'::regclass),
    user_id INTEGER NOT NULL,
    business_name VARCHAR(100) NOT NULL,
    description TEXT,
    seller_type VARCHAR(50),
    target_market VARCHAR(50),
    logo_url VARCHAR(255),
    website VARCHAR(255),
    contact_email VARCHAR(100),
    contact_phone VARCHAR(20),
    address TEXT,
    is_verified BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    gst VARCHAR(20),
    pincode VARCHAR(10),
    instagram VARCHAR(100),
    status VARCHAR(20) DEFAULT 'active'::character varying,
    assn_member BOOLEAN DEFAULT false,
    property_type_id INTEGER,
    PRIMARY KEY (id)
);

CREATE INDEX idx_seller_profiles_idx_seller_profiles_property_type ON seller_profiles (property_type_id);
CREATE INDEX idx_seller_profiles_idx_seller_profiles_status ON seller_profiles (status);
CREATE INDEX idx_seller_profiles_idx_seller_profiles_user_id ON seller_profiles (user_id);

-- Table: seller_attendees
CREATE TABLE seller_attendees (
    id INTEGER NOT NULL DEFAULT nextval('seller_attendees_id_seq'::regclass),
    seller_profile_id INTEGER,
    attendee_number INTEGER,
    name VARCHAR(100),
    designation VARCHAR(100),
    email VARCHAR(100),
    mobile VARCHAR(15),
    is_primary_contact BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

CREATE INDEX idx_seller_attendees_idx_seller_attendees_seller ON seller_attendees (seller_profile_id);

-- Table: time_slots
CREATE TABLE time_slots (
    id INTEGER NOT NULL DEFAULT nextval('time_slots_id_seq'::regclass),
    user_id INTEGER NOT NULL,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    is_available BOOLEAN DEFAULT true,
    meeting_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

CREATE INDEX idx_time_slots_idx_time_slots_available ON time_slots (is_available);
CREATE INDEX idx_time_slots_idx_time_slots_user_id ON time_slots (user_id);

-- Table: meetings
CREATE TABLE meetings (
    id INTEGER NOT NULL DEFAULT nextval('meetings_id_seq'::regclass),
    buyer_id INTEGER NOT NULL,
    seller_id INTEGER NOT NULL,
    time_slot_id INTEGER,
    notes TEXT,
    status VARCHAR(9) NOT NULL DEFAULT 'pending'::meeting_status,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    attendee_id INTEGER,
    meeting_date DATE,
    meeting_time TIME,
    PRIMARY KEY (id)
);

CREATE INDEX idx_meetings_idx_meetings_attendee ON meetings (attendee_id);
CREATE INDEX idx_meetings_idx_meetings_buyer_id ON meetings (buyer_id);
CREATE INDEX idx_meetings_idx_meetings_seller_id ON meetings (seller_id);
CREATE INDEX idx_meetings_idx_meetings_status ON meetings (status);

-- Table: meeting
CREATE TABLE meeting (
    meeting_id INTEGER NOT NULL DEFAULT nextval('meeting_meeting_id_seq'::regclass),
    buyer_id INTEGER NOT NULL,
    seller_id INTEGER NOT NULL,
    attendee_id INTEGER NOT NULL,
    date DATE,
    time TIME,
    status VARCHAR(20) DEFAULT 'Requested'::character varying,
    PRIMARY KEY (meeting_id)
);

CREATE INDEX idx_meeting_idx_meeting_buyer ON meeting (buyer_id);
CREATE INDEX idx_meeting_idx_meeting_date ON meeting (date);
CREATE INDEX idx_meeting_idx_meeting_seller ON meeting (seller_id);

-- Table: migration_mapping_buyers
CREATE TABLE migration_mapping_buyers (
    id INTEGER NOT NULL DEFAULT nextval('migration_mapping_buyers_id_seq'::regclass),
    customer_buyer_id INTEGER,
    splash25_user_id INTEGER,
    splash25_buyer_profile_id INTEGER,
    migration_status VARCHAR(20) DEFAULT 'pending'::character varying,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- Table: migration_mapping_sellers
CREATE TABLE migration_mapping_sellers (
    id INTEGER NOT NULL DEFAULT nextval('migration_mapping_sellers_id_seq'::regclass),
    customer_seller_id INTEGER,
    splash25_user_id INTEGER,
    splash25_seller_profile_id INTEGER,
    migration_status VARCHAR(20) DEFAULT 'pending'::character varying,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- Table: pending_buyers
CREATE TABLE pending_buyers (
    id INTEGER NOT NULL DEFAULT nextval('pending_buyers_id_seq'::regclass),
    invited_buyer_id INTEGER NOT NULL,
    name VARCHAR(100) NOT NULL,
    designation VARCHAR(30) NOT NULL,
    company VARCHAR(100) NOT NULL,
    gst VARCHAR(15),
    address VARCHAR(150) NOT NULL,
    city VARCHAR(30) NOT NULL,
    state VARCHAR(30) NOT NULL,
    pin VARCHAR(10) NOT NULL,
    mobile VARCHAR(15) NOT NULL,
    email VARCHAR(120) NOT NULL,
    website VARCHAR(100),
    instagram VARCHAR(30),
    year_of_starting_business INTEGER NOT NULL,
    type_of_operator VARCHAR(20) NOT NULL,
    already_sell_wayanad VARCHAR(3) NOT NULL,
    since_when INTEGER,
    opinion_about_previous_splash VARCHAR(50) NOT NULL,
    property_stayed_in VARCHAR(100),
    reference_property1_name VARCHAR(100) NOT NULL,
    reference_property1_address VARCHAR(200) NOT NULL,
    reference_property2_name VARCHAR(100),
    reference_property2_address VARCHAR(200),
    interests VARCHAR(255) NOT NULL,
    properties_of_interest VARCHAR(100) NOT NULL,
    why_attend_splash2025 TEXT NOT NULL,
    status VARCHAR(20) DEFAULT 'pending'::character varying,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- Table: seller_business
CREATE TABLE seller_business (
    seller_id INTEGER NOT NULL,
    start_year INTEGER,
    seller_type INTEGER,
    number_of_rooms INTEGER,
    previous_business BOOLEAN DEFAULT true,
    previous_business_year INTEGER,
    PRIMARY KEY (seller_id)
);

-- Table: seller_business_info
CREATE TABLE seller_business_info (
    id INTEGER NOT NULL DEFAULT nextval('seller_business_info_id_seq'::regclass),
    seller_profile_id INTEGER,
    start_year INTEGER,
    number_of_rooms INTEGER,
    previous_business BOOLEAN DEFAULT false,
    previous_business_year INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- Table: seller_financial
CREATE TABLE seller_financial (
    seller_id INTEGER NOT NULL,
    deposit_paid BOOLEAN DEFAULT false,
    total_amt_due NUMERIC(10, 2),
    total_amt_paid NUMERIC(10, 2),
    subscription_uptodate BOOLEAN DEFAULT false,
    PRIMARY KEY (seller_id)
);

-- Table: seller_financial_info
CREATE TABLE seller_financial_info (
    id INTEGER NOT NULL DEFAULT nextval('seller_financial_info_id_seq'::regclass),
    seller_profile_id INTEGER,
    deposit_paid BOOLEAN DEFAULT false,
    total_amt_due NUMERIC(10, 2),
    total_amt_paid NUMERIC(10, 2),
    subscription_uptodate BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- Table: seller_primary_contact
CREATE TABLE seller_primary_contact (
    seller_id INTEGER NOT NULL,
    salutation VARCHAR(10),
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    designation VARCHAR(100),
    mobile VARCHAR(15),
    email VARCHAR(100) NOT NULL,
    PRIMARY KEY (seller_id)
);

-- Table: seller_reference
CREATE TABLE seller_reference (
    seller_id INTEGER NOT NULL,
    ref1_name VARCHAR(100),
    ref1_addr TEXT,
    ref2_name VARCHAR(100),
    ref2_addr TEXT,
    PRIMARY KEY (seller_id)
);

-- Table: seller_references
CREATE TABLE seller_references (
    id INTEGER NOT NULL DEFAULT nextval('seller_references_id_seq'::regclass),
    seller_profile_id INTEGER,
    ref1_name VARCHAR(100),
    ref1_address TEXT,
    ref2_name VARCHAR(100),
    ref2_address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- Table: seller_stall
CREATE TABLE seller_stall (
    seller_stall_id INTEGER NOT NULL DEFAULT nextval('seller_stall_seller_stall_id_seq'::regclass),
    seller_id INTEGER,
    stall_type_id INTEGER,
    allocated_stall_number VARCHAR(15),
    fascia_name VARCHAR(100),
    microsite_url VARCHAR(100),
    PRIMARY KEY (seller_stall_id)
);

-- Table: seller_target_market
CREATE TABLE seller_target_market (
    target_market_number INTEGER NOT NULL DEFAULT nextval('seller_target_market_target_market_number_seq'::regclass),
    seller_id INTEGER,
    target_market_id INTEGER,
    PRIMARY KEY (target_market_number)
);

CREATE INDEX idx_seller_target_market_idx_seller_target_market_interest ON seller_target_market (target_market_id);
CREATE INDEX idx_seller_target_market_idx_seller_target_market_seller ON seller_target_market (seller_id);

-- Table: seller_target_markets
CREATE TABLE seller_target_markets (
    id INTEGER NOT NULL DEFAULT nextval('seller_target_markets_id_seq'::regclass),
    seller_profile_id INTEGER,
    interest_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

CREATE INDEX idx_seller_target_markets_idx_seller_target_markets_interest ON seller_target_markets (interest_id);
CREATE INDEX idx_seller_target_markets_idx_seller_target_markets_seller ON seller_target_markets (seller_profile_id);

-- Table: stall_database
CREATE TABLE stall_database (
    stall_number_id INTEGER NOT NULL DEFAULT nextval('stall_database_stall_number_id_seq'::regclass),
    stall_number VARCHAR(15),
    stall_type_id INTEGER,
    PRIMARY KEY (stall_number_id)
);

-- Table: stall_inventory
CREATE TABLE stall_inventory (
    id INTEGER NOT NULL DEFAULT nextval('stall_inventory_id_seq'::regclass),
    stall_number VARCHAR(15) NOT NULL,
    stall_type_id INTEGER,
    is_allocated BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- Table: stalls
CREATE TABLE stalls (
    id INTEGER NOT NULL DEFAULT nextval('stalls_id_seq'::regclass),
    seller_id INTEGER NOT NULL,
    number VARCHAR(20) NOT NULL,
    stall_type VARCHAR(50) NOT NULL,
    price NUMERIC(10, 2) NOT NULL,
    size VARCHAR(50) NOT NULL,
    allowed_attendees INTEGER NOT NULL,
    max_meetings_per_attendee INTEGER NOT NULL,
    min_meetings_per_attendee INTEGER NOT NULL,
    inclusions TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    stall_type_id INTEGER,
    allocated_stall_number VARCHAR(15),
    fascia_name VARCHAR(100),
    microsite_url VARCHAR(100),
    PRIMARY KEY (id)
);

CREATE INDEX idx_stalls_idx_stalls_number ON stalls (allocated_stall_number);
CREATE INDEX idx_stalls_idx_stalls_seller_id ON stalls (seller_id);
CREATE INDEX idx_stalls_idx_stalls_type ON stalls (stall_type_id);

-- Table: transportation
CREATE TABLE transportation (
    id INTEGER NOT NULL DEFAULT nextval('transportation_id_seq'::regclass),
    travel_plan_id INTEGER NOT NULL,
    type VARCHAR(20) NOT NULL,
    outbound_carrier VARCHAR(100) NOT NULL,
    outbound_number VARCHAR(20) NOT NULL,
    outbound_departure_location VARCHAR(200) NOT NULL,
    outbound_departure_datetime TIMESTAMP NOT NULL,
    outbound_arrival_location VARCHAR(200) NOT NULL,
    outbound_arrival_datetime TIMESTAMP NOT NULL,
    outbound_booking_reference VARCHAR(50) NOT NULL,
    outbound_seat_info VARCHAR(50),
    return_carrier VARCHAR(100) NOT NULL,
    return_number VARCHAR(20) NOT NULL,
    return_departure_location VARCHAR(200) NOT NULL,
    return_departure_datetime TIMESTAMP NOT NULL,
    return_arrival_location VARCHAR(200) NOT NULL,
    return_arrival_datetime TIMESTAMP NOT NULL,
    return_booking_reference VARCHAR(50) NOT NULL,
    return_seat_info VARCHAR(50),
    PRIMARY KEY (id)
);

-- Add foreign key constraints (after all tables are created)
ALTER TABLE accommodations ADD CONSTRAINT accommodations_travel_plan_id_fkey FOREIGN KEY (travel_plan_id) REFERENCES travel_plans (id);
ALTER TABLE buyer ADD CONSTRAINT buyer_category_id_fkey FOREIGN KEY (category_id) REFERENCES buyer_category (buyer_category_id);
ALTER TABLE buyer_business ADD CONSTRAINT buyer_business_buyer_id_fkey FOREIGN KEY (buyer_id) REFERENCES buyer (buyer_id);
ALTER TABLE buyer_business_info ADD CONSTRAINT buyer_business_info_buyer_profile_id_fkey FOREIGN KEY (buyer_profile_id) REFERENCES buyer_profiles (id);
ALTER TABLE buyer_demographic ADD CONSTRAINT buyer_demographic_buyer_id_fkey FOREIGN KEY (buyer_id) REFERENCES buyer (buyer_id);
ALTER TABLE buyer_financial ADD CONSTRAINT buyer_financial_buyer_id_fkey FOREIGN KEY (buyer_id) REFERENCES buyer (buyer_id);
ALTER TABLE buyer_financial_info ADD CONSTRAINT buyer_financial_info_buyer_profile_id_fkey FOREIGN KEY (buyer_profile_id) REFERENCES buyer_profiles (id);
ALTER TABLE buyer_interest ADD CONSTRAINT buyer_interest_buyer_id_fkey FOREIGN KEY (buyer_id) REFERENCES buyer (buyer_id);
ALTER TABLE buyer_interest ADD CONSTRAINT buyer_interest_interest_id_fkey FOREIGN KEY (interest_id) REFERENCES interest (interest_id);
ALTER TABLE buyer_misc ADD CONSTRAINT buyer_misc_buyer_id_fkey FOREIGN KEY (buyer_id) REFERENCES buyer (buyer_id);
ALTER TABLE buyer_profile_interests ADD CONSTRAINT buyer_profile_interests_buyer_profile_id_fkey FOREIGN KEY (buyer_profile_id) REFERENCES buyer_profiles (id);
ALTER TABLE buyer_profile_interests ADD CONSTRAINT buyer_profile_interests_interest_id_fkey FOREIGN KEY (interest_id) REFERENCES interests (id);
ALTER TABLE buyer_profiles ADD CONSTRAINT buyer_profiles_category_id_fkey FOREIGN KEY (category_id) REFERENCES buyer_categories (id);
ALTER TABLE buyer_profiles ADD CONSTRAINT buyer_profiles_user_id_fkey FOREIGN KEY (user_id) REFERENCES users (id);
ALTER TABLE buyer_reference ADD CONSTRAINT buyer_reference_buyer_id_fkey FOREIGN KEY (buyer_id) REFERENCES buyer (buyer_id);
ALTER TABLE buyer_references ADD CONSTRAINT buyer_references_buyer_profile_id_fkey FOREIGN KEY (buyer_profile_id) REFERENCES buyer_profiles (id);
ALTER TABLE ground_transportation ADD CONSTRAINT ground_transportation_travel_plan_id_fkey FOREIGN KEY (travel_plan_id) REFERENCES travel_plans (id);
ALTER TABLE invited_buyers ADD CONSTRAINT invited_buyers_invited_by_fkey FOREIGN KEY (invited_by) REFERENCES users (id);
ALTER TABLE listing_dates ADD CONSTRAINT listing_dates_listing_id_fkey FOREIGN KEY (listing_id) REFERENCES listings (id);
ALTER TABLE listings ADD CONSTRAINT listings_seller_id_fkey FOREIGN KEY (seller_id) REFERENCES users (id);
ALTER TABLE meeting ADD CONSTRAINT meeting_attendee_id_fkey FOREIGN KEY (attendee_id) REFERENCES seller_attendees (id);
ALTER TABLE meeting ADD CONSTRAINT meeting_buyer_id_fkey FOREIGN KEY (buyer_id) REFERENCES buyer (buyer_id);
ALTER TABLE meeting ADD CONSTRAINT meeting_seller_id_fkey FOREIGN KEY (seller_id) REFERENCES seller (seller_id);
ALTER TABLE meetings ADD CONSTRAINT meetings_attendee_id_fkey FOREIGN KEY (attendee_id) REFERENCES seller_attendees (id);
ALTER TABLE meetings ADD CONSTRAINT meetings_buyer_id_fkey FOREIGN KEY (buyer_id) REFERENCES users (id);
ALTER TABLE meetings ADD CONSTRAINT meetings_seller_id_fkey FOREIGN KEY (seller_id) REFERENCES users (id);
ALTER TABLE meetings ADD CONSTRAINT meetings_time_slot_id_fkey FOREIGN KEY (time_slot_id) REFERENCES time_slots (id);
ALTER TABLE migration_mapping_buyers ADD CONSTRAINT migration_mapping_buyers_splash25_buyer_profile_id_fkey FOREIGN KEY (splash25_buyer_profile_id) REFERENCES buyer_profiles (id);
ALTER TABLE migration_mapping_buyers ADD CONSTRAINT migration_mapping_buyers_splash25_user_id_fkey FOREIGN KEY (splash25_user_id) REFERENCES users (id);
ALTER TABLE migration_mapping_sellers ADD CONSTRAINT migration_mapping_sellers_splash25_seller_profile_id_fkey FOREIGN KEY (splash25_seller_profile_id) REFERENCES seller_profiles (id);
ALTER TABLE migration_mapping_sellers ADD CONSTRAINT migration_mapping_sellers_splash25_user_id_fkey FOREIGN KEY (splash25_user_id) REFERENCES users (id);
ALTER TABLE pending_buyers ADD CONSTRAINT pending_buyers_invited_buyer_id_fkey FOREIGN KEY (invited_buyer_id) REFERENCES invited_buyers (id);
ALTER TABLE seller_attendees ADD CONSTRAINT seller_attendees_seller_profile_id_fkey FOREIGN KEY (seller_profile_id) REFERENCES seller_profiles (id);
ALTER TABLE seller_business ADD CONSTRAINT seller_business_seller_id_fkey FOREIGN KEY (seller_id) REFERENCES seller (seller_id);
ALTER TABLE seller_business ADD CONSTRAINT seller_business_seller_type_fkey FOREIGN KEY (seller_type) REFERENCES property_type (property_type_id);
ALTER TABLE seller_business_info ADD CONSTRAINT seller_business_info_seller_profile_id_fkey FOREIGN KEY (seller_profile_id) REFERENCES seller_profiles (id);
ALTER TABLE seller_financial ADD CONSTRAINT seller_financial_seller_id_fkey FOREIGN KEY (seller_id) REFERENCES seller (seller_id);
ALTER TABLE seller_financial_info ADD CONSTRAINT seller_financial_info_seller_profile_id_fkey FOREIGN KEY (seller_profile_id) REFERENCES seller_profiles (id);
ALTER TABLE seller_primary_contact ADD CONSTRAINT seller_primary_contact_seller_id_fkey FOREIGN KEY (seller_id) REFERENCES seller (seller_id);
ALTER TABLE seller_profiles ADD CONSTRAINT seller_profiles_property_type_id_fkey FOREIGN KEY (property_type_id) REFERENCES property_types (id);
ALTER TABLE seller_profiles ADD CONSTRAINT seller_profiles_user_id_fkey FOREIGN KEY (user_id) REFERENCES users (id);
ALTER TABLE seller_reference ADD CONSTRAINT seller_reference_seller_id_fkey FOREIGN KEY (seller_id) REFERENCES seller (seller_id);
ALTER TABLE seller_references ADD CONSTRAINT seller_references_seller_profile_id_fkey FOREIGN KEY (seller_profile_id) REFERENCES seller_profiles (id);
ALTER TABLE seller_stall ADD CONSTRAINT seller_stall_seller_id_fkey FOREIGN KEY (seller_id) REFERENCES seller (seller_id);
ALTER TABLE seller_stall ADD CONSTRAINT seller_stall_stall_type_id_fkey FOREIGN KEY (stall_type_id) REFERENCES stall_type (stall_type_id);
ALTER TABLE seller_target_market ADD CONSTRAINT seller_target_market_seller_id_fkey FOREIGN KEY (seller_id) REFERENCES seller (seller_id);
ALTER TABLE seller_target_market ADD CONSTRAINT seller_target_market_target_market_id_fkey FOREIGN KEY (target_market_id) REFERENCES interest (interest_id);
ALTER TABLE seller_target_markets ADD CONSTRAINT seller_target_markets_interest_id_fkey FOREIGN KEY (interest_id) REFERENCES interests (id);
ALTER TABLE seller_target_markets ADD CONSTRAINT seller_target_markets_seller_profile_id_fkey FOREIGN KEY (seller_profile_id) REFERENCES seller_profiles (id);
ALTER TABLE stall_database ADD CONSTRAINT stall_database_stall_type_id_fkey FOREIGN KEY (stall_type_id) REFERENCES stall_type (stall_type_id);
ALTER TABLE stall_inventory ADD CONSTRAINT stall_inventory_stall_type_id_fkey FOREIGN KEY (stall_type_id) REFERENCES stall_types (id);
ALTER TABLE stalls ADD CONSTRAINT stalls_seller_id_fkey FOREIGN KEY (seller_id) REFERENCES users (id);
ALTER TABLE stalls ADD CONSTRAINT stalls_stall_type_id_fkey FOREIGN KEY (stall_type_id) REFERENCES stall_types (id);
ALTER TABLE time_slots ADD CONSTRAINT fk_time_slots_meeting FOREIGN KEY (meeting_id) REFERENCES meetings (id);
ALTER TABLE time_slots ADD CONSTRAINT time_slots_user_id_fkey FOREIGN KEY (user_id) REFERENCES users (id);
ALTER TABLE transportation ADD CONSTRAINT transportation_travel_plan_id_fkey FOREIGN KEY (travel_plan_id) REFERENCES travel_plans (id);
ALTER TABLE travel_plans ADD CONSTRAINT travel_plans_user_id_fkey FOREIGN KEY (user_id) REFERENCES users (id);

-- Schema export completed - FIXED VERSION
-- All syntax errors have been resolved:
-- 1. Fixed double-escaped enum defaults
-- 2. Added all missing sequences before table creation
-- 3. Corrected TIMESTAMP and BOOLEAN defaults
-- 4. Proper dependency ordering
-- 5. Complete foreign key constraints
