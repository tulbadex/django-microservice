import uuid
from django.test import TestCase
from api.models import TaskResult

class TaskResultModelTest(TestCase):
    def setUp(self):
        # Create a test task
        self.task = TaskResult.objects.create(
            email="test@example.com",
            message="Test message"
        )
    
    def test_task_creation(self):
        """Test the creation of a TaskResult object with auto-generated UUID"""
        self.assertIsNotNone(self.task.id)
        self.assertTrue(isinstance(uuid.UUID(str(self.task.id)), uuid.UUID))
        self.assertEqual(self.task.email, "test@example.com")
        self.assertEqual(self.task.message, "Test message")
        self.assertEqual(self.task.status, "PENDING")  # Default value
        self.assertIsNone(self.task.result)
        self.assertIsNotNone(self.task.created_at)
        self.assertIsNotNone(self.task.updated_at)
    
    def test_string_representation(self):
        """Test the string representation of a TaskResult"""
        self.assertEqual(str(self.task), f"Task {self.task.id} - PENDING")
    
    def test_status_update(self):
        """Test updating the status of a task"""
        self.task.status = "COMPLETED"
        self.task.result = "Processed successfully"
        self.task.save()
        
        # Fetch from database to confirm persistence
        updated_task = TaskResult.objects.get(id=self.task.id)
        self.assertEqual(updated_task.status, "COMPLETED")
        self.assertEqual(updated_task.result, "Processed successfully")