from flask.views import MethodView
from flask import Blueprint, jsonify, request
from models import db, Restaurant, Pizza, RestaurantPizza

api_bp = Blueprint('api', __name__, url_prefix='/api')


class RestaurantsView(MethodView):
    methods = ['GET']

    def get(self):
        restaurants = Restaurant.query.all()
        return jsonify([{'id': r.id, 'name': r.name, 'address': r.address} for r in restaurants])


class RestaurantView(MethodView):
    methods = ['GET', 'DELETE']

    def get(self, restaurant_id):
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

    def delete(self, restaurant_id):
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


class PizzasView(MethodView):
    methods = ['GET']

    def get(self):
        pizzas = Pizza.query.all()
        return jsonify([{'id': p.id, 'name': p.name, 'ingredients': p.ingredients} for p in pizzas])


class RestaurantPizzasView(MethodView):
    methods = ['POST']

    def post(self):
        data = request.get_json()
        new_pizza = RestaurantPizza(price=data['price'], pizza_id=data['pizza_id'], restaurant_id=data['restaurant_id'])
        db.session.add(new_pizza)
        db.session.commit()
        return jsonify({'id': new_pizza.pizza.id, 'name': new_pizza.pizza.name, 'ingredients': new_pizza.pizza.ingredients})
