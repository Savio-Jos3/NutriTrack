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

# Run the initialization when the file is executed directly
if __name__ == '__main__':
    init_db()