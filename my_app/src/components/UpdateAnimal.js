import { useState } from "react";

export default function UpdateAnimal() {
  const [animalId, setAnimalId] = useState("");
  const [name, setName] = useState("");
  const [diet, setDiet] = useState("");
  const [lifespan, setLifespan] = useState("");
  const [behavior, setBehavior] = useState("");
  const [habitatId, setHabitatId] = useState("");
  const [message, setMessage] = useState("");

  const handleUpdate = async () => {
    if (!animalId) {
      setMessage("Animal ID is required.");
      return;
    }

    const queryParams = new URLSearchParams({ aid: animalId });
    if (name) queryParams.append("name", name);
    if (diet) queryParams.append("diet", diet);
    if (lifespan) queryParams.append("lifespan", lifespan);
    if (behavior) queryParams.append("behavior", behavior);
    if (habitatId) queryParams.append("hid", habitatId);

    try {
      const response = await fetch(
        `http://localhost:8000/update_animal/?${queryParams.toString()}`,
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
      const data = await response.json();
      setMessage(data.message || "Animal updated successfully.");
    } catch (error) {
      setMessage("Error updating animal: " + error.message);
    }
  };

  return (
    <div className="p-4 border rounded shadow-md max-w-md mx-auto">
      <h2 className="text-xl font-bold mb-2">Update Animal</h2>
      
      <input
        type="text"
        placeholder="Animal ID"
        value={animalId}
        onChange={(e) => setAnimalId(e.target.value)}

        required
      />
      <input
        type="text"
        placeholder="New Name (optional)"
        value={name}
        onChange={(e) => setName(e.target.value)}

      />
      <input
        type="text"
        placeholder="Diet (optional)"
        value={diet}
        onChange={(e) => setDiet(e.target.value)}

      />
      <input
        type="number"
        placeholder="Lifespan (optional)"
        value={lifespan}
        onChange={(e) => setLifespan(e.target.value)}

      />
      <input
        type="text"
        placeholder="Behavior (optional)"
        value={behavior}
        onChange={(e) => setBehavior(e.target.value)}

      />
      <input
        type="text"
        placeholder="Habitat ID"
        value={habitatId}
        onChange={(e) => setHabitatId(e.target.value)}

      />
      
      <button
        onClick={handleUpdate}
        className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
      >
        Update Animal
      </button>

      {message && <p className="mt-2 text-sm text-gray-700">{message}</p>}
    </div>
  );
}
