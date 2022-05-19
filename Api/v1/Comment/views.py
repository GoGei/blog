from django.db.models.expressions import RawSQL
from rest_framework import viewsets, filters, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import CommentSerializer, CommentCreateUpdateSerializer, CommentListSerializer
from Api.permissions import IsOwnerOrReadOnly
from core.Comment.models import Comment
from core.Likes.models import CommentLike


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly, permissions.IsAuthenticatedOrReadOnly]

    queryset = Comment.objects.select_related('author', 'post').ordered()
    serializer_class = CommentSerializer
    serializer_map = {
        'create': CommentCreateUpdateSerializer,
        'update': CommentCreateUpdateSerializer,
        'list': CommentListSerializer,
    }

    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['post__title', 'author__email']
    filterset_fields = ['post', 'author']
    ordering_fields = ['id', 'created_stamp']

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

    def create(self, request, *args, **kwargs):
        data = self._get_modified_request_data(request)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data = self._get_modified_request_data(request)
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def _get_modified_request_data(self, request):
        data = request.data.copy()
        data['author'] = request.user.id
        return data

    @action(detail=True, methods=['get', 'post'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        comment = self.get_object()
        user = request.user
        obj, _ = CommentLike.objects.get_or_create(comment=comment, user=user)
        obj.like()
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=['get', 'post'], permission_classes=[permissions.IsAuthenticated])
    def dislike(self, request, pk=None):
        comment = self.get_object()
        user = request.user
        obj, _ = CommentLike.objects.get_or_create(comment=comment, user=user)
        obj.dislike()
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=['get', 'post'], permission_classes=[permissions.IsAuthenticated])
    def deactivate(self, request, pk=None):
        comment = self.get_object()
        user = request.user
        obj, _ = CommentLike.objects.get_or_create(comment=comment, user=user)
        obj.deactivate()
        return Response(status=status.HTTP_200_OK)
