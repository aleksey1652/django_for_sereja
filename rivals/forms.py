from django.forms import ModelForm, Textarea, CharField, ChoiceField
from django.core.exceptions import ValidationError
from django import forms

from .models import *

class AssemblageForm(ModelForm):
    class Meta:
        model = Assemblage
        fields = ['is_active']
        labels = { 'is_active': 'Вкл/выкл'}
