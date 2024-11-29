# tests/test_routes.py
import unittest
from app import app, db
from models import Product
from flask import json
from faker import Faker

fake = Faker()

class TestProductRoutes(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        # Setup the database
        with app.app_context():
            db.create_all()

    def tearDown(self):
        # Clean up the database
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_update_product(self):
        # Create a product and add it to the database
        product = Product(name=fake.company(),
                          description=fake.text(max_nb_chars=200),
                          price=99.99,
                          sku=fake.uuid4(),
                          category=fake.word(),
                          available=True)
        with app.app_context():
            db.session.add(product)
            db.session.commit()

        # New data for the product update
        updated_data = {
            'name': fake.company(),
            'description': fake.text(max_nb_chars=200),
            'price': 49.99,
            'sku': product.sku,
            'category': fake.word(),
            'available': False
        }

        # Update the product via the route
        response = self.app.put(f'/products/{product.id}', 
                                data=json.dumps(updated_data),
                                content_type='application/json')
        data = json.loads(response.data)

        # Check the response status and data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['name'], updated_data['name'])
        self.assertEqual(data['description'], updated_data['description'])
        self.assertEqual(data['price'], updated_data['price'])
        self.assertEqual(data['sku'], updated_data['sku'])
        self.assertEqual(data['category'], updated_data['category'])
        self.assertEqual(data['available'], updated_data['available'])

if __name__ == '__main__':
    unittest.main()
