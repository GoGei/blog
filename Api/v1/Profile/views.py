from django.db.models.expressions import RawSQL
from rest_framework import generics, viewsets
# from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .serializers import ProfileSerializer, ProfileUpdateSerializer
from Api.v1.Post.serializers import PostListSerializer
from core.User.models import User
from core.Post.models import Post
from core.Likes.models import PostLike


# TODO remove user
USER = User.objects.get(pk=59)


class ProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [AllowAny]

    serializer_class = ProfileSerializer
    serializer_map = {
        'get': ProfileSerializer,
        'put': ProfileUpdateSerializer,
        'patch': ProfileUpdateSerializer,
    }
    queryset = User.objects.prefetch_related('post_set').all()

    def get_serializer_class(self):
        method = self.request.method.lower()
        serializer = self.serializer_map.get(method, self.serializer_class)
        return serializer

    def get_object(self):
        # queryset = self.get_queryset()
        # obj = get_object_or_404(queryset, pk=self.request.user.pk)
        obj = USER
        return obj

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        context = self.get_context()
        serializer = self.get_serializer(instance, data=request.data, partial=partial, context=context)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def get_context(self):
        instance = self.get_object()
        context = {'instance': instance}
        return context


class ProfilePostsView(viewsets.ReadOnlyModelViewSet):
    serializer_class = PostListSerializer

    def get_queryset(self):
        user = self.request.user
        if user and user.is_authenticated:
            return user.post_set.all()
        return Post.objects.none()

    def list(self, request, *args, **kwargs):
        user = request.user
        queryset = self.get_queryset()

        queryset = queryset.annotate(
            is_liked=RawSQL('select is_liked from post_likes where post_id=post.id and user_id=%s',
                            (user.id,)))  # noqa

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ProfileLikedView(viewsets.ReadOnlyModelViewSet):
    serializer_class = PostListSerializer
    queryset = PostLike.objects.select_related('post', 'user').filter(is_liked=True)

    def list(self, request, *args, **kwargs):
        # user = request.user
        user = USER
        liked_posts = self.get_queryset().filter(user=user).values_list('post_id', flat=True)
        queryset = Post.objects.select_related('author').filter(id__in=liked_posts).ordered()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
