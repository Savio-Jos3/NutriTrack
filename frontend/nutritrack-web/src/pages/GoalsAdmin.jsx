import { useState, useEffect } from 'react';
import { usersAPI, goalsAPI } from '../api';

export default function GoalsAdmin() {
  const [users, setUsers] = useState([]);
  const [selectedUserId, setSelectedUserId] = useState('');
  const [currentGoal, setCurrentGoal] = useState(null);

  // Form state
  const initialForm = {
    daily_calories: '', protein_goal: '', carbohydrate_goal: '', fat_goal: '', fiber_goal: ''
  };
  const [formData, setFormData] = useState(initialForm);

  // 1. Fetch Users on Load
  useEffect(() => {
    const loadUsers = async () => {
      try {
        const data = await usersAPI.getAll();
        setUsers(data);
        if (data.length > 0) setSelectedUserId(data[0].user_id.toString());
      } catch (error) {
        console.error("Failed to load users:", error);
      }
    };
    loadUsers();
  }, []);

  // 2. Fetch Goal whenever the selected user changes
  useEffect(() => {
    if (!selectedUserId) return;
    
    const loadGoal = async () => {
      try {
        const goalData = await goalsAPI.get(selectedUserId);
        setCurrentGoal(goalData);
        
        // Pre-fill the form with existing data
        setFormData({
          daily_calories: goalData.daily_calories || '',
          protein_goal: goalData.protein_goal || '',
          carbohydrate_goal: goalData.carbohydrate_goal || '',
          fat_goal: goalData.fat_goal || '',
          fiber_goal: goalData.fiber_goal || ''
        });
      } catch (error) {
        // A 404 error means they just don't have a goal yet
        setCurrentGoal(null);
        setFormData(initialForm);
      }
    };
    loadGoal();
  }, [selectedUserId]);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  // 3. Save (Create or Update) Goal
  const handleSave = async (e) => {
    e.preventDefault();
    const payload = {
      user_id: Number(selectedUserId),
      daily_calories: Number(formData.daily_calories),
      protein_goal: Number(formData.protein_goal),
      carbohydrate_goal: Number(formData.carbohydrate_goal),
      fat_goal: Number(formData.fat_goal),
      fiber_goal: Number(formData.fiber_goal)
    };

    try {
      if (currentGoal) {
        await goalsAPI.update(selectedUserId, payload);
        alert("Goal updated successfully!");
      } else {
        await goalsAPI.create(payload);
        alert("Goal created successfully!");
      }
      
      // Refresh the active goal state
      const updatedGoal = await goalsAPI.get(selectedUserId);
      setCurrentGoal(updatedGoal);
    } catch (error) {
      alert("Failed to save goal.");
      console.error(error);
    }
  };

  // 4. Delete Goal
  const handleDelete = async () => {
    if (!window.confirm("Are you sure you want to delete this user's nutrition goal?")) return;
    try {
      await goalsAPI.delete(selectedUserId);
      setCurrentGoal(null);
      setFormData(initialForm);
      alert("Goal deleted successfully!");
    } catch (error) {
      console.error("Failed to delete goal:", error);
    }
  };

  return (
    <div>
      <h1 style={{ marginBottom: '1rem' }}>Nutrition Goals</h1>

      {/* USER SELECTOR */}
      <div style={{ marginBottom: '2rem', padding: '1rem', background: 'white', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
        <label style={{ fontWeight: 'bold', marginRight: '1rem' }}>Select User:</label>
        <select 
          value={selectedUserId} 
          onChange={(e) => setSelectedUserId(e.target.value)}
          style={{ padding: '0.5rem', width: '300px' }}
        >
          {users.map(u => (
            <option key={u.user_id} value={u.user_id}>{u.name} (Goal: {u.daily_calorie_goal} kcal)</option>
          ))}
        </select>
      </div>

      <div style={{ display: 'flex', gap: '2rem' }}>
        
        {/* LEFT: FORM */}
        <div style={{ flex: 1, background: 'white', padding: '1.5rem', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
          <h3 style={{ marginTop: 0 }}>{currentGoal ? "Update Goal" : "Set New Goal"}</h3>
          <form onSubmit={handleSave} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            <div>
              <label style={{ display: 'block', fontSize: '0.9rem', marginBottom: '0.25rem', color: '#64748b' }}>Daily Calories</label>
              <input required name="daily_calories" type="number" value={formData.daily_calories} onChange={handleChange} style={{ padding: '0.5rem', width: '100%' }} />
            </div>
            <div style={{ display: 'flex', gap: '1rem' }}>
              <div style={{ flex: 1 }}>
                <label style={{ display: 'block', fontSize: '0.9rem', marginBottom: '0.25rem', color: '#64748b' }}>Protein (g)</label>
                <input required name="protein_goal" type="number" step="0.1" value={formData.protein_goal} onChange={handleChange} style={{ padding: '0.5rem', width: '100%' }} />
              </div>
              <div style={{ flex: 1 }}>
                <label style={{ display: 'block', fontSize: '0.9rem', marginBottom: '0.25rem', color: '#64748b' }}>Carbs (g)</label>
                <input required name="carbohydrate_goal" type="number" step="0.1" value={formData.carbohydrate_goal} onChange={handleChange} style={{ padding: '0.5rem', width: '100%' }} />
              </div>
            </div>
            <div style={{ display: 'flex', gap: '1rem' }}>
              <div style={{ flex: 1 }}>
                <label style={{ display: 'block', fontSize: '0.9rem', marginBottom: '0.25rem', color: '#64748b' }}>Fat (g)</label>
                <input required name="fat_goal" type="number" step="0.1" value={formData.fat_goal} onChange={handleChange} style={{ padding: '0.5rem', width: '100%' }} />
              </div>
              <div style={{ flex: 1 }}>
                <label style={{ display: 'block', fontSize: '0.9rem', marginBottom: '0.25rem', color: '#64748b' }}>Fiber (g)</label>
                <input required name="fiber_goal" type="number" step="0.1" value={formData.fiber_goal} onChange={handleChange} style={{ padding: '0.5rem', width: '100%' }} />
              </div>
            </div>
            <div style={{ display: 'flex', gap: '1rem', marginTop: '1rem' }}>
              <button type="submit" style={{ flex: 1, padding: '0.75rem', background: '#3b82f6', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>
                {currentGoal ? "Update Goal" : "Create Goal"}
              </button>
              {currentGoal && (
                <button type="button" onClick={handleDelete} style={{ flex: 1, padding: '0.75rem', background: '#ef4444', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>
                  Delete Goal
                </button>
              )}
            </div>
          </form>
        </div>

        {/* RIGHT: CURRENT ACTIVE GOAL SUMMARY */}
        <div style={{ flex: 1, background: '#f8fafc', padding: '1.5rem', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
          <h3 style={{ marginTop: 0 }}>Current Target</h3>
          {!currentGoal ? (
            <p style={{ color: '#64748b' }}>This user does not have a customized macro goal yet.</p>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              <div style={{ padding: '1rem', background: 'white', borderRadius: '8px', borderLeft: '4px solid #ef4444' }}>
                <strong style={{ color: '#64748b', fontSize: '0.9rem' }}>Calories</strong>
                <h2 style={{ margin: 0 }}>{currentGoal.daily_calories} kcal</h2>
              </div>
              <div style={{ display: 'flex', gap: '1rem' }}>
                <div style={{ flex: 1, padding: '1rem', background: 'white', borderRadius: '8px', borderLeft: '4px solid #3b82f6' }}>
                  <strong style={{ color: '#64748b', fontSize: '0.9rem' }}>Protein</strong>
                  <h3 style={{ margin: 0 }}>{currentGoal.protein_goal}g</h3>
                </div>
                <div style={{ flex: 1, padding: '1rem', background: 'white', borderRadius: '8px', borderLeft: '4px solid #eab308' }}>
                  <strong style={{ color: '#64748b', fontSize: '0.9rem' }}>Carbs</strong>
                  <h3 style={{ margin: 0 }}>{currentGoal.carbohydrate_goal}g</h3>
                </div>
              </div>
              <div style={{ display: 'flex', gap: '1rem' }}>
                <div style={{ flex: 1, padding: '1rem', background: 'white', borderRadius: '8px', borderLeft: '4px solid #f97316' }}>
                  <strong style={{ color: '#64748b', fontSize: '0.9rem' }}>Fat</strong>
                  <h3 style={{ margin: 0 }}>{currentGoal.fat_goal}g</h3>
                </div>
                <div style={{ flex: 1, padding: '1rem', background: 'white', borderRadius: '8px', borderLeft: '4px solid #10b981' }}>
                  <strong style={{ color: '#64748b', fontSize: '0.9rem' }}>Fiber</strong>
                  <h3 style={{ margin: 0 }}>{currentGoal.fiber_goal}g</h3>
                </div>
              </div>
            </div>
          )}
        </div>

      </div>
    </div>
  );
}