import { useState, useEffect } from 'react'
import { analyticsAPI } from './api'
import { Flame, Activity, Wheat, Droplet } from 'lucide-react'
import './App.css'

function App() {
  // All hooks must live right here, at the top of the function component
  const [dailyData, setDailyData] = useState(null)
  const [loading, setLoading] = useState(true)

  const USER_ID = 1;
  const TEST_DATE = "2026-07-21";

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const data = await analyticsAPI.getDaily(USER_ID, TEST_DATE);
        setDailyData(data);
      } catch (error) {
        console.error("Failed to fetch analytics:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  if (loading) return <div>Loading dashboard...</div>;
  if (!dailyData) return <div>No data found for this date.</div>;

  return (
    <div style={{ padding: '2rem', fontFamily: 'sans-serif' }}>
      <h1>NutriTrack Dashboard</h1>
      <p>Data for: {TEST_DATE}</p>

      <div style={{ display: 'flex', gap: '1rem', marginTop: '2rem' }}>
        <div style={{ border: '1px solid #ccc', padding: '1.5rem', borderRadius: '8px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#ef4444' }}>
            <Flame size={20} />
            <h3>Calories</h3>
          </div>
          <h2>{dailyData.total_calories} kcal</h2>
        </div>

        <div style={{ border: '1px solid #ccc', padding: '1.5rem', borderRadius: '8px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#3b82f6' }}>
            <Activity size={20} />
            <h3>Protein</h3>
          </div>
          <h2>{dailyData.total_protein} g</h2>
        </div>
      </div>
    </div>
  )
}

export default App