from flask import Flask
from models import db
from view import api_bp, RestaurantsView, RestaurantView, PizzasView, RestaurantPizzasView
from flask_migrate import Migrate
import os


app = Flask(__name__)
migrate = Migrate(app, db)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pizza_restaurants.db'
db.init_app(app)

# Register views with the blueprint
api_bp.add_url_rule('/restaurants', view_func=RestaurantsView.as_view('restaurants'))
api_bp.add_url_rule('/restaurants/<int:restaurant_id>', view_func=RestaurantView.as_view('restaurant'))
api_bp.add_url_rule('/pizzas', view_func=PizzasView.as_view('pizzas'))
api_bp.add_url_rule('/restaurant_pizzas', view_func=RestaurantPizzasView.as_view('restaurant_pizzas'))

# Register blueprint
app.register_blueprint(api_bp)

if __name__ == '__main__':
    app.run(debug=True)
