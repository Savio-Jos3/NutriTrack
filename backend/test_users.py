"""
Unit tests for the Users endpoints.
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


def test_user_lifecycle(client):
    """Tests the full CRUD lifecycle for Users."""
    logger.info("=== STARTING USER TEST ===")

    random_suffix = uuid.uuid4().hex[:8]
    unique_email = f"user_tester_{random_suffix}@example.com"

    # --- A. Test Create User (POST) ---
    logger.info("Testing POST /users...")
    post_payload = {
        "name": "User Tester",
        "email": unique_email,
        "age": 30,
        "gender": "Female",
        "height": 165.0,
        "weight": 65.0,
        "daily_calorie_goal": 2000,
    }
    post_res = client.post("/users", json=post_payload)
    assert post_res.status_code == 201, f"User creation failed: {post_res.json}"

    user_id = post_res.json["user_id"]
    logger.info("Created User ID: %s", user_id)

    # --- B. Test Read User (GET) ---
    logger.info("Testing GET /users/%s...", user_id)
    get_res = client.get(f"/users/{user_id}")
    assert get_res.status_code == 200
    assert get_res.json["email"] == unique_email

    # --- C. Test Update User (PUT) ---
    logger.info("Testing PUT /users/%s...", user_id)
    put_payload = post_payload.copy()
    put_payload["age"] = 31
    put_res = client.put(f"/users/{user_id}", json=put_payload)
    assert put_res.status_code == 200

    # --- D. Test Delete User (DELETE) ---
    logger.info("Testing DELETE /users/%s...", user_id)
    del_res = client.delete(f"/users/{user_id}")
    assert del_res.status_code == 200

    logger.info("=== USER TEST COMPLETE ===")
