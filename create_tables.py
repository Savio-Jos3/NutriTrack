import db
import sqlite3


def create_schema():
    """Executes the DDL commands to generate the database schema."""
    conn = db.get_connection()
    cursor = conn.cursor()

    try:
        print("Initializing database schema...")
        cursor.execute("PRAGMA foreign_keys = ON;")

        # Users Table
        cursor.execute("""
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
        """)

        # Foods Table
        cursor.execute("""
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
        """)

        # Meals Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Meals (
                meal_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                meal_type VARCHAR NOT NULL,
                meal_date DATE NOT NULL,
                meal_time TIME NOT NULL,
                FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
            )
        """)

        # MealItems Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS MealItems (
                meal_id INTEGER NOT NULL,
                food_id INTEGER NOT NULL,
                quantity FLOAT NOT NULL,
                calories_consumed INTEGER NOT NULL,
                PRIMARY KEY (meal_id, food_id),
                FOREIGN KEY (meal_id) REFERENCES Meals(meal_id) ON DELETE CASCADE,
                FOREIGN KEY (food_id) REFERENCES Foods(food_id) ON DELETE CASCADE
            )
        """)

        # Nutrition Goals Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS NutritionGoals (
                goal_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE NOT NULL,
                daily_calories INTEGER NOT NULL,
                protein_goal FLOAT,
                carbohydrate_goal FLOAT,
                fat_goal FLOAT,
                fiber_goal FLOAT,
                FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
            )
        """)

        conn.commit()
        print("Schema creation successful! All tables are ready.")

    except sqlite3.Error as e:
        print(f"Schema creation failed: {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    create_schema()
