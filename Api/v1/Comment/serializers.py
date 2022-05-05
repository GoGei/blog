from rest_framework import serializers
from Api.v1.Post.serializers import PostSerializer
from Api.v1.User.serializers import UserSerializer
from core.Comment.models import Comment
from core.Likes.models import CommentLike


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'author', 'post', 'text']


class CommentListSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    post = PostSerializer(read_only=True)
    is_liked = serializers.BooleanField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'author', 'post', 'text', 'is_liked']


class CommentListPostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    is_liked = serializers.BooleanField(read_only=True)
    is_author = serializers.BooleanField(read_only=True)
    likes_counter = serializers.SerializerMethodField()
    dislikes_counter = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'author', 'text', 'is_liked', 'is_author', 'likes_counter', 'dislikes_counter']

    def get_likes_counter(self, obj):
        return CommentLike.objects.select_related('comment').filter(comment=obj, is_liked=True).count()

    def get_dislikes_counter(self, obj):
        return CommentLike.objects.select_related('comment').filter(comment=obj, is_liked=False).count()



class CommentCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'author', 'post', 'text']
