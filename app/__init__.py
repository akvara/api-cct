from flask import request, jsonify, abort, make_response
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import func

from instance.config import app_config

db = SQLAlchemy()

def create_app(config_name):
    from app.models.restaurant import Restaurant, Menu, Vote
    from app.models.user import User

    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    @app.route('/restaurants/', methods=['POST', 'GET'])
    def restaurants():
        if request.method == "POST":
            # TODO: making restaurant only for Admin

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
        # TODO: uploading menu only for Admin

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

        menu = Menu.query.filter_by(restaurant_id=restaurant.id, for_date=for_date).first()
        if not menu:
            menu = Menu(text=text, restaurant_id=restaurant.id, for_date=for_date)
            menu.save()
        else:
            menu.text = text
            menu.replace()

        response = jsonify({
            'id': menu.id,
            'text': menu.text,
            'date_created': menu.date_created,
            'date_modified': menu.date_modified
        })
        response.status_code = 201
        return response

    @app.route('/today', methods=['GET'])
    def menu_for_today(**kwargs):
        date_today = datetime.now().strftime('%Y-%m-%d')
        for_today = db.session\
            .query(Menu.id, Restaurant.name, Menu.text)\
            .join(Restaurant)\
            .filter(Menu.for_date == date_today)\
            .all()

        response = jsonify(for_today)
        response.status_code = 200
        return response\

    @app.route('/votes', methods=['GET'])
    def votes_all(**kwargs):
        # date_today = datetime.now().strftime('%Y-%m-%d')
        votes = Restaurant.get_all()
        results = []

        for vote in votes:
            obj = {
                'id': vote.id,
                'user_id': vote.user_id,
                'for_date': vote.for_date,
                'for_menu': vote.for_menu,
            }
            results.append(obj)
        response = jsonify(results)
        response.status_code = 200
        return response

    @app.route('/vote/', methods=['POST'])
    def accept_vote(**kwargs):
        # Get the access token from the header
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            abort(401)
        access_token = auth_header.split(" ")[1]

        if access_token:
            # Attempt to decode the token and get the User ID
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                for_menu = str(request.data.get('for_menu', ''))
                # TODO: vote only for existing menu

                today = datetime.now().strftime('%Y-%m-%d')
                vote = Vote.query.filter_by(user_id=user_id, for_date=today).first()

                if not vote:
                    vote = Vote(user_id=user_id, for_date=today, for_menu=for_menu)
                    vote.save()
                else:
                    vote.for_menu = for_menu
                    vote.save()

                response = jsonify({
                    'id': vote.id,
                    'user_id': vote.user_id,
                    'for_menu': vote.for_menu,
                    'for_date': vote.for_date,
                })

                return make_response(response), 201

            else:
                # user is not legit, so the payload is an error message
                message = user_id
                response = {
                    'message': message
                }
                return make_response(jsonify(response)), 401

    @app.route('/winner', methods=['GET'])
    def winner_for_today(**kwargs):
        date_today = datetime.now().strftime('%Y-%m-%d')

        counted_votes = db.session \
            .query(func.count(Vote.id).label('total'), Vote.for_menu)\
            .filter(Vote.for_date == date_today) \
            .group_by(Vote.for_menu)\
            .order_by('total desc')\
            .all()

        max_votes = counted_votes[0][0]

        winners = [v[1] for v in counted_votes if v[0] == max_votes]
        if len(winners) == 1:
            winners = winners[0]
        winners = {'winner': winners, 'wanted_by': max_votes}

        response = jsonify(winners)
        response.status_code = 200
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