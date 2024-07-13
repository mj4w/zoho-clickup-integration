import requests
from celery import shared_task
from .models import *

@shared_task(bind=True)
def sync_tasks():
    pass