import React, { useState } from "react";

export const DeleteAnimalForm = () => {
    const [animalId, setAnimalId] = useState("");

    const handleSubmit = async (e) => {
        e.preventDefault();

        const response = await fetch("http://localhost:8000/zoo/delete_animal/", {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ aid: animalId }),
        });

        const data = await response.json();
        if (response.ok) {
            alert(data.message);
        } else {
            alert(`Error: ${data.error}`);
        }

        setAnimalId("");
    };

    return (
        <form onSubmit={handleSubmit}>
            <div>
                <label>Animal ID to Delete:</label>
                <input
                    type="number"
                    value={animalId}
                    onChange={(e) => setAnimalId(e.target.value)}
                    required
                />
            </div>
            <button type="submit">Delete Animal</button>
        </form>
    );
};



export const DeleteHabitatForm = () => {
    const [habitatId, setHabitatId] = useState("");

    const handleSubmit = async (e) => {
        e.preventDefault();

        const response = await fetch("http://localhost:8000/zoo/delete_habitat/", {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ hid: habitatId }),
        });

        const data = await response.json();
        if (response.ok) {
            alert(data.message);
        } else {
            alert(`Error: ${data.error}`);
        }

        setHabitatId("");
    };

    return (
        <form onSubmit={handleSubmit}>
            <div>
                <label>Habitat ID to Delete:</label>
                <input
                    type="number"
                    value={habitatId}
                    onChange={(e) => setHabitatId(e.target.value)}
                    required
                />
            </div>
            <button type="submit">Delete Habitat</button>
        </form>
    );
};
