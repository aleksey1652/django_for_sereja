from django.forms import ModelForm
from .models import *
from django.core.exceptions import ValidationError
from django import forms

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
        labels = { 'class_computers': 'margin', 'warranty_computers': 'dollar rate'}
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
            if float(data) < 20 or float(data) > 100:
                raise ValidationError('Invalid date')
        except:
            raise ValidationError('Only 20+')
        return data

class ComputersForm_code(ComputersForm):
    code = forms.CharField()

    class Meta:
        model = Computers
        fields = ['class_computers', 'warranty_computers']
        labels = { 'class_computers': 'margin', 'warranty_computers': 'dollar rate', 'code': 'code'}

class ComputersForm_advanced(ComputersForm):

    class Meta:
        model = Computers
        fields = ['you_vid', 'perm_conf', 'elite_conf']
        labels = { 'you_vid': 'you_vid', 'perm_conf': 'perm_conf', 'elite_conf': 'elite_conf'}

class CompSearchForm(ModelForm):
    class Meta:
        model = Computers
        fields = ['name_computers']
        labels = { 'name_computers': 'Computer name'}

class Pc_assemblyForm(ModelForm):
    class Meta:
        model = Pc_assembly
        fields = ['name_assembly']
        labels = { 'name_assembly': 'name_assembly'}

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

class MailForm(forms.Form):
    #who = forms.CharField()
    mail_from = forms.EmailField()
    send_or_not = forms.BooleanField()

class CoolForm(ModelForm):
    class Meta:
        model = Cooler
        fields = ['name','part_number','vendor','price',
        'desc_ukr','desc_ru','fan_type_ua','fan_type_rus','fan_spd_ua',
        'fan_spd_rus','fan_noise_level','fan_size','more','depend_to','depend_to_type']
        labels = {'name':'name','part_number':'part_number','vendor':'vendor','price':'price',
        'desc_ukr':'desc_ukr','desc_ru':'desc_ru','fan_type_ua':'fan_type_ua',
        'fan_type_rus':'fan_type_rus','fan_spd_ua':'fan_spd_ua',
        'fan_spd_rus':'fan_spd_rus','fan_noise_level':'fan_noise_level','fan_size':'fan_size','more':'more',
        'depend_to':'depend_to','depend_to_type':'depend_to_type'}

class CpuForm(ModelForm):
    class Meta:
        model = CPU
        fields = ['name', 'part_number', 'vendor', 'price', 'desc_ukr', 'desc_ru',
        'f_name', 'cpu_c_t', 'f_cpu_c_t', 'cpu_b_f', 'cpu_cache', 'cpu_i_g_ua',
        'cpu_i_g_rus', 'more', 'depend_from', 'depend_from_type']
        labels = {'name':'name','part_number':'part_number','vendor':'vendor','price':'price',
        'desc_ukr':'desc_ukr','desc_ru':'desc_ru','f_name':'f_name',
        'cpu_c_t':'cpu_c_t', 'f_cpu_c_t':'f_cpu_c_t', 'cpu_b_f':'cpu_b_f',
        'cpu_cache':'cpu_cache', 'cpu_i_g_ua':'cpu_i_g_ua',
        'cpu_i_g_rus':'cpu_i_g_rus', 'more':'more',
        'depend_from':'depend_from', 'depend_from_type':'depend_from_type'}

class MbForm(ModelForm):
    class Meta:
        model = MB
        fields = ['name', 'part_number', 'vendor', 'main_category', 'price',
        'desc_ukr', 'desc_ru', 'mb_chipset', 'mb_max_ram', 'more', 'depend_to', 'depend_to_type',
        'depend_from','depend_from_type']
        labels = {'name': 'name', 'part_number': 'part_number', 'vendor': 'vendor',
        'main_category': 'main_category', 'price': 'price', 'desc_ukr': 'desc_ukr',
        'desc_ru': 'desc_ru', 'mb_chipset': 'mb_chipset', 'mb_max_ram': 'mb_max_ram',
        'more': 'more', 'depend_to': 'depend_to', 'depend_to_type': 'depend_to_type',
        'depend_from':'depend_from','depend_from_type':'depend_from_type'}

class RamForm(ModelForm):
    class Meta:
        model = RAM
        fields = ['name', 'part_number', 'vendor', 'f_name', 'price', 'desc_ukr',
         'desc_ru', 'mem_s', 'mem_spd', 'mem_l', 'more']
        labels = {'name': 'name', 'part_number': 'part_number', 'vendor': 'vendor',
        'f_name': 'f_name', 'price': 'price', 'desc_ukr': 'desc_ukr',
        'desc_ru': 'desc_ru', 'mem_s': 'mem_s', 'mem_spd': 'mem_spd',
        'mem_l': 'mem_l', 'more': 'more'}

class HddForm(ModelForm):
    class Meta:
        model = HDD
        fields = ['name', 'part_number', 'vendor', 'f_name', 'price', 'desc_ukr',
        'desc_ru', 'hdd_s', 'hdd_spd_ua', 'hdd_spd_rus', 'hdd_ca', 'more']
        labels = {'name': 'name', 'part_number': 'part_number', 'vendor': 'vendor',
        'f_name': 'f_name', 'price': 'price', 'desc_ukr': 'desc_ukr',
        'desc_ru': 'desc_ru', 'hdd_s': 'hdd_s', 'hdd_spd_ua': 'hdd_spd_ua',
        'hdd_spd_rus': 'hdd_spd_rus', 'hdd_ca': 'hdd_ca', 'more': 'more'}

class PsuForm(ModelForm):
    class Meta:
        model = PSU
        fields = ['name', 'part_number', 'vendor', 'price', 'desc_ukr', 'desc_ru',
        'psu_p', 'psu_c', 'psu_f', 'more']
        labels = {'name': 'name', 'part_number': 'part_number', 'vendor': 'vendor',
        'price': 'price', 'desc_ukr': 'desc_ukr', 'desc_ru': 'desc_ru',
        'psu_p': 'psu_p', 'psu_c': 'psu_c', 'psu_f': 'psu_f', 'more': 'more'}

class GpuForm(ModelForm):
    class Meta:
        model = GPU
        fields = ['name', 'part_number', 'vendor', 'main_category', 'f_name',
        'price', 'desc_ukr', 'desc_ru', 'gpu_fps', 'gpu_m_s', 'gpu_b',
        'gpu_cpu_spd', 'gpu_mem_spd', 'more']
        labels = {'name': 'name', 'part_number': 'part_number', 'vendor': 'vendor',
        'main_category': 'main_category', 'f_name': 'f_name', 'price': 'price',
        'desc_ukr': 'desc_ukr', 'desc_ru': 'desc_ru', 'gpu_fps': 'gpu_fps',
        'gpu_m_s': 'gpu_m_s', 'gpu_b': 'gpu_b', 'gpu_cpu_spd': 'gpu_cpu_spd',
        'gpu_mem_spd': 'gpu_mem_spd', 'more': 'more'}

class FanForm(ModelForm):
    class Meta:
        model = FAN
        fields = ['name', 'part_number', 'vendor', 'price', 'desc_ukr', 'desc_ru',
        'case_fan_spd_ua', 'case_fan_spd_rus', 'case_fan_noise_level', 'case_fan_size', 'more']
        labels = {'name': 'name', 'part_number': 'part_number', 'vendor': 'vendor',
        'price': 'price', 'desc_ukr': 'desc_ukr', 'desc_ru': 'desc_ru',
        'case_fan_spd_ua': 'case_fan_spd_ua', 'case_fan_spd_rus': 'case_fan_spd_rus',
        'case_fan_noise_level': 'case_fan_noise_level', 'case_fan_size': 'case_fan_size', 'more': 'more'}

class CaseForm(ModelForm):
    class Meta:
        model = CASE
        fields = ['name', 'part_number', 'vendor', 'price', 'desc_ukr', 'desc_ru', 'case_s', 'more']
        labels = {'name': 'name', 'part_number': 'part_number', 'vendor': 'vendor',
        'price': 'price', 'desc_ukr': 'desc_ukr', 'desc_ru': 'desc_ru',
        'case_s': 'case_s', 'more': 'more'}

class SsdForm(ModelForm):
    class Meta:
        model = SSD
        fields = ['name', 'part_number', 'vendor', 'f_name', 'price', 'desc_ukr', 'desc_ru',
        'ssd_s', 'ssd_spd', 'ssd_r_spd', 'ssd_type_cells', 'more']
        labels = {'name': 'name', 'part_number': 'part_number', 'vendor': 'vendor',
        'f_name': 'f_name', 'price': 'price', 'desc_ukr': 'desc_ukr', 'desc_ru': 'desc_ru',
        'ssd_s': 'ssd_s', 'ssd_spd': 'ssd_spd', 'ssd_r_spd': 'ssd_r_spd',
        'ssd_type_cells': 'ssd_type_cells', 'more': 'more'}

class WiFiForm(ModelForm):
    class Meta:
        model = WiFi
        fields = ['name', 'part_number', 'vendor', 'r_price', 'price', 'desc_ukr', 'desc_ru',
        'net_type_ukr', 'net_type_rus', 'net_max_spd', 'net_stand', 'net_int', 'more']
        labels = {'name': 'name', 'part_number': 'part_number', 'vendor': 'vendor',
        'r_price': 'r_price', 'price': 'price', 'desc_ukr': 'desc_ukr', 'desc_ru': 'desc_ru',
        'net_type_ukr': 'net_type_ukr', 'net_type_rus': 'net_type_rus', 'net_max_spd': 'net_max_spd',
        'net_stand': 'net_stand', 'net_int': 'net_int', 'more': 'more'}

class CablesForm(ModelForm):
    class Meta:
        model = Cables
        fields = ['name', 'part_number', 'vendor', 'r_price', 'desc_ukr', 'desc_ru',
        'cab_mat_ukr', 'cab_mat_ru', 'cab_col_ukr', 'cab_col_ru', 'cab_set', 'more']
        labels = {'name': 'name', 'part_number': 'part_number', 'vendor': 'vendor',
        'r_price': 'r_price', 'desc_ukr': 'desc_ukr', 'desc_ru': 'desc_ru',
        'cab_mat_ukr': 'cab_mat_ukr', 'cab_mat_ru': 'cab_mat_ru', 'cab_col_ukr': 'cab_col_ukr',
        'cab_col_ru': 'cab_col_ru', 'cab_set': 'cab_set', 'more': 'more'}

class SoftForm(ModelForm):
    class Meta:
        model = Soft
        fields = ['name', 'part_number', 'vendor', 'r_price', 'price', 'desc_ukr', 'desc_ru',
        'soft_type_ukr', 'soft_type_ru', 'soft_lang_ukr', 'soft_lang_ru', 'soft_set', 'more']
        labels = {'name': 'name', 'part_number': 'part_number', 'vendor': 'vendor',
        'r_price': 'r_price', 'price': 'price', 'desc_ukr': 'desc_ukr', 'desc_ru': 'desc_ru',
        'soft_type_ukr': 'soft_type_ukr', 'soft_type_ru': 'soft_type_ru', 'soft_lang_ukr': 'soft_lang_ukr', 'soft_lang_ru': 'soft_lang_ru',
        'soft_set': 'soft_set', 'more': 'more'}
