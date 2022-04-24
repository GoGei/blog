import factory
from factory import SubFactory

from core.Post.factories import PostFactory
from core.Comment.factories import CommentFactory
from .models import PostLike, CommentLike


class PostLikeFactory(factory.DjangoModelFactory):
    is_liked = True
    post = SubFactory(PostFactory)

    class Meta:
        model = PostLike


class CommentLikeFactory(factory.DjangoModelFactory):
    is_liked = True
    comment = SubFactory(CommentFactory)

    class Meta:
        model = CommentLike
