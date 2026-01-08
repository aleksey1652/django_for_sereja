import requests, re, json
import pandas as pd
from lxml import etree
import heapq
import os

from cat.models import Providers, Parts_full, Results

from django.db import transaction
from django.utils import timezone

from django.db.models import F, FloatField, IntegerField, CharField, Value
from django.db.models.functions import Substr, Cast, StrIndex


def find_min_bd(data, article):
    """ищем мин цену от files_providers, если есть - добавляем к data,
       возвращаем data неизменной или обновленной от files_providers
    """

    files_providers = ('erc', 'be', 'dw', 'pccooler')

    files = Parts_full.objects.filter(
    partnumber_parts=article, providers__name_provider__in=files_providers,
    availability_parts='yes', providerprice_parts__gt=0)

    if files.exists():
        min_prov = files.annotate(
        provider=F('providers__name_provider'),
        RRP_UAH=F('rrprice_parts')
        ).values(
        'provider', 'providerprice_parts',
        'RRP_UAH', 'availability_parts',
        'name_parts', 'partnumber_parts', 'kind'
        ).order_by('providerprice_parts').first()

        dict_ = dict(min_prov)
        if dict_:
            data[dict_['provider']] = {dict_['partnumber_parts']: dict_}

    return data

def find_min_price(data, article):
    """ищем мин цену из сумарного словаря поставщиков + от файловых постачей find_min_bd,
       возвращаем кортеж, например: ('dc', {словарь с инфой, в том числе и мин ценой})
    """

    data = find_min_bd(data, article) # добавляем в data файловых постачей, если они есть

    heap = [
        (source[article]['providerprice_parts'], key, source[article])
        for key, source in data.items() if article in source and\
        source[article]['availability_parts'] == 'yes'
    ]
    if heap:
        # Возвращаем источник и словарь с минимальной ценой
        _, min_key, min_data = heapq.nsmallest(1, heap, key=lambda x: x[0])[0]
        return min_key, min_data
    # Если артикул есть, но нет доступных товаров, сразу возвращаем дефолтное значение
    return next(
        ((key, {'providerprice_parts': 0, 'availability_parts': 'no'}
        ) for key, source in data.items() if article in source),
        None
    )
    return None


def bdRemainder():
    """
    Склад

    обновляем в Parts_full цену по складу, включаем если надо,
    в 1-го поставщика 'склад' если надо

    count_empty - только склад,
    count_no_empty - цена на складе дешевле чем от постачей
    возвращаем count_no_empty, count_empty
    """

    now = timezone.now()

    remainder_ = Parts_full.objects.filter(remainder__isnull=False)

    no_empty = remainder_.filter(availability_parts='yes').annotate(
    # обновленная цена но на складе дещевле
    start_pos=Cast(StrIndex(F('remainder'), Value(':')), IntegerField()) + Value(1),
    end_pos=Cast(StrIndex(F('remainder'), Value(';')), IntegerField()),
    substr_length=Cast(F('end_pos') - F('start_pos'), IntegerField()),
    price_str=Substr(F('remainder'), F('start_pos'), F('substr_length'),
    output_field=CharField()),
    price_remainder=Cast(F('price_str'), FloatField())
    ).filter(price_remainder__lt=F('providerprice_parts'))

    count_no_empty = no_empty.update(
    providerprice_parts=F('price_remainder'), name_parts_main='склад',
    date_chg=now) # склад цену в providerprice_parts

    empty = remainder_.filter(availability_parts='no').annotate( # есть только на складе
    start_pos=Cast(StrIndex(F('remainder'), Value(':')), IntegerField()) + Value(1),
    end_pos=Cast(StrIndex(F('remainder'), Value(';')), IntegerField()),
    substr_length=Cast(F('end_pos') - F('start_pos'), IntegerField()),
    price_str=Substr(F('remainder'), F('start_pos'), F('substr_length'),
    output_field=CharField()),
    price_remainder=Cast(F('price_str'), FloatField())
    )

    count_empty = empty.update(
    providerprice_parts=F('price_remainder'),
    availability_parts='yes',
    name_parts_main='склад',
    date_chg=now) # склад цену в providerprice_parts и включаем 'yes'

    return (count_no_empty, count_empty) # кол склад_с_постач, кол склад_только


def bdUpdate(dict_, part):
    """
    для конкретного prov_ обновляем Parts_full
    используя dict_ скач/обраб от prov_
    возвращаем обновленный part
    """

    now = timezone.now()

    try:
        price = dict_[part.partnumber_parts]['providerprice_parts']
        rrp = dict_[part.partnumber_parts]['RRP_UAH']
        avail = 'yes'
    except:
        price, rrp, avail = 0, 0, 'no'

    part.providerprice_parts = price
    part.rrprice_parts = rrp
    part.availability_parts = avail
    part.date_chg = now

    return part

def bdCreate(dict_, prov_):
    """
    для конкретного prov_ создаем Parts_full
    используя dict_ скач/обраб от prov_
    возвращаем full или None(при неудаче)
    """

    prov = Providers.objects.get(name_provider=prov_)

    now = timezone.now()

    try:
        full = Parts_full(
        name_parts=dict_['name_parts'],
        partnumber_parts=dict_['partnumber_parts'],
        availability_parts='yes',
        providerprice_parts=dict_['providerprice_parts'],
        rrprice_parts=dict_['RRP_UAH'],
        kind=dict_['kind'],
        date_chg=now,
        providers=prov
        )
    except:
        return None


    return full


def bdCreateFile(dict_res, article, prov):
    """
    для '-' создаем Parts_full
    используя dict_res
    prov для 1поставщика name_parts_main
    """

    now = timezone.now()
    prov_ = Providers.objects.get(name_provider='-')

    try:
        dict_ = dict_res[article]
        full = Parts_full(
        name_parts=dict_['name_parts'],
        partnumber_parts=dict_['partnumber_parts'],
        availability_parts='yes',
        providerprice_parts=dict_['providerprice_parts'],
        rrprice_parts=dict_['RRP_UAH'],
        kind=dict_['kind'],
        date_chg=now,
        providers=prov_,
        name_parts_main=prov,
        )
    except:
        return None

    return full

def bdUpdateFile(part):
    """
    !!! дораб это
    для конкретного prov_ обновляем Parts_full
    используя dict_ скач/обраб от prov_
    """

    now = timezone.now()
    avail = 'yes'
    article = part.partnumber_parts

    try:
        full_min = Parts_full.objects.filter(partnumber_parts=article,
        providerprice_parts__gt=0, availability_parts='yes'
        ).exclude(
        providers__name_provider='-'
        ).order_by('providerprice_parts').first()

        price = full_min.providerprice_parts
        rrp = full_min.rrprice_parts
        prov = full_min.providers.name_provider
    except:
        if not part.remainder:
            avail = 'no'
            price = 0
            rrp = 0
            prov = None
        else:
            return part

    part.providerprice_parts = price
    part.rrprice_parts = rrp
    part.availability_parts = avail
    part.date_chg = now
    part.name_parts_main = prov

    return part

def bdOldUpdateFile(part, prov):
    """
    !!! дораб это
    для конкретного prov_ обновляем Parts_full
    используя dict_ скач/обраб от prov_
    """

    now = timezone.now()

    return part


def bdUpdateMain(dict_full, part):
    """
    для "-" Parts_full обновляем
    используя dict_full скач/обраб от prov_
    используем find_min_price: находим постача с мин ценой
    возвращаем обновленный part
    """

    now = timezone.now()
    avail = 'yes'

    try:
        prov_min, dict_parts = find_min_price(dict_full, part.partnumber_parts)
        price = dict_parts['providerprice_parts']
        rrp = dict_parts['RRP_UAH']
    except:
        avail = 'no'
        price = 0
        prov_min = None
        rrp = 0

    part.providerprice_parts = price
    part.rrprice_parts = rrp
    part.availability_parts = avail
    part.date_chg = now
    part.name_parts_main = prov_min


    return part

def bdCreateMain(dict_full, article):
    """
    для "-" Parts_full создаем новый full
    используя dict_full скач/обраб от prov_
    используем find_min_price: находим постача с мин ценой
    возвращаем full или None(при неудаче)
    """

    now = timezone.now()
    avail = 'yes'
    prov = Providers.objects.get(name_provider='-')

    try:
        prov_min, dict_parts = find_min_price(dict_full, article)
        price = dict_parts['providerprice_parts']
    except:
        return None

    try:
        full = Parts_full(
        name_parts=dict_parts['name_parts'],
        partnumber_parts=dict_parts['partnumber_parts'],
        availability_parts='yes',
        providerprice_parts=dict_parts['providerprice_parts'],
        rrprice_parts=dict_parts['RRP_UAH'],
        kind=dict_parts['kind'],
        date_chg=now,
        providers=prov,
        name_parts_main=prov_min)
    except:
        return None

    return full


def updateResults(dict_message, duration, short_all, short_in, sklsdWith, sklsdOnly):
    """ запись результатов прайс-агрегатора(dict_message),
        время затраченное(duration),
        комп детали(short_all), к детали в компах(short_in),
        деш_склад_прайс(sklsdWith), только_склад(sklsdOnly)
        в Results
    """

    time_message = f';\n time: {duration}min'

    sklsd = f';\n склад_прайс/только_склад: {sklsdWith}/{sklsdOnly}'

    list_message = [f"{value['name_prov']}: new = {value['new']}, update =\
    {value['update']}, error = {value['diff_error']}/{value['empty_error']}\
    " for value in dict_message.values()]

    prov_message = ';\n'.join(list_message) + sklsd +  time_message

    short_ = f'обновлены комп_детали/комп_дет_для_сборок: {short_all}/{short_in}'

    if not Results.objects.filter(who='prov').exists():
        r = Results(who='prov',
        who_desc=prov_message)
        r.save()
    else:
        r = Results.objects.get(who='prov')
        r.who_desc = prov_message
        r.save()

    if not Results.objects.filter(who='comp_parts').exists():
        r = Results(who='comp_parts',
        who_desc=short_)
        r.save()
    else:
        r = Results.objects.get(who='comp_parts')
        r.who_desc = short_
        r.save()

    return True


def currentFileToBd(dict_res, prov):
    """
    создание/апдейт для "-" name_parts_main prov из руч-скач файла prov
    """

    mes_prov = {
    'name_prov': 'main',
    'new': 0,
    'update': 0,
    'diff_error': 0,
    'empty_error': 0
    }

    set_prov = set(dict_res)

    old_main = Parts_full.objects.filter(providers__name_provider='-',
    name_parts_main=prov).exclude(partnumber_parts__in=set_prov)
    # "-" где 1-й поставщик: prov, но его нет в set_prov, сделаем апдейт цены
    # для "-" если есть от других постачей или делаем неактивным

    for_update = Parts_full.objects.filter(providers__name_provider='-',
    partnumber_parts__in=set_prov) #  все "-" от свежего set_prov

    old_parts = list(old_main)
    old_updated_parts = [
        bdUpdateFile(part)
        for part in old_parts
    ]

    try:
        with transaction.atomic():
            old_main.bulk_update(
            old_updated_parts, [
            'providerprice_parts', 'rrprice_parts', 'availability_parts', 'date_chg',
            'name_parts_main']
            )
    except:
        old_updated_parts = []

    parts = list(for_update)
    updated_parts = [
        bdUpdateFile(part)
        for part in parts
    ]

    try:
        with transaction.atomic():
            for_update.bulk_update(
            updated_parts, [
            'providerprice_parts', 'rrprice_parts', 'availability_parts', 'date_chg',
            'name_parts_main']
            )
    except:
        updated_parts = []

    new_parts = [
        bdCreateFile(dict_res, article, prov)
        for article in set_prov if not \
        Parts_full.objects.filter(providers__name_provider='-',
        partnumber_parts=article).exists()
    ] # создаем новые "-" от свежего set_prov

    new_parts_ok = [new for new in new_parts if new] # на случай, если bdCreateFile None

    try:
        with transaction.atomic():
            new_in_bd = Parts_full.objects.bulk_create(new_parts_ok)
    except:
        new_in_bd = []

    diff = len(new_parts) - len(new_parts_ok)
    mes_prov['new'] = len(new_in_bd)
    mes_prov['update'] = f'свежий прайс: {len(updated_parts)};без: {len(old_updated_parts)}'
    mes_prov['diff_error'] = diff

    return mes_prov


def mainProvToBd(dict_):
    """из dict_full
       используя bdUpdateMain и bdCreateMain с dict_ обновляем или создаем прайс для '-'
       возвращаем инфу (message) по '-' message (позже доделать)
    """

    message = {
    'name_prov': 'main',
    'new': 0,
    'update': 0,
    'diff_error': 0,
    'empty_error': 0
    }

    count = 0 # подсчет пустых словарей от постачей
    error_empty = [count + 1 for key, value in dict_.items() if not value]
    message['empty_error'] = sum(error_empty)

    set_article = set(dict_['dc'].keys()) | set(dict_['asbis'].keys())\
    | set(dict_['elko'].keys()) | set(dict_['brain'].keys())\
    | set(dict_['mti'].keys()) | set(dict_['edg'].keys())

    temp = Parts_full.objects.filter(providers__name_provider='-',
    partnumber_parts__in=set_article)

    parts = list(temp)

    updated_parts = [
        bdUpdateMain(dict_, part)
        for part in parts
    ]

    try:
        with transaction.atomic():
            temp.bulk_update(
            updated_parts, ['providerprice_parts', 'availability_parts',
            'rrprice_parts', 'date_chg', 'name_parts_main']
            )
    except:
        updated_parts = []

    new_parts = [
        bdCreateMain(dict_, article)
        for article in set_article if not \
        Parts_full.objects.filter(providers__name_provider='-',
        partnumber_parts=article).exists()
    ]

    new_parts_ok = [new for new in new_parts if new] # на случай, если bdCreateMain None

    try:
        with transaction.atomic():
            new_in_bd = Parts_full.objects.bulk_create(new_parts_ok)
    except:
        new_in_bd = []

    diff = len(new_parts) - len(new_parts_ok)
    message['new'] = len(new_in_bd)
    message['update'] = len(updated_parts)
    message['diff_error'] = diff

    message_str = f'main, updated: {len(updated_parts)}, new: {len(new_in_bd)}'
    if diff != 0:
        message_str += f' ,create_error: {diff}'
    print(message_str)

    return message


def currentProvToBd(dict_, name_prov):
    """из dict_full получаем dict_ = dict_full[name_prov]
       используя bdUpdate и bdCreate с dict_ обновляем или создаем прайс для
       текущего провайдера с именем name_prov
       возвращаем инфу (message) по поставщику message (позже доделать)
    """

    message = {
    'name_prov': name_prov,
    'new': 0,
    'update': 0,
    'diff_error': 0,
    'empty_error': 0
    }

    if not dict_:
        message['empty_error'] = 1
        return message

    set_article = set(dict_.keys())

    temp = Parts_full.objects.filter(providers__name_provider=name_prov,
    partnumber_parts__in=set_article)

    parts = list(temp)

    set_bd = set(
    temp.values_list('partnumber_parts', flat=True)
    ) #set партнм которые в бд
    set_no_bd = set_article - set_bd # set партн-в кот-x нет в бд

    dict_no_bd = {key: value for key, value in dict_.items() if key in set_no_bd}
    # dict_no_bd словарь для записи новых Parts_full в бд


    updated_parts = [
        bdUpdate(dict_, part)
        for part in parts
    ]

    try:
        with transaction.atomic():
            temp.bulk_update(
            updated_parts, [
            'providerprice_parts', 'rrprice_parts', 'availability_parts', 'date_chg']
            )
    except:
        updated_parts = []


    new_parts = [
        bdCreate(dict_no_bd[article], name_prov)
        for article in dict_no_bd.keys()
    ]

    new_parts_ok = [new for new in new_parts if new] # на случай, если bdCreate None

    try:
        with transaction.atomic():
            new_in_bd = Parts_full.objects.bulk_create(new_parts_ok)
    except:
        new_in_bd = []

    diff = len(new_parts) - len(new_parts_ok)
    message['new'] = len(new_in_bd)
    message['update'] = len(updated_parts)
    message['diff_error'] = diff

    message_str = f'{name_prov}, updated: {len(updated_parts)}, new: {len(new_in_bd)}'
    if diff != 0:
        message_str += f' ,create_error: {diff}'
    print(message_str)

    return message
