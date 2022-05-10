import uuid
from django.test import TestCase
from django_hosts import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.Post.factories import PostFactory
from core.Likes.factories import PostLikeFactory
from core.User.factories import UserFactory


class ApiProfileTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory.create()
        self.client.force_authenticate(user=self.user)

        self.post = PostFactory.create(author=self.user)
        PostLikeFactory.create(user=self.user, post=self.post)

        password = uuid.uuid4()
        self.password_data = {
            'password': password,
            'repeat_password': password,
        }
        self.password_mismatch_data = {
            'password': uuid.uuid4(),
            'repeat_password': uuid.uuid4(),
        }

    def test_profile_get_success(self):
        response = self.client.get(reverse('api:profile', host='api'), HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.user.id)

    def test_profile_put_success(self):
        data = {
            'first_name': 'First name',
            'last_name': 'Last name',
            'email': 'useremail@gmail.com',
            # 'phone': '+380(99)-999-9999',
            'phone': '+380999999999',
        }
        response = self.client.put(reverse('api:profile', host='api'), data=data, HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result = response.data
        self.assertEqual(result['id'], self.user.id)
        for key in data.keys():
            self.assertEqual(result[key], data[key])

    def test_profile_posts_get_success(self):
        response = self.client.get(reverse('api:profile-posts-list', host='api'), HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.post)

    def test_profile_posts_liked_get_success(self):
        response = self.client.get(reverse('api:profile-posts-liked-list', host='api'), HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.post)

    def test_profile_set_password_success(self):
        response = self.client.post(reverse('api:profile-set-password', host='api'),
                                    HTTP_HOST='api', format='json', data=self.password_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_profile_set_password_mismatch(self):
        response = self.client.post(reverse('api:profile-set-password', host='api'),
                                    HTTP_HOST='api', format='json', data=self.password_mismatch_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        result = response.data
        self.assertIn('password', result)
