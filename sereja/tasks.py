from time import sleep
import json
from sereja.celery import app
from celery.result import AsyncResult
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
from django.template import Engine, Context

#from cat.models import *
from load_form_providers.load_element import *
from cat.views_to_admin_try import get_soup_art
from pars.fury import *
from pars.itblok import *
from pars.versum import *
from pars.ua import *
from pars.art import *
from rivals.views import *

def render_template(template, context):
    engine = Engine.get_default()
    tmpl = engine.get_template(template)
    return tmpl.render(Context(context))

@app.task
def task_rivals_to_models(rivals_):
    rivals_to_models(rivals_)

@app.task
def after():
    sleep(15)
    with open("load_form_providers/loads/log.json", "r") as write_file:
        dict1=json.load(write_file)
    return dict1

@app.task
def hello_world():
  sleep(10)
  return 'Hello World'

@app.task(bind=True)
def test(self):
  return self.AsyncResult(self.request.id).state

@app.task
def task_providers():
    Parsing_from_providers()

@app.task
def task_tech_price():
    to_model_price_from_dc()
    to_tech_price_from_dc()

@app.task
def task_art_to_admin(url, queryset):
    get_soup_art(url, queryset)

@app.task
def task_fury():
    load_fury()

@app.task
def task_itblok():
    load_itblok()

@app.task
def task_versum():
    load_versum()

@app.task
def task_ua():
    load_ua()

@app.task
def task_art():
    load_art()

@app.task
def task_trigger(*arg, **kw):
    t_now = timezone.now()+timezone.timedelta(minutes=30)
    while True:
        sleep(60)
        try:
            res = AsyncResult(task_id)
            if res.status == 'SUCCESS':
                try:
                    messages.success(request, f'{mask} update complite')
                except Exception as ex:
                    return f'{mask} update complite, but {ex}'
                break
            elif t_now < timezone.now():
                try:
                    messages.success(request, f'{mask} no update after 30 min')
                except Exception as ex:
                    return f'{mask} no update after 30 min, error: {ex}'
                break
        except Exception as ex:
            return ex

"""@app.task(bind=True, default_retry_delay=10 * 60)
def send_mail_task(self, subject, message, from_email, recipients):
    mes = Mail(
    from_email=from_email,
    to_emails=recipients,
    subject=subject,
    html_content=message)
    #message = 'Hello from Django'
    #html_message = render_template(f'{template}.html', context)
    try:
        sg = SendGridAPIClient(EMAIL_HOST_PASSWORD)
        response = sg.send(mes)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as ex:
        self.retry(exc=ex)"""
