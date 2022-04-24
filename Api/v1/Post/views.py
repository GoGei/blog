from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import PostSerializer, PostCreateSerializer
from core.Post.models import Post


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.select_related('author', 'category').ordered()
    serializer_class = PostSerializer
    serializer_map = {
        'create': PostCreateSerializer,
    }

    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['title', 'author__email']
    filterset_fields = ['category', 'author']
    ordering_fields = ['title']

    def get_serializer_class(self):
        serializer = self.serializer_map.get(self.action, self.serializer_class)
        return serializer
