from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Product

from product.serializers import ProductSerializer


PRODUCT_URL = reverse('product:product-list')


def sample_product(user, **params):
    """Create and return a sample product"""
    defaults = {
        'title': 'Sample product',
        'time_minutes': 10,
        'price': 5.00,
    }
    defaults.update(params)

    return Product.objects.create(user=user, **defaults)


class PublicProductApiTests(TestCase):
    """Test unauthenticated product API access"""

    def setUp(self):
        self.client = APIClient()

    def test_required_auth(self):
        """Test the authenticaiton is required"""
        res = self.client.get(PRODUCT_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateProductApiTests(TestCase):
    """Test authenticated product API access"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@gmail.com',
            'Testpass123'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_products(self):
        """Test retrieving list of products"""
        sample_product(user=self.user)
        sample_product(user=self.user)

        res = self.client.get(PRODUCT_URL)

        recipes = Product.objects.all().order_by('-id')
        serializer = ProductSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_products_limited_to_user(self):
        """Test retrieving products for user"""
        user2 = get_user_model().objects.create_user(
            'other@gmail.com',
            'pass'
        )
        sample_product(user=user2)
        sample_product(user=self.user)

        res = self.client.get(PRODUCT_URL)

        products = Product.objects.filter(user=self.user)
        serializer = ProductSerializer(products, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)
