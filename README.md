# Splash25 Backend

This is the backend for the Splash25 application, built with Flask.

## Setup and Installation

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set up the environment variables in `.env` file (already configured)

## Running the Application

To run the application, use the following command:

```
flask run
```

The application will be available at http://127.0.0.1:5000

## User Accounts

The following user accounts are available for testing:

### Admin User
- Username: admin_new
- Password: admin123
- Role: Admin

### Seller User
- Username: seller_new
- Password: seller123
- Role: Seller
- Business: New Adventure Tours

### Buyer User
- Username: buyer_new
- Password: buyer123
- Role: Buyer

## API Endpoints

### Authentication

- **Register**: `POST /api/auth/register`
  ```json
  {
    "username": "new_user",
    "email": "user@example.com",
    "password": "password123",
    "role": "buyer"
  }
  ```

- **Login**: `POST /api/auth/login`
  ```json
  {
    "username": "username",
    "password": "password"
  }
  ```

- **Refresh Token**: `POST /api/auth/refresh` (requires refresh token)
- **Get Current User**: `GET /api/auth/me` (requires access token)
- **Logout**: `POST /api/auth/logout` (requires access token)

### Other Endpoints

The application includes various other endpoints for buyers, sellers, and admins. These can be found in the respective route files:

- `app/routes/buyer.py`
- `app/routes/seller.py`
- `app/routes/admin.py`
- `app/routes/main.py`

## Database

The application uses SQLite by default. The database file is located at `instance/splash25.db`.

## Adding New Users

If you need to add new users, you can use the provided scripts:

- For admin users: `python3 add_admin.py`
- For seller users: `python3 add_seller.py`
- For buyer users: `python3 add_buyer.py`

## Initializing the Database

If you need to reset the database and initialize it with sample data, you can use:

```
python3 init_db.py
```

Note: This will only initialize the database if it's empty.
