"""
Unit tests for the Nutrition Goals endpoints.
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


def test_goal_lifecycle(client):
    """Tests the full CRUD lifecycle for Nutrition Goals."""
    logger.info("=== STARTING GOALS TEST ===")

    # --- A. Setup: Create a temporary User ---
    random_suffix = uuid.uuid4().hex[:8]
    unique_email = f"goal_tester_{random_suffix}@example.com"

    logger.info("Setting up temporary user...")
    user_res = client.post(
        "/users",
        json={
            "name": "Goal Tester",
            "email": unique_email,
            "age": 28,
            "gender": "Female",
            "height": 165.0,
            "weight": 60.0,
            "daily_calorie_goal": 2000,
        },
    )
    assert user_res.status_code == 201, f"User creation failed: {user_res.json}"
    user_id = user_res.json["user_id"]

    # --- B. Test Create Goal (POST) ---
    logger.info("Testing POST /goals...")
    post_res = client.post(
        "/goals",
        json={
            "user_id": user_id,
            "daily_calories": 2100,
            "protein_goal": 140.0,
            "carbohydrate_goal": 220.0,
            "fat_goal": 65.0,
            "fiber_goal": 25.0,
        },
    )
    assert post_res.status_code == 201

    # --- C. Test Read Goal (GET) ---
    logger.info("Testing GET /goals/user/%s...", user_id)
    get_res = client.get(f"/goals/user/{user_id}")
    assert get_res.status_code == 200
    assert get_res.json["daily_calories"] == 2100

    # --- D. Test Update Goal (PUT) ---
    logger.info("Testing PUT /goals/user/%s...", user_id)
    put_res = client.put(
        f"/goals/user/{user_id}",
        json={
            "daily_calories": 2300,
            "protein_goal": 160.0,
            "carbohydrate_goal": 240.0,
            "fat_goal": 70.0,
            "fiber_goal": 30.0,
        },
    )
    assert put_res.status_code == 200

    # --- E. Test Delete Goal (DELETE) ---
    logger.info("Testing DELETE /goals/user/%s...", user_id)
    del_res = client.delete(f"/goals/user/{user_id}")
    assert del_res.status_code == 200

    # --- F. Cleanup ---
    logger.info("Cleaning up database...")
    client.delete(f"/users/{user_id}")

    logger.info("=== GOALS TEST COMPLETE ===")
