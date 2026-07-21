<div align="center">

# 🥗 NutriTrack
### *Full-Stack Nutrition Tracking & Analytics Platform*

<p align="center">
Track meals • Analyze nutrition • Visualize progress • Reach your health goals
</p>

<p align="center">

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-Backend-000000?style=for-the-badge&logo=flask)
![React](https://img.shields.io/badge/React-Frontend-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![Vite](https://img.shields.io/badge/Vite-Build-646CFF?style=for-the-badge&logo=vite&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite)
![Pandas](https://img.shields.io/badge/Pandas-Analytics-150458?style=for-the-badge&logo=pandas)

</p>

---

*A modern full-stack nutrition tracking platform built with **Flask**, **React**, **SQLite**, and **Pandas** that enables users to log meals, monitor macronutrients, manage nutrition goals, and gain actionable insights through interactive analytics dashboards.*

</div>

---

# ✨ Features

## 👤 User Management
- Create, update, and manage user profiles
- Store demographic information
- Set personalized calorie goals
- RESTful CRUD operations

## 🍎 Food Database
- Maintain a centralized food catalog
- Store complete macronutrient information
- Add custom food items
- Update and delete existing foods

## 🍽️ Meal Tracking
- Log Breakfast, Lunch, Dinner, and Snacks
- Add multiple food items per meal
- Automatic nutrition calculations
- Daily meal history

## 🎯 Nutrition Goals
- Personalized calorie targets
- Protein goals
- Carbohydrate goals
- Fat goals
- Fiber goals
- Goal management per user

## 📊 Advanced Analytics
Powered by **Pandas** for high-performance aggregations.

- Daily nutrition summaries
- Weekly rolling analytics
- Monthly nutrition trends
- Top consumed foods
- Macro breakdowns
- Time-series analysis

## 📈 Interactive Dashboard
- Responsive charts
- Beautiful visualizations
- Nutrition trend graphs
- Macro distribution charts
- Mobile-friendly interface

---

# 🏗️ Tech Stack

## Backend

| Technology | Purpose |
|------------|---------|
| 🐍 Python | Backend Language |
| ⚡ Flask | REST API Framework |
| 🗄️ SQLite | Database for Development|
| 🗄️ SQL | Database for Production |
| 🐼 Pandas | Analytics & Aggregations |
| 🧪 Pytest | Testing |
| 🧹 Black | Code Formatter |
| 🔍 Pylint | Code Quality |
| 🌐 Flask-CORS | Cross-Origin Requests |

---

## Frontend

| Technology | Purpose |
|------------|---------|
| ⚛️ React | UI Framework |
| ⚡ Vite | Build Tool |
| 🔀 React Router | Routing |
| 🌐 Axios | API Communication |
| 📊 Recharts | Data Visualization |
| 🎨 Lucide React | Icons |

---

# 📂 Project Structure

```text
NutriTrack/
│
├── backend/
│   ├── app.py
│   ├── db.py
│   ├── seed_data.py
│   ├── analytics/
│   ├── routes/
│   ├── tests/
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── charts/
│   ├── public/
│   └── package.json
│
└── README.md
```

---

# 🚀 Getting Started

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/NutriTrack.git

cd NutriTrack
```

---

# ⚙️ Backend Setup

Navigate to the backend directory.

```bash
cd backend
```

### Create Virtual Environment

```bash
python3 -m venv .venv
```

### Activate Virtual Environment

**Linux / macOS**

```bash
source .venv/bin/activate
```

**Windows**

```bash
.venv\Scripts\activate
```

### Install Dependencies

```bash
pip install flask flask-cors pandas python-dotenv black pylint pytest
```

---

## Initialize Database

```bash
python create_table.py
```

---

## Seed Sample Data

```bash
python seed_data.py
```

---

## Start Backend

```bash
python app.py
```

Backend runs at

```text
http://127.0.0.1:5001
```

---

# 💻 Frontend Setup

Open a new terminal.

```bash
cd frontend
```

Install dependencies.

```bash
npm install
```

Run the development server.

```bash
npm run dev
```

Frontend runs at

```text
http://localhost:5173
```

---

# 📚 API Reference

## Base URL

```text
http://localhost:5001
```

---

# 👤 Users API

Manage user profiles.

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | `/users` | Get all users |
| GET | `/users/<id>` | Get user by ID |
| POST | `/users` | Create user |
| PUT | `/users/<id>` | Update user |
| DELETE | `/users/<id>` | Delete user |

### Example Payload

```json
{
  "name": "Jane Doe",
  "email": "jane@example.com",
  "age": 30,
  "gender": "Female",
  "height": 165.0,
  "weight": 65.0,
  "daily_calorie_goal": 2000
}
```

---

# 🍎 Foods API

Manage food database.

| Method | Endpoint |
|---------|----------|
| GET | `/foods` |
| GET | `/foods/<id>` |
| POST | `/foods` |
| PUT | `/foods/<id>` |
| DELETE | `/foods/<id>` |

### Example Payload

```json
{
  "food_name": "Apple",
  "serving_size": "1 medium",
  "calories": 95,
  "protein": 0.5,
  "carbohydrates": 25.0,
  "fat": 0.3,
  "fiber": 4.4,
  "sugar": 19.0
}
```

---

# 🍽️ Meals API

Manage meals and meal items.

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/meals` | Create meal |
| POST | `/meals/<id>/items` | Add food to meal |
| GET | `/meals/<id>` | Meal details |
| GET | `/meals/daily` | Daily meals |

### Query Parameters

```text
?user_id=1&date=2026-07-21
```

### Create Meal

```json
{
  "user_id": 1,
  "meal_type": "Breakfast",
  "meal_date": "2026-07-21",
  "meal_time": "08:00:00"
}
```

### Add Food Item

```json
{
  "food_id": 42,
  "quantity": 1.5
}
```

---

# 🎯 Nutrition Goals API

Manage nutrition targets.

| Method | Endpoint |
|---------|----------|
| GET | `/goals/user/<user_id>` |
| POST | `/goals` |
| PUT | `/goals/user/<user_id>` |
| DELETE | `/goals/user/<user_id>` |

### Example Payload

```json
{
  "user_id": 1,
  "daily_calories": 2100,
  "protein_goal": 140.0,
  "carbohydrate_goal": 220.0,
  "fat_goal": 65.0,
  "fiber_goal": 25.0
}
```

---

# 📊 Analytics API

Powered by **Pandas** for efficient aggregations.

| Endpoint | Description |
|----------|-------------|
| `/analytics/daily` | Daily nutrition summary |
| `/analytics/weekly` | 7-day rolling analytics |
| `/analytics/monthly` | 30-day rolling analytics |
| `/analytics/top-foods` | Top 5 consumed foods |

### Required Query Parameters

```text
user_id=<id>
date=<YYYY-MM-DD>
```

Example

```text
/analytics/daily?user_id=1&date=2026-07-21
```

---

# 📈 Analytics Capabilities

- 📅 Daily calorie tracking
- 📊 Weekly nutrition trends
- 📈 Monthly progress reports
- 🥩 Macronutrient breakdowns
- 🍎 Most consumed foods
- 🔥 Rolling averages
- 📉 Time-series aggregations
- 🎯 Goal comparison

---

# 🧪 Testing

Run all tests.

```bash
pytest
```

Code formatting.

```bash
black .
```

Linting.

```bash
pylint .
```

---

# 🌟 Highlights

- ⚡ Full Stack Architecture
- 📊 Interactive Analytics Dashboard
- 🐼 Pandas-Powered Data Processing
- ⚛️ Modern React UI
- 📱 Responsive Design
- 🗄️ SQLite Database
- 🔥 RESTful API
- 🎯 Nutrition Goal Tracking
- 📈 Beautiful Charts with Recharts
- 🧪 Automated Testing

---

<div align="center">

### 🥗 Eat Better • Track Smarter • Live Healthier

**Built with ❤️ using Flask, React, SQLite & Pandas**

⭐ If you found this project useful, consider giving it a star!

</div>