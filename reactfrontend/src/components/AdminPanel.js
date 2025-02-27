import React from 'react';
import AddHabitatForm from './AddHabitatForm';
import AddAnimalForm from './AddAnimalForm';

function AdminPanel() {
  return (
    <div className="admin-panel">
      <h1>Zoo Management System</h1>
      
      <div className="forms-container">
        <AddHabitatForm />
        <AddAnimalForm />
      </div>
    </div>
  );
}

export default AdminPanel;


