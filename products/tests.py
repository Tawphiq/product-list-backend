from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from .models import Product, CartItem

class ProductTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(
            username='admin', 
            email='admin@example.com', 
            password='adminpass'
        )
        self.product = Product.objects.create(
            name='Test Waffle',
            category='Waffle',
            price=6.50
        )

    def test_product_creation(self):
        self.assertEqual(self.product.name, 'Test Waffle')
        self.assertEqual(self.product.price, 6.50)

    def test_product_admin_access(self):
        # Log in as admin
        self.client.force_authenticate(user=self.admin_user)
        
        # Test product update
        response = self.client.put(
            f'/api/products/{self.product.id}/', 
            {'name': 'Updated Waffle', 'category': 'Waffle', 'price': 7.00}
        )
        self.assertEqual(response.status_code, 200)
        
        # Refresh product from database
        updated_product = Product.objects.get(id=self.product.id)
        self.assertEqual(updated_product.name, 'Updated Waffle')

class CartTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser', 
            email='test@example.com', 
            password='testpass'
        )
        self.product = Product.objects.create(
            name='Test Macaron',
            category='Macaron',
            price=8.00
        )

    def test_add_to_cart(self):
        # Log in as test user
        self.client.force_authenticate(user=self.user)
        
        # Add product to cart
        response = self.client.post('/api/cart/', {
            'product_id': self.product.id,
            'quantity': 2
        })
        
        self.assertEqual(response.status_code, 201)
        
        # Check cart contents
        cart_response = self.client.get('/api/cart/current_cart/')
        self.assertEqual(cart_response.status_code, 200)
        self.assertEqual(len(cart_response.data['items']), 1)
        self.assertEqual(cart_response.data['items'][0]['quantity'], 2)