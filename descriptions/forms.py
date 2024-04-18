from django.forms import ModelForm
from .models import *
from django.core.exceptions import ValidationError
from django import forms
#providerprice_parts
class Cooler_otherForm(ModelForm):
    name = forms.CharField()
    part_number = forms.CharField()
    vendor = forms.CharField()
    price = forms.CharField()
    desc_ukr = forms.CharField(widget=forms.Textarea)
    desc_ru = forms.CharField(widget=forms.Textarea)
    cool_type_ua = forms.CharField()
    cool_type_ru = forms.CharField()
    #fan_spd_ua = forms.CharField()
    #fan_spd_rus = forms.CharField()
    cool_max_no = forms.CharField()
    cool_fan_size = forms.CharField()
    #depend_to = forms.CharField()
    #depend_to_type = forms.CharField()

    class Meta:
        model = Cooler_OTHER
        fields = [
        'name', 'part_number', 'vendor', 'r_price',
        'price','desc_ukr', 'desc_ru', 'cool_warr_ua', 'cool_warr_ru',
        'you_vid', 'label', 'creditoff']


class CoolForm(ModelForm):
    class Meta:
        model = Cooler
        fields = ['name','part_number','vendor','price',
        'desc_ukr','desc_ru','fan_type_ua','fan_type_rus','fan_spd_ua',
        'fan_spd_rus','fan_noise_level','fan_size','more','depend_to','depend_to_type', 'cooler_height']
        labels = {'name':'name','part_number':'part_number','vendor':'vendor','price':'price',
        'desc_ukr':'desc_ukr','desc_ru':'desc_ru','fan_type_ua':'fan_type_ua',
        'fan_type_rus':'fan_type_rus','fan_spd_ua':'fan_spd_ua',
        'fan_spd_rus':'fan_spd_rus','fan_noise_level':'fan_noise_level','fan_size':'fan_size','more':'more',
        'depend_to':'depend_to','depend_to_type':'depend_to_type', 'cooler_height': 'cooler_height'}

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

class CPU_otherForm(ModelForm):
    name = forms.CharField()
    part_number = forms.CharField()
    vendor = forms.CharField()
    price = forms.CharField()
    desc_ukr = forms.CharField(widget=forms.Textarea)
    desc_ru = forms.CharField(widget=forms.Textarea)
    #cpu_c_t = forms.CharField()
    #f_cpu_c_t = forms.CharField()
    cpu_bfq = forms.CharField()
    cpu_cache = forms.CharField()
    #cpu_i_g_ua = forms.CharField()
    #cpu_i_g_rus = forms.CharField()
    #depend_from = forms.CharField()
    #depend_from_type = forms.CharField()

    class Meta:
        model = CPU_OTHER
        fields = [
        'name', 'part_number', 'vendor', 'r_price', 'price', 'desc_ukr', 'desc_ru',
        'you_vid', 'label', 'cpu_cache', 'creditoff'
        ]


class MB_otherForm(ModelForm):
    name = forms.CharField()
    part_number = forms.CharField()
    vendor = forms.CharField()
    price = forms.CharField()
    desc_ukr = forms.CharField(widget=forms.Textarea)
    desc_ru = forms.CharField(widget=forms.Textarea)
    part_mb_fam = forms.CharField()
    part_mb_ff = forms.CharField()
    part_mb_chip = forms.CharField()
    part_mb_ram_max_size = forms.CharField()

    class Meta:
        model = MB_OTHER
        fields = ['name', 'part_number', 'vendor', 'r_price', 'price', 'desc_ukr', 'desc_ru',
                'you_vid', 'label', 'creditoff']

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

class Ram_otherForm(ModelForm):
    name = forms.CharField()
    part_number = forms.CharField()
    vendor = forms.CharField()
    ram_size = forms.CharField()
    price = forms.CharField()
    desc_ukr = forms.CharField(widget=forms.Textarea)
    desc_ru = forms.CharField(widget=forms.Textarea)
    #mem_s = forms.CharField()
    ram_fq = forms.CharField()
    #mem_l = forms.CharField()

    class Meta:
        model = RAM_OTHER
        fields = ['name', 'part_number', 'vendor', 'r_price', 'price', 'desc_ukr', 'desc_ru',
                'you_vid', 'label', 'creditoff']

class HddForm(ModelForm):
    class Meta:
        model = HDD
        fields = ['name', 'part_number', 'vendor', 'f_name', 'price', 'desc_ukr',
        'desc_ru', 'hdd_s', 'hdd_spd_ua', 'hdd_spd_rus', 'hdd_ca', 'more']
        labels = {'name': 'name', 'part_number': 'part_number', 'vendor': 'vendor',
        'f_name': 'f_name', 'price': 'price', 'desc_ukr': 'desc_ukr',
        'desc_ru': 'desc_ru', 'hdd_s': 'hdd_s', 'hdd_spd_ua': 'hdd_spd_ua',
        'hdd_spd_rus': 'hdd_spd_rus', 'hdd_ca': 'hdd_ca', 'more': 'more'}

class HDD_otherForm(ModelForm):
    name = forms.CharField()
    part_number = forms.CharField()
    vendor = forms.CharField()
    hdd_size = forms.CharField()
    price = forms.CharField()
    desc_ukr = forms.CharField(widget=forms.Textarea)
    desc_ru = forms.CharField(widget=forms.Textarea)
    hdd_spd_ph_ua = forms.CharField()
    hdd_spd_ph_ru = forms.CharField()
    hdd_buf = forms.CharField()


    class Meta:
        model = HDD_OTHER
        fields = ['name', 'part_number', 'vendor', 'r_price', 'price', 'desc_ukr', 'desc_ru',
                'you_vid', 'label', 'creditoff']

class PSU_otherForm(ModelForm):
    name = forms.CharField()
    part_number = forms.CharField()
    vendor = forms.CharField()
    psu_pow = forms.CharField()
    price = forms.CharField()
    desc_ukr = forms.CharField(widget=forms.Textarea)
    desc_ru = forms.CharField(widget=forms.Textarea)
    psu_80 = forms.CharField()
    psu_fan = forms.CharField()


    class Meta:
        model = PSU_OTHER
        fields = ['name', 'part_number', 'vendor', 'r_price', 'price', 'desc_ukr', 'desc_ru',
                'you_vid', 'label', 'creditoff']

class PsuForm(ModelForm):
    class Meta:
        model = PSU
        fields = ['name', 'part_number', 'vendor', 'price', 'desc_ukr', 'desc_ru',
        'psu_p', 'psu_c', 'psu_f', 'more']
        labels = {'name': 'name', 'part_number': 'part_number', 'vendor': 'vendor',
        'price': 'price', 'desc_ukr': 'desc_ukr', 'desc_ru': 'desc_ru',
        'psu_p': 'psu_p', 'psu_c': 'psu_c', 'psu_f': 'psu_f', 'more': 'more'}

class GPU_otherForm(ModelForm):
    name = forms.CharField()
    part_number = forms.CharField()
    vendor = forms.CharField()
    gpu_mem_size = forms.CharField()
    price = forms.CharField()
    desc_ukr = forms.CharField(widget=forms.Textarea)
    desc_ru = forms.CharField(widget=forms.Textarea)
    gpu_bit = forms.CharField()
    part_gpu_gpu_spd = forms.CharField()
    part_gpu_mem_spd = forms.CharField()


    class Meta:
        model = GPU_OTHER
        fields = ['name', 'part_number', 'vendor', 'r_price', 'price', 'desc_ukr', 'desc_ru',
                'you_vid', 'label', 'creditoff']

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

class FAN_otherForm(ModelForm):
    name = forms.CharField()
    part_number = forms.CharField()
    vendor = forms.CharField()
    part_fan_size = forms.CharField()
    price = forms.CharField()
    desc_ukr = forms.CharField(widget=forms.Textarea)
    desc_ru = forms.CharField(widget=forms.Textarea)
    fan_max_no = forms.CharField()


    class Meta:
        model = FAN_OTHER
        fields = ['name', 'part_number', 'vendor', 'r_price', 'price', 'desc_ukr', 'desc_ru',
                'you_vid', 'label', 'creditoff']

class FanForm(ModelForm):
    class Meta:
        model = FAN
        fields = ['name', 'part_number', 'vendor', 'price', 'desc_ukr', 'desc_ru',
        'case_fan_spd_ua', 'case_fan_spd_rus', 'case_fan_noise_level', 'case_fan_size', 'more']
        labels = {'name': 'name', 'part_number': 'part_number', 'vendor': 'vendor',
        'price': 'price', 'desc_ukr': 'desc_ukr', 'desc_ru': 'desc_ru',
        'case_fan_spd_ua': 'case_fan_spd_ua', 'case_fan_spd_rus': 'case_fan_spd_rus',
        'case_fan_noise_level': 'case_fan_noise_level', 'case_fan_size': 'case_fan_size', 'more': 'more'}

class CASE_otherForm(ModelForm):
    name = forms.CharField()
    part_number = forms.CharField()
    vendor = forms.CharField()
    price = forms.CharField()
    desc_ukr = forms.CharField(widget=forms.Textarea)
    desc_ru = forms.CharField(widget=forms.Textarea)
    case_mb = forms.CharField()
    case_type = forms.CharField()

    class Meta:
        model = CASE_OTHER
        fields = ['name', 'part_number', 'vendor', 'price', 'r_price',
        'desc_ukr', 'desc_ru', 'you_vid', 'label', 'creditoff']

class CaseForm(ModelForm):
    class Meta:
        model = CASE
        fields = ['name', 'part_number', 'vendor', 'price', 'desc_ukr', 'desc_ru', 'case_s',
        'color_parent', 'color', 'color_ukr', 'color_ru', 'depend_to', 'depend_to_type', 'case_height', 'more']
        labels = {'name': 'name', 'part_number': 'part_number', 'vendor': 'vendor',
        'price': 'price', 'desc_ukr': 'desc_ukr', 'desc_ru': 'desc_ru',
        'case_s': 'case_s', 'color_parent': 'color_parent', 'color': 'color',
        'color_ukr': 'color_ukr', 'color_ru': 'color_ru', 'depend_to': 'depend_to',
        'depend_to_type': 'depend_to_type', 'case_height': 'case_height', 'more': 'more'}

class SSD_otherForm(ModelForm):
    name = forms.CharField()
    part_number = forms.CharField()
    vendor = forms.CharField()
    ssd_size = forms.CharField()
    price = forms.CharField()
    desc_ukr = forms.CharField(widget=forms.Textarea)
    desc_ru = forms.CharField(widget=forms.Textarea)
    ssd_nand = forms.CharField()


    class Meta:
        model = SSD_OTHER
        fields = ['name', 'part_number', 'vendor', 'r_price', 'price', 'desc_ukr', 'desc_ru',
                'you_vid', 'label', 'creditoff']

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
