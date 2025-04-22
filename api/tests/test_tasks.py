from django.test import TestCase
from api.models import TaskResult
from api.tasks import process_message
from unittest.mock import patch
import uuid

class CeleryTaskTest(TestCase):
    def setUp(self):
        self.task = TaskResult.objects.create(
            id=uuid.uuid4(),
            email="test@example.com",
            message="Test message",
            status="PENDING"
        )
    
    @patch('time.sleep')
    def test_process_message_success(self, mock_sleep):
        """Test successful task processing"""
        # Execute task synchronously
        process_message(str(self.task.id))
        
        # Refresh from database
        self.task.refresh_from_db()
        
        # Verify results
        self.assertEqual(self.task.status, "COMPLETED")
        self.assertIn('email', self.task.result)
        self.assertEqual(self.task.result['email'], self.task.email)
        self.assertIn('processed_message', self.task.result)
        self.assertEqual(self.task.result['processed_message'], 'TEST MESSAGE')
    
    # @patch('time.sleep')
    # def test_process_message_failure(self, mock_sleep):
    #     """Test task failure handling"""
    #     # Force an error
    #     mock_sleep.side_effect = Exception("Test error")
        
    #     # Process should catch the exception
    #     with self.assertRaises(Exception):
    #         process_message(str(self.task.id))
        
    #     # Refresh and verify status
    #     self.task.refresh_from_db()
    #     self.assertEqual(self.task.status, "FAILED")
    #     # self.assertIn("Error", self.task.result)

    #     self.assertIn("error", self.task.result.lower())
    #     self.assertIn("Test error", self.task.result)
    @patch('api.tasks.sleep')
    def test_process_message_failure(self, mock_sleep):
        """Test task failure handling"""
        # Force an error during sleep
        mock_sleep.side_effect = Exception("Test error")

        # Call the task directly (not as .delay)
        try:
            process_message(str(self.task.id))
        except Exception:
            pass  # Ignore expected exception

        # Reload the task
        self.task.refresh_from_db()

        # Now it should be marked as FAILED
        self.assertEqual(self.task.status, "FAILED")
        self.assertIn("error", self.task.result)
        self.assertIn("Test error", self.task.result['error'])