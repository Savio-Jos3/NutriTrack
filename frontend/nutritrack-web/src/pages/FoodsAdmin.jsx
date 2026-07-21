import { useState, useEffect } from 'react';
import { foodsAPI } from '../api';

export default function FoodsAdmin() {
  const [foods, setFoods] = useState([]);
  const [loading, setLoading] = useState(true);

  // Form state for creating a new food item
  const initialForm = {
    food_name: '', serving_size: '', calories: '', 
    protein: '', carbohydrates: '', fat: '', fiber: '', sugar: ''
  };
  const [formData, setFormData] = useState(initialForm);

  // 1. Fetch Foods on Load
  useEffect(() => {
    loadFoods();
  }, []);

  const loadFoods = async () => {
    try {
      const data = await foodsAPI.getAll();
      setFoods(data);
    } catch (error) {
      console.error("Failed to load foods:", error);
    } finally {
      setLoading(false);
    }
  };

  // 2. Handle Form Changes
  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  // 3. Create a New Food Item
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // Cast numeric fields for the database
      const payload = {
        ...formData,
        calories: Number(formData.calories),
        protein: Number(formData.protein),
        carbohydrates: Number(formData.carbohydrates),
        fat: Number(formData.fat),
        fiber: Number(formData.fiber),
        sugar: Number(formData.sugar)
      };
      
      await foodsAPI.create(payload);
      setFormData(initialForm); // Reset form
      loadFoods(); // Refresh the grid
    } catch (error) {
      alert("Failed to create food item.");
      console.error(error);
    }
  };

  // 4. Delete a Food Item
  const handleDelete = async (foodId) => {
    if (!window.confirm("Are you sure you want to delete this food item?")) return;
    try {
      await foodsAPI.delete(foodId);
      setFoods(foods.filter(f => f.food_id !== foodId));
    } catch (error) {
      console.error("Failed to delete food:", error);
    }
  };

  if (loading) return <h2>Loading Foods...</h2>;

  return (
    <div>
      <h1 style={{ marginBottom: '1rem' }}>Foods Database</h1>

      {/* --- CREATE FOOD FORM --- */}
      <div style={{ background: 'white', padding: '1.5rem', borderRadius: '8px', border: '1px solid #e2e8f0', marginBottom: '2rem' }}>
        <h3 style={{ marginTop: 0 }}>Add New Food</h3>
        <form onSubmit={handleSubmit} style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
          <input required name="food_name" placeholder="Food Name (e.g. Apple)" value={formData.food_name} onChange={handleChange} style={{ padding: '0.5rem', flex: '1 1 200px' }} />
          <input required name="serving_size" placeholder="Serving (e.g. 1 medium)" value={formData.serving_size} onChange={handleChange} style={{ padding: '0.5rem', flex: '1 1 150px' }} />
          
          <input required name="calories" type="number" placeholder="Calories" value={formData.calories} onChange={handleChange} style={{ padding: '0.5rem', width: '90px' }} />
          <input required name="protein" type="number" step="0.1" placeholder="Protein (g)" value={formData.protein} onChange={handleChange} style={{ padding: '0.5rem', width: '90px' }} />
          <input required name="carbohydrates" type="number" step="0.1" placeholder="Carbs (g)" value={formData.carbohydrates} onChange={handleChange} style={{ padding: '0.5rem', width: '90px' }} />
          <input required name="fat" type="number" step="0.1" placeholder="Fat (g)" value={formData.fat} onChange={handleChange} style={{ padding: '0.5rem', width: '90px' }} />
          <input required name="fiber" type="number" step="0.1" placeholder="Fiber (g)" value={formData.fiber} onChange={handleChange} style={{ padding: '0.5rem', width: '90px' }} />
          <input required name="sugar" type="number" step="0.1" placeholder="Sugar (g)" value={formData.sugar} onChange={handleChange} style={{ padding: '0.5rem', width: '90px' }} />
          
          <button type="submit" style={{ padding: '0.5rem 1rem', background: '#10b981', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>
            Add Food
          </button>
        </form>
      </div>

      {/* --- FOODS LIST --- */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: '1rem' }}>
        {foods.map(food => (
          <div key={food.food_id} style={{ background: 'white', padding: '1.5rem', borderRadius: '8px', border: '1px solid #e2e8f0', position: 'relative' }}>
            <button 
              onClick={() => handleDelete(food.food_id)}
              style={{ position: 'absolute', top: '10px', right: '10px', background: '#ef4444', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer', padding: '4px 8px' }}
            >
              Delete
            </button>
            <h3 style={{ margin: '0 0 0.25rem 0', paddingRight: '60px' }}>{food.food_name}</h3>
            <p style={{ margin: '0 0 1rem 0', color: '#64748b', fontSize: '0.9rem' }}>{food.serving_size}</p>
            
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.5rem', fontSize: '0.9rem' }}>
              <div><strong>🔥 Cals:</strong> {food.calories}</div>
              <div><strong>🥩 Pro:</strong> {food.protein}g</div>
              <div><strong>🍞 Carb:</strong> {food.carbohydrates}g</div>
              <div><strong>🥑 Fat:</strong> {food.fat}g</div>
              <div><strong>🌾 Fib:</strong> {food.fiber}g</div>
              <div><strong>🍬 Sug:</strong> {food.sugar}g</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}