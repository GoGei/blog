import django_filters
from django_filters import rest_framework

from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response

from Api.permissions import IsStaffOrReadOnly, IsAdminOrReadOnly
from Api.v1.Post.serializers import PostsArchiveSerializer
from .serializers import CategorySerializer, CategoryCreateUpdateSerializer, CategoryListSerializer, \
    CategoryArchiveSerializer
from core.Category.models import Category


class CategoryFilter(rest_framework.FilterSet):
    is_active = django_filters.ChoiceFilter(label='Is active', empty_label='Not selected', method='is_active_filter',
                                            choices=[('true', 'Active'), ('false', 'Not active')])

    class Meta:
        model = Category
        fields = ['is_active']

    def is_active_filter(self, queryset, name, value):
        if value == 'true':
            queryset = queryset.filter(archived_stamp__isnull=True)
        elif value == 'false':
            queryset = queryset.filter(archived_stamp__isnull=False)
        return queryset


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsStaffOrReadOnly]

    queryset = Category.objects.all().ordered()
    serializer_class = CategorySerializer
    serializer_map = {
        'list': CategoryListSerializer,
        'create': CategoryCreateUpdateSerializer,
        'update': CategoryCreateUpdateSerializer,
    }

    category_archive_serializer_class = CategoryArchiveSerializer
    posts_archive_serializer_class = PostsArchiveSerializer

    filter_backends = [filters.SearchFilter, filters.OrderingFilter, rest_framework.DjangoFilterBackend]
    search_fields = ['name', 'slug']
    filterset_class = CategoryFilter
    ordering_fields = ['position']

    def get_serializer_class(self):
        serializer = self.serializer_map.get(self.action, self.serializer_class)
        return serializer

    @action(detail=True, methods=['post'], permission_classes=[IsAdminOrReadOnly])
    def archive(self, request, pk=None):
        category = self.get_object()
        posts = category.post_set.all()
        posts.archive(request.user)
        category_data = self.category_archive_serializer_class(category).data
        posts_data = self.posts_archive_serializer_class(posts, many=True).data
        return Response({'category': category_data, 'posts': posts_data}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAdminOrReadOnly])
    def restore(self, request, pk=None):
        category = self.get_object()
        posts = category.post_set.all()
        posts.restore(request.user)
        category_data = self.category_archive_serializer_class(category).data
        posts_data = self.posts_archive_serializer_class(posts, many=True).data
        return Response({'category': category_data, 'posts': posts_data}, status=status.HTTP_200_OK)

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
