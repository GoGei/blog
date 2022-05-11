import json
import uuid
from django.test import TestCase
from django_hosts import reverse

from core.User.factories import UserFactory
from .test_login_data import registration_data, registration_error_data


class LoginViewTestCase(TestCase):
    def setUp(self):
        self.password = str(uuid.uuid4())
        self.user = UserFactory.create(is_active=True)
        self.user.set_password(self.password)
        self.user.save()

        self.data = {
            'email': self.user.email,
            'password': self.password,
            'remember_me': True
        }

    def test_login_get_success(self):
        response = self.client.get(reverse('blog-login', host='blog'), HTTP_HOST='blog')
        self.assertEqual(response.status_code, 200)

    def test_login_post_success(self):
        data = self.data.copy()
        response = self.client.post(reverse('blog-login', host='blog'), HTTP_HOST='blog', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url=reverse('blog-index', host='blog'))

    def test_login_post_password_not_success(self):
        data = self.data.copy()
        data['password'] = 'password'

        response = self.client.post(reverse('blog-login', host='blog'), HTTP_HOST='blog', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Please, enter correct email and password')

    def test_login_post_user_is_not_active(self):
        data = self.data.copy()
        self.user.is_active = False
        self.user.save()

        response = self.client.post(reverse('blog-login', host='blog'), HTTP_HOST='blog', data=data)
        self.assertEqual(response.status_code, 200)
        # self.assertContains(response, 'This account is not active')

    def test_logout_success(self):
        self.client.login(username=self.user.email, password=self.password)
        response = self.client.post(reverse('blog-logout', host='blog'), HTTP_HOST='blog')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url=reverse('blog-index', host='blog'))

    def test_register_get_success(self):
        response = self.client.post(reverse('blog-register', host='blog'), HTTP_HOST='blog')
        self.assertEqual(response.status_code, 200)

    def test_register_post_success(self):
        data = registration_data.copy()
        response = self.client.post(reverse('blog-register', host='blog'), data=data, HTTP_HOST='blog',
                                    **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        self.assertTrue(result['success'])

    def test_register_post_error(self):
        data = registration_error_data.copy()
        response = self.client.post(reverse('blog-register', host='blog'), data=data, HTTP_HOST='blog',
                                    **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        self.assertFalse(result['success'])
