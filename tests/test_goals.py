import pytest
from backend.app import app

@pytest.fixture
def client():
    """Configures a temporary Flask test client."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_goal_lifecycle(client):
    """Tests the full Create, Read, Update, and Delete flow for Nutrition Goals."""
    
    # --- A. Setup: Create a temporary User ---
    user_payload = {
        "name": "Goal Tester",
        "email": "goal_tester@example.com",
        "age": 28, "gender": "Female", "height": 165.0, "weight": 60.0, "daily_calorie_goal": 2000
    }
    user_res = client.post('/users', json=user_payload)
    assert user_res.status_code == 201
    user_id = user_res.json["user_id"]

    # --- B. Test Create Goal (POST) ---
    goal_payload = {
        "user_id": user_id,
        "daily_calories": 2100,
        "protein_goal": 140.0,
        "carbohydrate_goal": 220.0,
        "fat_goal": 65.0,
        "fiber_goal": 25.0
    }
    post_res = client.post('/goals', json=goal_payload)
    assert post_res.status_code == 201
    assert "goal_id" in post_res.json

    # --- C. Test Read Goal (GET) ---
    get_res = client.get(f'/goals/user/{user_id}')
    assert get_res.status_code == 200
    assert get_res.json["daily_calories"] == 2100
    assert get_res.json["protein_goal"] == 140.0

    # --- D. Test Update Goal (PUT) ---
    update_payload = {
        "daily_calories": 2300,  # Increasing calories
        "protein_goal": 160.0,   # Increasing protein
        "carbohydrate_goal": 240.0,
        "fat_goal": 70.0,
        "fiber_goal": 30.0
    }
    put_res = client.put(f'/goals/user/{user_id}', json=update_payload)
    assert put_res.status_code == 200

    # Verify the update saved
    get_updated = client.get(f'/goals/user/{user_id}')
    assert get_updated.json["daily_calories"] == 2300
    assert get_updated.json["protein_goal"] == 160.0

    # --- E. Test Delete Goal (DELETE) ---
    delete_res = client.delete(f'/goals/user/{user_id}')
    assert delete_res.status_code == 200

    # Verify Deletion
    get_deleted = client.get(f'/goals/user/{user_id}')
    assert get_deleted.status_code == 404

    # --- F. Cleanup ---
    client.delete(f'/users/{user_id}')