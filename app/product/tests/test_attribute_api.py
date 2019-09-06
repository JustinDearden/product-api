from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Attribute

from product.serializers import AttributeSerializer


ATTRIBUTE_URL = reverse('product:attribute-list')


class PublicAttributesApiTests(TestCase):
    """Test the publicly available attribute list"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to access the endpoint"""
        res = self.client.get(ATTRIBUTE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateAttributesApiTests(TestCase):
    """Test private attributes api"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@gmail.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_attribute_list(self):
        """Test retrieving a list of attributes"""

        Attribute.objects.create(user=self.user, name="Polka Dots")
        Attribute.objects.create(user=self.user, name="Stripes")

        res = self.client.get(ATTRIBUTE_URL)

        attributes = Attribute.objects.all().order_by('-name')
        serializer = AttributeSerializer(attributes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_attributes_limited_to_user(self):
        """Test that attributes for the authenticated user are returned"""
        user2 = get_user_model().objects.create_user(
            'other@gmail.com',
            'Testpass1234'
        )
        Attribute.objects.create(user=user2, name='tables')
        attribute = Attribute.objects.create(user=self.user, name='chairs')

        res = self.client.get(ATTRIBUTE_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], attribute.name)


def test_create_attribute_successful(self):
    """Test creating a new attribute"""
    payload = {'name': 'Fan'}
    self.client.post(ATTRIBUTE_URL, payload)

    exists = Attribute.objects.filter(
        user=self.user,
        name=payload['name']).exists()
    self.assertTrue(exists)


def test_create_attribute_invalid(self):
    """Test creating invalid attribute fails"""
    payload = {'name': ''}

    res = self.client.post(ATTRIBUTE_URL, payload)

    self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
