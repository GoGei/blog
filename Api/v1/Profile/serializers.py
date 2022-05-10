from rest_framework import serializers
from core.User.models import User
from core.Likes.models import PostLike
from core.Utils.validators import PhoneValidator


class ProfileSerializer(serializers.ModelSerializer):
    likes_counter = serializers.SerializerMethodField()
    posts_counter = serializers.SerializerMethodField()
    comments__counter = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'phone', 'label', 'full_name',
                  'likes_counter', 'posts_counter', 'comments__counter']

    def get_likes_counter(self, obj):
        return PostLike.objects.select_related('user').filter(user=obj).count()

    def get_posts_counter(self, obj):
        return obj.post_set.active().count()

    def get_comments__counter(self, obj):
        return obj.comment_set.active().count()


class ProfileUpdateSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(validators=[PhoneValidator])

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'phone']
        read_only = ['id']
