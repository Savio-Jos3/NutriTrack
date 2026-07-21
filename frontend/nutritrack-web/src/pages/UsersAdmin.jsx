import { useState, useEffect } from 'react';
import { usersAPI } from '../api';

export default function UsersAdmin() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);

  // Form state for creating a new user
  const initialForm = {
    name: '', email: '', age: '', gender: 'Male', height: '', weight: '', daily_calorie_goal: 2000
  };
  const [formData, setFormData] = useState(initialForm);

  // 1. Fetch Users on Load
  useEffect(() => {
    loadUsers();
  }, []);

  const loadUsers = async () => {
    try {
      const data = await usersAPI.getAll();
      setUsers(data);
    } catch (error) {
      console.error("Failed to load users:", error);
    } finally {
      setLoading(false);
    }
  };

  // 2. Handle Form Changes
  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  // 3. Create a New User
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // Cast string inputs to numbers for the backend
      const payload = {
        ...formData,
        age: Number(formData.age),
        height: Number(formData.height),
        weight: Number(formData.weight),
        daily_calorie_goal: Number(formData.daily_calorie_goal)
      };
      
      await usersAPI.create(payload);
      setFormData(initialForm); // Reset form
      loadUsers(); // Refresh the list
    } catch (error) {
      alert("Failed to create user. Did you miss a field?");
      console.error(error);
    }
  };

  // 4. Delete a User
  const handleDelete = async (userId) => {
    if (!window.confirm("Are you sure you want to delete this user?")) return;
    try {
      await usersAPI.delete(userId);
      setUsers(users.filter(u => u.user_id !== userId));
    } catch (error) {
      console.error("Failed to delete user:", error);
    }
  };

  if (loading) return <h2>Loading Users...</h2>;

  return (
    <div>
      <h1 style={{ marginBottom: '1rem' }}>User Management</h1>

      {/* --- CREATE USER FORM --- */}
      <div style={{ background: 'white', padding: '1.5rem', borderRadius: '8px', border: '1px solid #e2e8f0', marginBottom: '2rem' }}>
        <h3 style={{ marginTop: 0 }}>Add New User</h3>
        <form onSubmit={handleSubmit} style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
          <input required name="name" placeholder="Name" value={formData.name} onChange={handleChange} style={{ padding: '0.5rem' }} />
          <input required name="email" type="email" placeholder="Email" value={formData.email} onChange={handleChange} style={{ padding: '0.5rem' }} />
          <input required name="age" type="number" placeholder="Age" value={formData.age} onChange={handleChange} style={{ padding: '0.5rem', width: '80px' }} />
          
          <select name="gender" value={formData.gender} onChange={handleChange} style={{ padding: '0.5rem' }}>
            <option value="Male">Male</option>
            <option value="Female">Female</option>
          </select>

          <input required name="height" type="number" step="0.1" placeholder="Height (cm)" value={formData.height} onChange={handleChange} style={{ padding: '0.5rem', width: '100px' }} />
          <input required name="weight" type="number" step="0.1" placeholder="Weight (kg)" value={formData.weight} onChange={handleChange} style={{ padding: '0.5rem', width: '100px' }} />
          <input required name="daily_calorie_goal" type="number" placeholder="Calorie Goal" value={formData.daily_calorie_goal} onChange={handleChange} style={{ padding: '0.5rem', width: '110px' }} />
          
          <button type="submit" style={{ padding: '0.5rem 1rem', background: '#3b82f6', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>
            Create User
          </button>
        </form>
      </div>

      {/* --- USERS LIST --- */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '1rem' }}>
        {users.map(user => (
          <div key={user.user_id} style={{ background: 'white', padding: '1.5rem', borderRadius: '8px', border: '1px solid #e2e8f0', position: 'relative' }}>
            <button 
              onClick={() => handleDelete(user.user_id)}
              style={{ position: 'absolute', top: '10px', right: '10px', background: '#ef4444', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer', padding: '4px 8px' }}
            >
              Delete
            </button>
            <h3 style={{ margin: '0 0 0.5rem 0' }}>{user.name}</h3>
            <p style={{ margin: '0 0 0.25rem 0', color: '#64748b' }}>{user.email}</p>
            <p style={{ margin: '0 0 0.25rem 0', fontSize: '0.9rem' }}>Age: {user.age} | {user.gender}</p>
            <p style={{ margin: '0 0 0.25rem 0', fontSize: '0.9rem' }}>Height: {user.height}cm | Weight: {user.weight}kg</p>
            <p style={{ margin: 0, fontWeight: 'bold', color: '#10b981' }}>Goal: {user.daily_calorie_goal} kcal</p>
          </div>
        ))}
      </div>
    </div>
  );
}