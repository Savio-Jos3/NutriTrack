"""
Main Flask application providing the REST API endpoints for NutriTrack.
Handles routing, request validation, and responses for Users, Foods, Meals, Goals, and Analytics.
"""

from typing import Tuple, Any
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import db as db
import analytics as analytics

app = Flask(__name__)
CORS(app)

# ==========================================
# USER ENDPOINTS
# ==========================================


@app.route("/users", methods=["POST"])
def create_user() -> Tuple[Response, int]:
    """Creates a new user profile."""
    data = request.get_json(silent=True)

    if data is None:
        return (
            jsonify(
                {
                    "error": "No JSON payload received. Ensure Content-Type is application/json"
                }
            ),
            400,
        )

    required_fields = [
        "name",
        "email",
        "age",
        "gender",
        "height",
        "weight",
        "daily_calorie_goal",
    ]
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return jsonify({"error": f"Missing required fields: {missing_fields}"}), 400

    try:
        new_id = db.create_user(
            name=data["name"],
            email=data["email"],
            age=data["age"],
            gender=data["gender"],
            height=data["height"],
            weight=data["weight"],
            daily_calorie_goal=data["daily_calorie_goal"],
        )
        return jsonify({"message": "User created successfully", "user_id": new_id}), 201
    except Exception as error:  # pylint: disable=broad-exception-caught
        return jsonify({"error": str(error)}), 400


@app.route("/users", methods=["GET"])
def get_users() -> Tuple[Response, int]:
    """Retrieves all users."""
    users = db.get_all_users()
    return jsonify(users), 200


@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id: int) -> Tuple[Response, int]:
    """Retrieves a specific user by ID."""
    user = db.get_user_by_id(user_id)
    if user:
        return jsonify(user), 200
    return jsonify({"error": "User not found"}), 404


@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id: int) -> Tuple[Response, int]:
    """Updates a specific user."""
    data = request.get_json()

    required_fields = [
        "name",
        "email",
        "age",
        "gender",
        "height",
        "weight",
        "daily_calorie_goal",
    ]
    if not data or not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    success = db.update_user(
        user_id=user_id,
        name=data["name"],
        email=data["email"],
        age=data["age"],
        gender=data["gender"],
        height=data["height"],
        weight=data["weight"],
        daily_calorie_goal=data["daily_calorie_goal"],
    )

    if success:
        return jsonify({"message": "User updated successfully"}), 200
    return jsonify({"error": "User not found"}), 404


@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id: int) -> Tuple[Response, int]:
    """Deletes a specific user."""
    success = db.delete_user(user_id)

    if success:
        return jsonify({"message": "User deleted successfully"}), 200
    return jsonify({"error": "User not found"}), 404


# ==========================================
# FOODS ENDPOINTS
# ==========================================


@app.route("/foods", methods=["POST"])
def add_food() -> Tuple[Response, int]:
    """Adds a new food item to the database."""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "No JSON payload received"}), 400

    required_fields = [
        "food_name",
        "serving_size",
        "calories",
        "protein",
        "carbohydrates",
        "fat",
        "fiber",
        "sugar",
    ]
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return jsonify({"error": f"Missing required fields: {missing_fields}"}), 400

    try:
        new_id = db.create_food(
            food_name=data["food_name"],
            serving_size=data["serving_size"],
            calories=data["calories"],
            protein=data["protein"],
            carbohydrates=data["carbohydrates"],
            fat=data["fat"],
            fiber=data["fiber"],
            sugar=data["sugar"],
        )
        return jsonify({"message": "Food created successfully", "food_id": new_id}), 201
    except Exception as error:  # pylint: disable=broad-exception-caught
        return jsonify({"error": str(error)}), 400


@app.route("/foods", methods=["GET"])
def get_foods() -> Tuple[Response, int]:
    """Retrieves all food items."""
    try:
        foods = db.get_all_foods()
        return jsonify(foods), 200
    except Exception as error:  # pylint: disable=broad-exception-caught
        return jsonify({"error": str(error)}), 500


@app.route("/foods/<int:food_id>", methods=["GET"])
def get_food(food_id: int) -> Tuple[Response, int]:
    """Retrieves a specific food item by its ID."""
    try:
        food = db.get_food_by_id(food_id)
        if food:
            return jsonify(food), 200
        return jsonify({"error": "Food not found"}), 404
    except Exception as error:  # pylint: disable=broad-exception-caught
        return jsonify({"error": str(error)}), 500


@app.route("/foods/<int:food_id>", methods=["PUT"])
def update_food(food_id: int) -> Tuple[Response, int]:
    """Updates an existing food item."""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "No JSON payload received"}), 400

    try:
        success = db.update_food(
            food_id=food_id,
            food_name=data.get("food_name"),
            serving_size=data.get("serving_size"),
            calories=data.get("calories"),
            protein=data.get("protein"),
            carbohydrates=data.get("carbohydrates"),
            fat=data.get("fat"),
            fiber=data.get("fiber"),
            sugar=data.get("sugar"),
        )
        if success:
            return jsonify({"message": "Food updated successfully"}), 200
        return jsonify({"error": "Food not found"}), 404
    except Exception as error:  # pylint: disable=broad-exception-caught
        return jsonify({"error": str(error)}), 400


@app.route("/foods/<int:food_id>", methods=["DELETE"])
def delete_food(food_id: int) -> Tuple[Response, int]:
    """Deletes a specific food item."""
    try:
        success = db.delete_food(food_id)
        if success:
            return jsonify({"message": "Food deleted successfully"}), 200
        return jsonify({"error": "Food not found"}), 404
    except Exception as error:  # pylint: disable=broad-exception-caught
        return jsonify({"error": str(error)}), 500


# ==========================================
# MEALS ENDPOINTS
# ==========================================


@app.route("/meals", methods=["POST"])
def create_meal() -> Tuple[Response, int]:
    """Creates a new meal container for a user."""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "No JSON payload received"}), 400

    required_fields = ["user_id", "meal_type", "meal_date", "meal_time"]
    if any(field not in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        meal_id = db.create_meal(
            user_id=data["user_id"],
            meal_type=data["meal_type"],
            meal_date=data["meal_date"],
            meal_time=data["meal_time"],
        )
        return (
            jsonify({"message": "Meal created successfully", "meal_id": meal_id}),
            201,
        )
    except Exception as error:  # pylint: disable=broad-exception-caught
        return jsonify({"error": str(error)}), 400


@app.route("/meals/<int:meal_id>/items", methods=["POST"])
def add_meal_item(meal_id: int) -> Tuple[Response, int]:
    """Adds a food item and portion quantity to an existing meal."""
    data = request.get_json(silent=True)
    if not data or "food_id" not in data or "quantity" not in data:
        return jsonify({"error": "Requires food_id and quantity"}), 400

    try:
        calories_consumed = db.add_food_to_meal(
            meal_id=meal_id, food_id=data["food_id"], quantity=data["quantity"]
        )
        return (
            jsonify(
                {
                    "message": "Food added to meal",
                    "calories_consumed": calories_consumed,
                }
            ),
            201,
        )
    except ValueError as error:
        return jsonify({"error": str(error)}), 404
    except Exception as error:  # pylint: disable=broad-exception-caught
        return (
            jsonify(
                {
                    "error": "Database error, possibly duplicate food in this meal.",
                    "details": str(error),
                }
            ),
            400,
        )


@app.route("/meals/<int:meal_id>", methods=["GET"])
def get_meal(meal_id: int) -> Tuple[Response, int]:
    """Retrieves a meal and its complete nutritional breakdown."""
    try:
        meal_data = db.get_meal_details(meal_id)
        if meal_data:
            return jsonify(meal_data), 200
        return jsonify({"error": "Meal not found"}), 404
    except Exception as error:  # pylint: disable=broad-exception-caught
        return jsonify({"error": str(error)}), 500


# ==========================================
# NUTRITION GOALS ENDPOINTS
# ==========================================


@app.route("/goals", methods=["POST"])
def create_goal() -> Tuple[Response, int]:
    """Creates a daily nutrition goal for a user."""
    data = request.get_json(silent=True)
    if not data or "user_id" not in data or "daily_calories" not in data:
        return jsonify({"error": "Missing user_id or daily_calories"}), 400

    try:
        goal_id = db.create_nutrition_goal(
            user_id=data["user_id"],
            daily_calories=data["daily_calories"],
            protein_goal=data.get("protein_goal"),
            carbohydrate_goal=data.get("carbohydrate_goal"),
            fat_goal=data.get("fat_goal"),
            fiber_goal=data.get("fiber_goal"),
        )
        return (
            jsonify({"message": "Goal created successfully", "goal_id": goal_id}),
            201,
        )
    except Exception as error:  # pylint: disable=broad-exception-caught
        return (
            jsonify(
                {
                    "error": "Database error. Does this user already have a goal?",
                    "details": str(error),
                }
            ),
            400,
        )


@app.route("/goals/user/<int:user_id>", methods=["GET"])
def get_goal(user_id: int) -> Tuple[Response, int]:
    """Retrieves the nutrition goal for a specific user."""
    try:
        goal = db.get_nutrition_goal_by_user(user_id)
        if goal:
            return jsonify(goal), 200
        return jsonify({"error": "Nutrition goal not found for this user"}), 404
    except Exception as error:  # pylint: disable=broad-exception-caught
        return jsonify({"error": str(error)}), 500


@app.route("/goals/user/<int:user_id>", methods=["PUT"])
def update_goal(user_id: int) -> Tuple[Response, int]:
    """Updates the existing nutrition goal for a specific user."""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "No JSON payload received"}), 400

    try:
        success = db.update_nutrition_goal(
            user_id=user_id,
            daily_calories=data.get("daily_calories"),
            protein_goal=data.get("protein_goal"),
            carbohydrate_goal=data.get("carbohydrate_goal"),
            fat_goal=data.get("fat_goal"),
            fiber_goal=data.get("fiber_goal"),
        )
        if success:
            return jsonify({"message": "Goal updated successfully"}), 200
        return jsonify({"error": "Nutrition goal not found for this user"}), 404
    except Exception as error:  # pylint: disable=broad-exception-caught
        return jsonify({"error": str(error)}), 400


@app.route("/goals/user/<int:user_id>", methods=["DELETE"])
def delete_goal(user_id: int) -> Tuple[Response, int]:
    """Deletes the nutrition goal for a specific user."""
    try:
        success = db.delete_nutrition_goal(user_id)
        if success:
            return jsonify({"message": "Goal deleted successfully"}), 200
        return jsonify({"error": "Nutrition goal not found for this user"}), 404
    except Exception as error:  # pylint: disable=broad-exception-caught
        return jsonify({"error": str(error)}), 500


# ==========================================
# ANALYTICS ENDPOINTS (PANDAS POWERED)
# ==========================================


@app.route("/analytics/daily", methods=["GET"])
def analytics_daily() -> Tuple[Response, int]:
    """Retrieves a nutritional summary for a specific user on a specific date."""
    user_id = request.args.get("user_id")
    date = request.args.get("date")
    if not user_id or not date:
        return jsonify({"error": "Requires user_id and date query parameters"}), 400

    try:
        data = analytics.get_daily_summary(int(user_id), date)
        return jsonify(data), 200
    except Exception as error:  # pylint: disable=broad-exception-caught
        return jsonify({"error": str(error)}), 500


@app.route("/analytics/weekly", methods=["GET"])
def analytics_weekly() -> Tuple[Response, int]:
    """Retrieves the Current Calendar Week summary (Monday to Today)."""
    user_id = request.args.get("user_id")
    date = request.args.get("date")
    if not user_id:
        return jsonify({"error": "Requires user_id"}), 400
    try:
        return (
            jsonify(analytics.get_period_analytics(int(user_id), "weekly", date)),
            200,
        )
    except Exception as error:  # pylint: disable=broad-exception-caught
        return jsonify({"error": str(error)}), 500


@app.route("/analytics/monthly", methods=["GET"])
def analytics_monthly() -> Tuple[Response, int]:
    """Retrieves the Current Calendar Month summary (1st to Today)."""
    user_id = request.args.get("user_id")
    date = request.args.get("date")
    if not user_id:
        return jsonify({"error": "Requires user_id"}), 400
    try:
        return (
            jsonify(analytics.get_period_analytics(int(user_id), "monthly", date)),
            200,
        )
    except Exception as error:  # pylint: disable=broad-exception-caught
        return jsonify({"error": str(error)}), 500


@app.route("/analytics/last7days", methods=["GET"])
def analytics_last_7_days() -> Tuple[Response, int]:
    """Retrieves the rolling 7-day window summary."""
    user_id = request.args.get("user_id")
    date = request.args.get("date")
    if not user_id:
        return jsonify({"error": "Requires user_id"}), 400
    try:
        return (
            jsonify(analytics.get_period_analytics(int(user_id), "last7days", date)),
            200,
        )
    except Exception as error:  # pylint: disable=broad-exception-caught
        return jsonify({"error": str(error)}), 500


@app.route("/analytics/last30days", methods=["GET"])
def analytics_last_30_days() -> Tuple[Response, int]:
    """Retrieves the rolling 30-day window summary."""
    user_id = request.args.get("user_id")
    date = request.args.get("date")
    if not user_id:
        return jsonify({"error": "Requires user_id"}), 400
    try:
        return (
            jsonify(analytics.get_period_analytics(int(user_id), "last30days", date)),
            200,
        )
    except Exception as error:  # pylint: disable=broad-exception-caught
        return jsonify({"error": str(error)}), 500


@app.route("/analytics/top-foods", methods=["GET"])
def analytics_top_foods() -> Tuple[Response, int]:
    """Retrieves the most frequently consumed foods for a user."""
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "Requires user_id"}), 400
    try:
        data = analytics.get_top_foods(int(user_id))
        return jsonify(data), 200
    except Exception as error:  # pylint: disable=broad-exception-caught
        return jsonify({"error": str(error)}), 500


@app.route("/meals/daily", methods=["GET"])
def get_daily_meals():
    """Returns all meals and items consumed by a user on a specific date."""
    user_id = request.args.get("user_id", type=int)
    date_str = request.args.get("date")

    if not user_id or not date_str:
        return jsonify({"error": "Missing user_id or date"}), 400

    meals = db.get_meals_by_date(user_id, date_str)
    return jsonify(meals), 200


if __name__ == "__main__":
    app.run(port=5001, debug=True)
