from flask import Flask, request, jsonify
import db

app = Flask(__name__)

# --- USER ENDPOINTS ---

@app.route('/users', methods=['POST'])
def create_user():
    """Creates a new user profile."""
    data = request.get_json()
    
    # Input validation: check for required fields[cite: 2]
    required_fields = ['name', 'email', 'age', 'gender', 'height', 'weight', 'daily_calorie_goal']
    if not data or not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

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
        # Returns 201 Created upon successful insertion[cite: 2]
        return jsonify({"message": "User created successfully", "user_id": new_id}), 201
    except Exception as e:
        # Catch errors such as UNIQUE constraint failure on the email
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
    app.run(debug=True)