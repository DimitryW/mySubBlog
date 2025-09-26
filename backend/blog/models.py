from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.html import strip_tags


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    body = CKEditor5Field()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="posts/images/", blank=True, null=True)

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
        return text[:200] + "…" if len(text) > 200 else text
