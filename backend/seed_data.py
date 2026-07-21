"""
Seed script for NutriTrack.
Populates the database with initial users, nutritional goals,
a comprehensive food database, and historical meal data for analytics.
"""

import sqlite3
import random
from datetime import datetime, timedelta

import db as db


def seed_users(cursor: sqlite3.Cursor) -> None:
    """Seeds 10 dummy users into the database."""
    print("Seeding 10 Users...")
    users_data = [
        (1, "Alice Smith", "alice@example.com", 28, "Female", 165.0, 60.0, 2000),
        (2, "Bob Johnson", "bob@example.com", 34, "Male", 180.0, 85.0, 2500),
        (3, "Charlie Davis", "charlie@example.com", 22, "Male", 175.0, 70.0, 2800),
        (4, "Diana Prince", "diana@example.com", 30, "Female", 170.0, 65.0, 2200),
        (5, "Ethan Hunt", "ethan@example.com", 40, "Male", 178.0, 80.0, 2400),
        (6, "Fiona Gallagher", "fiona@example.com", 25, "Female", 160.0, 55.0, 1800),
        (7, "George Costanza", "george@example.com", 45, "Male", 165.0, 95.0, 2000),
        (8, "Hannah Abbott", "hannah@example.com", 29, "Female", 168.0, 62.0, 2100),
        (9, "Ian Malcolm", "ian@example.com", 50, "Male", 182.0, 78.0, 2300),
        (10, "Jane Doe", "jane@example.com", 31, "Female", 163.0, 58.0, 1900),
    ]

    cursor.executemany(
        """
        INSERT OR IGNORE INTO Users 
        (user_id, name, email, age, gender, height, weight, daily_calorie_goal)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        users_data,
    )


def seed_goals(cursor: sqlite3.Cursor) -> None:
    """Seeds nutritional goals for the first 5 users."""
    print("Seeding Nutrition Goals for Users 1-5...")
    goals_data = [
        # goal_id, user_id, daily_calories, protein, carbs, fat, fiber
        (1, 1, 2000, 120.0, 200.0, 60.0, 25.0),
        (2, 2, 2500, 180.0, 250.0, 80.0, 30.0),
        (3, 3, 2800, 200.0, 300.0, 85.0, 35.0),
        (4, 4, 2200, 140.0, 220.0, 65.0, 28.0),
        (5, 5, 2400, 160.0, 240.0, 75.0, 30.0),
    ]

    cursor.executemany(
        """
        INSERT OR IGNORE INTO NutritionGoals 
        (goal_id, user_id, daily_calories, protein_goal, 
        carbohydrate_goal, fat_goal, fiber_goal)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        goals_data,
    )


def seed_foods(cursor: sqlite3.Cursor) -> None:
    """Seeds 80 food items into the database."""
    print("Seeding 80 Food Items...")
    foods_data = [
        # Proteins
        ("Grilled Chicken Breast", "100g", 165, 31.0, 0.0, 3.6, 0.0, 0.0),
        ("Salmon Fillet", "100g", 208, 20.0, 0.0, 13.0, 0.0, 0.0),
        ("Lean Ground Beef (90/10)", "100g", 176, 20.0, 0.0, 10.0, 0.0, 0.0),
        ("Firm Tofu", "100g", 144, 15.7, 2.8, 8.7, 2.3, 0.6),
        ("Large Egg", "1 egg", 72, 6.3, 0.4, 4.8, 0.0, 0.2),
        ("Pork Tenderloin", "100g", 143, 26.0, 0.0, 3.5, 0.0, 0.0),
        ("Canned Tuna in Water", "100g", 85, 19.0, 0.0, 0.8, 0.0, 0.0),
        ("Shrimp (Cooked)", "100g", 99, 24.0, 0.2, 0.3, 0.0, 0.0),
        ("Turkey Breast", "100g", 135, 30.0, 0.0, 1.0, 0.0, 0.0),
        ("Cottage Cheese (2%)", "100g", 81, 10.4, 4.8, 2.3, 0.0, 4.0),
        # Carbohydrates
        ("Brown Rice (Cooked)", "1 cup", 216, 5.0, 45.0, 1.8, 3.5, 0.7),
        ("White Rice (Cooked)", "1 cup", 205, 4.3, 44.5, 0.4, 0.6, 0.1),
        ("Quinoa (Cooked)", "1 cup", 222, 8.1, 39.4, 3.6, 5.2, 1.6),
        ("Sweet Potato (Baked)", "1 medium", 103, 2.0, 23.6, 0.2, 3.8, 7.0),
        ("Russet Potato (Baked)", "1 medium", 161, 4.3, 36.6, 0.2, 3.8, 1.7),
        ("Oatmeal (Rolled Oats)", "1/2 cup dry", 150, 5.0, 27.0, 3.0, 4.0, 1.0),
        ("Whole Wheat Bread", "1 slice", 81, 4.0, 13.7, 1.1, 1.9, 1.4),
        ("White Bread", "1 slice", 75, 2.6, 14.1, 1.0, 0.8, 1.4),
        ("Whole Wheat Pasta", "1 cup cooked", 174, 7.5, 37.2, 0.8, 4.6, 0.8),
        ("Lentils (Cooked)", "1 cup", 230, 17.9, 39.9, 0.8, 15.6, 3.6),
        ("Black Beans (Cooked)", "1 cup", 227, 15.2, 40.8, 0.9, 15.0, 0.3),
        ("Chickpeas (Cooked)", "1 cup", 269, 14.5, 45.0, 4.2, 12.5, 7.9),
        # Vegetables
        ("Broccoli", "1 cup chopped", 31, 2.6, 6.0, 0.3, 2.4, 1.5),
        ("Spinach (Raw)", "1 cup", 7, 0.9, 1.1, 0.1, 0.7, 0.1),
        ("Kale (Raw)", "1 cup", 33, 2.9, 6.0, 0.6, 2.6, 1.3),
        ("Carrots", "1 medium", 25, 0.6, 5.8, 0.1, 1.7, 2.9),
        ("Bell Pepper (Red)", "1 medium", 31, 1.2, 7.2, 0.4, 2.5, 5.0),
        ("Zucchini", "1 medium", 33, 2.4, 6.1, 0.6, 2.0, 4.9),
        ("Cauliflower", "1 cup chopped", 27, 2.1, 5.3, 0.3, 2.1, 2.0),
        ("Brussels Sprouts", "1 cup", 38, 3.0, 7.9, 0.3, 3.3, 2.2),
        ("Asparagus", "1 cup", 27, 2.9, 5.2, 0.2, 2.8, 1.7),
        ("Cucumber", "1/2 cup sliced", 8, 0.3, 1.9, 0.1, 0.3, 0.9),
        ("Tomato", "1 medium", 22, 1.1, 4.8, 0.2, 1.5, 3.2),
        ("Onion", "1 medium", 44, 1.2, 10.3, 0.1, 1.9, 4.7),
        ("Garlic", "1 clove", 4, 0.2, 1.0, 0.0, 0.1, 0.0),
        ("Mushrooms (White)", "1 cup", 15, 2.2, 2.3, 0.2, 0.7, 1.4),
        ("Green Beans", "1 cup", 31, 1.8, 7.0, 0.1, 2.7, 3.3),
        # Fruits
        ("Apple", "1 medium", 95, 0.5, 25.1, 0.3, 4.4, 18.9),
        ("Banana", "1 medium", 105, 1.3, 27.0, 0.4, 3.1, 14.4),
        ("Orange", "1 medium", 62, 1.2, 15.4, 0.2, 3.1, 12.2),
        ("Strawberries", "1 cup whole", 46, 1.0, 11.1, 0.4, 2.9, 7.0),
        ("Blueberries", "1 cup", 84, 1.1, 21.4, 0.5, 3.6, 14.7),
        ("Grapes (Red/Green)", "1 cup", 104, 1.1, 27.3, 0.2, 1.4, 23.4),
        ("Watermelon", "1 cup diced", 46, 0.9, 11.5, 0.2, 0.6, 9.4),
        ("Pineapple", "1 cup chunks", 82, 0.9, 21.6, 0.2, 2.3, 16.3),
        ("Mango", "1 cup pieces", 99, 1.4, 24.7, 0.6, 2.6, 22.5),
        ("Peach", "1 medium", 59, 1.4, 14.3, 0.4, 2.3, 12.6),
        ("Pear", "1 medium", 101, 0.6, 27.1, 0.3, 5.5, 17.4),
        ("Kiwi", "1 medium", 42, 0.8, 10.1, 0.4, 2.1, 6.2),
        # Fats & Oils
        ("Avocado", "1/2 medium", 114, 1.0, 5.9, 10.5, 4.6, 0.2),
        ("Olive Oil", "1 tbsp", 119, 0.0, 0.0, 13.5, 0.0, 0.0),
        ("Butter", "1 tbsp", 102, 0.1, 0.0, 11.5, 0.0, 0.0),
        ("Coconut Oil", "1 tbsp", 117, 0.0, 0.0, 13.6, 0.0, 0.0),
        ("Almonds", "1 oz (28g)", 164, 6.0, 6.1, 14.1, 3.5, 1.2),
        ("Walnuts", "1 oz (28g)", 185, 4.3, 3.9, 18.5, 1.9, 0.7),
        ("Peanut Butter (Smooth)", "2 tbsp", 190, 8.0, 6.0, 16.0, 2.0, 3.0),
        ("Almond Butter", "2 tbsp", 196, 6.7, 6.0, 17.8, 3.3, 1.4),
        ("Chia Seeds", "1 oz (28g)", 138, 4.7, 11.9, 8.7, 9.8, 0.0),
        ("Flaxseeds (Ground)", "1 tbsp", 37, 1.3, 2.0, 3.0, 1.9, 0.1),
        # Dairy & Alternatives
        ("Whole Milk", "1 cup", 149, 7.7, 11.7, 7.9, 0.0, 12.3),
        ("Almond Milk (Unsweetened)", "1 cup", 39, 1.0, 3.4, 2.5, 0.5, 2.0),
        ("Greek Yogurt (Plain, Non-fat)", "100g", 59, 10.3, 3.6, 0.4, 0.0, 3.2),
        ("Cheddar Cheese", "1 slice (28g)", 113, 7.0, 0.4, 9.3, 0.0, 0.1),
        ("Mozzarella (Part-Skim)", "1 oz (28g)", 72, 6.9, 0.8, 4.5, 0.0, 0.3),
        # Snacks & Extras
        ("Dark Chocolate (70-85%)", "1 oz (28g)", 170, 2.2, 13.0, 12.1, 3.1, 6.8),
        ("Popcorn (Air-popped)", "1 cup", 31, 1.0, 6.2, 0.4, 1.2, 0.1),
        ("Hummus", "2 tbsp", 50, 2.4, 4.2, 2.8, 1.8, 0.1),
        ("Honey", "1 tbsp", 64, 0.1, 17.3, 0.0, 0.0, 17.2),
        ("Maple Syrup", "1 tbsp", 52, 0.0, 13.4, 0.0, 0.0, 12.1),
        ("Tortilla Chips", "1 oz (28g)", 140, 2.0, 19.0, 7.0, 1.5, 0.5),
        ("Salsa", "2 tbsp", 10, 0.5, 2.0, 0.0, 0.5, 1.0),
        ("Protein Powder (Whey)", "1 scoop (30g)", 113, 25.0, 2.0, 0.5, 0.0, 1.0),
        ("Oat Milk (Unsweetened)", "1 cup", 120, 3.0, 16.0, 5.0, 2.0, 7.0),
        ("Bacon", "1 slice", 43, 3.0, 0.1, 3.3, 0.0, 0.0),
        ("Avocado Oil", "1 tbsp", 124, 0.0, 0.0, 14.0, 0.0, 0.0),
        ("Cashews", "1 oz (28g)", 157, 5.2, 8.6, 12.4, 0.9, 1.7),
        ("Pistachios", "1 oz (28g)", 159, 5.7, 7.7, 12.8, 3.0, 2.2),
        ("Pumpkin Seeds", "1 oz (28g)", 151, 7.0, 5.0, 13.0, 1.7, 0.3),
        ("Sunflower Seeds", "1 oz (28g)", 164, 5.8, 5.6, 14.1, 2.4, 0.7),
        ("Mayonnaise", "1 tbsp", 94, 0.1, 0.1, 10.3, 0.0, 0.1),
    ]

    cursor.executemany(
        """
        INSERT OR IGNORE INTO Foods 
        (food_name, serving_size, calories, protein, 
        carbohydrates, fat, fiber, sugar)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        foods_data,
    )


def seed_meals(cursor: sqlite3.Cursor) -> None:
    """Generates 30 days of historical meal data for Analytics."""
    print("Generating 30 days of historical meal data for Analytics...")

    cursor.execute("SELECT food_id, calories FROM Foods")
    available_foods = cursor.fetchall()

    today = datetime.now()
    meal_templates = [
        ("Breakfast", "08:00:00"),
        ("Lunch", "13:00:00"),
        ("Snack", "15:30:00"),
        ("Dinner", "19:00:00"),
    ]

    target_users = [1, 2]

    for user_id in target_users:
        for day_offset in range(30):
            current_date = (today - timedelta(days=day_offset)).strftime("%Y-%m-%d")
            daily_meals = random.sample(meal_templates, random.randint(3, 4))

            for meal_type, meal_time in daily_meals:
                cursor.execute(
                    """
                    INSERT INTO Meals (user_id, meal_type, meal_date, meal_time)
                    VALUES (?, ?, ?, ?)
                    """,
                    (user_id, meal_type, current_date, meal_time),
                )
                meal_id = cursor.lastrowid

                num_items = random.randint(2, 4)
                selected_foods = random.sample(available_foods, num_items)

                for food in selected_foods:
                    food_id = food[0]
                    base_calories = food[1]
                    quantity = round(random.uniform(0.5, 2.5), 1)
                    calories_consumed = int(base_calories * quantity)

                    cursor.execute(
                        """
                        INSERT INTO MealItems 
                        (meal_id, food_id, quantity, calories_consumed)
                        VALUES (?, ?, ?, ?)
                        """,
                        (meal_id, food_id, quantity, calories_consumed),
                    )


def seed_database() -> None:
    """Main orchestrator to seed all database tables."""
    conn = db.get_connection()
    cursor = conn.cursor()

    try:
        # Enforce foreign key constraints
        cursor.execute("PRAGMA foreign_keys = ON;")
        print("Starting massive database seeding...")

        seed_users(cursor)
        seed_goals(cursor)
        seed_foods(cursor)
        seed_meals(cursor)

        conn.commit()
        print("Success! Database populated with rich historical analytics data.")

    except sqlite3.Error as error:
        print(f"Database error occurred: {error}")
    finally:
        conn.close()


if __name__ == "__main__":
    seed_database()
