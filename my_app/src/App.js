import React from "react";
import { AnimalList, HabitatList } from "./components/AnimalList";
import AddAnimalForm from "./components/AddAnimal";
import { DeleteAnimalForm, DeleteHabitatForm } from "./components/Deletion";

function App() {
    return (
        <div>
            <h1>Welcome to the Animal App!</h1>
            <AddAnimalForm />
            <DeleteAnimalForm />
            <DeleteHabitatForm />
            <AnimalList />
            <HabitatList />
        </div>
    );
}

export default App;
