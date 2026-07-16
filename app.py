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

if __name__ == '__main__':
    # Run the Flask development server
    app.run(port=5001, debug=True)