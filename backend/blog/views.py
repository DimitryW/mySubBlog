from django.shortcuts import render, get_object_or_404
from .models import Post, Category
from rest_framework import viewsets
from .serializers import PostSerializer, CategorySerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


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
    queryset = Category.objects.all().order_by("name")
    serializer_class = CategorySerializer
    pagination_class = None
    lookup_field = "slug"

    @action(detail=True, methods=["get"])
    def posts(self, request, slug=None):
        category = self.get_object()
        posts = Post.objects.filter(category=category).order_by("-created_at")
        paginator = CategoryPagination()
        page = paginator.paginate_queryset(posts, request)
        serializer = PostSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by("-created_at")
    serializer_class = PostSerializer

    def get_permissions(self):
        """
        列表公開，但 retrieve 文章內容需要登入
        """

        if self.action == "list":
            return [AllowAny()]
        else:  # retrieve, create, update, delete
            return [IsAuthenticated()]

    @action(detail=False, methods=["get"], url_path="tag/(?P<tag>[^/.]+)")
    def by_tag(self, request, tag=None):
        posts = Post.objects.filter(tags__name=tag).order_by("-created_at")
        paginator = TagsPostPagination()
        page = paginator.paginate_queryset(posts, request)
        serializer = self.get_serializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
