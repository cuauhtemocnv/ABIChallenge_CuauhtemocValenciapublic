import unittest
from your_flask_app import app, db, Prediction  # Replace 'your_flask_app' with the actual name of your Flask app module

class FlaskTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Set up the test database
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_db.sqlite3'
        app.config['TESTING'] = True
        with app.app_context():
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        # Clean up the test database
        with app.app_context():
            db.drop_all()

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_predict(self):
        # Test the /predict endpoint
        response = self.app.post('/predict', json={'input': [3, 0, 0, 0, 0, 0, 0, 0]})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('prediction', data)

    def test_predict_batch(self):
        # Test the /predict_batch endpoint
        response = self.app.post('/predict_batch', json={'inputs': [[3, 0, 0, 0, 0, 0, 0, 0], [3, 0, 0, 0, 0, 0, 0, 0]]})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('predictions', data)
        self.assertEqual(len(data['predictions']), 2)

    def test_database_entry(self):
        # Test that a prediction is stored in the database
        self.app.post('/predict', json={'input': [3, 0, 0, 0, 0, 0, 0, 0]})
        with app.app_context():
            prediction = Prediction.query.first()
            self.assertIsNotNone(prediction)
            self.assertEqual(prediction.input_data, '[3, 0, 0, 0, 0, 0, 0, 0]')

if __name__ == '__main__':
    unittest.main()
