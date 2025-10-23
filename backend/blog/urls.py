# blog/urls.py
from django.urls import path, include

# from .views import post_list, post_detail
from .views import PostViewSet, home, CategoryViewSet, CommentViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("posts", PostViewSet)
router.register("categories", CategoryViewSet, basename="category")

urlpatterns = [
    path("", include(router.urls)),  # /api/blog/posts/
    path("home/", home, name="home"),
    path(
        "posts/<int:post_id>/comments/", CommentViewSet.as_view(), name="post-comments"
    ),
]
