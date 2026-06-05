from django.test import TestCase
from .models import Order, User, Product
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

# Create your tests here.
# class UserOrderTestCase(TestCase):
#     def setUp(self):
#         user1 = User.objects.create_user(username='user1', password='pass123')
#         user2 = User.objects.create_user(username='user2', password='pass123')
#         Order.objects.create(user=user1)
#         Order.objects.create(user=user1)
#         Order.objects.create(user=user2)
#         Order.objects.create(user=user2)

#     def test_user_orders_retrieves_only_authenticated_users_orders(self):
#         user = User.objects.get(username='user2')
#         self.client.force_login(user)
#         response = self.client.get(reverse('user-orders'))
#         assert response.status_code == status.HTTP_200_OK
#         orders = response.json()
#         self.assertTrue(all(order['user'] == user.id for order in orders))

    
#     def test_user_orders_unauthenticated_access(self):
#         response = self.client.get(reverse('user-orders'))
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ProductAPITestCase(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(username='admin', password='pass123')
        self.normal_user = User.objects.create_user(username='user', password='pass123')
        self.product = Product.objects.create(
            name = "Test Product",
            description = "Test Description",
            price = 9.99,
            stock = 10
        )
        self.url = reverse('product-detail', kwargs={'product_id': self.product.pk})

    def test_get_product(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.product.name)

    def test_unauthorized_update_product(self):
        data = {
            'name': 'Updated Product',
            'description': 'Updated Description',
            'price': 99.99,                       
            'stock': 10                           
        }
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_unauthorized_delete_product(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_only_admin_can_update_product(self):
        # normal user can not update
        self.client.force_login(self.normal_user)
        data = {
            'name': 'Updated Product',
            'description': 'Updated Description',
            'price': 99.99,                       
            'stock': 10                           
        }
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Product.objects.get(pk=self.product.pk).name, self.product.name)

        # admin user can update
        # admin user can update
        self.client.force_login(self.admin_user)
        data = {
            'name': 'Updated Product',
            'description': 'Updated Description',
            'price': 99.99,                       
            'stock': 10                           
        }
        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], data['name'])

    def test_only_admin_can_delete_product(self):
        # normal user can not delete
        self.client.force_login(self.normal_user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Product.objects.filter(pk=self.product.pk).exists())

        # admin user can delete
        self.client.force_login(self.admin_user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(pk=self.product.pk).exists())


