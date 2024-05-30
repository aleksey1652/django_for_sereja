from django.forms import ModelForm, Textarea, CharField, ChoiceField
from .models import Pc_assembly
from django.core.exceptions import ValidationError
from django import forms

"""short_aproc = Parts_short.objects.filter(kind='aproc',kind2=False).values_list('name_parts',flat=True)
CHOISE_aproc = [(short, short) for short in short_aproc]"""

class ShortForm_aproc(forms.Form):
    proc = forms.ChoiceField(
        choices=('пусто','пусто'),#CHOISE_aproc,
        label=''
    )

"""short_amb = Parts_short.objects.filter(kind='amb',kind2=False).values_list('name_parts',flat=True)
CHOISE_amb = [(short, short) for short in short_amb]"""

class ShortForm_amb(forms.Form):
    mb = forms.ChoiceField(
        choices=('пусто','пусто'),#CHOISE_amb,
        label=''
    )

"""short_iproc = Parts_short.objects.filter(kind='iproc',kind2=False).values_list('name_parts',flat=True)
CHOISE_iproc = [(short, short) for short in short_iproc]"""

class ShortForm_iproc(forms.Form):
    proc = forms.ChoiceField(
        choices=('пусто','пусто'),#CHOISE_iproc,
        label=''
    )

"""short_imb = Parts_short.objects.filter(kind='imb',kind2=False).values_list('name_parts',flat=True)
CHOISE_imb = [(short, short) for short in short_imb]"""

class ShortForm_imb(forms.Form):
    mb = forms.ChoiceField(
        choices=('пусто','пусто'),#CHOISE_imb,
        label=''
    )

"""short_case = Parts_short.objects.filter(kind='case',kind2=False).values_list('name_parts',flat=True)
CHOISE_case = [(short, short) for short in short_case]"""

class ShortForm_case(forms.Form):
    case = forms.ChoiceField(
        choices=('пусто','пусто'),#CHOISE_case,
        label=''
    )

"""hdd_ssd = Parts_short.objects.filter(kind__in=('hdd','ssd'),kind2=False).values_list('name_parts',flat=True)
CHOISE_hdd_ssd = [(short, short) for short in hdd_ssd]"""

class ShortForm_hdd_ssd(forms.Form):
    hdd_ssd = forms.ChoiceField(
        choices=('пусто','пусто'),#CHOISE_hdd_ssd,
        label=''
    )

class ShortForm_hdd_ssd2(forms.Form):
    hdd_ssd2 = forms.ChoiceField(
        choices=('пусто','пусто'),#CHOISE_hdd_ssd,
        label=''
    )
"""short_hdd = Parts_short.objects.filter(kind='hdd',kind2=False).values_list('name_parts',flat=True)
CHOISE_hdd = [(short, short) for short in short_hdd]

class ShortForm_hdd(forms.Form):
    hdd = forms.ChoiceField(
        choices=CHOISE_hdd,
        label=''
    )"""

"""short_cool = Parts_short.objects.filter(kind='cool',kind2=False).values_list('name_parts',flat=True)
CHOISE_cool = [(short, short) for short in short_cool]"""

class ShortForm_cool(forms.Form):
    cool = forms.ChoiceField(
        choices=('пусто','пусто'),#CHOISE_cool,
        label=''
    )

"""short_video = Parts_short.objects.filter(kind='video',kind2=False).values_list('name_parts',flat=True)
CHOISE_video = [(short, short) for short in short_video]"""

class ShortForm_video(forms.Form):
    video = forms.ChoiceField(
        choices=('пусто','пусто'),#CHOISE_video,
        label=''
    )

"""short_mem = Parts_short.objects.filter(kind='mem',kind2=False).values_list('name_parts',flat=True)
CHOISE_mem = [(short, short) for short in short_mem]"""

class ShortForm_mem(forms.Form):
    mem = forms.ChoiceField(
        choices=('пусто','пусто'),#CHOISE_mem,
        label=''
    )

"""short_ps = Parts_short.objects.filter(kind='ps',kind2=False).values_list('name_parts',flat=True)
CHOISE_ps = [(short, short) for short in short_ps]"""

class ShortForm_ps(forms.Form):
    ps = forms.ChoiceField(
        choices=('пусто','пусто'),#CHOISE_ps,
        label=''
    )

"""short_vent = Parts_short.objects.filter(kind='vent',kind2=False).values_list('name_parts',flat=True)
CHOISE_vent = [(short, short) for short in short_vent]"""

class ShortForm_vent(forms.Form):
    vent = forms.ChoiceField(
        choices=('пусто','пусто'),#CHOISE_vent,
        label=''
    )

"""short_mon = Parts_short.objects.filter(kind='mon',kind2=False).values_list('name_parts',flat=True)
CHOISE_mon = [(short, short) for short in short_mon]"""

class ShortForm_mon(forms.Form):
    mon = forms.ChoiceField(
        choices=('пусто','пусто'),#CHOISE_mon,
        label=''
    )

"""short_wifi = Parts_short.objects.filter(kind='wifi',kind2=False).values_list('name_parts',flat=True)
CHOISE_wifi = [(short, short) for short in short_wifi]"""

class ShortForm_wifi(forms.Form):
    wifi = forms.ChoiceField(
        choices=('пусто','пусто'),#CHOISE_wifi,
        label=''
    )

"""short_km = Parts_short.objects.filter(kind='km',kind2=False).values_list('name_parts',flat=True)
CHOISE_km = [(short, short) for short in short_km]"""

class ShortForm_km(forms.Form):
    km = forms.ChoiceField(
        choices=('пусто','пусто'),#CHOISE_km,
        label=''
    )

"""short_soft = Parts_short.objects.filter(kind='soft',kind2=False).values_list('name_parts',flat=True)
CHOISE_soft = [(short, short) for short in short_soft]"""

class ShortForm_soft(forms.Form):
    soft = forms.ChoiceField(
        choices=('пусто','пусто'),#CHOISE_soft,
        label=''
    )

"""short_cables = Parts_short.objects.filter(kind='cables',kind2=False).values_list('name_parts',flat=True)
CHOISE_cables = [(short, short) for short in short_cables]"""

class ShortForm_cables(forms.Form):
    cables = forms.ChoiceField(
        choices=('пусто','пусто'),#CHOISE_cables,
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

"""promotion = Promotion.objects.all().values_list('prom',flat=True)
CHOISE_promotion = [(short, short) for short in promotion]"""

class Form_promotion(forms.Form):
    promotion = forms.ChoiceField(
        choices=('пусто','пусто'),#CHOISE_promotion,
        label='')

class Pc_assemblyForm(ModelForm):
    name_ass = Pc_assembly.objects.filter(sites__name_sites='versum').values_list('name_assembly',flat=True)
    CHOISE_name_ass = set([(short, short) for short in name_ass])
    name_assembly = forms.ChoiceField(
        choices=CHOISE_name_ass,
        label='')

    kind_ass = Pc_assembly.objects.filter(sites__name_sites='versum').values_list('kind_assembly',flat=True)
    CHOISE_kind_ass = set([(short, short) for short in kind_ass])
    kind_assembly = forms.ChoiceField(
        choices=CHOISE_kind_ass,
        label='')

    class Meta:
        model = Pc_assembly
        fields = ['name_assembly', 'kind_assembly', 'sites']
        labels = { 'name_assembly': 'Группа', 'kind_assembly': 'Серия', 'sites': 'Сайт'}
