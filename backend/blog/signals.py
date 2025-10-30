# blog/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post
from .tasks import notify_users_new_post
from decouple import config


@receiver(post_save, sender=Post)
def notify_users_on_new_post(sender, instance, created, **kwargs):
    if created:  # 只在新建立時觸發
        url = f"{config('FRONTEND_URL')}/posts/{instance.id}/"
        notify_users_new_post.delay(instance.id, instance.title, url)
