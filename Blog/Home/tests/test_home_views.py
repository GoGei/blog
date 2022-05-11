import json
import uuid

from django.forms import model_to_dict
from django.test import TestCase, Client
from django_hosts import reverse

from core.User.factories import UserFactory
from core.Post.factories import PostFactory
from core.Comment.factories import CommentFactory
from core.Category.factories import CategoryFactory


class HomeViewTestCase(TestCase):
    def setUp(self):
        self.password = str(uuid.uuid4())
        self.user = UserFactory.create(is_active=True)
        self.user.set_password(self.password)
        self.user.save()

        self.client = Client()
        self.client.login(username=self.user.email, password=self.password)

        self.category = CategoryFactory.create()
        self.post = PostFactory.create(category=self.category)
        self.post_comment = CommentFactory.create(post=self.post)
        self.excluded_keys = ['created_stamp', 'archived_stamp']

    def test_index_get_success(self):
        response = self.client.get(reverse('blog-index', host='blog'), HTTP_HOST='blog')
        self.assertEqual(response.status_code, 200)

    def test_post_view_get_success(self):
        post = self.post
        response = self.client.get(reverse('blog-post-view', args=[post.slug], host='blog'), HTTP_HOST='blog')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, post.title)

    def test_render_post_comment_get_success(self):
        data = {'comment_id': json.dumps(self.post_comment.id)}
        response = self.client.get(reverse('blog-render-post-comment', host='blog'), data=data, HTTP_HOST='blog')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post_comment.id)

    def test_render_post_comments_get_success(self):
        data = self.get_dumped_data([self.post_comment], self.excluded_keys)
        data = {'comments': data}
        response = self.client.get(reverse('blog-render-post-comments', host='blog'), data=data, HTTP_HOST='blog')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post_comment.id)

    def test_render_posts_get_success(self):
        data = self.get_dumped_data([self.post], self.excluded_keys)
        data = {'posts': data}
        response = self.client.get(reverse('blog-render-posts', host='blog'), data=data, HTTP_HOST='blog')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.id)

    def test_render_categories_get_success(self):
        data = self.get_dumped_data([self.category], self.excluded_keys)
        data = {'categories': data}
        response = self.client.get(reverse('blog-render-categories', host='blog'), data=data, HTTP_HOST='blog')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.category.id)

    def get_dumped_data(self, obj_list, keys_to_exclude):
        lst = list()
        for obj in obj_list:
            data = model_to_dict(obj)
            for key in keys_to_exclude:
                data.pop(key)
            lst.append(data)

        return json.dumps(lst)
