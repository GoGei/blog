from django.test import TestCase
from ..forms import PostForm, ProfileForm, ResetPasswordForm
from .test_account_data import post_form_data, profile_form_data, reset_password_data
from core.Category.factories import CategoryFactory


class TestPostForm(TestCase):
    def setUp(self):
        self.form = PostForm
        self.data = post_form_data.copy()
        category = CategoryFactory.create()
        self.data['category'] = category.id

    def test_post_form_valid(self):
        data = self.data.copy()
        form = self.form(data)
        self.assertTrue(form.is_valid())


class TestProfileForm(TestCase):
    def setUp(self):
        self.form = ProfileForm
        self.data = profile_form_data.copy()

    def test_post_form_valid(self):
        data = self.data.copy()
        form = self.form(data)
        self.assertTrue(form.is_valid())


class TestResetPasswordForm(TestCase):
    def setUp(self):
        self.form = ResetPasswordForm
        self.data = reset_password_data.copy()

    def test_post_form_valid(self):
        data = self.data.copy()
        form = self.form(data)
        self.assertTrue(form.is_valid())
