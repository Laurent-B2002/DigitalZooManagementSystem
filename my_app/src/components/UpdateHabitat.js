import { useState } from "react";

export default function UpdateHabitat() {
  const [habitatId, setHabitatId] = useState("");
  const [name, setName] = useState("");
  const [size, setSize] = useState("");
  const [climate, setClimate] = useState("");
  const [suitableSpecies, setSuitableSpecies] = useState("");
  const [message, setMessage] = useState("");

  const handleUpdate = async () => {
    if (!habitatId) {
      setMessage("Habitat ID is required.");
      return;
    }

    const queryParams = new URLSearchParams({ hid: habitatId });
    if (name) queryParams.append("name", name);
    if (size) queryParams.append("size", size);
    if (climate) queryParams.append("climate", climate);
    if (suitableSpecies) queryParams.append("suitable_species", suitableSpecies);

    try {
      const response = await fetch(
        `http://localhost:8000/update_habitat/?${queryParams.toString()}`,
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
      const data = await response.json();
      setMessage(data.message || "Habitat updated successfully.");
    } catch (error) {
      setMessage("Error updating habitat: " + error.message);
    }
  };

  return (
    <div className="p-4 border rounded shadow-md max-w-md mx-auto">
      <h2 className="text-xl font-bold mb-2">Update Habitat</h2>

      <input
        type="text"
        placeholder="Habitat ID"
        value={habitatId}
        onChange={(e) => setHabitatId(e.target.value)}
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
        placeholder="Size (optional)"
        value={size}
        onChange={(e) => setSize(e.target.value)}

      />

      <input
        type="text"
        placeholder="Climate (optional)"
        value={climate}
        onChange={(e) => setClimate(e.target.value)}

      />

      <input
        type="text"
        placeholder="Suitable Species (optional)"
        value={suitableSpecies}
        onChange={(e) => setSuitableSpecies(e.target.value)}

      />

      <button
        onClick={handleUpdate}
        className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 w-full"
      >
        Update Habitat
      </button>

      {message && <p className="mt-2 text-sm text-gray-700">{message}</p>}
    </div>
  );
}
