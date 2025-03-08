import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import SmartDustbinPage from './pages/SmartDustbinPage';

const App = () => {
  return (
    <Router>
      <div className="app-container">
        {/* Page Routes */}
        <Routes>
          <Route path="/" element={<SmartDustbinPage />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
