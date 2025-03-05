import React, { useState } from "react";
import { deleteTask } from "../services/api";

const TaskDelete = () => {
  const [taskId, setTaskId] = useState("");

  const handleDelete = async () => {
    if (!window.confirm("Are you sure you want to delete this task?")) return;

    try {
      await deleteTask(taskId);
      alert("Task deleted successfully!");
      setTaskId("");
    } catch (error) {
      console.error("Failed to delete task:", error);
    }
  };

  return (
    <div>
      <h2>Delete Task</h2>
      <input type="text" value={taskId} onChange={(e) => setTaskId(e.target.value)} placeholder="Task ID" required />
      <button onClick={handleDelete}>Delete Task</button>
    </div>
  );
};

export default TaskDelete;


