from django.test import TestCase

from ..models import Comment
from ..factories import CommentFactory
from core.Post.factories import PostFactory
from core.User.factories import UserFactory


class CommentTests(TestCase):
    def setUp(self):
        pass

    def test_create(self):
        obj = CommentFactory.create()
        qs = Comment.objects.filter(pk=obj.pk)
        self.assertTrue(qs.exists())
        self.assertEqual(qs[0], obj)

    def test_delete(self):
        obj = CommentFactory.create()
        obj.delete()

        qs = Comment.objects.filter(pk=obj.pk)
        self.assertFalse(qs.exists())

    def test_delete_cascade_user(self):
        author = UserFactory.create()
        obj = CommentFactory.create(author=author)
        author.delete()

        qs = Comment.objects.filter(pk=obj.pk)
        self.assertFalse(qs.exists())

    def test_delete_cascade_post(self):
        post = PostFactory.create()
        obj = CommentFactory.create(post=post)
        post.delete()

        qs = Comment.objects.filter(pk=obj.pk)
        self.assertFalse(qs.exists())
