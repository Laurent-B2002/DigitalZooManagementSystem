import React, { useState } from "react";

const AddAnimalForm = () => {
    const [name, setName] = useState("");
    const [habitatId, setHabitatId] = useState("");

    const handleSubmit = async (e) => {
        e.preventDefault();

        const response = await fetch("http://localhost:8000/zoo/add_animal/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ name, hid: habitatId }),
        });

        const data = await response.json();
        if (response.ok) {
            alert(`New animal added: ${data.name} in ${data.habitat}`);
        } else {
            alert(`Error: ${data.error}`);
        }

        setName("");
        setHabitatId("");
    };

    return (
        <form onSubmit={handleSubmit}>
            <div>
                <label>Animal Name:</label>
                <input
                    type="text"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    required
                />
            </div>
            <div>
                <label>Habitat ID:</label>
                <input
                    type="number"
                    value={habitatId}
                    onChange={(e) => setHabitatId(e.target.value)}
                    required
                />
            </div>
            <button type="submit">Add Animal</button>
        </form>
    );
};

export default AddAnimalForm;
