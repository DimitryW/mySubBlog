from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()


# # Delete avatar file from storage when Profile is deleted
# @receiver(post_delete, sender=Profile)
# def delete_avatar_on_profile_delete(sender, instance, **kwargs):
#     if instance.avatar and instance.avatar.storage.exists(instance.avatar.name):
#         instance.avatar.storage.delete(instance.avatar.name)


# # Delete old avatar file from storage when Profile avatar is changed
# @receiver(pre_save, sender=Profile)
# def delete_old_avatar_on_change(sender, instance, **kwargs):
#     if not instance.pk:
#         return  # 新增，不處理

#     old_avatar = sender.objects.get(pk=instance.pk).avatar
#     new_avatar = instance.avatar

#     if old_avatar and old_avatar != new_avatar:
#         if old_avatar.storage.exists(old_avatar.name):
#             old_avatar.storage.delete(old_avatar.name)
