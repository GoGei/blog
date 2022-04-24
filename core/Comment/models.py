from django.db import models
from core.Utils.Mixins.models import CrmMixin


class Comment(CrmMixin):
    author = models.ForeignKey('User.User', on_delete=models.CASCADE)
    post = models.ForeignKey('Post.Post', on_delete=models.CASCADE)
    text = models.CharField(max_length=512)

    class Meta:
        db_table = 'comment'
