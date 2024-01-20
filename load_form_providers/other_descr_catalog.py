import requests, re, json
#import lxml
from lxml import etree

def quantity_to_avail(str_):
    # for get_from_json_elko2
    #пребразование из quantity в общий статус (yes, no)

    if str_.find('>') != -1:
        return 'yes'
    elif str_ == '0':
        return 'no'
    else:
        return 'q'

def category_re(str_):
    k = "миша|крісло|клавіатура|комплект|гарнітура|навушники|акустична система|комп'ютерний стіл|килимок|поверхня|веб камера"
    try:
        return  re.findall(k,str_.lower())[0]
    except IndexError:
        return 'noname'

class From_provders_filePrices:
    """ меняем цену в dict_ если дешевле при наличии
        set_parts - партнамберы периферии всех? категорий """

    def __init__(self, set_parts, dict_, currency):
        self.set_parts = set_parts
        self.dict_ = dict_
        self.currency = currency

    def to_priceUSD(self, price):
        try:
            return round(float(price) / float(self.currency), 1)
        except (ZeroDivisionError, ValueError):
            return 0

    def from_brain(self, filename):
        # из скачанного файла brain меняем dict

        __count_new, __count_update = 0, 0
        # __count_new, __count_update - счетчики добавлений в dict_ и замены

        dict_sub = {
        'Акустические системы': '25',
        'Фильтры питания': '45',
        'Веб-камеры': '54',
        'Мониторы': '5',
        'Наушники, гарнитуры, микрофоны': '56'
        }
        # категории brain в dict_ категории

        if not isinstance(filename, str):
            json_data = filename
            # временная доработка (вместо файла-содержимое файла)

        else:
            try:
                with open(filename, "r") as write_file:
                    json_data=json.load(write_file)
            except:
                return (False, {'count_new': __count_new,
                        'count_update': __count_update,
                        'status': 'no_file'})


        if isinstance(json_data, dict):

            for data_json_data in json_data.values():
                try:
                    if data_json_data['Article'] in self.set_parts and\
                    data_json_data['DayDelivery'] in ('0', '1', '2', '3') and\
                    data_json_data['Group'] in dict_sub:
                        # если партнамбер-brain есть в set_parts и наличие тру
                        # и категория-brain есть в dict_sub
                        price_ = float(data_json_data['PriceUSD'])
                        try:
                            rrp = float(data_json_data['RetailPrice'])
                        except:
                            rrp = 0
                        if dict_sub[data_json_data['Group']] in self.dict_:
                            # если категория-brain в dict_
                            if data_json_data['Article'] in self.dict_[
                            dict_sub[data_json_data['Group']]
                            ]:
                                # если партнамбер уже существует и цена ниже - меняем в dict_
                                try:
                                    price_dict = float(
                                    self.dict_[dict_sub[
                                    data_json_data['Group']]][data_json_data['Article']][
                                    'PriceUSD'])
                                except:
                                    price_dict = 0
                                if price_ < price_dict:
                                    self.dict_[
                                    dict_sub[
                                    data_json_data['Group']]][data_json_data['Article']] = \
                                    {'PriceUSD': price_,
                                    'provider': 'brain',
                                    'RRP_UAH': rrp}
                                    __count_update += 1
                            else:
                                # если партнамбера нет - записываем в dict_
                                self.dict_[
                                dict_sub[data_json_data['Group']]][data_json_data['Article']] =\
                                {'PriceUSD': price_,
                                'provider': 'brain',
                                'RRP_UAH': rrp}
                                __count_new += 1
                        else:
                            # если категория-brain нет dict_ - создаем кат и записываем нов об-т
                            self.dict_[dict_sub[data_json_data['Group']]] = {}
                            self.dict_[
                            dict_sub[data_json_data['Group']]][data_json_data['Article']] =\
                            {'PriceUSD': price_,
                            'provider': 'brain',
                            'RRP_UAH': rrp}
                            __count_new += 1
                except Exception as e:
                    return (False, {'count_new': __count_new,
                            'count_update': __count_update,
                            'status': e})

            return (True, {'count_new': __count_new,
                    'count_update': __count_update,
                    'status': 'ok'})

        else:
            return (False, {'count_new': __count_new,
                    'count_update': __count_update,
                    'status': 'json_data_no_dict'})

    def from_edg(self, filename):
        # из скачанного файла edg меняем dict_

        __count_new, __count_update = 0, 0
        # __count_new, __count_update - счетчики добавлений в dict_ и замены

        dict_sub = {
        'Миші': '11',
        'Геймерські крісла': '125',
        'Клавіатури': '33',
        'Комплекти (клавіатура+миша)': '968',
        'Навушники та мікрофони': '56',
        'Акустичні системи': '25',
        'Ігрові столи': '1376',
        'Мережеві фільтри': '45',
        'Килимки': '24',
        'Вебкамери': '54',
        'Аудіо/відео кабелі': '648',
        }
        # категории edg в dict_ категории

        status_ = ('В наявності', 'Закінчується')

        try:
            with open(filename, 'rb') as fobj:
                xml = fobj.read()
        except:
            return (False, {'count_new': __count_new,
                    'count_update': __count_update,
                    'status': 'no_file'})

        try:
            root = etree.fromstring(xml)
            result_data=root.find('items').findall('item')
        except:
            return (False, {'count_new': __count_new,
                    'count_update': __count_update,
                    'status': 'xml_data_bad'})

        for data in result_data:
            try:
                temp = dict()
                for k in data.getchildren():
                    if k.tag in ['Code', 'Price', 'StockName', 'Subcategory', 'RRP']:
                        temp[k.tag] = k.text
                if temp['Subcategory'] in dict_sub and temp['Code'] in\
                self.set_parts and temp['StockName'] in status_:
                    price_ = float(temp['Price'])
                    try:
                        rrp = float(temp['RRP'])
                    except:
                        rrp = 0
                    if dict_sub[temp['Subcategory']] in self.dict_:
                        # если категория-edg в dict_
                        if temp['Code'] in self.dict_[
                        dict_sub[temp['Subcategory']]
                        ]:
                            # если партнамбер уже существует и цена ниже - меняем в dict_
                            try:
                                price_dict = float(
                                self.dict_[dict_sub[
                                temp['Subcategory']]][temp['Code']][
                                'PriceUSD'])
                            except:
                                price_dict = 0
                            if price_ < price_dict:
                                self.dict_[
                                dict_sub[
                                temp['Subcategory']]][temp['Code']] = \
                                {'PriceUSD': price_,
                                'provider': 'edg',
                                'RRP_UAH': rrp}
                                __count_update += 1
                        else:
                            # если партнамбера нет - записываем в dict_
                            self.dict_[
                            dict_sub[temp['Subcategory']]][temp['Code']] =\
                            {'PriceUSD': price_,
                            'provider': 'edg',
                            'RRP_UAH': rrp}
                            __count_new += 1
                    else:
                        # если категория-edg нет dict_ - создаем кат и записываем нов об-т
                        self.dict_[dict_sub[temp['Subcategory']]] = {}
                        self.dict_[
                        dict_sub[temp['Subcategory']]][temp['Code']] =\
                        {'PriceUSD': price_,
                        'provider': 'edg',
                        'RRP_UAH': rrp}
                        __count_new += 1

            except Exception as e:
                return (False, {'count_new': __count_new,
                        'count_update': __count_update,
                        'status': e})
        return (True, {'count_new': __count_new,
                'count_update': __count_update,
                'status': 'ok'})

    def from_elko(self, filename):
        # из скачанного файла elko меняем dict_

        __count_new, __count_update = 0, 0
        # __count_new, __count_update - счетчики добавлений в dict_ и замены

        dict_sub = {
        'LC3': '5',
        'MOU': '11',
        'KEY': '33',
        'HST': '56',
        'SPE': '25',
        }
        # категории elko в dict_ категории

        try:
            with open(filename, "r") as write_file:
                json_data=json.load(write_file)
        except:
            return (False, {'count_new': __count_new,
                    'count_update': __count_update,
                    'status': 'no_file'})

        if isinstance(json_data, list):

            for data in json_data:
                try:
                    if data['manufacturerCode'] in self.set_parts and\
                    quantity_to_avail(data['quantity']) == 'yes' and\
                    data['catalog'] in dict_sub:
                        # если партнамбер-elko есть в set_parts и наличие тру
                        # и категория-elko есть в dict_sub
                        price_ = self.to_priceUSD(data['price'])
                        try:
                            rrp = float(data['rrp'])
                        except:
                            rrp = 0
                        if dict_sub[data['catalog']] in self.dict_:
                            # если категория-elko в dict_
                            if data['manufacturerCode'] in self.dict_[
                            dict_sub[data['catalog']]
                            ]:
                                # если партнамбер уже существует и цена ниже - меняем в dict_
                                try:
                                    price_dict = float(self.dict_[
                                    dict_sub[
                                    data['catalog']]][data['manufacturerCode']]['PriceUSD']
                                    )
                                except:
                                    price_dict = 0
                                if price_ and price_ < price_dict:
                                    self.dict_[
                                    dict_sub[
                                    data['catalog']]][data['manufacturerCode']] = \
                                    {'PriceUSD': price_,
                                    'provider': 'elko',
                                    'RRP_UAH': rrp}
                                    __count_update += 1
                            else:
                                # если партнамбера нет - записываем в dict_
                                self.dict_[
                                dict_sub[data['catalog']]][data['manufacturerCode']] =\
                                {'PriceUSD': price_,
                                'provider': 'elko',
                                'RRP_UAH': rrp}
                                __count_new += 1
                        else:
                            # если категория-elko нет dict_ - создаем кат и записываем нов об-т
                            self.dict_[dict_sub[data['catalog']]] = {}
                            self.dict_[
                            dict_sub[data['catalog']]][data['manufacturerCode']] =\
                            {'PriceUSD': price_,
                            'provider': 'elko',
                            'RRP_UAH': rrp}
                            __count_new += 1
                except Exception as e:
                    return (False, {'count_new': __count_new,
                            'count_update': __count_update,
                            'status': e})

            return (True, {'count_new': __count_new,
                    'count_update': __count_update,
                    'status': 'ok'})

        else:
            return (False, {'count_new': __count_new,
                    'count_update': __count_update,
                    'status': 'json_data_no_dict'})

    def from_mti(self, filename):
        # из скачанного файла mti меняем dict_

        __count_new, __count_update = 0, 0
        # __count_new, __count_update - счетчики добавлений в dict_ и замены

        dict_sub = {
        '164': '11',
        '1241': '125',
        '165': '33',
        '166': '968',
        '171': '56',
        '163': '25',
        '1703': '1376',
        '168': '54',
        '1730': '24',
        '143': '5',
        }
        # категории mti в dict_ категории

        status_ = {'8', '50 и более', '6', '7', '4', '9', '10 и более', '3', '5'}

        try:
            with open(filename, 'rb') as fobj:
                xml = fobj.read()
        except:
            return (False, {'count_new': __count_new,
                    'count_update': __count_update,
                    'status': 'no_file'})

        try:
            root = etree.fromstring(xml)
            result_data=root.find('result').findall('productgroup')
        except:
            return (False, {'count_new': __count_new,
                    'count_update': __count_update,
                    'status': 'xml_data_bad'})

        for x in result_data:
            list_temp=x.find('products').findall('product')
            for data in list_temp:
                temp = dict()
                try:
                    for k in data.getchildren():
                        if k.tag in ['partnum', 'price_uah', 'store', 'productgroup_id']:
                            temp[k.tag] = k.text
                    if temp['productgroup_id'] in dict_sub and temp['partnum'] in\
                    self.set_parts and temp['store'] in status_:
                        price_ = self.to_priceUSD(temp['price_uah'])
                        try:
                            rrp = float(temp['rrp'])
                        except:
                            rrp = 0
                        if dict_sub[temp['productgroup_id']] in self.dict_:
                            # если категория-mti в dict_
                            if temp['partnum'] in self.dict_[
                            dict_sub[temp['productgroup_id']]
                            ]:
                                # если партнамбер уже существует и цена ниже - меняем в dict_
                                try:
                                    price_dict = float(
                                    self.dict_[
                                    dict_sub[
                                    temp['productgroup_id']]][temp['partnum']]['PriceUSD']
                                    )
                                except:
                                    price_dict = 0
                                if price_ and price_ < price_dict:
                                    self.dict_[
                                    dict_sub[
                                    temp['productgroup_id']]][temp['partnum']] = \
                                    {'PriceUSD': price_,
                                    'provider': 'mti',
                                    'RRP_UAH': rrp}
                                    __count_update += 1
                            else:
                                # если партнамбера нет - записываем в dict_
                                self.dict_[
                                dict_sub[temp['productgroup_id']]][temp['partnum']] =\
                                {'PriceUSD': price_,
                                'provider': 'mti',
                                'RRP_UAH': rrp}
                                __count_new += 1
                        else:
                            # если категория-mti нет dict_ - создаем кат и записываем нов об-т

                            self.dict_[dict_sub[temp['productgroup_id']]] = {}
                            self.dict_[
                            dict_sub[temp['productgroup_id']]][temp['partnum']] =\
                            {'PriceUSD': price_,
                            'provider': 'mti',
                            'RRP_UAH': rrp}
                            __count_new += 1

                except Exception as e:
                    return (False, {'count_new': __count_new,
                            'count_update': __count_update,
                            'status': e})
        return (True, {'count_new': __count_new,
                'count_update': __count_update,
                'status': 'ok'})

    def from_eletek(self, filename):
        # filename - здесь урл eletek

        __count_new, __count_update = 0, 0
        # __count_new, __count_update - счетчики добавлений в dict_ и замены

        dict_sub = {
        'миша': '11',
        'крісло': '125',
        'клавіатура': '33',
        'комплект': '968',
        'гарнітура': '56',
        'навушники': '56',
        'акустична система': '25',
        "комп'ютерний стіл": '1376',
        'килимок': '24',
        'поверхня': '24',
        'веб камера': '54',
        }
        # категории eletek в dict_ категории

        status_ = ('В наявності', 'Багато', 'Мало',)

        try:
            eletek = requests.get(filename)
            xml = eletek.content
        except:
            return (False, {'count_new': __count_new,
                    'count_update': __count_update,
                    'status': 'bad_request'})

        try:
            root = etree.fromstring(xml)
            result_data=root.find('offers').findall('offer')
        except:
            return (False, {'count_new': __count_new,
                    'count_update': __count_update,
                    'status': 'xml_data_bad'})

        for data in result_data:
            try:
                temp = dict()
                for k in data.getchildren():
                    if k.tag in ['vendorCode', 'name', 'in_stock',
                    'your_priceUAH', 'regular_RRPUAH']:
                        temp[k.tag] = k.text
                # из названия получаем категорию
                category_ = category_re(temp['name'])
                if category_ in dict_sub and temp['vendorCode'] in\
                self.set_parts and temp['in_stock'] in status_:
                    price_ = self.to_priceUSD(temp['your_priceUAH'])
                    try:
                        rrp = float(temp['regular_RRPUAH'])
                    except:
                        rrp = 0
                    if dict_sub[category_] in self.dict_:
                        # если категория-eletek в dict_
                        if temp['vendorCode'] in self.dict_[
                        dict_sub[category_]
                        ]:
                            # если партнамбер уже существует и цена ниже - меняем в dict_
                            try:
                                price_dict = float(
                                self.dict_[dict_sub[
                                category_]][temp['vendorCode']][
                                'PriceUSD'])
                            except:
                                price_dict = 0
                            if price_ < price_dict:
                                self.dict_[
                                dict_sub[
                                category_]][temp['vendorCode']] = \
                                {'PriceUSD': price_,
                                'provider': 'eletek',
                                'RRP_UAH': rrp}
                                __count_update += 1
                        else:
                            # если партнамбера нет - записываем в dict_
                            self.dict_[
                            dict_sub[category_]][temp['vendorCode']] =\
                            {'PriceUSD': price_,
                            'provider': 'eletek',
                            'RRP_UAH': rrp}
                            __count_new += 1
                    else:
                        # если категория-eletek нет dict_ - создаем кат и записываем нов об-т
                        self.dict_[dict_sub[category_]] = {}
                        self.dict_[
                        dict_sub[category_]][temp['vendorCode']] =\
                        {'PriceUSD': price_,
                        'provider': 'eletek',
                        'RRP_UAH': rrp}
                        __count_new += 1

            except Exception as e:
                return (False, {'count_new': __count_new,
                        'count_update': __count_update,
                        'status': e})
        return (True, {'count_new': __count_new,
                'count_update': __count_update,
                'status': 'ok'})
