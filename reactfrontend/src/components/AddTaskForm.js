import React, { useState, useEffect } from "react";
import { addTask, getAnimals, getZookeepers } from "../services/api";

const AddTaskForm = ({ onTaskAdded }) => {
  const [task, setTask] = useState({
    zookeeper: "",
    animal: "",
    task_type: "",
    description: "",
    scheduled_time: "",
  });

  const [animals, setAnimals] = useState([]);
  const [zookeepers, setZookeepers] = useState([]);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const animalData = await getAnimals();
      const zookeeperData = await getZookeepers();
      setAnimals(animalData);
      setZookeepers(zookeeperData);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  const handleChange = (e) => {
    setTask({ ...task, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      await addTask(task);
      alert("Task added successfully!");
      setTask({ zookeeper: "", animal: "", task_type: "", description: "", scheduled_time: "" });
      onTaskAdded();
    } catch (error) {
      console.error("Failed to add task:", error);
    }
  };

  return (
    <div>
      <h2>Add Task</h2>
      <form onSubmit={handleSubmit}>
        {/* Zookeeper Dropdown */}
        <select name="zookeeper" value={task.zookeeper} onChange={handleChange} required>
          <option value="">Select Zookeeper</option>
          {zookeepers.map((keeper) => (
            <option key={keeper.name} value={keeper.name}>
              {keeper.name}
            </option>
          ))}
        </select>

        {/* Animal Dropdown */}
        <select name="animal" value={task.animal} onChange={handleChange} required>
          <option value="">Select Animal</option>
          {animals.map((animal) => (
            <option key={animal.species} value={animal.species}>
              {animal.species}
            </option>
          ))}
        </select>

        {/* Task Type Dropdown */}
        <select name="task_type" value={task.task_type} onChange={handleChange} required>
          <option value="">Select Task Type</option>
          <option value="FEEDING">Feeding</option>
          <option value="MEDICAL">Medical</option>
          <option value="CLEANING">Cleaning</option>
          <option value="OTHER">Other</option>
        </select>

        <input type="text" name="description" value={task.description} onChange={handleChange} placeholder="Description" required />
        <input type="datetime-local" name="scheduled_time" value={task.scheduled_time} onChange={handleChange} required />

        <button type="submit">Add Task</button>
      </form>
    </div>
  );
};

export default AddTaskForm;


