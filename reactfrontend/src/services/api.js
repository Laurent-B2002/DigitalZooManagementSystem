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

export const getSpecies = async () => {
  try {
    const response = await axios.get(`${API_URL}species/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching species:', error);
    throw error.response ? error.response.data : error;
  }
};

export const addSpecies = async (speciesData) => {
  try {
    const params = new URLSearchParams();
    params.append('name', speciesData.name);
    
    const response = await axios.get(`${API_URL}species/add/?${params.toString()}`);
    return response.data;
  } catch (error) {
    console.error('Error adding species:', error);
    throw error.response ? error.response.data : error;
  }
};

export const updateSpecies = async (speciesData) => {
  try {
    const params = new URLSearchParams();
    params.append('name', speciesData.name);
    params.append('new_name', speciesData.new_name);
    
    const response = await axios.get(`${API_URL}species/update/?${params.toString()}`);
    return response.data;
  } catch (error) {
    console.error('Error updating species:', error);
    throw error.response ? error.response.data : error;
  }
};

export const deleteSpecies = async (name) => {
  try {
    const params = new URLSearchParams();
    params.append('name', name);
    
    const response = await axios.get(`${API_URL}species/delete/?${params.toString()}`);
    return response.data;
  } catch (error) {
    console.error('Error deleting species:', error);
    throw error.response ? error.response.data : error;
  }
};

export const getSpeciesDetail = async (name) => {
  try {
    const response = await axios.get(`${API_URL}species/${name}/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching species details:', error);
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
    params.append('name', animalData.name);
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
    params.append('name', animalData.name);
    
    if (animalData.new_name) {
      params.append('new_name', animalData.new_name);
    }
    if (animalData.species) {
      params.append('species', animalData.species);
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

export const deleteAnimal = async (name) => {
  try {
    const params = new URLSearchParams();
    params.append('name', name);
    
    const response = await axios.get(`${API_URL}animals/delete/?${params.toString()}`);
    return response.data;
  } catch (error) {
    console.error('Error deleting animal:', error);
    throw error.response ? error.response.data : error;
  }
};

export const getAnimalDetail = async (name) => {
  try {
    const response = await axios.get(`${API_URL}animals/${name}/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching animal details:', error);
    throw error.response ? error.response.data : error;
  }
};

export const getZookeepers = async () => {
  try {
    const response = await axios.get(`${API_URL}zookeepers/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching zookeepers:', error);
    throw error.response ? error.response.data : error;
  }
};

export const addZookeeper = async (zookeeperData) => {
  try {
    const params = new URLSearchParams();
    params.append('name', zookeeperData.name);
    params.append('qualification', zookeeperData.qualification);
    params.append('responsibilities', zookeeperData.responsibilities);
    
    const response = await axios.get(`${API_URL}zookeepers/add/?${params.toString()}`);
    return response.data;
  } catch (error) {
    console.error('Error adding zookeeper:', error);
    throw error.response ? error.response.data : error;
  }
};

export const updateZookeeper = async (zookeeperData) => {
  try {
    const params = new URLSearchParams();
    params.append('name', zookeeperData.name);
    
    if (zookeeperData.new_name) {
      params.append('new_name', zookeeperData.new_name);
    }
    if (zookeeperData.qualification) {
      params.append('qualification', zookeeperData.qualification);
    }
    if (zookeeperData.responsibilities) {
      params.append('responsibilities', zookeeperData.responsibilities);
    }
    
    const response = await axios.get(`${API_URL}zookeepers/update/?${params.toString()}`);
    return response.data;
  } catch (error) {
    console.error('Error updating zookeeper:', error);
    throw error.response ? error.response.data : error;
  }
};

export const deleteZookeeper = async (name) => {
  try {
    const params = new URLSearchParams();
    params.append('name', name);
    
    const response = await axios.get(`${API_URL}zookeepers/delete/?${params.toString()}`);
    return response.data;
  } catch (error) {
    console.error('Error deleting zookeeper:', error);
    throw error.response ? error.response.data : error;
  }
};

export const getZookeeperDetail = async (name) => {
  try {
    const response = await axios.get(`${API_URL}zookeepers/${name}/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching zookeeper details:', error);
    throw error.response ? error.response.data : error;
  }
};

export const getCareRoutines = async () => {
  try {
    const response = await axios.get(`${API_URL}care-routines/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching care routines:', error);
    throw error.response ? error.response.data : error;
  }
};

export const addCareRoutine = async (routineData) => {
  try {
    const params = new URLSearchParams();
    params.append('feeding_time', routineData.feeding_time);
    params.append('diet', routineData.diet);
    
    if (routineData.medical_needs) {
      params.append('medical_needs', routineData.medical_needs);
    }
    
    if (routineData.zookeepers && routineData.zookeepers.length > 0) {
      params.append('zookeepers', routineData.zookeepers.join(','));
    }
    
    const response = await axios.get(`${API_URL}care-routines/add/?${params.toString()}`);
    return response.data;
  } catch (error) {
    console.error('Error adding care routine:', error);
    throw error.response ? error.response.data : error;
  }
};

export const updateCareRoutine = async (routineData) => {
  try {
    const params = new URLSearchParams();
    params.append('id', routineData.id);
    
    if (routineData.feeding_time) {
      params.append('feeding_time', routineData.feeding_time);
    }
    if (routineData.diet) {
      params.append('diet', routineData.diet);
    }
    if (routineData.medical_needs) {
      params.append('medical_needs', routineData.medical_needs);
    }
    if (routineData.zookeepers && routineData.zookeepers.length > 0) {
      params.append('zookeepers', routineData.zookeepers.join(','));
    }
    
    const response = await axios.get(`${API_URL}care-routines/update/?${params.toString()}`);
    return response.data;
  } catch (error) {
    console.error('Error updating care routine:', error);
    throw error.response ? error.response.data : error;
  }
};

export const deleteCareRoutine = async (id) => {
  try {
    const params = new URLSearchParams();
    params.append('id', id);
    
    const response = await axios.get(`${API_URL}care-routines/delete/?${params.toString()}`);
    return response.data;
  } catch (error) {
    console.error('Error deleting care routine:', error);
    throw error.response ? error.response.data : error;
  }
};

export const getCareRoutineDetail = async (id) => {
  try {
    const response = await axios.get(`${API_URL}care-routines/${id}/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching care routine details:', error);
    throw error.response ? error.response.data : error;
  }
};

