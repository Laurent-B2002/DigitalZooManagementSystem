import React, { useEffect, useState } from "react";

const AnimalList = () => {
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
                        {animal.name} — {animal.habitat || "Unknown habitat"}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default AnimalList;
