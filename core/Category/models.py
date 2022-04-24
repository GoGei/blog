from django.db import models
from django.template.defaultfilters import slugify
from core.Utils.Mixins.models import CrmMixin


class Category(CrmMixin):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True, db_index=True)
    position = models.IntegerField(null=True)

    class Meta:
        db_table = 'category'

    @property
    def label(self):
        return self.name or self.slug

    @classmethod
    def is_allowed_to_assign_slug(cls, title, instance=None):
        slug = slugify(title)
        qs = cls.objects.filter(slug=slug)
        if instance:
            qs = qs.exclude(pk=instance.pk)
        return not qs.exists()

    def assign_slug(self):
        self.slug = slugify(self.name)
        self.save()
        return self
