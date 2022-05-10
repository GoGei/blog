from django.test import TestCase
from django_hosts import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.User.factories import UserFactory, StaffFactory, SuperuserFactory
from core.Category.models import Category
from core.Category.factories import CategoryFactory


class ApiCategoryViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = CategoryFactory.create()
        self.user = UserFactory.create()
        self.staff = StaffFactory.create()
        self.superuser = SuperuserFactory.create()
        self.client.force_authenticate(user=self.staff)

        self.category_data = {
            'name': 'category-name',
            'position': 1,
        }
        self.category_new_data = {
            'name': 'category-new-name',
            'position': 10,
        }

    def test_category_list(self):
        response = self.client.get(reverse('api:categories-list', host='api'),
                                   HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['id'], self.category.id)

    def test_category_create_staff_success(self):
        client = APIClient()
        client.force_authenticate(user=self.staff)
        data = self.category_data.copy()
        response = client.post(reverse('api:categories-list', host='api'),
                               HTTP_HOST='api', format='json', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        result = response.data
        self.assertTrue(Category.objects.filter(id=result['id']))
        self.assertTrue(Category.objects.filter(slug=result['slug']))
        for key in data.keys():
            self.assertEqual(data[key], result[key])

    def test_category_create_superuser_success(self):
        client = APIClient()
        client.force_authenticate(user=self.superuser)
        data = self.category_data.copy()
        response = client.post(reverse('api:categories-list', host='api'),
                               HTTP_HOST='api', format='json', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        result = response.data
        self.assertTrue(Category.objects.filter(slug=result['slug']))
        for key in data.keys():
            self.assertEqual(data[key], result[key])

    def test_category_create_user_forbidden(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.post(reverse('api:categories-list', host='api'),
                               HTTP_HOST='api', format='json', data=self.category_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_category_create_name_error(self):
        client = APIClient()
        client.force_authenticate(user=self.staff)
        data = self.category_data.copy()
        client.post(reverse('api:categories-list', host='api'),
                    HTTP_HOST='api', format='json', data=data)
        response = client.post(reverse('api:categories-list', host='api'),
                               HTTP_HOST='api', format='json', data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        result = response.data
        self.assertIn('name', result)

    def test_category_update_success(self):
        data = self.category_new_data.copy()
        response = self.client.put(reverse('api:categories-detail', args=[self.category.id], host='api'),
                                   HTTP_HOST='api', format='json', data=data)
        result = response.data
        self.assertTrue(Category.objects.filter(slug=result['slug']))
        for key in data.keys():
            self.assertEqual(data[key], result[key])

    def test_category_update_name_error(self):
        data = self.category_data.copy()
        self.client.post(reverse('api:categories-list', host='api'),
                         HTTP_HOST='api', format='json', data=data)

        response = self.client.put(reverse('api:categories-detail', args=[self.category.id], host='api'),
                                   HTTP_HOST='api', format='json', data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        result = response.data
        self.assertIn('name', result)

    def test_category_retrieve_success(self):
        response = self.client.get(reverse('api:categories-detail', args=[self.category.id], host='api'),
                                   HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_category_delete_success(self):
        response = self.client.delete(reverse('api:categories-detail', args=[self.category.id], host='api'),
                                      HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Category.objects.all().exists())

    def test_category_get_by_slug_success(self):
        category = self.category
        response = self.client.get(reverse('api:categories-get-by-slug', host='api'),
                                   HTTP_HOST='api', format='json', data={'slug': category.slug})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['category']['id'], category.id)
