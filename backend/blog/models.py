from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.urls import reverse
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.html import strip_tags
from django.utils.text import slugify
from taggit.managers import TaggableManager


class Post(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    body = CKEditor5Field(config_name="extends")
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="posts/images/", blank=True, null=True)
    category = models.ForeignKey(
        "Category",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="posts",
    )
    tags = TaggableManager(blank=True)
    is_locked = models.BooleanField(default=False, help_text="是否僅限訂閱者閱讀")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        text = strip_tags(self.body)
        text = text.replace("\n", " ")
        return reverse("post_detail", kwargs={"pk": self.pk})

    @property
    def short_body(self):
        text = strip_tags(self.body)  # 移除 HTML 標籤
        text = text.replace("\n", " ")  # 換行轉空格
        return text[:500] + "…" if len(text) > 500 else text


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True, allow_unicode=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE, related_name="replies"
    )
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}: {self.content[:20]}"
