from django.db.models.expressions import RawSQL
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import CommentSerializer, CommentCreateUpdateSerializer, CommentListSerializer
from core.Comment.models import Comment
from core.Likes.models import CommentLike


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related('author', 'post').ordered()
    serializer_class = CommentSerializer
    serializer_map = {
        'create': CommentCreateUpdateSerializer,
        'update': CommentCreateUpdateSerializer,
        'list': CommentListSerializer,
    }

    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['post__title', 'author__email']
    filterset_fields = ['post', 'author']

    def get_serializer_class(self):
        serializer = self.serializer_map.get(self.action, self.serializer_class)
        return serializer

    def list(self, request, *args, **kwargs):
        user = request.user
        queryset = self.filter_queryset(self.get_queryset())

        queryset = queryset.annotate(
            is_liked=RawSQL('select is_liked from comment_likes where comment_id=comment.id and user_id=%s',
                            (user.id,)))  # noqa

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get', 'post'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        comment = self.get_object()
        user = request.user
        obj, _ = CommentLike.objects.get_or_create(comment=comment, user=user)
        obj.like()
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=['get', 'post'], permission_classes=[IsAuthenticated])
    def dislike(self, request, pk=None):
        comment = self.get_object()
        user = request.user
        obj, _ = CommentLike.objects.get_or_create(comment=comment, user=user)
        obj.dislike()
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=['get', 'post'], permission_classes=[IsAuthenticated])
    def deactivate(self, request, pk=None):
        comment = self.get_object()
        user = request.user
        obj, _ = CommentLike.objects.get_or_create(comment=comment, user=user)
        obj.deactivate()
        return Response(status=status.HTTP_200_OK)
