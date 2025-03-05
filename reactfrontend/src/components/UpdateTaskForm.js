import React, { useState, useEffect } from "react";
import { updateTask, getAnimals, getZookeepers } from "../services/api";

const UpdateTaskForm = ({ onTaskUpdated }) => {
  const [taskId, setTaskId] = useState("");
  const [taskData, setTaskData] = useState({
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
    setTaskData({ ...taskData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      await updateTask(taskId, taskData);
      alert("Task updated successfully!");
      setTaskId("");
      setTaskData({ zookeeper: "", animal: "", task_type: "", description: "", scheduled_time: "" });
      onTaskUpdated();
    } catch (error) {
      console.error("Failed to update task:", error);
    }
  };

  return (
    <div>
      <h2>Update Task</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={taskId}
          onChange={(e) => setTaskId(e.target.value)}
          placeholder="Task ID"
          required
        />

        {/* Zookeeper Dropdown */}
        <select name="zookeeper" value={taskData.zookeeper} onChange={handleChange} required>
          <option value="">Select Zookeeper</option>
          {zookeepers.map((keeper) => (
            <option key={keeper.name} value={keeper.name}>
              {keeper.name}
            </option>
          ))}
        </select>

        {/* Animal Dropdown */}
        <select name="animal" value={taskData.animal} onChange={handleChange} required>
          <option value="">Select Animal</option>
          {animals.map((animal) => (
            <option key={animal.species} value={animal.species}>
              {animal.species}
            </option>
          ))}
        </select>

        <select name="task_type" value={taskData.task_type} onChange={handleChange} required>
          <option value="">Select Task Type</option>
          <option value="FEEDING">Feeding</option>
          <option value="MEDICAL">Medical</option>
          <option value="CLEANING">Cleaning</option>
          <option value="OTHER">Other</option>
        </select>

        <input
          type="text"
          name="description"
          value={taskData.description}
          onChange={handleChange}
          placeholder="Description"
          required
        />
        <input
          type="datetime-local"
          name="scheduled_time"
          value={taskData.scheduled_time}
          onChange={handleChange}
          required
        />

        <button type="submit">Update Task</button>
      </form>
    </div>
  );
};

export default UpdateTaskForm;


