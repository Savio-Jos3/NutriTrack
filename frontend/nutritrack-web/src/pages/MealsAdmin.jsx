import { useState, useEffect } from 'react';
import { usersAPI, foodsAPI, mealsAPI } from '../api';

export default function MealsAdmin() {
  const [users, setUsers] = useState([]);
  const [foods, setFoods] = useState([]);
  
  // This state holds the meal we are currently editing
  const [activeMeal, setActiveMeal] = useState(null); 

  // Form states
  const [mealForm, setMealForm] = useState({
    user_id: '', meal_type: 'Breakfast', 
    meal_date: new Date().toISOString().split('T')[0], // Defaults to today
    meal_time: '08:00'
  });
  
  const [itemForm, setItemForm] = useState({ food_id: '', quantity: 1 });

  // Load Users and Foods for the dropdowns
  useEffect(() => {
    const loadDependencies = async () => {
      try {
        const [loadedUsers, loadedFoods] = await Promise.all([
          usersAPI.getAll(),
          foodsAPI.getAll()
        ]);
        setUsers(loadedUsers);
        setFoods(loadedFoods);
        
        // Set default dropdown values if data exists
        if (loadedUsers.length > 0) setMealForm(f => ({ ...f, user_id: loadedUsers[0].user_id }));
        if (loadedFoods.length > 0) setItemForm(f => ({ ...f, food_id: loadedFoods[0].food_id }));
      } catch (error) {
        console.error("Failed to load dependencies:", error);
      }
    };
    loadDependencies();
  }, []);

  // --- Step 1: Create the Meal Container ---
  const handleCreateMeal = async (e) => {
    e.preventDefault();
    try {
      const payload = { ...mealForm, user_id: Number(mealForm.user_id) };
      const response = await mealsAPI.create(payload);
      
      // Fetch the newly created meal details to activate the "Add Food" panel
      refreshActiveMeal(response.meal_id);
    } catch (error) {
      alert("Failed to create meal container.");
      console.error(error);
    }
  };

  // --- Step 2: Add Food to the Active Meal ---
  const handleAddFood = async (e) => {
    e.preventDefault();
    if (!activeMeal) return;
    
    try {
      const payload = { 
        food_id: Number(itemForm.food_id), 
        quantity: Number(itemForm.quantity) 
      };
      await mealsAPI.addItem(activeMeal.meal_id, payload);
      
      // Refresh the meal details to show updated macros
      refreshActiveMeal(activeMeal.meal_id);
    } catch (error) {
      alert("Failed to add food. Is it already in this meal?");
      console.error(error);
    }
  };

  const refreshActiveMeal = async (mealId) => {
    const details = await mealsAPI.getDetails(mealId);
    setActiveMeal(details);
  };

  return (
    <div>
      <h1 style={{ marginBottom: '1rem' }}>Meal Logger</h1>

      <div style={{ display: 'flex', gap: '2rem', alignItems: 'flex-start' }}>
        
        {/* LEFT COLUMN: Controls */}
        <div style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: '2rem' }}>
          
          {/* Create Meal Form */}
          <div style={{ background: 'white', padding: '1.5rem', borderRadius: '8px', border: '1px solid #e2e8f0', opacity: activeMeal ? 0.5 : 1 }}>
            <h3 style={{ marginTop: 0 }}>1. Create Meal Container</h3>
            <form onSubmit={handleCreateMeal} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              <select 
                value={mealForm.user_id} 
                onChange={e => setMealForm({...mealForm, user_id: e.target.value})}
                style={{ padding: '0.5rem' }} disabled={activeMeal}
              >
                {users.map(u => <option key={u.user_id} value={u.user_id}>{u.name}</option>)}
              </select>

              <div style={{ display: 'flex', gap: '1rem' }}>
                <select value={mealForm.meal_type} onChange={e => setMealForm({...mealForm, meal_type: e.target.value})} style={{ padding: '0.5rem', flex: 1 }} disabled={activeMeal}>
                  <option value="Breakfast">Breakfast</option>
                  <option value="Lunch">Lunch</option>
                  <option value="Snack">Snack</option>
                  <option value="Dinner">Dinner</option>
                </select>
                <input type="date" value={mealForm.meal_date} onChange={e => setMealForm({...mealForm, meal_date: e.target.value})} style={{ padding: '0.5rem' }} disabled={activeMeal} />
                <input type="time" value={mealForm.meal_time} onChange={e => setMealForm({...mealForm, meal_time: e.target.value})} style={{ padding: '0.5rem' }} disabled={activeMeal} />
              </div>

              <button type="submit" disabled={activeMeal} style={{ padding: '0.5rem', background: '#3b82f6', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>
                Start Meal
              </button>
            </form>
          </div>

          {/* Add Food Form (Only visible if a meal is active) */}
          {activeMeal && (
            <div style={{ background: 'white', padding: '1.5rem', borderRadius: '8px', border: '2px solid #3b82f6' }}>
              <h3 style={{ marginTop: 0 }}>2. Add Foods to {activeMeal.meal_type}</h3>
              <form onSubmit={handleAddFood} style={{ display: 'flex', gap: '1rem' }}>
                <select 
                  value={itemForm.food_id} 
                  onChange={e => setItemForm({...itemForm, food_id: e.target.value})}
                  style={{ padding: '0.5rem', flex: 1 }}
                >
                  {foods.map(f => <option key={f.food_id} value={f.food_id}>{f.food_name} ({f.serving_size})</option>)}
                </select>
                <input 
                  type="number" step="0.1" min="0.1" placeholder="Qty" 
                  value={itemForm.quantity} 
                  onChange={e => setItemForm({...itemForm, quantity: e.target.value})}
                  style={{ padding: '0.5rem', width: '80px' }} 
                />
                <button type="submit" style={{ padding: '0.5rem 1rem', background: '#10b981', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>
                  Add
                </button>
              </form>
              <button 
                onClick={() => setActiveMeal(null)} 
                style={{ marginTop: '1rem', width: '100%', padding: '0.5rem', background: '#64748b', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}
              >
                Done / Log Another Meal
              </button>
            </div>
          )}
        </div>

        {/* RIGHT COLUMN: Live Meal Receipt */}
        <div style={{ flex: 1, background: 'white', padding: '1.5rem', borderRadius: '8px', border: '1px solid #e2e8f0', minHeight: '400px' }}>
          <h3 style={{ marginTop: 0 }}>Meal Summary</h3>
          {!activeMeal ? (
            <p style={{ color: '#64748b' }}>Create a meal container to start logging.</p>
          ) : (
            <>
              <div style={{ padding: '1rem', background: '#f8fafc', borderRadius: '8px', marginBottom: '1rem' }}>
                <h2 style={{ margin: '0 0 0.5rem 0' }}>{activeMeal.total_calories} kcal</h2>
                <div style={{ display: 'flex', gap: '1rem', fontSize: '0.9rem' }}>
                  <span><strong>Pro:</strong> {activeMeal.total_protein}g</span>
                  <span><strong>Carb:</strong> {activeMeal.total_carbs}g</span>
                  <span><strong>Fat:</strong> {activeMeal.total_fat}g</span>
                </div>
              </div>

              <h4>Items Added:</h4>
              <ul style={{ listStyle: 'none', padding: 0, margin: 0 }}>
                {activeMeal.items?.length === 0 && <li style={{ color: '#64748b' }}>No foods added yet.</li>}
                {activeMeal.items?.map(item => (
                  <li key={item.food_id} style={{ display: 'flex', justifyContent: 'space-between', padding: '0.75rem 0', borderBottom: '1px solid #e2e8f0' }}>
                    <span>{item.quantity}x {item.food_name}</span>
                    <strong>{item.calories_consumed} kcal</strong>
                  </li>
                ))}
              </ul>
            </>
          )}
        </div>

      </div>
    </div>
  );
}