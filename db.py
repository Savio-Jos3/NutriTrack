import os
import sqlite3
from dotenv import load_dotenv

# Load the development environment variables
load_dotenv('.env.development')

DB_TYPE = os.getenv('DB_TYPE')
DB_PATH = os.getenv('DB_PATH')

def get_connection():
    """Establishes and returns a database connection based on the environment."""
    if DB_TYPE == 'sqlite':
        # SQLite is built-in, so we just point it to the file path
        conn = sqlite3.connect(DB_PATH, timeout=15)
        # This allows us to access columns by name (like a dictionary)
        conn.row_factory = sqlite3.Row 
        return conn
    else:
        # We will implement the MySQL connection here later for production
        pass


from typing import List, Dict, Optional, Any

# --- USER CRUD OPERATIONS ---

def create_user(name: str, email: str, age: int, gender: str, height: float, weight: float, daily_calorie_goal: int) -> int:
    """Inserts a new user into the database and returns the new user_id."""
    conn = get_connection()
    cursor = conn.cursor()
    
    query = '''
        INSERT INTO Users (name, email, age, gender, height, weight, daily_calorie_goal)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    '''
    # Parameterized query to prevent SQL injection
    cursor.execute(query, (name, email, age, gender, height, weight, daily_calorie_goal))
    conn.commit()
    
    new_id = cursor.lastrowid
    conn.close()
    return new_id

def get_all_users() -> List[Dict[str, Any]]:
    """Retrieves all users from the database."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM Users")
    rows = cursor.fetchall()
    conn.close()
    
    # Convert sqlite3.Row objects to standard Python dictionaries
    return [dict(row) for row in rows]

def get_user_by_id(user_id: int) -> Optional[Dict[str, Any]]:
    """Retrieves a specific user by their ID."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM Users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return dict(row)
    return None

def update_user(user_id: int, name: str, email: str, age: int, gender: str, height: float, weight: float, daily_calorie_goal: int) -> bool:
    """Updates an existing user's information. Returns True if successful."""
    conn = get_connection()
    cursor = conn.cursor()
    
    query = '''
        UPDATE Users 
        SET name = ?, email = ?, age = ?, gender = ?, height = ?, weight = ?, daily_calorie_goal = ?
        WHERE user_id = ?
    '''
    cursor.execute(query, (name, email, age, gender, height, weight, daily_calorie_goal, user_id))
    conn.commit()
    
    rows_affected = cursor.rowcount
    conn.close()
    
    return rows_affected > 0

def delete_user(user_id: int) -> bool:
    """Deletes a user from the database. Returns True if successful."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM Users WHERE user_id = ?", (user_id,))
    conn.commit()
    
    rows_affected = cursor.rowcount
    conn.close()
    
    return rows_affected > 0

# ==========================================
# FOOD CRUD OPERATIONS
# ==========================================

def create_food(food_name, serving_size, calories, protein, carbohydrates, fat, fiber, sugar):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Foods (food_name, serving_size, calories, protein, carbohydrates, fat, fiber, sugar)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (food_name, serving_size, calories, protein, carbohydrates, fat, fiber, sugar))
    conn.commit()
    food_id = cursor.lastrowid
    conn.close()
    return food_id

def get_all_foods():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Foods')
    foods = cursor.fetchall()
    conn.close()
    return [dict(row) for row in foods]

def get_food_by_id(food_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Foods WHERE food_id = ?', (food_id,))
    food = cursor.fetchone()
    conn.close()
    return dict(food) if food else None

def update_food(food_id, food_name, serving_size, calories, protein, carbohydrates, fat, fiber, sugar):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE Foods 
        SET food_name = ?, serving_size = ?, calories = ?, protein = ?, 
            carbohydrates = ?, fat = ?, fiber = ?, sugar = ?
        WHERE food_id = ?
    ''', (food_name, serving_size, calories, protein, carbohydrates, fat, fiber, sugar, food_id))
    conn.commit()
    rows_affected = cursor.rowcount
    conn.close()
    return rows_affected > 0

def delete_food(food_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Foods WHERE food_id = ?', (food_id,))
    conn.commit()
    rows_affected = cursor.rowcount
    conn.close()
    return rows_affected > 0

#MEAL CRUD OPERATIONS
# ==========================================
# MEALS & MEAL ITEMS OPERATIONS
# ==========================================

def create_meal(user_id, meal_type, meal_date, meal_time):
    """Creates a new meal container for a user."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Meals (user_id, meal_type, meal_date, meal_time)
        VALUES (?, ?, ?, ?)
    ''', (user_id, meal_type, meal_date, meal_time))
    conn.commit()
    meal_id = cursor.lastrowid
    conn.close()
    return meal_id

def add_food_to_meal(meal_id, food_id, quantity):
    """Adds a food to a meal safely, ensuring connections close on error."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        
        # 1. Fetch base calories
        cursor.execute('SELECT calories FROM Foods WHERE food_id = ?', (food_id,))
        food = cursor.fetchone()
        if not food:
            raise ValueError("Food item not found")
            
        base_calories = food['calories']
        calories_consumed = int(base_calories * float(quantity))

        # 2. Insert the meal item
        cursor.execute('''
            INSERT INTO MealItems (meal_id, food_id, quantity, calories_consumed)
            VALUES (?, ?, ?, ?)
        ''', (meal_id, food_id, quantity, calories_consumed))
        
        conn.commit()
        return calories_consumed
        
    finally:
        # This will ALWAYS execute, whether the insert succeeds or crashes
        conn.close()

def get_meal_details(meal_id):
    """Fetches a meal, all its food items, and the total caloric sum."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # 1. Get the base meal data
    cursor.execute('SELECT * FROM Meals WHERE meal_id = ?', (meal_id,))
    meal = cursor.fetchone()
    if not meal:
        conn.close()
        return None
        
    meal_dict = dict(meal)

    # 2. Get all associated food items by joining MealItems with Foods
    cursor.execute('''
        SELECT mi.food_id, f.food_name, f.serving_size, mi.quantity, mi.calories_consumed
        FROM MealItems mi
        JOIN Foods f ON mi.food_id = f.food_id
        WHERE mi.meal_id = ?
    ''', (meal_id,))
    items = cursor.fetchall()
    
    meal_dict['items'] = [dict(item) for item in items]
    
    # 3. Calculate the total calories for the entire meal
    meal_dict['total_meal_calories'] = sum(item['calories_consumed'] for item in meal_dict['items'])
    
    conn.close()
    return meal_dict

# ==========================================
# NUTRITION GOALS OPERATIONS
# ==========================================

def create_nutrition_goal(user_id, daily_calories, protein_goal, carbohydrate_goal, fat_goal, fiber_goal):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO NutritionGoals (user_id, daily_calories, protein_goal, carbohydrate_goal, fat_goal, fiber_goal)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, daily_calories, protein_goal, carbohydrate_goal, fat_goal, fiber_goal))
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()

def get_nutrition_goal_by_user(user_id):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM NutritionGoals WHERE user_id = ?', (user_id,))
        goal = cursor.fetchone()
        return dict(goal) if goal else None
    finally:
        conn.close()

def update_nutrition_goal(user_id, daily_calories, protein_goal, carbohydrate_goal, fat_goal, fiber_goal):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE NutritionGoals 
            SET daily_calories = ?, protein_goal = ?, carbohydrate_goal = ?, fat_goal = ?, fiber_goal = ?
            WHERE user_id = ?
        ''', (daily_calories, protein_goal, carbohydrate_goal, fat_goal, fiber_goal, user_id))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()

def delete_nutrition_goal(user_id):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM NutritionGoals WHERE user_id = ?', (user_id,))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()