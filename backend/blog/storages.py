# blog/storages.py
from storages.backends.gcloud import GoogleCloudStorage
from django.conf import settings
from google.oauth2 import service_account
from decouple import config

GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
    config("GOOGLE_APPLICATION_CREDENTIALS")
)
bucket_name = config("GS_BUCKET_NAME")


class MyGoogleCloudStorage(GoogleCloudStorage):
    def __init__(self, *args, **kwargs):
        # 從 STORAGES['default']['OPTIONS'] 讀取設定
        default_options = (
            getattr(settings, "STORAGES", {}).get("default", {}).get("OPTIONS", {})
        )
        default_options.setdefault("bucket_name", bucket_name)
        default_options.setdefault("credentials", GS_CREDENTIALS)

        super().__init__(*args, **default_options)
