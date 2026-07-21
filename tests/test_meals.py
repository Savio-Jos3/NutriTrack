import pytest
from backend.app import app

@pytest.fixture
def client():
    """Configures a temporary Flask test client."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_meal_lifecycle(client):
    """Tests the full flow: create dependencies, create meal, add items, and verify."""
    
    # --- A. Setup: Create a temporary User ---
    user_payload = {
        "name": "Meal Tester",
        "email": "meal_tester@example.com",
        "age": 25, "gender": "Male", "height": 175.0, "weight": 70.0, "daily_calorie_goal": 2500
    }
    user_res = client.post('/users', json=user_payload)
    user_id = user_res.json["user_id"]

    # --- B. Setup: Create a temporary Food ---
    food_payload = {
        "food_name": "Test Banana",
        "serving_size": "1 medium",
        "calories": 105, # Base calories for 1 banana
        "protein": 1.3, "carbohydrates": 27.0, "fat": 0.4, "fiber": 3.1, "sugar": 14.4
    }
    food_res = client.post('/foods', json=food_payload)
    food_id = food_res.json["food_id"]

    # --- C. Test Create Meal (POST) ---
    meal_payload = {
        "user_id": user_id,
        "meal_type": "Snack",
        "meal_date": "2026-07-21",
        "meal_time": "15:00:00"
    }
    meal_res = client.post('/meals', json=meal_payload)
    assert meal_res.status_code == 201
    assert "meal_id" in meal_res.json
    meal_id = meal_res.json["meal_id"]

    # --- D. Test Add Food to Meal (POST) ---
    item_payload = {
        "food_id": food_id,
        "quantity": 2.0  # We are eating 2 bananas
    }
    item_res = client.post(f'/meals/{meal_id}/items', json=item_payload)
    assert item_res.status_code == 201
    
    # Verify the backend correctly multiplied 105 base calories by 2.0 quantity
    assert item_res.json["calories_consumed"] == 210

    # --- E. Test Get Meal Details (GET) ---
    get_res = client.get(f'/meals/{meal_id}')
    assert get_res.status_code == 200
    meal_data = get_res.json
    
    assert meal_data["total_meal_calories"] == 210
    assert len(meal_data["items"]) == 1
    assert meal_data["items"][0]["food_name"] == "Test Banana"
    assert meal_data["items"][0]["quantity"] == 2.0

    # --- F. Cleanup ---
    # Deleting the user and food will automatically cascade and delete the meal and meal items
    client.delete(f'/users/{user_id}')
    client.delete(f'/foods/{food_id}')