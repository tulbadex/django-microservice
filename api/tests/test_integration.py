from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from api.models import TaskResult
import time
from django.contrib.auth import get_user_model

User = get_user_model()

class IntegrationTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Auth setup
        self.user = User.objects.create_user(email="integration@example.com", password="strongpass")
        self.client.force_authenticate(user=self.user)

        self.url = reverse('process')
        self.valid_payload = {
            'email': 'integration@example.com',
            'message': 'Integration test message'
        }
    
    def test_full_process_flow(self):
        """Test the entire flow from API request to task completion"""
        # Submit task via API
        response = self.client.post(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, 202)
        id = response.data['task_id']
        
        # Wait for Celery to process (with timeout)
        max_wait = 30  # seconds
        start_time = time.time()
        task = None
        
        while time.time() - start_time < max_wait:
            try:
                task = TaskResult.objects.get(id=id)
                if task.status != 'PENDING':
                    break
            except TaskResult.DoesNotExist:
                pass
            time.sleep(1)
        
        # Verify task was processed
        self.assertIsNotNone(task, "Task not found in database")
        self.assertEqual(task.status, 'COMPLETED')
        
        # Check task status via API
        status_url = reverse('task_status', kwargs={'task_id': id})
        status_response = self.client.get(status_url)
        
        self.assertEqual(status_response.status_code, 200)
        self.assertEqual(status_response.data['status'], 'COMPLETED')
        self.assertIn('email', status_response.data['result'])
        self.assertEqual(status_response.data['result']['email'], self.valid_payload['email'])
        self.assertIn('processed_message', status_response.data['result'])
        self.assertEqual(status_response.data['result']['processed_message'], 'INTEGRATION TEST MESSAGE')