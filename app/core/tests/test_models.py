from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email - is successful"""
        email = 'test@gmail.com'
        password = 'Testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user to see if it's normalized"""
        email = 'test@GMAIL.com'
        user = get_user_model().objects.create_user(email, 'test1234')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            # Everything ran in here will raise a value error
            get_user_model().objects.create_user(None, 'test1234')

    def test_create_new_superuser(self):
        """Test to create a new super user"""
        user = get_user_model().objects.create_superuser(
            'test@gmail.com',
            'test1234'
        )
        # is_superuser is part of the PermissionMixin
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        