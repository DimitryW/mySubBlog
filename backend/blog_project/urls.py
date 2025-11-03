# blog_project/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/blog/", include("blog.urls")),
    path("api/user/", include("accounts.urls")),
    path("api/paddle/", include("paddle_sync.urls")),
    path("ckeditor5/", include("django_ckeditor_5.urls")),
    path("accounts/", include("allauth.urls")),  # allauth 提供的登入/登出/社群登入路徑
    path("api/nowpayment/", include("nowpayment.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
