from celery import shared_task
from .services import sync_products


@shared_task
def sync_products_task():
    sync_products()
