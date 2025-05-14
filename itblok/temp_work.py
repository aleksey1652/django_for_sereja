import re
import json
from lxml import etree

from django.db.models import Sum, Count, F, Q
from django.db import transaction
from django.utils import timezone

from cat.models import Parts_short as short
from .models import *


def get_cpu(str_):
    #
    if short.objects.filter(
    kind__in=('aproc', 'iproc'), name_parts__icontains=str_).exists():
        min = short.objects.filter(
        kind__in=('aproc', 'iproc'), name_parts__icontains=str_
        ).order_by('x_code').first()
        return min
    #
    return None
    # short.objects.filter(
    #kind__in=('aproc', 'iproc'), kind2=False).order_by('x_code').first()

def get_cooler(str_):
    #
    if short.objects.filter(
    kind='cool', name_parts__icontains=str_).exists():
        min = short.objects.filter(
        kind='cool', name_parts__icontains=str_
        ).order_by('x_code').first()
        return min
    #
    #return short.objects.filter(kind='cool', name_parts='пусто').first()
    return None

def get_mb(str_):
    #
    str_edit = re.sub(r's\d+|am\d', '', str_.lower()).strip()
    if str_edit.find('ddr4') != -1:
        if short.objects.filter(
        Q(kind__in=('amb', 'imb'), name_parts__icontains=str_edit[:-5],
        kind2=False) &
        Q(name_parts__icontains='ddr4')).exists():
            min = short.objects.filter(
            Q(kind__in=('amb', 'imb'), name_parts__icontains=str_edit[:-5],
            kind2=False) &
            Q(name_parts__icontains='ddr4')).order_by('x_code').first()
            return min
    if str_edit.find('ddr5') != -1:
        if short.objects.filter(
        Q(kind__in=('amb', 'imb'), name_parts__icontains=str_edit[:-5],
        kind2=False) &
        Q(name_parts__icontains='ddr5')).exists():
            min = short.objects.filter(
            Q(kind__in=('amb', 'imb'), name_parts__icontains=str_edit[:-5],
            kind2=False) &
            Q(name_parts__icontains='ddr5')).order_by('x_code').first()
            return min
    if short.objects.filter(kind2=False,
    kind__in=('amb', 'imb'), name_parts__icontains=str_edit).exists():
        min = short.objects.filter(kind2=False,
        kind__in=('amb', 'imb'), name_parts__icontains=str_edit
        ).order_by('x_code').first()
        return min
    #return short.objects.filter(
    #kind__in=('amb', 'imb'), name_parts='пусто').first()
    return None

def get_ram(str_):
    #
    gb = re.findall(r'\d+gb', str_.lower())
    gb = gb[0] if gb else '4gb'
    type_ = re.findall(r'ddr\d', str_.lower())
    type_ = type_[0] if type_ else 'ddr4'
    mhz = re.findall(r'\d+mhz', str_.lower())
    mhz = mhz[0] if mhz else '3200mhz'
    dop = re.findall(r'\(2x\d+\)', str_.lower())
    dop = dop[0] if dop else None
    #
    query = short.objects.filter(kind='mem', kind2=False).filter(
    Q(name_parts__icontains=gb) &
    Q(name_parts__icontains=type_) &
    Q(name_parts__icontains=mhz)
    )
    #
    if query.exists():
        if not dop:
            return query.order_by('x_code').first()
        if query.filter(name_parts__icontains=dop).exists():
            return query.filter(name_parts__icontains=dop).order_by('x_code').first()
    #return short.objects.filter(kind='mem', kind2=False).order_by('x_code').first()
    return None

def get_gpu(str_):
    #
    query_edit, query = None, None
    str_edit = re.sub(
    r'geforce|rtx|gtx|radeon|rx|amd|super|ti|xtx|xt|\d+gb',
    '', str_.lower()).strip()
    if short.objects.filter(kind2=False,
    kind='video', name_parts__icontains=str_edit).exists():
        query = short.objects.filter(kind2=False,
        kind='video', name_parts__icontains=str_edit)
    if str_.lower().find('ti') != -1:
        if query.filter(name_parts__icontains='ti').exists():
            query_edit = query.filter(
            name_parts__icontains='ti')#.order_by('x_code').first()
            if str_.lower().find('super') != -1:
                if query_edit.filter(name_parts__icontains='super').exists():
                    query_edit = query_edit.filter(
                    name_parts__icontains='super')#.order_by('x_code').first()
    elif str_.lower().find('super') != -1:
        if query.filter(name_parts__icontains='super').exists():
            query_edit = query.filter(
            name_parts__icontains='super')#.order_by('x_code').first()
    elif str_.lower().find('xtx') != -1:
        if query.filter(name_parts__icontains='xtx').exists():
            query_edit = query.filter(
            name_parts__icontains='xtx')#.order_by('x_code').first()
    elif str_.lower().find('xt') != -1:
        if query.filter(name_parts__icontains='xt').exists():
            query_edit = query.filter(
            name_parts__icontains='xt')#.order_by('x_code').first()
    gb_list = re.findall(r'\d+gb', str_.lower())
    if query_edit and gb_list:
        if query_edit.filter(name_parts__icontains=gb_list[0]).exists():
            query_edit =  query_edit.filter(
            name_parts__icontains=gb_list[0])#.order_by('x_code').first()
    if query and not query_edit:
        if gb_list:
            if query.filter(name_parts__icontains=gb_list[0]).exists():
                query =  query.filter(
                name_parts__icontains=gb_list[0])#.order_by('x_code').first()
        return query.order_by('x_code').first()
    if query_edit:
        return query_edit.order_by('x_code').first()
    #return short.objects.filter(kind='video', name_parts='пусто').first()
    return None


def get_hdd(str_):
    #
    return short.objects.filter(kind='hdd', name_parts='пусто').first()

def get_ssd(str_):
    #
    type_ = None
    #
    gb = re.findall(r'\d+gb|\d+tb', str_.lower())
    gb = gb[0] if gb else '120gb'
    if str_.lower().find('m.2') != -1:
        type_ = 'm.2'
    query = short.objects.filter(kind='ssd', kind2=False).filter(
    name_parts__icontains=gb)
    if query.exists():
        if not type_:
            return query.order_by('x_code').first()
        if query.filter(name_parts__icontains=type_).exists():
            return query.filter(name_parts__icontains=type_).order_by('x_code').first()
    #return short.objects.filter(kind='ssd', name_parts='пусто').first()
    return None

def get_psu(str_):
    #
    power = re.findall(r'\d+w', str_.lower())
    power = power[0] if power else '300w'
    #
    if short.objects.filter(
    kind='ps', name_parts__icontains=power).exists():
        min = short.objects.filter(
        kind='ps', name_parts__icontains=power
        ).order_by('x_code').first()
        return min
    #
    #return short.objects.filter(kind='ps', name_parts='пусто').first()
    return None

def get_case(str_):
    #
    if short.objects.filter(
    kind='case', name_parts__icontains=str_).exists():
        min = short.objects.filter(
        kind='case', name_parts__icontains=str_
        ).order_by('x_code').first()
        return min
    #
    #return short.objects.filter(kind='case', kind2=False).order_by('x_code').first()
    return None


def get_fan(str_):
    #
    if short.objects.filter(
    kind='vent', name_parts__icontains=str_).exists():
        min = short.objects.filter(
        kind='vent', name_parts__icontains=str_
        ).order_by('x_code').first()
        return min
    #
    #return short.objects.filter(kind='vent', name_parts='пусто').first()
    return None

def get_series(str_):
    #
    series,_ = Series.objects.get_or_create(series_name=str_)
    #
    return series


def get_grups(str_):
    #
    grups,_ = Grups.objects.get_or_create(group_name=str_)
    #
    return grups



def it_comp_create(dict_):
    #

    try:
        it = ItblokComputers(
        name_computers=dict_['name_computers'],
        name_computers_ua=dict_['name_computers'],
        cpu=get_cpu(dict_['cpu']),
        cooler=get_cooler(dict_['cooler']),
        mb=get_mb(dict_['mb']),
        ram=get_ram(dict_['ram']),
        gpu=get_gpu(dict_['gpu']),
        hdd=get_hdd(dict_['hdd']),
        ssd=get_ssd(dict_['ssd']),
        psu=get_psu(dict_['psu']),
        case=get_case(dict_['case']),
        fan=get_fan(dict_['fan']),
        vent_num_computers = dict_['vent_num_computers'],
        series = get_series(dict_['series']),
        grups = get_grups(dict_['grups'])
        )
    except:
        return None


    return it


def all_comps_create(dict_full):
    #

    new_parts = [
        it_comp_create(dict_full[article])
        for article in dict_full.keys()
    ]

    new_parts_ok = [new for new in new_parts if new] # на случай, если bdCreate None

    try:
        with transaction.atomic():
            new_in_bd = ItblokComputers.objects.bulk_create(new_parts_ok)
    except:
        new_in_bd = []

    res = f'all_comps: {len(dict_full)}, try: {len(new_parts_ok)}, ok: {len(new_in_bd)}'

    return res


dict_xlsx = {
'Название': None,
'Процессор Intel': 'cpu',
'Процессор AMD': 'cpu',
'Мать Intel': 'mb',
'Мать AMD': 'mb',
'cpu cooler': 'cooler',
'ОЗУ': 'ram',
'Видеокарта': 'gpu',
'HDD': 'hdd',
'SSD': 'ssd',
'ОЗУ': 'ram',
'Корпус': 'case',
'Блок питания': 'psu',
'Вентилятор': 'fan',
}

def ukr_fun(str_):
    if str_.find('Оптимальный Игровой') != -1:
        return 'Оптимальний Iгровий ' + str_[20:]
    if str_.find('Прогрессивный Игровой') != -1:
        return 'Прогресивний Iгровий ' + str_[22:]
    if str_.find('Максимальный Игровой') != -1:
        return 'Максимальний Iгровий ' + str_[21:]
    if str_.find('Мультимедийный') != -1:
        return 'Мультимедiйний ' + str_[15:]
    if str_.find('Прогрессивный Бизнес') != -1:
        return 'Прогресивний Бiзнес ' + str_[21:]
    return str_

def all_tu_ukr(dict_):
    for val in dict_.values():
        val['name_computers_ua'] = ukr_fun(val['name_computers_ua'])
    return dict_
