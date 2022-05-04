from rest_framework import serializers
from core.User.models import User
from core.Utils.validators import PhoneValidator


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'phone', 'label', 'full_name']


class ProfileUpdateSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(validators=[PhoneValidator])

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone']
