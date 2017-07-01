import unittest
import json
from app import create_app, db

class RestaurantsTestCase(unittest.TestCase):
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.restaurant = {'name': 'McDonalds'}
        self.menu = {'text': 'Buger', 'date': '2017-07-01'}

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

    @unittest.skip("temp")
    def test_restaurant_creation(self):
        """Test API can create a restaurant (POST request)"""
        res = self.client().post('/restaurants/', data=self.restaurant)
        self.assertEqual(res.status_code, 201)
        self.assertIn(self.restaurant['name'], str(res.data))

    @unittest.skip("temp")
    def test_api_can_get_all_restaurants(self):
        """Test API can get all restaurants (GET request)."""
        res = self.client().post('/restaurants/', data=self.restaurant)
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/restaurants/')
        self.assertEqual(res.status_code, 200)
        self.assertIn(self.restaurant['name'], str(res.data))

    @unittest.skip("temp")
    def test_api_can_get_restaurant_by_id(self):
        """Test API can get a single restaurant by using it's id."""
        rv = self.client().post('/restaurants/', data=self.restaurant)
        self.assertEqual(rv.status_code, 201)
        result_in_json = json.loads(rv.data.decode('utf-8').replace("'", "\""))
        result = self.client().get(
            '/restaurants/{}'.format(result_in_json['id']))
        self.assertEqual(result.status_code, 200)
        self.assertIn(self.restaurant['name'], str(result.data))

    @unittest.skip("temp")
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


    def test_returns_error_on_no_restaurant(self):
        res = self.client().post('/restaurants/', data=self.restaurant)
        self.assertEqual(res.status_code, 201)
        result_in_json = json.loads(res.data.decode('utf-8').replace("'", "\""))
        restaurant_id = result_in_json['id'] + 1
        self.menu['restaurant_id'] = restaurant_id
        res = self.client().post(
            '/restaurants/{}/menu/'.format(restaurant_id),
            data=self.menu)
        self.assertEqual(res.status_code, 400)

    def test_returns_error_on_wrong_date(self):
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
        self.assertEqual(res.status_code, 201)
        result_in_json = json.loads(res.data.decode('utf-8').replace("'", "\""))
        restaurant_id = result_in_json['id']
        self.menu['restaurant_id'] = restaurant_id
        res = self.client().post(
            '/restaurants/{}/menu/'.format(restaurant_id),
            data=self.menu)
        result_in_json = json.loads(res.data.decode('utf-8').replace("'", "\""))
        first_id = result_in_json['id']
        res = self.client().post(
            '/restaurants/{}/menu/'.format(restaurant_id),
            data=self.menu)
        result_in_json = json.loads(res.data.decode('utf-8').replace("'", "\""))
        self.assertEqual(first_id, result_in_json['id'])

if __name__ == "__main__":
    unittest.main()