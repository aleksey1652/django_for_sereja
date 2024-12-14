from django.forms import ModelForm
from .models import *
from django.core.exceptions import ValidationError
from django import forms
#providerprice_parts price Pc_assemblyForm ComputersForm

class Parts_short_se_Form(ModelForm):
    class Meta:
        model = Parts_short
        #fields = ['name_parts', 'x_code', 'min_price', 'auto','kind',]
        exclude = ('parts_full', 'computer_shorts')

    def clean(self):
        from descriptions.models import Cooler,CPU,MB,RAM,HDD,PSU,GPU,FAN,CASE,SSD,WiFi,Cables,Soft
        from pars.ecatalog import dict_name_all
        cleaned_data = super(Parts_short_se_Form, self).clean()
        #name_parts_ = cleaned_data.get('name_parts')
        art = cleaned_data.get('partnumber_list')
        active_ = cleaned_data.get('kind2')
        kind_ = cleaned_data.get('kind')
        active_reverse = False if active_ == True else True
        desc_ = eval(dict_name_all[kind_])
        desc = desc_.filter(part_number=art, is_active=active_reverse)
        if desc.exists():
            raise ValidationError(f'Недопустимо, причина дубликат в описнии- {art}')
        return cleaned_data

class PartsForm(ModelForm):
    class Meta:
        model = Parts_short
        fields = ['Advanced_parts']
        labels = { 'Advanced_parts': 'Number'}
    def clean_Advanced_parts(self):
        data = self.cleaned_data['Advanced_parts']
        try:
            if int(data) < 0 or int(data) > 20:
                raise ValidationError('Invalid date')
        except:
            raise ValidationError('Only 1,2,3,..')
        return data
    def clean_x_code(self):
        data = self.cleaned_data['x_code']
        try:
            if float(data) < 0 or float(data) > 10000:
                raise ValidationError('Invalid date')
        except:
            raise ValidationError('Only digit')
        return data

class PartsForm_code(PartsForm):
    #code = forms.CharField()
    procent = forms.CharField()

    class Meta:
        model = Parts_short
        fields = ['Advanced_parts', 'procent']
        labels = { 'Advanced_parts': 'Number', 'procent':'%'}

class ComputersForm(ModelForm):
    class Meta:
        model = Computers
        fields = ['class_computers', 'warranty_computers']
        labels = { 'class_computers': 'наценка', 'warranty_computers': 'USD'}
    def clean_Advanced_parts(self):
        data = self.cleaned_data['class_computers']
        try:
            if float(data) < 1 or float(data) > 2:
                raise ValidationError('Invalid date')
        except:
            raise ValidationError('Only 1..2')
        return data
    def clean_x_code(self):
        data = self.cleaned_data['warranty_computers']
        try:
            if float(data) < 0:
                raise ValidationError('Only >= 0')
        except:
            raise ValidationError('Invalid date')
        return data

class ComputersForm_code(ComputersForm):
    code = forms.CharField()

    class Meta:
        model = Computers
        fields = ['class_computers', 'warranty_computers']
        labels = {'class_computers': 'margin', 'warranty_computers': 'dollar rate',
        'code': 'code'}

class ComputersSpecialPrice(ComputersForm):
    exch = forms.FloatField()

    class Meta:
        model = Computers
        fields = ['class_computers', 'warranty_computers']
        labels = {'class_computers': 'Наценка', 'warranty_computers': 'Спец цена',
        'exch': 'Курс'}

class ComputersForm_advanced(ComputersForm):

    class Meta:
        model = Computers
        fields = ['you_vid', 'perm_conf', 'elite_conf']
        labels = { 'you_vid': 'you_vid', 'perm_conf': 'perm_conf', 'elite_conf': 'elite_conf'}

class CompSearchForm(ModelForm):
    class Meta:
        model = Computers
        fields = ['name_computers']
        labels = { 'name_computers': 'Название компа'}

class Pc_assemblyForm(ModelForm):
    class Meta:
        model = Pc_assembly
        fields = ['name_assembly']
        labels = { 'name_assembly': 'name_assembly'}

class Pc_assemblyForm_advanced(ModelForm):
    class Meta:
        model = Pc_assembly
        fields = ['desc_ru', 'desc_ukr']
        labels = { 'desc_ru': 'desc_ru', 'desc_ukr': 'desc_ukr'}

class ShortSearchForm(ModelForm):
    id = None
    class Meta:
        model = Parts_short
        fields = ['name_parts']
        labels = { 'name_parts': 'Enter'}

class ShortCreateForm(ModelForm):
    update = forms.CharField()
    class Meta:
        model = Parts_short
        fields = ['name_parts','kind','kind2']
        labels = {'kind2':'for itblok','name_parts': 'name_parts','kind':'kind'}

class ShortdeForm(ModelForm):
    class Meta:
        model = Parts_short
        fields = ['name_parts']
        labels = {'name_parts': 'computer_parts'}

class FulldeForm(ModelForm):
    class Meta:
        model = Parts_full
        fields = ['partnumber_parts']
        labels = {'partnumber_parts': 'price_parts'}

class ArticleSearchForm(ModelForm):
    id = None
    class Meta:
        model = Parts_short
        fields = ['name_parts']
        labels = { 'name_parts': 'Parts_article'}

class ArticleCreateForm(ModelForm):
    class Meta:
        model = Articles
        fields = ['article','item_name','item_price']
        labels = {'article': 'partnumber',
                  'item_name': 'name parts',
                  'item_price': 'kind item'
                  }

class PasswordForm(ModelForm):
    class Meta:
        model = Parts_short
        fields = ['name_parts']
        labels = { 'name_parts': 'Enter password'}

class PfullForm(ModelForm):
    id = None
    class Meta:
        model = Parts_full
        fields = ['providerprice_parts']
        labels = { 'providerprice_parts': 'New price'}

class PfullForm_kind(ModelForm):
    id = None
    class Meta:
        model = Parts_full
        fields = ['kind']
        labels = { 'kind': 'New kind'}

class MailForm(forms.Form):
    #who = forms.CharField()
    mail_from = forms.EmailField()
    send_or_not = forms.BooleanField()


class PromotionForm(ModelForm):
    class Meta:
        model = Promotion
        fields = ['prom']
        labels = {'prom': 'promotion'}
