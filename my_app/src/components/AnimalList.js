import React, { useEffect, useState } from "react";

export const AnimalList = () => {
    const [animals, setAnimals] = useState([]);

    useEffect(() => {
        fetch("http://localhost:8000/zoo/animals/")
            .then((response) => response.json())
            .then((data) => setAnimals(data))
            .catch((error) => console.error("Error fetching animals:", error));
    }, []);

    return (
        <div>
            <h1>Animal List</h1>
            <ul>
                {animals.map((animal, index) => (
                    <li key={index}>
                        {animal.id} — {animal.name} — {animal.habitat || "Unknown habitat"}
                    </li>
                ))}
            </ul>
        </div>
    );
};


export const HabitatList = () => {
    const [habitats, setHabitats] = useState([]);

    useEffect(() => {
        fetch("http://localhost:8000/zoo/habitats/")
            .then((response) => response.json())
            .then((data) => setHabitats(data))
            .catch((error) => console.error("Error fetching habitats:", error));
    }, []);

    return (
        <div>
            <h1>Habitat List</h1>
            <ul>
                {habitats.map((habitat, index) => (
                    <li key={index}>
                        {habitat.id} — {habitat.name} — {habitat.animals || "Unknown habitat"}
                    </li>
                ))}
            </ul>
        </div>
    );
};

