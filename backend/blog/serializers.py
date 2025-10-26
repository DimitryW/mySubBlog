# blog/serializers.py
from rest_framework import serializers
from .models import Post, Category, Comment


class CategorySerializer(serializers.ModelSerializer):
    posts_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = ["id", "name", "slug", "posts_count"]


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  # 顯示 username
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ["id", "user", "content", "parent", "replies", "created_at"]

    def get_replies(self, obj):
        # 僅取直接回覆 (單層)
        qs = obj.replies.all().order_by("created_at")
        return CommentSerializer(qs, many=True).data


class PostSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)
    category = CategorySerializer()
    tags = serializers.SlugRelatedField(many=True, slug_field="name", read_only=True)
    comments_count = serializers.IntegerField(read_only=True)

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
            "comments_count",
            "is_locked",
        ]
