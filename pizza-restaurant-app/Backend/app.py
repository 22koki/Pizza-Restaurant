# app.py

from flask import Flask, jsonify, request
from models import db, Restaurant, Pizza, RestaurantPizza

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pizza_restaurants.db'
db.init_app(app)

# ... other configurations ...

# Route to get all restaurants
@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    restaurants = Restaurant.query.all()
    return jsonify([{'id': r.id, 'name': r.name, 'address': r.address} for r in restaurants])

# Route to get a specific restaurant by id
@app.route('/restaurants/<int:restaurant_id>', methods=['GET'])
def get_restaurant(restaurant_id):
    restaurant = Restaurant.query.get(restaurant_id)
    if restaurant:
        return jsonify({
            'id': restaurant.id,
            'name': restaurant.name,
            'address': restaurant.address,
            'pizzas': [{'id': p.id, 'name': p.name, 'ingredients': p.ingredients} for p in restaurant.pizzas]
        })
    else:
        return jsonify({'error': 'Restaurant not found'}), 404

# Route to delete a restaurant by id
@app.route('/restaurants/<int:restaurant_id>', methods=['DELETE'])
def delete_restaurant(restaurant_id):
    restaurant = Restaurant.query.get(restaurant_id)
    if restaurant:
        # Delete associated RestaurantPizza records
        RestaurantPizza.query.filter_by(restaurant_id=restaurant.id).delete()
        # Delete the restaurant
        db.session.delete(restaurant)
        db.session.commit()
        return '', 204
    else:
        return jsonify({'error': 'Restaurant not found'}), 404

# Route to get all pizzas
@app.route('/pizzas', methods=['GET'])
def get_pizzas():
    pizzas = Pizza.query.all()
    return jsonify([{'id': p.id, 'name': p.name, 'ingredients': p.ingredients} for p in pizzas])

# Route to create a new RestaurantPizza
@app.route('/restaurant_pizzas', methods=['POST'])
def create_restaurant_pizza():
    data = request.get_json()
    new_pizza = RestaurantPizza(price=data['price'], pizza_id=data['pizza_id'], restaurant_id=data['restaurant_id'])
    db.session.add(new_pizza)
    db.session.commit()
    return jsonify({'id': new_pizza.pizza.id, 'name': new_pizza.pizza.name, 'ingredients': new_pizza.pizza.ingredients})

# ... other routes ...

if __name__ == '__main__':
    app.run(debug=True)
