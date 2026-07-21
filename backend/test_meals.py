"""
Unit tests for the Meals endpoints.
"""

# pylint: disable=redefined-outer-name

import logging
import uuid
import pytest
from app import app

logger = logging.getLogger(__name__)


@pytest.fixture
def client():
    """Configures a temporary Flask test client."""
    app.config["TESTING"] = True
    with app.test_client() as test_client:
        yield test_client


def test_meal_lifecycle(client):
    """Tests the creation and retrieval of meals and meal items."""
    logger.info("=== STARTING MEALS TEST ===")

    # --- A. Setup: Create a temporary User ---
    random_suffix = uuid.uuid4().hex[:8]
    unique_email = f"meal_tester_{random_suffix}@example.com"

    logger.info("Setting up temporary user...")
    user_res = client.post(
        "/users",
        json={
            "name": "Meal Tester",
            "email": unique_email,
            "age": 25,
            "gender": "Male",
            "height": 175.0,
            "weight": 70.0,
            "daily_calorie_goal": 2500,
        },
    )
    assert user_res.status_code == 201, f"User creation failed: {user_res.json}"
    user_id = user_res.json["user_id"]

    # --- B. Setup: Create a temporary Food ---
    logger.info("Setting up temporary food...")
    food_res = client.post(
        "/foods",
        json={
            "food_name": "Test Banana",
            "serving_size": "1 medium",
            "calories": 105,
            "protein": 1.3,
            "carbohydrates": 27.0,
            "fat": 0.4,
            "fiber": 3.1,
            "sugar": 14.4,
        },
    )
    food_id = food_res.json["food_id"]

    # --- C. Test Create Meal (POST) ---
    logger.info("Testing POST /meals...")
    meal_res = client.post(
        "/meals",
        json={
            "user_id": user_id,
            "meal_type": "Snack",
            "meal_date": "2026-07-21",
            "meal_time": "15:00:00",
        },
    )
    assert meal_res.status_code == 201
    meal_id = meal_res.json["meal_id"]

    # --- D. Test Add Food to Meal (POST) ---
    logger.info("Testing POST /meals/%s/items...", meal_id)
    item_res = client.post(
        f"/meals/{meal_id}/items", json={"food_id": food_id, "quantity": 2.0}
    )
    assert item_res.status_code == 201
    assert item_res.json["calories_consumed"] == 210

    # --- E. Test Get Meal Details (GET) ---
    logger.info("Testing GET /meals/%s...", meal_id)
    get_res = client.get(f"/meals/{meal_id}")
    assert get_res.status_code == 200
    assert get_res.json["total_calories"] == 210
    assert get_res.json["total_protein"] == 2.6

    # --- F. Cleanup ---
    logger.info("Cleaning up database...")
    client.delete(f"/users/{user_id}")
    client.delete(f"/foods/{food_id}")

    logger.info("=== MEALS TEST COMPLETE ===")
