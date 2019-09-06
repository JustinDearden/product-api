from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Product, Tag, Attribute

from product.serializers import ProductSerializer
import tempfile
import os
from PIL import Image


PRODUCT_URL = reverse('product:product-list')


def image_upload_url(product_id):
    """Return URL for product image upload"""
    return reverse('product:product-upload-image', args=[product_id])


def sample_tag(user, name='Outdoors'):
    """Create and return a sample tag"""
    return Tag.objects.create(user=user, name=name)


def sample_attribute(user, name='Green'):
    """Create and return a sample attribute"""
    return Attribute.objects.create(user=user, name=name)


def detail_url(product_id):
    """Return product detail URL"""
    return reverse('product:product-list', args=[product_id])


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

    def test_view_recipe_detail(self):
        """Test viewing a product detail"""
        product = sample_product(user=self.user)
        product.tags.add(sample_tag(user=self.user))
        product.attributes.add(sample_attribute(user=self.user))

    def test_create_basic_product(self):
        """Test creating product"""
        payload = {
            'title': 'Test product',
            'time_minutes': 30,
            'price': 10.00,
        }
        res = self.client.post(PRODUCT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        product = Product.objects.get(id=res.data['id'])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(product, key))

    def test_create_product_with_tags(self):
        """Test creating a product with tags"""
        tag1 = sample_tag(user=self.user, name='Tag 1')
        tag2 = sample_tag(user=self.user, name='Tag 2')
        payload = {
            'title': 'Test product with two tags',
            'tags': [tag1.id, tag2.id],
            'time_minutes': 30,
            'price': 10.00
        }
        res = self.client.post(PRODUCT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        product = Product.objects.get(id=res.data['id'])
        tags = product.tags.all()
        self.assertEqual(tags.count(), 2)
        self.assertIn(tag1, tags)
        self.assertIn(tag2, tags)

    def test_create_product_with_attributes(self):
        """Test creating product with attributes"""
        attribute1 = sample_attribute(user=self.user, name='Attribute 1')
        attribute2 = sample_attribute(user=self.user, name='Attribute 2')
        payload = {
            'title': 'Test product with attributes',
            'attributes': [attribute1.id, attribute2.id],
            'time_minutes': 45,
            'price': 15.00
        }

        res = self.client.post(PRODUCT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        product = Product.objects.get(id=res.data['id'])
        attributes = product.attributes.all()
        self.assertEqual(attributes.count(), 2)
        self.assertIn(attribute1, attributes)
        self.assertIn(attribute2, attributes)


class ProductImageUploadTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user('user', 'testpass')
        self.client.force_authenticate(self.user)
        self.product = sample_product(user=self.user)

    def tearDown(self):
        self.product.image.delete()

    def test_upload_image_to_product(self):
        """Test uploading an image to product"""
        url = image_upload_url(self.product.id)
        with tempfile.NamedTemporaryFile(suffix='.jpg') as ntf:
            img = Image.new('RGB', (10, 10))
            img.save(ntf, format='JPEG')
            ntf.seek(0)
            res = self.client.post(url, {'image': ntf}, format='multipart')

        self.product.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('image', res.data)
        self.assertTrue(os.path.exists(self.product.image.path))

    def test_upload_image_bad_request(self):
        """Test uploading an invalid image"""
        url = image_upload_url(self.product.id)
        res = self.client.post(url, {'image': 'notimage'}, format='multipart')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
