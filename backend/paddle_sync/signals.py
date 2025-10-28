from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .tasks import create_paddle_customer_task


@receiver(post_save, sender=User)
def enqueue_paddle_customer_creation(sender, instance, created, **kwargs):
    """在用戶註冊後，觸發 Celery 任務建立 Paddle Customer"""
    if created:
        print(
            f"[Paddle Sync] Enqueue Paddle customer creation for user {instance.username}"
        )
        create_paddle_customer_task.delay(instance.id)
