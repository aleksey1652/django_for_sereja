import os,json,pickle,django
os.environ.setdefault('DJANGO_SETTINGS_MODULE','sereja.settings')
django.setup()
from cat.models import *
import pandas as pd
from load_form_providers.load_element import get_xls

get_xls()
