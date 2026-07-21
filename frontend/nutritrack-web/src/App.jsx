import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import './App.css';
import UsersAdmin from './pages/UsersAdmin';
import FoodsAdmin from './pages/FoodsAdmin';
import MealsAdmin from './pages/MealsAdmin'; 
import GoalsAdmin from './pages/GoalsAdmin';

function App() {
  return (
    <BrowserRouter>
      <div style={{ display: 'flex', minHeight: '100vh', fontFamily: 'sans-serif' }}>
        
        {/* Sidebar Navigation */}
        <nav style={{ width: '250px', background: '#1e293b', color: 'white', padding: '2rem' }}>
          <h2 style={{ marginTop: 0, marginBottom: '2rem', color: '#38bdf8' }}>NutriTrack</h2>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            <Link to="/" style={{ color: 'white', textDecoration: 'none', fontSize: '1.1rem' }}>📊 Dashboard</Link>
            <Link to="/users" style={{ color: 'white', textDecoration: 'none', fontSize: '1.1rem' }}>👥 Users</Link>
            <Link to="/foods" style={{ color: 'white', textDecoration: 'none', fontSize: '1.1rem' }}>🍎 Foods</Link>
            <Link to="/meals" style={{ color: 'white', textDecoration: 'none', fontSize: '1.1rem' }}>🍽️ Meals & Goals</Link>
            <Link to="/goals" style={{ color: 'white', textDecoration: 'none', fontSize: '1.1rem' }}>🎯 Goals</Link>
          </div>
        </nav>

        {/* Main Content Area */}
        <main style={{ flex: 1, padding: '2rem', background: '#f1f5f9' }}>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/users" element={<UsersAdmin />} />
            <Route path="/foods" element={<FoodsAdmin />} />
            <Route path="/meals" element={<MealsAdmin />} />
            <Route path="/goals" element={<GoalsAdmin />} />
          </Routes>
        </main>

      </div>
    </BrowserRouter>
  );
}

export default App;