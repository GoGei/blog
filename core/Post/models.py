from django.db import models
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
