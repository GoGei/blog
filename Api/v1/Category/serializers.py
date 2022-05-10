from rest_framework import serializers
from core.Category.models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'position', 'slug', 'short_name']


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'position', 'slug', 'short_name', 'is_active']
        read_only_fields = ['id', 'slug', 'is_active']


class CategoryArchiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']


class CategoryCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'slug', 'name', 'position']
        read_only_fields = ['id', 'slug']

    def validate(self, data):
        name = data['name']
        if not Category.is_allowed_to_assign_slug(name):
            raise serializers.ValidationError(
                {'name': 'This name cause creation of the existing slug. Please, change the name.'})

        return data

    def create(self, validated_data):
        instance = super().create(validated_data)
        instance.assign_slug()
        return instance

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        instance.assign_slug()
        return instance
