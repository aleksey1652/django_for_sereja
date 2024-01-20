import os
import django
from celery import Celery
#from django.conf import settings
from celery.schedules import crontab
os.environ.setdefault('DJANGO_SETTINGS_MODULE','sereja.settings')
#django.setup()
app = Celery('sereja')
#app = Celery('sereja',broker='redis://localhost:6379/0', backend='redis://localhost:6379/1')
app.config_from_object('django.conf:settings',namespace='CELERY')
#app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.autodiscover_tasks()
app.conf.beat_schedule = {
    'pars-every-tday': {
        'task': 'sereja.tasks.task_providers',
        'schedule': crontab(minute=0, hour=0)
    },
    'pars-tech': {
        'task': 'sereja.tasks.task_tech_price',
        'schedule': crontab(minute=30, hour=0)
    },
}
