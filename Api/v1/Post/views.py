import django_filters
from django_filters import rest_framework
from django.db.models import Case, When
from django.db.models.expressions import RawSQL
from rest_framework import viewsets, filters, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import PostSerializer, PostCreateUpdateSerializer, PostListSerializer, PostRetrieveSerializer
from Api.v1.Comment.serializers import CommentCreateUpdateSerializer, CommentListPostSerializer
from Api.permissions import IsOwnerOrReadOnly
from core.Post.models import Post
from core.Likes.models import PostLike


class PostsFilter(rest_framework.FilterSet):
    is_active = django_filters.ChoiceFilter(label='Is active', empty_label='Not selected', method='is_active_filter',
                                            choices=[('true', 'Active'), ('false', 'Not active')])
    category_is_active = django_filters.ChoiceFilter(label='Category is active', empty_label='Not selected',
                                                     method='category_is_active_filter',
                                                     choices=[('true', 'Active'), ('false', 'Not active')])

    class Meta:
        model = Post
        fields = ['category', 'author', 'is_active', 'category_is_active']

    def is_active_filter(self, queryset, name, value):
        if value == 'true':
            queryset = queryset.filter(archived_stamp__isnull=True)
        elif value == 'false':
            queryset = queryset.filter(archived_stamp__isnull=False)
        return queryset

    def category_is_active_filter(self, queryset, name, value):
        if value == 'true':
            queryset = queryset.filter(category__archived_stamp__isnull=True)
        elif value == 'false':
            queryset = queryset.filter(category__archived_stamp__isnull=False)
        return queryset


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly, permissions.IsAuthenticatedOrReadOnly]

    queryset = Post.objects.select_related('author', 'category').ordered()
    serializer_class = PostSerializer
    serializer_map = {
        'create': PostCreateUpdateSerializer,
        'update': PostCreateUpdateSerializer,
        'list': PostListSerializer,
        'retrieve': PostRetrieveSerializer,
        'comment': CommentCreateUpdateSerializer,
        'comments': CommentListPostSerializer
    }

    filter_backends = [filters.SearchFilter, filters.OrderingFilter, rest_framework.DjangoFilterBackend]
    search_fields = ['title', 'author__email', 'text']
    filterset_class = PostsFilter
    # filterset_fields = ['category', 'author'']
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

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        context = {'user': self.request.user}
        serializer = self.get_serializer(instance, context=context)
        return Response(serializer.data)

    def _get_modified_request_data(self, request):
        data = request.data.copy()
        data['author'] = request.user.id
        return data

    @action(detail=True, methods=['get', 'post'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user
        obj, _ = PostLike.objects.get_or_create(post=post, user=user)
        obj.like()
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=['get', 'post'], permission_classes=[permissions.IsAuthenticated])
    def dislike(self, request, pk=None):
        post = self.get_object()
        user = request.user
        obj, _ = PostLike.objects.get_or_create(post=post, user=user)
        obj.dislike()
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=['get', 'post'], permission_classes=[permissions.IsAuthenticated])
    def deactivate(self, request, pk=None):
        post = self.get_object()
        user = request.user
        obj, _ = PostLike.objects.get_or_create(post=post, user=user)
        obj.deactivate()
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def comment(self, request, pk=None):
        post = self.get_object()
        user = request.user
        text = self.request.data.get('text', None)
        data = {
            'author': user.id,
            'post': post.id,
            'text': text,
        }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        post = self.get_object()
        user = request.user
        queryset = post.comment_set.active().all().ordered()

        queryset = queryset.annotate(
            is_liked=RawSQL('select is_liked from comment_likes where comment_id=comment.id and user_id=%s',
                            (user.id,)))  # noqa

        queryset = queryset.annotate(is_author=Case(When(author_id=user.id, then=True), default=False))  # noqa

        params = request.GET
        if params:
            order_by = params.get('order_by')
            if order_by:
                queryset = queryset.order_by(order_by)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
