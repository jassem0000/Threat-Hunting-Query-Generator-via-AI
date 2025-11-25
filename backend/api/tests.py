from django.test import TestCase
from django.urls import reverse
from django.test import Client

class APITestCase(TestCase):
    def setUp(self):
        self.client = Client()
    
    def test_health_check(self):
        """Test the health check endpoint"""
        response = self.client.get('/api/health')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'status': 'healthy'})