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

CPU_PATTERN = re.compile(
    r'\b(RYZEN|INTEL|CORE|ULTRA|I[3579]|CELERON|PENTIUM|ATHLON)\b',
    re.I
)
GPU_PATTERN = re.compile(r'\b(RTX|GTX|RX)\b', re.I)
RAM_PATTERN = re.compile(r'^\d+\s*(GB)?$', re.I)

def parse_nb_parts(parts):
    """ для парсинга из строки наз ноута """

    result = {
        'nb_sc_d': '',
        'nb_cpu_model': '',
        'nb_ram_v': '',
        'nb_ssd': '',
        'nb_gpu_model': 'Integrated Graphics',
        'os': ''
    }

    for part in parts:
        p = part.strip()

        if not p:
            continue

        # экран
        if '"' in p:
            result['nb_sc_d'] = p
            continue

        # игнорируем герцовку
        if 'HZ' in p.upper():
            continue

        # SSD
        if 'SSD' in p.upper():
            result['nb_ssd'] = p
            continue

        # GPU
        if GPU_PATTERN.search(p):
            result['nb_gpu'] = p
            continue

        # CPU
        if CPU_PATTERN.search(p):
            result['nb_cpu_model'] = p
            continue

        # RAM
        if RAM_PATTERN.match(p):
            result['nb_ram_v'] = f'{p}Gb'
            continue

        # всё остальное — считаем ОС
        result['os'] = p

    return result

def normalize_storage(value):
    """ для Gb в названии """
    if not value:
        return ''

    value = str(value).upper()

    # ищем число (например 512, 1024 и т.д.)
    match = re.search(r'(\d+)', value)
    if not match:
        return ''

    size = int(match.group(1))

    # если вдруг будет TB
    if 'TB' in value:
        size *= 1024

    return f'{size} ГБ'

def get_clean_name(name_nb):
    """ для name_to_parts вспомагательная """
    # убираем "Ноутбук " в начале (если есть)
    name_nb = re.sub(r'^Ноутбук\s+', '', name_nb)

    # удаляем все (...) вместе с содержимым
    new_name = re.sub(r'\([^)]*\)', '', name_nb)

    # убираем лишние пробелы
    return ' '.join(new_name.split())

def get_vendor_series(name_nb):
    """ полчаем вендор и серию из названия ноутов
    (первым в строке идет вендор потом серия) """
    if not name_nb:
        return '', ''

    #clean = get_clean_name(name_nb)
    parts = name_nb.split()

    if not parts:
        return '', ''

    vendor = parts[0]
    seria = parts[1] if len(parts) > 1 else ''

    return vendor, seria

def name_to_parts(name_nb):
    """
    из имени ноута получаем параметры + тру/фалсе и размер списка параметров
    пример name_nb: 'Ноутбук Acer Aspire (15.6"/Ryzen 7 5825U/16/SSD512/DOS)'
    """
    if not name_nb:
        return False, 0, [], '-'

    match = re.search(r'\(([^)]+)\)\s*$', name_nb)
    if not match:
        return False, 0, [], name_nb

    parts = match.group(1).split('/')
    dict_parts = parse_nb_parts(parts)

    return True, len(parts), dict_parts, get_clean_name(name_nb)
