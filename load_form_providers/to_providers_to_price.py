import requests, re, json
import pandas as pd
from lxml import etree
import heapq
import os

def single_clear(set_be):
    # выключает обьекты single(кулеры и вентиляторы) если
    # их нет в set_be   is_active

    from singleparts.models import FAN_OTHER, Cooler_OTHER

    pp = FAN_OTHER.objects.exclude(part_number__in=set_be).filter(
    provider='pccooler')
    pp.update(is_active=False, provider='нет', price_ua=0, price_usd=0, rrp_price=0)

    pp = Cooler_OTHER.objects.exclude(part_number__in=set_be).filter(
    provider='pccooler')
    pp.update(is_active=False, provider='нет', price_ua=0, price_usd=0, rrp_price=0)

def pccooler_to_single(partnum, kind, usd_ex):
    # по партнамберу обновим вентилятор или кулер в singleparts

    from singleparts.models import FAN_OTHER, Cooler_OTHER
    from load_form_providers.dc_descr_catalog import objects_edit

    if kind == 'vent':
        if FAN_OTHER.objects.filter(part_number=partnum).exists():
            fan = FAN_OTHER.objects.filter(part_number=partnum).first()
            objects_edit(fan, usd_ex)

    if kind == 'cool':
        if Cooler_OTHER.objects.filter(part_number=partnum).exists():
            cool = Cooler_OTHER.objects.filter(part_number=partnum).first()
            objects_edit(cool, usd_ex)

def to_article2_1(d,pr=1):
    """ убрать в load_element, erc2 и оставить только здесь """

    if pr==1:
        if d.lower().find('core') !=-1:
            return 'iproc'
        elif d.lower().find('pentium') !=-1:
            return 'iproc'
        elif d.lower().find('celeron') !=-1:
            return 'iproc'
        elif d.lower().find('xeon') !=-1:
            return 'iproc'
        elif d.lower().find('intel') !=-1:
            return 'iproc'
        else:
            return 'aproc'
    else:
        if re.findall(r'fm3|fm2|am3|am4|9830|320|450|x470|x570|a68|x399|trx40|550|520|amd|x670|650|850|870',d.lower()):
            return 'amb'
        if re.findall(r'4005|1800|1900|61|41|81|110|310|365|360|z390|x299|410|z490|b460|z590|z690|370|470|510|b560|1200|h570|h610|b660|670|710|760|790|b750|810|860|890|intel',
                    d.lower()):
            return 'imb'
        else:
            return 'amb'


def str_to_float(str_):
    """ строку, флоат в флоат; из '839,00' в 839.0 например """
    try:
        return float(str_)
    except:
        try:
            return float(re.sub(',', '.', str_))
        except:
            return 0


def get_text(element, default=''):
    """Возвращает текст или
    текст тега или значение по умолчанию, если тег пустой или отсутствует"""
    if isinstance(element, str):
        return element[:49].strip()
    try:
        return element.text[:49].strip()
    except:
        return default

def get_float(element):
    """Безопасно преобразует в float, иначе возвращает 0"""
    if isinstance(element, (float, int)):
        return round(element, 1)
    text = get_text(element)
    try:
        return round(float(text), 1) if text is not None else 0
    except ValueError:
        return 0  # Ошибки преобразования

def get_int(element):
    """Безопасно преобразует в int, иначе возвращает 0"""
    text = get_text(element)
    try:
        return int(text) if text is not None else 0
    except ValueError:
        return 0  # Ошибки преобразования

def price_usd(price, usd, usd_data='usd'):
    """для пересчета в $ для elko но можно и для других
    пока не используем usd т.к.'currency': 'usd' в товарах,
    поэтому(usd_data='usd')"""
    if get_text(usd_data).lower() != 'usd':
        try:
            return round(get_float(price) / float(usd), 1)
        except:
            return 0
    return get_float(price)


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
