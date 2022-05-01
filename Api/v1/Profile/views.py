from django.db.models import BooleanField
from django.db.models.expressions import RawSQL, Case
from rest_framework import generics, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .serializers import ProfileSerializer
from Api.v1.Post.serializers import PostListSerializer
from core.User.models import User
from core.Post.models import Post
from core.Likes.models import PostLike


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    posts_serializer_class = PostListSerializer
    queryset = User.objects.prefetch_related('post_set').all()

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=self.request.user.pk)
        return obj


class ProfilePostsView(viewsets.ReadOnlyModelViewSet):
    serializer_class = PostListSerializer

    def get_queryset(self):
        return self.request.user.post_set.all()

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
        user = request.user
        liked_posts = self.get_queryset().filter(user=user).values_list('post_id', flat=True)
        queryset = Post.objects.select_related('author').filter(id__in=liked_posts).ordered()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
