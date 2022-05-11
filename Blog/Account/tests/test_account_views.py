import json
import uuid

from django.forms import model_to_dict
from django.test import TestCase, Client
from django_hosts import reverse

from core.User.factories import UserFactory
from core.Post.factories import PostFactory
from core.Likes.factories import PostLikeFactory


class AccountViewTestCase(TestCase):
    def setUp(self):
        self.password = str(uuid.uuid4())
        self.user = UserFactory.create(is_active=True)
        self.user.set_password(self.password)
        self.user.save()

        self.client = Client()
        self.client.login(username=self.user.email, password=self.password)

        self.post = PostFactory.create()
        PostLikeFactory.create(post=self.post, user=self.user)
        self.excluded_keys = ['created_stamp', 'archived_stamp']

    def test_index_get_success(self):
        response = self.client.get(reverse('profile', host='blog'), HTTP_HOST='blog')
        self.assertEqual(response.status_code, 200)

    def test_post_view_get_success(self):
        post = self.post
        response = self.client.get(reverse('profile-post-view', args=[post.slug], host='blog'), HTTP_HOST='blog')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, post.title)

    def test_account_post_add_form_success(self):
        response = self.client.get(reverse('profile-post-add-form', host='blog'), HTTP_HOST='blog')
        self.assertEqual(response.status_code, 200)

    def test_account_post_edit_form_success(self):
        data = {'post': json.dumps(self.post.id)}
        response = self.client.get(reverse('profile-post-edit-form', host='blog'), data=data, HTTP_HOST='blog')
        self.assertEqual(response.status_code, 200)

    def test_account_post_delete_form_success(self):
        data = {'post': json.dumps(self.post.id)}
        response = self.client.get(reverse('profile-post-delete-form', host='blog'), data=data, HTTP_HOST='blog')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.title)

    def test_account_render_post_success(self):
        data = {'post_id': json.dumps(self.post.id)}
        response = self.client.get(reverse('profile-render-post', host='blog'), data=data, HTTP_HOST='blog')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.id)

    def test_account_render_profile_form_get_success(self):
        response = self.client.get(reverse('profile-render-profile-form', host='blog'), HTTP_HOST='blog')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.email)

    def test_account_render_profile_password_form_get_success(self):
        response = self.client.get(reverse('profile-render-set-password-form', host='blog'), HTTP_HOST='blog')
        self.assertEqual(response.status_code, 200)

    def test_render_posts_list_get_success(self):
        data = self.get_dumped_data([self.post], self.excluded_keys)
        data = {'posts': data}
        response = self.client.get(reverse('profile-render-posts', host='blog'), data=data, HTTP_HOST='blog')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.id)

    def test_render_posts_liked_list_get_success(self):
        data = self.get_dumped_data([self.post], self.excluded_keys)
        data = {'posts': data}
        response = self.client.get(reverse('profile-render-liked-posts', host='blog'), data=data, HTTP_HOST='blog')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.id)

    def get_dumped_data(self, obj_list, keys_to_exclude):
        lst = list()
        for obj in obj_list:
            data = model_to_dict(obj)
            for key in keys_to_exclude:
                data.pop(key)
            lst.append(data)

        return json.dumps(lst)
