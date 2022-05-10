from django.test import TestCase
from django_hosts import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.User.factories import UserFactory, StaffFactory, SuperuserFactory
from core.Comment.models import Comment
from core.Comment.factories import CommentFactory
from core.Post.factories import PostFactory
from core.Likes.factories import CommentLikeFactory


class ApiCommentViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.post = PostFactory.create()

        self.user = UserFactory.create()
        self.staff = StaffFactory.create()
        self.superuser = SuperuserFactory.create()
        self.client.force_authenticate(user=self.superuser)

        self.author = self.superuser
        self.not_author = self.staff
        self.comment = CommentFactory.create(post=self.post, author=self.superuser)

        self.comment_data = {
            'post': self.post.id,
            'text': 'Comment text',
        }
        self.comment_new_data = {
            'post': self.post.id,
            'text': 'Comment new text',
        }

    def test_comment_list(self):
        CommentLikeFactory.create(user=self.superuser, comment=self.comment, is_liked=True)
        response = self.client.get(reverse('api:comments-list', host='api'),
                                   HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['id'], self.comment.id)
        self.assertTrue(results[0]['is_liked'])

    def test_comment_create_success(self):
        data = self.comment_data.copy()
        response = self.client.post(reverse('api:comments-list', host='api'),
                                    HTTP_HOST='api', format='json', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        result = response.data
        for key in data.keys():
            self.assertEqual(data[key], result[key])

    def test_comment_update_success(self):
        data = self.comment_new_data.copy()
        client = APIClient()
        client.force_authenticate(user=self.author)
        response = client.put(reverse('api:comments-detail', args=[self.comment.id], host='api'),
                              HTTP_HOST='api', format='json', data=data)
        result = response.data
        for key in data.keys():
            self.assertEqual(data[key], result[key])

    def test_comment_update_not_author_error(self):
        data = self.comment_new_data.copy()
        client = APIClient()
        client.force_authenticate(user=self.not_author)
        response = client.put(reverse('api:comments-detail', args=[self.comment.id], host='api'),
                              HTTP_HOST='api', format='json', data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_comment_retrieve_success(self):
        response = self.client.get(reverse('api:comments-detail', args=[self.comment.id], host='api'),
                                   HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_comment_delete_not_author_error(self):
        client = APIClient()
        client.force_authenticate(user=self.not_author)
        response = client.delete(reverse('api:comments-detail', args=[self.comment.id], host='api'),
                                 HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_comment_delete_success(self):
        client = APIClient()
        client.force_authenticate(user=self.author)
        response = client.delete(reverse('api:comments-detail', args=[self.comment.id], host='api'),
                                 HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Comment.objects.all().exists())

    def test_comment_like_success(self):
        response = self.client.get(reverse('api:comments-like', args=[self.comment.id], host='api'),
                                   HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.comment.likes_counter)
        self.assertFalse(self.comment.dislikes_counter)

    def test_comment_dislike_success(self):
        response = self.client.get(reverse('api:comments-dislike', args=[self.comment.id], host='api'),
                                   HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(self.comment.likes_counter)
        self.assertTrue(self.comment.dislikes_counter)

    def test_comment_deactivate_success(self):
        response = self.client.get(reverse('api:comments-deactivate', args=[self.comment.id], host='api'),
                                   HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(self.comment.likes_counter)
        self.assertFalse(self.comment.dislikes_counter)
