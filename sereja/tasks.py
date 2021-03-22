from time import sleep
import json
from sereja.celery import app
from load_form_providers.load_element import *
from pars.fury import *
from pars.itblok import *
from pars.versum import *
from pars.ua import *
from pars.art import *

@app.task
def after():
    sleep(15)
    with open("load_form_providers/loads/log.json", "r") as write_file:
        dict1=json.load(write_file)
    return dict1

@app.task
def hello_world():
  sleep(10)
  print('Hello World')

@app.task
def task_providers():
    Parsing_from_providers()

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
