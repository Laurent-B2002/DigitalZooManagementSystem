import React, { useState, useEffect } from 'react';
import { addAnimal, getHabitats, getSpecies } from '../services/api';

function AddAnimalForm() {
  const [formData, setFormData] = useState({
    name: '',
    species: '',
    diet: '',
    lifespan: '',
    behaviour: '',
    habitats: []
  });
  const [availableHabitats, setAvailableHabitats] = useState([]);
  const [availableSpecies, setAvailableSpecies] = useState([]);
  const [message, setMessage] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [dataLoading, setDataLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Fetch both habitats and species in parallel
        const [habitats, species] = await Promise.all([
          getHabitats(),
          getSpecies()
        ]);
        
        setAvailableHabitats(habitats);
        setAvailableSpecies(species);
      } catch (err) {
        setError('Failed to load data');
      } finally {
        setDataLoading(false);
      }
    };
    
    fetchData();
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };

  const handleHabitatChange = (e) => {
    const options = e.target.options;
    const selectedValues = [];
    for (let i = 0; i < options.length; i++) {
      if (options[i].selected) {
        selectedValues.push(options[i].value);
      }
    }
    
    setFormData({
      ...formData,
      habitats: selectedValues
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setMessage(null);
    
    try {
      const response = await addAnimal(formData);
      setMessage(response.message);
      setFormData({
        name: '',
        species: '',
        diet: '',
        lifespan: '',
        behaviour: '',
        habitats: []
      });
    } catch (err) {
      setError(err.error || 'An unexpected error occurred');
    } finally {
      setLoading(false);
    }
  };

  if (dataLoading) return <p>Loading data...</p>;

  return (
    <div className="form-container">
      <h2>Add New Animal</h2>
      
      {message && <div className="success-message">{message}</div>}
      {error && <div className="error-message">{error}</div>}
      
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="name">Name:</label>
          <input
            type="text"
            id="name"
            name="name"
            value={formData.name}
            onChange={handleChange}
            required
          />
        </div>
        
        <div className="form-group">
          <label htmlFor="species">Species:</label>
          <select
            id="species"
            name="species"
            value={formData.species}
            onChange={handleChange}
            required
          >
            <option value="">Select a species</option>
            {availableSpecies.map(species => (
              <option key={species.id} value={species.name}>
                {species.name}
              </option>
            ))}
          </select>
        </div>
        
        <div className="form-group">
          <label htmlFor="diet">Diet:</label>
          <input
            type="text"
            id="diet"
            name="diet"
            value={formData.diet}
            onChange={handleChange}
            required
          />
        </div>
        
        <div className="form-group">
          <label htmlFor="lifespan">Lifespan (years):</label>
          <input
            type="number"
            id="lifespan"
            name="lifespan"
            min="1"
            value={formData.lifespan}
            onChange={handleChange}
            required
          />
        </div>
        
        <div className="form-group">
          <label htmlFor="behaviour">Behaviour:</label>
          <textarea
            id="behaviour"
            name="behaviour"
            value={formData.behaviour}
            onChange={handleChange}
            required
          />
        </div>
        
        <div className="form-group">
          <label htmlFor="habitats">Habitats:</label>
          <select
            id="habitats"
            name="habitats"
            multiple
            value={formData.habitats}
            onChange={handleHabitatChange}
          >
            {availableHabitats.map(habitat => (
              <option key={habitat.id} value={habitat.name}>
                {habitat.name}
              </option>
            ))}
          </select>
          <small>Hold Ctrl (or Cmd on Mac) to select multiple habitats</small>
        </div>
        
        <button type="submit" disabled={loading}>
          {loading ? 'Adding...' : 'Add Animal'}
        </button>
      </form>
    </div>
  );
}

export default AddAnimalForm;

