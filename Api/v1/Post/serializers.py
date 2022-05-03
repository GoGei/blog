from rest_framework import serializers
from Api.v1.Category.serializers import CategorySerializer
from Api.v1.User.serializers import UserSerializer
from core.Post.models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'author', 'category', 'title', 'text', 'slug']


class PostListSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    is_liked = serializers.BooleanField(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'author', 'category', 'title', 'text', 'slug', 'is_liked', 'created_date']


class PostCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'author', 'category', 'title', 'text', 'slug']

    def create(self, validated_data):
        instance = super().create(validated_data)
        instance.assign_slug()
        return instance

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        instance.assign_slug()
        return instance
