from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from Api.permissions import IsStaffOrReadOnly
from .serializers import CategorySerializer, CategoryCreateUpdateSerializer
from core.Category.models import Category


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsStaffOrReadOnly]

    queryset = Category.objects.all().ordered()
    serializer_class = CategorySerializer
    serializer_map = {
        'create': CategoryCreateUpdateSerializer,
        'update': CategoryCreateUpdateSerializer,
    }

    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['name', 'slug']
    ordering_fields = ['position']

    def get_serializer_class(self):
        serializer = self.serializer_map.get(self.action, self.serializer_class)
        return serializer

    @action(detail=False, methods=['get'])
    def get_by_slug(self, request):
        slug = request.GET.get('slug')
        if slug:
            category_qs = Category.objects.filter(slug=slug)
            if category_qs.exists():
                category = category_qs.first()
                data = self.serializer_class(category).data
                return Response({'category': data}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'slug': 'Slug not provided in request GET arguments'},
                            status=status.HTTP_400_BAD_REQUEST)
