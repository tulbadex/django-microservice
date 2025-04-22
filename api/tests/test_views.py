from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import TaskResult
from unittest.mock import patch
import uuid
from django.contrib.auth import get_user_model
User = get_user_model()

class ProcessViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="test@example.com", password="testpass")
        self.client.force_authenticate(user=self.user)

        self.url = reverse('process')
        self.valid_payload = {
            'email': 'test@example.com',
            'message': 'Test message'
        }
    
    @patch('api.views.process_message')
    def test_create_task(self, mock_process_message):
        """Test creating a task via the API"""
        # Mock the Celery task to return a id
        mock_process_message.delay.return_value = type('obj', (object,), {'task_id': str(uuid.uuid4())})
        
        response = self.client.post(self.url, self.valid_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertIn('task_id', response.data)
        self.assertEqual(response.data['status'], 'PENDING')
        
        # Verify task was created in the database
        task = TaskResult.objects.get(id=response.data['task_id'])
        self.assertEqual(task.email, self.valid_payload['email'])
        self.assertEqual(task.message, self.valid_payload['message'])
    
    def test_create_task_invalid_data(self):
        """Test API validation rejects invalid data"""
        invalid_payload = {
            'message': 'Missing email'
        }
        response = self.client.post(self.url, invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

class TaskStatusViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="test@example.com", password="testpass")
        self.client.force_authenticate(user=self.user)
        
        self.task = TaskResult.objects.create(
            email="test@example.com",
            message="Test message",
            status="COMPLETED",
            result="Task completed successfully"
        )
        self.url = reverse('task_status', kwargs={'task_id': str(self.task.id)})
    
    def test_get_task_status(self):
        """Test retrieving a task's status"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['task_id'], str(self.task.id))
        self.assertEqual(response.data['status'], 'COMPLETED')
        self.assertEqual(response.data['result'], 'Task completed successfully')
    
    def test_task_not_found(self):
        """Test retrieving a non-existent task"""
        url = reverse('task_status', kwargs={'task_id': str(uuid.uuid4())})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)