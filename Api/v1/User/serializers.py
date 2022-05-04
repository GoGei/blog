from rest_framework import serializers
from core.User.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'phone', 'label', 'full_name', 'is_active', 'is_staff',
                  'is_superuser']


class UserCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone', 'is_active', 'is_staff', 'is_superuser']


class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        required=True, min_length=8, max_length=36,
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    repeat_password = serializers.CharField(
        required=True, min_length=8, max_length=36,
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    def validate(self, data):
        if data['password'] != data['repeat_password']:
            raise serializers.ValidationError({'password': 'Password mismatched!'})
        return data
