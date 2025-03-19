import React, { useState, useEffect } from "react";
import { getHabitats } from '../services/api';

export const AddTour = () => {
    const [habitats, setHabitats] = useState([]);
    const [selectedHabitats, setSelectedHabitats] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [order, setOrder] = useState(1);
    const [time, setTime] = useState('');

    useEffect(() => {
        const fetchHabitats = async () => {
            try {
                setLoading(true);
                const data = await getHabitats();
                setHabitats(data);
                setError(null);
            } catch (err) {
                setError('Failed to fetch habitats');
                console.error("Error fetching habitats:", err);
            } finally {
                setLoading(false);
            }
        };

        fetchHabitats();
    }, []);

    const handleSelectHabitat = (habitat) => {
        if (selectedHabitats.some(h => h.id === habitat.id)) {
            return;
        }

        const newHabitats = habitats.filter(h => h.id !== habitat.id);
        setHabitats(newHabitats);

        setSelectedHabitats([...selectedHabitats, { ...habitat, order, time }]);
        setOrder(order + 1);
    };

    const handleTimeChange = (e, habitatId) => {
        const updatedHabitats = selectedHabitats.map(item =>
            item.id === habitatId ? { ...item, time: e.target.value } : item
        );
        setSelectedHabitats(updatedHabitats);
    };

    const handleSubmit = () => {
        console.log("Tour Routes:", selectedHabitats);
    };

    if (loading) return <p>Loading habitats...</p>;
    if (error) return <p className="error-message">{error}</p>;

    return (
        <div>
            <h1>Create Tour Routes</h1>

            <div>
                <h2>Select Habitats</h2>
                {habitats.length === 0 ? (
                    <p>No habitats available to select.</p>
                ) : (
                    <ul>
                        {habitats.map(habitat => (
                            <li key={habitat.id}>
                                <button onClick={() => handleSelectHabitat(habitat)}>
                                    {habitat.name}
                                </button>
                            </li>
                        ))}
                    </ul>
                )}
            </div>

            <div>
                <h2>Selected Habitats</h2>
                <ul>
                    {selectedHabitats.map(habitat => (
                        <li key={habitat.id}>
                            {habitat.order}: {habitat.name} - Time: 
                            <input
                                type="time"
                                value={habitat.time || ''}
                                onChange={(e) => handleTimeChange(e, habitat.id)}
                            />
                        </li>
                    ))}
                </ul>
            </div>

            <div>
                <button onClick={handleSubmit}>Submit Tour</button>
            </div>
        </div>
    );
};

export default AddTour;
