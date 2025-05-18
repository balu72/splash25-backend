import requests
import json
import jwt

def test_travel_plans():
    """Test the travel plans endpoint."""
    # Login to get token
    login_url = "http://127.0.0.1:5000/api/auth/login"
    login_data = {
        "username": "user1",
        "password": "password"
    }
    
    response = requests.post(login_url, json=login_data)
    if response.status_code != 200:
        print(f"Login failed: {response.status_code}")
        print(response.text)
        return
    
    # Extract token
    token_data = response.json()
    access_token = token_data.get("access_token")
    
    if not access_token:
        print("No access token in response")
        print(response.text)
        return
    
    # Decode token to see what's inside
    try:
        # Note: This will only work if the token is not encrypted
        decoded_token = jwt.decode(access_token, options={"verify_signature": False})
        print("Decoded token:")
        print(json.dumps(decoded_token, indent=2))
    except Exception as e:
        print(f"Error decoding token: {e}")
    
    # Get travel plans
    travel_plans_url = "http://127.0.0.1:5000/api/buyer/travel-plans"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    response = requests.get(travel_plans_url, headers=headers)
    print(f"Travel plans response: {response.status_code}")
    print(json.dumps(response.json(), indent=2))

if __name__ == "__main__":
    test_travel_plans()
