import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { Menu } from 'lucide-react';
import './App.css';
import HomePage from './pages/HomePage';
import WasteDetectPage from './pages/WasteDetectPage';
import SmartDustbinPage from './pages/SmartDustbinPage';
import PlaceholderPage from './pages/PlaceholderPage';

const App = () => {
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <Router>
      <div className="app-container">
        {/* Menu Icon */}
        <div 
          className="menu-icon left" 
          onMouseEnter={() => setMenuOpen(true)} 
          onMouseLeave={() => setMenuOpen(false)}
        >
          <Menu size={32} />
          {menuOpen && (
            <div className="menu-bar left">
              <Link to="/" className="menu-link">Home</Link>
              <Link to="/waste-detect" className="menu-link">Waste Throwing Detect</Link>
              <Link to="/smart-dustbin" className="menu-link">Smart Dustbin</Link>
              <Link to="/automated-recycling" className="menu-link">Automated Recycling</Link>
            </div>
          )}
        </div>

        {/* Page Routes */}
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/waste-detect" element={<WasteDetectPage />} />
          <Route path="/smart-dustbin" element={<SmartDustbinPage />} />
          <Route path="/automated-recycling" element={<PlaceholderPage title="Automated Recycling" />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
