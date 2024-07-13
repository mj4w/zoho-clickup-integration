from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_celery_project.settings')

app = Celery('integration')
app.conf.enable_utc = False
app.conf.update(timezone = 'Asia/Manila')
app.config_from_object(settings, namespace='CELERY')


# Celery Beat Settings
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f"Request: {0!r}".format(self.request))
