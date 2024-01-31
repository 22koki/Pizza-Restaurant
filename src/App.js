// src/App.js

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

const App = () => {
  const [restaurants, setRestaurants] = useState([]);
  const [pizzas, setPizzas] = useState([]);
  const [newPizzaData, setNewPizzaData] = useState({
    price: 0,
    pizza_id: 1,
    restaurant_id: 1,
  });
  const [selectedRestaurant, setSelectedRestaurant] = useState(null);

  useEffect(() => {
    axios.get('http://localhost:5000/restaurants')
      .then(response => setRestaurants(response.data))
      .catch(error => console.error('Error fetching restaurants:', error));

    axios.get('http://localhost:5000/pizzas')
      .then(response => setPizzas(response.data))
      .catch(error => console.error('Error fetching pizzas:', error));
  }, []);

  const handleDeleteRestaurant = (restaurantId) => {
    axios.delete(`http://localhost:5000/restaurants/${restaurantId}`)
      .then(() => {
        setRestaurants(restaurants.filter(r => r.id !== restaurantId));
      })
      .catch(error => console.error('Error deleting restaurant:', error));
  };

  const handleCreateRestaurantPizza = () => {
    axios.post('http://localhost:5000/restaurant_pizzas', newPizzaData)
      .then(response => {
        setPizzas([...pizzas, response.data]);
      })
      .catch(error => console.error('Error creating restaurant pizza:', error));
  };

  const handleViewRestaurantData = (restaurantId) => {
    setSelectedRestaurant(restaurantId);
  };

  return (
    <div className="container">
      <h1>Pizza Restaurant App</h1>

      <h2>Restaurants</h2>
      <ul>
        {restaurants.map(restaurant => (
          <li key={restaurant.id}>
            <span>
              {restaurant.name} - {restaurant.address}
            </span>
            <button onClick={() => handleDeleteRestaurant(restaurant.id)}>Delete</button>
            <button onClick={() => handleViewRestaurantData(restaurant.id)}>View Data</button>
          </li>
        ))}
      </ul>

      {selectedRestaurant && (
        <div>
          <h2>Restaurant Data</h2>
          <p>Name: {restaurants.find(r => r.id === selectedRestaurant)?.name}</p>
          <p>Address: {restaurants.find(r => r.id === selectedRestaurant)?.address}</p>
          {/* Add more information as needed */}
          <button onClick={() => setSelectedRestaurant(null)}>Back to Restaurants</button>
        </div>
      )}

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
};

export default App;
