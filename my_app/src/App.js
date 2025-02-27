import React from "react";
import AnimalList from "./components/AnimalList";
import AddAnimalForm from "./components/AddAnimal";
import UpdateAnimal from "./components/UpdateAnimal";
import UpdateHabitat from "./components/UpdateHabitat";

function App() {
    return (
        <div>
            <h1>Welcome to the Animal App!</h1>
            <AddAnimalForm />
            <AnimalList />
            <UpdateAnimal />
            <UpdateHabitat />
        </div>
    );
}

export default App;
