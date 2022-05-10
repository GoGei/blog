import factory
from factory import SubFactory

from core.Post.factories import PostFactory
from core.Comment.factories import CommentFactory
from core.User.factories import UserFactory
from .models import PostLike, CommentLike


class PostLikeFactory(factory.DjangoModelFactory):
    is_liked = True
    user = SubFactory(UserFactory)
    post = SubFactory(PostFactory)

    class Meta:
        model = PostLike


class CommentLikeFactory(factory.DjangoModelFactory):
    is_liked = True
    user = SubFactory(UserFactory)
    comment = SubFactory(CommentFactory)

    class Meta:
        model = CommentLike
