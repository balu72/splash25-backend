-- Splash25 Database Data Export
-- Generated on: 2025-05-26T12:17:30.614486
-- Source Database: splash25_core_db
-- Total Tables: 53

-- Connect to database
\c splash25_core_db;

-- Disable foreign key checks during data loading
SET session_replication_role = replica;

-- Table: buyer_categories (6 records)
INSERT INTO buyer_categories (id, name, deposit_amount, entry_fee, accommodation_hosted, transfers_hosted, max_meetings, min_meetings, created_at) VALUES
    (1, 'Hosted', '5000.00', '0.00', TRUE, TRUE, 30, 0, '2025-05-26T05:27:33.810811'),
    (2, 'Pre-reg', '0.00', '500.00', FALSE, FALSE, 0, 0, '2025-05-26T05:27:33.810811'),
    (3, 'Media', '0.00', '0.00', FALSE, FALSE, 0, 0, '2025-05-26T05:27:33.810811'),
    (4, 'Blogger', '0.00', '0.00', TRUE, TRUE, 0, 0, '2025-05-26T05:27:33.810811'),
    (5, 'Government', '0.00', '0.00', TRUE, TRUE, 0, 0, '2025-05-26T05:27:33.810811'),
    (6, 'Student', '0.00', '0.00', FALSE, FALSE, 0, 0, '2025-05-26T05:27:33.810811');

-- Table: buyer_category (6 records)
INSERT INTO buyer_category (buyer_category_id, category_name, deposit_amount, entry_fee, accommodation_hosted, transfers_hosted, max_meetings, min_meetings) VALUES
    (1, 'Hosted', '5000.00', '0.00', TRUE, TRUE, 30, 0),
    (2, 'Pre-reg', '0.00', '500.00', FALSE, FALSE, 0, 0),
    (3, 'Media', '0.00', '0.00', FALSE, FALSE, 0, 0),
    (4, 'Blogger', '0.00', '0.00', TRUE, TRUE, 0, 0),
    (5, 'Government', '0.00', '0.00', TRUE, TRUE, 0, 0),
    (6, 'Student', '0.00', '0.00', FALSE, FALSE, 0, 0);

-- Table: property_types (5 records)
INSERT INTO property_types (id, name, description, created_at) VALUES
    (1, 'Homestay', NULL, '2025-05-26T05:27:33.811149'),
    (2, 'Service Villa', NULL, '2025-05-26T05:27:33.811149'),
    (3, 'Budget Resort', NULL, '2025-05-26T05:27:33.811149'),
    (4, 'Premium Resort', NULL, '2025-05-26T05:27:33.811149'),
    (5, 'Not a property', NULL, '2025-05-26T05:27:33.811149');

-- Table: property_type (5 records)
INSERT INTO property_type (property_type_id, property_type_name) VALUES
    (1, 'Homestay'),
    (2, 'Service Villa'),
    (3, 'Budget Resort'),
    (4, 'Premium Resort'),
    (5, 'Not a property');

-- Table: interests (13 records)
INSERT INTO interests (id, name, description, created_at) VALUES
    (1, 'Adventure', NULL, '2025-05-26T05:27:33.810465'),
    (2, 'Agritourism', NULL, '2025-05-26T05:27:33.810465'),
    (3, 'Ayurveda', NULL, '2025-05-26T05:27:33.810465'),
    (4, 'Culture', NULL, '2025-05-26T05:27:33.810465'),
    (5, 'Family Holidays', NULL, '2025-05-26T05:27:33.810465'),
    (6, 'Honeymoon', NULL, '2025-05-26T05:27:33.810465'),
    (7, 'MICE', NULL, '2025-05-26T05:27:33.810465'),
    (8, 'Nature', NULL, '2025-05-26T05:27:33.810465'),
    (9, 'Schools & Colleges', NULL, '2025-05-26T05:27:33.810465'),
    (10, 'Spiritual', NULL, '2025-05-26T05:27:33.810465'),
    (11, 'Wildlife', NULL, '2025-05-26T05:27:33.810465'),
    (12, 'Yoga', NULL, '2025-05-26T05:27:33.810465'),
    (13, 'Sightseeing', NULL, '2025-05-26T05:27:33.810465');

-- Table: interest (13 records)
INSERT INTO interest (interest_id, interest_name) VALUES
    (1, 'Adventure'),
    (2, 'Agritourism'),
    (3, 'Ayurveda'),
    (4, 'Culture'),
    (5, 'Family Holidays'),
    (6, 'Honeymoon'),
    (7, 'MICE'),
    (8, 'Nature'),
    (9, 'Schools & Colleges'),
    (10, 'Spiritual'),
    (11, 'Wildlife'),
    (12, 'Yoga'),
    (13, 'Sightseeing');

-- Table: stall_types (8 records)
INSERT INTO stall_types (id, name, price, attendees, max_meetings_per_attendee, min_meetings_per_attendee, size, saleable, inclusions, created_at) VALUES
    (1, 'Standard Stall', '25000.00', 2, 30, 0, '2m x 2m', TRUE, 'Standard location, basic branding, meeting space, chairs, power supply', '2025-05-26T05:27:33.811451'),
    (2, 'Standard Corner', '27500.00', 2, 30, 0, '2m x 2m', TRUE, 'Corner location, meeting table, chairs, power supply, WiFi', '2025-05-26T05:27:33.811451'),
    (3, 'Premium Stall', '40000.00', 4, 30, 0, '4m x 2m', TRUE, 'Premium branding, meeting table, chairs, power supply, WiFi', '2025-05-26T05:27:33.811451'),
    (4, 'Premium Corner', '44000.00', 4, 30, 0, '4m x 2m', TRUE, 'Corner location, premium branding, meeting table, chairs, power supply, WiFi', '2025-05-26T05:27:33.811451'),
    (5, 'Tablespace', '12000.00', 1, 30, 0, '1.5m x 1m', TRUE, 'Table space, chairs, power supply', '2025-05-26T05:27:33.811451'),
    (6, 'WTO Standard Stall', '20000.00', 2, 30, 0, '2m x 2m', FALSE, 'Standard location, basic branding, meeting space, chairs, power supply', '2025-05-26T05:27:33.811451'),
    (7, 'FOC Std Stall', '0.00', 2, 0, 0, '2m x 2m', FALSE, 'Standard location, basic branding, meeting space, chairs, power supply', '2025-05-26T05:27:33.811451'),
    (8, 'Sponsor Stall', '0.00', 2, 0, 0, '2m x 2m', FALSE, 'Stall for Sponsor, meeting space, chairs, power supply', '2025-05-26T05:27:33.811451');

-- Table: stall_type (8 records)
INSERT INTO stall_type (stall_type_id, stall_name, price, attendees, max_meetings_per_attendee, min_meetings_per_attendee, size, saleable, inclusions) VALUES
    (1, 'Standard Stall', '25000.00', 2, 30, 0, '2m x 2m', TRUE, 'Standard location, basic branding, meeting space, chairs, power supply'),
    (2, 'Standard Corner', '27500.00', 2, 30, 0, '2m x 2m', TRUE, 'Corner location, meeting table, chairs, power supply, WiFi'),
    (3, 'Premium Stall', '40000.00', 4, 30, 0, '4m x 2m', TRUE, 'Premium branding, meeting table, chairs, power supply, WiFi'),
    (4, 'Premium Corner', '44000.00', 4, 30, 0, '4m x 2m', TRUE, 'Corner location, premium branding, meeting table, chairs, power supply, WiFi'),
    (5, 'Tablespace', '12000.00', 1, 30, 0, '1.5m x 1m', TRUE, 'Table space, chairs, power supply'),
    (6, 'WTO Standard Stall', '20000.00', 2, 30, 0, '2m x 2m', FALSE, 'Standard location, basic branding, meeting space, chairs, power supply'),
    (7, 'FOC Std Stall', '0.00', 2, 0, 0, '2m x 2m', FALSE, 'Standard location, basic branding, meeting space, chairs, power supply'),
    (8, 'Sponsor Stall', '0.00', 2, 0, 0, '2m x 2m', FALSE, 'Stall for Sponsor, meeting space, chairs, power supply');

-- Table domain_restrictions: No data

-- Table system_settings: No data

-- Table: migration_log (5 records)
INSERT INTO migration_log (id, step_name, status, message, started_at, completed_at, duration_seconds) VALUES
    (1, 'current_schema_creation', 'completed', 'Current Splash25 schema created successfully', '2025-05-26T05:27:33.646505', '2025-05-26T05:27:33.689347', 0),
    (2, 'customer_schema_conversion', 'completed', 'Customer schema converted to PostgreSQL successfully', '2025-05-26T05:27:33.703202', '2025-05-26T05:27:33.742034', 0),
    (3, 'customer_data_insertion', 'completed', 'Customer sample data inserted successfully', '2025-05-26T05:27:33.756310', '2025-05-26T05:27:33.766056', 0),
    (4, 'hybrid_integration', 'completed', 'Hybrid integration schema created successfully', '2025-05-26T05:27:33.779968', '2025-05-26T05:27:33.826856', 0),
    (5, 'data_migration', 'started', 'Starting customer data migration to Splash25 schema', '2025-05-26T05:27:33.840834', NULL, NULL);

-- Table: users (21 records)
INSERT INTO users (id, username, email, password_hash, role, created_at, business_name, business_description, is_verified) VALUES
    (1, 'rajesh.kumar', 'rajesh.kumar@wanderlust.com', '$2b$12$dummy.hash.for.migration.testing.only.replace.in.production', 'buyer', '2025-05-26T05:27:33.842751', 'Wanderlust Travels Pvt Ltd', NULL, TRUE),
    (2, 'priya.sharma', 'priya.sharma@dreamtravel.in', '$2b$12$dummy.hash.for.migration.testing.only.replace.in.production', 'buyer', '2025-05-26T05:27:33.842751', 'Dream Travel Solutions', NULL, TRUE),
    (3, 'amit.patel', 'amit.patel@explorindia.com', '$2b$12$dummy.hash.for.migration.testing.only.replace.in.production', 'buyer', '2025-05-26T05:27:33.842751', 'Explor India Tours', NULL, TRUE),
    (4, 'sunita.reddy', 'sunita.reddy@southtours.co.in', '$2b$12$dummy.hash.for.migration.testing.only.replace.in.production', 'buyer', '2025-05-26T05:27:33.842751', 'South India Tours & Travels', NULL, TRUE),
    (5, 'vikram.singh', 'vikram.singh@royaljourney.com', '$2b$12$dummy.hash.for.migration.testing.only.replace.in.production', 'buyer', '2025-05-26T05:27:33.842751', 'Royal Journey Travels', NULL, FALSE),
    (6, 'kavya.nair', 'kavya.nair@keralatours.in', '$2b$12$dummy.hash.for.migration.testing.only.replace.in.production', 'buyer', '2025-05-26T05:27:33.842751', 'Kerala Tours & Holidays', NULL, TRUE),
    (7, 'arjun.menon', 'arjun.menon@backwaters.com', '$2b$12$dummy.hash.for.migration.testing.only.replace.in.production', 'buyer', '2025-05-26T05:27:33.842751', 'Backwaters Kerala Pvt Ltd', NULL, TRUE),
    (8, 'deepika.iyer', 'deepika.iyer@spiceroute.in', '$2b$12$dummy.hash.for.migration.testing.only.replace.in.production', 'buyer', '2025-05-26T05:27:33.842751', 'Spice Route Travels', NULL, FALSE),
    (9, 'rohit.gupta', 'rohit.gupta@hillstation.com', '$2b$12$dummy.hash.for.migration.testing.only.replace.in.production', 'buyer', '2025-05-26T05:27:33.842751', 'Hill Station Holidays', NULL, TRUE),
    (10, 'ananya.das', 'ananya.das@bengaltours.in', '$2b$12$dummy.hash.for.migration.testing.only.replace.in.production', 'buyer', '2025-05-26T05:27:33.842751', 'Bengal Tours & Travels', NULL, TRUE),
    (11, 'suresh.nair', 'suresh.nair@backwaterbliss.com', '$2b$12$dummy.hash.for.migration.testing.only.replace.in.production', 'seller', '2025-05-26T05:27:33.847847', 'Backwater Bliss Resort', NULL, TRUE),
    (12, 'lakshmi.pillai', 'lakshmi.pillai@spicegardenretreat.com', '$2b$12$dummy.hash.for.migration.testing.only.replace.in.production', 'seller', '2025-05-26T05:27:33.847847', 'Spice Garden Retreat', NULL, TRUE),
    (13, 'ravi.kumar', 'ravi.kumar@coconutgrovehomestay.in', '$2b$12$dummy.hash.for.migration.testing.only.replace.in.production', 'seller', '2025-05-26T05:27:33.847847', 'Coconut Grove Homestay', NULL, TRUE),
    (14, 'meera.menon', 'meera.menon@mistymountainresort.com', '$2b$12$dummy.hash.for.migration.testing.only.replace.in.production', 'seller', '2025-05-26T05:27:33.847847', 'Misty Mountain Resort', NULL, TRUE),
    (15, 'ayush.sharma', 'ayush.sharma@ayurvedawellness.in', '$2b$12$dummy.hash.for.migration.testing.only.replace.in.production', 'seller', '2025-05-26T05:27:33.847847', 'Ayurveda Wellness Center', NULL, TRUE),
    (16, 'krishnan.nambiar', 'krishnan.nambiar@heritagehouseboat.com', '$2b$12$dummy.hash.for.migration.testing.only.replace.in.production', 'seller', '2025-05-26T05:27:33.847847', 'Heritage Houseboat', NULL, TRUE),
    (17, 'priya.varma', 'priya.varma@cliffedgeresort.in', '$2b$12$dummy.hash.for.migration.testing.only.replace.in.production', 'seller', '2025-05-26T05:27:33.847847', 'Cliff Edge Resort', NULL, TRUE),
    (18, 'arun.thampi', 'arun.thampi@teaestatevilla.com', '$2b$12$dummy.hash.for.migration.testing.only.replace.in.production', 'seller', '2025-05-26T05:27:33.847847', 'Tea Estate Villa', NULL, TRUE),
    (19, 'geetha.raj', 'geetha.raj@wayanadwildresort.com', '$2b$12$dummy.hash.for.migration.testing.only.replace.in.production', 'seller', '2025-05-26T05:27:33.847847', 'Wayanad Wild Resort', NULL, TRUE),
    (20, 'vinod.das', 'vinod.das@beachparadisehotel.com', '$2b$12$dummy.hash.for.migration.testing.only.replace.in.production', 'seller', '2025-05-26T05:27:33.847847', 'Beach Paradise Hotel', NULL, TRUE),
    (34, 'debug_user_1748240249', 'debug_1748240249@test.com', '$2b$12$dummy.hash.for.testing.purposes.only', 'buyer', '2025-05-26T06:17:29.029554', NULL, NULL, FALSE);

-- Table: buyer_profiles (11 records)
INSERT INTO buyer_profiles (id, user_id, name, organization, designation, operator_type, interests, properties_of_interest, country, state, city, address, mobile, website, instagram, year_of_starting_business, selling_wayanad, since_when, bio, profile_image, created_at, updated_at, category_id, salutation, first_name, last_name, vip, status, gst, pincode) VALUES
    (1, 1, 'Rajesh Kumar', 'Wanderlust Travels Pvt Ltd', 'CEO', 'Tour Operator', NULL, NULL, 'India', 'Karnataka', 'Bangalore', '123 MG Road', '+91-9876543210', 'www.wanderlust.com', '@wanderlust_travels', 2015, TRUE, 2020, NULL, NULL, '2025-05-26T05:27:33.843778', NULL, 1, 'Mr.', 'Rajesh', 'Kumar', TRUE, 'confirmed', '29ABCDE1234F1Z5', '560001'),
    (2, 2, 'Priya Sharma', 'Dream Travel Solutions', 'Director', 'Travel Agent', NULL, NULL, 'India', 'West Bengal', 'Kolkata', '456 Park Street', '+91-9876543211', 'www.dreamtravel.in', '@dreamtravel_official', 2012, TRUE, 2018, NULL, NULL, '2025-05-26T05:27:33.843778', NULL, 1, 'Ms.', 'Priya', 'Sharma', TRUE, 'confirmed', '19FGHIJ5678K2L6', '700016'),
    (3, 3, 'Amit Patel', 'Explor India Tours', 'Managing Director', 'DMC', NULL, NULL, 'India', 'Maharashtra', 'Pune', '789 FC Road', '+91-9876543212', 'www.explorindia.com', '@explorindia', 2018, TRUE, 2021, NULL, NULL, '2025-05-26T05:27:33.843778', NULL, 2, 'Mr.', 'Amit', 'Patel', FALSE, 'confirmed', '27MNOPQ9012R3S7', '411005'),
    (4, 4, 'Sunita Reddy', 'South India Tours & Travels', 'Founder', 'Tour Operator', NULL, NULL, 'India', 'Telangana', 'Hyderabad', '321 Jubilee Hills', '+91-9876543213', 'www.southtours.co.in', '@southtours', 2010, TRUE, 2016, NULL, NULL, '2025-05-26T05:27:33.843778', NULL, 2, 'Mrs.', 'Sunita', 'Reddy', FALSE, 'confirmed', '36TUVWX3456Y4Z8', '500033'),
    (5, 5, 'Vikram Singh', 'Royal Journey Travels', 'General Manager', 'Travel Agent', NULL, NULL, 'India', 'Delhi', 'Delhi', '654 Civil Lines', '+91-9876543214', 'www.royaljourney.com', '@royaljourney', 2020, FALSE, NULL, NULL, NULL, '2025-05-26T05:27:33.843778', NULL, 2, 'Mr.', 'Vikram', 'Singh', FALSE, 'pending', '07ABCDE7890F5G9', '110054'),
    (6, 6, 'Kavya Nair', 'Kerala Tours & Holidays', 'Operations Head', 'DMC', NULL, NULL, 'India', 'Kerala', 'Kochi', '987 Marine Drive', '+91-9876543215', 'www.keralatours.in', '@keralatours', 2014, TRUE, 2019, NULL, NULL, '2025-05-26T05:27:33.843778', NULL, 3, 'Ms.', 'Kavya', 'Nair', FALSE, 'confirmed', '32HIJKL2345M6N0', '682031'),
    (7, 7, 'Arjun Menon', 'Backwaters Kerala Pvt Ltd', 'Director', 'Tour Operator', NULL, NULL, 'India', 'Kerala', 'Kottayam', '147 Boat Club Road', '+91-9876543216', 'www.backwaters.com', '@backwaters_kerala', 2016, TRUE, 2020, NULL, NULL, '2025-05-26T05:27:33.843778', NULL, 3, 'Mr.', 'Arjun', 'Menon', FALSE, 'confirmed', '32OPQRS6789T7U1', '686001'),
    (8, 8, 'Deepika Iyer', 'Spice Route Travels', 'CEO', 'Travel Agent', NULL, NULL, 'India', 'Tamil Nadu', 'Chennai', '258 Anna Salai', '+91-9876543217', 'www.spiceroute.in', '@spiceroute', 2013, TRUE, 2017, NULL, NULL, '2025-05-26T05:27:33.843778', NULL, 3, 'Mrs.', 'Deepika', 'Iyer', FALSE, 'pending', '33VWXYZ0123A8B2', '600002'),
    (9, 9, 'Rohit Gupta', 'Hill Station Holidays', 'Manager', 'DMC', NULL, NULL, 'India', 'Himachal Pradesh', 'Shimla', '369 Mall Road', '+91-9876543218', 'www.hillstation.com', '@hillstation', 2019, FALSE, NULL, NULL, NULL, '2025-05-26T05:27:33.843778', NULL, 4, 'Mr.', 'Rohit', 'Gupta', FALSE, 'confirmed', '02CDEFG4567H9I3', '171001'),
    (10, 10, 'Ananya Das', 'Bengal Tours & Travels', 'Travel Consultant', 'Travel Agent', NULL, NULL, 'India', 'West Bengal', 'Kolkata', '741 Salt Lake', '+91-9876543219', 'www.bengaltours.in', '@bengaltours', 2011, TRUE, 2015, NULL, NULL, '2025-05-26T05:27:33.843778', NULL, 4, 'Ms.', 'Ananya', 'Das', FALSE, 'confirmed', '19JKLMN8901O0P4', '700064'),
    (34, 34, 'Debug Test User', 'Debug Org', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, FALSE, NULL, NULL, NULL, '2025-05-26T06:17:29.051716', NULL, NULL, 'Dr.', 'Debug', 'User', TRUE, 'active', 'GST123456789', '123456');

-- Table: seller_profiles (10 records)
INSERT INTO seller_profiles (id, user_id, business_name, description, seller_type, target_market, logo_url, website, contact_email, contact_phone, address, is_verified, created_at, updated_at, gst, pincode, instagram, status, assn_member, property_type_id) VALUES
    (1, 11, 'Backwater Bliss Resort', 'Migrated from customer database', NULL, NULL, NULL, 'www.backwaterbliss.com', 'suresh.nair@backwaterbliss.com', '+91-9447123456', 'Kumarakom Lake Side, Kumarakom, Kerala, 686563, India', TRUE, '2025-05-26T05:27:33.848301', NULL, '32ABCDE1234F1Z5', '686563', '@backwaterbliss', 'active', TRUE, 1),
    (2, 12, 'Spice Garden Retreat', 'Migrated from customer database', NULL, NULL, NULL, 'www.spicegardenretreat.com', 'lakshmi.pillai@spicegardenretreat.com', '+91-9447123457', 'Thekkady Hills, Thekkady, Kerala, 685536, India', TRUE, '2025-05-26T05:27:33.848301', NULL, '32FGHIJ5678K2L6', '685536', '@spicegarden', 'active', TRUE, 1),
    (3, 13, 'Coconut Grove Homestay', 'Migrated from customer database', NULL, NULL, NULL, 'www.coconutgrovehomestay.in', 'ravi.kumar@coconutgrovehomestay.in', '+91-9447123458', 'Alleppey Backwaters, Alleppey, Kerala, 688001, India', TRUE, '2025-05-26T05:27:33.848301', NULL, '32MNOPQ9012R3S7', '688001', '@coconutgrove', 'active', FALSE, 3),
    (4, 14, 'Misty Mountain Resort', 'Migrated from customer database', NULL, NULL, NULL, 'www.mistymountainresort.com', 'meera.menon@mistymountainresort.com', '+91-9447123459', 'Munnar Hills, Munnar, Kerala, 685612, India', TRUE, '2025-05-26T05:27:33.848301', NULL, '32TUVWX3456Y4Z8', '685612', '@mistymountain', 'active', TRUE, 1),
    (5, 15, 'Ayurveda Wellness Center', 'Migrated from customer database', NULL, NULL, NULL, 'www.ayurvedawellness.in', 'ayush.sharma@ayurvedawellness.in', '+91-9447123460', 'Kovalam Beach, Kovalam, Kerala, 695527, India', TRUE, '2025-05-26T05:27:33.848301', NULL, '32ABCDE7890F5G9', '695527', '@ayurvedawellness', 'active', TRUE, 1),
    (6, 16, 'Heritage Houseboat', 'Migrated from customer database', NULL, NULL, NULL, 'www.heritagehouseboat.com', 'krishnan.nambiar@heritagehouseboat.com', '+91-9447123461', 'Alleppey Canals, Alleppey, Kerala, 688012, India', TRUE, '2025-05-26T05:27:33.848301', NULL, '32HIJKL2345M6N0', '688012', '@heritagehouseboat', 'active', FALSE, 5),
    (7, 17, 'Cliff Edge Resort', 'Migrated from customer database', NULL, NULL, NULL, 'www.cliffedgeresort.in', 'priya.varma@cliffedgeresort.in', '+91-9447123462', 'Varkala Cliffs, Varkala, Kerala, 695141, India', TRUE, '2025-05-26T05:27:33.848301', NULL, '32OPQRS6789T7U1', '695141', '@cliffedge', 'active', TRUE, 1),
    (8, 18, 'Tea Estate Villa', 'Migrated from customer database', NULL, NULL, NULL, 'www.teaestatevilla.com', 'arun.thampi@teaestatevilla.com', '+91-9447123463', 'Munnar Tea Gardens, Munnar, Kerala, 685565, India', TRUE, '2025-05-26T05:27:33.848301', NULL, '32VWXYZ0123A8B2', '685565', '@teaestate', 'active', FALSE, 5),
    (9, 19, 'Wayanad Wild Resort', 'Migrated from customer database', NULL, NULL, NULL, 'www.wayanadwildresort.com', 'geetha.raj@wayanadwildresort.com', '+91-9447123464', 'Wayanad Forest, Wayanad, Kerala, 673121, India', TRUE, '2025-05-26T05:27:33.848301', NULL, '32CDEFG4567H9I3', '673121', '@wayanadwild', 'active', TRUE, 1),
    (10, 20, 'Beach Paradise Hotel', 'Migrated from customer database', NULL, NULL, NULL, 'www.beachparadisehotel.com', 'vinod.das@beachparadisehotel.com', '+91-9447123465', 'Kovalam Beach Road, Kovalam, Kerala, 695527, India', TRUE, '2025-05-26T05:27:33.848301', NULL, '32JKLMN0123O4P5', '695527', '@beachparadise', 'active', TRUE, 2);

-- Table: buyer (10 records)
INSERT INTO buyer (buyer_id, salutation, first_name, last_name, designation, email, category_id, status, vip) VALUES
    (1, 'Mr.', 'Rajesh', 'Kumar', 'CEO', 'rajesh.kumar@wanderlust.com', 1, 'Confirmed', TRUE),
    (2, 'Ms.', 'Priya', 'Sharma', 'Director', 'priya.sharma@dreamtravel.in', 1, 'Confirmed', TRUE),
    (3, 'Mr.', 'Amit', 'Patel', 'Managing Director', 'amit.patel@explorindia.com', 2, 'Confirmed', FALSE),
    (4, 'Mrs.', 'Sunita', 'Reddy', 'Founder', 'sunita.reddy@southtours.co.in', 2, 'Confirmed', FALSE),
    (5, 'Mr.', 'Vikram', 'Singh', 'General Manager', 'vikram.singh@royaljourney.com', 2, 'Pending', FALSE),
    (6, 'Ms.', 'Kavya', 'Nair', 'Operations Head', 'kavya.nair@keralatours.in', 3, 'Confirmed', FALSE),
    (7, 'Mr.', 'Arjun', 'Menon', 'Director', 'arjun.menon@backwaters.com', 3, 'Confirmed', FALSE),
    (8, 'Mrs.', 'Deepika', 'Iyer', 'CEO', 'deepika.iyer@spiceroute.in', 3, 'Pending', FALSE),
    (9, 'Mr.', 'Rohit', 'Gupta', 'Manager', 'rohit.gupta@hillstation.com', 4, 'Confirmed', FALSE),
    (10, 'Ms.', 'Ananya', 'Das', 'Travel Consultant', 'ananya.das@bengaltours.in', 4, 'Confirmed', FALSE);

-- Table: seller (10 records)
INSERT INTO seller (seller_id, company_name, address, city, state, pincode, country, instagram, gst, website, status, assn_member) VALUES
    (1, 'Backwater Bliss Resort', 'Kumarakom Lake Side', 'Kumarakom', 'Kerala', '686563', 'India', '@backwaterbliss', '32ABCDE1234F1Z5', 'www.backwaterbliss.com', 'Active', TRUE),
    (2, 'Spice Garden Retreat', 'Thekkady Hills', 'Thekkady', 'Kerala', '685536', 'India', '@spicegarden', '32FGHIJ5678K2L6', 'www.spicegardenretreat.com', 'Active', TRUE),
    (3, 'Coconut Grove Homestay', 'Alleppey Backwaters', 'Alleppey', 'Kerala', '688001', 'India', '@coconutgrove', '32MNOPQ9012R3S7', 'www.coconutgrovehomestay.in', 'Active', FALSE),
    (4, 'Misty Mountain Resort', 'Munnar Hills', 'Munnar', 'Kerala', '685612', 'India', '@mistymountain', '32TUVWX3456Y4Z8', 'www.mistymountainresort.com', 'Active', TRUE),
    (5, 'Ayurveda Wellness Center', 'Kovalam Beach', 'Kovalam', 'Kerala', '695527', 'India', '@ayurvedawellness', '32ABCDE7890F5G9', 'www.ayurvedawellness.in', 'Active', TRUE),
    (6, 'Heritage Houseboat', 'Alleppey Canals', 'Alleppey', 'Kerala', '688012', 'India', '@heritagehouseboat', '32HIJKL2345M6N0', 'www.heritagehouseboat.com', 'Active', FALSE),
    (7, 'Cliff Edge Resort', 'Varkala Cliffs', 'Varkala', 'Kerala', '695141', 'India', '@cliffedge', '32OPQRS6789T7U1', 'www.cliffedgeresort.in', 'Active', TRUE),
    (8, 'Tea Estate Villa', 'Munnar Tea Gardens', 'Munnar', 'Kerala', '685565', 'India', '@teaestate', '32VWXYZ0123A8B2', 'www.teaestatevilla.com', 'Active', FALSE),
    (9, 'Wayanad Wild Resort', 'Wayanad Forest', 'Wayanad', 'Kerala', '673121', 'India', '@wayanadwild', '32CDEFG4567H9I3', 'www.wayanadwildresort.com', 'Active', TRUE),
    (10, 'Beach Paradise Hotel', 'Kovalam Beach Road', 'Kovalam', 'Kerala', '695527', 'India', '@beachparadise', '32JKLMN0123O4P5', 'www.beachparadisehotel.com', 'Active', TRUE);

-- Table: buyer_business (10 records)
INSERT INTO buyer_business (buyer_id, start_year, operator_type, property_interest_1, property_interest_2, sell_wayanad, sell_wayanad_year) VALUES
    (1, 2015, 'Tour Operator', 'Luxury Resorts', 'Adventure Activities', TRUE, 2020),
    (2, 2012, 'Travel Agent', 'Heritage Hotels', 'Cultural Experiences', TRUE, 2018),
    (3, 2018, 'DMC', 'Eco Resorts', 'Wildlife Lodges', TRUE, 2021),
    (4, 2010, 'Tour Operator', 'Beach Resorts', 'Backwater Stays', TRUE, 2016),
    (5, 2020, 'Travel Agent', 'Boutique Hotels', 'Wellness Centers', FALSE, NULL),
    (6, 2014, 'DMC', 'Homestays', 'Houseboat Stays', TRUE, 2019),
    (7, 2016, 'Tour Operator', 'Backwater Resorts', 'Ayurveda Centers', TRUE, 2020),
    (8, 2013, 'Travel Agent', 'Cultural Properties', 'Spice Plantations', TRUE, 2017),
    (9, 2019, 'DMC', 'Hill Stations', 'Adventure Camps', FALSE, NULL),
    (10, 2011, 'Travel Agent', 'Budget Hotels', 'Local Experiences', TRUE, 2015);

-- Table: buyer_business_info (10 records)
INSERT INTO buyer_business_info (id, buyer_profile_id, start_year, property_interest_1, property_interest_2, sell_wayanad, sell_wayanad_year, previous_visit, previous_stay_property, why_visit, created_at) VALUES
    (1, 1, 2015, 'Luxury Resorts', 'Adventure Activities', TRUE, 2020, TRUE, 'Taj Kumarakom Resort', 'Expand luxury portfolio in Kerala', '2025-05-26T05:27:33.845434'),
    (2, 2, 2012, 'Heritage Hotels', 'Cultural Experiences', TRUE, 2018, FALSE, NULL, 'Explore new destinations for cultural tours', '2025-05-26T05:27:33.845434'),
    (3, 3, 2018, 'Eco Resorts', 'Wildlife Lodges', TRUE, 2021, TRUE, 'Spice Village Thekkady', 'Source eco-friendly properties', '2025-05-26T05:27:33.845434'),
    (4, 4, 2010, 'Beach Resorts', 'Backwater Stays', TRUE, 2016, TRUE, 'Backwater Ripples Kumarakom', 'Strengthen South India network', '2025-05-26T05:27:33.845434'),
    (5, 5, 2020, 'Boutique Hotels', 'Wellness Centers', FALSE, NULL, FALSE, NULL, 'Enter Kerala market for wellness tourism', '2025-05-26T05:27:33.845434'),
    (6, 6, 2014, 'Homestays', 'Houseboat Stays', TRUE, 2019, TRUE, 'Coconut Lagoon', 'Expand homestay network', '2025-05-26T05:27:33.845434'),
    (7, 7, 2016, 'Backwater Resorts', 'Ayurveda Centers', TRUE, 2020, TRUE, 'Kumarakom Lake Resort', 'Add premium backwater properties', '2025-05-26T05:27:33.845434'),
    (8, 8, 2013, 'Cultural Properties', 'Spice Plantations', TRUE, 2017, FALSE, NULL, 'Develop cultural tourism packages', '2025-05-26T05:27:33.845434'),
    (9, 9, 2019, 'Hill Stations', 'Adventure Camps', FALSE, NULL, FALSE, NULL, 'Explore hill station properties', '2025-05-26T05:27:33.845434'),
    (10, 10, 2011, 'Budget Hotels', 'Local Experiences', TRUE, 2015, TRUE, 'Local Homestay Alleppey', 'Budget-friendly options for clients', '2025-05-26T05:27:33.845434');

-- Table: buyer_demographic (10 records)
INSERT INTO buyer_demographic (buyer_id, mobile, address, city, state, pincode, country, instagram, company_name, gst, website) VALUES
    (1, '+91-9876543210', '123 MG Road', 'Bangalore', 'Karnataka', '560001', 'India', '@wanderlust_travels', 'Wanderlust Travels Pvt Ltd', '29ABCDE1234F1Z5', 'www.wanderlust.com'),
    (2, '+91-9876543211', '456 Park Street', 'Kolkata', 'West Bengal', '700016', 'India', '@dreamtravel_official', 'Dream Travel Solutions', '19FGHIJ5678K2L6', 'www.dreamtravel.in'),
    (3, '+91-9876543212', '789 FC Road', 'Pune', 'Maharashtra', '411005', 'India', '@explorindia', 'Explor India Tours', '27MNOPQ9012R3S7', 'www.explorindia.com'),
    (4, '+91-9876543213', '321 Jubilee Hills', 'Hyderabad', 'Telangana', '500033', 'India', '@southtours', 'South India Tours & Travels', '36TUVWX3456Y4Z8', 'www.southtours.co.in'),
    (5, '+91-9876543214', '654 Civil Lines', 'Delhi', 'Delhi', '110054', 'India', '@royaljourney', 'Royal Journey Travels', '07ABCDE7890F5G9', 'www.royaljourney.com'),
    (6, '+91-9876543215', '987 Marine Drive', 'Kochi', 'Kerala', '682031', 'India', '@keralatours', 'Kerala Tours & Holidays', '32HIJKL2345M6N0', 'www.keralatours.in'),
    (7, '+91-9876543216', '147 Boat Club Road', 'Kottayam', 'Kerala', '686001', 'India', '@backwaters_kerala', 'Backwaters Kerala Pvt Ltd', '32OPQRS6789T7U1', 'www.backwaters.com'),
    (8, '+91-9876543217', '258 Anna Salai', 'Chennai', 'Tamil Nadu', '600002', 'India', '@spiceroute', 'Spice Route Travels', '33VWXYZ0123A8B2', 'www.spiceroute.in'),
    (9, '+91-9876543218', '369 Mall Road', 'Shimla', 'Himachal Pradesh', '171001', 'India', '@hillstation', 'Hill Station Holidays', '02CDEFG4567H9I3', 'www.hillstation.com'),
    (10, '+91-9876543219', '741 Salt Lake', 'Kolkata', 'West Bengal', '700064', 'India', '@bengaltours', 'Bengal Tours & Travels', '19JKLMN8901O0P4', 'www.bengaltours.in');

-- Table: buyer_financial (10 records)
INSERT INTO buyer_financial (buyer_id, deposit_paid, entry_fee_paid) VALUES
    (1, TRUE, TRUE),
    (2, TRUE, TRUE),
    (3, TRUE, TRUE),
    (4, TRUE, TRUE),
    (5, FALSE, TRUE),
    (6, TRUE, TRUE),
    (7, TRUE, TRUE),
    (8, FALSE, FALSE),
    (9, TRUE, TRUE),
    (10, TRUE, TRUE);

-- Table: buyer_financial_info (10 records)
INSERT INTO buyer_financial_info (id, buyer_profile_id, deposit_paid, entry_fee_paid, deposit_amount, entry_fee_amount, payment_date, created_at) VALUES
    (1, 1, TRUE, TRUE, NULL, NULL, NULL, '2025-05-26T05:27:33.844801'),
    (2, 2, TRUE, TRUE, NULL, NULL, NULL, '2025-05-26T05:27:33.844801'),
    (3, 3, TRUE, TRUE, NULL, NULL, NULL, '2025-05-26T05:27:33.844801'),
    (4, 4, TRUE, TRUE, NULL, NULL, NULL, '2025-05-26T05:27:33.844801'),
    (5, 5, FALSE, TRUE, NULL, NULL, NULL, '2025-05-26T05:27:33.844801'),
    (6, 6, TRUE, TRUE, NULL, NULL, NULL, '2025-05-26T05:27:33.844801'),
    (7, 7, TRUE, TRUE, NULL, NULL, NULL, '2025-05-26T05:27:33.844801'),
    (8, 8, FALSE, FALSE, NULL, NULL, NULL, '2025-05-26T05:27:33.844801'),
    (9, 9, TRUE, TRUE, NULL, NULL, NULL, '2025-05-26T05:27:33.844801'),
    (10, 10, TRUE, TRUE, NULL, NULL, NULL, '2025-05-26T05:27:33.844801');

-- Table: buyer_misc (10 records)
INSERT INTO buyer_misc (buyer_id, previous_visit, previous_stay_property, why_visit) VALUES
    (1, TRUE, 'Taj Kumarakom Resort', 'Expand luxury portfolio in Kerala'),
    (2, FALSE, NULL, 'Explore new destinations for cultural tours'),
    (3, TRUE, 'Spice Village Thekkady', 'Source eco-friendly properties'),
    (4, TRUE, 'Backwater Ripples Kumarakom', 'Strengthen South India network'),
    (5, FALSE, NULL, 'Enter Kerala market for wellness tourism'),
    (6, TRUE, 'Coconut Lagoon', 'Expand homestay network'),
    (7, TRUE, 'Kumarakom Lake Resort', 'Add premium backwater properties'),
    (8, FALSE, NULL, 'Develop cultural tourism packages'),
    (9, FALSE, NULL, 'Explore hill station properties'),
    (10, TRUE, 'Local Homestay Alleppey', 'Budget-friendly options for clients');

-- Table: buyer_reference (10 records)
INSERT INTO buyer_reference (buyer_id, ref1_name, ref1_addr, ref2_name, ref2_addr) VALUES
    (1, 'Kerala Tourism Board', 'Thiruvananthapuram, Kerala', 'IATO Delhi', 'New Delhi'),
    (2, 'West Bengal Tourism', 'Kolkata, West Bengal', 'TAAI Mumbai', 'Mumbai, Maharashtra'),
    (3, 'Maharashtra Tourism', 'Mumbai, Maharashtra', 'ADTOI Pune', 'Pune, Maharashtra'),
    (4, 'Telangana Tourism', 'Hyderabad, Telangana', 'SITA Travels', 'Chennai, Tamil Nadu'),
    (5, 'Delhi Tourism', 'New Delhi', 'Cox & Kings', 'Mumbai, Maharashtra'),
    (6, 'Kochi Tourism', 'Kochi, Kerala', 'KTDC', 'Thiruvananthapuram, Kerala'),
    (7, 'Kumarakom Tourism', 'Kottayam, Kerala', 'DTPC Kottayam', 'Kottayam, Kerala'),
    (8, 'Tamil Nadu Tourism', 'Chennai, Tamil Nadu', 'TTDC', 'Chennai, Tamil Nadu'),
    (9, 'Himachal Tourism', 'Shimla, Himachal Pradesh', 'HPTDC', 'Shimla, Himachal Pradesh'),
    (10, 'WBTDC', 'Kolkata, West Bengal', 'Travel Agents Association', 'Kolkata, West Bengal');

-- Table: buyer_references (10 records)
INSERT INTO buyer_references (id, buyer_profile_id, ref1_name, ref1_address, ref2_name, ref2_address, created_at) VALUES
    (1, 1, 'Kerala Tourism Board', 'Thiruvananthapuram, Kerala', 'IATO Delhi', 'New Delhi', '2025-05-26T05:27:33.846031'),
    (2, 2, 'West Bengal Tourism', 'Kolkata, West Bengal', 'TAAI Mumbai', 'Mumbai, Maharashtra', '2025-05-26T05:27:33.846031'),
    (3, 3, 'Maharashtra Tourism', 'Mumbai, Maharashtra', 'ADTOI Pune', 'Pune, Maharashtra', '2025-05-26T05:27:33.846031'),
    (4, 4, 'Telangana Tourism', 'Hyderabad, Telangana', 'SITA Travels', 'Chennai, Tamil Nadu', '2025-05-26T05:27:33.846031'),
    (5, 5, 'Delhi Tourism', 'New Delhi', 'Cox & Kings', 'Mumbai, Maharashtra', '2025-05-26T05:27:33.846031'),
    (6, 6, 'Kochi Tourism', 'Kochi, Kerala', 'KTDC', 'Thiruvananthapuram, Kerala', '2025-05-26T05:27:33.846031'),
    (7, 7, 'Kumarakom Tourism', 'Kottayam, Kerala', 'DTPC Kottayam', 'Kottayam, Kerala', '2025-05-26T05:27:33.846031'),
    (8, 8, 'Tamil Nadu Tourism', 'Chennai, Tamil Nadu', 'TTDC', 'Chennai, Tamil Nadu', '2025-05-26T05:27:33.846031'),
    (9, 9, 'Himachal Tourism', 'Shimla, Himachal Pradesh', 'HPTDC', 'Shimla, Himachal Pradesh', '2025-05-26T05:27:33.846031'),
    (10, 10, 'WBTDC', 'Kolkata, West Bengal', 'Travel Agents Association', 'Kolkata, West Bengal', '2025-05-26T05:27:33.846031');

-- Table: seller_business (10 records)
INSERT INTO seller_business (seller_id, start_year, seller_type, number_of_rooms, previous_business, previous_business_year) VALUES
    (1, 2010, 1, 25, FALSE, 2008),
    (2, 2015, 1, 18, FALSE, 2012),
    (3, 2018, 3, 8, TRUE, 2016),
    (4, 2012, 1, 30, TRUE, 2010),
    (5, 2008, 1, 15, FALSE, 2005),
    (6, 2016, 5, 4, TRUE, 2014),
    (7, 2014, 1, 22, FALSE, 2012),
    (8, 2019, 5, 6, TRUE, 2017),
    (9, 2017, 1, 12, TRUE, 2015),
    (10, 2011, 2, 35, FALSE, 2009);

-- Table: seller_business_info (10 records)
INSERT INTO seller_business_info (id, seller_profile_id, start_year, number_of_rooms, previous_business, previous_business_year, created_at) VALUES
    (1, 1, 2010, 25, FALSE, 2008, '2025-05-26T05:27:33.849757'),
    (2, 2, 2015, 18, FALSE, 2012, '2025-05-26T05:27:33.849757'),
    (3, 3, 2018, 8, TRUE, 2016, '2025-05-26T05:27:33.849757'),
    (4, 4, 2012, 30, TRUE, 2010, '2025-05-26T05:27:33.849757'),
    (5, 5, 2008, 15, FALSE, 2005, '2025-05-26T05:27:33.849757'),
    (6, 6, 2016, 4, TRUE, 2014, '2025-05-26T05:27:33.849757'),
    (7, 7, 2014, 22, FALSE, 2012, '2025-05-26T05:27:33.849757'),
    (8, 8, 2019, 6, TRUE, 2017, '2025-05-26T05:27:33.849757'),
    (9, 9, 2017, 12, TRUE, 2015, '2025-05-26T05:27:33.849757'),
    (10, 10, 2011, 35, FALSE, 2009, '2025-05-26T05:27:33.849757');

-- Table: seller_financial (10 records)
INSERT INTO seller_financial (seller_id, deposit_paid, total_amt_due, total_amt_paid, subscription_uptodate) VALUES
    (1, TRUE, '150000.00', '150000.00', TRUE),
    (2, TRUE, '100000.00', '100000.00', TRUE),
    (3, FALSE, '75000.00', '50000.00', FALSE),
    (4, TRUE, '150000.00', '150000.00', TRUE),
    (5, TRUE, '125000.00', '125000.00', TRUE),
    (6, FALSE, '75000.00', '25000.00', FALSE),
    (7, TRUE, '100000.00', '100000.00', TRUE),
    (8, TRUE, '125000.00', '100000.00', FALSE),
    (9, TRUE, '100000.00', '100000.00', TRUE),
    (10, TRUE, '100000.00', '100000.00', TRUE);

-- Table: seller_financial_info (10 records)
INSERT INTO seller_financial_info (id, seller_profile_id, deposit_paid, total_amt_due, total_amt_paid, subscription_uptodate, created_at) VALUES
    (1, 1, TRUE, '150000.00', '150000.00', TRUE, '2025-05-26T05:27:33.850234'),
    (2, 2, TRUE, '100000.00', '100000.00', TRUE, '2025-05-26T05:27:33.850234'),
    (3, 3, FALSE, '75000.00', '50000.00', FALSE, '2025-05-26T05:27:33.850234'),
    (4, 4, TRUE, '150000.00', '150000.00', TRUE, '2025-05-26T05:27:33.850234'),
    (5, 5, TRUE, '125000.00', '125000.00', TRUE, '2025-05-26T05:27:33.850234'),
    (6, 6, FALSE, '75000.00', '25000.00', FALSE, '2025-05-26T05:27:33.850234'),
    (7, 7, TRUE, '100000.00', '100000.00', TRUE, '2025-05-26T05:27:33.850234'),
    (8, 8, TRUE, '125000.00', '100000.00', FALSE, '2025-05-26T05:27:33.850234'),
    (9, 9, TRUE, '100000.00', '100000.00', TRUE, '2025-05-26T05:27:33.850234'),
    (10, 10, TRUE, '100000.00', '100000.00', TRUE, '2025-05-26T05:27:33.850234');

-- Table: seller_primary_contact (10 records)
INSERT INTO seller_primary_contact (seller_id, salutation, first_name, last_name, designation, mobile, email) VALUES
    (1, 'Mr.', 'Suresh', 'Nair', 'General Manager', '+91-9447123456', 'suresh.nair@backwaterbliss.com'),
    (2, 'Ms.', 'Lakshmi', 'Pillai', 'Resort Manager', '+91-9447123457', 'lakshmi.pillai@spicegardenretreat.com'),
    (3, 'Mr.', 'Ravi', 'Kumar', 'Owner', '+91-9447123458', 'ravi.kumar@coconutgrovehomestay.in'),
    (4, 'Mrs.', 'Meera', 'Menon', 'Operations Head', '+91-9447123459', 'meera.menon@mistymountainresort.com'),
    (5, 'Dr.', 'Ayush', 'Sharma', 'Director', '+91-9447123460', 'ayush.sharma@ayurvedawellness.in'),
    (6, 'Mr.', 'Krishnan', 'Nambiar', 'Captain', '+91-9447123461', 'krishnan.nambiar@heritagehouseboat.com'),
    (7, 'Ms.', 'Priya', 'Varma', 'Resort Director', '+91-9447123462', 'priya.varma@cliffedgeresort.in'),
    (8, 'Mr.', 'Arun', 'Thampi', 'Estate Manager', '+91-9447123463', 'arun.thampi@teaestatevilla.com'),
    (9, 'Mrs.', 'Geetha', 'Raj', 'Wildlife Guide', '+91-9447123464', 'geetha.raj@wayanadwildresort.com'),
    (10, 'Mr.', 'Vinod', 'Das', 'Hotel Manager', '+91-9447123465', 'vinod.das@beachparadisehotel.com');

-- Table: seller_reference (10 records)
INSERT INTO seller_reference (seller_id, ref1_name, ref1_addr, ref2_name, ref2_addr) VALUES
    (1, 'KTDC Kumarakom', 'Kumarakom, Kerala', 'Tourism Department', 'Kottayam, Kerala'),
    (2, 'Forest Department', 'Thekkady, Kerala', 'Spice Board India', 'Kochi, Kerala'),
    (3, 'Alleppey Tourism', 'Alleppey, Kerala', 'Homestay Association', 'Kochi, Kerala'),
    (4, 'Munnar Tourism', 'Munnar, Kerala', 'Tea Board India', 'Kochi, Kerala'),
    (5, 'Ayurveda Board', 'Thiruvananthapuram, Kerala', 'Medical Tourism', 'Kovalam, Kerala'),
    (6, 'Boat Owners Association', 'Alleppey, Kerala', 'Backwater Tourism', 'Kumarakom, Kerala'),
    (7, 'Varkala Tourism', 'Varkala, Kerala', 'Beach Resort Association', 'Kovalam, Kerala'),
    (8, 'Tea Growers Association', 'Munnar, Kerala', 'Hill Station Tourism', 'Munnar, Kerala'),
    (9, 'Forest Department', 'Wayanad, Kerala', 'Wildlife Board', 'Wayanad, Kerala'),
    (10, 'Beach Tourism Board', 'Kovalam, Kerala', 'Hotel Association', 'Thiruvananthapuram, Kerala');

-- Table: seller_references (10 records)
INSERT INTO seller_references (id, seller_profile_id, ref1_name, ref1_address, ref2_name, ref2_address, created_at) VALUES
    (1, 1, 'KTDC Kumarakom', 'Kumarakom, Kerala', 'Tourism Department', 'Kottayam, Kerala', '2025-05-26T05:27:33.850702'),
    (2, 2, 'Forest Department', 'Thekkady, Kerala', 'Spice Board India', 'Kochi, Kerala', '2025-05-26T05:27:33.850702'),
    (3, 3, 'Alleppey Tourism', 'Alleppey, Kerala', 'Homestay Association', 'Kochi, Kerala', '2025-05-26T05:27:33.850702'),
    (4, 4, 'Munnar Tourism', 'Munnar, Kerala', 'Tea Board India', 'Kochi, Kerala', '2025-05-26T05:27:33.850702'),
    (5, 5, 'Ayurveda Board', 'Thiruvananthapuram, Kerala', 'Medical Tourism', 'Kovalam, Kerala', '2025-05-26T05:27:33.850702'),
    (6, 6, 'Boat Owners Association', 'Alleppey, Kerala', 'Backwater Tourism', 'Kumarakom, Kerala', '2025-05-26T05:27:33.850702'),
    (7, 7, 'Varkala Tourism', 'Varkala, Kerala', 'Beach Resort Association', 'Kovalam, Kerala', '2025-05-26T05:27:33.850702'),
    (8, 8, 'Tea Growers Association', 'Munnar, Kerala', 'Hill Station Tourism', 'Munnar, Kerala', '2025-05-26T05:27:33.850702'),
    (9, 9, 'Forest Department', 'Wayanad, Kerala', 'Wildlife Board', 'Wayanad, Kerala', '2025-05-26T05:27:33.850702'),
    (10, 10, 'Beach Tourism Board', 'Kovalam, Kerala', 'Hotel Association', 'Thiruvananthapuram, Kerala', '2025-05-26T05:27:33.850702');

-- Table: stall_database (15 records)
INSERT INTO stall_database (stall_number_id, stall_number, stall_type_id) VALUES
    (1, 'A1', 1),
    (2, 'A2', 2),
    (3, 'A3', 2),
    (4, 'A4', 1),
    (5, 'A5', 3),
    (6, 'B1', 4),
    (7, 'B2', 2),
    (8, 'B3', 2),
    (9, 'B4', 3),
    (10, 'B5', 5),
    (11, 'C1', 6),
    (12, 'C2', 2),
    (13, 'C3', 3),
    (14, 'C4', 2),
    (15, 'C5', 1);

-- Table: stall_inventory (15 records)
INSERT INTO stall_inventory (id, stall_number, stall_type_id, is_allocated, created_at) VALUES
    (1, 'A1', 1, FALSE, '2025-05-26T05:27:33.811811'),
    (2, 'A2', 2, FALSE, '2025-05-26T05:27:33.811811'),
    (3, 'A3', 2, FALSE, '2025-05-26T05:27:33.811811'),
    (4, 'A4', 1, FALSE, '2025-05-26T05:27:33.811811'),
    (5, 'A5', 3, FALSE, '2025-05-26T05:27:33.811811'),
    (6, 'B1', 4, FALSE, '2025-05-26T05:27:33.811811'),
    (7, 'B2', 2, FALSE, '2025-05-26T05:27:33.811811'),
    (8, 'B3', 2, FALSE, '2025-05-26T05:27:33.811811'),
    (9, 'B4', 3, FALSE, '2025-05-26T05:27:33.811811'),
    (10, 'B5', 5, FALSE, '2025-05-26T05:27:33.811811'),
    (11, 'C1', 6, FALSE, '2025-05-26T05:27:33.811811'),
    (12, 'C2', 2, FALSE, '2025-05-26T05:27:33.811811'),
    (13, 'C3', 3, FALSE, '2025-05-26T05:27:33.811811'),
    (14, 'C4', 2, FALSE, '2025-05-26T05:27:33.811811'),
    (15, 'C5', 1, FALSE, '2025-05-26T05:27:33.811811');

-- Table stalls: No data

-- Table: seller_stall (10 records)
INSERT INTO seller_stall (seller_stall_id, seller_id, stall_type_id, allocated_stall_number, fascia_name, microsite_url) VALUES
    (1, 1, 1, 'A1', 'Backwater Bliss Resort', 'www.splash2025.com/backwaterbliss'),
    (2, 2, 2, 'A2', 'Spice Garden Retreat', 'www.splash2025.com/spicegarden'),
    (3, 3, 3, 'A3', 'Coconut Grove Homestay', 'www.splash2025.com/coconutgrove'),
    (4, 4, 1, 'A4', 'Misty Mountain Resort', 'www.splash2025.com/mistymountain'),
    (5, 5, 6, 'C1', 'Ayurveda Wellness Center', 'www.splash2025.com/ayurvedawellness'),
    (6, 6, 3, 'A5', 'Heritage Houseboat', 'www.splash2025.com/heritagehouseboat'),
    (7, 7, 2, 'B2', 'Cliff Edge Resort', 'www.splash2025.com/cliffedge'),
    (8, 8, 6, 'C5', 'Tea Estate Villa', 'www.splash2025.com/teaestate'),
    (9, 9, 2, 'B3', 'Wayanad Wild Resort', 'www.splash2025.com/wayanadwild'),
    (10, 10, 2, 'C2', 'Beach Paradise Hotel', 'www.splash2025.com/beachparadise');

-- Table: seller_attendees (20 records)
INSERT INTO seller_attendees (id, seller_profile_id, attendee_number, name, designation, email, mobile, is_primary_contact, created_at) VALUES
    (1, 1, 1, 'Suresh Nair', 'General Manager', 'suresh.nair@backwaterbliss.com', '+91-9447123456', TRUE, '2025-05-26T05:27:33.849085'),
    (2, 1, 2, 'Radha Krishnan', 'Sales Manager', 'radha.krishnan@backwaterbliss.com', '+91-9447123466', FALSE, '2025-05-26T05:27:33.849085'),
    (3, 2, 1, 'Lakshmi Pillai', 'Resort Manager', 'lakshmi.pillai@spicegardenretreat.com', '+91-9447123457', TRUE, '2025-05-26T05:27:33.849085'),
    (4, 2, 2, 'Mohan Kumar', 'Marketing Head', 'mohan.kumar@spicegardenretreat.com', '+91-9447123467', FALSE, '2025-05-26T05:27:33.849085'),
    (5, 3, 1, 'Ravi Kumar', 'Owner', 'ravi.kumar@coconutgrovehomestay.in', '+91-9447123458', TRUE, '2025-05-26T05:27:33.849085'),
    (6, 3, 2, 'Sita Devi', 'Co-owner', 'sita.devi@coconutgrovehomestay.in', '+91-9447123468', FALSE, '2025-05-26T05:27:33.849085'),
    (7, 4, 1, 'Meera Menon', 'Operations Head', 'meera.menon@mistymountainresort.com', '+91-9447123459', TRUE, '2025-05-26T05:27:33.849085'),
    (8, 4, 2, 'Rajesh Nair', 'Guest Relations', 'rajesh.nair@mistymountainresort.com', '+91-9447123469', FALSE, '2025-05-26T05:27:33.849085'),
    (9, 5, 1, 'Dr. Ayush Sharma', 'Director', 'ayush.sharma@ayurvedawellness.in', '+91-9447123460', TRUE, '2025-05-26T05:27:33.849085'),
    (10, 5, 2, 'Priya Menon', 'Wellness Coordinator', 'priya.menon@ayurvedawellness.in', '+91-9447123470', FALSE, '2025-05-26T05:27:33.849085'),
    (11, 6, 1, 'Krishnan Nambiar', 'Captain', 'krishnan.nambiar@heritagehouseboat.com', '+91-9447123461', TRUE, '2025-05-26T05:27:33.849085'),
    (12, 6, 2, 'Unni Krishnan', 'Boat Manager', 'unni.krishnan@heritagehouseboat.com', '+91-9447123471', FALSE, '2025-05-26T05:27:33.849085'),
    (13, 7, 1, 'Priya Varma', 'Resort Director', 'priya.varma@cliffedgeresort.in', '+91-9447123462', TRUE, '2025-05-26T05:27:33.849085'),
    (14, 7, 2, 'Anil Kumar', 'Operations Manager', 'anil.kumar@cliffedgeresort.in', '+91-9447123472', FALSE, '2025-05-26T05:27:33.849085'),
    (15, 8, 1, 'Arun Thampi', 'Estate Manager', 'arun.thampi@teaestatevilla.com', '+91-9447123463', TRUE, '2025-05-26T05:27:33.849085'),
    (16, 8, 2, 'Deepa Nair', 'Guest Services', 'deepa.nair@teaestatevilla.com', '+91-9447123473', FALSE, '2025-05-26T05:27:33.849085'),
    (17, 9, 1, 'Geetha Raj', 'Wildlife Guide', 'geetha.raj@wayanadwildresort.com', '+91-9447123464', TRUE, '2025-05-26T05:27:33.849085'),
    (18, 9, 2, 'Babu Antony', 'Nature Guide', 'babu.antony@wayanadwildresort.com', '+91-9447123474', FALSE, '2025-05-26T05:27:33.849085'),
    (19, 10, 1, 'Vinod Das', 'Hotel Manager', 'vinod.das@beachparadisehotel.com', '+91-9447123465', TRUE, '2025-05-26T05:27:33.849085'),
    (20, 10, 2, 'Suma Nair', 'Front Office Manager', 'suma.nair@beachparadisehotel.com', '+91-9447123475', FALSE, '2025-05-26T05:27:33.849085');

-- Table: buyer_interest (20 records)
INSERT INTO buyer_interest (interest_number, buyer_id, interest_id) VALUES
    (1, 1, 2),
    (2, 1, 1),
    (3, 2, 5),
    (4, 2, 9),
    (5, 3, 3),
    (6, 3, 8),
    (7, 4, 6),
    (8, 4, 3),
    (9, 5, 4),
    (10, 5, 2),
    (11, 6, 11),
    (12, 6, 3),
    (13, 7, 6),
    (14, 7, 4),
    (15, 8, 5),
    (16, 8, 10),
    (17, 9, 7),
    (18, 9, 1),
    (19, 10, 12),
    (20, 10, 11);

-- Table: buyer_profile_interests (20 records)
INSERT INTO buyer_profile_interests (id, buyer_profile_id, interest_id, created_at) VALUES
    (1, 1, 2, '2025-05-26T05:27:33.846516'),
    (2, 1, 1, '2025-05-26T05:27:33.846516'),
    (3, 2, 5, '2025-05-26T05:27:33.846516'),
    (4, 2, 9, '2025-05-26T05:27:33.846516'),
    (5, 3, 3, '2025-05-26T05:27:33.846516'),
    (6, 3, 8, '2025-05-26T05:27:33.846516'),
    (7, 4, 6, '2025-05-26T05:27:33.846516'),
    (8, 4, 3, '2025-05-26T05:27:33.846516'),
    (9, 5, 4, '2025-05-26T05:27:33.846516'),
    (10, 5, 2, '2025-05-26T05:27:33.846516'),
    (11, 6, 11, '2025-05-26T05:27:33.846516'),
    (12, 6, 3, '2025-05-26T05:27:33.846516'),
    (13, 7, 6, '2025-05-26T05:27:33.846516'),
    (14, 7, 4, '2025-05-26T05:27:33.846516'),
    (15, 8, 5, '2025-05-26T05:27:33.846516'),
    (16, 8, 10, '2025-05-26T05:27:33.846516'),
    (17, 9, 7, '2025-05-26T05:27:33.846516'),
    (18, 9, 1, '2025-05-26T05:27:33.846516'),
    (19, 10, 12, '2025-05-26T05:27:33.846516'),
    (20, 10, 11, '2025-05-26T05:27:33.846516');

-- Table: seller_target_market (20 records)
INSERT INTO seller_target_market (target_market_number, seller_id, target_market_id) VALUES
    (1, 1, 2),
    (2, 1, 6),
    (3, 2, 3),
    (4, 2, 8),
    (5, 3, 11),
    (6, 3, 3),
    (7, 4, 7),
    (8, 4, 12),
    (9, 5, 4),
    (10, 5, 9),
    (11, 6, 5),
    (12, 6, 6),
    (13, 7, 6),
    (14, 7, 12),
    (15, 8, 7),
    (16, 8, 11),
    (17, 9, 8),
    (18, 9, 1),
    (19, 10, 6),
    (20, 10, 11);

-- Table: seller_target_markets (20 records)
INSERT INTO seller_target_markets (id, seller_profile_id, interest_id, created_at) VALUES
    (1, 1, 2, '2025-05-26T05:27:33.851266'),
    (2, 1, 6, '2025-05-26T05:27:33.851266'),
    (3, 2, 3, '2025-05-26T05:27:33.851266'),
    (4, 2, 8, '2025-05-26T05:27:33.851266'),
    (5, 3, 11, '2025-05-26T05:27:33.851266'),
    (6, 3, 3, '2025-05-26T05:27:33.851266'),
    (7, 4, 7, '2025-05-26T05:27:33.851266'),
    (8, 4, 12, '2025-05-26T05:27:33.851266'),
    (9, 5, 4, '2025-05-26T05:27:33.851266'),
    (10, 5, 9, '2025-05-26T05:27:33.851266'),
    (11, 6, 5, '2025-05-26T05:27:33.851266'),
    (12, 6, 6, '2025-05-26T05:27:33.851266'),
    (13, 7, 6, '2025-05-26T05:27:33.851266'),
    (14, 7, 12, '2025-05-26T05:27:33.851266'),
    (15, 8, 7, '2025-05-26T05:27:33.851266'),
    (16, 8, 11, '2025-05-26T05:27:33.851266'),
    (17, 9, 8, '2025-05-26T05:27:33.851266'),
    (18, 9, 1, '2025-05-26T05:27:33.851266'),
    (19, 10, 6, '2025-05-26T05:27:33.851266'),
    (20, 10, 11, '2025-05-26T05:27:33.851266');

-- Table travel_plans: No data

-- Table transportation: No data

-- Table accommodations: No data

-- Table ground_transportation: No data

-- Table time_slots: No data

-- Table meetings: No data

-- Table meeting: No data

-- Table listings: No data

-- Table listing_dates: No data

-- Table invited_buyers: No data

-- Table pending_buyers: No data

-- Table: migration_mapping_buyers (10 records)
INSERT INTO migration_mapping_buyers (id, customer_buyer_id, splash25_user_id, splash25_buyer_profile_id, migration_status, created_at) VALUES
    (1, 1, 1, 1, 'completed', '2025-05-26T05:27:33.847255'),
    (2, 2, 2, 2, 'completed', '2025-05-26T05:27:33.847255'),
    (3, 3, 3, 3, 'completed', '2025-05-26T05:27:33.847255'),
    (4, 4, 4, 4, 'completed', '2025-05-26T05:27:33.847255'),
    (5, 5, 5, 5, 'completed', '2025-05-26T05:27:33.847255'),
    (6, 6, 6, 6, 'completed', '2025-05-26T05:27:33.847255'),
    (7, 7, 7, 7, 'completed', '2025-05-26T05:27:33.847255'),
    (8, 8, 8, 8, 'completed', '2025-05-26T05:27:33.847255'),
    (9, 9, 9, 9, 'completed', '2025-05-26T05:27:33.847255'),
    (10, 10, 10, 10, 'completed', '2025-05-26T05:27:33.847255');

-- Table migration_mapping_sellers: No data

-- Reset sequences
SELECT setval('users_id_seq', 34, true);
SELECT setval('buyer_profiles_id_seq', 34, true);
SELECT setval('seller_profiles_id_seq', 10, true);
SELECT setval('property_types_id_seq', 5, true);
SELECT setval('buyer_categories_id_seq', 6, true);
SELECT setval('stall_types_id_seq', 8, true);
SELECT setval('stall_inventory_id_seq', 15, true);
SELECT setval('buyer_financial_info_id_seq', 10, true);
SELECT setval('interests_id_seq', 13, true);
SELECT setval('buyer_business_info_id_seq', 10, true);
SELECT setval('buyer_references_id_seq', 10, true);
SELECT setval('buyer_profile_interests_id_seq', 20, true);
SELECT setval('seller_attendees_id_seq', 20, true);
SELECT setval('seller_business_info_id_seq', 10, true);
SELECT setval('seller_financial_info_id_seq', 10, true);
SELECT setval('seller_references_id_seq', 10, true);
SELECT setval('seller_target_markets_id_seq', 20, true);
SELECT setval('migration_mapping_buyers_id_seq', 10, true);
SELECT setval('migration_log_id_seq', 5, true);

-- Re-enable foreign key checks
SET session_replication_role = DEFAULT;

-- Data export completed