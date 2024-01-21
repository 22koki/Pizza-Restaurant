// src/App.js

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import'./App.css'

const App = () => {
  const [restaurants, setRestaurants] = useState([]);
  const [pizzas, setPizzas] = useState([]);
  const [newPizzaData, setNewPizzaData] = useState({
    price: 0,
    pizza_id: 1, // Default pizza_id, you may want to change this based on your data
    restaurant_id: 1, // Default restaurant_id, you may want to change this based on your data
  });

  useEffect(() => {
    // Fetch all restaurants
    axios.get('/restaurants')
      .then(response => setRestaurants(response.data))
      .catch(error => console.error('Error fetching restaurants:', error));

    // Fetch all pizzas
    axios.get('/pizzas')
      .then(response => setPizzas(response.data))
      .catch(error => console.error('Error fetching pizzas:', error));
  }, []);

  const handleDeleteRestaurant = (restaurantId) => {
    // Delete a restaurant
    axios.delete(`/restaurants/${restaurantId}`)
      .then(() => {
        // Remove the deleted restaurant from the state
        setRestaurants(restaurants.filter(r => r.id !== restaurantId));
      })
      .catch(error => console.error('Error deleting restaurant:', error));
  };

  const handleCreateRestaurantPizza = () => {
    // Create a new RestaurantPizza
    axios.post('/restaurant_pizzas', newPizzaData)
      .then(response => {
        // Update the state with the newly created pizza
        setPizzas([...pizzas, response.data]);
      })
      .catch(error => console.error('Error creating restaurant pizza:', error));
  };

  return (
    <div>
      <h1>Pizza Restaurant App</h1>

      <h2>Restaurants</h2>
      <ul>
        {restaurants.map(restaurant => (
          <li key={restaurant.id}>
            {restaurant.name} - {restaurant.address}
            <button onClick={() => handleDeleteRestaurant(restaurant.id)}>Delete</button>
          </li>
        ))}
      </ul>

      <h2>Pizzas</h2>
      <ul>
        {pizzas.map(pizza => (
          <li key={pizza.id}>
            {pizza.name} - {pizza.ingredients}
          </li>
        ))}
      </ul>

      <h2>Create New Restaurant Pizza</h2>
      <label>Price: </label>
      <input
        type="number"
        value={newPizzaData.price}
        onChange={(e) => setNewPizzaData({ ...newPizzaData, price: e.target.value })}
      />
      <label>Pizza ID: </label>
      <input
        type="number"
        value={newPizzaData.pizza_id}
        onChange={(e) => setNewPizzaData({ ...newPizzaData, pizza_id: e.target.value })}
      />
      <label>Restaurant ID: </label>
      <input
        type="number"
        value={newPizzaData.restaurant_id}
        onChange={(e) => setNewPizzaData({ ...newPizzaData, restaurant_id: e.target.value })}
      />
      <button onClick={handleCreateRestaurantPizza}>Create</button>
    </div>
  );
}

export default App;
