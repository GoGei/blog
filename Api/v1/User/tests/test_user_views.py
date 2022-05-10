import uuid

from django.test import TestCase
from django_hosts import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.User.models import User
from core.User.factories import UserFactory, StaffFactory, SuperuserFactory


class ApiUserViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory.create()
        self.staff = StaffFactory.create()
        self.superuser = SuperuserFactory.create()
        self.client.force_authenticate(user=self.superuser)

        self.user_data = {
            'email': 'useremail@example.com',
            'first_name': 'first_name',
            'last_name': 'last_name',
            'is_active': True,
            'is_staff': True,
            'is_superuser': True,
        }
        self.user_new_data = {
            'email': 'newuseremail@example.com',
            'first_name': 'new_first_name',
            'last_name': 'new_last_name',
            'is_active': True,
            'is_staff': True,
            'is_superuser': True,
        }

        password = uuid.uuid4()
        self.password_data = {
            'password': password,
            'repeat_password': password,
        }
        self.password_mismatch_data = {
            'password': uuid.uuid4(),
            'repeat_password': uuid.uuid4(),
        }

    def test_user_list(self):
        response = self.client.get(reverse('api:users-list', host='api'),
                                   HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        self.assertEqual(len(results), 3)

    def test_user_create_superuser_success(self):
        client = APIClient()
        client.force_authenticate(user=self.superuser)
        data = self.user_data.copy()
        response = client.post(reverse('api:users-list', host='api'),
                               HTTP_HOST='api', format='json', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        result = response.data
        self.assertTrue(User.objects.filter(id=result['id']))
        for key in data.keys():
            self.assertEqual(data[key], result[key])

    def test_user_create_staff_forbidden(self):
        client = APIClient()
        client.force_authenticate(user=self.staff)
        response = client.post(reverse('api:users-list', host='api'),
                               HTTP_HOST='api', format='json', data=self.user_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_create_user_forbidden(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.post(reverse('api:users-list', host='api'),
                               HTTP_HOST='api', format='json', data=self.user_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_create_name_error(self):
        client = APIClient()
        client.force_authenticate(user=self.superuser)
        data = self.user_data.copy()
        client.post(reverse('api:users-list', host='api'),
                    HTTP_HOST='api', format='json', data=data)
        response = client.post(reverse('api:users-list', host='api'),
                               HTTP_HOST='api', format='json', data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        result = response.data
        self.assertIn('email', result)

    def test_user_update_success(self):
        data = self.user_new_data.copy()
        response = self.client.put(reverse('api:users-detail', args=[self.user.id], host='api'),
                                   HTTP_HOST='api', format='json', data=data)
        result = response.data
        for key in data.keys():
            self.assertEqual(data[key], result[key])

    def test_user_update_email_error(self):
        data = self.user_data.copy()
        self.client.post(reverse('api:users-list', host='api'),
                         HTTP_HOST='api', format='json', data=data)

        response = self.client.put(reverse('api:users-detail', args=[self.user.id], host='api'),
                                   HTTP_HOST='api', format='json', data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        result = response.data
        self.assertIn('email', result)

    def test_user_retrieve_success(self):
        response = self.client.get(reverse('api:users-detail', args=[self.user.id], host='api'),
                                   HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_delete_success(self):
        response = self.client.delete(reverse('api:users-detail', args=[self.user.id], host='api'),
                                      HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.all().filter(id=self.user.id))

    def test_user_set_password_success(self):
        user = self.user
        response = self.client.post(reverse('api:users-set-password', args=[user.id], host='api'),
                                    HTTP_HOST='api', format='json', data=self.password_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_set_password_mismatch(self):
        user = self.user
        response = self.client.post(reverse('api:users-set-password', args=[user.id], host='api'),
                                    HTTP_HOST='api', format='json', data=self.password_mismatch_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        result = response.data
        self.assertIn('password', result)
