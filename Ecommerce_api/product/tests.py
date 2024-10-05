from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Product, Order, Category
from rest_framework_simplejwt.tokens import RefreshToken

class UserViewSetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.admin_user = User.objects.create_superuser(username='admin', password='adminpass')
        self.token = str(RefreshToken.for_user(self.user).access_token)

    def test_create_user(self):
        response = self.client.post(reverse('user-list'), {
            'username': 'newuser', 'password': 'newpass', 'email': 'newuser@example.com'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.get(reverse('user-detail', args=[self.user.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_unauthenticated(self):
        response = self.client.get(reverse('user-detail', args=[self.user.id]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ProductViewSetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.category = Category.objects.create(name='Test Category')
        self.token = str(RefreshToken.for_user(self.user).access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_list_products(self):
        response = self.client.get(reverse('product-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_product(self):
        response = self.client.post(reverse('product-list'), {
            'name': 'New Product',
            'price': 15.99,
            'stock_quantity': 50,
            'category': self.category.id,
            'image_url': 'https://example.com/image.jpg',
            'description': 'This is a great product.'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_product_unauthenticated(self):
        self.client.logout()  # Log out the authenticated user
        response = self.client.post(reverse('product-list'), {
            'name': 'New Product',
            'price': 15.99,
            'stock_quantity': 50,
            'category': self.category.id
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class OrderViewSetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.category = Category.objects.create(name='Test Category')  # Ensure category is created
        self.product = Product.objects.create(
            name='Test Product', 
            price=10.99, 
            stock_quantity=100, 
            category=self.category
        )
        self.token = str(RefreshToken.for_user(self.user).access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_create_order(self):
        response = self.client.post(reverse('order-list'), {
            'user': self.user.id,
            'product': self.product.id,
            'quantity': 2,
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_order_unauthenticated(self):
        self.client.logout()
        response = self.client.post(reverse('order-list'), {
            'user': self.user.id,
            'product': self.product.id,
            'quantity': 2
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ReviewViewSetTests(APITestCase):
    def setUp(self):
        # Create a category instance
        self.category = Category.objects.create(name='Test Category')
        
        # Create a product instance and assign the category
        self.product = Product.objects.create(
            name='Test Product',
            price=10.99,
            image_url='http://example.com/image.jpg',  # Provide a valid URL for the image
            description='Test Product Description',
            stock_quantity=100,
            category=self.category  # Assign the category here
        )
    def test_create_review(self):
        # Make a request with authentication
        response = self.client.post(
            '/api/reviews/',  # Adjust the URL to your reviews endpoint
            data={
                'product': self.product.id,
                'rating': 5,
                'comment': 'Great product!'
            },
            HTTP_AUTHORIZATION='Token ' + self.token.key  # Include the token in headers
        )
        
        # Assert that the response status code is 201
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    def test_create_review_unauthenticated(self):
        self.client.logout()
        response = self.client.post(reverse('review-list'), {
            'product': self.product.id,
            'rating': 5,
            'comment': 'Great product!'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CategoryViewSetTests(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Test Category')

    def test_list_categories(self):
        response = self.client.get(reverse('category-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
