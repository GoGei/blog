import factory
from factory import SubFactory
from faker import Faker

from .models import Comment
from core.Post.factories import PostFactory
from core.User.factories import UserFactory

faker = Faker()


class CommentFactory(factory.DjangoModelFactory):
    author = SubFactory(UserFactory)
    post = SubFactory(PostFactory)
    text = faker.text()

    class Meta:
        model = Comment
