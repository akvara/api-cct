from flask import request, jsonify, abort
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from instance.config import app_config

db = SQLAlchemy()

def create_app(config_name):
    from app.models.restaurant import Restaurant, Menu
    from app.models.user import User

    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    @app.route('/restaurants/', methods=['POST', 'GET'])
    def restaurants():
        if request.method == "POST":
            name = str(request.data.get('name', ''))
            if name:
                restaurant = Restaurant(name=name)
                restaurant.save()
                response = jsonify({
                    'id': restaurant.id,
                    'name': restaurant.name,
                    'date_created': restaurant.date_created,
                    'date_modified': restaurant.date_modified
                })
                response.status_code = 201
                return response
        else:
            # GET
            restaurants = Restaurant.get_all()
            results = []

            for restaurant in restaurants:
                obj = {
                    'id': restaurant.id,
                    'name': restaurant.name,
                    'date_created': restaurant.date_created,
                    'date_modified': restaurant.date_modified
                }
                results.append(obj)
            response = jsonify(results)
            response.status_code = 200
            return response

    @app.route('/restaurants/<int:id>', methods=['GET'])
    def restaurant_manipulation(id, **kwargs):
        restaurant = Restaurant.query.filter_by(id=id).first()
        if not restaurant:
            abort(404)

        response = jsonify({
            'id': restaurant.id,
            'name': restaurant.name,
            'date_created': restaurant.date_created,
            'date_modified': restaurant.date_modified
        })
        response.status_code = 200
        return response

    @app.route('/restaurants/<int:id>/menu/', methods=['POST'])
    def menu_manipulation(id, **kwargs):
        restaurant = Restaurant.query.filter_by(id=id).first()

        if not restaurant:
            response = jsonify({"error": 'Restaurant not found'})
            response.status_code = 400
            return response

        today = datetime.now().strftime('%Y-%m-%d')
        date_text = request.data.get('date', today)
        if not validate(date_text):
            response = jsonify({"error": 'Invalid date: ' + date_text})
            response.status_code = 400
            return response

        for_date = datetime.strptime(date_text, '%Y-%m-%d')
        text = request.data.get('text', None)
        if not text:
            response = jsonify({})
            response.status_code = 200
            return response

        menu = Menu.query.filter_by(restaurant=restaurant.id, for_date=for_date).first()
        if not menu:
            menu = Menu(text=text, restaurant=restaurant.id, for_date=for_date)
        else:
            menu.text = text
        menu.save()
        response = jsonify({
            'id': menu.id,
            'date_created': menu.date_created,
            'date_modified': menu.date_modified
        })
        response.status_code = 201
        return response



    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app

def validate(date_text):
    try:
        datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except:
        return False