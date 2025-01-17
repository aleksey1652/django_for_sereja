from cat.models import *
from money.models import Gross_profit
from descriptions.models import *
from cat.forms_admin_comps import *
from load_form_providers.load_element import to_article2_1
import re
from money.service import cpu_to_code, video_to_code, mem_to_code, video_html, get_art_single_comp, test_art_comp
from scrapy import desktop_agents, random_headers, get_html
import bs4
from bs4 import BeautifulSoup
import requests
from random import choice
from load_form_providers.load_element import get_min_short, to_article2_1
from cat.views_to_admin_try import *
from django.db.models import Q
#providerprice_parts x_code  get_comp_context

def count_video_price_per_our_price(art_comp_price, parts_price):
    margin = Gross_profit.objects.filter(site='Versum').last()
    margin = 1 + (margin.rentability)/100 if margin else 0
    if isinstance(art_comp_price, int) and  isinstance(parts_price, float) and  isinstance(margin, float):
        return round(float(art_comp_price - parts_price * margin)/margin)
    else:
        return 0.0

def get_comp_context(object_id):
    comp = Computers.objects.filter(pk=object_id)

    comp_parts = comp.values(
    'proc_computers', 'cool_computers', 'mb_computers',
    'mem_computers', 'video_computers', 'hdd_computers',
    'ps_computers', 'case_computers', 'vent_computers',
    'vent_computers', 'mon_computers', 'wifi_computers',
    'km_computers', 'cables_computers', 'soft_computers')[0]
    try:
        comp_parts['hdd2_computers'] = comp_parts['hdd_computers'].split(';')[1]
    except:
        comp_parts['hdd2_computers'] = 'пусто'
    comp_parts['hdd_computers'] = comp_parts['hdd_computers'].split(';')[0]

    comp_num = comp.values('mem_num_computers', 'video_num_computers', 'vent_num_computers')[0]

    list_form = []
    price_count = 0
    amd_intel = to_article2_1(comp[0].proc_computers)
    for k, v in comp_parts.items():
        v = v if v else 'пусто'
        if k not in ('hdd2_computers', 'hdd_computers'):
            try:
                if k in ('mb_computers', 'proc_computers') and amd_intel == 'aproc':
                    kind_ = 'a' + k[:-10]
                    short = Parts_short.objects.filter(kind=kind_, kind2=False,
                    name_parts=v)
                elif k in ('mb_computers', 'proc_computers') and amd_intel == 'iproc':
                    kind_ = 'i' + k[:-10]
                    short = Parts_short.objects.filter(kind=kind_, kind2=False,
                    name_parts=v)
                else:
                    kind_ = k[:-10]
                    short = Parts_short.objects.filter(kind=kind_, kind2=False,
                    name_parts=v)
                try:
                    #price = round(float(short.values_list('parts_full__providerprice_parts',flat=True)[0]))
                    price = round(float(short.values_list('x_code',flat=True)[0]))
                except:
                    price = 0
                short_pk = short.first().pk if short.exists() else 0
                if k == 'mem_computers':
                    try:
                        price = f"({price} x{comp_num['mem_num_computers']})"
                    except:
                        price = f"({price} x1)"
                if k == 'video_computers':
                    try:
                        price = f"({price} x{comp_num['video_num_computers']})"
                    except:
                        price = f"({price} x1)"
                if k == 'vent_computers':
                    try:
                        price = f"({price} x{comp_num['vent_num_computers']})"
                    except:
                        price = f"({price} x1)"
            except:
                price = 0
                price, short_pk = 0, 0
            try:
                price_count += price
            except:
                try:
                    n, m = round(float(re.findall(r'\d+',price)[0])), int(re.findall(r'\d+',price)[1])
                    price_count += n*m
                except:
                    price_count = 0
        else:
            try:
                short = Parts_short.objects.filter(kind__in=('hdd', 'ssd'),
                kind2=False, name_parts=v)
                try:
                    #price = round(float(short.values_list('parts_full__providerprice_parts',flat=True)[0])) #x_code
                    price = round(float(short.values_list('x_code',flat=True)[0])) #x_code
                except:
                    price = 0
                short_pk = short.first().pk if short.exists() else 0
            except:
                price, short_pk = 0, 0
            price_count += price
        link_ = f"{short_pk},Parts_short{comp[0].pk}" if short_pk else None
        short_ = Parts_short.objects.filter(kind=kind_,kind2=False).values_list('name_parts',flat=True)
        CHOISE_ = [(short, short) for short in short_]
        if k in ('proc_computers', 'mb_computers'):
            if amd_intel == 'aproc':
                form_ = eval(dict_form[k][0])
                key_ = list(form_.fields.keys())[0]
                form_.base_fields[key_].choices = CHOISE_
                list_form.append((form_, price, link_, k))
                #list_form.append((eval(dict_form[k][0]), price, link_, k))
            else:
                form_ = eval(dict_form[k][1])
                key_ = list(form_.fields.keys())[0]
                form_.base_fields[key_].choices = CHOISE_
                list_form.append((form_, price, link_, k))
                #list_form.append((eval(dict_form[k][1]), price, link_, k))
        elif k in ('hdd2_computers', 'hdd_computers'):
            short_ = Parts_short.objects.filter(kind__in=('hdd', 'ssd'),kind2=False).values_list('name_parts',flat=True)
            CHOISE_ = [(short, short) for short in short_]
            form_ = eval(dict_form[k])
            key_ = list(form_.fields.keys())[0]
            form_.base_fields[key_].choices = CHOISE_
            list_form.append((form_, price, link_, k))
        else:
            try:
                form_ = eval(dict_form[k])
                key_ = list(form_.fields.keys())[0]
                form_.base_fields[key_].choices = CHOISE_
                list_form.append((form_, price, link_, k, dict_form[k + '_num']))
                #list_form.append((eval(dict_form[k]), price, link_, k, dict_form[k + '_num']))
            except:
                form_ = eval(dict_form[k])
                key_ = list(form_.fields.keys())[0]
                form_.base_fields[key_].choices = CHOISE_
                list_form.append((form_, price, link_, k))
                #list_form.append((eval(dict_form[k]), price, link_, k))
    temp = list_form.pop(-1)
    list_form.insert(5, temp)
    for_comp_price = comp[0]
    for_comp_price.price_computers = price_count
    for_comp_price.save()

    return (list_form, price_count)

def get_art_comp_context(object_id, queryset_comps=None ):
    queryset_comps_first = queryset_comps.first().comp if queryset_comps else None
    if queryset_comps_first:
        get_comp_context(queryset_comps_first.pk)
        queryset_comps_first = Computers.objects.get(pk=queryset_comps_first.pk)
    case_from_queryset = queryset_comps_first.case_computers if queryset_comps_first else None
    comp = Computers.objects.filter(pk=object_id)
    try:
        comp_price = comp[0].compprice
    except:
        comp_price = None

    comp_parts = comp.values(
    'proc_computers', 'mb_computers', 'mem_computers', 'video_computers', 'hdd_computers',
    'ps_computers', 'case_computers', 'cool_computers',
    'vent_computers', 'mon_computers', 'wifi_computers', 'km_computers',
    'cables_computers', 'soft_computers')[0]
    try:
        comp_parts['hdd2_computers'] = comp_parts['hdd_computers'].split(';')[1]
    except:
        comp_parts['hdd2_computers'] = 'пусто'
    comp_parts['hdd_computers'] = comp_parts['hdd_computers'].split(';')[0]
    comp_parts['case_computers'] = case_from_queryset if case_from_queryset else comp_parts['case_computers']

    #comp_num = comp.values('mem_num_computers', 'video_num_computers', 'vent_num_computers')[0]

    list_form = []
    price_count = 0
    amd_intel = to_article2_1(comp[0].proc_computers)
    for k, v in comp_parts.items():
        v = v if v else 'пусто'
        if k not in ('hdd2_computers', 'hdd_computers'):
            vv = re.findall(r'\d+', v)
            vv = vv[-1] if vv else 'пусто'
            try:
                """if k in ('mb_computers', 'proc_computers') and amd_intel == 'aproc':
                    kind_ = 'a' + k[:-10]
                    #print(kind_,vv)
                    short = Parts_short.objects.filter(kind=kind_, kind2=False,
                    name_parts__icontains=vv)
                elif k in ('mb_computers', 'proc_computers') and amd_intel == 'iproc':
                    kind_ = 'i' + k[:-10]
                    short = Parts_short.objects.filter(kind=kind_, kind2=False,
                    name_parts__icontains=vv)
                else:
                    kind_ = k[:-10]
                    short = Parts_short.objects.filter(kind=kind_, kind2=False,
                    name_parts__icontains=vv)"""
                if k in ('mb_computers', 'proc_computers') and amd_intel == 'aproc':
                    kind_ = 'a' + k[:-10]
                elif k in ('mb_computers', 'proc_computers') and amd_intel == 'iproc':
                    kind_ = 'i' + k[:-10]
                else:
                    kind_ = k[:-10]
                #kind_ = 'a' + k[:-10] if k in ('mb_computers', 'proc_computers') else k[:-10]
                short = comparison_parts(kind_, v)
                try:
                    if comp_price and comp_price.__dict__[k]:
                        price = float(comp_price.__dict__[k])
                        #print('yes',price)
                    else:
                        short = min(short,key=get_min_short)
                        price = round(float(short.x_code)) #x_code
                        if kind_ == 'video':
                            video_price = price
                        #price = round(float(short.parts_full.first().providerprice_parts)) #providerprice_parts
                except:
                    price = 0
                    #print(k,price)
                #short_pk = short.pk
                short_pk = 0
            except:
                #print(k,1)
                price, short_pk = 0, 0
            try:
                price_count += price
            except:
                price_count = 0
        else:
            try:
                kind_ = 'ssd' if v.lower().find('ssd') != -1 else 'hdd'
                """vv = re.findall(r'\d+', v)
                vv = vv[-1] if vv else 'пусто'
                short = Parts_short.objects.filter(kind=kind_,
                kind2=False, name_parts__icontains=vv)"""
                short = comparison_parts(kind_, v)
                try:
                    if comp_price and comp_price.__dict__[k]:
                        price = float(comp_price.__dict__[k])
                    else:
                        short = min(short,key=get_min_short)
                        price = round(float(short.x_code)) #x_code
                        #price = round(float(short.parts_full.first().providerprice_parts)) #providerprice_parts
                except:
                    price = 0
                #short_pk = short.pk
                short_pk = 0
            except:
                price, short_pk = 0, 0
            price_count += price
        link_ = f"{short_pk},Parts_short{comp[0].pk}" if short_pk else None
        #print(v, price, price_count)
        short_ = Parts_short.objects.filter(kind=kind_,kind2=False).values_list('name_parts',flat=True)
        CHOISE_ = [(short, short) for short in short_]
        if k in ('proc_computers', 'mb_computers'):
            form_ = eval(dict_form[k][0]) if amd_intel == 'aproc' else eval(dict_form[k][1])
            key_ = list(form_.fields.keys())[0]
            form_.base_fields[key_].choices = CHOISE_
            list_form.append((form_, price, link_, k, v))
            #print('yes',price)
            """if amd_intel == 'aproc':
                form_ = eval(dict_form[k][0])
                key_ = list(form_.fields.keys())[0]
                form_.base_fields[key_].choices = CHOISE_
                list_form.append((form_, price, link_, k, v))
                #list_form.append((eval(dict_form[k][0]), price, link_, k))
            else:
                form_ = eval(dict_form[k][0])
                key_ = list(form_.fields.keys())[0]
                form_.base_fields[key_].choices = CHOISE_
                list_form.append((form_, price, link_, k, v))
                #list_form.append((eval(dict_form[k][1]), price, link_, k))"""
        else:
            try:
                form_ = eval(dict_form[k])
                key_ = list(form_.fields.keys())[0]
                form_.base_fields[key_].choices = CHOISE_
                list_form.append((form_, price, link_, k, v))
                #list_form.append((eval(dict_form[k]), price, link_, k, dict_form[k + '_num']))
            except:
                form_ = eval(dict_form[k])
                key_ = list(form_.fields.keys())[0]
                form_.base_fields[key_].choices = CHOISE_
                list_form.append((form_, price, link_, k, v))
                #list_form.append((eval(dict_form[k]), price, link_, k))
    temp = list_form.pop(-1)
    list_form.insert(5, temp)
    try:
        art_comp_price = round(float(comp[0].price_computers))
        price_count = float(price_count - video_price)
    except:
        art_comp_price = 0
    count_video_price = count_video_price_per_our_price(art_comp_price, price_count)
    #print(f'for test {comp[0].name_computers}:',price_count)

    return (list_form, comp[0], count_video_price)

def count_our_video_price(video_code):
    try:
        split1, split2 = video_code[0].split(' ')
        short = Parts_short.objects.filter(Q(name_parts__icontains=split1) & Q(name_parts__icontains=split2),
        kind='video', kind2=False)
    except:
        split1 = video_code[0].split(' ')[0]
        if split1:
            short = Parts_short.objects.filter(kind='video', kind2=False,
            name_parts__icontains=split1)
        else:
            short = Parts_short.objects.none()
    try:
        short_ = min(short,key=get_min_short)
        price = round(float(short_.x_code)) #x_code
        #price = round(float(short_.parts_full.first().providerprice_parts)) #providerprice_parts
    except:
        price = 0
        short_ = None
    video_name = short_.name_parts if short_ else 'пусто'
    return (video_name, price)

def get_stats_art(queryset):

    queryset_comps_ = queryset.select_related('comp')
    code_dict = get_code_from_queryset(queryset)
    count_our_video = count_our_video_price(code_dict['video_computers'])
    print(code_dict)
    art = Computers.objects.filter(pc_assembly__sites__name_sites='art')\
    .filter(video_computers__in=code_dict['video_computers'])
    if code_dict['proc_computers'] != (None,):
        art = art.filter(proc_computers__in=code_dict['proc_computers'])
    if code_dict['mem_computers'] != (None,):
        art = art.filter(mem_computers__in=code_dict['mem_computers'])
    art_list = [(get_art_comp_context(comp.pk, queryset_comps=queryset_comps_), comp.name_computers) for comp in art]
    #art ~ (list_form, price_count, count_video_price)

    return (art_list, count_our_video, queryset_comps_)
