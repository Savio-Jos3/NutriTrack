import pytest
from app import app

# 1. Setup the Test Client Fixture
@pytest.fixture
def client():
    """Configures a temporary Flask test client for our tests."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# 2. The Tests
def test_get_all_users(client):
    """Test that the GET /users endpoint returns a 200 OK."""
    response = client.get('/users')
    assert response.status_code == 200
    assert type(response.json) == list

def test_user_lifecycle(client):
    """Tests the Create, Read, and Delete flow for a user."""
    
    # --- A. Test Create (POST) ---
    new_user_payload = {
        "name": "Test User",
        "email": "test_user_999@example.com",
        "age": 30,
        "gender": "Male",
        "height": 180.0,
        "weight": 75.0,
        "daily_calorie_goal": 2000
    }
    
    post_response = client.post('/users', json=new_user_payload)
    assert post_response.status_code == 201
    assert "user_id" in post_response.json
    
    # Save the generated ID so we can test the other endpoints
    user_id = post_response.json["user_id"]

    # --- B. Test Read (GET single user) ---
    get_response = client.get(f'/users/{user_id}')
    assert get_response.status_code == 200
    assert get_response.json["name"] == "Test User"
    assert get_response.json["email"] == "test_user_999@example.com"

    # --- C. Test Delete (DELETE) ---
    delete_response = client.delete(f'/users/{user_id}')
    assert delete_response.status_code == 200
    assert delete_response.json["message"] == "User deleted successfully"

    # --- D. Verify Deletion ---
    verify_response = client.get(f'/users/{user_id}')
    assert verify_response.status_code == 404