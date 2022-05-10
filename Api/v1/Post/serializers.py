from rest_framework import serializers
from Api.v1.Category.serializers import CategorySerializer
from Api.v1.User.serializers import UserSerializer
from core.Post.models import Post
from core.Likes.models import PostLike


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


class PostRetrieveSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    is_liked = serializers.SerializerMethodField()
    likes_counter = serializers.SerializerMethodField()
    dislikes_counter = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'author', 'category', 'title', 'text', 'slug', 'is_liked', 'created_date', 'likes_counter',
                  'dislikes_counter']

    def get_is_liked(self, obj):
        user = self.context.get('user')
        if user.is_authenticated:
            like = PostLike.objects.select_related('post', 'user').filter(post=obj, user=user).first()
            if like:
                return like.is_liked
        return False

    def get_likes_counter(self, obj):
        return PostLike.objects.select_related('post').filter(post=obj, is_liked=True).count()

    def get_dislikes_counter(self, obj):
        return PostLike.objects.select_related('post').filter(post=obj, is_liked=False).count()


class PostCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'author', 'category', 'title', 'text', 'slug']
        read_only_fields = ['id', 'slug']

    def create(self, validated_data):
        instance = super().create(validated_data)
        instance.assign_slug()
        return instance

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        instance.assign_slug()
        return instance
