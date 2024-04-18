from django.forms import ModelForm, Textarea, CharField, ChoiceField
from .models import *
from cat.models import Parts_short
from django.core.exceptions import ValidationError
from django import forms
#providerprice_parts Офис Form_glav_buh

class BidsSearchForm(ModelForm):
    class Meta:
        model = Bids
        fields = ['nds']
        labels = { 'nds': 'Bids ID'}

class GoodsSearchForm(ModelForm):
    class Meta:
        model = Goods
        fields = ['discr']
        labels = { 'discr': 'discr'}
        widgets = {
            'discr': Textarea(attrs={'cols': 20, 'rows': 1}),
        }

class SiteSearchForm(ModelForm):
    class Meta:
        model = Bids
        fields = ['site']
        labels = { 'site': 'Site choice'}


class Statistics_serviceForm(ModelForm):
    CHOISE = (
        ('простой', 'простой'),
        ('обычный', 'обычный'),
        ('сложный', 'сложный'),
        ('ультра', 'ультра'),
    )

    CHOISE2 = (
        ('Ремонт ПК', 'Ремонт ПК'),
        ('Обслуживание', 'Обслуживание'),
    )

    service_sloznostPK = forms.ChoiceField(
        choices=CHOISE,
        label='Сложность работы'
    )

    service_kind = forms.ChoiceField(
            choices=CHOISE2,
            label='Виды работ  с ПК'
        )

    class Meta:
        model = Statistics_service
        fields = ['service_sloznostPK', 'service_kind', 'obsluj_count']
        labels = {'service_sloznostPK': 'Сложность работы', 'service_kind': 'Вид работ', 'obsluj_count': 'Колличество'
                }

class Statistics_serviceForm_sborsik(ModelForm):
    CHOISE = (
        ('простой', 'простой'),
        ('обычный', 'обычный'),
        ('сложный', 'сложный'),
        ('ультра', 'ультра'),
        ('лед таблички', 'лед таблички'),
    )
    service_sloznostPK = forms.ChoiceField(
        choices=CHOISE,
        label='Сложность сборки'
    )

    class Meta:
        model = Statistics_service
        fields = ['service_sloznostPK', 'sborka_count']
        labels = { 'service_sloznostPK': 'Сложность сборки', 'sborka_count': 'Колличество'}



class Form_glav_buh(forms.Form):

    CHOISE = (
        ('versum', 'Верум'),
        ('itblok', 'Айтиблок'),
        ('both', 'Тендер'),
        ('both', 'Другие'),
    )

    bids_type = forms.ChoiceField(
        widget=forms.Select(),
        choices=CHOISE,
        label='',
        help_text="Выберите тип заявки"
        )
    bids_id = forms.IntegerField(label='Номер заявки')
    dohod = forms.FloatField(label='Доход')
    zatrati = forms.FloatField(label='Затраты')
    #pribil = forms.FloatField(label='Прибыль')
    #nalog_na_pribil = forms.FloatField(label='Налог на прибыль')
    #nds = forms.FloatField(label='НДС')
    #chistaja_pribil = forms.FloatField(label='Чистая прибыль')

    def clean(self):
        cleaned_data = super(Form_glav_buh, self).clean()
        data = cleaned_data.get('bids_id')
        if Expense.objects.filter(expense_groups__name='НДС').filter(discr__iregex=f'id: {data}').exists():
            raise ValidationError(f'Налог по этой заявке: {data} уже посчитан')
        return cleaned_data

class KurierForm(forms.Form):
    bids = forms.IntegerField(label='Введите номер заявки',)
    summa = forms.IntegerField(label='Сумма',)
    #km = forms.IntegerField(label='Введите км за тукущий месяц',)

class One_C_Form(forms.Form):

    CHOISE = (
        ('простой', 'простой'),
        ('обычный', 'обычный'),
        ('сложный', 'сложный'),
    )

    service_sloznostPK = forms.ChoiceField(
        choices=CHOISE,
        label='Сложность заявки'
    )
    sborka_count = forms.IntegerField(label='Колличество')

    class Meta:
        #model = Statistics_service
        fields = ['service_sloznostPK', 'sborka_count']
        labels = { 'service_sloznostPK': 'Сложность заявки', 'sborka_count': 'Колличество'}

class PlanForm(ModelForm):
    class Meta:
        model = Plan
        fields = ['plan', 'zero_plan']
        labels = {'plan': 'План', 'zero_plan': 'Выход в 0'}

class GrossprofitForm(ModelForm):
    class Meta:
        model = Gross_profit
        fields = ['rentability', 'amount', 'quantity']
        labels = {'rentability': 'Наценка', 'amount': 'Оборот_ПК', 'quantity': 'Колличество_ПК'}
