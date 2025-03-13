import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, Navigate } from 'react-router-dom';
import Login from './components/Login';
import EventLog from './components/EventLog';
import AddVisitorForm from './components/AddVisitorForm';
import ZooManager from './components/ZooManager';

import './App.css';

const App = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  const PrivateRoute = ({ element }) => {
    return isAuthenticated ? element : <Navigate to="/" />;
  };

  return (
    <Router>
      <div>
        <header>
          <nav>
            <Link to="/">Login</Link>
            <Link to="/register">Register</Link>
            <Link to="/zooManager">Zoo Manager</Link>
            <Link to="/eventlog">Event Log</Link>
          </nav>
        </header>

        <main>
          <Routes>
            <Route path="/" element={<Login setIsAuthenticated={setIsAuthenticated} />} />
            <Route path="/register" element={<AddVisitorForm />} />
            <Route path="/zooManager" element={<ZooManager />} />

            <Route path="/eventlog" element={<PrivateRoute element={<EventLog />} />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
};

export default App;
