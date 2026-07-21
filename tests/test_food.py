import pytest
from backend.app import app

# Setup the Test Client Fixture
@pytest.fixture
def client():
    """Configures a temporary Flask test client for our tests."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# 1. Test getting the list of foods
def test_get_all_foods(client):
    """Test that the GET /foods endpoint returns a 200 OK and a list."""
    response = client.get('/foods')
    assert response.status_code == 200
    assert type(response.json) == list

# 2. Test the full CRUD lifecycle for a single food item
def test_food_lifecycle(client):
    """Tests the Create, Read, Update, and Delete flow for a food item."""
    
    # --- A. Test Create (POST) ---
    new_food_payload = {
        "food_name": "Test Apple",
        "serving_size": "1 medium",
        "calories": 95,
        "protein": 0.5,
        "carbohydrates": 25.0,
        "fat": 0.3,
        "fiber": 4.4,
        "sugar": 19.0
    }
    
    post_response = client.post('/foods', json=new_food_payload)
    assert post_response.status_code == 201
    assert "food_id" in post_response.json
    
    # Save the generated ID for the next steps
    food_id = post_response.json["food_id"]

    # --- B. Test Read (GET single food) ---
    get_response = client.get(f'/foods/{food_id}')
    assert get_response.status_code == 200
    assert get_response.json["food_name"] == "Test Apple"
    assert get_response.json["calories"] == 95

    # --- C. Test Update (PUT) ---
    update_payload = {
        "food_name": "Test Apple (Updated)",
        "serving_size": "1 large",
        "calories": 115,
        "protein": 0.6,
        "carbohydrates": 30.0,
        "fat": 0.4,
        "fiber": 5.0,
        "sugar": 22.0
    }
    
    put_response = client.put(f'/foods/{food_id}', json=update_payload)
    assert put_response.status_code == 200
    
    # Verify the update actually saved to the database
    get_updated = client.get(f'/foods/{food_id}')
    assert get_updated.json["food_name"] == "Test Apple (Updated)"
    assert get_updated.json["calories"] == 115

    # --- D. Test Delete (DELETE) ---
    delete_response = client.delete(f'/foods/{food_id}')
    assert delete_response.status_code == 200
    assert delete_response.json["message"] == "Food deleted successfully"

    # --- E. Verify Deletion ---
    verify_response = client.get(f'/foods/{food_id}')
    assert verify_response.status_code == 404