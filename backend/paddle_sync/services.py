# paddle_sync/services.py
import logging
from django_paddle_billing.models import Product, Price

logger = logging.getLogger(__name__)


def sync_products():
    created_p, updated_p = Product.sync_from_paddle()
    logger.info("Products: created %d, updated %d", created_p, updated_p)

    created_pr, updated_pr = Price.sync_from_paddle()
    logger.info("Prices: created %d, updated %d", created_pr, updated_pr)
