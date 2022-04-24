import factory
from factory import fuzzy
from django.template.defaultfilters import slugify
from .models import Category


class CategoryFactory(factory.DjangoModelFactory):
    name = fuzzy.FuzzyText(length=50)
    slug = factory.LazyAttribute(lambda o: slugify(o.name))
    position = fuzzy.FuzzyInteger(low=0, high=100)

    class Meta:
        model = Category
        django_get_or_create = ('slug',)
