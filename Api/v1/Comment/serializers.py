from rest_framework import serializers
from Api.v1.Post.serializers import PostSerializer
from Api.v1.User.serializers import UserSerializer
from core.Comment.models import Comment


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

    class Meta:
        model = Comment
        fields = ['id', 'author', 'text', 'is_liked', 'is_author']


class CommentCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'author', 'post', 'text']
