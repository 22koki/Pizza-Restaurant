from flask import Flask
from models import db, Restaurant, Pizza, RestaurantPizza

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pizza_restaurants.db'
db.init_app(app)

def seed_data():
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()

        # Create restaurants
        restaurant1 = Restaurant(name='Pizza Palace', address='123 Main St')
        restaurant2 = Restaurant(name='Cheesy Bites', address='456 Oak St')

        # Create pizzas
        pizza1 = Pizza(name='Margherita', ingredients='Tomato, mozzarella, basil')
        pizza2 = Pizza(name='Pepperoni', ingredients='Pepperoni, tomato sauce, cheese')

        # Create restaurant-pizza associations
        rp1 = RestaurantPizza(price=10.99, pizza=pizza1, restaurant=restaurant1)
        rp2 = RestaurantPizza(price=12.99, pizza=pizza2, restaurant=restaurant2)

        # Add to session and commit to the database
        db.session.add_all([restaurant1, restaurant2, pizza1, pizza2, rp1, rp2])
        db.session.commit()
print("Database seeded succesfully!")

if __name__ == '__main__':
    seed_data()
