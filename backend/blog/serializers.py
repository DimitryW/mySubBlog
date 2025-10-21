# blog/serializers.py
from rest_framework import serializers
from .models import Post, Category


class CategorySerializer(serializers.ModelSerializer):
    posts_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = ["id", "name", "slug", "posts_count"]


class PostSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)
    category = CategorySerializer()
    tags = serializers.SlugRelatedField(many=True, slug_field="name", read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "body",
            "author",
            "created_at",
            "image",
            "short_body",
            "category",
            "tags",
        ]
