import unittest
import json
from app import create_app, db

class RestaurantsTestCase(unittest.TestCase):
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.restaurant = {'name': 'McDonalds'}

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


if __name__ == "__main__":
    unittest.main()