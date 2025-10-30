from django.apps import AppConfig
import logging

logger = logging.getLogger(__name__)


class PaddleSyncConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "paddle_sync"

    def ready(self):
        import paddle_sync.signals
        from django_paddle_billing.models import PaddleBaseModel

        def patched_validate_occurred_at(self, occurred_at):
            if (
                occurred_at is not None
                and self.occurred_at is not None
                and occurred_at <= self.occurred_at
            ):
                logger.warning("ignoring duplicate webhook event")
                return False
            logger.info("processing webhook event")
            return True

        PaddleBaseModel.validate_occurred_at = patched_validate_occurred_at
