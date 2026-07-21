"""
Analytics service layer for NutriTrack.
Uses Pandas to process, aggregate, and calculate nutritional data
and trends from the SQLite database.
"""

from typing import Dict, List, Optional, Any
import pandas as pd
import db


def get_user_nutrition_dataframe(user_id: int) -> pd.DataFrame:
    """Fetches all raw nutrition data for a user into a Pandas DataFrame."""
    conn = db.get_connection()
    query = """
        SELECT 
            m.meal_date,
            f.food_name,
            mi.quantity,
            mi.calories_consumed,
            (f.protein * mi.quantity) as protein,
            (f.carbohydrates * mi.quantity) as carbs,
            (f.fat * mi.quantity) as fat,
            (f.fiber * mi.quantity) as fiber,
            (f.sugar * mi.quantity) as sugar
        FROM Meals m
        JOIN MealItems mi ON m.meal_id = mi.meal_id
        JOIN Foods f ON mi.food_id = f.food_id
        WHERE m.user_id = ?
    """
    df = pd.read_sql_query(query, conn, params=(user_id,))
    conn.close()
    return df


def get_daily_summary(user_id: int, target_date: str) -> Dict[str, Any]:
    """Calculates macros, fiber, and sugar for a specific day using Pandas."""
    df = get_user_nutrition_dataframe(user_id)

    # Define our empty fallback template
    empty_response = {
        "total_calories": 0,
        "total_protein": 0.0,
        "total_carbs": 0.0,
        "total_fat": 0.0,
        "total_fiber": 0.0,
        "total_sugar": 0.0,
    }

    if df.empty:
        return empty_response

    daily_df = df[df["meal_date"] == target_date]
    if daily_df.empty:
        return empty_response

    # Sum all the columns including fiber and sugar
    summary = daily_df[
        ["calories_consumed", "protein", "carbs", "fat", "fiber", "sugar"]
    ].sum()

    return {
        "total_calories": int(summary["calories_consumed"]),
        "total_protein": round(float(summary["protein"]), 1),
        "total_carbs": round(float(summary["carbs"]), 1),
        "total_fat": round(float(summary["fat"]), 1),
        "total_fiber": round(float(summary["fiber"]), 1),
        "total_sugar": round(float(summary["sugar"]), 1),
    }


def aggregate_period_data(period_df: pd.DataFrame) -> Dict[str, Any]:
    """Takes a filtered DataFrame and calculates totals, averages, and daily trends."""
    empty_response = {
        "totals": {
            "calories": 0,
            "protein": 0.0,
            "carbs": 0.0,
            "fat": 0.0,
            "fiber": 0.0,
            "sugar": 0.0,
        },
        "averages": {
            "calories": 0,
            "protein": 0.0,
            "carbs": 0.0,
            "fat": 0.0,
            "fiber": 0.0,
            "sugar": 0.0,
        },
        "days_logged": 0,
        "daily_trends": [],
    }

    if period_df.empty:
        return empty_response

    # 1. Group by date first to get accurate DAILY sums
    daily_sums = (
        period_df.groupby("meal_date")[
            ["calories_consumed", "protein", "carbs", "fat", "fiber", "sugar"]
        ]
        .sum()
        .reset_index()
    )
    daily_sums = daily_sums.sort_values("meal_date")

    # 2. Calculate Totals for the entire period
    totals = daily_sums.sum(numeric_only=True)

    # 3. Calculate Averages (Mean of the daily sums)
    averages = daily_sums.mean(numeric_only=True)

    # 4. Format dates back to string for clean JSON output
    daily_sums["meal_date"] = daily_sums["meal_date"].dt.strftime("%Y-%m-%d")
    daily_trends = daily_sums.to_dict(orient="records")

    return {
        "totals": {
            "calories": int(totals["calories_consumed"]),
            "protein": round(float(totals["protein"]), 1),
            "carbs": round(float(totals["carbs"]), 1),
            "fat": round(float(totals["fat"]), 1),
            "fiber": round(float(totals["fiber"]), 1),
            "sugar": round(float(totals["sugar"]), 1),
        },
        "averages": {
            "calories": int(averages["calories_consumed"]),
            "protein": round(float(averages["protein"]), 1),
            "carbs": round(float(averages["carbs"]), 1),
            "fat": round(float(averages["fat"]), 1),
            "fiber": round(float(averages["fiber"]), 1),
            "sugar": round(float(averages["sugar"]), 1),
        },
        "days_logged": len(daily_sums),
        "daily_trends": daily_trends,  # We keep the breakdown so your charts still work!
    }


def get_period_analytics(
    user_id: int, period_type: str, reference_date_str: Optional[str] = None
) -> Dict[str, Any]:
    """Filters data by specific calendar or rolling windows and returns full aggregations."""
    df = get_user_nutrition_dataframe(user_id)
    if df.empty:
        return aggregate_period_data(df)

    # Convert dates to Pandas datetime objects for mathematical filtering
    df["meal_date"] = pd.to_datetime(df["meal_date"])

    if reference_date_str:
        ref_date = pd.to_datetime(reference_date_str)
    else:
        ref_date = pd.to_datetime("today").normalize()

    # Define the time window boundaries
    if period_type == "weekly":
        # Monday (0) to current reference date
        start_date = ref_date - pd.Timedelta(days=ref_date.weekday())
        end_date = ref_date
    elif period_type == "monthly":
        # 1st of the month to current reference date
        start_date = ref_date.replace(day=1)
        end_date = ref_date
    elif period_type == "last7days":
        # Rolling 7 days inclusive
        start_date = ref_date - pd.Timedelta(days=6)
        end_date = ref_date
    elif period_type == "last30days":
        # Rolling 30 days inclusive
        start_date = ref_date - pd.Timedelta(days=29)
        end_date = ref_date
    else:
        start_date = df["meal_date"].min()
        end_date = ref_date

    # Apply the date filter mask
    mask = (df["meal_date"] >= start_date) & (df["meal_date"] <= end_date)
    period_df = df.loc[mask].copy()

    return aggregate_period_data(period_df)


def get_top_foods(user_id: int) -> List[Dict[str, Any]]:
    """Finds the most frequently eaten foods using Pandas aggregations."""
    df = get_user_nutrition_dataframe(user_id)
    if df.empty:
        return []

    # Group by food name and calculate count and sum
    top_foods = (
        df.groupby("food_name")
        .agg(times_eaten=("food_name", "count"), total_portions=("quantity", "sum"))
        .reset_index()
    )

    # Sort by frequency, keep top 5
    top_foods = top_foods.sort_values(
        by=["times_eaten", "total_portions"], ascending=[False, False]
    ).head(5)

    # Round portions for clean JSON
    top_foods["total_portions"] = top_foods["total_portions"].round(1)

    return top_foods.to_dict(orient="records")
