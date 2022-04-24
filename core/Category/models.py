from django.db import models
from core.Utils.Mixins.models import CrmMixin, SlugifyMixin


class Category(CrmMixin, SlugifyMixin):
    SLUGIFY_FIELD = 'name'
    name = models.CharField(max_length=50, unique=True)
    position = models.IntegerField(null=True)

    class Meta:
        db_table = 'category'

    @property
    def label(self):
        return self.name or self.slug or f'Post: {self.id}'

