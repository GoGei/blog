from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import CategorySerializer, CategoryCreateUpdateSerializer
from core.Category.models import Category


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().ordered()
    serializer_class = CategorySerializer
    serializer_map = {
        'create': CategoryCreateUpdateSerializer,
        'update': CategoryCreateUpdateSerializer,
    }

    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['name']
    ordering_fields = ['position']

    def get_serializer_class(self):
        serializer = self.serializer_map.get(self.action, self.serializer_class)
        return serializer
