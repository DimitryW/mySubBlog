from django.shortcuts import render, get_object_or_404
from .models import Post, Category, Comment
from rest_framework import viewsets, generics
from .serializers import PostSerializer, CategorySerializer, CommentSerializer
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Count


def home(request):
    return render(request, "home.html")


class CategoryPagination(PageNumberPagination):
    page_size = 10  # 每頁 10 筆
    page_size_query_param = "page_size"  # 可以用 ?page_size=5 調整
    max_page_size = 50


class TagsPostPagination(PageNumberPagination):
    page_size = 10  # 每頁 10 筆
    page_size_query_param = "page_size"  # 可以用 ?page_size=5 調整
    max_page_size = 50


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.annotate(posts_count=Count("posts")).order_by("name")
    serializer_class = CategorySerializer
    pagination_class = None
    lookup_field = "slug"

    @action(detail=True, methods=["get"])
    def posts(self, request, slug=None):
        category = self.get_object()
        posts = (
            Post.objects.filter(category=category)
            .annotate(comments_count=Count("comments"))
            .order_by("-created_at")
        )
        paginator = CategoryPagination()
        page = paginator.paginate_queryset(posts, request)
        serializer = PostSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)


class CommentViewSet(generics.ListCreateAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs["post_id"]
        return Comment.objects.filter(post_id=post_id, parent=None).order_by(
            "-created_at"
        )

    def perform_create(self, serializer):
        comment = serializer.save(
            user=self.request.user, post_id=self.kwargs["post_id"]
        )
        if comment.parent and self.request.user.is_staff:
            Comment.objects.filter(pk__in=[comment.pk, comment.parent.pk]).update(
                is_read=True
            )

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated()]
        return [AllowAny()]

    permission_classes = [IsAuthenticatedOrReadOnly]


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.annotate(comments_count=Count("comments")).order_by(
        "-created_at"
    )
    serializer_class = PostSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        else:  # create, update, delete
            return [IsAuthenticated()]

    @action(detail=False, methods=["get"], url_path="tag/(?P<tag>[^/.]+)")
    def by_tag(self, request, tag=None):
        posts = (
            Post.objects.filter(tags__name=tag)
            .annotate(comments_count=Count("comments"))
            .order_by("-created_at")
        )
        paginator = TagsPostPagination()
        page = paginator.paginate_queryset(posts, request)
        serializer = self.get_serializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    @action(detail=False, methods=["get"], url_path="members-only")
    def members_only(self, request):
        posts = (
            Post.objects.filter(is_locked=True)
            .annotate(comments_count=Count("comments"))
            .order_by("-created_at")
        )

        paginator = TagsPostPagination()
        page = paginator.paginate_queryset(posts, request)
        serializer = self.get_serializer(page, many=True)

        return paginator.get_paginated_response(serializer.data)
