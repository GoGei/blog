from django.db import models
from core.Utils.Mixins.models import LikeMixin


class PostLike(LikeMixin):
    post = models.ForeignKey('Post.Post', on_delete=models.CASCADE)

    class Meta:
        db_table = 'post_likes'


class CommentLike(LikeMixin):
    comment = models.ForeignKey('Comment.Comment', on_delete=models.CASCADE)

    class Meta:
        db_table = 'comment_likes'
