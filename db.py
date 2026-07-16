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
        conn = sqlite3.connect(DB_PATH)
        # This allows us to access columns by name (like a dictionary)
        conn.row_factory = sqlite3.Row 
        return conn
    else:
        # We will implement the MySQL connection here later for production
        pass

def init_db():
    """Initializes the SQLite database with the required tables."""
    conn = get_connection()
    cursor = conn.cursor()

    # 1. Create Users Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR NOT NULL,
            email VARCHAR UNIQUE NOT NULL,
            age INTEGER,
            gender VARCHAR,
            height FLOAT,
            weight FLOAT,
            daily_calorie_goal INTEGER,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 2. Create Foods Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Foods (
            food_id INTEGER PRIMARY KEY AUTOINCREMENT,
            food_name VARCHAR NOT NULL,
            serving_size VARCHAR,
            calories INTEGER NOT NULL,
            protein FLOAT,
            carbohydrates FLOAT,
            fat FLOAT,
            fiber FLOAT,
            sugar FLOAT
        )
    ''')

    # We will add the Meals, MealItems, and NutritionGoals tables next...

    conn.commit()
    conn.close()
    print("Database initialized successfully!")

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

# Run the initialization when the file is executed directly
if __name__ == '__main__':
    init_db()