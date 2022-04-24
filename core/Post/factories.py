import factory
from django.utils.text import slugify
from factory import fuzzy, SubFactory
from faker import Faker

from .models import Post
from core.User.factories import UserFactory
from core.Category.factories import CategoryFactory
faker = Faker()


class PostFactory(factory.DjangoModelFactory):
    author = SubFactory(UserFactory)
    category = SubFactory(CategoryFactory)
    title = fuzzy.FuzzyText(length=100)
    text = faker.text()

    slug = factory.LazyAttribute(lambda o: slugify(o.title))

    class Meta:
        model = Post
        django_get_or_create = ('slug',)
