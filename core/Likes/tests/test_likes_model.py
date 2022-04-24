from django.test import TestCase

from ..models import PostLike, CommentLike
from ..factories import PostLikeFactory, CommentLikeFactory
from core.Post.factories import PostFactory
from core.Comment.factories import CommentFactory
from core.User.factories import UserFactory


class PostLikeTests(TestCase):
    def test_create(self):
        obj = PostLikeFactory.create()
        qs = PostLike.objects.filter(pk=obj.pk)
        self.assertTrue(qs.exists())
        self.assertEqual(qs[0], obj)

    def test_delete(self):
        obj = PostLikeFactory.create()
        obj.delete()

        qs = PostLike.objects.filter(pk=obj.pk)
        self.assertFalse(qs.exists())

    def test_delete_cascade_user(self):
        user = UserFactory.create()
        obj = PostLikeFactory.create(user=user)
        user.delete()

        qs = PostLike.objects.filter(pk=obj.pk)
        self.assertFalse(qs.exists())

    def test_delete_cascade_post(self):
        post = PostFactory.create()
        obj = PostLikeFactory.create(post=post)
        post.delete()

        qs = PostLike.objects.filter(pk=obj.pk)
        self.assertFalse(qs.exists())


class CommentLikeTests(TestCase):
    def test_create(self):
        obj = CommentLikeFactory.create()
        qs = CommentLike.objects.filter(pk=obj.pk)
        self.assertTrue(qs.exists())
        self.assertEqual(qs[0], obj)

    def test_delete(self):
        obj = CommentLikeFactory.create()
        obj.delete()

        qs = CommentLike.objects.filter(pk=obj.pk)
        self.assertFalse(qs.exists())

    def test_delete_cascade_user(self):
        user = UserFactory.create()
        obj = CommentLikeFactory.create(user=user)
        user.delete()

        qs = CommentLike.objects.filter(pk=obj.pk)
        self.assertFalse(qs.exists())

    def test_delete_cascade_post(self):
        comment = CommentFactory.create()
        obj = CommentLikeFactory.create(comment=comment)
        comment.delete()

        qs = CommentLike.objects.filter(pk=obj.pk)
        self.assertFalse(qs.exists())
