from django.shortcuts import render
from .models import *
from django.db.models import Q
from cat.forms import *

# shorts_in_comps

def content_parts_filter(key_, value_, num="1"):

    dict_atr = {
    'mb_computers': 'mb',
    'proc_computers': 'cpu',
    'mem_computers': 'ram',
    'video_computers': 'gpu',
    'hdd': 'hdd',
    'ssd': 'ssd',
    'case_computers': 'case',
    'ps_computers': 'psu',
    'cool_computers': 'cooler',
    'vent_computers': 'fan',
    'wifi_computers': 'wifi',
    'cables_computers': 'cables',
    'soft_computers': 'soft',
    'pc_assembly__kind_assembly': 'category',
    'pc_assembly__desc_ru': 'desc_ru',
    'pc_assembly__desc_ukr': 'desc_ukr',
    'promotion': 'promotion',
    'you_vid': 'you_vid',
    'perm_conf': 'perm_conf',
    'elite_conf': 'elite_conf',
    'time_assembly_ru': 'time_assembly_ru',
    'time_assembly_ukr': 'time_assembly_ukr',
                }

    dict_v = {
    'proc_computers': "CPU.objects.get(name=value_)",
    'cool_computers': "Cooler.objects.get(name=value_)",
    'mb_computers': "MB.objects.get(name=value_)",
    'mem_computers': "RAM.objects.get(name=value_)",
    'video_computers': "GPU.objects.get(name=value_)",
    'ps_computers': "PSU.objects.get(name=value_)",
    'vent_computers': "FAN.objects.get(name=value_)",
    'case_computers': "CASE.objects.get(name=value_)",
    'wifi_computers': "WiFi.objects.get(name=value_)",
    'cables_computers': "Cables.objects.get(name=value_)",
    'soft_computers': "Soft.objects.get(name=value_)",
    'ssd': "SSD.objects.get(name=value_)",
    'hdd': "HDD.objects.get(name=value_)"
            }

    if value_ == 'пусто' and key_ not in ('you_vid', 'perm_conf', 'elite_conf',
                                        'time_assembly_ru', 'time_assembly_ukr'):
        try:
            return [
                    dict_atr[key_],
                    "пусто",
                    "",
                    "1"
                    ]
        except:
            return [
                key_,
                "пусто",
                "",
                "1"
                ]

    if key_ in dict_v:
        try:
            temp = [
                    dict_atr[key_],
                    value_,
                    eval(dict_v[key_]).part_number,
                    num
                    ]
        except:
            temp = [
                    dict_atr[key_],
                    "пусто",
                    "",
                    "1"
                    ]
        return temp
    elif key_ in dict_atr:
        return [
                dict_atr[key_],
                value_
                ]
    elif key_ == 'hdd_computers':
        hdd_ssd = value_.split(';')
        temp = []
        for hdd_or_ssd in hdd_ssd:
            if  hdd_or_ssd.lower().find('ssd') != -1:
                try:
                    temp.append(
                    [
                            'ssd',
                            hdd_or_ssd,
                            SSD.objects.get(name=hdd_or_ssd).part_number,
                            '1'
                            ]
                                )
                except:
                    temp.append(
                    [
                            'ssd',
                            "пусто",
                            "",
                            "1"
                            ]
                                )
        for hdd_or_ssd in hdd_ssd:
            if  hdd_or_ssd.lower().find('ssd') == -1 and hdd_or_ssd.lower() != 'пусто':
                try:
                    temp.append(
                    [
                            'hdd',
                            hdd_or_ssd,
                            HDD.objects.get(name=hdd_or_ssd).part_number,
                            '1'
                            ]
                                )
                except:
                    temp.append(
                    [
                            'hdd',
                            "пусто",
                            "",
                            "1"
                            ]
                                )
        if len(temp) == 1 and temp[0][0] == 'ssd':
            temp.append(
            [
                'hdd',
                'пусто',
                '',
                '1'
                ]
                        )
        elif len(temp) == 1 and temp[0][0] == 'hdd':
                temp.append(
                [
                    'ssd',
                    'пусто',
                    '',
                    '1'
                    ]
                            )
        return temp

    else:
        return value_
#
def shorts_in_comps():
    shorts = Parts_short.objects.filter(kind2=False)
    for short in shorts:
        search_term = short.name_parts
        queryset = Computers.objects.filter(
        Q(video_computers__exact=search_term)|
        Q(proc_computers__exact=search_term) |Q (mem_computers__exact=search_term)|
        Q(mb_computers__exact=search_term) | Q(vent_computers__exact=search_term)|
        Q(hdd_computers__icontains=search_term) | Q(cool_computers__exact=search_term)|
        Q(case_computers__exact=search_term) | Q(ps_computers__exact=search_term)|
        Q(wifi_computers__exact=search_term) | Q(soft_computers__exact=search_term)|
        Q(cables_computers__exact=search_term)
        )#.exclude(pc_assembly__name_assembly='For Today') # исключаем For Today
        if queryset.exclude(pc_assembly__name_assembly='For Today').exists():
            short.in_comps = True
            short.computer_shorts.clear()
            short.save()
        elif not queryset.exists():
            short.in_comps = False
            short.computer_shorts.clear()
            short.save()
        elif queryset.filter(pc_assembly__name_assembly='For Today').exists():
            short.in_comps = False
            short.computer_shorts.clear()
            short.computer_shorts.add(
            queryset.filter(pc_assembly__name_assembly='For Today').first()
            )
            short.save()



def get_comp_for_api(comp):

    list_comp = [
                [comp.name_computers, comp.pk]
                ]

    comp_values = Computers.objects.filter(pk=comp.pk).values(
    'mb_computers',
    'proc_computers',
    'mem_computers',
    'video_computers',
    'hdd_computers',
    'case_computers',
    'ps_computers',
    'cool_computers',
    'vent_computers',
    'wifi_computers',
    'cables_computers',
    'soft_computers',
    'pc_assembly__kind_assembly',
    'pc_assembly__desc_ru',
    'pc_assembly__desc_ukr',
    'promotion',
    'you_vid',
    'perm_conf',
    'elite_conf',
    'time_assembly_ru',
    'time_assembly_ukr')

    for k, v in comp_values[0].items():
        if k == 'hdd_computers':
            list_comp += content_parts_filter('hdd_computers', comp.hdd_computers, num="1")
        elif k == 'promotion':
            prom = ["promotion"] + [x['english_prom'] if x else 'пусто' for x in comp.promotion_set.all().values('english_prom')]
            list_comp.append(prom)
        elif k == 'mem_computers':
            list_comp.append(content_parts_filter(k, v, num=comp.mem_num_computers))
        elif k == 'video_computers':
            list_comp.append(content_parts_filter(k, v, num=comp.video_num_computers))
        elif k == 'vent_computers':
            list_comp.append(content_parts_filter(k, v, num=comp.vent_num_computers))
        else:
            list_comp.append(content_parts_filter(k, v, num="1"))
    return list_comp

def content_comp_filter(dict_):
    list_atr = ['mb_computers', 'proc_computers', 'mem_computers', 'video_computers',
    'hdd_computers', 'case_computers', 'ps_computers', 'cool_computers','vent_computers',
    'wifi_computers','cables_computers','soft_computers']

    dict_result = [[dict_['name_computers'],dict_['id']]]

    hdd_ssd = dict_['hdd_computers'].split(';')
    hdd_ssd_list = [['ssd', hdd_or_ssd, content_parts_filter('ssd', hdd_or_ssd), "1"] if hdd_or_ssd.lower().find('ssd') != -1 else ['hdd', hdd_or_ssd, content_parts_filter('hdd', hdd_or_ssd), "1"] for hdd_or_ssd in hdd_ssd]

    for k, v in dict_.items():
        dict_result.append(content_parts_filter(k, v, num="1", hdd_or_ssd=''))






def test_distrib(kind, se=''):
    if kind in ('soft', 'wifi', 'cables', 'hdd', 'ssd', 'vent', 'ps', 'amb', 'imb') and se == 'пусто':
        return True

    dict_base_name = {'aproc':CPU.objects.filter(name=se, is_active=True),
                'iproc':CPU.objects.filter(name=se, is_active=True),
                'amb':MB.objects.filter(name=se, is_active=True),
                'imb':MB.objects.filter(name=se, is_active=True),
                'mem':RAM.objects.filter(name=se, is_active=True),
                'hdd':HDD.objects.filter(name=se, is_active=True),
                'ssd':SSD.objects.filter(name=se, is_active=True),
                'video':GPU.objects.filter(name=se, is_active=True),
                'ps':PSU.objects.filter(name=se, is_active=True),
                'vent':FAN.objects.filter(name=se, is_active=True),
                'case':CASE.objects.filter(name=se, is_active=True),
                'wifi':WiFi.objects.filter(name=se, is_active=True),
                'cables':Cables.objects.filter(name=se, is_active=True),
                'soft':Soft.objects.filter(name=se, is_active=True),
                'cool':Cooler.objects.filter(name=se, is_active=True),
                'mon':CPU.objects.none(),
                'km':CPU.objects.none()
                }
    try:
        if dict_base_name[kind].exists() and dict_base_name[kind].count() == 1:
            return True
        else:
            return False
    except KeyError:
        return False

def test_distrib_price_none():
    list_res = []
    dict_base_name = {'aproc':CPU.objects.filter(Q(price=0)|Q(price__isnull=True), is_active=True),
                'iproc':CPU.objects.filter(Q(price=0)|Q(price__isnull=True), is_active=True),
                'amb':MB.objects.filter(Q(price=0)|Q(price__isnull=True), is_active=True),
                'imb':MB.objects.filter(Q(price=0)|Q(price__isnull=True), is_active=True),
                'mem':RAM.objects.filter(Q(price=0)|Q(price__isnull=True), is_active=True),
                'hdd':HDD.objects.filter(Q(price=0)|Q(price__isnull=True), is_active=True),
                'ssd':SSD.objects.filter(Q(price=0)|Q(price__isnull=True), is_active=True),
                'video':GPU.objects.filter(Q(price=0)|Q(price__isnull=True), is_active=True),
                'ps':PSU.objects.filter(Q(price=0)|Q(price__isnull=True), is_active=True),
                'vent':FAN.objects.filter(Q(price=0)|Q(price__isnull=True), is_active=True),
                'case':CASE.objects.filter(Q(price=0)|Q(price__isnull=True), is_active=True),
                'wifi':WiFi.objects.filter(Q(price=0)|Q(price__isnull=True), is_active=True),
                'cables':Cables.objects.filter(Q(r_price=0)|Q(r_price__isnull=True), is_active=True),
                'soft':Soft.objects.filter(Q(price=0)|Q(price__isnull=True), is_active=True),
                'cool':Cooler.objects.filter(Q(price=0)|Q(price__isnull=True), is_active=True),
                }

    for v in dict_base_name.values():
        temp = [t.name for t in v if t]
        list_res += temp

    return set(list_res)
