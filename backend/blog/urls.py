# blog/urls.py
from django.urls import path, include

# from .views import post_list, post_detail
from .views import PostViewSet, home, CategoryViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("posts", PostViewSet)
router.register("categories", CategoryViewSet, basename="category")

urlpatterns = [
    path("", include(router.urls)),  # /api/blog/posts/
    path("home/", home, name="home"),
]
