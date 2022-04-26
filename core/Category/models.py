from django.db import models
from core.Utils.Mixins.models import CrmMixin, SlugifyMixin


class Category(CrmMixin, SlugifyMixin):
    SLUGIFY_FIELD = 'name'
    CHARS_FOR_SHORT_NAME = 35
    name = models.CharField(max_length=50, unique=True)
    position = models.IntegerField(null=True)

    class Meta:
        db_table = 'category'

    def __str__(self):
        return self.label

    @property
    def label(self):
        return self.name or self.slug or f'Category: {self.id}'

    @property
    def short_name(self):
        name = self.name
        chars = self.CHARS_FOR_SHORT_NAME
        return name if len(name) < chars else name[:chars-5] + '...'
