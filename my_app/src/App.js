import React from "react";
import AnimalList from "./components/AnimalList";
import AddAnimalForm from "./components/AddAnimal";

function App() {
    return (
        <div>
            <h1>Welcome to the Animal App!</h1>
            <AddAnimalForm />
            <AnimalList />
        </div>
    );
}

export default App;
