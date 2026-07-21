"""
Unit tests for the Foods endpoints.
"""

# pylint: disable=redefined-outer-name

import logging
import pytest
from app import app

logger = logging.getLogger(__name__)


@pytest.fixture
def client():
    """Configures a temporary Flask test client."""
    app.config["TESTING"] = True
    with app.test_client() as test_client:
        yield test_client


def test_food_lifecycle(client):
    """Tests the full CRUD lifecycle for Foods."""
    logger.info("=== STARTING FOOD TEST ===")

    # --- A. Test Create Food (POST) ---
    logger.info("Testing POST /foods...")
    post_payload = {
        "food_name": "Test Apple",
        "serving_size": "1 medium",
        "calories": 95,
        "protein": 0.5,
        "carbohydrates": 25.0,
        "fat": 0.3,
        "fiber": 4.4,
        "sugar": 19.0,
    }
    post_res = client.post("/foods", json=post_payload)
    assert post_res.status_code == 201

    food_id = post_res.json["food_id"]
    logger.info("Created Food ID: %s", food_id)

    # --- B. Test Read Food (GET) ---
    logger.info("Testing GET /foods/%s...", food_id)
    get_res = client.get(f"/foods/{food_id}")
    assert get_res.status_code == 200
    assert get_res.json["food_name"] == "Test Apple"

    # --- C. Test Update Food (PUT) ---
    logger.info("Testing PUT /foods/%s...", food_id)
    put_payload = post_payload.copy()
    put_payload["calories"] = 100
    put_res = client.put(f"/foods/{food_id}", json=put_payload)
    assert put_res.status_code == 200

    # --- D. Test Delete Food (DELETE) ---
    logger.info("Testing DELETE /foods/%s...", food_id)
    del_res = client.delete(f"/foods/{food_id}")
    assert del_res.status_code == 200

    logger.info("=== FOOD TEST COMPLETE ===")
