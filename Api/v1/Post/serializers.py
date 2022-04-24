from rest_framework import serializers
from core.Post.models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'author', 'category', 'title', 'text', 'slug']


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['author', 'category', 'title', 'text']
