from django.db import models
from django.utils.functional import cached_property

from core.Likes.models import PostLike
from core.Utils.Mixins.models import CrmMixin, SlugifyMixin


class Post(CrmMixin, SlugifyMixin):
    SLUGIFY_FIELD = 'title'

    author = models.ForeignKey('User.User', on_delete=models.PROTECT)
    category = models.ForeignKey('Category.Category', on_delete=models.PROTECT)
    title = models.CharField(max_length=100, unique=True)
    text = models.TextField()

    class Meta:
        db_table = 'post'

    def __str__(self):
        return self.label

    @property
    def label(self):
        return self.title or self.slug or f'Post: {self.id}'

    @property
    def created_date(self):
        return self.created_stamp.strftime('%d %B, %Y')

    @cached_property
    def likes_counter(self):
        return PostLike.objects.select_related('post').filter(post=self, is_liked=True).count()

    @cached_property
    def dislikes_counter(self):
        return PostLike.objects.select_related('post').filter(post=self, is_liked=False).count()
