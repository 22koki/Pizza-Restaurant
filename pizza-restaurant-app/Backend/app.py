from flask import Flask, request, jsonify
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import joinedload
from models import db, Restaurant, Pizza, RestaurantPizza
from flask_migrate import Migrate

app = Flask(__name__)
migrate = Migrate(app, db)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pizza_restaurants.db'
db.init_app(app)

api = Api(app)

# ... Your existing models and routes ...

class RestaurantsResource(Resource):
    def get(self, restaurant_id=None):
        if restaurant_id:
            restaurant = Restaurant.query.options(joinedload('pizzas')).get(restaurant_id)
            if restaurant:
                return jsonify({
                    'id': restaurant.id,
                    'name': restaurant.name,
                    'address': restaurant.address,
                    'pizzas': [{'id': pizza.id, 'name': pizza.name, 'ingredients': pizza.ingredients}
                               for pizza in restaurant.pizzas]
                })
            else:
                return {"error": "Restaurant not found"}, 404
        else:
            restaurants = Restaurant.query.all()
            return jsonify([{'id': r.id, 'name': r.name, 'address': r.address} for r in restaurants])

class PizzasResource(Resource):
    def get(self, pizza_id=None):
        if pizza_id:
            pizza = Pizza.query.get(pizza_id)
            if pizza:
                return jsonify({'id': pizza.id, 'name': pizza.name, 'ingredients': pizza.ingredients})
            else:
                return {"error": f"Pizza with ID {pizza_id} not found"}, 404
        else:
            pizzas = Pizza.query.all()
            return jsonify([{'id': p.id, 'name': p.name, 'ingredients': p.ingredients} for p in pizzas])

class RestaurantPizzasResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('price', type=float, required=True, help='Price is required')
        parser.add_argument('pizza_id', type=int, required=True, help='Pizza ID is required')
        parser.add_argument('restaurant_id', type=int, required=True, help='Restaurant ID is required')
        args = parser.parse_args()

        pizza = Pizza.query.get(args['pizza_id'])
        restaurant = Restaurant.query.get(args['restaurant_id'])

        if not pizza or not restaurant:
            return {'errors': ['validation errors']}, 400

        new_restaurant_pizza = RestaurantPizza(price=args['price'], pizza_id=pizza.id, restaurant_id=restaurant.id)
        db.session.add(new_restaurant_pizza)
        db.session.commit()

        return jsonify({
            'id': pizza.id,
            'name': pizza.name,
            'ingredients': pizza.ingredients
        })

# Add the resources to the API
api.add_resource(RestaurantsResource, '/restaurants', '/restaurants/<int:restaurant_id>')
api.add_resource(PizzasResource, '/pizzas', '/pizzas/<int:pizza_id>')
api.add_resource(RestaurantPizzasResource, '/restaurant_pizzas')


# Your other routes...

if __name__ == '__main__':
    app.run(debug=True)
