from flask import Flask, request
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from models import db, Restaurant, Pizza, RestaurantPizza

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pizza_restaurants.db'
db.init_app(app)

api = Api(app)

class RestaurantsResource(Resource):
    def get(self, restaurant_id=None):
        if restaurant_id:
            restaurant = Restaurant.query.get(restaurant_id)
            if restaurant:
                return {'id': restaurant.id, 'name': restaurant.name, 'address': restaurant.address}
            else:
                return {"message": f"Restaurant with ID {restaurant_id} not found"}
        else:
            restaurants = Restaurant.query.all()
            return {'restaurants': [{'id': r.id, 'name': r.name, 'address': r.address} for r in restaurants]}

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help='Name is required')
        parser.add_argument('address', type=str, required=True, help='Address is required')
        args = parser.parse_args()

        new_restaurant = Restaurant(name=args['name'], address=args['address'])
        db.session.add(new_restaurant)
        db.session.commit()

        return {'id': new_restaurant.id, 'name': new_restaurant.name, 'address': new_restaurant.address}

    def put(self, restaurant_id):
        restaurant = Restaurant.query.get(restaurant_id)
        if not restaurant:
            return {'message': f'Restaurant with ID {restaurant_id} not found'}
        
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('address', type=str)
        args = parser.parse_args()

        if args['name']:
            restaurant.name = args['name']
        if args['address']:
            restaurant.address = args['address']

        db.session.commit()

        return {'id': restaurant.id, 'name': restaurant.name, 'address': restaurant.address}

    def delete(self, restaurant_id):
        restaurant = Restaurant.query.get(restaurant_id)
        if not restaurant:
            return {'message': f'Restaurant with ID {restaurant_id} not found'}

        db.session.delete(restaurant)
        db.session.commit()

        return {'message': f'Restaurant with ID {restaurant_id} has been deleted'}


class PizzasResource(Resource):
    def get(self, pizza_id=None):
        if pizza_id:
            pizza = Pizza.query.get(pizza_id)
            if pizza:
                return {'id': pizza.id, 'name': pizza.name, 'ingredients': pizza.ingredients}
            else:
                return {"message": f"Pizza with ID {pizza_id} not found"}
        else:
            pizzas = Pizza.query.all()
            return {'pizzas': [{'id': p.id, 'name': p.name, 'ingredients': p.ingredients} for p in pizzas]}

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help='Name is required')
        parser.add_argument('ingredients', type=str, required=True, help='Ingredients are required')
        args = parser.parse_args()

        new_pizza = Pizza(name=args['name'], ingredients=args['ingredients'])
        db.session.add(new_pizza)
        db.session.commit()

        return {'id': new_pizza.id, 'name': new_pizza.name, 'ingredients': new_pizza.ingredients}

    def put(self, pizza_id):
        pizza = Pizza.query.get(pizza_id)
        if not pizza:
            return {'message': f'Pizza with ID {pizza_id} not found'}

        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('ingredients', type=str)
        args = parser.parse_args()

        if args['name']:
            pizza.name = args['name']
        if args['ingredients']:
            pizza.ingredients = args['ingredients']

        db.session.commit()

        return {'id': pizza.id, 'name': pizza.name, 'ingredients': pizza.ingredients}

    def delete(self, pizza_id):
        pizza = Pizza.query.get(pizza_id)
        if not pizza:
            return {'message': f'Pizza with ID {pizza_id} not found'}

        db.session.delete(pizza)
        db.session.commit()

        return {'message': f'Pizza with ID {pizza_id} has been deleted'}


class RestaurantPizzasResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('price', type=float, required=True, help='Price is required')
        parser.add_argument('pizza_id', type=int, required=True, help='Pizza ID is required')
        parser.add_argument('restaurant_id', type=int, required=True, help='Restaurant ID is required')
        args = parser.parse_args()

        restaurant = Restaurant.query.get(args)
