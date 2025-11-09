from django.db import models
from django.contrib.auth.models import User


def user_avatar_path(instance, filename):
    # 上傳的檔案會放在 media/avatars/user_<id>/<filename>
    return f"avatars/user_{instance.user.id}/{filename}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    avatar = models.ImageField(upload_to=user_avatar_path, blank=True, null=True)

    def __str__(self):
        return self.user.username
