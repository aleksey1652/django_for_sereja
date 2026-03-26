#import requests, re, json
#import pandas as pd
#from lxml import etree
#import heapq
#import os
from .to_providers_to_price import *
from .from_providers_to_bd import *


# ниже словарь групп-категорий поставщиков для обработки
# в каждом обработчике (например dc_kind) есть соответсвия c унифицированным 'kind'
OnlyGroups = {
'dc': (
'8', '3', '724', '255', '1', '9', '27', '2', '23', '6', '5'
),
'asbis': (
'Блок питания', 'Видеоплата', 'Корпус', 'Вентилятор', 'Жесткий диск для настольного ПК',
'Память для игрового ПК', 'Монитор со светодиодной подсветкой LED', 'Gaming Monitor',
'Твердотельный накопитель (SSD)', 'Память для настольных систем', 'Система охлаждения',
'Процессор для настольного ПК'
),
'elko': (
'COC','CAS','LC3','MEM','WRA', 'MBA', 'HDS', 'VGP',
'PSU', 'SSM', 'MBI', 'SSU', 'CPU', 'COS',
),
'mti': (
'199', '143', '119', '111', '115', '118',
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
'itlink': (# '4374ac8b-e017-11ec-80d9-000c29e58d51'
"4d06d5bc-d49f-11ea-80c4-000c29e58d51",
"4d06d5f4-d49f-11ea-80c4-000c29e58d51",
"4d06d5c0-d49f-11ea-80c4-000c29e58d51",
"4d06d5c4-d49f-11ea-80c4-000c29e58d51",
"4d06d5c6-d49f-11ea-80c4-000c29e58d51",
"4d06d5de-d49f-11ea-80c4-000c29e58d51",
"4d06d5d6-d49f-11ea-80c4-000c29e58d51", #видяхи не выгружаем
"4d06d5f8-d49f-11ea-80c4-000c29e58d51",
"4d06d5ac-d49f-11ea-80c4-000c29e58d51",
"4d06d5b2-d49f-11ea-80c4-000c29e58d51",
),
}


def do_xml_param_itlink_(item, attrs, attrs_values):
    """
    вспомогательная ф для получения значения атрибута тэга xml item (для
    примера: <param name="Модельный ряд">Red Pro</param>
             <param other="other values">...</param>
     attrs="name",
    attrs_values="Модельный ряд")
    """
    try:
        return [param for param in item.findall("param") if param.get(
        attrs) == attrs_values][0].text.lower()
    except Exception as e:
        return None


def GroupToKind(provider):
    """ из OnlyGroups (словарь групп-категорий поставщиков)
    возвращем кортеж нужных групп или False """

    try:
        return OnlyGroups[provider]
    except KeyError:
        return False


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


def itlinkP_avail(data, tag='available'):
    """itlink data - тэг с параметром tag, на выходе - унифицированный статус
    согласно словаря иначе 'no' """

    avail_dict = {
    "true":'yes',
    'false':'no',
    }
    try:
        return avail_dict[data.get(tag)]
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
                    #print("Тип данных: Неизвестный")
                    try:
                        etree.fromstring(self.content.encode('utf-8'))
                        print("Тип данных: XML")
                        self.content = self.content.encode('utf-8')
                    except:
                        print("Тип данных: Неизвестный")
        else:
            print("Тип данных: Не байт и не строка")


    @staticmethod
    def _loadFromFile(filename):
        # альтернативная загрузка xml данных от поставщика

        try:
            with open(filename, 'rb') as fobj:
                xml = fobj.read()
        except FileNotFoundError:
            return None

        return xml

    @staticmethod
    def _loadFromFileJson(filename):
        # альтернативная загрузка json данных от поставщика

        try:
            with open(filename, "r") as w:
                json_ = json.load(w)
        except FileNotFoundError:
            return None

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
        'Процессор для настольного ПК': 'proc',
        'Система охлаждения': 'cool',
        'Жесткий диск для настольного ПК': 'hdd',
        'Gaming Monitor': 'mon',
        'Монитор со светодиодной подсветкой LED': 'mon',
        'Видеоплата': 'video',
        'Твердотельный накопитель (SSD)': 'ssd',
        'Память для настольных систем': 'mem',
        'Память для игрового ПК': 'mem',
        'Блок питания': 'ps',
        'Вентилятор': 'vent',
        'Корпус': 'case',
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
        '115': 'hdd',
        '119': 'ps',
        '143': 'video',
        '111': 'video',
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

        if not brain or not isinstance(brain, dict):
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


    def _itlink_kind(self, Group, item, Vendor):
        """Создаем 'kind' согласно Category_main_dict.
        item - сам элемент с тэгом param и атрибутом name: Опис - это для материнок надо
        """
        kind_item = 'vent'
        Category_main_dict = {
        "4d06d5bc-d49f-11ea-80c4-000c29e58d51": 'ps',
        "4d06d5f4-d49f-11ea-80c4-000c29e58d51": 'mem',
        "4d06d5c0-d49f-11ea-80c4-000c29e58d51": 'mb',
        "4d06d5c4-d49f-11ea-80c4-000c29e58d51": 'case',
        "4d06d5c6-d49f-11ea-80c4-000c29e58d51": 'ssd',
        "4d06d5de-d49f-11ea-80c4-000c29e58d51": 'hdd',
        "4d06d5d6-d49f-11ea-80c4-000c29e58d51": 'video',
        "4d06d5f8-d49f-11ea-80c4-000c29e58d51": 'proc',
        "4d06d5ac-d49f-11ea-80c4-000c29e58d51": 'cool',
        "4d06d5b2-d49f-11ea-80c4-000c29e58d51": 'vent',
        }
        if Group in Category_main_dict:
            temp_kind = Category_main_dict[Group]
            if temp_kind == 'proc':
                kind_item = 'iproc' if Vendor.lower() == 'intel' else 'aproc'
                return kind_item
            if temp_kind == 'mb':
                res = do_xml_param_itlink_(item, 'name', 'Чипсет')
                if res:
                    _ = isinstance(res, str) and res.lower().find('intel') != -1
                    intel_or_amd = 'imb' if _ else 'amb'
                    return intel_or_amd
                res = do_xml_param_itlink_(item, 'name', 'Опис')
                if res:
                    intel_or_amd = 'imb' if res.find('intel') != -1 else 'amb'
                    return intel_or_amd
                return 'amb'

            return Category_main_dict[Group]
        return kind_item


    def getItlink(self, file=None):
        """ возвращаем словарь где ключи: партнамбера от 'itlink', а значения типа:
            {'partnumber_parts': 'GLE850', 'name_parts': 'Блок живлення 850 Вт',
            'availability_parts': 'yes', 'kind': 'ps',
            'providerprice_parts': 116.0, 'RRP_UAH': 5899.0}
        """

        data = {} # пока пустой словарь

        #usd = self.currency

        xml = self._loadFromFile(file) if file else self.content

        group = GroupToKind('itlink') # получим кортеж нужных групп от 'itlink'
        if not group:
            print('no group')
            return data

        try:
            root = etree.fromstring(xml)
        except:
            print('ошибка в xml')
            return data
        try:
            itlink_price = root.xpath("//offer")
        except:
            print('структура xml уже другая?')
            return data

        data = {
            get_text(item.find("vendorCode")): {
                "partnumber_parts": get_text(item.find("vendorCode")),
                "name_parts": get_text(item.find("name")),
                "availability_parts": itlinkP_avail(item),
                "kind": self._itlink_kind(get_text(item.find("categoryId")), item,
                get_text(item.find("vendor")),
                ),
                "providerprice_parts": get_float(item.find("price")),
                "RRP_UAH": get_float(item.find("rrp")),
            }
            for item in itlink_price if get_text(item.find("categoryId")) in group\
            and itlinkP_avail(item) == 'yes'
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


#
ForFiles = {
'itlink': {
    'mes': {
        'name_prov': 'itlink',
        'new': 0,
        'update': 0,
        'diff_error': 0,
        'empty_error': 0
    },
    'list_category': (
        'kind', 'partnumber_parts',
        'name_parts', 'availability_parts',
        'providerprice_parts','RRP_UAH'
        ),
    'catalog': {
        'SSD':'ssd',
        'Корпуса для ПК':'case',
        'Кулери': 'cool',
        'Материнські плати': 0,
        'Вентилятори': 'vent',
        'Жорсткі диски': 'hdd',
        'Відеокарти':'video',
        "Модулі пам'яті": 'mem',
        'Процесори': 1,
        'Джерело живлення': 'ps',
    },
    'filename': '/прайс.xls',
    'cols': (0,2,3,6,8,9)
},
'erc': {
    'mes': {
        'name_prov': 'erc',
        'new': 0,
        'update': 0,
        'diff_error': 0,
        'empty_error': 0
    },
    'list_category': (
        'subcategory', 'name_parts', 'partnumber_parts', 'RRP_UAH',
        'providerprice_parts', 'usd', 'availability_parts'
        ),
    'catalog': {
                'Накопичувачі SSD':'ssd',
                'Корпуси ПК':'case',
                'Материнські плати':0,
                'Процесори': 1,
                "Накопичувачі HDD внутрішні комп'ютерів":'hdd',
                'Відеокарти':'video',
                'Кулери та радіатори ПК': 'cool',
                "Пам'ять оперативна DDR ПК":'mem',
                'Пам&#39;ять оперативна DDR ПК':'mem',
                'Блоки живлення ПК':'ps',
                'Накопичувачі SSD':'ssd'
    },
    'filename': '/прайс_erc.xls',
    'cols': (2, 3, 4, 6, 9, 10, 13)
},
'be': {
    'mes': {
        'name_prov': 'be',
        'new': 0,
        'update': 0,
        'diff_error': 0,
        'empty_error': 0
    },
    'list_category': (
        'partnumber_parts', 'name_parts',
        'providerprice_parts', 'RRP_UAH', 'availability_parts', 'kind'
        ),
    'catalog': {'Блок живлення':'ps',
                'Корпус для ПК':'case',
                'Охолодження процесора':'cool',
                "Вентилятор для ПК":'vent',
                'кабель-адаптер':'cables',
                'Термопаста': 'cool',
                "Охолодження для SSD накопичувача":'vent',
                },
    'filename': '/прайс_be.xls',
    'cols': (0, 1, 2, 3, 4, 8)
},
'dw': {
    'mes': {
        'name_prov': 'dw',
        'new': 0,
        'update': 0,
        'diff_error': 0,
        'empty_error': 0
    },
    'list_category': (
        'partnumber_parts', 'name_parts',
        'providerprice_parts', 'RRP_UAH', 'availability_parts'
        ),
    'filename': '/прайс_DiWeave.xlsx',
    'cols': (0, 3, 4, 5, 7)
},
'pccooler': {
    'mes': {
        'name_prov': 'pccooler',
        'new': 0,
        'update': 0,
        'diff_error': 0,
        'empty_error': 0
    },
    'list_category': (
        'partnumber_parts', 'name_parts',
        'providerprice_parts', 'RRP_UAH', 'availability_parts'
        ),
    'filename': '/прайс_pccooler.xlsx',
    'cols': (1, 2, 3, 4, 6)
},
}

def prov_fun(current_prov):
    """
    вспомогательная ф для getDataFile
    по сути эта ф - словарь перестраховка от несущ ключа
    """

    dict_prov = {
    'get_itlink': 'itlink',
    'get_erc': 'erc',
    'get_bequiet': 'be',
    'get_DiWeave': 'dw',
    'get_pccooler': 'pccooler',
    }

    if current_prov in dict_prov:
        return dict_prov[current_prov]
    return None

def itlink_avail(values):
    """
    метод для преобразования availability_parts для itlink
    """

    try:
        avail = 'yes' if int(values) > 0 else 'no'
    except (ValueError, TypeError):
        avail = 'yes' if values == 'есть' else 'no'

    return avail

def get_kind_cooler(str_):
    """
    для cooler возвращаем 'vent' или 'cool'
    """

    if not isinstance(str_, str):
        return 'cool'

    if str_.lower().find('вентилятор') != -1:
        return 'vent'
    return 'cool'


def erc_avail(av):
    """
    метод для преобразования availability_parts для erc
    """

    temp = [x for x in re.findall(r'\d*',av) if x]
    temp = int(temp[0]) if temp else 0
    if temp <= 1 and temp != 0:
        return 'q'
    elif temp > 1:
        return 'yes'
    else:
        return 'no'


def bequiet_avail(str_):
    """
    метод для преобразования availability_parts для DiWeave и bequiet
    """

    if isinstance(str_, str):
        str_ = str_.strip()
    else:
        return 'no'
    dict_status = {
                'Y': 'yes',
                'N': 'no'
                    }
    if str_ in dict_status:
        return dict_status[str_]
    return 'no'


def pccooler_avail(str_):
    """ для pccooler возвращаем 'yes' or 'no' """

    if isinstance(str_, str):
        str_ = str_.strip()
    else:
        return 'no'
    dict_status = {
                '+': 'yes',
                '-': 'no'
                    }
    if str_ in dict_status:
        return dict_status[str_]
    return 'no'

def get_kind_DW(str_):
    """ для get_DiWeave из имени в кайнд """

    dict_kind = {'Блок живлення':'ps',
                'Корпус для ПК':'case',
                'Водяне':'cool',
                "Вентилятор":'vent',
                'Повітряне': 'cool',
                }

    res_temp = re.findall(
    r'Блок живлення|Корпус для ПК|Водяне|Повітряне|Вентилятор', str_
    )

    try:
        return dict_kind[res_temp[0]]
    except:
        return None


class From_file_to_bd:
    """
    для вручную скачанных данных от одного из провайдера(erc, itlink, dw, pccooler, be)
    добавляем/меняем в бд, результат работы в Results для данного провайдера
    """

    def __init__(self, content, usd=0):
        """ загружаем скачанный контент: """
        self.content = content # pandas массив
        self.usd = usd # курс доллара


    def clearProvDb(self, provname):
        """ отключение деталей для данного провайдера """

        count = Parts_full.objects.filter( # выключаем все детали из provname
        providers__name_provider=provname).update(
        availability_parts='no', providerprice_parts=0, rrprice_parts=0)

        return count

    def clearNb(self, provname='itlink'):
        """ отключение itlink nb """
        from tech.models import NB

        count = NB.objects.filter( # выключаем все детали из provname
        provider=provname).update(
        is_active=False, price_ua=0, price_usd=0, rrp_price=0)

        return count


    def itlink_dictToOrder(self, dict_, row_category):
        """
        функция для get_itlink
        меняем данные для:
        RRP_UAH(если пусто то 0),
        availability_parts(унифицируем в yes,no),
        name_parts(сокращаем),
        добавляем:
         в dict_ унифицированный kind из row_category
        """

        rrp = dict_['RRP_UAH']
        rrp = rrp if pd.notna(rrp) else 0
        dict_['RRP_UAH'] = rrp

        if row_category in (0,1):
            row_category = to_article2_1(dict_['name_parts'], pr=row_category)
        dict_['kind'] = row_category

        dict_['availability_parts'] = itlink_avail(dict_['availability_parts'])

        dict_['name_parts'] = dict_['name_parts'][:50]

        return dict_


    def itlink_nb_dictToOrder(self, dict_):
    """
    обработка ноутов:
    - нормализация RRP_UAH
    - availability_parts -> yes/no
    - парсинг name_parts
    """

    # RRP
    rrp = dict_.get('RRP_UAH')
    dict_['RRP_UAH'] = rrp if pd.notna(rrp) and rrp != '' else 0

    # тип
    dict_['kind'] = 'nb'

    # наличие
    dict_['availability_parts'] = itlink_avail(dict_.get('availability_parts'))

    # парсинг имени
    has_parts, count, parts, clean_name = name_to_parts(dict_.get('name_parts'))
    # (True, 5, ['15.6"', 'Ryzen 7 5825U', '16', 'SSD512', 'DOS'],
    # 'Acer Aspire Go 15 AG15-42P') - пример получаемого из name_to_parts

    # дефолтные значения
    for key in ['nb_sc_d', 'nb_cpu_model', 'nb_ram_v', 'nb_ssd', 'os',
               'name_parts', 'vendor', 'seria']:
        dict_[key] = ''

    dict_['nb_cpu_vendor'] = 'Intel'

    vendor, seria = get_vendor_series(clean_name)

    # если всё ок
    if has_parts and count >= 5:
        nb_sc_d, nb_cpu_model, nb_ram_v, nb_ssd, os, *_ = parts

        if 'RYZEN' in clean_name.upper():
            dict_['nb_cpu_vendor'] = 'AMD'

        dict_['nb_sc_d'] = nb_sc_d
        dict_['nb_cpu_model'] = nb_cpu_model
        dict_['nb_ram_v'] = nb_ram_v
        dict_['nb_ssd'] = nb_ssd
        dict_['os'] = os
        dict_['name_parts'] = clean_name
        dict_['vendor'] = vendor
        dict_['seria'] = seria

    return dict_


    def erc_dictToOrder(self, dict_, row_category):
        """
        функция для get_erc
        меняем данные для:
        RRP_UAH(если пусто то 0);
        в providerprice_parts при dict_['usd'] == 0 в долларах,
        иначе в грн - тогда пересчет по курсу с учетом usd_cuurency;
        availability_parts(унифицируем в yes,no);
        name_parts(сокращаем)
        добавляем:
        в dict_ унифицированный kind из row_category, get_kind_cooler -
        для уточнения в кулерах(могут быть вентиляторы)
        """

        try:
            price = float(dict_['providerprice_parts'])
        except:
            price = 0

        usd_cuurency = self.usd
        usd_cuurency = usd_cuurency if usd_cuurency else 1

        rrp = dict_['RRP_UAH']
        rrp = rrp if pd.notna(rrp) else 0
        try:
            rrp = float(rrp)
        except:
            rrp = 0
        dict_['RRP_UAH'] = rrp

        usd = dict_['usd']
        usd = usd if pd.notna(usd) else '0'
        price = price if usd == '0' else price / usd_cuurency
        price = round(price, 1)
        dict_['providerprice_parts'] = price

        if row_category in (0,1):
            row_category = to_article2_1(dict_['name_parts'], pr=row_category)
        if row_category == 'cool':
            dict_['kind'] = get_kind_cooler(dict_['name_parts'])
        dict_['kind'] = row_category

        dict_['availability_parts'] = erc_avail(dict_['availability_parts'])

        dict_['name_parts'] = dict_['name_parts'][:50]

        return dict_


    def be_dictToOrder(self, dict_, row_category):
        """
        функция для get_be
        меняем данные для:
        RRP_UAH(если пусто то 0);
        в providerprice_parts при dict_['usd'] == 0 в долларах,
        иначе в грн - тогда пересчет по курсу с учетом usd_cuurency;
        availability_parts(унифицируем в yes,no);
        name_parts(сокращаем)
        добавляем:
        в dict_ унифицированный kind из row_category
        """

        price = str_to_float(dict_['providerprice_parts'])

        usd_cuurency = self.usd
        usd_cuurency = usd_cuurency if usd_cuurency else 1

        price =  price / usd_cuurency
        price = round(price, 1)
        dict_['providerprice_parts'] = price
        dict_['RRP_UAH'] = str_to_float(dict_['RRP_UAH'])

        dict_['kind'] = ForFiles['be']['catalog'][dict_['kind']]

        dict_['availability_parts'] = bequiet_avail(dict_['availability_parts'])

        dict_['name_parts'] = dict_['name_parts'][:50]

        return dict_


    def dw_dictToOrder(self, dict_, row_category):
        """
        функция для get_DiWeave
        меняем данные для:
        RRP_UAH(если пусто то 0);
        availability_parts(унифицируем в yes,no);
        name_parts(сокращаем)
        добавляем:
        в dict_  kind == row_category
        """

        price = str_to_float(dict_['providerprice_parts'])

        usd_cuurency = self.usd
        usd_cuurency = usd_cuurency if usd_cuurency else 1

        price =  price / usd_cuurency
        price = round(price, 1)
        dict_['providerprice_parts'] = price
        dict_['RRP_UAH'] = str_to_float(dict_['RRP_UAH'])

        dict_['kind'] = row_category

        dict_['availability_parts'] = bequiet_avail(dict_['availability_parts'])

        dict_['name_parts'] = dict_['name_parts'][:50]

        return dict_


    def pccooler_dictToOrder(self, dict_, row_category):
        """
        функция для get_pccooler
        меняем данные для:
        RRP_UAH(если пусто то 0);
        availability_parts(унифицируем в yes,no);
        name_parts(сокращаем)
        добавляем:
        в dict_  kind == row_category
        """

        price = str_to_float(dict_['providerprice_parts'])

        usd_cuurency = self.usd
        usd_cuurency = usd_cuurency if usd_cuurency else 1

        price =  price / usd_cuurency
        price = round(price, 1)
        dict_['providerprice_parts'] = price
        dict_['RRP_UAH'] = str_to_float(dict_['RRP_UAH'])

        dict_['kind'] = row_category

        dict_['availability_parts'] = pccooler_avail(dict_['availability_parts'])

        dict_['name_parts'] = dict_['name_parts'][:50]

        return dict_


    def get_itlink(self):
        """
        из пандас массива получаем dict_res -
        упорядоченный/унифицированный за счет itlink_dictToOrder
        также отключем детали прайса itlink с clearProvDb
        """

        dict_res = {}
        itlink = self.content

        itlink_catalog = ForFiles['itlink']['catalog']
        list_category = ForFiles['itlink']['list_category']

        count = self.clearProvDb('itlink')

        current_category = None

        for row in itlink.itertuples(index=False):
            if row[0] in itlink_catalog:
                current_category = row[0]
            if row[0] not in itlink_catalog and not pd.notna(row[1]):
                current_category = None
            if pd.notna(row[1]) and current_category:
                temp = dict(
                zip(
                list_category, tuple(row)
                ))
                new_dict = self.itlink_dictToOrder(temp, itlink_catalog[current_category])
                if new_dict['availability_parts'] == 'yes':
                    dict_res[new_dict['partnumber_parts']] = new_dict

        return dict_res


    def get_nb_itlink(self):
        """
        из пандас массива получаем dict_res (для ноутов) -
        упорядоченный/унифицированный за счет itlink_nb_dictToOrder
        также отключем ноуты itlink с clearNb
        """

        dict_res = {}
        itlink = self.content

        itlink_catalog = {
        'Ноутбуки':'nb'
        }
        list_category = (
        'kind', 'partnumber_parts',
        'name_parts', 'availability_parts',
        'providerprice_parts','RRP_UAH'
        )

        count = self.clearNb()

        current_category = None

        for row in itlink.itertuples(index=False):
            if row[0] in itlink_catalog:
                current_category = row[0]
            if row[0] not in itlink_catalog and not pd.notna(row[1]):
                current_category = None
            if pd.notna(row[1]) and current_category:
                temp = dict(
                zip(
                list_category, tuple(row)
                ))
                new_dict = self.itlink_nb_dictToOrder(temp)
                if new_dict['availability_parts'] == 'yes':
                    dict_res[new_dict['partnumber_parts']] = new_dict

        return dict_res


    def get_erc(self):
        """
        из пандас массива получаем dict_res -
        упорядоченный/унифицированный за счет erc_dictToOrder
        также отключем детали прайса erc с clearProvDb
        """

        dict_res = {}
        erc = self.content

        erc_catalog = ForFiles['erc']['catalog']
        list_category = ForFiles['erc']['list_category']

        count = self.clearProvDb('erc')

        current_category = None

        for row in erc.itertuples(index=False):
            if row[0] in erc_catalog:
                current_category = row[0]
                temp = dict(
                zip(
                list_category, tuple(row)
                ))
                new_dict = self.erc_dictToOrder(temp, erc_catalog[current_category])
                if new_dict['availability_parts'] == 'yes':
                    dict_res[new_dict['partnumber_parts']] = new_dict

        return dict_res


    def get_bequiet(self):
        """
        из пандас массива получаем dict_res -
        упорядоченный/унифицированный за счет be_dictToOrder
        также отключем детали прайса be с clearProvDb
        """

        dict_res = {}
        be = self.content

        be_catalog = ForFiles['be']['catalog']
        list_category = ForFiles['be']['list_category']

        count = self.clearProvDb('be')

        current_category = None

        for row in be.itertuples(index=False):
            if row[5] in be_catalog:
                current_category = row[5]
                temp = dict(
                zip(
                list_category, tuple(row)
                ))
                new_dict = self.be_dictToOrder(temp, be_catalog[current_category])
                if new_dict['availability_parts'] == 'yes':
                    dict_res[new_dict['partnumber_parts']] = new_dict

        return dict_res


    def get_DiWeave(self):
        """
        из пандас массива получаем dict_res -
        упорядоченный/унифицированный за счет dw_dictToOrder
        также отключем детали прайса be с clearProvDb
        """

        dict_res = {}
        dw = self.content

        #be_catalog = ForFiles['dw']['catalog']
        list_category = ForFiles['dw']['list_category']

        count = self.clearProvDb('dw')

        current_category = None

        for row in dw.itertuples(index=False):
            if isinstance(row[1], str):
                kind = get_kind_DW(row[1])
            else:
                kind = None
            if kind:
                temp = dict(
                zip(
                list_category, tuple(row)
                ))
                new_dict = self.dw_dictToOrder(temp, kind)
                if new_dict['availability_parts'] == 'yes':
                    dict_res[new_dict['partnumber_parts']] = new_dict

        return dict_res


    def get_pccooler(self):
        """
        из пандас массива получаем dict_res -
        упорядоченный/унифицированный за счет pccooler_dictToOrder
        также отключем детали прайса be с clearProvDb
        """

        dict_res = {}
        pccooler = self.content

        #be_catalog = ForFiles['pccooler']['catalog']
        list_category = ForFiles['pccooler']['list_category']

        count = self.clearProvDb('pccooler')

        current_category = None

        for row in pccooler.itertuples(index=False):
            if isinstance(row[1], str):
                kind = get_kind_cooler(row[1])
            else:
                kind = None
            if kind:
                temp = dict(
                zip(
                list_category, tuple(row)
                ))
                new_dict = self.pccooler_dictToOrder(temp, kind)
                if new_dict['availability_parts'] == 'yes':
                    dict_res[new_dict['partnumber_parts']] = new_dict

        set_be = set(dict_res.keys()) # !!! нужен импорт single_clear, pccooler_to_single
        single_clear(set_be) # выключает обьекты single(кулеры и вентиляторы) если
        # их нет в set_be

        temp = [
        pccooler_to_single(
        key, part['kind'], self.usd) for key, part in dict_res.items()
        ] # по партнамберу обновим вентилятор или кулер в singleparts

        return dict_res

    def getDataFile(self, current):
        """
        Универсальный вызов для всех get_itlink, ..., getEDG;
        current = 'get_itlink' (например);
        из get_itlink, ..., getEDG получаем dict_res, который потом в бд;
        результат и время работы в Results;
        возвращаем кортеж (сообщение, время работы)
        """

        current_prov = prov_fun(current) # получаем например 'itlink' из 'get_itlink'
        if not current_prov:
            # доработать с Results ForFiles[current_prov]['mes']
            return ('ERROR', 'erc')

        start = timezone.now()

        current_fun = getattr(self, current, None)  # Проверяем наличие метода current
        if callable(current_fun):  # Вызываем, если метод существует
            dict_res = current_fun()

        if not dict_res:
            # доработать с Results ForFiles[current_prov]['mes']
            return ('ERROR', '00: 00')

        mes = currentProvToBd(dict_res, current_prov) # создание/апдейт для current_prov

        mes_file = currentFileToBd(dict_res, current_prov) # создание/апдейт для "-"
        #от current_prov

        end = timezone.now()

        duration = str(end-start)[2:7]
        #print(f'{duration} min')

        time_message = f';\n time: {duration}min'

        str_message = f"{mes['name_prov']}: new = {mes['new']}, update =\
        {mes['update']}, error = {mes['diff_error']}/{mes['empty_error']}"

        str_main_mes = f";\n{mes_file['name_prov']}: new = {mes_file['new']}, update =\
        {mes_file['update']}, error = {mes_file['diff_error']}/{mes_file['empty_error']}"

        prov_message = str_message + str_main_mes + time_message # + sklsd

        if not Results.objects.filter(who=current_prov).exists():
            r = Results(who=current_prov,
            who_desc=prov_message)
            r.save()
        else:
            r = Results.objects.get(who=current_prov)
            r.who_desc = prov_message
            r.save()

        return (mes, duration)



"""
3,5" 3Tb Seagate
3,5" 6Tb Seagate

def in_comps_parts(short):
    kind, name = short.kind, short.name_parts
    dict_ = {'aproc': Parts_short.objects.filter(cpu__isnull=False,
                name_parts=name, kind=kind),
                'iproc': Parts_short.objects.filter(cpu__isnull=False,
                name_parts=name, kind=kind),
                'amb': Parts_short.objects.filter(mb__isnull=False,
                name_parts=name, kind=kind),
                'imb': Parts_short.objects.filter(mb__isnull=False,
                name_parts=name, kind=kind),
                'mem': Parts_short.objects.filter(ram__isnull=False,
                name_parts=name, kind=kind),
                'hdd': Parts_short.objects.filter(hdd__isnull=False,
                name_parts=name, kind=kind),
                'ssd': Parts_short.objects.filter(ssd__isnull=False,
                name_parts=name, kind=kind),
                'video': Parts_short.objects.filter(gpu__isnull=False,
                name_parts=name, kind=kind),
                'ps': Parts_short.objects.filter(psu__isnull=False,
                name_parts=name, kind=kind),
                'vent': Parts_short.objects.filter(fan__isnull=False,
                name_parts=name, kind=kind),
                'case': Parts_short.objects.filter(case__isnull=False,
                name_parts=name, kind=kind),
                'cool': Parts_short.objects.filter(cooler__isnull=False,
                name_parts=name, kind=kind),
                }
    if kind in dict_:
        if dict_[kind].exists():
            short.in_comps_it = True
            return short
    return None

def in_comps_it_all():
    #
    for_update = Parts_short.objects.all()

    parts = list(for_update)
    updated_parts = [
        in_comps_parts(part)
        for part in parts
    ]

    updated_parts_ok = [part for part in updated_parts if part]

    try:
        with transaction.atomic():
            for_update.bulk_update(
            updated_parts_ok, ['in_comps_it']
            )
    except:
        updated_parts_ok = []

"""
