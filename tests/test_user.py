import unittest
import json
from app import create_app
from unittest.mock import patch

class TestUser(unittest.TestCase):
    def setUp(self):
        self.app = create_app('app.config.Config')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        
    def tearDown(self):
        self.app_context.pop()
    
    @patch('app.models.user_model.User.get_all')
    def test_get_users(self, mock_get_all):
        # Données mockées
        mock_get_all.return_value = [
            {
                "_id": "60d21b4667d0d8992e610c85",
                "username": "test_user",
                "email": "test@example.com",
                "created_at": "2023-08-01T12:00:00"
            }
        ]
        
        response = self.client.get('/api/users/')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['username'], 'test_user')
    
    @patch('app.models.user_model.User.create')
    def test_create_user(self, mock_create):
        # Données mockées
        mock_create.return_value = "60d21b4667d0d8992e610c85"
        
        user_data = {
            "username": "new_user",
            "email": "new@example.com",
            "password": "password123"
        }
        
        response = self.client.post(
            '/api/users/', 
            data=json.dumps(user_data),
            content_type='application/json'
        )
        
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 201)
        self.assertIn('user_id', data)

if __name__ == '__main__':
    unittest.main()