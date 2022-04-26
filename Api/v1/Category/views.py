from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
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

    @action(detail=False, methods=['get'])
    def name_by_slug(self, request):
        response = self._get_category_by_slug(request)
        if isinstance(response, Response):
            return response
        elif isinstance(response, Category):
            category = response
            return Response({'name': category.short_name}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def id_by_slug(self, request):
        response = self._get_category_by_slug(request)
        if isinstance(response, Response):
            return response
        elif isinstance(response, Category):
            category = response
            return Response({'id': category.id}, status=status.HTTP_200_OK)

    @classmethod
    def _get_category_by_slug(cls, request):
        slug = request.GET.get('slug')
        if slug:
            category_qs = Category.objects.filter(slug=slug)
            if category_qs.exists():
                category = category_qs.first()
                return category
            else:
                return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'Slug not provided in request GET arguments'},
                            status=status.HTTP_400_BAD_REQUEST)
