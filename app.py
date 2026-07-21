from flask import Flask, request, jsonify
from flask_cors import CORS # Import CORS
import db

app = Flask(__name__)
CORS(app)
# --- USER ENDPOINTS ---

@app.route('/users', methods=['POST'])
def create_user():
    """Creates a new user profile."""
    # silent=True prevents Flask from crashing if the payload isn't JSON
    data = request.get_json(silent=True) 
    
    # 1. Check if Flask sees any JSON at all
    if data is None:
        print("DEBUG: No JSON detected. Check Content-Type header in Postman.")
        return jsonify({"error": "No JSON payload received. Ensure Content-Type is application/json"}), 400

    print("DEBUG: Received JSON Data:", data)

    # 2. Check exactly which fields are missing
    required_fields = ['name', 'email', 'age', 'gender', 'height', 'weight', 'daily_calorie_goal']
    missing_fields = [field for field in required_fields if field not in data]
    
    if missing_fields:
        print("DEBUG: Missing fields ->", missing_fields)
        return jsonify({"error": f"Missing required fields: {missing_fields}"}), 400

    try:
        new_id = db.create_user(
            name=data['name'],
            email=data['email'],
            age=data['age'],
            gender=data['gender'],
            height=data['height'],
            weight=data['weight'],
            daily_calorie_goal=data['daily_calorie_goal']
        )
        return jsonify({"message": "User created successfully", "user_id": new_id}), 201
    except Exception as e:
        print("DEBUG: Database Error ->", str(e))
        return jsonify({"error": str(e)}), 400

@app.route('/users', methods=['GET'])
def get_users():
    """Retrieves all users."""
    users = db.get_all_users()
    # Returns 200 OK by default[cite: 2]
    return jsonify(users), 200

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Retrieves a specific user by ID."""
    user = db.get_user_by_id(user_id)
    if user:
        return jsonify(user), 200
    
    # Returns 404 if the resource is not found[cite: 2]
    return jsonify({"error": "User not found"}), 404

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Updates a specific user."""
    data = request.get_json()
    
    required_fields = ['name', 'email', 'age', 'gender', 'height', 'weight', 'daily_calorie_goal']
    if not data or not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    success = db.update_user(
        user_id=user_id,
        name=data['name'],
        email=data['email'],
        age=data['age'],
        gender=data['gender'],
        height=data['height'],
        weight=data['weight'],
        daily_calorie_goal=data['daily_calorie_goal']
    )
    
    if success:
        return jsonify({"message": "User updated successfully"}), 200
    
    return jsonify({"error": "User not found"}), 404

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Deletes a specific user."""
    success = db.delete_user(user_id)
    
    if success:
        return jsonify({"message": "User deleted successfully"}), 200
    
    return jsonify({"error": "User not found"}), 404

@app.route('/foods', methods=['POST'])
def add_food():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "No JSON payload received"}), 400

    required_fields = ['food_name', 'serving_size', 'calories', 'protein', 'carbohydrates', 'fat', 'fiber', 'sugar']
    missing_fields = [field for field in required_fields if field not in data]
    
    if missing_fields:
        return jsonify({"error": f"Missing required fields: {missing_fields}"}), 400

    try:
        new_id = db.create_food(
            food_name=data['food_name'],
            serving_size=data['serving_size'],
            calories=data['calories'],
            protein=data['protein'],
            carbohydrates=data['carbohydrates'],
            fat=data['fat'],
            fiber=data['fiber'],
            sugar=data['sugar']
        )
        return jsonify({"message": "Food created successfully", "food_id": new_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/foods', methods=['GET'])
def get_foods():
    try:
        foods = db.get_all_foods()
        return jsonify(foods), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/foods/<int:food_id>', methods=['GET'])
def get_food(food_id):
    try:
        food = db.get_food_by_id(food_id)
        if food:
            return jsonify(food), 200
        return jsonify({"error": "Food not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/foods/<int:food_id>', methods=['PUT'])
def update_food(food_id):
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "No JSON payload received"}), 400
        
    try:
        success = db.update_food(
            food_id=food_id,
            food_name=data.get('food_name'),
            serving_size=data.get('serving_size'),
            calories=data.get('calories'),
            protein=data.get('protein'),
            carbohydrates=data.get('carbohydrates'),
            fat=data.get('fat'),
            fiber=data.get('fiber'),
            sugar=data.get('sugar')
        )
        if success:
            return jsonify({"message": "Food updated successfully"}), 200
        return jsonify({"error": "Food not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/foods/<int:food_id>', methods=['DELETE'])
def delete_food(food_id):
    try:
        success = db.delete_food(food_id)
        if success:
            return jsonify({"message": "Food deleted successfully"}), 200
        return jsonify({"error": "Food not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==========================================
# MEALS ENDPOINTS
# ==========================================

@app.route('/meals', methods=['POST'])
def create_meal():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "No JSON payload received"}), 400

    required_fields = ['user_id', 'meal_type', 'meal_date', 'meal_time']
    if any(field not in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        meal_id = db.create_meal(
            user_id=data['user_id'],
            meal_type=data['meal_type'],
            meal_date=data['meal_date'],
            meal_time=data['meal_time']
        )
        return jsonify({"message": "Meal created successfully", "meal_id": meal_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/meals/<int:meal_id>/items', methods=['POST'])
def add_meal_item(meal_id):
    data = request.get_json(silent=True)
    if not data or 'food_id' not in data or 'quantity' not in data:
        return jsonify({"error": "Requires food_id and quantity"}), 400

    try:
        calories_consumed = db.add_food_to_meal(
            meal_id=meal_id,
            food_id=data['food_id'],
            quantity=data['quantity']
        )
        return jsonify({
            "message": "Food added to meal", 
            "calories_consumed": calories_consumed
        }), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        # Catch SQLite Integrity Errors (like adding the same food twice to one meal)
        return jsonify({"error": "Database error, possibly duplicate food in this meal.", "details": str(e)}), 400

@app.route('/meals/<int:meal_id>', methods=['GET'])
def get_meal(meal_id):
    try:
        meal_data = db.get_meal_details(meal_id)
        if meal_data:
            return jsonify(meal_data), 200
        return jsonify({"error": "Meal not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==========================================
# NUTRITION GOALS ENDPOINTS
# ==========================================

@app.route('/goals', methods=['POST'])
def create_goal():
    data = request.get_json(silent=True)
    if not data or 'user_id' not in data or 'daily_calories' not in data:
        return jsonify({"error": "Missing user_id or daily_calories"}), 400

    try:
        goal_id = db.create_nutrition_goal(
            user_id=data['user_id'],
            daily_calories=data['daily_calories'],
            protein_goal=data.get('protein_goal'),
            carbohydrate_goal=data.get('carbohydrate_goal'),
            fat_goal=data.get('fat_goal'),
            fiber_goal=data.get('fiber_goal')
        )
        return jsonify({"message": "Goal created successfully", "goal_id": goal_id}), 201
    except Exception as e:
        # If user_id already has a goal, the UNIQUE constraint will throw an error
        return jsonify({"error": "Database error. Does this user already have a goal?", "details": str(e)}), 400

@app.route('/goals/user/<int:user_id>', methods=['GET'])
def get_goal(user_id):
    try:
        goal = db.get_nutrition_goal_by_user(user_id)
        if goal:
            return jsonify(goal), 200
        return jsonify({"error": "Nutrition goal not found for this user"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/goals/user/<int:user_id>', methods=['PUT'])
def update_goal(user_id):
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "No JSON payload received"}), 400
        
    try:
        success = db.update_nutrition_goal(
            user_id=user_id,
            daily_calories=data.get('daily_calories'),
            protein_goal=data.get('protein_goal'),
            carbohydrate_goal=data.get('carbohydrate_goal'),
            fat_goal=data.get('fat_goal'),
            fiber_goal=data.get('fiber_goal')
        )
        if success:
            return jsonify({"message": "Goal updated successfully"}), 200
        return jsonify({"error": "Nutrition goal not found for this user"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/goals/user/<int:user_id>', methods=['DELETE'])
def delete_goal(user_id):
    try:
        success = db.delete_nutrition_goal(user_id)
        if success:
            return jsonify({"message": "Goal deleted successfully"}), 200
        return jsonify({"error": "Nutrition goal not found for this user"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Run the Flask development server
    app.run(port=5001, debug=True)