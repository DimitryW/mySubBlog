# blog/serializers.py
from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = Post
        fields = ["id", "title", "body", "author", "created_at", "image", "short_body"]
