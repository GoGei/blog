from django.db import models
from django.utils.functional import cached_property

from core.Utils.Mixins.models import CrmMixin
from core.Likes.models import CommentLike


class Comment(CrmMixin):
    author = models.ForeignKey('User.User', on_delete=models.CASCADE)
    post = models.ForeignKey('Post.Post', on_delete=models.CASCADE)
    text = models.CharField(max_length=512)

    class Meta:
        db_table = 'comment'

    @cached_property
    def likes_counter(self):
        return CommentLike.objects.select_related('comment').filter(comment=self, is_liked=True).count()

    @cached_property
    def dislikes_counter(self):
        return CommentLike.objects.select_related('comment').filter(comment=self, is_liked=False).count()

