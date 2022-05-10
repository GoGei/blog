from django.test import TestCase
from django_hosts import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.User.factories import UserFactory, StaffFactory, SuperuserFactory
from core.Post.models import Post
from core.Post.factories import PostFactory
from core.Comment.factories import CommentFactory
from core.Category.factories import CategoryFactory
from core.Likes.factories import PostLikeFactory, CommentLikeFactory


class ApiPostViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = UserFactory.create()
        self.staff = StaffFactory.create()
        self.superuser = SuperuserFactory.create()
        self.client.force_authenticate(user=self.superuser)

        self.author = self.superuser
        self.not_author = self.staff
        self.category = CategoryFactory.create()
        self.post = PostFactory.create(author=self.superuser, category=self.category)

        self.post_data = {
            'category': self.category.id,
            'title': 'Post title',
            'text': 'Post text',
        }
        self.post_new_data = {
            'category': self.category.id,
            'title': 'Post new title',
            'text': 'Post new text',
        }

    def test_post_list(self):
        PostLikeFactory.create(user=self.superuser, post=self.post, is_liked=True)
        response = self.client.get(reverse('api:posts-list', host='api'),
                                   HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['id'], self.post.id)
        self.assertTrue(results[0]['is_liked'])

    def test_post_create_success(self):
        data = self.post_data.copy()
        response = self.client.post(reverse('api:posts-list', host='api'),
                                    HTTP_HOST='api', format='json', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        result = response.data
        self.assertTrue(Post.objects.filter(slug=result['slug']))
        for key in data.keys():
            self.assertEqual(data[key], result[key])

    def test_post_update_success(self):
        data = self.post_new_data.copy()
        client = APIClient()
        client.force_authenticate(user=self.author)
        response = client.put(reverse('api:posts-detail', args=[self.post.id], host='api'),
                              HTTP_HOST='api', format='json', data=data)
        result = response.data
        self.assertTrue(Post.objects.filter(slug=result['slug']))
        for key in data.keys():
            self.assertEqual(data[key], result[key])

    def test_post_update_not_author_error(self):
        data = self.post_new_data.copy()
        client = APIClient()
        client.force_authenticate(user=self.not_author)
        response = client.put(reverse('api:posts-detail', args=[self.post.id], host='api'),
                              HTTP_HOST='api', format='json', data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_retrieve_success(self):
        response = self.client.get(reverse('api:posts-detail', args=[self.post.id], host='api'),
                                   HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_delete_not_author_error(self):
        client = APIClient()
        client.force_authenticate(user=self.not_author)
        response = client.delete(reverse('api:posts-detail', args=[self.post.id], host='api'),
                                 HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_delete_success(self):
        client = APIClient()
        client.force_authenticate(user=self.author)
        response = client.delete(reverse('api:posts-detail', args=[self.post.id], host='api'),
                                 HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Post.objects.all().exists())

    def test_post_like_success(self):
        response = self.client.get(reverse('api:posts-like', args=[self.post.id], host='api'),
                                   HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.post.likes_counter)
        self.assertFalse(self.post.dislikes_counter)

    def test_post_dislike_success(self):
        response = self.client.get(reverse('api:posts-dislike', args=[self.post.id], host='api'),
                                   HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(self.post.likes_counter)
        self.assertTrue(self.post.dislikes_counter)

    def test_post_deactivate_success(self):
        response = self.client.get(reverse('api:posts-deactivate', args=[self.post.id], host='api'),
                                   HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(self.post.likes_counter)
        self.assertFalse(self.post.dislikes_counter)

    def test_post_comment_success(self):
        data = {
            'text': 'Comment text'
        }
        response = self.client.post(reverse('api:posts-comment', args=[self.post.id], host='api'),
                                    HTTP_HOST='api', format='json', data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data
        self.assertEqual(results['author'], self.superuser.id)
        self.assertEqual(results['post'], self.post.id)
        self.assertEqual(results['text'], data['text'])

    def test_post_comments(self):
        comment = CommentFactory.create(post=self.post)
        CommentLikeFactory.create(comment=comment, user=self.superuser, is_liked=True)
        response = self.client.get(reverse('api:posts-comments', args=[self.post.id], host='api'),
                                   HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['id'], comment.id)
        self.assertTrue(results[0]['is_liked'])
