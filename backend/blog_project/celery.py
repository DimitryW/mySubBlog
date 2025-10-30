import os
from celery import Celery
from decouple import config

os.environ.setdefault("GOOGLE_EMAIL_USER", config("GOOGLE_EMAIL_USER"))
os.environ.setdefault("GOOGLE_EMAIL_PASSWORD", config("GOOGLE_EMAIL_PASSWORD"))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blog_project.settings")
app = Celery("blog_project")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
