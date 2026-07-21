"""
Unit tests for the Pandas Analytics endpoints.
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


def test_analytics_aggregations(client):
    """Tests the Pandas analytics aggregations with controlled data."""
    logger.info("=== STARTING ANALYTICS TEST ===")

    # --- A. Setup: Create User ---
    random_suffix = uuid.uuid4().hex[:8]
    unique_email = f"analytics_tester_{random_suffix}@example.com"

    logger.info("Setting up temporary user...")
    user_res = client.post(
        "/users",
        json={
            "name": "Analytics Tester",
            "email": unique_email,
            "age": 30,
            "gender": "Female",
            "height": 160.0,
            "weight": 60.0,
            "daily_calorie_goal": 2000,
        },
    )
    user_id = user_res.json["user_id"]
    logger.info("Created User ID: %s", user_id)

    # --- B. Setup: Create Food ---
    logger.info("Setting up temporary food item...")
    food_res = client.post(
        "/foods",
        json={
            "food_name": "Test Protein Bar",
            "serving_size": "1 bar",
            "calories": 100,
            "protein": 10.0,
            "carbohydrates": 10.0,
            "fat": 5.0,
            "fiber": 2.0,
            "sugar": 1.0,
        },
    )
    food_id = food_res.json["food_id"]
    logger.info("Created Food ID: %s", food_id)

    # --- C. Setup: Log Meals ---
    logger.info("Logging Meal 1 (Monday)...")
    meal1_res = client.post(
        "/meals",
        json={
            "user_id": user_id,
            "meal_type": "Breakfast",
            "meal_date": "2026-07-20",
            "meal_time": "08:00:00",
        },
    )
    client.post(
        f"/meals/{meal1_res.json['meal_id']}/items",
        json={"food_id": food_id, "quantity": 1.0},
    )

    logger.info("Logging Meal 2 (Tuesday)...")
    meal2_res = client.post(
        "/meals",
        json={
            "user_id": user_id,
            "meal_type": "Lunch",
            "meal_date": "2026-07-21",
            "meal_time": "12:00:00",
        },
    )
    client.post(
        f"/meals/{meal2_res.json['meal_id']}/items",
        json={"food_id": food_id, "quantity": 2.0},
    )

    # --- D. Test Daily Analytics ---
    logger.info("Testing GET /analytics/daily...")
    daily_res = client.get(f"/analytics/daily?user_id={user_id}&date=2026-07-21")
    logger.info("Daily Analytics Response: %s", daily_res.json)
    assert daily_res.status_code == 200
    assert daily_res.json["total_calories"] == 200

    # --- E. Test Weekly Analytics ---
    logger.info("Testing GET /analytics/weekly...")
    weekly_res = client.get(f"/analytics/weekly?user_id={user_id}&date=2026-07-21")
    logger.info("Weekly Analytics Totals: %s", weekly_res.json["totals"])
    assert weekly_res.status_code == 200
    assert weekly_res.json["totals"]["calories"] == 300

    # --- F. Cleanup ---
    logger.info("Cleaning up database...")
    client.delete(f"/users/{user_id}")
    client.delete(f"/foods/{food_id}")
    logger.info("=== ANALYTICS TEST COMPLETE ===")
