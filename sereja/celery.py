import os
import django
from celery import Celery
#from django.conf import settings
from celery.schedules import crontab
os.environ.setdefault('DJANGO_SETTINGS_MODULE','sereja.settings')
#django.setup()
app = Celery('sereja')
app.config_from_object('django.conf:settings',namespace='CELERY')
#app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.autodiscover_tasks()
app.conf.beat_schedule = {
    'pars-every-tday': {
        'task': 'sereja.tasks.task_providers',
        'schedule': crontab(minute=0, hour=0)
    },
}
