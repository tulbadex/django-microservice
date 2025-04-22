from django.test import TestCase
from accounts.models import CustomUser

class CustomUserModelTest(TestCase):
    def test_create_user(self):
        user = CustomUser.objects.create_user(email='test@example.com', password='pass1234')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('pass1234'))

    def test_create_superuser(self):
        admin = CustomUser.objects.create_superuser(email='admin@example.com', password='adminpass')
        self.assertTrue(admin.is_superuser)
        self.assertTrue(admin.is_staff)
