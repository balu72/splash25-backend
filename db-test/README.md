# Database Testing & Data Ingestion Scripts

This directory contains all scripts for creating test data, user profiles, and testing database functionality for the Splash25 application.

## 📁 Directory Structure

```
db-test/
├── users/          # User creation scripts
├── profiles/       # Profile creation scripts  
├── data/          # Data ingestion scripts
├── tests/         # Testing scripts
└── README.md      # This documentation
```

## 🔐 Test Credentials

### Admin Account
- **Username:** `admin_new`
- **Password:** `admin123`
- **Email:** `admin_new@splash25.com`

### Buyer Account (with Travel Plan Data)
- **Username:** `buyer_new`
- **Password:** `buyer123`
- **Email:** `buyer_new@example.com`

### Seller Account
- **Username:** `seller_new`
- **Password:** `seller123`
- **Email:** `seller_new@example.com`

### Additional Test Buyers
- **Username:** `buyer_test1` | **Password:** `test123` | **Email:** `buyer1@test.com`
- **Username:** `buyer_test2` | **Password:** `test123` | **Email:** `buyer2@test.com`

## 📂 Users Directory (`users/`)

### `add_admin.py`
Creates an admin user with full system privileges.
```bash
cd splash25-backend && python db-test/users/add_admin.py
```

### `add_buyer.py`
Creates a buyer user for testing buyer functionality.
```bash
cd splash25-backend && python db-test/users/add_buyer.py
```

### `add_seller.py`
Creates a seller user with business details.
```bash
cd splash25-backend && python db-test/users/add_seller.py
```

### `add_users.py`
Creates multiple users at once (admin, buyer, seller).
```bash
cd splash25-backend && python db-test/users/add_users.py
```

## 👤 Profiles Directory (`profiles/`)

### `create_buyer_profile_table.py`
Creates the buyer profile table structure in the database.
```bash
cd splash25-backend && python db-test/profiles/create_buyer_profile_table.py
```

### `create_buyer_profiles.py`
Creates detailed buyer profile data for testing.
```bash
cd splash25-backend && python db-test/profiles/create_buyer_profiles.py
```

### `create_seller_profile.py`
Creates seller profile data with business information.
```bash
cd splash25-backend && python db-test/profiles/create_seller_profile.py
```

## 📊 Data Directory (`data/`)

### `create_stall_data.py`
Creates stall/booth data for sellers at the event.
```bash
cd splash25-backend && python db-test/data/create_stall_data.py
```

### `create_travel_plan_data.py`
Creates comprehensive travel plan data for buyers.
```bash
cd splash25-backend && python db-test/data/create_travel_plan_data.py
```

## 🧪 Tests Directory (`tests/`)

### `test_travel_plans.py`
Tests the travel plans API endpoints.
```bash
cd splash25-backend && python db-test/tests/test_travel_plans.py
```

## 🚀 Quick Setup Guide

### 1. Create All Users
```bash
cd splash25-backend && python db-test/users/add_users.py
```

### 2. Create Profiles
```bash
cd splash25-backend && python db-test/profiles/create_buyer_profiles.py
cd splash25-backend && python db-test/profiles/create_seller_profile.py
```

### 3. Add Data
```bash
cd splash25-backend && python db-test/data/create_stall_data.py
cd splash25-backend && python db-test/data/create_travel_plan_data.py
```

### 4. Test Functionality
```bash
cd splash25-backend && python db-test/tests/test_travel_plans.py
```

## 📝 Usage Notes

- **Prerequisites:** Ensure the Flask application and database are running
- **Order Matters:** Create users before profiles, profiles before data
- **Database:** All scripts work with the PostgreSQL database
- **Environment:** Scripts should be run from the `splash25-backend` directory
- **Dependencies:** All scripts use the same app context and models

## 🔧 Troubleshooting

### Common Issues:
1. **Import Errors:** Ensure you're running from the `splash25-backend` directory
2. **Database Connection:** Check that PostgreSQL is running and accessible
3. **Duplicate Data:** Scripts check for existing data before creating new records
4. **Permission Errors:** Ensure proper database permissions

### Database Reset:
If you need to reset test data, you can:
1. Drop and recreate the database
2. Run the migration scripts
3. Re-run the data creation scripts in order

## 🎯 Testing Workflow

1. **Setup:** Run user and profile creation scripts
2. **Data:** Add stall and travel plan data
3. **Test:** Use the web interface with test credentials
4. **Verify:** Run API tests to ensure functionality
5. **Debug:** Check logs and database state if issues arise

## 📞 Support

For issues with these scripts:
1. Check the console output for error messages
2. Verify database connectivity
3. Ensure all dependencies are installed
4. Check that the Flask app context is available
