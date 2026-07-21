import { useState, useEffect } from 'react';
import { analyticsAPI, mealsAPI } from '../api';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, BarChart, Bar } from 'recharts';
import { Flame, Activity, Wheat, Droplet, Leaf, Cookie } from 'lucide-react';

export default function Dashboard() {
  // Master State
  const [loading, setLoading] = useState(true);
  const [dailyData, setDailyData] = useState(null);
  const [dailyMeals, setDailyMeals] = useState([]);
  const [trendData, setTrendData] = useState(null);
  const [topFoods, setTopFoods] = useState([]);

  // Controls
  const [userId, setUserId] = useState(1); // Default User
  const [targetDate, setTargetDate] = useState("2026-07-21"); // Default Date
  const [trendPeriod, setTrendPeriod] = useState('weekly'); // 'weekly' or 'monthly'

  useEffect(() => {
    const fetchAllDashboardData = async () => {
      setLoading(true);
      try {
        // Run all API calls in parallel for maximum speed
        const [daily, meals, trends, foods] = await Promise.all([
          analyticsAPI.getDaily(userId, targetDate),
          mealsAPI.getDailyMeals(userId, targetDate),
          trendPeriod === 'weekly' 
            ? analyticsAPI.getWeekly(userId, targetDate) 
            : analyticsAPI.getMonthly(userId, targetDate),
          analyticsAPI.getTopFoods(userId)
        ]);

        setDailyData(daily);
        setDailyMeals(meals);
        setTrendData(trends);
        setTopFoods(foods);
      } catch (error) {
        console.error("Failed to load dashboard data:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchAllDashboardData();
  }, [userId, targetDate, trendPeriod]);

  if (loading) return <h2>Loading Comprehensive Dashboard...</h2>;

  return (
    <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
      
      {/* HEADER & CONTROLS */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
        <div>
          <h1 style={{ margin: '0 0 0.5rem 0' }}>Analytics Dashboard</h1>
          <p style={{ margin: 0, color: '#64748b' }}>Comprehensive overview of your nutrition.</p>
        </div>
        <div style={{ display: 'flex', gap: '1rem', background: 'white', padding: '1rem', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
          <div>
            <label style={{ fontSize: '0.8rem', color: '#64748b', display: 'block' }}>User ID</label>
            <input type="number" value={userId} onChange={e => setUserId(e.target.value)} style={{ padding: '0.5rem', width: '80px' }} />
          </div>
          <div>
            <label style={{ fontSize: '0.8rem', color: '#64748b', display: 'block' }}>Date</label>
            <input type="date" value={targetDate} onChange={e => setTargetDate(e.target.value)} style={{ padding: '0.5rem' }} />
          </div>
        </div>
      </div>

      {/* 1. DAILY MACROS */}
      <h2 style={{ borderBottom: '2px solid #e2e8f0', paddingBottom: '0.5rem' }}>1. Daily Macros ({targetDate})</h2>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))', gap: '1rem', marginBottom: '2rem' }}>
        
        <div style={{ background: 'white', padding: '1.5rem', borderRadius: '8px', border: '1px solid #fca5a5' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#ef4444', marginBottom: '0.5rem' }}>
            <Flame size={20} /> <strong>Calories</strong>
          </div>
          <h2 style={{ margin: 0 }}>{dailyData?.total_calories || 0} kcal</h2>
        </div>

        <div style={{ background: 'white', padding: '1.5rem', borderRadius: '8px', border: '1px solid #93c5fd' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#3b82f6', marginBottom: '0.5rem' }}>
            <Activity size={20} /> <strong>Protein</strong>
          </div>
          <h2 style={{ margin: 0 }}>{dailyData?.total_protein || 0} g</h2>
        </div>

        <div style={{ background: 'white', padding: '1.5rem', borderRadius: '8px', border: '1px solid #fde047' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#eab308', marginBottom: '0.5rem' }}>
            <Wheat size={20} /> <strong>Carbs</strong>
          </div>
          <h2 style={{ margin: 0 }}>{dailyData?.total_carbs || 0} g</h2>
        </div>

        <div style={{ background: 'white', padding: '1.5rem', borderRadius: '8px', border: '1px solid #fdba74' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#f97316', marginBottom: '0.5rem' }}>
            <Droplet size={20} /> <strong>Fat</strong>
          </div>
          <h2 style={{ margin: 0 }}>{dailyData?.total_fat || 0} g</h2>
        </div>

        <div style={{ background: 'white', padding: '1.5rem', borderRadius: '8px', border: '1px solid #86efac' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#22c55e', marginBottom: '0.5rem' }}>
            <Leaf size={20} /> <strong>Fiber</strong>
          </div>
          <h2 style={{ margin: 0 }}>{dailyData?.total_fiber || 0} g</h2>
        </div>

        <div style={{ background: 'white', padding: '1.5rem', borderRadius: '8px', border: '1px solid #d8b4fe' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#a855f7', marginBottom: '0.5rem' }}>
            <Cookie size={20} /> <strong>Sugar</strong>
          </div>
          <h2 style={{ margin: 0 }}>{dailyData?.total_sugar || 0} g</h2>
        </div>

      </div>

      {/* 2. TODAY'S MEAL LOG */}
      <h2 style={{ borderBottom: '2px solid #e2e8f0', paddingBottom: '0.5rem' }}>2. Meals Consumed Today</h2>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '1rem', marginBottom: '3rem' }}>
        {dailyMeals.length === 0 ? (
          <p style={{ color: '#64748b' }}>No meals logged for this date.</p>
        ) : (
          dailyMeals.map(meal => (
            <div key={meal.meal_id} style={{ background: 'white', padding: '1.5rem', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid #e2e8f0', paddingBottom: '0.5rem', marginBottom: '1rem' }}>
                <h3 style={{ margin: 0, color: '#334155' }}>{meal.meal_type}</h3>
                <span style={{ color: '#64748b' }}>{meal.meal_time}</span>
              </div>
              <ul style={{ listStyle: 'none', padding: 0, margin: 0 }}>
                {meal.items.map((item, idx) => (
                  <li key={idx} style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem', fontSize: '0.95rem' }}>
                    <span>{item.quantity}x {item.food_name}</span>
                    <strong style={{ color: '#ef4444' }}>{item.calories_consumed} kcal</strong>
                  </li>
                ))}
              </ul>
            </div>
          ))
        )}
      </div>

      <div style={{ display: 'flex', gap: '2rem' }}>
        
        {/* 3. TRENDS GRAPH (Left Side) */}
        <div style={{ flex: 2 }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end', borderBottom: '2px solid #e2e8f0', paddingBottom: '0.5rem', marginBottom: '1rem' }}>
            <h2 style={{ margin: 0 }}>3. Calorie Trends</h2>
            <select value={trendPeriod} onChange={e => setTrendPeriod(e.target.value)} style={{ padding: '0.5rem' }}>
              <option value="weekly">Last 7 Days</option>
              <option value="monthly">Last 30 Days</option>
            </select>
          </div>
          
          <div style={{ height: '350px', background: 'white', padding: '1rem', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
            {trendData && trendData.daily_trends.length > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={trendData.daily_trends} margin={{ top: 5, right: 20, left: 0, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} />
                  <XAxis dataKey="meal_date" tick={{fontSize: 12}} />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Line type="monotone" dataKey="calories_consumed" name="Calories" stroke="#ef4444" strokeWidth={3} activeDot={{ r: 8 }} />
                  <Line type="monotone" dataKey="protein" name="Protein (g)" stroke="#3b82f6" strokeWidth={3} />
                </LineChart>
              </ResponsiveContainer>
            ) : (
              <div style={{ height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#64748b' }}>
                No trend data available for this period.
              </div>
            )}
          </div>
        </div>

        {/* 4. TOP FOODS (Right Side) */}
        <div style={{ flex: 1 }}>
          <h2 style={{ borderBottom: '2px solid #e2e8f0', paddingBottom: '0.5rem', marginBottom: '1rem' }}>4. Top Foods</h2>
          <div style={{ background: 'white', padding: '1.5rem', borderRadius: '8px', border: '1px solid #e2e8f0', height: '350px', overflowY: 'auto' }}>
            {topFoods.length === 0 ? (
              <p style={{ color: '#64748b' }}>No foods logged yet.</p>
            ) : (
              <ul style={{ listStyle: 'none', padding: 0, margin: 0 }}>
                {topFoods.map((food, idx) => (
                  <li key={idx} style={{ padding: '1rem 0', borderBottom: '1px solid #f1f5f9' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                      <div style={{ width: '30px', height: '30px', background: '#3b82f6', color: 'white', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 'bold' }}>
                        {idx + 1}
                      </div>
                      <div style={{ flex: 1 }}>
                        <h4 style={{ margin: '0 0 0.25rem 0' }}>{food.food_name}</h4>
                        <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem', color: '#64748b' }}>
                          <span>Eaten <strong>{food.times_eaten}</strong> times</span>
                          <span><strong>{food.total_portions}</strong> total portions</span>
                        </div>
                      </div>
                    </div>
                  </li>
                ))}
              </ul>
            )}
          </div>
        </div>

      </div>

    </div>
  );
}