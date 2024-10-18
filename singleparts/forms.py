from django import forms

class RentabilityForm(forms.Form):
    rentability = forms.CharField(label='наценка')

class AutoForm(forms.Form):
    # изменение ручной цены
    auto = forms.BooleanField(required=False, label='ручная')

class IsActiveForm(forms.Form):
    # изменение is_active

    CHOICES = (
        ('вкл', 'вкл'),
        ('выкл', 'выкл'),
    )

    is_active = forms.ChoiceField(
                                choices=CHOICES,
                                widget=forms.RadioSelect,
                                label=''
    )

class SinglePackFewForm(forms.Form):
    CHOICES = (
        ('hotline', 'hotline'),
        ('delivery', 'delivery'),
        ('label', 'label'),
        ('creditoff', 'creditoff'),
    )
    hotline = forms.BooleanField(required=False, label='hotline')
    delivery = forms.BooleanField(required=False, label='доставка')
    label_ = forms.CharField(required=False, label='label')
    creditoff = forms.BooleanField(required=False, label='creditoff')
    only_thing = forms.ChoiceField(
                                choices=CHOICES,
                                widget=forms.RadioSelect,
                                label='Только для:'
    )
