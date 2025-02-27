import axios from 'axios';

const API_URL = 'http://localhost:8000/';

export const addHabitat = async (habitatData) => {
  try {
    const params = new URLSearchParams();
    params.append('name', habitatData.name);
    params.append('size', habitatData.size);
    params.append('climate', habitatData.climate);
    
    const response = await axios.get(`${API_URL}habitats/add/?${params.toString()}`);
    return response.data;
  } catch (error) {
    console.error('Error adding habitat:', error);
    throw error.response ? error.response.data : error;
  }
};

export const addAnimal = async (animalData) => {
  try {
    const params = new URLSearchParams();
    params.append('species', animalData.species);
    params.append('diet', animalData.diet);
    params.append('lifespan', animalData.lifespan);
    params.append('behaviour', animalData.behaviour);
    
    if (animalData.habitats) {
      params.append('habitats', animalData.habitats.join(','));
    }
    
    const response = await axios.get(`${API_URL}animals/add/?${params.toString()}`);
    return response.data;
  } catch (error) {
    console.error('Error adding animal:', error);
    throw error.response ? error.response.data : error;
  }
};

export const getHabitats = async () => {
  try {
    const response = await axios.get(`${API_URL}habitats/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching habitats:', error);
    throw error;
  }
};

