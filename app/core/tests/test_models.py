from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


def sample_user(email='test@gmail.com', password='Testpass123'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


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

    def test_tag_str(self):
        """Test the tag string representation"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Shirt'
        )

        self.assertEqual(str(tag), tag.name)

    def test_attribute_str(self):
        """Test and ingredient string"""
        ingredient = models.Attribute.objects.create(
            user=sample_user(),
            name="lamp"
        )

        self.assertEqual(str(ingredient), ingredient.name)
