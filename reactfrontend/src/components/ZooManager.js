import React, { useState } from 'react';
import { AnimalList } from './AnimalList';
import { HabitatList } from './HabitatList';
import AddAnimalForm from './AddAnimalForm';
import AddHabitatForm from './AddHabitatForm';
import UpdateAnimalForm from './UpdateAnimalForm';
import UpdateHabitatForm from './UpdateHabitatForm';
import { DeleteAnimalForm } from './DeleteAnimalForm';
import { DeleteHabitatForm } from './DeleteHabitatForm';
import ZookeeperList from './ZookeeperList';
import AddZookeeperForm from './AddZookeeperForm';
import UpdateZookeeperForm from './UpdateZookeeperForm';
import DeleteZookeeperForm from './DeleteZookeeperForm';

function ZooManager() {
  const [activeTab, setActiveTab] = useState('viewAnimals');
  const [refreshKey, setRefreshKey] = useState(0);

  const refreshData = () => {
    setRefreshKey(prevKey => prevKey + 1);
  };

  return (
    <div className="zoo-manager">
      <h1>Zoo Management System</h1>
      
      <div className="tabs">
        <div className="tab-group">
          <h3>View Data</h3>
          <button 
            className={activeTab === 'viewAnimals' ? 'active' : ''} 
            onClick={() => setActiveTab('viewAnimals')}
          >
            View Animals
          </button>
          <button 
            className={activeTab === 'viewHabitats' ? 'active' : ''} 
            onClick={() => setActiveTab('viewHabitats')}
          >
            View Habitats
          </button>
          <button 
            className={activeTab === 'viewZookeepers' ? 'active' : ''} 
            onClick={() => setActiveTab('viewZookeepers')}
          >
            View Zookeepers
          </button>
        </div>
        
        <div className="tab-group">
          <h3>Add Data</h3>
          <button 
            className={activeTab === 'addAnimal' ? 'active' : ''} 
            onClick={() => setActiveTab('addAnimal')}
          >
            Add Animal
          </button>
          <button 
            className={activeTab === 'addHabitat' ? 'active' : ''} 
            onClick={() => setActiveTab('addHabitat')}
          >
            Add Habitat
          </button>
          <button 
            className={activeTab === 'addZookeeper' ? 'active' : ''}
            onClick={() => setActiveTab('addZookeeper')}
          >
            Add Zookeeper
          </button>
        </div>
        
        <div className="tab-group">
          <h3>Update Data</h3>
          <button 
            className={activeTab === 'updateAnimal' ? 'active' : ''} 
            onClick={() => setActiveTab('updateAnimal')}
          >
            Update Animal
          </button>
          <button 
            className={activeTab === 'updateHabitat' ? 'active' : ''} 
            onClick={() => setActiveTab('updateHabitat')}
          >
            Update Habitat
          </button>
          <button 
            className={activeTab === 'updateZookeeper' ? 'active' : ''} 
            onClick={() => setActiveTab('updateZookeeper')}
          >
            Update Zookeeper
          </button>
        </div>
        
        <div className="tab-group">
          <h3>Delete Data</h3>
          <button 
            className={activeTab === 'deleteAnimal' ? 'active' : ''} 
            onClick={() => setActiveTab('deleteAnimal')}
          >
            Delete Animal
          </button>
          <button 
            className={activeTab === 'deleteHabitat' ? 'active' : ''} 
            onClick={() => setActiveTab('deleteHabitat')}
          >
            Delete Habitat
          </button>
          <button 
            className={activeTab === 'deleteZookeeper' ? 'active' : ''} 
            onClick={() => setActiveTab('deleteZookeeper')}
          >
            Delete Zookeeper
          </button>
        </div>
      </div>
      
      <div className="tab-content">
        {/* View Components */}
        {activeTab === 'viewAnimals' && <AnimalList key={`animals-${refreshKey}`} />}
        {activeTab === 'viewHabitats' && <HabitatList key={`habitats-${refreshKey}`} />}
        {activeTab === 'viewZookeepers' && <ZookeeperList key={`zookeepers-${refreshKey}`} />}
        
        {/* Add Components */}
        {activeTab === 'addAnimal' && (
          <AddAnimalForm onAnimalAdded={() => {
            refreshData();
            alert("Animal added successfully! View the updated list in the View Animals tab.");
          }} />
        )}
        {activeTab === 'addHabitat' && (
          <AddHabitatForm onHabitatAdded={() => {
            refreshData();
            alert("Habitat added successfully! View the updated list in the View Habitats tab.");
          }} />
        )}
        {activeTab === 'addZookeeper' && (
          <AddZookeeperForm onZookeeperAdded={() => {
            refreshData();
            alert("Zookeeper added successfully! View the updated list in the View Zookeepers tab.");
          }} />
        )}
        
        {/* Update Components */}
        {activeTab === 'updateAnimal' && (
          <UpdateAnimalForm onAnimalUpdated={() => {
            refreshData();
          }} />
        )}
        {activeTab === 'updateHabitat' && (
          <UpdateHabitatForm onHabitatUpdated={() => {
            refreshData();
          }} />
        )}
        {activeTab === 'updateZookeeper' && (
          <UpdateZookeeperForm onZookeeperUpdated={() => {
            refreshData();
          }} />
        )}
        
        {/* Delete Components */}
        {activeTab === 'deleteAnimal' && (
          <DeleteAnimalForm onAnimalDeleted={() => {
            refreshData();
          }} />
        )}
        {activeTab === 'deleteHabitat' && (
          <DeleteHabitatForm onHabitatDeleted={() => {
            refreshData();
          }} />
        )}
        {activeTab === 'deleteZookeeper' && (
          <DeleteZookeeperForm onZookeeperDeleted={() => {
            refreshData();
          }} />
        )}
      </div>
    </div>
  );
}

export default ZooManager;
