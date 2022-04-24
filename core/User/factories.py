import factory
from factory import faker
from .models import User


class UserFactory(factory.DjangoModelFactory):
    email = faker.Faker('email')
    is_active = True
    is_staff = False
    is_superuser = False

    class Meta:
        model = User


class StaffFactory(UserFactory):
    is_staff = True
    is_superuser = False

    class Meta:
        model = User


class SuperuserFactory(UserFactory):
    is_staff = True
    is_superuser = True

    class Meta:
        model = User
