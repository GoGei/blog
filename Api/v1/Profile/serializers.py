from rest_framework import serializers
from core.User.models import User


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'label', 'is_active', 'is_staff', 'is_superuser']
