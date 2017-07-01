from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from instance.config import app_config
from flask import request, jsonify, abort

db = SQLAlchemy()

def create_app(config_name):
    from app.models import Restaurant

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
        # retrieve a restaurant using it's ID
        restaurant = Restaurant.query.filter_by(id=id).first()
        if not restaurant:
            # Raise an HTTPException with a 404 not found status code
            abort(404)

        response = jsonify({
            'id': restaurant.id,
            'name': restaurant.name,
            'date_created': restaurant.date_created,
            'date_modified': restaurant.date_modified
        })
        response.status_code = 200
        return response

    return app