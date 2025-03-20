import requests, re, json
from lxml import etree
import heapq

from cat.models import Providers, Parts_full, Results

from django.db import transaction
from django.utils import timezone

from django.db.models import F, FloatField, IntegerField, CharField, Value
from django.db.models.functions import Substr, Cast, StrIndex


def bdRemainder():
    # прверить алгоритм!!!

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
    providerprice_parts=F('price_remainder'),
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
    date_chg=now) # склад цену в providerprice_parts и включаем 'yes'

    return (count_no_empty, count_empty) # кол склад_с_постач, кол склад_только


def bdUpdate(dict_, part):
    #
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
    #

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


def bdUpdateMain(dict_full, part):
    #
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

    part.providerprice_parts = price
    part.rrprice_parts = rrp
    part.availability_parts = avail
    part.date_chg = now
    part.name_parts_main = prov_min


    return part

def bdCreateMain(dict_full, article):
    #
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


def find_min_price(data, article):
    """ищем мин цену из сумарного словаря поставщиков
       возвращаем кортеж, например: ('dc', {словарь с инфой, в том числе и мин ценой})
    """

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


# ниже словарь групп-категорий поставщиков для обработки
# в каждом обработчике (например dc_kind) есть соответсвия c унифицированным 'kind'
OnlyGroups = {
'dc': (
'8', '3', '724', '255', '1', '9', '27', '2', '23', '6', '5'
),
'asbis': (
'Monitor LCD', 'Cooling System', 'Monitor LED','CPU Desktop',
'HDD Video Surveillance', 'SSD Client', 'Memory Desktop',
'Video Card', 'HDD NAS', 'HDD Desktop'
),
'elko': (
'COC','CAS','LC3','MEM','WRA', 'MBA', 'HDS', 'VGP',
'PSU', 'SSM', 'MBI', 'SSU', 'CPU', 'COS',
),
'mti': (
'199', '143' '119','111', '115', '118',
'112', '1668', '116', '114', '121', '122'
),
'brain': (
'Корпуса', 'Модули памяти', 'Материнские платы',
'Корпуса  имп.', 'Накопители SSD',
'Накопители HDD - 3.5", 2.5", внутренние',
'Видеокарты', 'Процессоры', 'Системы охлаждения',
'Сетевое оборудование активное', 'Мониторы'
),
'edg':
(
'Блоки живлення ATX','Корпуси', 'Системи охолодження, Cooler',
),
}

def GroupToKind(provider):
    """ из OnlyGroups (словарь групп-категорий поставщиков)
    возвращем кортеж нужных групп или False """

    try:
        return OnlyGroups[provider]
    except KeyError:
        return False


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


def dc_avail(data):
    """dc data - статус наличия, на выходе - унифицированный статус
    согласно словаря иначе 'no'  """

    avail_dict = {
    '*******':'yes',
    '******':'yes',
    '*****':'yes',
    '****':'yes',
    '***':'yes',
    '**':'yes',
    '*':'yes',
    'z':'q',
    'w':'q',
    }
    try:
        return avail_dict[data]
    except:
        return 'no'


def asbis_avail(data):
    """asbis data - статус наличия, на выходе - унифицированный статус
    согласно словаря иначе 'no' """

    avail_dict = {
    'достаточно': 'yes',
    'мало': 'yes',
    'звоните': 'q',
    }

    try:
        return avail_dict[data]
    except:
        return 'no'


def elko_avail(data):
    """elko data - статус наличия, на выходе - унифицированный статус
    согласно словаря иначе 'no'  """

    try:
        if int(data) > 0:
            return 'yes'
    except ValueError:
        if data.find('>') != -1:
            return 'yes'

    return 'no'

def mti_avail(data):
    """mti data - статус наличия, на выходе - унифицированный статус
    согласно словаря иначе 'no'  """

    try:
        if int(data) > 0:
            return 'yes'
    except ValueError:
        if data.find('более') != -1:
            return 'yes'

    return 'no'


def brain_avail(data):
    """brain data - статус наличия, на выходе - унифицированный статус
    согласно словаря иначе 'no'  """

    try:
        if int(data) > 0:
            return 'yes'
    except:
        return 'no'
    return 'no'


def edg_avail(data):
    """edg data - статус наличия, на выходе - унифицированный статус
    согласно словаря иначе 'no' """

    avail_dict = {
    'В наявності':'yes',
    'Закінчується':'yes',
    'Зарезервовано':'q',
    'Немає в наявності':'no',
    }
    try:
        return avail_dict[data]
    except:
        return 'no'


class From_provders_to_dict:
    """ собираем в dict инфу от провайдеров, структура: ... """

    def __init__(self, currency, content):
        # загружаеи курс USD и скачанный контент
        try:
            self.currency = float(currency)
        except:
            print("USD должно быть int, float")
            self.currency = 1
        self.content = content
        self._detect_content_type()

    def _detect_content_type(self):
        # выводим тип скачанных данных (временная ф)
        # потом водим сразу через etree или json и функцию тест ок в переменную
        if isinstance(self.content, (bytes, str)):
            try:
                json.loads(self.content)
                print("Тип данных: JSON")
            except:
                try:
                    etree.fromstring(self.content)
                    print("Тип данных: XML")
                except:
                    print("Тип данных: Неизвестный")
        else:
            print("Тип данных: Не байт и не строка")


    @staticmethod
    def _loadFromFile(filename):
        # альтернативная загрузка xml данных от поставщика

        with open(filename, 'rb') as fobj:
            xml = fobj.read()

        return xml

    @staticmethod
    def _loadFromFileJson(filename):
        # альтернативная загрузка json данных от поставщика

        with open(filename, "r") as w:
            json_ = json.load(w)

        return json_


    def _dc_kind(self, CategoryID, Subcategory, Vendor):
        """ Создаем 'kind' согласно Category_main_dict.
        что-то не по плану, тогда 'vent', если материнки или процы то через доп
        параметры 'Vendor', 'Subcategory'.
        Возвращаем kind_item
        """

        kind_item = 'vent'
        Category_main_dict = {
        '1': 'proc',
        '6': 'mb',
        '23': 'cool',
        '8': 'case',
        '3': 'hdd',
        '724': 'ps',
        '9': 'video',
        '27': 'ssd',
        '2': 'mem',
        '5': 'mon',
        }

        intel_mb = ('Socket 1851', 'Socket 1700', 'CPU onboard', 'Socket 1200',)
        amd_mb = ('Socket AM5', 'Socket AM4')
        # intel_mb и amd_mb редактируем в будущем !!!

        if CategoryID in Category_main_dict:
            temp_kind = Category_main_dict[CategoryID]
            if temp_kind == 'proc':
                kind_item = 'iproc' if Vendor == 'Intel' else 'aproc'
                return kind_item
            if temp_kind == 'mb':
                if Subcategory in intel_mb:
                    return 'imb'
                else:
                    return 'amb'
            return Category_main_dict[CategoryID]

        return kind_item

    def getDC(self, file=None):
        """ возвращаем словарь где ключи: партнамбера от 'dc', а значения типа:
            {'partnumber_parts': 'GLE850', 'name_parts': 'Блок живлення 850 Вт',
            'availability_parts': 'yes', 'kind': 'ps',
            'providerprice_parts': 116.0, 'RRP_UAH': 5899.0}
        """

        data = {} # пока пустой словарь

        xml = self._loadFromFile(file) if file else self.content

        group = GroupToKind('dc') # получим кортеж нужных групп от 'dc'
        if not group:
            print('no group')
            return data

        try:
            root = etree.fromstring(xml)
        except:
            print('ошибка в xml')
            return data

        data = {
            get_text(item.find("Article")): {
                "partnumber_parts": get_text(item.find("Article")),
                "name_parts": get_text(item.find("Name")),
                "availability_parts": dc_avail(get_text(item.find("Availability"))
                ),
                "kind": self._dc_kind(get_text(item.find("CategoryID")),
                get_text(item.find("Subcategory")),
                get_text(item.find("Vendor")),
                ),
                "providerprice_parts": get_float(item.find("PriceUSD")),
                "RRP_UAH": get_float(item.find("RRP_UAH")),
            }
            for item in root.findall("Product") if get_text(
            item.find("CategoryID")) in group\
            and dc_avail(get_text(item.find("Availability"))) == 'yes'
        }

        return data


    def _asbis_kind(self, CategoryID, DESCRIPTION, Vendor):
        """ Создаем 'kind' согласно Category_main_dict.
        что-то не по плану, тогда 'vent', если процы то через доп
        параметр 'Vendor', 'DESCRIPTION' - для кулеров/вентиляторов
        """
        kind_item = 'vent'
        Category_main_dict = {
        'CPU Desktop': 'proc',
        'Cooling System': 'cool',
        'HDD Desktop': 'hdd',
        'HDD Video Surveillance': 'hdd',
        'HDD NAS': 'hdd',
        'Monitor LCD': 'mon',
        'Monitor LED': 'mon',
        'Video Card': 'video',
        'SSD Client': 'ssd',
        'Memory Desktop': 'mem',
        }
        if CategoryID in Category_main_dict:
            temp_kind = Category_main_dict[CategoryID]
            if temp_kind == 'proc':
                kind_item = 'iproc' if Vendor.lower() == 'intel' else 'aproc'
                return kind_item
            if temp_kind == 'cool':
                if DESCRIPTION.lower().find('mm') != -1:
                    return 'vent'
                else:
                    return 'cool'
            return Category_main_dict[CategoryID]
        return kind_item

    def getASBIS(self, file=None):
        """ возвращаем словарь где ключи: партнамбера от 'asbis', а значения типа:
            {'partnumber_parts': 'GLE850', 'name_parts': 'Блок живлення 850 Вт',
            'availability_parts': 'yes', 'kind': 'ps',
            'providerprice_parts': 116.0, 'RRP_UAH': 5899.0}
        """

        data = {} # пока пустой словарь

        usd = self.currency

        xml = self._loadFromFile(file) if file else self.content

        group = GroupToKind('asbis') # получим кортеж нужных групп от 'asbis'
        if not group:
            print('no group')
            return data

        try:
            root = etree.fromstring(xml)
        except:
            print('ошибка в xml')
            return data
        try:
            asbis_price = root.find('PRICES').findall('PRICE')
        except:
            print('структура xml уже другая?')
            return data

        data = {
            get_text(item.find("WIC")): {
                "partnumber_parts": get_text(item.find("WIC")),
                "name_parts": get_text(item.find("DESCRIPTION")),
                "availability_parts": asbis_avail(get_text(item.find("AVAIL"))),
                "kind": self._asbis_kind(get_text(item.find("GROUP_NAME")),
                get_text(item.find("DESCRIPTION")),
                get_text(item.find("VENDOR_NAME")),
                ),
                "providerprice_parts": round(get_float(item.find("MY_PRICE")) / usd, 1),
                "RRP_UAH": get_float(item.find("RETAIL_PRICE")),
            }
            for item in asbis_price if get_text(item.find("GROUP_NAME")) in group\
            and asbis_avail(get_text(item.find("AVAIL"))) == 'yes'
        }

        return data


    def _elko_kind(self, CategoryID, Vendor):
        """Создаем 'kind' согласно Category_main_dict.
        что-то не по плану, тогда 'vent', если процы то через доп
        параметры 'Vendor'
        """
        kind_item = 'vent'
        Category_main_dict = {
        'CPU': 'proc',
        'MBA': 'amb',
        'MBI': 'imb',
        'COC': 'cool',
        'PSU': 'ps',
        'CAS': 'case',
        'HDS': 'hdd',
        'LC3': 'mon',
        'VGP': 'video',
        'SSM': 'ssd',
        'SSU': 'ssd',
        'MEM': 'mem',
        'COS': 'vent',
        'WRA': 'wifi',
        }
        if CategoryID in Category_main_dict:
            temp_kind = Category_main_dict[CategoryID]
            if temp_kind == 'proc':
                kind_item = 'iproc' if Vendor.lower() == 'intel' else 'aproc'
                return kind_item
            return Category_main_dict[CategoryID]
        return kind_item

    def getELKO(self, file=None):
        """ возвращаем словарь где ключи: партнамбера от 'elko', а значения типа:
            {'partnumber_parts': 'GLE850', 'name_parts': 'Блок живлення 850 Вт',
            'availability_parts': 'yes', 'kind': 'ps',
            'providerprice_parts': 116.0, 'RRP_UAH': 5899.0}
        """

        data = {} # пока пустой словарь

        usd = self.currency

        json_ = self._loadFromFileJson(file) if file else self.content

        group = GroupToKind('elko') # получим кортеж нужных групп от 'elko'
        if not group:
            print('no group')
            return data

        try:
            elko = json.loads(json_) if isinstance(json_, str) else json_
        except:
            print('ошибка в json')
            return data

        if not elko:
            return data

        data = {
            get_text(item["manufacturerCode"]): {
                "partnumber_parts": get_text(item["manufacturerCode"]),
                "name_parts": get_text(item["name"]),
                "availability_parts": elko_avail(get_text(item["quantity"])),
                "kind": self._elko_kind(get_text(item["catalog"]),
                get_text(item["vendorName"]),
                ),
                "providerprice_parts": price_usd(get_float(item["price"]),
                usd, get_text(item["currency"])
                ),
                "RRP_UAH": get_float(item["rrp"]),
            }
            for item in elko if get_text(item['catalog']) in group\
            and elko_avail(get_text(item["quantity"])) == 'yes'
        }

        return data


    def _mti_kind(self, CategoryID, name, Vendor):
        """Создаем 'kind' согласно Category_main_dict.
        что-то не по плану, тогда 'vent', если материнки или процы то через доп
        параметры 'name', 'Vendor'
        """
        kind_item = 'vent'
        Category_main_dict = {
        '114': 'proc',
        '112': 'mb',
        '122': 'cool',
        '121': 'vent',
        '118': 'case',
        '111': 'hdd',
        '119': 'ps',
        '143': 'video',
        '116': 'ssd',
        '1668': 'mem',
        '143': 'mon',
        '199': 'wifi',
        }

        if CategoryID in Category_main_dict:
            temp_kind = Category_main_dict[CategoryID]
            if temp_kind == 'proc':
                kind_item = 'aproc' if Vendor == 'amd' else 'iproc'
                return kind_item
            if temp_kind == 'mb':
                if name.lower().find('am') != -1 or name.lower().find('x870') != -1:
                    return 'amb'
                else:
                    return 'imb'
            return Category_main_dict[CategoryID]
        return kind_item

    def getMTI(self, file=None):
        """ возвращаем словарь где ключи: партнамбера от 'mti', а значения типа:
            {'partnumber_parts': 'GLE850', 'name_parts': 'Блок живлення 850 Вт',
            'availability_parts': 'yes', 'kind': 'ps',
            'providerprice_parts': 116.0, 'RRP_UAH': 5899.0}
        """

        data = {} # пока пустой словарь

        usd = self.currency

        xml = self._loadFromFile(file) if file else self.content

        group = GroupToKind('mti') # получим кортеж нужных групп от 'mti'
        if not group:
            print('no group')
            return data

        try:
            root = etree.fromstring(xml)
        except:
            print('ошибка в xml')
            return data
        try:
            mti_price = root.find('result').findall('productgroup')
        except:
            print('структура xml уже другая?')
            return data

        data = {
            get_text(item.find("partnum")): {
                "partnumber_parts": get_text(item.find("partnum")),
                "name_parts": get_text(item.find("prodname")),
                "availability_parts": mti_avail(get_text(item.find("store"))),
                "kind": self._mti_kind(
                    get_text(item.find("productgroup_id")),
                    get_text(item.find("prodname")),
                    get_text(item.find("brand")),
                ),
                "providerprice_parts": round(get_float(item.find("price_uah")) / usd, 1),
                "RRP_UAH": get_float(item.find("rrp")),
            }
            for prod in (x.find('products').findall('product') for x in mti_price)
            for item in prod
            if get_text(item.find("productgroup_id")) in group\
            and mti_avail(get_text(item.find("store"))) == 'yes'
        }

        return data


    def _brain_kind(self, Group, CategoryName, Vendor, Description):
        """Создаем 'kind' согласно Category_main_dict.
        что-то не по плану, тогда 'vent', если материнки или процы то через доп
        параметры 'Vendor', 'Description'.
        'CategoryName' для корпусов/бп и для келеров/вентиляторов
        """
        kind_item = 'vent'
        Category_main_dict = {
        'Корпуса': 'case_ps',
        'Модули памяти': 'mem',
        'Материнские платы': 'mb',
        'Корпуса  имп.': 'case_ps',
        'Накопители SSD': 'ssd',
        'Накопители HDD - 3.5", 2.5", внутренние': 'hdd',
        'Видеокарты': 'video',
        'Процессоры': 'proc',
        'Системы охлаждения': 'cool_vent',
        'Сетевое оборудование активное': 'wifi',
        'Мониторы': 'mon',
        }
        if Group in Category_main_dict:
            temp_kind = Category_main_dict[Group]
            if temp_kind == 'proc':
                kind_item = 'iproc' if Vendor == 'Intel' else 'aproc'
                return kind_item
            if temp_kind == 'mb':
                if Description.lower().find('am') == -1:
                    return 'imb'
                else:
                    return 'amb'
            if temp_kind == 'case_ps':
                if CategoryName == 'Корпуса':
                    return 'case'
                else:
                    return 'ps'
            if temp_kind == 'cool_vent':
                if CategoryName == 'Кулеры к процессорам':
                    return 'cool'
                else:
                    return 'vent'
            return Category_main_dict[Group]
        return kind_item

    def getBRAIN(self, file=None):
        """ возвращаем словарь где ключи: партнамбера от 'brain', а значения типа:
            {'partnumber_parts': 'GLE850', 'name_parts': 'Блок живлення 850 Вт',
            'availability_parts': 'yes', 'kind': 'ps',
            'providerprice_parts': 116.0, 'RRP_UAH': 5899.0}
        """

        data = {} # пока пустой словарь

        #usd = self.currency

        json_ = self._loadFromFileJson(file) if file else self.content

        group = GroupToKind('brain') # получим кортеж нужных групп от 'brain'
        if not group:
            print('no group')
            return data

        try:
            #brain = json_.json()
            brain = json.loads(json_) if isinstance(json_, str) else json_
        except:
            print('ошибка в json')
            return data

        if not brain:
            return data

        data = {
            item["Article"]: {
                "partnumber_parts": get_text(item["Article"]),
                "name_parts": get_text(item["Name"]),
                "availability_parts": brain_avail(get_text(item["Stock"])),
                "kind": self._brain_kind(get_text(item["Group"]),
                get_text(item["CategoryName"]),
                get_text(item["Vendor"]),
                get_text(item["Description"]),
                ),
                "providerprice_parts": get_float(item["PriceUSD"]),
                "RRP_UAH": get_float(item["RetailPrice"]),
            }
            for item in brain.values() if item["Group"] in group\
            and brain_avail(get_text(item["Stock"])) == 'yes'
        }

        return data


    def _edg_kind(self, CategoryID, Name):
        """Создаем 'kind' согласно Category_main_dict.
        что-то не по плану, тогда 'vent', если охлаждение то через доп
        параметры 'Name'
        """
        kind_item = 'vent'
        Category_main_dict = {
        'Системи охолодження, Cooler': 'cool_vent',
        'Блоки живлення ATX': 'ps',
        'Корпуси': 'case',
        }
        if CategoryID in Category_main_dict:
            temp_kind = Category_main_dict[CategoryID]
            if temp_kind == 'cool_vent':
                kind_item = 'cool' if Name.lower().find('кулер') != -1 else 'vent'
                return kind_item
            return Category_main_dict[CategoryID]
        return kind_item

    def getEDG(self, file=None):
        """ возвращаем словарь где ключи: партнамбера от 'edg', а значения типа:
            {'partnumber_parts': 'GLE850', 'name_parts': 'Блок живлення 850 Вт',
            'availability_parts': 'yes', 'kind': 'ps',
            'providerprice_parts': 116.0, 'RRP_UAH': 5899.0}
        """

        data = {} # пока пустой словарь

        #usd = self.currency

        xml = self._loadFromFile(file) if file else self.content

        group = GroupToKind('edg') # получим кортеж нужных групп от 'edg'
        if not group:
            print('no group')
            return data

        try:
            root = etree.fromstring(xml)
        except:
            print('ошибка в xml')
            return data
        try:
            edg_price = root.find('items').findall('item')
        except:
            print('структура xml уже другая?')
            return data

        data = {
            get_text(item.find("Code")): {
                "partnumber_parts": get_text(item.find("Code")),
                "name_parts": get_text(item.find("Name")),
                "availability_parts": edg_avail(get_text(item.find("StockName"))
                ),
                "kind": self._edg_kind(get_text(item.find("Subcategory")),
                get_text(item.find("Name")),
                ),
                "providerprice_parts": get_float(item.find("Price")),
                "RRP_UAH": get_float(item.find("RRP")),
            }
            for item in edg_price if get_text(item.find("Subcategory")) in group\
            and edg_avail(get_text(item.find("StockName"))) == 'yes'
        }

        return data


    def GetPriceAll(self, current, file=None):
        """Универсальный вызов для всех getDС, ..., getEDG
           current = 'getDС' (например)
           возвращает один из getDС, ..., getEDG
        """

        current_fun = getattr(self, current, None)  # Проверяем наличие метода current
        if callable(current_fun):  # Вызываем, если метод существует
            return current_fun(file)
        else:
            return f"Метод {current} не найден"


"""
3,5" 3Tb Seagate
"""
