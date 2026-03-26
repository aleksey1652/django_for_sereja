import json
import pandas as pd
import requests
from lxml import etree
from xml.etree.ElementTree import ParseError
import re
from django.db.models import F, Q, Value, Func
from django.db.models.functions import Coalesce, Concat

from singleparts.models import *
from tech.models import *
from cat.models import Parts_full, USD, Results
from .other_descr_catalog import From_provders_filePrices
from .dc_descr_adv import to_False_or_True,get_discr_categ_dc,get_foto_price_name,\
key_in_dict, dict_color, key_in_dict_values
from .dc_descr_adv import newMonitor, newKM, newKeyboards, newMouses, newPads,\
newHeadsets, newWebcams, newWiFis, newAcoustics, newTables, newChairs,\
newCabelsplus, newFilters, newMike, newNB

#from load_form_providers.get_service Cooler_OTHER get_from_xml, from_price_get_new_models
# to_model_price_from_dc upload_edit_foto to_tech_price_from_dc


def get_foto_list(categ, DC_LOGIN, DC_PASSWORD):
    # возвращает dict (заданной категории categ) ДС с ключами 'Code' со списком фото
    dict_categ = {}
    img_ = requests.post(
        'https://api.dclink.com.ua/api/GetPicturesUrlByCategory', data={
            'login': DC_LOGIN,
            'password': DC_PASSWORD,
             'category': categ
        })
    root = etree.fromstring(img_.content)
    list_elements = root.getchildren()

    for elem_ in list_elements:
        elem = elem_.getchildren()
        if isinstance(elem, list):
            try:
                dict_categ[elem[0].text].append(elem[1].text)
            except KeyError:
                try:
                    dict_categ[elem[0].text] = [elem[1].text]
                except:
                    continue
    return dict_categ


def get_from_xml(xml, DC_LOGIN, DC_PASSWORD, ff=True, periphery=False):
    # скачиваем с DC товары с баз описаниями для осн категорий или
    # периферию(periphery=True) с ссылками на фото

    category_main = (
    '8', '3', '724', '1', '9', '27', '2', '23', '6',
    )

    category_periphery = (
    '11', '24', '33', '56', '125', '1410', '125', '5', '255',
    '45', '54', '648', '125', '968', '1376', '25', '970', '31',
    )

    category = category_periphery if periphery else category_main

    dict_category_periphery = dict()
    dict_category_foto = dict()

    for cat in category:
        discr2_row = requests.post(
        'https://api.dclink.com.ua/api/GetItemPropertiesByCategory', data={
            'login': DC_LOGIN,
            'password': DC_PASSWORD,
            'category': cat
        })
        data = discr2_row.json()
        dict_category_periphery[cat] = data
        dict_category_foto[cat] = get_foto_list(cat, DC_LOGIN, DC_PASSWORD)

    url_item = 'https://opt.dclink.com.ua/item.htm?id='

    try:
        root = etree.fromstring(xml)
    except:
        print('Wrong  data')
        return []

    l=root.getchildren()
    list_soup_dict=[]
    for x in l:
        d={}
        for y in x.getchildren():
            if not y.text:
                d[y.tag] = 'None'
            else:
                d[y.tag] = y.text
        if d['Code']:
            d['Url'] = url_item + d['Code']
        else:
            d['Url'] = ''
        if ff:
            if d['CategoryID'] in category:
                list_soup_dict.append(d)
        else:
            list_soup_dict.append(d)
            #if d['Article'] in ff: list_soup_dict.append(d)
        #else:
            #list_soup_dict.append(d)

    return (list_soup_dict, dict_category_periphery, dict_category_foto)

def from_file_get_part(filename, periphery=False):

    category_main = (
    '8', '3', '724', '1', '9', '27', '2', '23', '6',
    )

    category_periphery = (
    '11', '24', '33', '56', '125', '1410', '125', '5', '255',
    '45', '54', '648', '125', '968', '1376', '25', '970', '31',
    )

    category = category_periphery if periphery else category_main

    with open(filename, 'rb') as fobj:
        xml = fobj.read()

    try:
        root = etree.fromstring(xml)
    except:
        print('Wrong  data')
        return []

    l=root.getchildren()
    dict_res={}
    for x in l:
        d={}
        for y in x.getchildren():
            if not y.text:
                d[y.tag] = 'None'
            else:
                d[y.tag] = y.text
        if d['Code']:
            url_item = 'https://opt.dclink.com.ua/item.htm?id='
            d['Url'] = url_item + d['Code']
        else:
            d['Url'] = ''
        if d['CategoryID'] in category:
            dict_res[d['Article']] = d

    return dict_res

def get_price_rent_price_ua(price_rent, price_ua):
    # считает процент для колонки get_price_rent в бд
    # раньше в моделях была как функция - аналог действия

    try:
        temp = round((price_rent / price_ua - 1) * 100)
        temp = temp if temp > 0 else 0
        return temp
    except:
        return 0

def label_auto_edited(obj, bool_, label_='recommend'):
    # добавляем/удаляем ярлык если товар (obj) есть/нету на складе,
    # bool_ - булево есть/нету на складе

    str_ = obj.label
    str_ = str_.lower().strip() if str_ else ''
    if bool_:
        if str_.find(label_) == -1:
            if str_:
                obj.label = f'{obj.label}, {label_}'
            else:
                obj.label = label_
            obj.save()
    else:
        if str_.find(label_) != -1:
            obj.label = re.sub(
            f', {label_}|,{label_}|{label_},|{label_}', '', str_
            ).strip()
            obj.save()

def min_price_another(obj_full, obj):
    #принимает партс_фулл_обж, выдет имя поставщика с мин ценой и саму цену + rrp
    # (рекомендов-ю цену)

    # новое: фун в provider добавляет цену со склада если есть
    # еще новее: принимет еще и obj для редактирования obj.label в label_auto_edited

    try:
        rrp = round(obj_full.rrprice_parts) # округляем только rrprice_parts
    except:
        rrp = 0

    if obj_full.name_parts_main != 'склад' and not obj_full.remainder:
        label_auto_edited(obj, False)
        return (obj_full.name_parts_main, obj_full.providerprice_parts,
               rrp)

    label_auto_edited(obj, True)

    try:
        #выделяем цену из "price:1649.08; 2"
        stock_price = round(
        float(re.findall(r':(.+);', obj_full.remainder)[0])
        )
    except:
        stock_price = 1000000


    if stock_price <= obj_full.providerprice_parts:
        return (f'{stock_price}; склад', stock_price, 0)

    if stock_price != 1000000 and stock_price > obj_full.providerprice_parts:
        return (f'{stock_price}; {obj_full.name_parts_main}', stock_price, 0)

    return (obj_full.name_parts_main, obj_full.providerprice_parts,
            rrp)

def objects_edit(obj, usd_cuurency):
    # singleparts - обновление цен
    if Parts_full.objects.filter(availability_parts='yes',
    partnumber_parts=obj.part_number, providers__name_provider='-',
    providerprice_parts__gt=0, name_parts_main__isnull=False).exists():
        full = Parts_full.objects.filter(
        partnumber_parts=obj.part_number, providers__name_provider='-',
        providerprice_parts__gt=0).first()
        provider_, temp_price, rrp = min_price_another(full, obj)
        #temp_price = full.providerprice_parts
        try:
            temp_rentability = 1 + (obj.rentability / 100)
        except:
            temp_rentability = 1.15
        label_active = True # механизм для auto
        if obj.auto == True:
            # если ручная цена: price_rent не трогаем, остальное меняем согласно прайсу
            if obj.r_price < (temp_price * usd_cuurency):
                obj.is_active = False
                label_active = False
            obj.price_ua = round(temp_price * usd_cuurency)
            obj.price_usd = round(temp_price)
            obj.provider = provider_ #full.name_parts_main
            obj.rrp_price = rrp
            obj.is_active = True if label_active else False
            #obj.get_price_rent =\
            #get_price_rent_price_ua(obj.price_rent, obj.price_ua) # для нов колонки %
            obj.save()
        elif obj.r_price > (temp_price * usd_cuurency):
            obj.price_ua = round(temp_price * usd_cuurency)
            obj.price_usd = round(temp_price)
            obj.price_rent = round(temp_price * usd_cuurency * temp_rentability)
            obj.provider = provider_ #full.name_parts_main
            obj.rrp_price = rrp
            obj.is_active = True
            #obj.get_price_rent =\
            #get_price_rent_price_ua(obj.price_rent, obj.price_ua) # для нов колонки %
            obj.save()
        else:
            obj.price_ua = round(temp_price * usd_cuurency)
            obj.price_usd = round(temp_price)
            obj.price_rent = round(temp_price * usd_cuurency * temp_rentability)
            obj.provider = provider_ #full.name_parts_main
            obj.rrp_price = rrp
            obj.is_active = False
            #obj.get_price_rent =\
            #get_price_rent_price_ua(obj.price_rent, obj.price_ua) # для нов колонки %
            obj.save()
    else:
        if obj.auto == True:
            # если ручная цена: price_rent не трогаем, остальное меняем согласно прайсу
            obj.price_ua = 0
            obj.price_usd = 0
            obj.provider = 'нет'
            obj.rrp_price = 0
            obj.is_active = False
            #obj.get_price_rent = 0
            #obj.get_price_rent =\
            #get_price_rent_price_ua(obj.price_rent, obj.price_ua) # для нов колонки %
            obj.save()
        else:
            obj.is_active = False
            obj.price_ua = 0
            obj.price_usd = 0
            obj.price_rent = 0
            obj.provider = 'нет'
            obj.rrp_price = 0
            #obj.get_price_rent = 0
            #obj.get_price_rent =\
            #get_price_rent_price_ua(obj.price_rent, obj.price_ua) # для нов колонки %
            obj.save()

def objects_edit_multi(obj, usd_cuurency):
    # отличается от objects_edit работой с мульти партнамберами (obj.tags ниже)

    if obj.tags.exists():
        for q in obj.tags.all():
            objects_edit(q, usd_cuurency)
        queryset_ = obj.tags.filter(is_active=True).order_by('price_usd')
        if queryset_.exists():
            query = queryset_.first()
            obj.price_usd = query.price_usd
            obj.price_ua = query.price_ua
            obj.price_rent = query.price_rent
            obj.provider = query.provider
            obj.rrp_price = query.rrp_price
            obj.part_number = f'{query.part_number}_'
            obj.is_active = True
            #obj.get_price_rent =\
            #get_price_rent_price_ua(obj.price_rent, obj.price_ua) # для нов колонки %
            obj.save()
        else:
            obj.is_active = False
            obj.price_ua = 0
            obj.price_usd = 0
            obj.price_rent = 0
            obj.provider = 'нет'
            obj.rrp_price = 0
            #obj.get_price_rent = 0
            #obj.get_price_rent =\
            #get_price_rent_price_ua(obj.price_rent, obj.price_ua) # для нов колонки %
            obj.save()
        return True
    if Parts_full.objects.filter(availability_parts='yes',
    partnumber_parts=obj.part_number, providers__name_provider='-',
    providerprice_parts__gt=0, name_parts_main__isnull=False).exists():
        full = Parts_full.objects.filter(
        partnumber_parts=obj.part_number, providers__name_provider='-',
        providerprice_parts__gt=0).first()
        provider_, temp_price, rrp = min_price_another(full, obj)
        #temp_price = full.providerprice_parts
        try:
            temp_rentability = 1 + (obj.rentability / 100)
        except:
            temp_rentability = 1.05
        label_active = True # механизм для auto
        if obj.auto == True:
            # если ручная цена: price_rent не трогаем, остальное меняем согласно прайсу
            if obj.r_price < (temp_price * usd_cuurency):
                obj.is_active = False
                label_active = False
            obj.price_ua = round(temp_price * usd_cuurency)
            obj.price_usd = round(temp_price)
            obj.provider = provider_ #full.name_parts_main
            obj.rrp_price = rrp
            obj.is_active = True if label_active else False
            #obj.get_price_rent =\
            #get_price_rent_price_ua(obj.price_rent, obj.price_ua) # для нов колонки %
            obj.save()
        elif obj.r_price > (temp_price * usd_cuurency):
            obj.price_ua = round(temp_price * usd_cuurency)
            obj.price_usd = round(temp_price)
            obj.price_rent = round(temp_price * usd_cuurency * temp_rentability)
            obj.provider = provider_ #full.name_parts_main
            obj.rrp_price = rrp
            obj.is_active = True
            #obj.get_price_rent =\
            #get_price_rent_price_ua(obj.price_rent, obj.price_ua) # для нов колонки %
            obj.save()
        else:
            obj.price_ua = round(temp_price * usd_cuurency)
            obj.price_usd = round(temp_price)
            obj.price_rent = round(temp_price * usd_cuurency * temp_rentability)
            obj.provider = provider_ #full.name_parts_main
            obj.rrp_price = rrp
            obj.is_active = False
            #obj.get_price_rent =\
            #get_price_rent_price_ua(obj.price_rent, obj.price_ua) # для нов колонки %
            obj.save()
    else:
        if obj.auto == True:
            # если ручная цена: price_rent не трогаем, остальное меняем согласно прайсу
            obj.price_ua = 0
            obj.price_usd = 0
            obj.provider = 'нет'
            obj.rrp_price = 0
            obj.is_active = False
            #obj.get_price_rent = 0
            #obj.get_price_rent =\
            #get_price_rent_price_ua(obj.price_rent, obj.price_ua) # для нов колонки %
            obj.save()
        else:
            obj.is_active = False
            obj.price_ua = 0
            obj.price_usd = 0
            obj.price_rent = 0
            obj.provider = 'нет'
            obj.rrp_price = 0
            #obj.get_price_rent = 0
            #obj.get_price_rent =\
            #get_price_rent_price_ua(obj.price_rent, obj.price_ua) # для нов колонки %
            obj.save()

def objects_tech_edit(obj, usd_cuurency, dc_dict, prov='dc'):
    #  для tech обьектов dc_dict с партнамберами в ключах
    # редактируем цену, наличие, вкл/выкл и тд to_tech_price_from_dc

    # работa с мульти партнамберами (obj.tags ниже)
    if obj.tags.exists():
        for q in obj.tags.all():
            objects_tech_edit(q, usd_cuurency, dc_dict)
        queryset_ = obj.tags.filter(is_active=True).order_by('price_usd')
        if queryset_.exists():
            query = queryset_.first()
            obj.price_usd = query.price_usd
            obj.price_ua = query.price_ua
            obj.price_rent = query.price_rent
            obj.provider = query.provider
            obj.rrp_price = query.rrp_price
            obj.part_number = f'{query.part_number}_'
            obj.is_active = True
            obj.get_price_rent =\
            get_price_rent_price_ua(obj.price_rent, obj.price_ua) # для нов колонки %
            obj.save()
        else:
            obj.is_active = False
            obj.price_ua = 0
            obj.price_usd = 0
            obj.price_rent = 0
            obj.provider = 'нет'
            obj.rrp_price = 0
            obj.get_price_rent = 0 # для нов колонки %
            obj.save()
        return True

    try:
        rrp = float(dc_dict[obj.part_number]['RRP_UAH'])
    except:
        rrp = 0

    stock_price = 0 # для отслеживания склада
    if Parts_full.objects.filter(availability_parts='yes',
    partnumber_parts=obj.part_number, providers__name_provider='-',
    providerprice_parts__gt=0, remainder__isnull=False).exists():
        full = Parts_full.objects.filter(availability_parts='yes',
        partnumber_parts=obj.part_number, providers__name_provider='-',
        providerprice_parts__gt=0, remainder__isnull=False).first()
        try:
            #выделяем цену из "price:1649.08; 2"
            stock_price = round(
            float(re.findall(r':(.+);', full.remainder)[0])
            )
        except:
            stock_price = 0

    if obj.part_number in dc_dict:
        try:
            if stock_price != 0:
                prov = f"{stock_price}; {dc_dict[obj.part_number]['provider']}"
                label_auto_edited(obj, True) # добавляем лабел recommend
            else:
                prov = dc_dict[obj.part_number]['provider']
                label_auto_edited(obj, False) # удаляем(если есть) лабел recommend
            provider_, temp_price = (prov, float(dc_dict[obj.part_number]['PriceUSD']))
        except:
            #print(f"error{obj.part_number}---{dc_dict[obj.part_number]['provider']}")
            provider_, temp_price = ('error', 0)

        if stock_price and stock_price <= temp_price:
            provider_, temp_price, rrp =  (f'{stock_price}; склад', stock_price, 0)

        try:
            temp_rentability = 1 + (obj.rentability / 100)
        except:
            temp_rentability = 1.15
        label_active = True # механизм для auto
        if obj.auto == True:
            # если ручная цена: price_rent не трогаем, остальное меняем согласно прайсу
            if obj.r_price < (temp_price * usd_cuurency):
                obj.is_active = False
                label_active = False
            obj.price_ua = round(temp_price * usd_cuurency)
            obj.price_usd = round(temp_price)
            obj.provider = provider_ #full.name_parts_main
            obj.rrp_price = rrp
            obj.is_active = True if label_active else False
            obj.get_price_rent =\
            get_price_rent_price_ua(obj.price_rent, obj.price_ua) # для нов колонки %
            obj.save()
        elif obj.r_price > (temp_price * usd_cuurency):
            obj.price_ua = round(temp_price * usd_cuurency)
            obj.price_usd = round(temp_price)
            obj.price_rent = round(temp_price * usd_cuurency * temp_rentability)
            obj.provider = provider_ #full.name_parts_main
            obj.rrp_price = rrp
            obj.is_active = True
            obj.get_price_rent =\
            get_price_rent_price_ua(obj.price_rent, obj.price_ua) # для нов колонки %
            obj.save()
        else:
            obj.price_ua = round(temp_price * usd_cuurency)
            obj.price_usd = round(temp_price)
            obj.price_rent = round(temp_price * usd_cuurency * temp_rentability)
            obj.provider = provider_ #full.name_parts_main
            obj.rrp_price = rrp
            obj.is_active = False
            obj.get_price_rent =\
            get_price_rent_price_ua(obj.price_rent, obj.price_ua) # для нов колонки %
            obj.save()
    else:
        if stock_price:
            label_auto_edited(obj, True) # добавляем лабел recommend
            try:
                temp_rentability = 1 + (obj.rentability / 100)
            except:
                temp_rentability = 1.15
            active = True
            if obj.r_price < (stock_price * usd_cuurency):
                active = False
            if obj.auto == True:
                # если ручная цена: price_rent не трогаем, остальное меняем согласно прайсу
                obj.price_ua = round(stock_price * usd_cuurency)
                obj.price_usd = round(stock_price)
                obj.provider = f'{stock_price}; склад'
                obj.rrp_price = 0
                obj.is_active = True if active else False
                obj.get_price_rent =\
                get_price_rent_price_ua(obj.price_rent, obj.price_ua) # для нов колонки %
                obj.save()
            else:
                obj.is_active = True if active else False
                obj.price_ua = round(stock_price * usd_cuurency)
                obj.price_usd = round(stock_price)
                obj.price_rent = round(stock_price * usd_cuurency * temp_rentability)
                obj.provider = f'{stock_price}; склад'
                obj.rrp_price = 0
                obj.get_price_rent =\
                get_price_rent_price_ua(obj.price_rent, obj.price_ua) # для нов колонки %
                obj.save()
        else:
            label_auto_edited(obj, False) # удаляем(если есть) лабел recommend
            if obj.auto == True:
                # если ручная цена: price_rent не трогаем, остальное меняем согласно прайсу
                obj.price_ua = 0
                obj.price_usd = 0
                obj.provider = 'нет'
                obj.rrp_price = 0
                obj.is_active = False
                obj.get_price_rent = 0 # для нов колонки %
                obj.save()
            else:
                obj.is_active = False
                obj.price_ua = 0
                obj.price_usd = 0
                obj.price_rent = 0
                obj.provider = 'нет'
                obj.rrp_price = 0
                obj.get_price_rent = 0 # для нов колонки %
                obj.save()

def to_model_price_from_dc():
    usd = USD.objects.last()
    usd_cuurency = usd.usd if usd else 37
    for obj in CPU_OTHER.objects.all():
        objects_edit_multi(obj, usd_cuurency)
    for obj in Cooler_OTHER.objects.all():
        objects_edit_multi(obj, usd_cuurency)
    for obj in MB_OTHER.objects.all():
        objects_edit_multi(obj, usd_cuurency)
    for obj in RAM_OTHER.objects.all():
        objects_edit_multi(obj, usd_cuurency)
    for obj in HDD_OTHER.objects.all():
        objects_edit_multi(obj, usd_cuurency)
    for obj in PSU_OTHER.objects.all():
        objects_edit_multi(obj, usd_cuurency)
    for obj in GPU_OTHER.objects.all():
        objects_edit_multi(obj, usd_cuurency)
    for obj in FAN_OTHER.objects.all():
        objects_edit_multi(obj, usd_cuurency)
    for obj in CASE_OTHER.objects.all():
        objects_edit_multi(obj, usd_cuurency)
    for obj in SSD_OTHER.objects.all():
        objects_edit_multi(obj, usd_cuurency)
    #for obj in WiFi_OTHER.objects.all():
    #    objects_edit_multi(obj, usd_cuurency)
    #for obj in Cables_OTHER.objects.all():
    #    objects_edit_multi(obj, usd_cuurency)
    #for obj in Soft_OTHER.objects.all():
    #    objects_edit_multi(obj, usd_cuurency)

def test_tech():
    # только для теста, временная ф
    count_dc = 0
    category_periphery = (
    '11', '24', '33', '56', '125', '1410', '125', '5', '255',
    '45', '54', '648', '125', '968', '1376', '25',
    )
    status_ = {'*****':'yes','****':'yes','***':'yes','**':'yes','*':'yes'}

    with open('load_form_providers/dclink-price.xml', 'rb') as fobj:
        xml = fobj.read()
    try:
        root = etree.fromstring(xml)
    except:
        print('Wrong  data')
        return []

    l=root.getchildren()
    dc_dict = dict()
    for x in l:
        d={}
        try:
            for y in x.getchildren():
                if not y.text:
                    d[y.tag] = 'None'
                else:
                    d[y.tag] = y.text
            d['provider'] = 'dc'
            if d['CategoryID'] in category_periphery and d['Availability'] in status_:
                count_dc += 1
                if not d['CategoryID'] in dc_dict:
                    dc_dict[d['CategoryID']] = {d['Article']: d}
                else:
                    dc_dict[d['CategoryID']][d['Article']] = d
        except Exception as e:
            print(e)
            break
    return dc_dict

def to_tech_price_from_dc(for_brain=None):
    # из счанного файла ДС создаем словарь {'CategoryID': {'part_number': {data}, ...}, ...}
    # в objects_tech_edit кроме прочего передаем {'part_number': {data}, ...}
    usd = USD.objects.last()
    usd_cuurency = usd.usd if usd else 37
    count_dc = 0

    category_periphery = (
    '11', '24', '33', '56', '125', '1410', '125', '5', '255',
    '45', '54', '648', '125', '968', '1376', '25', '970', '31',
    )
    status_ = {'*****':'yes','****':'yes','***':'yes','**':'yes','*':'yes'}

    with open('load_form_providers/dclink-price.xml', 'rb') as fobj:
        xml = fobj.read()
    try:
        root = etree.fromstring(xml)
    except:
        print('Wrong  data')
        if not Results.objects.filter(who='tech').exists():
            r = Results(who='tech',
            who_desc='dc file error')
            r.save()
        else:
            r = Results.objects.get(who='tech')
            r.who_desc = 'dc file error'
            r.save()
        return []

    l=root.getchildren()
    dc_dict = dict()
    for x in l:
        d={}
        try:
            for y in x.getchildren():
                if not y.text:
                    d[y.tag] = 'None'
                else:
                    d[y.tag] = y.text
            d['provider'] = 'dc'
            if d['CategoryID'] in category_periphery and d['Availability'] in status_:
                count_dc += 1
                if not d['CategoryID'] in dc_dict:
                    dc_dict[d['CategoryID']] = {d['Article']: d}
                else:
                    dc_dict[d['CategoryID']][d['Article']] = d
        except:
            print('error but next')

    partnums_tech = list(Monitors.objects.all().values_list('part_number',flat=True))
    partnums_tech += list(KM.objects.all().values_list('part_number',flat=True))
    partnums_tech += list(Keyboards.objects.all().values_list('part_number',flat=True))
    partnums_tech += list(Mouses.objects.all().values_list('part_number',flat=True))
    partnums_tech += list(Pads.objects.all().values_list('part_number',flat=True))
    partnums_tech += list(Headsets.objects.all().values_list('part_number',flat=True))
    partnums_tech += list(Webcams.objects.all().values_list('part_number',flat=True))
    partnums_tech += list(WiFis.objects.all().values_list('part_number',flat=True))
    partnums_tech += list(Acoustics.objects.all().values_list('part_number',flat=True))
    partnums_tech += list(Tables.objects.all().values_list('part_number',flat=True))
    partnums_tech += list(Chairs.objects.all().values_list('part_number',flat=True))
    partnums_tech += list(Cabelsplus.objects.all().values_list('part_number',flat=True))
    partnums_tech += list(Filters.objects.all().values_list('part_number',flat=True))
    partnums_tech += list(Mike.objects.all().values_list('part_number',flat=True))
    #partnums_tech += list(NB.objects.all().values_list('part_number',flat=True))

    f = From_provders_filePrices(partnums_tech, dc_dict, usd_cuurency)
    if for_brain:
        brain = f.from_brain(for_brain)
        print(brain)
    else:
        brain = f.from_brain('load_form_providers/brain-price.json')
        print(brain)
    edg = f.from_edg('load_form_providers/edg-price.xml')
    print(edg)
    elko = f.from_elko('load_form_providers/elko-price.json')
    print(elko)
    mti = f.from_mti('load_form_providers/mti_price.xml')
    print(mti)
    brain = f.from_brain('load_form_providers/brain-price.json')
    print(brain)
    edg = f.from_edg('load_form_providers/edg-price.xml')
    print(edg)
    eletek = f.from_eletek('https://www.eletek.ua/ru/pricelist-distry-versum.xml')
    print(eletek)

    if not Results.objects.filter(who='tech').exists():
        r = Results(who='tech',
        who_desc=f'brain: {brain}, edg: {edg}, elko: {elko}, mti: {mti}, eletek: {eletek}, dc: {count_dc}')
        r.save()
    else:
        r = Results.objects.get(who='tech')
        r.who_desc = f'brain: {brain}, edg: {edg}, elko: {elko}, mti: {mti}, eletek: {eletek}, dc: {count_dc}'
        r.save()

    for obj in Monitors.objects.all():
        if '5' in dc_dict:
            objects_tech_edit(obj, usd_cuurency, dc_dict['5'])
    for obj in KM.objects.all():
        if '968' in dc_dict:
            objects_tech_edit(obj, usd_cuurency, dc_dict['968'])
    for obj in Keyboards.objects.all():
        if '33' in dc_dict:
            objects_tech_edit(obj, usd_cuurency, dc_dict['33'])
    for obj in Mouses.objects.all():
        if '11' in dc_dict:
            objects_tech_edit(obj, usd_cuurency, dc_dict['11'])
    for obj in Pads.objects.all():
        if '24' in dc_dict:
            objects_tech_edit(obj, usd_cuurency, dc_dict['24'])
    for obj in Headsets.objects.all():
        if '56' in dc_dict:
            objects_tech_edit(obj, usd_cuurency, dc_dict['56'])
    for obj in Webcams.objects.all():
        if '54' in dc_dict:
            objects_tech_edit(obj, usd_cuurency, dc_dict['54'])
    for obj in WiFis.objects.all():
        if '1410' in dc_dict:
            objects_tech_edit(obj, usd_cuurency, dc_dict['1410'])
    for obj in Acoustics.objects.all():
        if '25' in dc_dict:
            objects_tech_edit(obj, usd_cuurency, dc_dict['25'])
    for obj in Tables.objects.all():
        if '1376' in dc_dict:
            objects_tech_edit(obj, usd_cuurency, dc_dict['1376'])
    for obj in Chairs.objects.all():
        if '125' in dc_dict:
            objects_tech_edit(obj, usd_cuurency, dc_dict['125'])
    for obj in Cabelsplus.objects.all():
        if '648' in dc_dict:
            objects_tech_edit(obj, usd_cuurency, dc_dict['648'])
    for obj in Filters.objects.all():
        if '45' in dc_dict:
            objects_tech_edit(obj, usd_cuurency, dc_dict['45'])
    for obj in Mike.objects.all():
        if '970' in dc_dict:
            objects_tech_edit(obj, usd_cuurency, dc_dict['970'])
    """for obj in NB.objects.all():
        if '31' in dc_dict:
            objects_tech_edit(obj, usd_cuurency, dc_dict['31'])"""

# словарь tech_ для работы с from_price_new_tech_per_kind
# lambda для отложенного вызова функций с еще несформированными словарми,
# являющимися аргументами функции
tech_ = {
'mon': (
        lambda d1, d2, d3, f=newMonitor: f(d1, d2, d3),
        '5',
        Monitors.objects.all().values_list('part_number', flat=True),
        ),
'km': (
        lambda d1, d2, d3, f=newKM: f(d1, d2, d3),
        '968',
        KM.objects.all().values_list('part_number', flat=True),
        ),
'kb': (
        lambda d1, d2, d3, f=newKeyboards: f(d1, d2, d3),
        '33',
        Keyboards.objects.all().values_list('part_number', flat=True),
        ),
'mouse': (
        lambda d1, d2, d3, f=newMouses: f(d1, d2, d3),
        '11',
        Mouses.objects.all().values_list('part_number', flat=True),
        ),
'pad': (
        lambda d1, d2, d3, f=newPads: f(d1, d2, d3),
        '24',
        Pads.objects.all().values_list('part_number', flat=True),
        ),
'head': (
        lambda d1, d2, d3, f=newHeadsets: f(d1, d2, d3),
        '56',
        Headsets.objects.all().values_list('part_number', flat=True),
        ),
'web': (
        lambda d1, d2, d3, f=newWebcams: f(d1, d2, d3),
        '54',
        Webcams.objects.all().values_list('part_number', flat=True),
        ),
'wifi': (
        lambda d1, d2, d3, f=newWiFis: f(d1, d2, d3),
        '1410',
        WiFis.objects.all().values_list('part_number', flat=True),
        ),
'acust': (
        lambda d1, d2, d3, f=newAcoustics: f(d1, d2, d3),
        '25',
        Acoustics.objects.all().values_list('part_number', flat=True),
        ),
'tab': (
        lambda d1, d2, d3, f=newTables: f(d1, d2, d3),
        '1376',
        Tables.objects.all().values_list('part_number', flat=True),
        ),
'chair': (
        lambda d1, d2, d3, f=newChairs: f(d1, d2, d3),
        '125',
        Chairs.objects.all().values_list('part_number', flat=True),
        ),
'cab': (
        lambda d1, d2, d3, f=newCabelsplus: f(d1, d2, d3),
        '648',
        Cabelsplus.objects.all().values_list('part_number', flat=True),
        ),
'filter': (
        lambda d1, d2, d3, f=newFilters: f(d1, d2, d3),
        '45',
        Filters.objects.all().values_list('part_number', flat=True),
        ),
'mike': (
        lambda d1, d2, d3, f=newMike: f(d1, d2, d3),
        '970',
        Filters.objects.all().values_list('part_number', flat=True),
        ),
}


def from_price_new_tech_per_kind(kind_tech):
    """
    находим новые детали по конкретной категориям tech (kind_tech='mon', ...)
    """

    category_periphery = (
    '11', '24', '33', '56', '125', '1410', '125', '5', '255',
    '45', '54', '648', '125', '968', '1376', '25', '970',
    )

    with open('load_form_providers/dclink-price.xml', 'rb') as fobj:
        xml = fobj.read()

    DC_LOGIN = 'itblok'
    DC_PASSWORD = 'VIA5qPUv'
    list_periphery, dict_category_periphery, dict_category_foto = get_from_xml(
    xml, DC_LOGIN, DC_PASSWORD, periphery=True) # исп-ем для получения описаний

    try:
        root = etree.fromstring(xml)
    except:
        print('Wrong  data')
        return []

    l=root.getchildren()
    dc_dict = dict()
    for x in l:
        d={}
        try:
            for y in x.getchildren():
                if not y.text:
                    d[y.tag] = 'None'
                else:
                    d[y.tag] = y.text
            if d['CategoryID'] in category_periphery:
                if not d['CategoryID'] in dc_dict:
                    dc_dict[d['CategoryID']] = {d['Article']: d}
                else:
                    dc_dict[d['CategoryID']][d['Article']] = d
        except:
            print('error but next')
    try:
        dict_set = set(dc_dict[tech_[kind_tech][1]].keys()) #dc_dict['5'] для "mon"
    except:
        dict_set = set()
    q_set = set(tech_[kind_tech][2])
    res = dict_set - q_set
    res_list_dict = [
    {'name_parts': x,
    'partnumber_parts': dc_dict[tech_[kind_tech][1]][x]['Name']} for x in res
    ]
    for_result = json.dumps(res_list_dict,
    ensure_ascii=False)
    r, _ = Results.objects.get_or_create(who=f'{kind_tech}_dc')
    r.json_data = for_result
    r.save()
    for key in res:
        tech_[kind_tech][0](dict_category_periphery,
        dc_dict[tech_[kind_tech][1]][key],
        dict_category_foto,
        )
        # берем например newMonitor из tech_ и вставляем 3 словаря в ( ) как параметры
        # функции newMonitor(), аналог отдельной кат-ии из from_price_get_new_tech,
        # смотри там как работает, здесь тоже но с отложенным вызовом с lambda



def from_price_get_new_tech(prov):
    """ находим новые детали по категориям tech (prov=dc) """

    category_periphery = (
    '11', '24', '33', '56', '125', '1410', '125', '5', '255',
    '45', '54', '648', '125', '968', '1376', '25', '970',
    )

    with open('load_form_providers/dclink-price.xml', 'rb') as fobj:
        xml = fobj.read()

    DC_LOGIN = 'itblok'
    DC_PASSWORD = 'VIA5qPUv'
    list_periphery, dict_category_periphery, dict_category_foto = get_from_xml(
    xml, DC_LOGIN, DC_PASSWORD, periphery=True) # исп-ем для получения описаний

    try:
        root = etree.fromstring(xml)
    except:
        print('Wrong  data')
        return []

    l=root.getchildren()
    dc_dict = dict()
    for x in l:
        d={}
        try:
            for y in x.getchildren():
                if not y.text:
                    d[y.tag] = 'None'
                else:
                    d[y.tag] = y.text
            if d['CategoryID'] in category_periphery:
                if not d['CategoryID'] in dc_dict:
                    dc_dict[d['CategoryID']] = {d['Article']: d}
                else:
                    dc_dict[d['CategoryID']][d['Article']] = d
        except:
            print('error but next')

    try:
        dict_set = set(dc_dict['970'].keys())
    except:
        dict_set = set()
    q_set = set(Mike.objects.all().values_list('part_number', flat=True))
    res = dict_set - q_set
    res_list_dict = [
    {'name_parts': x, 'partnumber_parts': dc_dict['970'][x]['Name']} for x in res
    ]
    for_result = json.dumps(res_list_dict,
    ensure_ascii=False)
    r, _ = Results.objects.get_or_create(who=f'mike_{prov}')
    r.json_data = for_result
    r.save()
    for key in res:
        newMike(dict_category_periphery, dc_dict['970'][key], dict_category_foto)

    try:
        dict_set = set(dc_dict['5'].keys())
    except:
        dict_set = set()
    q_set = set(Monitors.objects.all().values_list('part_number', flat=True))
    res = dict_set - q_set
    res_list_dict = [
    {'name_parts': x, 'partnumber_parts': dc_dict['5'][x]['Name']} for x in res
    ]
    for_result = json.dumps(res_list_dict,
    ensure_ascii=False)
    r, _ = Results.objects.get_or_create(who=f'mon_{prov}')
    r.json_data = for_result
    r.save()
    for key in res:
        newMonitor(dict_category_periphery, dc_dict['5'][key], dict_category_foto)

    try:
        dict_set = set(dc_dict['968'].keys())
    except:
        dict_set = set()
    q_set = set(KM.objects.all().values_list('part_number', flat=True))
    res = dict_set - q_set
    res_list_dict = [{'name_parts': x, 'partnumber_parts': dc_dict['968'][x]['Name']} for x in res]
    for_result = json.dumps(res_list_dict,
    ensure_ascii=False)
    r, _ = Results.objects.get_or_create(who=f'km_{prov}')
    r.json_data = for_result
    r.save()
    for key in res:
        newKM(dict_category_periphery, dc_dict['968'][key], dict_category_foto)

    try:
        dict_set = set(dc_dict['33'].keys())
    except:
        dict_set = set()
    q_set = set(Keyboards.objects.all().values_list('part_number', flat=True))
    res = dict_set - q_set
    res_list_dict = [{'name_parts': x, 'partnumber_parts': dc_dict['33'][x]['Name']} for x in res]
    for_result = json.dumps(res_list_dict,
    ensure_ascii=False)
    r, _ = Results.objects.get_or_create(who=f'kbrd_{prov}')
    r.json_data = for_result
    r.save()
    for key in res:
        newKeyboards(dict_category_periphery, dc_dict['33'][key], dict_category_foto)

    try:
        dict_set = set(dc_dict['11'].keys())
    except:
        dict_set = set()
    q_set = set(Mouses.objects.all().values_list('part_number', flat=True))
    res = dict_set - q_set
    res_list_dict = [{'name_parts': x, 'partnumber_parts': dc_dict['11'][x]['Name']} for x in res]
    for_result = json.dumps(res_list_dict,
    ensure_ascii=False)
    r, _ = Results.objects.get_or_create(who=f'mouse_{prov}')
    r.json_data = for_result
    r.save()
    for key in res:
        newMouses(dict_category_periphery, dc_dict['11'][key], dict_category_foto)

    try:
        dict_set = set(dc_dict['24'].keys())
    except:
        dict_set = set()
    q_set = set(Pads.objects.all().values_list('part_number', flat=True))
    res = dict_set - q_set
    res_list_dict = [{'name_parts': x, 'partnumber_parts': dc_dict['24'][x]['Name']} for x in res]
    for_result = json.dumps(res_list_dict,
    ensure_ascii=False)
    r, _ = Results.objects.get_or_create(who=f'pads_{prov}')
    r.json_data = for_result
    r.save()
    for key in res:
        newPads(dict_category_periphery, dc_dict['24'][key], dict_category_foto)

    try:
        dict_set = set(dc_dict['56'].keys())
    except:
        dict_set = set()
    q_set = set(Headsets.objects.all().values_list('part_number', flat=True))
    res = dict_set - q_set
    res_list_dict = [{'name_parts': x, 'partnumber_parts': dc_dict['56'][x]['Name']} for x in res]
    for_result = json.dumps(res_list_dict,
    ensure_ascii=False)
    r, _ = Results.objects.get_or_create(who=f'headsts_{prov}')
    r.json_data = for_result
    r.save()
    for key in res:
        newHeadsets(dict_category_periphery, dc_dict['56'][key], dict_category_foto)

    try:
        dict_set = set(dc_dict['54'].keys())
    except:
        dict_set = set()
    q_set = set(Webcams.objects.all().values_list('part_number', flat=True))
    res = dict_set - q_set
    res_list_dict = [{'name_parts': x, 'partnumber_parts': dc_dict['54'][x]['Name']} for x in res]
    for_result = json.dumps(res_list_dict,
    ensure_ascii=False)
    r, _ = Results.objects.get_or_create(who=f'webcms_{prov}')
    r.json_data = for_result
    r.save()
    for key in res:
        newWebcams(dict_category_periphery, dc_dict['54'][key], dict_category_foto)

    try:
        dict_set = set(dc_dict['1410'].keys())
    except:
        dict_set = set()
    q_set = set(WiFis.objects.all().values_list('part_number', flat=True))
    res = dict_set - q_set
    res_list_dict = [{'name_parts': x, 'partnumber_parts': dc_dict['1410'][x]['Name']} for x in res]
    for_result = json.dumps(res_list_dict,
    ensure_ascii=False)
    r, _ = Results.objects.get_or_create(who=f'wifi_{prov}')
    r.json_data = for_result
    r.save()
    for key in res:
        newWiFis(dict_category_periphery, dc_dict['1410'][key], dict_category_foto)

    try:
        dict_set = set(dc_dict['1420'].keys())
    except:
        dict_set = set()
    q_set = set(Acoustics.objects.all().values_list('part_number', flat=True))
    res = dict_set - q_set
    res_list_dict = [{'name_parts': x, 'partnumber_parts': dc_dict['1420'][x]['Name']} for x in res]
    for_result = json.dumps(res_list_dict,
    ensure_ascii=False)
    r, _ = Results.objects.get_or_create(who=f'acust_{prov}')
    r.json_data = for_result
    r.save()
    for key in res:
        newAcoustics(dict_category_periphery, dc_dict['1420'][key], dict_category_foto)

    try:
        dict_set = set(dc_dict['1376'].keys())
    except:
        dict_set = set()
    q_set = set(Tables.objects.all().values_list('part_number', flat=True))
    res = dict_set - q_set
    res_list_dict = [{'name_parts': x, 'partnumber_parts': dc_dict['1376'][x]['Name']} for x in res]
    for_result = json.dumps(res_list_dict,
    ensure_ascii=False)
    r, _ = Results.objects.get_or_create(who=f'table_{prov}')
    r.json_data = for_result
    r.save()
    for key in res:
        newTables(dict_category_periphery, dc_dict['1376'][key], dict_category_foto)

    try:
        dict_set = set(dc_dict['125'].keys())
    except:
        dict_set = set()
    q_set = set(Chairs.objects.all().values_list('part_number', flat=True))
    res = dict_set - q_set
    res_list_dict = [{'name_parts': x, 'partnumber_parts': dc_dict['125'][x]['Name']} for x in res]
    for_result = json.dumps(res_list_dict,
    ensure_ascii=False)
    r, _ = Results.objects.get_or_create(who=f'chairs_{prov}')
    r.json_data = for_result
    r.save()
    for key in res:
        newChairs(dict_category_periphery, dc_dict['125'][key], dict_category_foto)

    try:
        dict_set = set(dc_dict['648'].keys())
    except:
        dict_set = set()
    q_set = set(Cabelsplus.objects.all().values_list('part_number', flat=True))
    res = dict_set - q_set
    res_list_dict = [{'name_parts': x, 'partnumber_parts': dc_dict['648'][x]['Name']} for x in res]
    for_result = json.dumps(res_list_dict,
    ensure_ascii=False)
    r, _ = Results.objects.get_or_create(who=f'cabs_{prov}')
    r.json_data = for_result
    r.save()
    for key in res:
        newCabelsplus(dict_category_periphery, dc_dict['648'][key], dict_category_foto)

    try:
        dict_set = set(dc_dict['45'].keys())
    except:
        dict_set = set()
    q_set = set(Filters.objects.all().values_list('part_number', flat=True))
    res = dict_set - q_set
    res_list_dict = [{'name_parts': x, 'partnumber_parts': dc_dict['45'][x]['Name']} for x in res]
    for_result = json.dumps(res_list_dict,
    ensure_ascii=False)
    r, _ = Results.objects.get_or_create(who=f'filters_{prov}')
    r.json_data = for_result
    r.save()
    for key in res:
        newFilters(dict_category_periphery, dc_dict['45'][key], dict_category_foto)


def from_price_get_new_models(prov):
    # находим новые детали по категориям singleparts
    # newWiFi, newCables в планах

    from .dc_descr_adv_single import newCPU, newCASE, newHDD, newPSU, newGPU,\
    newSSD, newRAM, newCooler, newMB, newFAN

    category_main = (
    '8', '3', '724', '1', '9', '27', '2', '23', '6',
    )

    with open('load_form_providers/dclink-price.xml', 'rb') as fobj:
        xml = fobj.read()

    DC_LOGIN = 'itblok'
    DC_PASSWORD = 'VIA5qPUv'
    list_periphery, dict_category_periphery, dict_category_foto = get_from_xml(
    xml, DC_LOGIN, DC_PASSWORD, periphery=False) # исп-ем для получения описаний

    try:
        root = etree.fromstring(xml)
    except:
        print('Wrong  data')
        return []

    l=root.getchildren()
    dc_dict = dict()
    for x in l:
        d={}
        try:
            for y in x.getchildren():
                if not y.text:
                    d[y.tag] = 'None'
                else:
                    d[y.tag] = y.text
            if d['CategoryID'] in category_main:
                if not d['CategoryID'] in dc_dict:
                    dc_dict[d['CategoryID']] = {d['Article']: d}
                else:
                    dc_dict[d['CategoryID']][d['Article']] = d
        except:
            print('error but next')
    try:
        dict_set = set(dc_dict['1'].keys())
    except:
        dict_set = set()
    q_set = set(CPU_OTHER.objects.all().values_list('part_number', flat=True))
    res = dict_set - q_set
    res_list_dict = [
    {'name_parts': x, 'partnumber_parts': dc_dict['1'][x]['Name']} for x in res
    ]
    for_result = json.dumps(res_list_dict,
    ensure_ascii=False)
    r, _ = Results.objects.get_or_create(who=f'cpu_{prov}')
    r.json_data = for_result
    r.save()
    for key in res:
        newCPU(dict_category_periphery, dc_dict['1'][key], dict_category_foto)


    """cpu = CPU_OTHER.objects.all().values_list('part_number', flat=True)
    cpu_set = set(cpu)
    full = Parts_full.objects.filter(providers__name_provider=prov,
    kind__in=('aproc', 'iproc'), availability_parts='yes')
    full_sub_cpu = full.exclude(partnumber_parts__in=cpu_set)
    for_result = json.dumps(list(full_sub_cpu.values('name_parts', 'partnumber_parts')),
    ensure_ascii=False)
    r,_ = Results.objects.get_or_create(who=f'cpu_{prov}')
    r.json_data = for_result
    r.save()"""

    try:
        dict_set = set(dc_dict['23'].keys())
        full = Parts_full.objects.filter(providers__name_provider='dc',
        kind='cool', availability_parts='yes')
         # чтоб отделить вентиляторы от кулеров
        set_price = set(full.values_list('partnumber_parts', flat=True))
        dict_set_inter = dict_set & set_price
    except:
        dict_set_inter = set()
    q_set = set(Cooler_OTHER.objects.all().values_list('part_number', flat=True))
    res = dict_set_inter - q_set
    res_list_dict = [
    {'name_parts': x, 'partnumber_parts': dc_dict['23'][x]['Name']} for x in res
    ]
    for_result = json.dumps(res_list_dict,
    ensure_ascii=False)
    r, _ = Results.objects.get_or_create(who=f'cool_{prov}')
    r.json_data = for_result
    r.save()
    for key in res:
        newCooler(dict_category_periphery, dc_dict['23'][key], dict_category_foto)

    """cool = Cooler_OTHER.objects.all().values_list('part_number', flat=True)
    cool_set = set(cool)
    full = Parts_full.objects.filter(providers__name_provider=prov,
    kind='cool', availability_parts='yes')
    full_sub_cool = full.exclude(partnumber_parts__in=cool_set)
    for_result = json.dumps(list(full_sub_cool.values('name_parts', 'partnumber_parts')),
    ensure_ascii=False)
    r,_ = Results.objects.get_or_create(who=f'cool_{prov}')
    r.json_data = for_result
    r.save()"""

    try:
        dict_set = set(dc_dict['6'].keys())
    except:
        dict_set = set()
    q_set = set(MB_OTHER.objects.all().values_list('part_number', flat=True))
    res = dict_set - q_set
    res_list_dict = [
    {'name_parts': x, 'partnumber_parts': dc_dict['6'][x]['Name']} for x in res
    ]
    for_result = json.dumps(res_list_dict,
    ensure_ascii=False)
    r, _ = Results.objects.get_or_create(who=f'mb_{prov}')
    r.json_data = for_result
    r.save()
    for key in res:
        newMB(dict_category_periphery, dc_dict['6'][key], dict_category_foto)

    """mb = MB_OTHER.objects.all().values_list('part_number', flat=True)
    mb_set = set(mb)
    full = Parts_full.objects.filter(providers__name_provider=prov,
    kind__in=('amb', 'imb'), availability_parts='yes')
    full_sub_mb = full.exclude(partnumber_parts__in=mb_set)
    for_result = json.dumps(list(full_sub_mb.values('name_parts', 'partnumber_parts')),
    ensure_ascii=False)
    r,_ = Results.objects.get_or_create(who=f'mb_{prov}')
    r.json_data = for_result
    r.save()"""

    try:
        dict_set = set(dc_dict['2'].keys())
    except:
        dict_set = set()
    q_set = set(RAM_OTHER.objects.all().values_list('part_number', flat=True))
    res = dict_set - q_set
    res_list_dict = [
    {'name_parts': x, 'partnumber_parts': dc_dict['2'][x]['Name']} for x in res
    ]
    for_result = json.dumps(res_list_dict,
    ensure_ascii=False)
    r, _ = Results.objects.get_or_create(who=f'ram_{prov}')
    r.json_data = for_result
    r.save()
    for key in res:
        newRAM(dict_category_periphery, dc_dict['2'][key], dict_category_foto)

    """ram = RAM_OTHER.objects.all().values_list('part_number', flat=True)
    ram_set = set(ram)
    full = Parts_full.objects.filter(providers__name_provider=prov,
    kind='mem', availability_parts='yes')
    full_sub_ram = full.exclude(partnumber_parts__in=ram_set)
    for_result = json.dumps(list(full_sub_ram.values('name_parts', 'partnumber_parts')),
    ensure_ascii=False)
    r,_ = Results.objects.get_or_create(who=f'mem_{prov}')
    r.json_data = for_result
    r.save()"""

    try:
        dict_set = set(dc_dict['3'].keys())
    except:
        dict_set = set()
    q_set = set(HDD_OTHER.objects.all().values_list('part_number', flat=True))
    res = dict_set - q_set
    res_list_dict = [
    {'name_parts': x, 'partnumber_parts': dc_dict['3'][x]['Name']} for x in res
    ]
    for_result = json.dumps(res_list_dict,
    ensure_ascii=False)
    r, _ = Results.objects.get_or_create(who=f'hdd_{prov}')
    r.json_data = for_result
    r.save()
    for key in res:
        newHDD(dict_category_periphery, dc_dict['3'][key], dict_category_foto)

    """hdd = HDD_OTHER.objects.all().values_list('part_number', flat=True)
    hdd_set = set(hdd)
    full = Parts_full.objects.filter(providers__name_provider=prov,
    kind='hdd', availability_parts='yes')
    full_sub_hdd = full.exclude(partnumber_parts__in=hdd_set)
    for_result = json.dumps(list(full_sub_hdd.values('name_parts', 'partnumber_parts')),
    ensure_ascii=False)
    r,_ = Results.objects.get_or_create(who=f'hdd_{prov}')
    r.json_data = for_result
    r.save()"""

    try:
        dict_set = set(dc_dict['724'].keys())
    except:
        dict_set = set()
    q_set = set(PSU_OTHER.objects.all().values_list('part_number', flat=True))
    res = dict_set - q_set
    res_list_dict = [
    {'name_parts': x, 'partnumber_parts': dc_dict['724'][x]['Name']} for x in res
    ]
    for_result = json.dumps(res_list_dict,
    ensure_ascii=False)
    r, _ = Results.objects.get_or_create(who=f'psu_{prov}')
    r.json_data = for_result
    r.save()
    for key in res:
        newPSU(dict_category_periphery, dc_dict['724'][key], dict_category_foto)

    """psu = PSU_OTHER.objects.all().values_list('part_number', flat=True)
    psu_set = set(psu)
    full = Parts_full.objects.filter(providers__name_provider=prov,
    kind='ps', availability_parts='yes')
    full_sub_psu = full.exclude(partnumber_parts__in=psu_set)
    for_result = json.dumps(list(full_sub_psu.values('name_parts', 'partnumber_parts')),
    ensure_ascii=False)
    r,_ = Results.objects.get_or_create(who=f'psu_{prov}')
    r.json_data = for_result
    r.save()"""

    try:
        dict_set = set(dc_dict['9'].keys())
    except:
        dict_set = set()
    q_set = set(GPU_OTHER.objects.all().values_list('part_number', flat=True))
    res = dict_set - q_set
    res_list_dict = [
    {'name_parts': x, 'partnumber_parts': dc_dict['9'][x]['Name']} for x in res
    ]
    for_result = json.dumps(res_list_dict,
    ensure_ascii=False)
    r, _ = Results.objects.get_or_create(who=f'gpu_{prov}')
    r.json_data = for_result
    r.save()
    for key in res:
        newGPU(dict_category_periphery, dc_dict['9'][key], dict_category_foto)

    """gpu = GPU_OTHER.objects.all().values_list('part_number', flat=True)
    gpu_set = set(gpu)
    full = Parts_full.objects.filter(providers__name_provider=prov,
    kind='video', availability_parts='yes')
    full_sub_gpu = full.exclude(partnumber_parts__in=gpu_set)
    for_result = json.dumps(list(full_sub_gpu.values('name_parts', 'partnumber_parts')),
    ensure_ascii=False)
    r,_ = Results.objects.get_or_create(who=f'gpu_{prov}')
    r.json_data = for_result
    r.save()"""

    try:
        dict_set = set(dc_dict['23'].keys())
        full = Parts_full.objects.filter(providers__name_provider='dc',
        kind='vent', availability_parts='yes')
         # чтоб отделить кулер от вентилятор
        set_price = set(full.values_list('partnumber_parts', flat=True))
        dict_set_inter = dict_set & set_price
    except:
        dict_set_inter = set()
    q_set = set(FAN_OTHER.objects.all().values_list('part_number', flat=True))
    res = dict_set_inter - q_set
    res_list_dict = [
    {'name_parts': x, 'partnumber_parts': dc_dict['23'][x]['Name']} for x in res
    ]
    for_result = json.dumps(res_list_dict,
    ensure_ascii=False)
    r, _ = Results.objects.get_or_create(who=f'fan_{prov}')
    r.json_data = for_result
    r.save()
    for key in res:
        newFAN(dict_category_periphery, dc_dict['23'][key], dict_category_foto)

    """fan = FAN_OTHER.objects.all().values_list('part_number', flat=True)
    fan_set = set(fan)
    full = Parts_full.objects.filter(providers__name_provider=prov,
    kind='vent', availability_parts='yes')
    full_sub_fan = full.exclude(partnumber_parts__in=fan_set)
    for_result = json.dumps(list(full_sub_fan.values('name_parts', 'partnumber_parts')),
    ensure_ascii=False)
    r,_ = Results.objects.get_or_create(who=f'fan_{prov}')
    r.json_data = for_result
    r.save()"""

    try:
        dict_set = set(dc_dict['8'].keys())
    except:
        dict_set = set()
    q_set = set(CASE_OTHER.objects.all().values_list('part_number', flat=True))
    res = dict_set - q_set
    res_list_dict = [
    {'name_parts': x, 'partnumber_parts': dc_dict['8'][x]['Name']} for x in res
    ]
    for_result = json.dumps(res_list_dict,
    ensure_ascii=False)
    r, _ = Results.objects.get_or_create(who=f'case_{prov}')
    r.json_data = for_result
    r.save()
    for key in res:
        newCASE(dict_category_periphery, dc_dict['8'][key], dict_category_foto)

    """case = CASE_OTHER.objects.all().values_list('part_number', flat=True)
    case_set = set(case)
    full = Parts_full.objects.filter(providers__name_provider=prov,
    kind='case', availability_parts='yes')
    full_sub_case = full.exclude(partnumber_parts__in=case_set)
    for_result = json.dumps(list(full_sub_case.values('name_parts', 'partnumber_parts')),
    ensure_ascii=False)
    r,_ = Results.objects.get_or_create(who=f'case_{prov}')
    r.json_data = for_result
    r.save()"""

    try:
        dict_set = set(dc_dict['27'].keys())
    except:
        dict_set = set()
    q_set = set(SSD_OTHER.objects.all().values_list('part_number', flat=True))
    res = dict_set - q_set
    res_list_dict = [
    {'name_parts': x, 'partnumber_parts': dc_dict['27'][x]['Name']} for x in res
    ]
    for_result = json.dumps(res_list_dict,
    ensure_ascii=False)
    r, _ = Results.objects.get_or_create(who=f'ssd_{prov}')
    r.json_data = for_result
    r.save()
    for key in res:
        newSSD(dict_category_periphery, dc_dict['27'][key], dict_category_foto)

    """ssd = SSD_OTHER.objects.all().values_list('part_number', flat=True)
    ssd_set = set(ssd)
    full = Parts_full.objects.filter(providers__name_provider=prov,
    kind='ssd', availability_parts='yes')
    full_sub_ssd = full.exclude(partnumber_parts__in=ssd_set)
    for_result = json.dumps(list(full_sub_ssd.values('name_parts', 'partnumber_parts')),
    ensure_ascii=False)
    r,_ = Results.objects.get_or_create(who=f'ssd_{prov}')
    r.json_data = for_result
    r.save()"""

def edit_kb_h():
    # дозаливка+- с ДС kb and head(for tech) vinujdenno
    DC_LOGIN = 'itblok'
    DC_PASSWORD = 'VIA5qPUv'

    """r = requests.post('https://api.dclink.com.ua/api/GetPriceAll', data={
        'login': DC_LOGIN,
        'password': DC_PASSWORD
    })"""
    with open('load_form_providers/dclink-price.xml', 'rb') as fobj:
        xml = fobj.read()

    list_periphery, dict_category_periphery, dict_category_foto = get_from_xml(
    xml, DC_LOGIN, DC_PASSWORD, periphery=True)

    for list_ in list_periphery:
        if list_['CategoryID'] == '56':
            dc_products = list_

            res = get_discr_categ_dc(dict_category_periphery[dc_products['CategoryID']],
                                    dc_products['Code'])
            try:
                if Headsets.objects.filter(
                part_number=dc_products['Article']).exists():
                    print('hok')
                    obj = Headsets.objects.get(
                    part_number=dc_products['Article'])

                    try:
                        hs_ver_ = to_False_or_True(
                        res[dc_products['Code']]['Версія Bluetooth'],
                        str_or_minus=True)
                    except:
                        hs_ver_ = '-'
                    obj.hs_ver = hs_ver_
                    obj.save()
            except Exception as e:
                print(list_, e)

        if list_['CategoryID'] == '33':
            dc_products = list_

            res = get_discr_categ_dc(dict_category_periphery[dc_products['CategoryID']],
                                    dc_products['Code'])
            try:
                if Keyboards.objects.filter(
                part_number=dc_products['Article']).exists():
                    print('kok')
                    obj = Keyboards.objects.get(
                    part_number=dc_products['Article'])

                    try:
                        kb_type_con_ua_ = to_False_or_True(
                        res[dc_products['Code']]['Тип підключення'],
                        str_or_minus=True)
                    except:
                        kb_type_con_ua_ = '-'
                    try:
                        kb_type_but_ua_ = to_False_or_True(
                        res[dc_products['Code']]['Тип клавіш'],
                        str_or_minus=True)
                    except:
                        kb_type_but_ua_ = '-'
                    try:
                        kb_type_pow_ua_ = to_False_or_True(
                        res[dc_products['Code']]['Джерело живлення'],
                        str_or_minus=True)
                    except:
                        kb_type_pow_ua_ = '-'
                    try:
                        kb_form_ua_ = to_False_or_True(
                        res[dc_products['Code']]['Форм-фактор'],
                        str_or_minus=True)
                    except:
                        kb_form_ua_ = '-'
                    try:
                        kb_type_conn_ = to_False_or_True(
                        res[dc_products['Code']]['Тип перемикачів'],
                        str_or_minus=True)
                    except:
                        kb_type_conn_ = '-'

                    obj.kb_type_con_ua = kb_type_con_ua_
                    obj.kb_type_but_ua = kb_type_but_ua_
                    obj.kb_type_pow_ua = kb_type_pow_ua_
                    obj.kb_form_ua = kb_form_ua_
                    obj.kb_type_conn = kb_type_conn_
                    obj.save()
            except Exception as e:
                print(list_, e)

def edit_obj():
    # дозаливка+- с ДС данными(for singleparts)
    DC_LOGIN = 'itblok'
    DC_PASSWORD = 'VIA5qPUv'

    """r = requests.post('https://api.dclink.com.ua/api/GetPriceAll', data={
        'login': DC_LOGIN,
        'password': DC_PASSWORD
    })"""
    with open('load_form_providers/dclink-price.xml', 'rb') as fobj:
        xml = fobj.read()

    list_periphery, dict_category_periphery, dict_category_foto = get_from_xml(
    xml, DC_LOGIN, DC_PASSWORD, periphery=False)

    for list_ in list_periphery:
        if list_['CategoryID'] == '9':
            dc_products = list_

            res = get_discr_categ_dc(dict_category_periphery[dc_products['CategoryID']],
                                    dc_products['Code'])
            try:
                if GPU_OTHER.objects.filter(
                part_number=dc_products['Article']).exists():
                    obj = GPU_OTHER.objects.get(
                    part_number=dc_products['Article'])
                    obj.gpu_mem_type = res[dc_products['Code']]["Тип пам'яті"]
                    obj.gpu_core_fq = res[dc_products['Code']]['Частота ядра, МГц']
                    obj.gpu_mem_fq = res[dc_products['Code']]["Частота пам'яті, МГц"]
                    obj.gpu_pci_type = res[dc_products['Code']]['Інтерфейс підключення']
                    obj.gpu_watt = res[dc_products['Code']]['Рекомендована потужність блоку живлення']
                    obj.full = True
                    obj.save()
            except Exception as e:
                print(list_, e)

        if list_['CategoryID'] == '724':
            dc_products = list_

            res = get_discr_categ_dc(dict_category_periphery[dc_products['CategoryID']],
                                    dc_products['Code'])
            try:
                psu_mod_ = res[dc_products['Code']]['Модульне підключення']
                psu_mod_ = False if psu_mod_ == 'нет' else True

                if PSU_OTHER.objects.filter(
                part_number=dc_products['Article']).exists():
                    obj = PSU_OTHER.objects.get(
                    part_number=dc_products['Article'])
                    obj.psu_mod = psu_mod_
                    obj.full = True
                    obj.save()
            except Exception as e:
                print(list_, e)

        if list_['CategoryID'] == '2':
            dc_products = list_

            res = get_discr_categ_dc(dict_category_periphery[dc_products['CategoryID']],
                                    dc_products['Code'])
            try:
                ram_led_ = res[dc_products['Code']]['Наявність підсвічування']
                ram_led_ = False if ram_led_ == 'без підсвічування' else True

                if RAM_OTHER.objects.filter(
                part_number=dc_products['Article']).exists():
                    obj = RAM_OTHER.objects.get(
                    part_number=dc_products['Article'])
                    obj.ram_cl = res[dc_products['Code']]["Таймінги"]
                    obj.ram_led = ram_led_
                    obj.full = True
                    obj.save()
            except Exception as e:
                print(list_, e)




def start():
    # заливка с ДС данными(for singleparts)

    DC_LOGIN = 'itblok'
    DC_PASSWORD = 'VIA5qPUv'

    """r = requests.post('https://api.dclink.com.ua/api/GetPriceAll', data={
        'login': DC_LOGIN,
        'password': DC_PASSWORD
    })"""
    with open('load_form_providers/dclink-price.xml', 'rb') as fobj:
        xml = fobj.read()

    list_periphery, dict_category_periphery, dict_category_foto = get_from_xml(
    xml, DC_LOGIN, DC_PASSWORD, periphery=False)

    for list_ in list_periphery:
        if list_['CategoryID'] == '1':
            try:
                dc_products = list_

                res = get_discr_categ_dc(dict_category_periphery[dc_products['CategoryID']],
                                        dc_products['Code'])
                foto_ = dict_category_foto[dc_products['CategoryID']]
                try:
                    foto_ = foto_[dc_products['Code']]
                except:
                    foto_ = ['пусто']
                foto_ = foto_ if len(foto_) > 1 else foto_ + foto_
                temp_price = float(dc_products['PriceUSD'])

                CPU_OTHER.objects.create(
                name=dc_products['Name'][:99],
                part_number=dc_products['Article'],
                price_rent=round(temp_price * 1.05 * 37),
                r_price=round(temp_price * 1.05 * 37),
                price_ua=round(temp_price * 37),
                price_usd=temp_price,
                vendor=dc_products['Vendor'],
                cpu_fam=res[dc_products['Code']]['Сімейство процесора'],
                cpu_bfq=re.split('-', res[dc_products['Code']]['Внутрішня тактова частота (ГГц)'])[0],
                cpu_cache=res[dc_products['Code']]['Кеш L3'],
                cpu_soc=res[dc_products['Code']]["Роз'єми"],
                cpu_core=res[dc_products['Code']]['Кількість ядер процесора'],
                cpu_threeds=res[dc_products['Code']]['Кількість потоків'],
                cpu_tbfq=re.split('-', res[dc_products['Code']]['Внутрішня тактова частота (ГГц)'])[-1],
                cpu_gpu=res[dc_products['Code']]['Інтегрована графіка'],
                cpu_warr_ua=dc_products['Warranty'],
                cpu_warr_ru=dc_products['Warranty'],
                cover1=foto_[0],
                cover2=foto_[1],
                cover3=foto_[-1],
                )
            except Exception as e:
                print(list_, e)

        if list_['CategoryID'] == '8':
            try:
                dc_products = list_

                res = get_discr_categ_dc(dict_category_periphery[dc_products['CategoryID']],
                                        dc_products['Code'])
                foto_ = dict_category_foto[dc_products['CategoryID']]
                try:
                    foto_ = foto_[dc_products['Code']]
                except:
                    foto_ = ['пусто']
                foto_ = foto_ if len(foto_) > 1 else foto_ + foto_
                temp_price = float(dc_products['PriceUSD'])

                try:
                    ps = False if res[dc_products['Code']]['Потужність блоку живлення'].find(
                    'немає') != -1 else True
                except:
                    ps = '-'

                CASE_OTHER.objects.create(
                name=dc_products['Name'][:99],
                part_number=dc_products['Article'],
                price_rent=round(temp_price * 1.05 * 37),
                r_price=round(temp_price * 1.05 * 37),
                price_ua=round(temp_price * 37),
                price_usd=temp_price,
                vendor=dc_products['Vendor'],
                case_mb=res[dc_products['Code']]['Форм-фактор материнської плати'],

                case_fan=res[dc_products['Code']]['Вентилятори'],
                case_psu_p = ps,
                case_s = dc_products['Subcategory'],
                case_warr_ua=dc_products['Warranty'],
                case_warr_ru=dc_products['Warranty'],
                cover1=foto_[0],
                cover2=foto_[1],
                cover3=foto_[-1],
                )
            except Exception as e:
                print(list_, e)

        if list_['CategoryID'] == '3':
            try:
                dc_products = list_

                res = get_discr_categ_dc(dict_category_periphery[dc_products['CategoryID']],
                                        dc_products['Code'])
                foto_ = dict_category_foto[dc_products['CategoryID']]
                try:
                    foto_ = foto_[dc_products['Code']]
                except:
                    foto_ = ['пусто']
                foto_ = foto_ if len(foto_) > 1 else foto_ + foto_
                temp_price = float(dc_products['PriceUSD'])

                HDD_OTHER.objects.create(
                name=dc_products['Name'],
                part_number=dc_products['Article'],
                price_rent=round(temp_price * 1.05 * 37),
                r_price=round(temp_price * 1.05 * 37),
                price_ua=round(temp_price * 37),
                price_usd=temp_price,
                vendor=dc_products['Vendor'],
                hdd_size=res[dc_products['Code']]["Об'єм жорсткого диска (GB)"],
                hdd_spd_ph_ua=res[dc_products['Code']]['Швидкість обертання (об/хв)'],
                hdd_spd_ph_ru=res[dc_products['Code']]['Швидкість обертання (об/хв)'],
                hdd_buf=res[dc_products['Code']]["Об'єм буфера (MB)"],
                hdd_ff=res[dc_products['Code']]['Форм-фактор'],
                hdd_warr_ua=dc_products['Warranty'],
                hdd_warr_ru=dc_products['Warranty'],
                cover1=foto_[0],
                cover2=foto_[1],
                cover3=foto_[-1],
                )
            except Exception as e:
                print(list_, e)

        if list_['CategoryID'] == '724':
            try:
                dc_products = list_

                res = get_discr_categ_dc(dict_category_periphery[dc_products['CategoryID']],
                                        dc_products['Code'])
                foto_ = dict_category_foto[dc_products['CategoryID']]
                try:
                    foto_ = foto_[dc_products['Code']]
                except:
                    foto_ = ['пусто']
                foto_ = foto_ if len(foto_) > 1 else foto_ + foto_
                temp_price = float(dc_products['PriceUSD'])

                PSU_OTHER.objects.create(
                name=dc_products['Name'],
                part_number=dc_products['Article'],
                price_rent=round(temp_price * 1.05 * 37),
                r_price=round(temp_price * 1.05 * 37),
                price_ua=round(temp_price * 37),
                price_usd=temp_price,
                vendor=dc_products['Vendor'],
                psu_pow=res[dc_products['Code']]['Потужність'],
                psu_fan=res[dc_products['Code']]['Охолодження'],
                psu_ff=res[dc_products['Code']]['Форм-фактор'],
                psu_warr_ua=dc_products['Warranty'],
                psu_warr_ru=dc_products['Warranty'],
                cover1=foto_[0],
                cover2=foto_[1],
                cover3=foto_[-1],
                )
            except Exception as e:
                print(list_, e)

        if list_['CategoryID'] == '9':
            try:
                dc_products = list_

                res = get_discr_categ_dc(dict_category_periphery[dc_products['CategoryID']],
                                        dc_products['Code'])
                foto_ = dict_category_foto[dc_products['CategoryID']]
                try:
                    foto_ = foto_[dc_products['Code']]
                except:
                    foto_ = ['пусто']
                foto_ = foto_ if len(foto_) > 1 else foto_ + foto_
                temp_price = float(dc_products['PriceUSD'])

                vga = False if res[dc_products['Code']]['D-Sub'].find(
                'відсутній') != -1 else True
                hdmi = False if res[dc_products['Code']]['HDMI'].find(
                'відсутній') != -1 else True
                dp = False if res[dc_products['Code']]['DisplayPort'].find(
                'відсутній') != -1 else True
                dvi = False if res[dc_products['Code']]['DVI'].find(
                'відсутній') != -1 else True

                GPU_OTHER.objects.create(
                name=dc_products['Name'],
                part_number=dc_products['Article'],
                price_rent=round(temp_price * 1.05 * 37),
                r_price=round(temp_price * 1.05 * 37),
                price_ua=round(temp_price * 37),
                price_usd=temp_price,
                vendor=dc_products['Vendor'],
                gpu_main_category=res[dc_products['Code']]['Виробник відеокарти'],
                gpu_model=res[dc_products['Code']]['Графічний чіп'],
                gpu_mem_size=res[dc_products['Code']]["Об'єм пам'яті"],
                gpu_bit=res[dc_products['Code']]["Шина пам'яті"],
                gpu_fan=res[dc_products['Code']]['Кількість вентиляторів'],
                gpu_max_l=res[dc_products['Code']]['Довжина відеокарти'],
                gpu_vga=vga,
                gpu_dvi=dvi,
                gpu_hdmi=hdmi,
                gpu_dp=dp,
                gpu_warr_ua=dc_products['Warranty'],
                gpu_warr_ru=dc_products['Warranty'],
                cover1=foto_[0],
                cover2=foto_[1],
                cover3=foto_[-1],
                )
            except Exception as e:
                print(list_, e)

        if list_['CategoryID'] == '27':
            try:
                dc_products = list_

                res = get_discr_categ_dc(dict_category_periphery[dc_products['CategoryID']],
                                        dc_products['Code'])
                foto_ = dict_category_foto[dc_products['CategoryID']]
                try:
                    foto_ = foto_[dc_products['Code']]
                except:
                    foto_ = ['пусто']
                foto_ = foto_ if len(foto_) > 1 else foto_ + foto_
                temp_price = float(dc_products['PriceUSD'])

                SSD_OTHER.objects.create(
                name=dc_products['Name'],
                part_number=dc_products['Article'],
                price_rent=round(temp_price * 1.05 * 37),
                r_price=round(temp_price * 1.05 * 37),
                price_ua=round(temp_price * 37),
                price_usd=temp_price,
                vendor=dc_products['Vendor'],
                ssd_size=res[dc_products['Code']]["Об'єм жорсткого диска"],
                ssd_nand=res[dc_products['Code']]["Тип пам'яті"],
                ssd_ff=res[dc_products['Code']]['Форм-фактор'],
                ssd_int=res[dc_products['Code']]["Інтерфейс"],
                part_ssd_r_spd=res[dc_products['Code']]['Швидкість зчитування'],
                part_ssd_w_spd=res[dc_products['Code']]['Швидкість запису'],
                ssd_warr_ua=dc_products['Warranty'],
                ssd_warr_ru=dc_products['Warranty'],
                cover1=foto_[0],
                cover2=foto_[1],
                cover3=foto_[-1],
                )
            except Exception as e:
                print(list_, e)

        if list_['CategoryID'] == '2':
            try:
                dc_products = list_

                res = get_discr_categ_dc(dict_category_periphery[dc_products['CategoryID']],
                                        dc_products['Code'])
                foto_ = dict_category_foto[dc_products['CategoryID']]
                try:
                    foto_ = foto_[dc_products['Code']]
                except:
                    foto_ = ['пусто']
                foto_ = foto_ if len(foto_) > 1 else foto_ + foto_
                temp_price = float(dc_products['PriceUSD'])

                size = res[dc_products['Code']]["Об'єм одного модуля"]
                num = res[dc_products['Code']]["Кількість модулів у комплекті"]
                size_num = f'{size} * {num}'

                RAM_OTHER.objects.create(
                name=dc_products['Name'],
                part_number=dc_products['Article'],
                price_rent=round(temp_price * 1.05 * 37),
                r_price=round(temp_price * 1.05 * 37),
                price_ua=round(temp_price * 37),
                price_usd=temp_price,
                vendor=dc_products['Vendor'],
                ram_size=size_num,
                ram_fq=res[dc_products['Code']]["Частота пам'яті"],
                ram_type=res[dc_products['Code']]["Тип оперативної пам'яті"],
                ram_mod_am=num,
                ram_col_ua=res[dc_products['Code']]['Колір'],
                ram_col_ru=res[dc_products['Code']]['Колір'],
                ram_warr_ua=dc_products['Warranty'],
                ram_warr_ru=dc_products['Warranty'],
                cover1=foto_[0],
                cover2=foto_[1],
                cover3=foto_[-1],
                )
            except Exception as e:
                print(list_, e)

        if list_['CategoryID'] == '23' and list_['Name'].find('Вентилятор') == -1:
            try:
                dc_products = list_

                res = get_discr_categ_dc(dict_category_periphery[dc_products['CategoryID']],
                                        dc_products['Code'])
                foto_ = dict_category_foto[dc_products['CategoryID']]
                try:
                    foto_ = foto_[dc_products['Code']]
                except:
                    foto_ = ['пусто']
                foto_ = foto_ if len(foto_) > 1 else foto_ + foto_
                temp_price = float(dc_products['PriceUSD'])
                rgb = res[dc_products['Code']]['Підсвічування']
                rgb = rgb if rgb.find('немає') == -1 else '-'
                s1=';1200' if res[dc_products['Code']]['Socket 1200'].find('немає')==-1 else ''
                s2=';am3' if res[dc_products['Code']]['Socket AM3+'].find('немає')==-1 else ''
                s3=';am4' if res[dc_products['Code']]['Socket AM4'].find('немає')==-1 else ''
                s4=';2066' if res[dc_products['Code']]['Socket 2066'].find('немає')==-1 else ''
                s5=';trx4' if res[dc_products['Code']]['Socket TRX4'].find('немає')==-1 else ''
                s6=';1700' if res[dc_products['Code']]['Socket 1700'].find('немає')==-1 else ''
                s7=';tr4' if res[dc_products['Code']]['Socket TR4'].find('немає')==-1 else ''
                s8=';2011' if res[dc_products['Code']]['Socket 2011'].find('немає')==-1 else ''
                s9=';1151' if res[dc_products['Code']]['Socket 1151'].find('немає')==-1 else ''
                s10=';am5' if res[dc_products['Code']]['Socket AM5'].find('немає')==-1 else ''
                sock = f'{s1}{s2}{s3}{s4}{s5}{s6}{s7}{s8}{s9}{s10}'

                Cooler_OTHER.objects.create(
                name=dc_products['Name'],
                part_number=dc_products['Article'],
                price_rent=round(temp_price * 1.05 * 37),
                r_price=round(temp_price * 1.05 * 37),
                price_ua=round(temp_price * 37),
                price_usd=temp_price,
                vendor=dc_products['Vendor'],
                cool_fan_max_spd_ua=res[dc_products['Code']][
                'Максимальна швидкість обертання, об/хв'],
                cool_fan_max_spd_ru=res[dc_products['Code']][
                'Максимальна швидкість обертання, об/хв'],
                cool_fan_size=res[dc_products['Code']]['Діаметр вентилятора'],
                cool_sock=sock, #
                cool_max_tdp=res[dc_products['Code']]['Максимальний TDP (для ЦП і відеокарт)'],
                cool_col_ua=res[dc_products['Code']]['Колір'],
                cool_col_ru=res[dc_products['Code']]['Колір'],
                cool_rgb=rgb,
                cool_h=res[dc_products['Code']]['Висота системи охолодження'],
                cool_warr_ua=dc_products['Warranty'],
                cool_warr_ru=dc_products['Warranty'],
                cover1=foto_[0],
                cover2=foto_[1],
                cover3=foto_[-1],
                )
            except Exception as e:
                print(list_, e)

        if list_['CategoryID'] == '6':
            try:
                dc_products = list_

                res = get_discr_categ_dc(dict_category_periphery[dc_products['CategoryID']],
                                        dc_products['Code'])
                foto_ = dict_category_foto[dc_products['CategoryID']]
                try:
                    foto_ = foto_[dc_products['Code']]
                except:
                    foto_ = ['пусто']
                foto_ = foto_ if len(foto_) > 1 else foto_ + foto_
                temp_price = float(dc_products['PriceUSD'])

                header = True if res[dc_products['Code']][
                'Контроль підсвічування'].find('немає')==-1 else False
                raid = True if res[dc_products['Code']][
                'RAID 10'].find('немає')==-1 else False
                vga = True if res[dc_products['Code']][
                'D-Sub'].find('немає')==-1 else False
                dvi = True if res[dc_products['Code']][
                'DVI'].find('немає')==-1 else False
                hdmi = True if res[dc_products['Code']][
                'HDMI'].find('немає')==-1 else False
                dp = True if res[dc_products['Code']][
                'Display Port'].find('немає')==-1 else False
                lan = True if res[dc_products['Code']][
                'Мережевий адаптер (LAN)'].find('немає')==-1 else False
                wifi = True if res[dc_products['Code']][
                'Wi-Fi'].find('немає')==-1 else False
                bt = True if res[dc_products['Code']][
                'Bluetooth'].find('немає')==-1 else False
                usbtc = True if res[dc_products['Code']][
                'USB Type-C'].find('немає')==-1 else False

                MB_OTHER.objects.create(
                name=dc_products['Name'],
                part_number=dc_products['Article'],
                price_rent=round(temp_price * 1.05 * 37),
                r_price=round(temp_price * 1.05 * 37),
                price_ua=round(temp_price * 37),
                price_usd=temp_price,
                vendor=dc_products['Vendor'],
                part_mb_fam=res[dc_products['Code']]['Для процесорів'],
                part_mb_chip=res[dc_products['Code']]['Чіпсет'],
                part_mb_ram_max_size=res[dc_products['Code']][
                "Максимальний об'єм оперативної пам'яті"],
                part_mb_ram_sl=res[dc_products['Code']]["Кількість слотів пам'яті"].strip(),
                part_mb_ram_type=res[dc_products['Code']]["Тип оперативної пам'яті"].strip(),
                part_mb_sock=res[dc_products['Code']]['Сокет'],
                part_mb_ff=res[dc_products['Code']]['Форм-фактор'],
                part_mb_rgb_header=header,
                part_mb_sata=res[dc_products['Code']]["Роз'єм SATA "],
                part_mb_m2=res[dc_products['Code']]['M.2'],
                part_mb_raid=raid,
                part_mb_vga=vga,
                part_mb_dvi=dvi,
                part_mb_hdmi=hdmi,
                part_mb_dp=dp,
                part_mb_lan=lan,
                part_mb_wifi=wifi,
                part_mb_bt=bt,
                part_mb_usb_type_c=usbtc,
                part_mb_warr_ua=dc_products['Warranty'],
                part_mb_warr_ru=dc_products['Warranty'],
                cover1=foto_[0],
                cover2=foto_[1],
                cover3=foto_[-1],
                )
            except Exception as e:
                print(list_, res, e)


        if list_['CategoryID'] == '23' and list_['Name'].find('Вентилятор') != -1:
            try:
                dc_products = list_

                res = get_discr_categ_dc(dict_category_periphery[dc_products['CategoryID']],
                                        dc_products['Code'])
                foto_ = dict_category_foto[dc_products['CategoryID']]
                try:
                    foto_ = foto_[dc_products['Code']]
                except:
                    foto_ = ['пусто']
                foto_ = foto_ if len(foto_) > 1 else foto_ + foto_
                temp_price = float(dc_products['PriceUSD'])
                rgb = res[dc_products['Code']]['Підсвічування']
                rgb = rgb if rgb.find('немає') == -1 else '-'

                FAN_OTHER.objects.create(
                name=dc_products['Name'],
                part_number=dc_products['Article'],
                price_rent=round(temp_price * 1.05 * 37),
                r_price=round(temp_price * 1.05 * 37),
                price_ua=round(temp_price * 37),
                price_usd=temp_price,
                vendor=dc_products['Vendor'],
                fan_max_spd_ua=res[dc_products['Code']][
                'Максимальна швидкість обертання, об/хв'],
                fan_max_spd_ru=res[dc_products['Code']][
                'Максимальна швидкість обертання, об/хв'],
                part_fan_size=res[dc_products['Code']]['Діаметр вентилятора'],
                fan_b_type_ru=res[dc_products['Code']]["Тип підшипника"],
                fan_b_type_ua=res[dc_products['Code']]['Тип підшипника'],
                fan_quantity=res[dc_products['Code']]['Кількість вентиляторів'],
                fan_pow=res[dc_products['Code']]["Тип роз'єму"],
                fan_led_type_ua=rgb,
                fan_led_type_ru=rgb,
                fan_col_ua=res[dc_products['Code']]["Колір"],
                fan_col_ru=res[dc_products['Code']]["Колір"],
                fan_warr_ua=dc_products['Warranty'],
                fan_warr_ru=dc_products['Warranty'],
                cover1=foto_[0],
                cover2=foto_[1],
                cover3=foto_[-1],
                )
            except Exception as e:
                print(list_, e)
#from load_form_providers.dc_descr_catalog import start

# to_False_or_True
def start_tech():
    # заливка с ДС данными(for tech)

    DC_LOGIN = 'itblok'
    DC_PASSWORD = 'VIA5qPUv'

    """r = requests.post('https://api.dclink.com.ua/api/GetPriceAll', data={
        'login': DC_LOGIN,
        'password': DC_PASSWORD
    })"""
    with open('load_form_providers/dclink-price.xml', 'rb') as fobj:
        xml = fobj.read()

    list_periphery, dict_category_periphery, dict_category_foto = get_from_xml(
    xml, DC_LOGIN, DC_PASSWORD, periphery=True)

    for list_ in list_periphery:
        if list_['CategoryID'] == '5':
            try:
                dc_products = list_
                #print(dc_products['Name'])

                res = get_discr_categ_dc(dict_category_periphery[dc_products['CategoryID']],
                                        dc_products['Code'])
                foto_ = dict_category_foto[dc_products['CategoryID']]
                try:
                    foto_ = foto_[dc_products['Code']]
                except:
                    foto_ = ['пусто']
                foto_ = foto_ if len(foto_) > 1 else foto_ + foto_
                temp_price = float(dc_products['PriceUSD'])

                name_ = re.sub(
                'Монитор ', '', dc_products['Name'][:99]
                )
                dvi = to_False_or_True(res[dc_products['Code']]['DVI'],
                cifar= True)
                D_Sub = to_False_or_True(res[dc_products['Code']]['D-Sub'],
                cifar= True)
                HDMI = to_False_or_True(res[dc_products['Code']]['HDMI'],
                cifar= True)
                DisplayPort = to_False_or_True(res[dc_products['Code']]['DisplayPort'],
                cifar= True)
                arch = to_False_or_True(
                res[dc_products['Code']]['Вигнутий екран'],
                )
                audio = to_False_or_True(
                res[dc_products['Code']]['Вбудована аудіосистема'],
                )
                audio_p = to_False_or_True(
                res[dc_products['Code']]['Потужність аудіосистеми'],
                str_or_minus=True)
                spin = to_False_or_True(
                res[dc_products['Code']]['Поворотний екран (Pivot)'],
                )
                h_reg = to_False_or_True(
                res[dc_products['Code']]['Регулювання по висоті'],
                )
                usb = to_False_or_True(
                res[dc_products['Code']]['Концентратор USB'],
                )
                game = to_False_or_True(
                res[dc_products['Code']]['Ігрові технології'],
                )
                fi = to_False_or_True(
                res[dc_products['Code']]['Безрамковий монітор'],
                )


                Monitors.objects.create(
                name=name_,
                category_ru='Монитор',
                category_ua='Монiтор',
                part_number=dc_products['Article'],
                price_rent=round(temp_price * 1.05 * 37),
                r_price=round(temp_price * 1.05 * 37),
                price_ua=round(temp_price * 37),
                price_usd=temp_price,
                vendor=dc_products['Vendor'],
                sc_d=res[dc_products['Code']]['Діагональ екрану'],
                sc_r=res[dc_products['Code']]['Роздільна здатність екрану'],
                sc_t=res[dc_products['Code']]['Тип матриці'],
                sc_ss=res[dc_products['Code']]["Співвідношення сторін"],
                sc_l=res[dc_products['Code']]['Час реакції'],
                sc_v=res[dc_products['Code']]['Кут огляду'],
                sc_b=res[dc_products['Code']]['Яскравість'],
                sc_s=res[dc_products['Code']]['Контрастність'],
                sc_h=res[dc_products['Code']]['Частота оновлення'],
                sc_surf_ua=res[dc_products['Code']]['Поверхня екрану'],
                sc_d_sub=D_Sub,
                sc_dvi=dvi,
                sc_hdmi=HDMI,
                sc_dp=DisplayPort,
                sc_arch=arch,
                sc_spk=audio,
                sc_spk_p=audio_p,
                sc_spin=spin,
                sc_hight=h_reg,
                sc_usb=usb,
                sc_o=game,
                sc_fi=fi,
                sc_vesa=res[dc_products['Code']]['Кріплення на стіну'],
                sc_vol=res[dc_products['Code']]['Габарити (ШхВхГ)'],
                sc_weight=res[dc_products['Code']]['Вага'],
                sc_col_ua=res[dc_products['Code']]['Колір'],

                sc_warr_ua=dc_products['Warranty'],
                sc_warr_ru=dc_products['Warranty'],
                cover1=foto_[0],
                cover2=foto_[1],
                cover3=foto_[-1],
                )
            except Exception as e:
                print(list_, e)
        if list_['CategoryID'] == '968':
            try:
                dc_products = list_
                #print(dc_products['Name'])

                res = get_discr_categ_dc(dict_category_periphery[dc_products['CategoryID']],
                                        dc_products['Code'])
                foto_ = dict_category_foto[dc_products['CategoryID']]
                try:
                    foto_ = foto_[dc_products['Code']]
                except:
                    foto_ = ['пусто']
                foto_ = foto_ if len(foto_) > 1 else foto_ + foto_
                temp_price = float(dc_products['PriceUSD'])

                name_ = re.sub(
                'Комплект (клавиатура+мышь) ', '', dc_products['Name'][:99]
                )
                light = to_False_or_True(
                res[dc_products['Code']]['Підсвічування клавіатури']
                )
                km_ua_ = to_False_or_True(
                res[dc_products['Code']]['Українська розкладка']
                )
                buttoms = to_False_or_True(
                res[dc_products['Code']]['Кількість клавіш клавіатури'],
                cifar= True)
                mouse_light = to_False_or_True(
                res[dc_products['Code']]['Підсвічування миші']
                )
                mouse_w = to_False_or_True(
                res[dc_products['Code']]['Вага клавіатури'],
                str_or_minus= True)
                k_w = to_False_or_True(
                res[dc_products['Code']]['Вага миші'],
                str_or_minus= True)

                KM.objects.create(
                name=name_,
                category_ru='Комплект (клавиатура+мышь)',
                category_ua='Комплект (клавіатура, мишка)',
                part_number=dc_products['Article'],
                price_rent=round(temp_price * 1.05 * 37),
                r_price=round(temp_price * 1.05 * 37),
                price_ua=round(temp_price * 37),
                price_usd=temp_price,
                vendor=dc_products['Vendor'],
                km_connect_ua=res[dc_products['Code']]['Підключення'],
                km_int=res[dc_products['Code']]['Інтерфейс'],
                km_key_type_ua=res[dc_products['Code']]['Тип клавіш клавіатури'],
                km_k_light=light,
                km_ua=km_ua_,
                km_pow_k_ua=res[dc_products['Code']]['Живлення клавіатури'],
                km_sensor_ua=res[dc_products['Code']]['Тип сенсора миші'],
                km_numb_buttoms=buttoms,
                km_dpi=res[dc_products['Code']]['Роздільна здатність миші'],
                km_mouse_light=mouse_light,
                km_pow_mouse_ua=res[dc_products['Code']]['Живлення миші'],
                km_k_vol=res[dc_products['Code']]['Габарити клавіатури'],
                km_mouse_vol=res[dc_products['Code']]['Габарити миші'],
                km_k_weight=mouse_w,
                km_mouse_weight=k_w,
                km_col_ua=res[dc_products['Code']]['Колір'],

                km_warr_ua=dc_products['Warranty'],
                km_warr_ru=dc_products['Warranty'],
                cover1=foto_[0],
                cover2=foto_[1],
                cover3=foto_[-1],
                )
            except Exception as e:
                print(list_, e)

        if list_['CategoryID'] == '33':
            try:
                dc_products = list_
                #print(dc_products['Name'])

                res = get_discr_categ_dc(dict_category_periphery[dc_products['CategoryID']],
                                        dc_products['Code'])
                foto_ = dict_category_foto[dc_products['CategoryID']]
                try:
                    foto_ = foto_[dc_products['Code']]
                except:
                    foto_ = ['пусто']
                foto_ = foto_ if len(foto_) > 1 else foto_ + foto_
                temp_price = float(dc_products['PriceUSD'])

                name_ = re.sub(
                'Клавиатура ', '', dc_products['Name'][:99]
                )
                kb_light_ = to_False_or_True(
                res[dc_products['Code']]['Підсвічування клавіш']
                )
                kb_rgb_ = to_False_or_True(
                res[dc_products['Code']]['Наявність RGB']
                )
                kb_res_ = to_False_or_True(
                res[dc_products['Code']]['Вологостійкість']
                )
                plus_but = to_False_or_True(
                res[dc_products['Code']]['Додаткові клавіші'],
                cifar= True)

                kb_usb_ = to_False_or_True(
                res[dc_products['Code']]['USB']
                )
                kb_ps_ = to_False_or_True(
                res[dc_products['Code']]['PS/2']
                )
                kb_bt_ = to_False_or_True(
                res[dc_products['Code']]['Bluetooth']
                )
                kb_usb_resiver_ = to_False_or_True(
                res[dc_products['Code']]['USB-ресивер']
                )
                kb_usb_type_c_ = to_False_or_True(
                res[dc_products['Code']]['USB Type-C']
                )
                kb_vol_ = to_False_or_True(
                res[dc_products['Code']]['Габарити'],
                str_or_minus= True)
                kb_weight_ = to_False_or_True(
                res[dc_products['Code']]['Вага'],
                str_or_minus= True)

                Keyboards.objects.create(
                name=name_,
                category_ru='Клавиатура',
                category_ua='Клавіатура',
                part_number=dc_products['Article'],
                price_rent=round(temp_price * 1.05 * 37),
                r_price=round(temp_price * 1.05 * 37),
                price_ua=round(temp_price * 37),
                price_usd=temp_price,
                vendor=dc_products['Vendor'],
                kb_plus_but=plus_but,
                kb_light=kb_light_,
                kb_rgb=kb_rgb_,
                kb_res=kb_res_,
                kb_cab_long=res[dc_products['Code']]['Довжина кабеля'],
                kb_leng=res[dc_products['Code']]['Розкладка'],
                kb_vol=kb_vol_,
                kb_weight=kb_weight_,
                kb_usb=kb_usb_,
                kb_ps=kb_ps_,
                kb_bt=kb_bt_,
                kb_usb_resiver=kb_usb_resiver_,
                kb_usb_type_c=kb_usb_type_c_,
                kb_col_ua=res[dc_products['Code']]['Колір'],

                kb_warr_ua=dc_products['Warranty'],
                kb_warr_ru=dc_products['Warranty'],
                cover1=foto_[0],
                cover2=foto_[1],
                cover3=foto_[-1],
                )
            except Exception as e:
                print(list_, e)

        if list_['CategoryID'] == '11':
            try:
                dc_products = list_
                #print(dc_products['Name'])

                res = get_discr_categ_dc(dict_category_periphery[dc_products['CategoryID']],
                                        dc_products['Code'])
                foto_ = dict_category_foto[dc_products['CategoryID']]
                try:
                    foto_ = foto_[dc_products['Code']]
                except:
                    foto_ = ['пусто']
                foto_ = foto_ if len(foto_) > 1 else foto_ + foto_
                temp_price = float(dc_products['PriceUSD'])

                name_ = re.sub(
                'Мышь ', '', dc_products['Name'][:99]
                )
                buttoms = to_False_or_True(
                res[dc_products['Code']]['Кількість кнопок'],
                cifar= True)

                Mouses.objects.create(
                name=name_,
                category_ru='Мышь',
                category_ua='Мишка',
                part_number=dc_products['Article'],
                price_rent=round(temp_price * 1.05 * 37),
                r_price=round(temp_price * 1.05 * 37),
                price_ua=round(temp_price * 37),
                price_usd=temp_price,
                vendor=dc_products['Vendor'],
                mouse_type_connect_ua=res[dc_products['Code']]["Тип з'єднання"],
                mouse_int=res[dc_products['Code']]["Інтерфейс з'єднання"],
                mouse_sensor_ua=res[dc_products['Code']]["Тип сенсора"],
                mouse_dpi=res[dc_products['Code']]["Роздільна здатність"],
                mouse_numb_buttoms=buttoms,
                mouse_pow_ua=res[dc_products['Code']]['Живлення'],
                mouse_length_cable=res[dc_products['Code']]['Довжина кабелю'],
                mouse_vol=res[dc_products['Code']]['Розмір'],
                mouse_weight=res[dc_products['Code']]['Вага'],
                mouse_col_ua=res[dc_products['Code']]['Колір'],

                mouse_warr_ua=dc_products['Warranty'],
                mouse_warr_ru=dc_products['Warranty'],
                cover1=foto_[0],
                cover2=foto_[1],
                cover3=foto_[-1],
                )
            except Exception as e:
                print(list_, e)

        if list_['CategoryID'] == '24':
            try:
                dc_products = list_
                #print(dc_products['Name'])

                res = get_discr_categ_dc(dict_category_periphery[dc_products['CategoryID']],
                                        dc_products['Code'])
                foto_ = dict_category_foto[dc_products['CategoryID']]
                try:
                    foto_ = foto_[dc_products['Code']]
                except:
                    foto_ = ['пусто']
                foto_ = foto_ if len(foto_) > 1 else foto_ + foto_
                temp_price = float(dc_products['PriceUSD'])

                name_ = re.sub(
                'Коврик для мыши ', '', dc_products['Name'][:99]
                )
                pad_light_ = to_False_or_True(
                res[dc_products['Code']]['Наявність підсвічування']
                )

                Pads.objects.create(
                name=name_,
                category_ru='Коврик для мыши',
                category_ua='Килимок для миші',
                part_number=dc_products['Article'],
                price_rent=round(temp_price * 1.05 * 37),
                r_price=round(temp_price * 1.05 * 37),
                price_ua=round(temp_price * 37),
                price_usd=temp_price,
                vendor=dc_products['Vendor'],
                pad_bot_ua=res[dc_products['Code']]["Матеріал"],
                pad_vol=res[dc_products['Code']]["Габарити"],
                pad_light=pad_light_,
                pad_col_ua=res[dc_products['Code']]['Колір'],

                pad_warr_ua=dc_products['Warranty'],
                pad_warr_ru=dc_products['Warranty'],
                cover1=foto_[0],
                cover2=foto_[1],
                cover3=foto_[-1],
                )
            except Exception as e:
                print(list_, e)

        if list_['CategoryID'] == '56':
            try:
                dc_products = list_
                #print(dc_products['Name'])

                res = get_discr_categ_dc(dict_category_periphery[dc_products['CategoryID']],
                                        dc_products['Code'])
                foto_ = dict_category_foto[dc_products['CategoryID']]
                try:
                    foto_ = foto_[dc_products['Code']]
                except:
                    foto_ = ['пусто']
                foto_ = foto_ if len(foto_) > 1 else foto_ + foto_
                temp_price = float(dc_products['PriceUSD'])

                name_ = re.sub(
                'гарнитура ', '', dc_products['Name'][:99].lower()
                )
                try:
                    mike = res[dc_products['Code']]['Наявність мікрофону']
                except:
                    mike = 'y'
                hs_mike_avail_ = False if mike.find('з мікрофоном') == -1 else True
                hs_interface_ = to_False_or_True(
                res[dc_products['Code']]['3.5 мм (mini-jack)']
                )
                hs_usb_ = to_False_or_True(
                res[dc_products['Code']]['USB']
                )
                hs_usb_type_c_ = to_False_or_True(
                res[dc_products['Code']]['USB Type-C']
                )
                hs_water_res_ = to_False_or_True(
                res[dc_products['Code']]['Вологостійкість']
                )
                hs_light_ = to_False_or_True(
                res[dc_products['Code']]['Наявність підсвічування']
                )
                hs_resistance_ = to_False_or_True(
                res[dc_products['Code']]['Опір навушників'],
                str_or_minus=True)
                hs_weight_ = to_False_or_True(
                res[dc_products['Code']]['Вага'],
                str_or_minus=True)
                hs_time_ = to_False_or_True(
                res[dc_products['Code']]['Час роботи розмова/очікування'],
                str_or_minus=True)
                hs_con_type_ = to_False_or_True(
                res[dc_products['Code']]['Тип бездротового підключення'],
                str_or_minus=True)

                Headsets.objects.create(
                name=name_,
                category_ru='Гарнитура',
                category_ua='Гарнітура',
                part_number=dc_products['Article'],
                price_rent=round(temp_price * 1.05 * 37),
                r_price=round(temp_price * 1.05 * 37),
                price_ua=round(temp_price * 37),
                price_usd=temp_price,
                vendor=dc_products['Vendor'],
                hs_type_connect_ua=res[dc_products['Code']]['Тип підключення'],
                hs_sound_range=res[dc_products['Code']]['Частотний діапазон'],
                hs_resistance=hs_resistance_,
                hs_purpose_ua=res[dc_products['Code']]['Призначення'],
                hs_type_ua=res[dc_products['Code']]['Тип навушників'],
                hs_s_type_ua=res[dc_products['Code']]['Тип гарнітури'],
                hs_mike_ua=res[dc_products['Code']]['Конструкція мікрофону'],
                hs_mike_avail=hs_mike_avail_,
                hs_cable_length=res[dc_products['Code']]['Довжина кабелю'],
                hs_interface=hs_interface_,
                hs_usb=hs_usb_,
                hs_usb_type_c=hs_usb_type_c_,
                hs_col_ua=res[dc_products['Code']]['Колір'],

                hs_weight=hs_weight_,
                hs_ear_pads_material_ua=res[dc_products['Code']]['Матеріал амбушюр'],
                hs_metal_pads_material_ua=res[dc_products['Code']]['Матеріал корпусу'],
                hs_time=hs_time_,
                hs_con_type=hs_con_type_,
                hs_water_res=hs_water_res_,
                hs_light=hs_light_,
                hs_pow_ua=res[dc_products['Code']]['Живлення'],

                hs_warr_ua=dc_products['Warranty'],
                hs_warr_ru=dc_products['Warranty'],
                cover1=foto_[0],
                cover2=foto_[1],
                cover3=foto_[-1],
                )
            except Exception as e:
                print(list_, e)

        if list_['CategoryID'] == '54':
            try:
                dc_products = list_
                #print(dc_products['Name'])

                res = get_discr_categ_dc(dict_category_periphery[dc_products['CategoryID']],
                                        dc_products['Code'])
                foto_ = dict_category_foto[dc_products['CategoryID']]
                try:
                    foto_ = foto_[dc_products['Code']]
                except:
                    foto_ = ['пусто']
                foto_ = foto_ if len(foto_) > 1 else foto_ + foto_
                temp_price = float(dc_products['PriceUSD'])

                name_ = re.sub(
                'Веб-камера ', '', dc_products['Name'][:99]
                )
                web_mike_ = to_False_or_True(
                res[dc_products['Code']]['Мікрофон']
                )
                web_max_f_ = to_False_or_True(
                res[dc_products['Code']]['Максимальна частота кадрів відео'],
                cifar=True)
                web_focus_ = to_False_or_True(
                res[dc_products['Code']]['Фокусування'],
                str_or_minus=True)
                web_weight_ = to_False_or_True(
                res[dc_products['Code']]['Вага (г)'],
                str_or_minus=True)

                Webcams.objects.create(
                name=name_,
                category_ru='Веб-камера',
                category_ua='Веб-камера',
                part_number=dc_products['Article'],
                price_rent=round(temp_price * 1.05 * 37),
                r_price=round(temp_price * 1.05 * 37),
                price_ua=round(temp_price * 37),
                price_usd=temp_price,
                vendor=dc_products['Vendor'],
                web_r=res[dc_products['Code']]["Роздільна здатність"],
                web_pixel=res[dc_products['Code']]["Кількість мегапікселів веб-камери"],
                web_type_sensor=res[dc_products['Code']]["Тип сенсора"],
                web_mike=web_mike_,

                web_focus=web_focus_,
                web_int=res[dc_products['Code']]["Інтерфейси"],
                web_angle=res[dc_products['Code']]["Кут огляду"],
                web_max_f=web_max_f_,
                web_weight=web_weight_,
                web_col_ua=res[dc_products['Code']]["Колір"],

                web_warr_ua=dc_products['Warranty'],
                web_warr_ru=dc_products['Warranty'],
                cover1=foto_[0],
                cover2=foto_[1],
                cover3=foto_[-1],
                )
            except Exception as e:
                print(list_, e)

        if list_['CategoryID'] == '1410':
            try:
                dc_products = list_
                #print(dc_products['Name'])

                res = get_discr_categ_dc(dict_category_periphery[dc_products['CategoryID']],
                                        dc_products['Code'])
                foto_ = dict_category_foto[dc_products['CategoryID']]
                try:
                    foto_ = foto_[dc_products['Code']]
                except:
                    foto_ = ['пусто']
                foto_ = foto_ if len(foto_) > 1 else foto_ + foto_
                temp_price = float(dc_products['PriceUSD'])

                name_ = re.sub(
                'Беспроводной адаптер ', '', dc_products['Name'][:99]
                )
                net_wifi_bt_ = to_False_or_True(
                res[dc_products['Code']]['Підтримка Bluetooth']
                )
                net_wifi_ant_am_ = to_False_or_True(
                res[dc_products['Code']]['Зовнішні антени'],
                cifar=True)

                WiFis.objects.create(
                name=name_,
                category_ru='Беспроводной адаптер',
                category_ua='Бездротовий адаптер',
                part_number=dc_products['Article'],
                price_rent=round(temp_price * 1.05 * 37),
                r_price=round(temp_price * 1.05 * 37),
                price_ua=round(temp_price * 37),
                price_usd=temp_price,
                vendor=dc_products['Vendor'],
                net_wifi_int=res[dc_products['Code']]["Інтерфейс підключення"],
                net_wifi_ant_am=net_wifi_ant_am_,
                net_wifi_st=res[dc_products['Code']]["Стандарти Wi-Fi"],
                net_wifi_ghz=res[dc_products['Code']]['Частота роботи Wi-Fi'],
                net_wifi_bt=net_wifi_bt_,

                net_wifi_warr_ua=dc_products['Warranty'],
                net_wifi_warr_ru=dc_products['Warranty'],
                cover1=foto_[0],
                cover2=foto_[1],
                cover3=foto_[-1],
                )
            except Exception as e:
                print(list_, e)

        if list_['CategoryID'] == '25':
            try:
                dc_products = list_
                #print(dc_products['Name'])

                res = get_discr_categ_dc(dict_category_periphery[dc_products['CategoryID']],
                                        dc_products['Code'])
                foto_ = dict_category_foto[dc_products['CategoryID']]
                try:
                    foto_ = foto_[dc_products['Code']]
                except:
                    foto_ = ['пусто']
                foto_ = foto_ if len(foto_) > 1 else foto_ + foto_
                temp_price = float(dc_products['PriceUSD'])

                name_ = re.sub(
                'Акустическая система ', '', dc_products['Name'][:99]
                )
                a_usb_ = to_False_or_True(
                res[dc_products['Code']]['USB']
                )
                a_card_ = to_False_or_True(
                res[dc_products['Code']]['Кардрідер']
                )
                a_wifi_ = to_False_or_True(
                res[dc_products['Code']]['Wi-Fi']
                )
                a_bt_ = to_False_or_True(
                res[dc_products['Code']]['Bluetooth']
                )
                a_fm_ = to_False_or_True(
                res[dc_products['Code']]['FM-приймач']
                )
                a_control_ = to_False_or_True(
                res[dc_products['Code']]['Пульт ДК']
                )
                a_audio_ = to_False_or_True(
                res[dc_products['Code']]["Аудіо"],
                str_or_minus=True
                )

                Acoustics.objects.create(
                name=name_,
                category_ru='Акустическая система',
                category_ua='Акустична система',
                part_number=dc_products['Article'],
                price_rent=round(temp_price * 1.05 * 37),
                r_price=round(temp_price * 1.05 * 37),
                price_ua=round(temp_price * 37),
                price_usd=temp_price,
                vendor=dc_products['Vendor'],
                a_format=res[dc_products['Code']]['Формат акустики'],
                a_p=res[dc_products['Code']]['Потужність'],
                a_f=res[dc_products['Code']]['Частотний діапазон'],
                a_s_n=res[dc_products['Code']]['Співвідношення сигнал/шум'],
                a_audio=a_audio_,
                a_usb=a_usb_,
                a_card=a_card_,
                a_wifi=a_wifi_,
                a_bt=a_bt_,
                a_fm=a_fm_,
                a_control=a_control_,
                a_pow_ua=res[dc_products['Code']]['Живлення'],
                a_bot_ua=res[dc_products['Code']]['Матеріал корпусу'],
                a_vol=res[dc_products['Code']]['Габарити загальні'],
                a_weight=res[dc_products['Code']]['Вага загальна'],
                a_col_ua=res[dc_products['Code']]['Колір'],

                a_warr_ua=dc_products['Warranty'],
                a_warr_ru=dc_products['Warranty'],
                cover1=foto_[0],
                cover2=foto_[1],
                cover3=foto_[-1],
                )
            except Exception as e:
                print(list_, e)

        if list_['CategoryID'] == '1376':
            try:
                dc_products = list_
                #print(dc_products['Name'])

                res = get_discr_categ_dc(dict_category_periphery[dc_products['CategoryID']],
                                        dc_products['Code'])
                foto_ = dict_category_foto[dc_products['CategoryID']]
                try:
                    foto_ = foto_[dc_products['Code']]
                except:
                    foto_ = ['пусто']
                foto_ = foto_ if len(foto_) > 1 else foto_ + foto_
                temp_price = float(dc_products['PriceUSD'])

                name_ = re.sub(
                'Геймерский стол ', '', dc_products['Name'][:99]
                )
                tb_led_ = to_False_or_True(
                res[dc_products['Code']]['Світлодіодне підсвічування']
                )
                tb_h_ = to_False_or_True(
                res[dc_products['Code']]['Регулятор висоти']
                )
                tb_angle_ = to_False_or_True(
                res[dc_products['Code']]['Регулятор нахилу']
                )
                tb_up_ = to_False_or_True(
                res[dc_products['Code']]['Надставка']
                )
                tb_in_ = to_False_or_True(
                res[dc_products['Code']]['Висувна поліця для клавіатури']
                )
                tb_box_ = to_False_or_True(
                res[dc_products['Code']]['Висувні ящики']
                )
                tb_wheels_ = to_False_or_True(
                res[dc_products['Code']]["Наявність коліс"]
                )
                tb_cab_ = to_False_or_True(
                res[dc_products['Code']]['Кабельне введення']
                )
                tb_down_ = to_False_or_True(
                res[dc_products['Code']]["Підставка під системний блок"]
                )
                tb_bot_r_ua_ = to_False_or_True(
                res[dc_products['Code']]["Матеріал рами"],
                str_or_minus=True
                )

                Tables.objects.create(
                name=name_,
                category_ru='Геймерский стол',
                category_ua='Геймерський стіл',
                part_number=dc_products['Article'],
                price_rent=round(temp_price * 1.05 * 37),
                r_price=round(temp_price * 1.05 * 37),
                price_ua=round(temp_price * 37),
                price_usd=temp_price,
                vendor=dc_products['Vendor'],
                tb_format_ua=res[dc_products['Code']]['Форма'],
                tb_led=tb_led_,
                tb_h=tb_h_,
                tb_angle=tb_angle_,
                tb_up=tb_up_,
                tb_in=tb_in_,
                tb_box=tb_box_,
                tb_wheels=tb_wheels_,
                tb_cab=tb_cab_,
                tb_down=tb_down_,
                tb_bot_t_ua=res[dc_products['Code']]['Матеріал стільниці'],
                tb_bot_r_ua=tb_bot_r_ua_,
                tb_hight=res[dc_products['Code']]['Висота'],
                tb_width=res[dc_products['Code']]['Ширина'],
                tb_depth=res[dc_products['Code']]['Глибина'],
                tb_weight=res[dc_products['Code']]['Вага'],
                tb_col_ua=res[dc_products['Code']]['Колір'],

                tb_warr_ua=dc_products['Warranty'],
                tb_warr_ru=dc_products['Warranty'],
                cover1=foto_[0],
                cover2=foto_[1],
                cover3=foto_[-1],
                )
            except Exception as e:
                print(list_, e)

        if list_['CategoryID'] == '125':
            try:
                dc_products = list_
                #print(dc_products['Name'])

                res = get_discr_categ_dc(dict_category_periphery[dc_products['CategoryID']],
                                        dc_products['Code'])
                foto_ = dict_category_foto[dc_products['CategoryID']]
                try:
                    foto_ = foto_[dc_products['Code']]
                except:
                    foto_ = ['пусто']
                foto_ = foto_ if len(foto_) > 1 else foto_ + foto_
                temp_price = float(dc_products['PriceUSD'])

                name_ = re.sub(
                'Кресло для геймеров ', '', dc_products['Name'][:99]
                )
                ch_hand_ = to_False_or_True(
                res[dc_products['Code']]['Регулювання підлокітників']
                )
                ch_hight_ = to_False_or_True(
                res[dc_products['Code']]['Регулювання висоти сидіння']
                )
                try:
                    frame_ = res[dc_products['Code']]['Каркас ']
                except:
                    frame_ = '-'

                Chairs.objects.create(
                name=name_,
                category_ru='Кресло для геймеров',
                category_ua='Крісло для геймерів',
                part_number=dc_products['Article'],
                price_rent=round(temp_price * 1.05 * 37),
                r_price=round(temp_price * 1.05 * 37),
                price_ua=round(temp_price * 37),
                price_usd=temp_price,
                vendor=dc_products['Vendor'],
                ch_type_ua=res[dc_products['Code']]['Тип'],
                ch_main_ua=res[dc_products['Code']]['Основа'],
                ch_chr_ua=res[dc_products['Code']]['Хрестовина'],
                ch_mat_ua=res[dc_products['Code']]['Оббивка'],
                ch_frame_ua=frame_,
                ch_vol=res[dc_products['Code']]['Розміри сидіння'],
                ch_back=res[dc_products['Code']]['Розміри спинки'],
                ch_back_angle=res[dc_products['Code']]['Кут нахилу спинки'],
                ch_hand=ch_hand_,
                ch_hight=ch_hight_,
                ch_mech_ua=res[dc_products['Code']]['Вбудовані механізми'],
                ch_max_weight=res[dc_products['Code']]['Максимально допустиме навантаження'],
                ch_weight=res[dc_products['Code']]['Вага'],
                ch_col_ua=res[dc_products['Code']]['Колір'],

                ch_warr_ua=dc_products['Warranty'],
                ch_warr_ru=dc_products['Warranty'],
                cover1=foto_[0],
                cover2=foto_[1],
                cover3=foto_[-1],
                )
            except Exception as e:
                print(list_, e)

        if list_['CategoryID'] == '648':
            try:
                dc_products = list_
                #print(dc_products['Name'])

                res = get_discr_categ_dc(dict_category_periphery[dc_products['CategoryID']],
                                        dc_products['Code'])
                foto_ = dict_category_foto[dc_products['CategoryID']]
                try:
                    foto_ = foto_[dc_products['Code']]
                except:
                    foto_ = ['пусто']
                foto_ = foto_ if len(foto_) > 1 else foto_ + foto_
                temp_price = float(dc_products['PriceUSD'])

                name_ = re.sub(
                'Адаптер |Кабель ', '', dc_products['Name'][:99]
                )
                cab_flat_ = to_False_or_True(
                res[dc_products['Code']]['Плаский кабель']
                )
                cab_tissue_ = to_False_or_True(
                res[dc_products['Code']]['Тканинне обплетення']
                )
                cab_metal_ = to_False_or_True(
                res[dc_products['Code']]['Металеве обплетення']
                )
                cab_g_type_ = to_False_or_True(
                res[dc_products['Code']]['Г-подібний']
                )

                Cabelsplus.objects.create(
                name=name_,
                category_ru='Адаптер_Кабель',
                category_ua='Адаптер_Кабель',
                part_number=dc_products['Article'],
                price_rent=round(temp_price * 1.05 * 37),
                r_price=round(temp_price * 1.05 * 37),
                price_ua=round(temp_price * 37),
                price_usd=temp_price,
                vendor=dc_products['Vendor'],
                cab_con_f=res[dc_products['Code']]["Роз'єм 1"],
                cab_con_s=res[dc_products['Code']]["Роз'єм 2"],
                cab_conn_ua=res[dc_products['Code']]['Конектори'],
                cab_flat=cab_flat_,
                cab_tissue=cab_tissue_,
                cab_metal=cab_metal_,
                cab_g_type=cab_g_type_,
                cab_ver='-',
                cab_long=res[dc_products['Code']]['Довжина кабеля'],
                cab_col_ua=res[dc_products['Code']]['Колір'],

                cab_warr_ua=dc_products['Warranty'],
                cab_warr_ru=dc_products['Warranty'],
                cover1=foto_[0],
                cover2=foto_[1],
                cover3=foto_[-1],
                )
            except Exception as e:
                print(list_, e)

        if list_['CategoryID'] == '45':
            try:
                dc_products = list_
                #print(dc_products['Name'])

                res = get_discr_categ_dc(dict_category_periphery[dc_products['CategoryID']],
                                        dc_products['Code'])
                foto_ = dict_category_foto[dc_products['CategoryID']]
                try:
                    foto_ = foto_[dc_products['Code']]
                except:
                    foto_ = ['пусто']
                foto_ = foto_ if len(foto_) > 1 else foto_ + foto_
                temp_price = float(dc_products['PriceUSD'])

                name_ = re.sub(
                'Фильтр питания |Сетевой фильтр |Сетевой удлинитель ',
                '', dc_products['Name'][:99]
                )
                fi_con_ = to_False_or_True(
                res[dc_products['Code']]['Вимикач']
                )

                Filters.objects.create(
                name=name_,
                category_ru='Фильтр питания',
                category_ua='Фільтр живлення',
                part_number=dc_products['Article'],
                price_rent=round(temp_price * 1.05 * 37),
                r_price=round(temp_price * 1.05 * 37),
                price_ua=round(temp_price * 37),
                price_usd=temp_price,
                vendor=dc_products['Vendor'],
                fi_num=res[dc_products['Code']]["Кількість розеток"],
                fi_cab_lenght=res[dc_products['Code']]["Довжина кабеля"],
                fi_u=res[dc_products['Code']]['Робоча напруга'],
                fi_max_i=res[dc_products['Code']]['Максимальна сила струму'],
                fi_max_pow=res[dc_products['Code']]['Максимальна сумарна потужність навантаження'],
                fi_con=fi_con_,
                fi_bot_ua=res[dc_products['Code']]['Матеріал'],
                fi_col_ua=res[dc_products['Code']]['Колір'],

                fi_warr_ua=dc_products['Warranty'],
                fi_warr_ru=dc_products['Warranty'],
                cover1=foto_[0],
                cover2=foto_[1],
                cover3=foto_[-1],
                )
            except Exception as e:
                print(list_, e)

def start_tech2():
    # заливка с ДС acust(for tech) temp work

    DC_LOGIN = 'itblok'
    DC_PASSWORD = 'VIA5qPUv'

    """r = requests.post('https://api.dclink.com.ua/api/GetPriceAll', data={
        'login': DC_LOGIN,
        'password': DC_PASSWORD
    })"""
    with open('load_form_providers/dclink-price.xml', 'rb') as fobj:
        xml = fobj.read()

    list_periphery, dict_category_periphery, dict_category_foto = get_from_xml(
    xml, DC_LOGIN, DC_PASSWORD, periphery=True)

    for list_ in list_periphery:
        if list_['CategoryID'] == '25':
            try:
                dc_products = list_
                #print(dc_products['Name'])

                res = get_discr_categ_dc(dict_category_periphery[dc_products['CategoryID']],
                                        dc_products['Code'])
                foto_ = dict_category_foto[dc_products['CategoryID']]
                try:
                    foto_ = foto_[dc_products['Code']]
                except:
                    foto_ = ['пусто']
                foto_ = foto_ if len(foto_) > 1 else foto_ + foto_
                temp_price = float(dc_products['PriceUSD'])

                name_ = re.sub(
                'Акустическая система ', '', dc_products['Name'][:99]
                )
                a_usb_ = to_False_or_True(
                res[dc_products['Code']]['USB']
                )
                a_card_ = to_False_or_True(
                res[dc_products['Code']]['Кардрідер']
                )
                a_wifi_ = to_False_or_True(
                res[dc_products['Code']]['Wi-Fi']
                )
                a_bt_ = to_False_or_True(
                res[dc_products['Code']]['Bluetooth']
                )
                a_fm_ = to_False_or_True(
                res[dc_products['Code']]['FM-приймач']
                )
                a_control_ = to_False_or_True(
                res[dc_products['Code']]['Пульт ДК']
                )
                a_audio_ = to_False_or_True(
                res[dc_products['Code']]["Аудіо"],
                str_or_minus=True
                )

                Acoustics.objects.create(
                name=name_,
                category_ru='Акустическая система',
                category_ua='Акустична система',
                part_number=dc_products['Article'],
                price_rent=round(temp_price * 1.05 * 37),
                r_price=round(temp_price * 1.05 * 37),
                price_ua=round(temp_price * 37),
                price_usd=temp_price,
                vendor=dc_products['Vendor'],
                a_format=res[dc_products['Code']]['Формат акустики'],
                a_p=res[dc_products['Code']]['Потужність'],
                a_f=res[dc_products['Code']]['Частотний діапазон'],
                a_s_n=res[dc_products['Code']]['Співвідношення сигнал/шум'],
                a_audio=a_audio_,
                a_usb=a_usb_,
                a_card=a_card_,
                a_wifi=a_wifi_,
                a_bt=a_bt_,
                a_fm=a_fm_,
                a_control=a_control_,
                a_pow_ua=res[dc_products['Code']]['Живлення'],
                a_bot_ua=res[dc_products['Code']]['Матеріал корпусу'],
                a_vol=res[dc_products['Code']]['Габарити'],
                a_weight=res[dc_products['Code']]['Вага'],
                a_col_ua=res[dc_products['Code']]['Колір'],

                a_warr_ua=dc_products['Warranty'],
                a_warr_ru=dc_products['Warranty'],
                cover1=foto_[0],
                cover2=foto_[1],
                cover3=foto_[-1],
                )
            except Exception as e:
                print(list_, e)

def start_tech3():
    # заливка с ДС acust(for tech) temp work

    DC_LOGIN = 'itblok'
    DC_PASSWORD = 'VIA5qPUv'

    """r = requests.post('https://api.dclink.com.ua/api/GetPriceAll', data={
        'login': DC_LOGIN,
        'password': DC_PASSWORD
    })"""
    with open('load_form_providers/dclink-price.xml', 'rb') as fobj:
        xml = fobj.read()

    list_periphery, dict_category_periphery, dict_category_foto = get_from_xml(
    xml, DC_LOGIN, DC_PASSWORD, periphery=True)

    for list_ in list_periphery:
        if list_['CategoryID'] == '5':
            try:
                dc_products = list_
                #print(dc_products['Name'])

                res = get_discr_categ_dc(dict_category_periphery[dc_products['CategoryID']],
                                        dc_products['Code'])


                game = to_False_or_True(
                res[dc_products['Code']]["Ігрові технології"],
                str_or_minus=True
                )

                mon = Monitors.objects.filter(part_number=dc_products['Article'])
                mon.update(sc_os=game)
            except Exception as e:
                print(list_, e)


def edit_monitor():
    # доливаем параметры в моніторы: sc_os, sc_vesa (Ігрові технології, Кріплення на стіну)
    DC_LOGIN = 'itblok'
    DC_PASSWORD = 'VIA5qPUv'
    with open('load_form_providers/dclink-price.xml', 'rb') as fobj:
        xml = fobj.read()
    list_periphery, dict_category_periphery, dict_category_foto = get_from_xml(
    xml, DC_LOGIN, DC_PASSWORD, periphery=True)
    dict_res = {}
    error = set()
    for list_ in list_periphery:
        if list_['CategoryID'] == '5':
            try:
                dc_products = list_
                #print(dc_products['Name'])
                res = get_discr_categ_dc(dict_category_periphery[dc_products['CategoryID']],
                                        dc_products['Code'])
                game = to_False_or_True(
                res[dc_products['Code']]["Ігрові технології"],
                str_or_minus=True
                )
                vesa = to_False_or_True(
                res[dc_products['Code']]['VESA'],
                str_or_minus=True
                )#res[dc_products['Code']]['Кріплення на стіну']
                mon = Monitors.objects.filter(part_number=dc_products['Article'])
                _ = mon.update(sc_os=game, sc_vesa=vesa)
                dict_res[dc_products['Article']] = res
            except Exception as e:
                error.add(e)
    return (dict_res, error)


def new_mike_test():
    #
    DC_LOGIN = 'itblok'
    DC_PASSWORD = 'VIA5qPUv'
    with open('load_form_providers/dclink-price.xml', 'rb') as fobj:
        xml = fobj.read()
    list_periphery, dict_category_periphery, dict_category_foto = get_from_xml(
    xml, DC_LOGIN, DC_PASSWORD, periphery=True)
    dict_res = {}
    error = set()
    list_error = []
    for list_ in list_periphery:
        if list_['CategoryID'] == '970':
            try:
                dc_products = list_
                name_t = 'Микрофон '
                if Mike.objects.filter(part_number=dc_products['Article']).exists():
                    continue
                res, foto_, temp_price, name_ = get_foto_price_name(
                dict_category_periphery, dc_products, dict_category_foto, name_t)

                type = \
                res[dc_products['Code']]['Тип підключення']\
                 if 'Тип підключення' in res[dc_products['Code']] else '-'
                int_ = \
                res[dc_products['Code']]['Інтерфейс']\
                 if 'Інтерфейс' in res[dc_products['Code']] else '-'
                focus = \
                res[dc_products['Code']]['Спрямованість']\
                 if 'Спрямованість' in res[dc_products['Code']] else '-'
                frequency = \
                res[dc_products['Code']]['Частотний діапазон']\
                 if 'Частотний діапазон' in res[dc_products['Code']] else '-'
                db = \
                res[dc_products['Code']]['Чутливість']\
                 if 'Чутливість' in res[dc_products['Code']] else '-'
                vol = \
                res[dc_products['Code']]['Габарити']\
                 if 'Габарити' in res[dc_products['Code']] else '-'
                w = \
                res[dc_products['Code']]['Вага']\
                 if 'Вага' in res[dc_products['Code']] else '-'
                color = \
                res[dc_products['Code']]['Колір']\
                 if 'Колір' in res[dc_products['Code']] else '-'

                Mike.objects.create(
                name=name_,
                is_active=False,
                full=False,
                category_ru='Микрофон',
                category_ua='Мiкрофон',
                part_number=dc_products['Article'],
                price_rent=round(temp_price * 1.05 * 42),
                r_price=round(temp_price * 1.05 * 42),
                price_ua=round(temp_price * 42),
                price_usd=temp_price,
                vendor=key_in_dict(dc_products, 'Vendor'),
                mk_type_connect_ua=type,
                mk_type_connect_ru=type,
                mk_int=int_,
                mk_focus_ua=focus,
                mk_focus_ru=focus,
                mk_freq=frequency,
                mk_db_ua=db,
                mk_db_ru=db,
                mk_col_ua=color,
                mk_col_ru=color,
                mk_weight=w,
                mk_vol=vol,

                mk_warr_ua=key_in_dict(dc_products, 'Warranty'),
                mk_warr_ru=key_in_dict(dc_products, 'Warranty'),
                cover1=foto_[0],
                cover2=foto_[1],
                cover3=foto_[-1],
                )

                dict_res[dc_products['Article']] = res
            except Exception as e:
                error.add(e)
                list_error.append({dc_products['Article']: e})
    return (dict_res, error)

nb_list = []

def new_nb_test(nb_list):
    #
    DC_LOGIN = 'itblok'
    DC_PASSWORD = 'VIA5qPUv'
    with open('load_form_providers/dclink-price.xml', 'rb') as fobj:
        xml = fobj.read()
    list_periphery, dict_category_periphery, dict_category_foto = get_from_xml(
    xml, DC_LOGIN, DC_PASSWORD, periphery=True)
    dict_res = {}
    error = set()
    list_error = []
    for list_ in list_periphery:
        if list_['CategoryID'] == '31':
            try:
                dc_products = list_
                if dc_products['Article'] not in nb_list:
                    continue # ноутов много - для ограничения, nb_list заполняется вручную
                name_t = 'Ноутбук '
                if NB.objects.filter(part_number=dc_products['Article']).exists():
                    continue
                res, foto_, temp_price, name_ = get_foto_price_name(
                dict_category_periphery, dc_products, dict_category_foto, name_t)
                nb_class = key_in_dict_values(res[dc_products['Code']], 'Геймерські')
                sensor = key_in_dict_values(res[dc_products['Code']], 'Сенсорний екран',
                dict_values={
                'з сенсорним екраном': True, 'відсутній': False, 'default': False
                })
                surf = key_in_dict_values(res[dc_products['Code']], 'Покриття екрану',
                dict_values={
                'матове': {'ua': 'матове', 'ru': 'матовое'},
                'глянцеве': {'ua': 'глянцеве', 'ru': 'глянцевое'},
                'default': {'ua': '-', 'ru': '-'},
                })
                gpu_type = key_in_dict_values(res[dc_products['Code']], 'Тип відеокарти',
                dict_values={
                'інтегрована': {'ua': 'інтегрована', 'ru': 'интегрированная'},
                'дискретна': {'ua': 'дискретна', 'ru': 'дискретная'},
                'default': {'ua': '-', 'ru': '-'},
                })
                lan = key_in_dict(res[dc_products['Code']], 'LAN (RJ-45)')
                if lan and 'відсутній' in lan:
                    lan = '-'
                usb2 = key_in_dict(res[dc_products['Code']], 'USB 2.0')
                try:
                    usb2 = int(usb2.strip())
                except:
                    usb2 = 0
                usb3 = key_in_dict(res[dc_products['Code']], 'USB 3.2 Gen 1 (USB 3.0/3.1 Gen 1)')
                try:
                    usb3 = int(usb3.strip())
                except:
                    usb3 = 0
                usb4 = key_in_dict(res[dc_products['Code']], 'USB4')
                try:
                    usb4 = int(usb4.strip())
                except:
                    usb4 = 0
                hdmi = key_in_dict_values(res[dc_products['Code']], 'HDMI',
                dict_values={
                'є mini': True, 'є': True, 'відсутній': False,
                'microHDMI': True, 'default': False
                })
                dp = key_in_dict_values(res[dc_products['Code']], 'Display Port',
                dict_values={
                'є (mini)': True, 'є': True, 'відсутній': False,
                'є mini': True, 'default': False,
                })
                crd = key_in_dict_values(res[dc_products['Code']], 'Кардридер',
                dict_values={
                'microSD': True, 'є': True, 'Smart Card Reader': True, 'SD': True,
                'відсутній': False, 'default': False
                })
                th = key_in_dict_values(res[dc_products['Code']], 'Thunderbolt 4',
                dict_values={
                'є': True, 'відсутній': False, 'default': False
                })
                ssd = key_in_dict(res[dc_products['Code']], 'Обсяг SSD')
                if ssd == 'немає':
                    ssd = key_in_dict(res[dc_products['Code']], 'Обсяг eMMC / UFS')
                kb_light = key_in_dict_values(res[dc_products['Code']],
                'Наявність підсвічування клавіатури',
                dict_values={
                'з підсвічуванням': True, 'без підсвічування': False, 'default': False
                })
                finger = key_in_dict_values(res[dc_products['Code']],
                'Ідентифікація відбитка пальця',
                dict_values={
                'ідентифікація відбитка пальця': True, 'відсутня\t': False, 'default': False
                })
                col = key_in_dict(res[dc_products['Code']], 'Колір')
                col_ru = dict_color[col] if col in dict_color else col
                NB.objects.create(
                name=name_,
                is_active=False,
                full=False,
                category_ru='Ноутбук',
                category_ua='Ноутбук',
                part_number=dc_products['Article'],
                price_rent=round(temp_price * 1.05 * 43),
                r_price=round(temp_price * 1.05 * 43),
                price_ua=round(temp_price * 43),
                price_usd=temp_price,
                nb_vendor=key_in_dict(dc_products, 'Vendor'),
                nb_class_ua=nb_class['ua'],
                nb_class_ru=nb_class['ru'],
                nb_seria=key_in_dict(res[dc_products['Code']], 'Серія'),
                nb_sc_d=key_in_dict(res[dc_products['Code']], 'Діагональ екрану'),
                nb_sc_r=key_in_dict(res[dc_products['Code']], 'Роздільна здатність екрану'),
                nb_sc_sensor=sensor,
                nb_sc_surf_ua=surf['ua'],
                nb_sc_surf_ru=surf['ru'],
                nb_sc_h=key_in_dict(res[dc_products['Code']], 'Частота оновлення екрану'),
                nb_sc_t=key_in_dict(res[dc_products['Code']], 'Тип екрану'),
                nb_cpu_vendor=key_in_dict(res[dc_products['Code']], 'Виробник процесора'),
                nb_cpu_seria=key_in_dict(res[dc_products['Code']], 'Серія процесора'),
                nb_cpu_model=key_in_dict(res[dc_products['Code']], 'Модель процесора'),
                nb_cpu_f=key_in_dict(res[dc_products['Code']], 'Частота процесора'),
                nb_cpu_q_core=key_in_dict(res[dc_products['Code']],
                'Кількість ядер процесора'),
                nb_ram_v=key_in_dict(res[dc_products['Code']], "Об'єм оперативної пам'яті"),
                nb_ram_type=key_in_dict(res[dc_products['Code']], "Тип оперативної пам'яті"),
                nb_gpu_type_ua=gpu_type['ua'],
                nb_gpu_type_ru=gpu_type['ru'],
                nb_gpu_model=key_in_dict(res[dc_products['Code']], 'Модель відеокарти'),
                nb_gpu_vol=key_in_dict(res[dc_products['Code']], "Обсяг пам'яті відеокарти"),
                nb_wireless_wifi=key_in_dict(res[dc_products['Code']], ' Wi-Fi '),
                nb_wireless_bt=key_in_dict(res[dc_products['Code']], 'Bluetooth'),
                nb_pin_lan=lan,
                nb_pin_usb2_0=usb2,
                nb_pin_usb3_2=usb3,
                nb_pin_usb4=usb4,
                nb_pin_hdmi=hdmi,
                nb_pin_dp=dp,
                nb_pin_crd=crd,
                nb_pin_th=th,
                nb_ssd=ssd,
                nb_os=key_in_dict(res[dc_products['Code']], 'Операційна система'),
                nb_acum=key_in_dict(res[dc_products['Code']], 'Ємність акумулятору'),
                nb_kb_light=kb_light,
                nb_finger=finger,
                nb_year='2025',
                nb_col_ua=col,
                nb_col_ru=col_ru,
                nb_body_ua=key_in_dict(res[dc_products['Code']], 'Матеріал корпусу'),
                nb_body_ru=key_in_dict(res[dc_products['Code']], 'Матеріал корпусу'),
                nb_weight=key_in_dict(res[dc_products['Code']], 'Вага'),
                nb_vol=key_in_dict(res[dc_products['Code']], 'Габарити (ШхГхВ)'),
                nb_warr_ua='12',
                nb_warr_ru='12',
                cover1=foto_[0],
                cover2=foto_[1],
                cover3=foto_[-1],
                )
                dict_res[dc_products['Article']] = res
            except Exception as e:
                error.add(e)
                list_error.append({dc_products['Article']: e})
    return (dict_res, error)

    def update_nb_from_dict(dict_res, usd, rent):
        """ """
        temp_price  = get_float(dict_res['providerprice_parts'])
        price_rent_ = round(temp_price * rent * usd)
        price_ua_ = round(temp_price * usd)
        rentability_ = (rent - 1) * 100
        NB.objects.filter(name=dict_res['name_parts']
        ).update(price_rent=price_rent_,
        r_price=price_rent_,
        price_ua=price_ua_,
        price_usd=temp_price,
        rentability = rentability_,
        provider='itlink')


    def edit_nb_from_dict(dict_res, usd, rent):
        """ """
        if NB.objects.filter(name=dict_res['name_parts']).exists():
            _ = update_nb_from_dict(dict_res, usd, rent)
            return _
        temp_price  = get_float(dict_res['providerprice_parts'])
        _ = NB.objects.create(
        name=dict_res['name_parts'],
        is_active=False,
        full=False,
        category_ru='Ноутбук',
        category_ua='Ноутбук',
        part_number=dict_res['partnumber_parts'],
        price_rent=round(temp_price * rent * usd),
        r_price=round(temp_price * rent * usd),
        price_ua=round(temp_price * usd),
        rentability=(rent - 1) * 100,
        price_usd=temp_price,
        nb_vendor=dict_res['vendor'],
        nb_seria=dict_res['seria'],
        nb_sc_d=dict_res['nb_sc_d'],
        nb_cpu_vendor=dict_res['nb_cpu_vendor'],
        nb_cpu_model=dict_res['nb_cpu_model'],
        nb_ram_v=dict_res['nb_ram_v'],
        nb_os=dict_res['os'],
        nb_warr_ua='12',
        nb_warr_ru='12',
        provider='itlink',
        )
        return _

    def do_nb_from_file(dict_, usd, rent):
        """ """
        for value in dict_.values():
            _ = edit_nb_from_dict(value, usd, rent)
