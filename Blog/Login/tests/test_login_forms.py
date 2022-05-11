import uuid
import json

from django.test import TestCase
from core.User.models import User
from core.User.factories import UserFactory
from ..forms import RegistrationForm, LoginForm
from .test_login_data import registration_data, login_data


class TestRegistrationForm(TestCase):
    def setUp(self):
        self.form = RegistrationForm

    def test_registration_form_valid(self):
        data = registration_data.copy()
        form = self.form(data)
        self.assertTrue(form.is_valid())

    def test_registration_form_save(self):
        data = registration_data.copy()
        form = self.form(data)
        form.is_valid()
        user = form.save()
        self.assertTrue(User.objects.get(id=user.id))

    def test_registration_form_invalid_errors(self):
        user = UserFactory.create()
        user.phone = registration_data['phone']
        user.save()

        data = {
            'email': user.email,
            'phone': user.phone,
            'password': uuid.uuid4(),
            'repeat_password': uuid.uuid4(),
        }
        form = self.form(data)
        self.assertFalse(form.is_valid())
        errors = json.dumps(form.errors)
        for key in data.keys():
            self.assertIn(key, errors)


class TestLoginForm(TestCase):
    def setUp(self):
        self.form = LoginForm
        self.data = login_data.copy()

    def test_login_form_valid(self):
        data = self.data.copy()
        form = self.form(data)
        self.assertTrue(form.is_valid())
