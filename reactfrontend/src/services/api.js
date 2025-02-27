import axios from 'axios';

const API_URL = 'http://localhost:8000/';

export const getHabitats = async () => {
  try {
    const response = await axios.get(`${API_URL}habitats/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching habitats:', error);
    throw error.response ? error.response.data : error;
  }
};

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

export const updateHabitat = async (habitatData) => {
  try {
    const params = new URLSearchParams();
    params.append('name', habitatData.name);
    
    if (habitatData.new_name) {
      params.append('new_name', habitatData.new_name);
    }
    if (habitatData.size) {
      params.append('size', habitatData.size);
    }
    if (habitatData.climate) {
      params.append('climate', habitatData.climate);
    }
    
    const response = await axios.get(`${API_URL}habitats/update/?${params.toString()}`);
    return response.data;
  } catch (error) {
    console.error('Error updating habitat:', error);
    throw error.response ? error.response.data : error;
  }
};

export const deleteHabitat = async (name) => {
  try {
    const params = new URLSearchParams();
    params.append('name', name);
    
    const response = await axios.get(`${API_URL}habitats/delete/?${params.toString()}`);
    return response.data;
  } catch (error) {
    console.error('Error deleting habitat:', error);
    throw error.response ? error.response.data : error;
  }
};

export const getHabitatDetail = async (name) => {
  try {
    const response = await axios.get(`${API_URL}habitats/${name}/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching habitat details:', error);
    throw error.response ? error.response.data : error;
  }
};

export const getAnimals = async () => {
  try {
    const response = await axios.get(`${API_URL}animals/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching animals:', error);
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
    
    if (animalData.habitats && animalData.habitats.length > 0) {
      params.append('habitats', animalData.habitats.join(','));
    }
    
    const response = await axios.get(`${API_URL}animals/add/?${params.toString()}`);
    return response.data;
  } catch (error) {
    console.error('Error adding animal:', error);
    throw error.response ? error.response.data : error;
  }
};

export const updateAnimal = async (animalData) => {
  try {
    const params = new URLSearchParams();
    params.append('species', animalData.species);
    
    if (animalData.new_species) {
      params.append('new_species', animalData.new_species);
    }
    if (animalData.diet) {
      params.append('diet', animalData.diet);
    }
    if (animalData.lifespan) {
      params.append('lifespan', animalData.lifespan);
    }
    if (animalData.behaviour) {
      params.append('behaviour', animalData.behaviour);
    }
    if (animalData.habitats && animalData.habitats.length > 0) {
      params.append('habitats', animalData.habitats.join(','));
    }
    
    const response = await axios.get(`${API_URL}animals/update/?${params.toString()}`);
    return response.data;
  } catch (error) {
    console.error('Error updating animal:', error);
    throw error.response ? error.response.data : error;
  }
};

export const deleteAnimal = async (species) => {
  try {
    const params = new URLSearchParams();
    params.append('species', species);
    
    const response = await axios.get(`${API_URL}animals/delete/?${params.toString()}`);
    return response.data;
  } catch (error) {
    console.error('Error deleting animal:', error);
    throw error.response ? error.response.data : error;
  }
};

export const getAnimalDetail = async (species) => {
  try {
    const response = await axios.get(`${API_URL}animals/${species}/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching animal details:', error);
    throw error.response ? error.response.data : error;
  }
};


