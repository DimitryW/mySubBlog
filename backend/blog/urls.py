# blog/urls.py
from django.urls import path, include

# from .views import post_list, post_detail
from .views import PostViewSet, home
from rest_framework.routers import DefaultRouter

# urlpatterns = [
#     path("", post_list, name="home"),
#     path("post/<int:pk>/", post_detail, name="post_detail"),
# ]
router = DefaultRouter()
router.register("posts", PostViewSet)

urlpatterns = [
    path("", include(router.urls)),  # /api/blog/posts/
    path("home/", home, name="home"),
]
