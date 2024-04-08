from django.forms import ModelForm, Textarea, CharField, ChoiceField
from .models import *
from django.core.exceptions import ValidationError
from django import forms
#providerprice_parts price Form_text_input

dict_kind_to_short = {
'iproc': 'proc_computers',
'aproc':'proc_computers',
'cool':'cool_computers',
'imb':'mb_computers',
'amb':'mb_computers',
'mem':'mem_computers',
'hdd':'hdd_computers',
'ssd':'hdd_computers',
'video':'video_computers',
'ps':'ps_computers',
'vent':'vent_computers',
'case':'case_computers',
'wifi':'wifi_computers',
'cables':'cables_computers',
'soft':'soft_computers',
'mon': 'mon_computers',
'km': 'km_computers'
                    }

dict_form_to_short = {
'proc': 'proc_computers',
'mb': 'mb_computers',
'case': 'case_computers',
'hdd_ssd': 'hdd_computers',
'cool': 'cool_computers',
'video': 'video_computers',
'mem': 'mem_computers',
'ps': 'ps_computers',
'vent': 'vent_computers',
'mon': 'mon_computers',
'wifi': 'wifi_computers',
'km': 'km_computers',
'soft': 'soft_computers',
'cables': 'cables_computers'
}

try:
    short_aproc = Parts_short.objects.filter(kind='aproc',kind2=False).values_list('name_parts',flat=True)
    CHOISE_aproc = [(short, short) for short in short_aproc]
except:
    CHOISE_aproc = [('AMD', 'AMD')]

class ShortForm_aproc(forms.Form):
    proc = forms.ChoiceField(
        choices=CHOISE_aproc,
        label=''
    )

try:
    short_amb = Parts_short.objects.filter(kind='amb',kind2=False).values_list('name_parts',flat=True)
    CHOISE_amb = [(short, short) for short in short_amb]
except:
    CHOISE_amb = [('AMD', 'AMD')]

class ShortForm_amb(forms.Form):
    mb = forms.ChoiceField(
        choices=CHOISE_amb,
        label=''
    )

try:
    short_iproc = Parts_short.objects.filter(kind='iproc',kind2=False).values_list('name_parts',flat=True)
    CHOISE_iproc = [(short, short) for short in short_iproc]
except:
    CHOISE_iproc = [('AMD', 'AMD')]

class ShortForm_iproc(forms.Form):
    proc = forms.ChoiceField(
        choices=CHOISE_iproc,
        label=''
    )

try:
    short_imb = Parts_short.objects.filter(kind='imb',kind2=False).values_list('name_parts',flat=True)
    CHOISE_imb = [(short, short) for short in short_imb]
except:
    CHOISE_imb = [('AMD', 'AMD')]


class ShortForm_imb(forms.Form):
    mb = forms.ChoiceField(
        choices=CHOISE_imb,
        label=''
    )
try:
    short_case = Parts_short.objects.filter(kind='case',kind2=False).values_list('name_parts',flat=True)
    CHOISE_case = [(short, short) for short in short_case]
except:
    CHOISE_case = [('AMD', 'AMD')]

class ShortForm_case(forms.Form):
    case = forms.ChoiceField(
        choices=CHOISE_case,
        label=''
    )

try:
    hdd_ssd = Parts_short.objects.filter(kind__in=('hdd','ssd'),kind2=False).values_list('name_parts',flat=True)
    CHOISE_hdd_ssd = [(short, short) for short in hdd_ssd]
except:
    CHOISE_hdd_ssd = [('AMD', 'AMD')]


class ShortForm_hdd_ssd(forms.Form):
    hdd_ssd = forms.ChoiceField(
        choices=CHOISE_hdd_ssd,
        label=''
    )

class ShortForm_hdd_ssd2(forms.Form):
    hdd_ssd2 = forms.ChoiceField(
        choices=CHOISE_hdd_ssd,
        label=''
    )
"""short_hdd = Parts_short.objects.filter(kind='hdd',kind2=False).values_list('name_parts',flat=True)
CHOISE_hdd = [(short, short) for short in short_hdd]

class ShortForm_hdd(forms.Form):
    hdd = forms.ChoiceField(
        choices=CHOISE_hdd,
        label=''
    )"""
try:
    short_cool = Parts_short.objects.filter(kind='cool',kind2=False).values_list('name_parts',flat=True)
    CHOISE_cool = [(short, short) for short in short_cool]
except:
    CHOISE_cool = [('AMD', 'AMD')]

class ShortForm_cool(forms.Form):
    cool = forms.ChoiceField(
        choices=CHOISE_cool,
        label=''
    )
try:
    short_video = Parts_short.objects.filter(kind='video',kind2=False).values_list('name_parts',flat=True)
    CHOISE_video = [(short, short) for short in short_video]
except:
    CHOISE_video = [('AMD', 'AMD')]

class ShortForm_video(forms.Form):
    video = forms.ChoiceField(
        choices=CHOISE_video,
        label=''
    )
try:
    short_mem = Parts_short.objects.filter(kind='mem',kind2=False).values_list('name_parts',flat=True)
    CHOISE_mem = [(short, short) for short in short_mem]
except:
    CHOISE_mem = [('AMD', 'AMD')]


class ShortForm_mem(forms.Form):
    mem = forms.ChoiceField(
        choices=CHOISE_mem,
        label=''
    )
try:
    short_ps = Parts_short.objects.filter(kind='ps',kind2=False).values_list('name_parts',flat=True)
    CHOISE_ps = [(short, short) for short in short_ps]
except:
    CHOISE_ps = [('AMD', 'AMD')]

class ShortForm_ps(forms.Form):
    ps = forms.ChoiceField(
        choices=CHOISE_ps,
        label=''
    )
try:
    short_vent = Parts_short.objects.filter(kind='vent',kind2=False).values_list('name_parts',flat=True)
    CHOISE_vent = [(short, short) for short in short_vent]
except:
    CHOISE_vent = [('AMD', 'AMD')]

class ShortForm_vent(forms.Form):
    vent = forms.ChoiceField(
        choices=CHOISE_vent,
        label=''
    )
try:
    short_mon = Parts_short.objects.filter(kind='mon',kind2=False).values_list('name_parts',flat=True)
    CHOISE_mon = [(short, short) for short in short_mon]
except:
    CHOISE_mon = [('AMD', 'AMD')]

class ShortForm_mon(forms.Form):
    mon = forms.ChoiceField(
        choices=CHOISE_mon,
        label=''
    )
try:
    short_wifi = Parts_short.objects.filter(kind='wifi',kind2=False).values_list('name_parts',flat=True)
    CHOISE_wifi = [(short, short) for short in short_wifi]
except:
    CHOISE_wifi = [('AMD', 'AMD')]


class ShortForm_wifi(forms.Form):
    wifi = forms.ChoiceField(
        choices=CHOISE_wifi,
        label=''
    )
try:
    short_km = Parts_short.objects.filter(kind='km',kind2=False).values_list('name_parts',flat=True)
    CHOISE_km = [(short, short) for short in short_km]
except:
    CHOISE_km = [('AMD', 'AMD')]

class ShortForm_km(forms.Form):
    km = forms.ChoiceField(
        choices=CHOISE_km,
        label=''
    )
try:
    short_soft = Parts_short.objects.filter(kind='soft',kind2=False).values_list('name_parts',flat=True)
    CHOISE_soft = [(short, short) for short in short_soft]
except:
    CHOISE_soft = [('AMD', 'AMD')]

class ShortForm_soft(forms.Form):
    soft = forms.ChoiceField(
        choices=CHOISE_soft,
        label=''
    )
try:
    short_cables = Parts_short.objects.filter(kind='cables',kind2=False).values_list('name_parts',flat=True)
    CHOISE_cables = [(short, short) for short in short_cables]
except:
    CHOISE_cables = [('AMD', 'AMD')]

class ShortForm_cables(forms.Form):
    cables = forms.ChoiceField(
        choices=CHOISE_cables,
        label=''
    )

CHOISE_num = (
    ('1', 'x1'),
    ('2', 'x2'),
    ('3', 'x3'),
    ('4', 'x4'),
)

class Form_mem_num(forms.Form):
    mem_num = forms.ChoiceField(
        choices=CHOISE_num,
        label='')

class Form_vent_num(forms.Form):
    vent_num = forms.ChoiceField(
        choices=CHOISE_num,
        label='')

class Form_video_num(forms.Form):
    video_num = forms.ChoiceField(
        choices=CHOISE_num,
        label='')


dict_form = {
'proc_computers': ["ShortForm_aproc(initial={'proc':v})", "ShortForm_iproc(initial={'proc':v})"],
'mb_computers': ["ShortForm_amb(initial={'mb':v})", "ShortForm_imb(initial={'mb':v})"],
'mem_computers': "ShortForm_mem(initial={'mem':v})",
'video_computers': "ShortForm_video(initial={'video':v})",
'case_computers': "ShortForm_case(initial={'case':v})",
'ps_computers': "ShortForm_ps(initial={'ps':v})",
'hdd_computers': "ShortForm_hdd_ssd(initial={'hdd_ssd':v})",
'hdd2_computers': "ShortForm_hdd_ssd2(initial={'hdd_ssd2':v})",
'cool_computers': "ShortForm_cool(initial={'cool':v})",
'vent_computers': "ShortForm_vent(initial={'vent':v})",
'mon_computers': "ShortForm_mon(initial={'mon':v})",
'soft_computers': "ShortForm_soft(initial={'soft':v})",
'cables_computers': "ShortForm_cables(initial={'cables':v})",
'km_computers': "ShortForm_km(initial={'km':v})",
'wifi_computers': "ShortForm_wifi(initial={'wifi':v})",
'video_computers_num': Form_video_num(),
'mem_computers_num': Form_mem_num(),
'vent_computers_num': Form_vent_num()
}
try:
    promotion = Promotion.objects.all().values_list('prom',flat=True)
    CHOISE_promotion = [(short, short) for short in promotion]
except:
    CHOISE_promotion = [('AMD', 'AMD')]

class Form_promotion(forms.Form):
    promotion = forms.ChoiceField(
        choices=CHOISE_promotion,
        label='')

class Pc_assemblyForm(forms.Form):
    try:
        name_ass = Pc_assembly.objects.filter(
        sites__name_sites='versum').values_list('name_assembly',flat=True).distinct()
        CHOISE_name_ass = set([(short, short) for short in name_ass])
    except:
        CHOISE_name_ass = [('AMD', 'AMD')]

    name_assembly = forms.ChoiceField(
        choices=CHOISE_name_ass,
        label='Группа')

    try:
        kind_ass = Pc_assembly.objects.filter(
        sites__name_sites='versum').values_list('kind_assembly',flat=True).distinct()
        CHOISE_kind_ass = set([(short, short) for short in kind_ass])
    except:
        CHOISE_kind_ass = [('AMD', 'AMD')]

    kind_assembly = forms.ChoiceField(
        choices=CHOISE_kind_ass,
        label='Серия')

"""class Pc_assemblyForm(ModelForm):
    class Meta:
        model = Pc_assembly
        fields = ['name_assembly', 'kind_assembly']
        labels = { 'name_assembly': 'Группа', 'kind_assembly': 'Серия'}"""

class Comps_time_assemblyForm(ModelForm):
    class Meta:
        model = Computers
        fields = ['time_assembly_ru', 'time_assembly_ukr']
        labels = { 'time_assembly_ru': 'Срок сборки(ру)',
        'time_assembly_ukr': 'Срок сборки(укр)'}

class PromotionForCompsForm(ModelForm):
    class Meta:
        model = Promotion
        fields = ['prom', 'prom']
        labels = { 'prom': 'Ярлык'}

class FullForm(forms.Form):
    full = forms.CharField(label='', )
    price_full = forms.FloatField(label='', initial=0)

CHOISE_type = (
    ('AMD', 'AMD'),
    ('Intel', 'Intel'),
)
#
CHOISE_Num_Vent = (
    ('пусто', 'пусто'),
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
)

class Form_num_vent(forms.Form):
    num = forms.ChoiceField(
        widget=forms.Select(attrs={"class":"myfield"}),
        choices=CHOISE_Num_Vent,
        label='',
        help_text="Выберите пусто или кол"
        )

class Form_amd_intel(forms.Form):
    calc = forms.ChoiceField(
        widget=forms.Select(attrs={"class":"myfield"}),
        choices=CHOISE_type,
        label='',
        help_text="Выберите платформу"
        )

class Form_new_comp(forms.Form):
    calc = forms.ChoiceField(
        widget=forms.Select(attrs={"class":"myfield"}),
        choices=CHOISE_type,
        label='',
        help_text="Выберите платформу"
        )
    new = forms.CharField(
        widget=forms.TextInput(attrs={"class":"myfield"}),
        label='',
        help_text="Название"
        )

class Short_kind_Form(ModelForm):
    class Meta:
        model = Parts_short
        fields = ['kind']
        labels = {'kind': 'kind'}

class Form_text_input(forms.Form):
    new = forms.CharField(
        label='',
        initial='Ручной ввод детали',
        widget=forms.TextInput(attrs={'style': 'width: 486px;'}),
    )
