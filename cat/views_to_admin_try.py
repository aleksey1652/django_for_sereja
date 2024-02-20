from cat.models import *
import re
from money.service import cpu_to_code, video_to_code, mem_to_code, video_html, get_art_single_comp, test_art_comp
from scrapy import desktop_agents, random_headers, get_html
import bs4
from bs4 import BeautifulSoup
import requests
from random import choice
from load_form_providers.load_element import get_min_short, to_article2_1
from django.db.models import Q
#providerprice_parts add_or_clear_comp_code

def mem_comparison(name_):
    name_se = re.findall(r'\d+', name_)
    name_se = name_se[0] if name_se else 'пусто'
    short = Parts_short.objects.filter(kind='mem', kind2=False,
    name_parts__startswith=name_se)
    return short

def mb_comparison(name_):
    name_se = re.findall(r'\d+', name_)
    name_se = name_se[0] if name_se else 'пусто'
    short = Parts_short.objects.filter(kind__in=('imb', 'amb'), kind2=False,
    name_parts__iregex=r'^\D+{}'.format(name_se))
    return short

def cpu_comparison(name_):
    name_se = re.findall(r'\d+', name_)
    name_se = name_se[-1] if name_se else 'пусто'
    short = Parts_short.objects.filter(kind__in=('iproc', 'aproc'), kind2=False,
    name_parts__icontains=name_se)
    return short

def video_comparison(name_):
    try:
        split1, split2 = name_.split(' ')
        short = Parts_short.objects.filter(Q(name_parts__icontains=split1) & Q(name_parts__icontains=split2),
        kind='video', kind2=False)
    except:
        split1 = name_.split(' ')[0]
        if split1:
            short = Parts_short.objects.filter(kind='video', kind2=False,
            name_parts__icontains=split1)
        else:
            short = Parts_short.objects.none()
    return short

def ps_comparison(name_):
    name_se = re.findall(r'\d+', name_)
    name_se = name_se[0] if name_se else 'пусто'
    short = Parts_short.objects.filter(kind='ps', kind2=False,
    name_parts__icontains=name_se)
    return short

def ssd_hdd_comparison(name_):
    name_se = re.findall(r'(\d+)[gt]b', name_.lower())
    kind_ = 'ssd' if name_.lower().find('ssd') != -1 else 'hdd'
    name_se = name_se[0] if name_se else 'пусто'
    short = Parts_short.objects.filter(kind=kind_, kind2=False,
    name_parts__iregex=r'{}[gt]b'.format(name_se))
    return short

def case_comparison(name_):
    short = Parts_short.objects.filter(kind='case', kind2=False,
    name_parts=name_)
    return short

def comparison_parts(kind_, name_):
    dict_comparison_parts = {
                            'iproc':'cpu_comparison(name_)',
                            'aproc':'cpu_comparison(name_)',
                            'cool':'None',
                            'imb':'mb_comparison(name_)',
                            'amb':'mb_comparison(name_)',
                            'mem':'mem_comparison(name_)',
                            'hdd':'ssd_hdd_comparison(name_)',
                            'ssd':'ssd_hdd_comparison(name_)',
                            'video':'video_comparison(name_)',
                            'ps':'ps_comparison(name_)',
                            'case':'case_comparison(name_)',
                            'vent':'None',
                            'mon':'None',
                            'cables':'None',
                            'wifi':'None',
                            'km':'None',
                            'soft':'None',
                            }
    return eval(dict_comparison_parts[kind_])

def get_html_from_comp_code(queryset):
    main = '/catalog/kompyutery-artline/grafika='
    return main + '-or-'.join(list(queryset.values_list('video_html_code', flat=True)))

def get_code_from_queryset(queryset):
    queryset_dict = {}
    queryset_list = list(queryset.values_list('cpu_code','video_code','mem_code'))
    queryset_dict['proc_computers'],queryset_dict['video_computers'],queryset_dict['mem_computers'] = list(zip(*queryset_list))
    return queryset_dict

def single_comp_to_code(comp):
    cpu = cpu_to_code(comp.proc_computers)
    video = video_to_code(comp.video_computers)
    video_html_ = video_html(video)
    mem = mem_to_code(comp.mem_computers)
    try:
        comp_code = comp.code
        comp_code.code_is_active = False if comp_code.code_is_active == True else True
        comp_code.cpu_code = cpu
        comp_code.video_code = video
        comp_code.video_html_code = video_html_
        comp_code.mem_code = mem
        comp_code.save()
    except:
        comp_code = Computer_code(comp=comp, cpu_code = cpu, video_code = video, mem_code = mem, video_html_code = video_html_)
        comp_code.save()

def add_or_clear_comp_code(selected_comps):
    for comp in selected_comps:
        single_comp_to_code(comp)

def create_or_update_single_art_comp(comp, queryset):
    usd = USD.objects.last().usd
    try:
        comp['price_computers'] = round(float(comp['price_computers']) / usd)
    except:
        comp['price_computers'] = 0
    queryset_dict = get_code_from_queryset(queryset)
    if (comp['proc_computers'] in queryset_dict['proc_computers'] or queryset_dict['proc_computers'] == (None,)) and  (comp['mem_computers'] in queryset_dict['mem_computers'] or queryset_dict['mem_computers'] == (None,)):
        if Computers.objects.filter(name_computers=comp['name_computers'], pc_assembly__sites__name_sites='art').exists():
            art_comp = Computers.objects.get(name_computers=comp['name_computers'], pc_assembly__sites__name_sites='art')
            art_comp.is_active = True
            for k,v in comp.items():
                art_comp.__dict__[k] = v
            art_comp.save()
        else:
            assembly = Pc_assembly.objects.get(sites__name_sites='art')
            Computers.objects.create(name_computers=comp['name_computers'], url_computers='',
            price_computers=comp['price_computers'],proc_computers=comp['proc_computers'],
            mb_computers=comp['mb_computers'],mem_computers=comp['mem_computers'],
            video_computers=comp['video_computers'],hdd_computers=comp['hdd_computers'],
            ps_computers=comp['ps_computers'],case_computers=comp['case_computers'],
            cool_computers='',class_computers=' ',
            warranty_computers='', mon_computers='',wifi_computers='',km_computers='',
            vent_computers='',vent_num_computers='',mem_num_computers='',
            video_num_computers='', pc_assembly=assembly)

def get_soup_art(url, queryset_set):
    queryset = Computer_code.objects.filter(pk__in=queryset_set)
    label = 'product-cart product-cart-js'
    label_per_video_filter = get_html_from_comp_code(queryset)
    dict_art={}
    #url_list = []
    #list_error = []
    for m in range(1,6):
        g = get_html(url + label_per_video_filter + f'/page={m}')
        print(url + label_per_video_filter + f'/page={m}')
        if g:
            soup = BeautifulSoup(g, "html.parser")
            comps = soup.find_all(class_=label)
            #print(f'find {len(comps)} comps')
            if comps:
                for comp in comps:
                    if isinstance(comp, bs4.element.Tag) and comp.has_attr('data-url'):
                        url_comp = comp['data-url']
                        #url_list.append(url_comp)
                        data_ = get_art_single_comp(url_comp)
                        if test_art_comp(data_):
                            print(url_comp)
                            create_or_update_single_art_comp(data_, queryset)
                            dict_art[data_['name_computers']] = data_
