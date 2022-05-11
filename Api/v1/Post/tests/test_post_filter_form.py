from django.test import TestCase

from core.User.factories import UserFactory
from core.Category.factories import CategoryFactory
from ..views import PostsFilter


class ApiTestPostsFilter(TestCase):
    def setUp(self):
        self.form = PostsFilter
        self.data = {
            'is_active': 'true',
            'category_is_active': 'true',
            'author': UserFactory.create(),
            'category': CategoryFactory.create(),
        }

    def test_form_valid(self):
        form = self.form(self.data)
        self.assertTrue(form.is_valid())
