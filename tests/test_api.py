import unittest
import json
from app import create_app, db
from datetime import datetime, timedelta
from app.models.user import User
from app.models.restaurant import Vote


class RestaurantsTestCase(unittest.TestCase):
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.restaurant = {'name': 'McDonalds'}
        self.menu = {'text': 'Buger', 'for_date': '2017-07-01'}

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

    def register_user(self, email="user@test.com", password="test1234"):
        user_data = {
            'email': email,
            'password': password
        }
        return self.client().post('/auth/register', data=user_data)

    def login_user(self, email="user@test.com", password="test1234"):
        user_data = {
            'email': email,
            'password': password
        }
        return self.client().post('/auth/login', data=user_data)

    def register_login_and_vote(self, vote, email="user@test.com"):
        self.register_user(email=email)
        result = self.login_user(email=email)
        access_token = json.loads(result.data.decode())['access_token']
        user_id = User.decode_token(access_token)

        vote['user_id'] = user_id

        return self.client().post(
            '/vote/',
            headers=dict(Authorization="Bearer " + access_token),
            data=vote)

    def test_restaurant_creation(self):
        """Test API can create a restaurant (POST request)"""
        res = self.client().post('/restaurants/', data=self.restaurant)
        self.assertEqual(res.status_code, 201)
        self.assertIn(self.restaurant['name'], str(res.data))

    def test_api_can_get_all_restaurants(self):
        """Test API can get all restaurants (GET request)."""
        res = self.client().post('/restaurants/', data=self.restaurant)
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/restaurants/')
        self.assertEqual(res.status_code, 200)
        self.assertIn(self.restaurant['name'], str(res.data))

    def test_api_can_get_restaurant_by_id(self):
        """Test API can get a single restaurant by using it's id."""
        rv = self.client().post('/restaurants/', data=self.restaurant)
        self.assertEqual(rv.status_code, 201)
        result_in_json = json.loads(rv.data.decode('utf-8').replace("'", "\""))
        result = self.client().get(
            '/restaurants/{}'.format(result_in_json['id']))
        self.assertEqual(result.status_code, 200)
        self.assertIn(self.restaurant['name'], str(result.data))

    def test_menu_upload(self):
        """Test API can upload menu for a restaurant (POST request)"""
        res = self.client().post('/restaurants/', data=self.restaurant)
        self.assertEqual(res.status_code, 201)
        result_in_json = json.loads(res.data.decode('utf-8').replace("'", "\""))
        restaurant_id = result_in_json['id']
        self.menu['restaurant_id'] = restaurant_id
        res = self.client().post(
            '/restaurants/{}/menu/'.format(restaurant_id),
            data=self.menu)
        self.assertEqual(res.status_code, 201)

    def test_returns_error_on_menu_no_restaurant(self):
        res = self.client().post('/restaurants/', data=self.restaurant)
        self.assertEqual(res.status_code, 201)
        result_in_json = json.loads(res.data.decode('utf-8').replace("'", "\""))
        restaurant_id = result_in_json['id'] + 1
        self.menu['restaurant_id'] = restaurant_id
        res = self.client().post(
            '/restaurants/{}/menu/'.format(restaurant_id),
            data=self.menu)
        self.assertEqual(res.status_code, 400)

    def test_returns_error_on_wrong_menu_date(self):
        res = self.client().post('/restaurants/', data=self.restaurant)
        self.assertEqual(res.status_code, 201)
        result_in_json = json.loads(res.data.decode('utf-8').replace("'", "\""))
        restaurant_id = result_in_json['id']
        self.menu['restaurant_id'] = restaurant_id
        self.menu['date'] = '17-17-17'
        res = self.client().post(
            '/restaurants/{}/menu/'.format(restaurant_id),
            data=self.menu)
        self.assertEqual(res.status_code, 400)

    def test_replaces_menu_for_the_same_date(self):
        res = self.client().post('/restaurants/', data=self.restaurant)
        result_in_json = json.loads(res.data.decode('utf-8').replace("'", "\""))
        restaurant_id = result_in_json['id']
        self.menu['restaurant_id'] = restaurant_id
        res = self.client().post(
            '/restaurants/{}/menu/'.format(restaurant_id),
            data=self.menu)
        result_in_json = json.loads(res.data.decode('utf-8').replace("'", "\""))
        first_id = result_in_json['id']
        self.menu['text'] = "New menu"
        res = self.client().post(
            '/restaurants/{}/menu/'.format(restaurant_id),
            data=self.menu)
        result_in_json = json.loads(res.data.decode('utf-8').replace("'", "\""))
        self.assertEqual(first_id, result_in_json['id'])
        self.assertEqual("New menu", result_in_json['text'])

    def test_returns_menu_for_foday(self):
        # make a restaurant
        res = self.client().post('/restaurants/', data=self.restaurant)
        result_in_json = json.loads(res.data.decode('utf-8').replace("'", "\""))
        restaurant_id = result_in_json['id']
        self.menu['restaurant_id'] = restaurant_id

        # upload menu for yesterday
        self.menu['date'] = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        res = self.client().post(
            '/restaurants/{}/menu/'.format(restaurant_id),
            data=self.menu)

        # upload menu for today
        self.menu['date'] = datetime.now().strftime('%Y-%m-%d')
        res = self.client().post(
            '/restaurants/{}/menu/'.format(restaurant_id),
            data=self.menu)
        result_in_json = json.loads(res.data.decode('utf-8').replace("'", "\""))
        todays_menu_id = result_in_json['id']

        # upload menu for tomorrow
        self.menu['date'] = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        res = self.client().post(
            '/restaurants/{}/menu/'.format(restaurant_id),
            data=self.menu)

        res = self.client().get('/today')

        result_in_json = json.loads(res.data.decode('utf-8').replace("'", "\""))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(1, len(result_in_json))
        self.assertEqual(todays_menu_id, result_in_json[0][0])

    def test_vote_creation(self):
        vote = {
            'for_menu': 1
        }

        res = self.register_login_and_vote(vote)

        self.assertEqual(res.status_code, 201)

        result_in_json = json.loads(res.data.decode('utf-8').replace("'", "\""))

        self.assertEqual(vote['user_id'], result_in_json['user_id'])
        self.assertEqual(vote['for_menu'], result_in_json['for_menu'])

    def test_unregistered_users_cannot_vote(self):
        vote = {
            'for_menu': 1,
            'user_id': 1
        }

        res = self.client().post(
            '/vote/',
            data=vote)

        self.assertEqual(res.status_code, 401)

    def test_duplicating_vote_is_replaced(self):
        vote = {'for_menu': 1}
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        user_id = User.decode_token(access_token)

        vote['user_id'] = user_id

        res = self.client().post(
            '/vote/',
            headers=dict(Authorization="Bearer " + access_token),
            data=vote)

        result_in_json = json.loads(res.data.decode('utf-8').replace("'", "\""))
        vote_id = result_in_json['id']
        vote['for_menu'] = 2

        res = self.client().post(
            '/vote/',
            headers=dict(Authorization="Bearer " + access_token),
            data=vote)
        self.assertEqual(res.status_code, 201)
        result_in_json = json.loads(res.data.decode('utf-8').replace("'", "\""))

        self.assertEqual(vote_id, result_in_json['id'])
        self.assertEqual(2, result_in_json['for_menu'])

    @unittest.skip("temp")
    def test_no_vote_for_non_existing_menu(self):
        vote = {
            'for_menu': 10
        }

        res = self.register_login_and_vote(vote)

        self.assertEqual(res.status_code, 400)

    def test_one_winner(self):
        vote = {'for_menu': 1}
        self.register_login_and_vote(vote, "user1@cct.lt")

        vote = {'for_menu': 2}
        self.register_login_and_vote(vote, "user2@cct.lt")
        self.register_login_and_vote(vote, "user3@cct.lt")
        self.register_login_and_vote(vote, "user4@cct.lt")

        res = self.client().get('/winner')
        result_in_json = json.loads(res.data.decode('utf-8').replace("'", "\""))

        self.assertEqual(2, result_in_json['winner'])
        self.assertEqual(3, result_in_json['wanted_by'])

    def test_several_winners(self):
        vote = {'for_menu': 2}

        self.register_login_and_vote(vote, "user1@cct.lt")
        self.register_login_and_vote(vote, "user2@cct.lt")

        vote = {'for_menu': 1}
        self.register_login_and_vote(vote, "user3@cct.lt")
        self.register_login_and_vote(vote, "user4@cct.lt")

        res = self.client().get('/winner')

        result_in_json = json.loads(res.data.decode('utf-8').replace("'", "\""))

        self.assertEqual([1, 2], result_in_json['winner'])
        self.assertEqual(2, result_in_json['wanted_by'])

if __name__ == "__main__":
    unittest.main()