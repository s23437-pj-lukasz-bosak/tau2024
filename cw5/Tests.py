import unittest
from main import app

class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

        # Resetowanie danych testowych
        global users
        users = [
            {"id": 1, "name": "Jan Kowalski", "email": "jan@kowalski.pl"},
            {"id": 2, "name": "Anna Nowak", "email": "anna@nowak.pl"}
        ]

    # Test GET /users
    def test_get_users(self):
        response = self.app.get('/users')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), list)

    # Test GET /users/{id}
    def test_get_user_existing(self):
        response = self.app.get('/users/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["id"], 1)

    def test_get_user_non_existing(self):
        response = self.app.get('/users/999')
        self.assertEqual(response.status_code, 404)
        self.assertIn("error", response.get_json())

    # Test POST /users
    def test_create_user(self):
        response = self.app.post('/users', json={"name": "Piotr", "email": "piotr@example.com"})
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.get_json())

    def test_create_user_invalid_data(self):
        response = self.app.post('/users', json={"name": "Piotr"})
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.get_json())

    # Test PUT /users/{id}
    def test_update_user(self):
        response = self.app.put('/users/1', json={"name": "Jan Nowak"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["name"], "Jan Nowak")

    def test_update_user_non_existing(self):
        response = self.app.put('/users/999', json={"name": "Jan Nowak"})
        self.assertEqual(response.status_code, 404)
        self.assertIn("error", response.get_json())

    # Test DELETE /users/{id}
    def test_delete_user(self):
        response = self.app.delete('/users/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.get_json())

    def test_delete_user_non_existing(self):
        response = self.app.delete('/users/999')
        self.assertEqual(response.status_code, 404)
        self.assertIn("error", response.get_json())

if __name__ == '__main__':
    unittest.main()