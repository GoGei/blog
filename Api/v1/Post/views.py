from django.db.models.expressions import RawSQL
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import PostSerializer, PostCreateUpdateSerializer, PostListSerializer
from core.Post.models import Post
from core.Likes.models import PostLike


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.select_related('author', 'category').ordered()
    serializer_class = PostSerializer
    serializer_map = {
        'create': PostCreateUpdateSerializer,
        'update': PostCreateUpdateSerializer,
        'list': PostListSerializer,
    }

    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['title', 'author__email', 'text']
    filterset_fields = ['category', 'author']
    ordering_fields = ['title']

    def get_serializer_class(self):
        serializer = self.serializer_map.get(self.action, self.serializer_class)
        return serializer

    def list(self, request, *args, **kwargs):
        user = request.user
        queryset = self.filter_queryset(self.get_queryset())

        queryset = queryset.annotate(
            is_liked=RawSQL('select is_liked from post_likes where post_id=post.id and user_id=%s',
                               (user.id,)))  # noqa

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get', 'post'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user
        obj, _ = PostLike.objects.get_or_create(post=post, user=user)
        obj.like()
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=['get', 'post'], permission_classes=[IsAuthenticated])
    def dislike(self, request, pk=None):
        post = self.get_object()
        user = request.user
        obj, _ = PostLike.objects.get_or_create(post=post, user=user)
        obj.dislike()
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=['get', 'post'], permission_classes=[IsAuthenticated])
    def deactivate(self, request, pk=None):
        post = self.get_object()
        user = request.user
        obj, _ = PostLike.objects.get_or_create(post=post, user=user)
        obj.deactivate()
        return Response(status=status.HTTP_200_OK)
