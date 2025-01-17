from money.models import *
from django.utils import timezone
from django.db.models import Sum, Count, F
import re

class StatsRules:
    # Статистика

    month, year = None, None

    def __init__(self, month, year):
        self.month, self.year = month, year
