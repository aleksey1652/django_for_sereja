import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
import json
import requests
import pandas as pd
import gspread
from lxml import etree
from xml.etree.ElementTree import ParseError
from bs4 import BeautifulSoup
import re
from load_form_providers.dc_descr_catalog import *
#get_from_xml_asbis2 get_from_xml_mti2 get_from_xml_edg2 price_test get_from_dc
#get_from_json_elko2

def Service():
    CREDENTIALS_FILE = 'credentials.json'
    spreadsheetId = '1U0n_v-XMcrqOyWl0oVLOBDjwl3C1hwRk45DX0bocOKQ'
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
                                                        CREDENTIALS_FILE,
                                                        ['https://www.googleapis.com/auth/spreadsheets',
                                                         'https://www.googleapis.com/auth/drive']
                                                         )
    httpAuth = credentials.authorize(httplib2.Http())
    service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)
    return service,CREDENTIALS_FILE,spreadsheetId

#service, CREDENTIALS_FILE, spreadsheetId = Service()
dict_per = {'Mouse&mats': 1199948343, 'Keyboard&set': 434282992, 'Monitor': 2047822690,
            'WiFi': 645462020, 'Headsets&audio': 1604022275, 'Электротехника': 705809254,
            'Gaiming chairs': 1609497906, 'Оргтехника': 2089149462}

def artile_test(element):
    return element if element and len(element) > 1 else ''

def price_test(element):
    if element:
        try:
            float(element)
        except:
            return 0
        return element
    else:
        return 0

def download_file(url,file_name, s=requests):
    try:
        r = s.get(url)

        with open(file_name, 'wb') as f:
            f.write(r.content)

        return file_name
    except Exception as e:
        print(e)
        return ''

def get_list_sheet(l, l2):
    results = service.spreadsheets().values().batchGet(spreadsheetId = spreadsheetId,
                                     ranges = f"{l}!{l2}",
                                     valueRenderOption = 'FORMATTED_VALUE',
                                     dateTimeRenderOption = 'FORMATTED_STRING').execute()
    return results['valueRanges'][0]['values']

def send_list(l,list_dict,l2):
    results = service.spreadsheets().values().batchUpdate(spreadsheetId = spreadsheetId, body = {
    "valueInputOption": "USER_ENTERED",
    "data": [
        {"range": f"{l}!{l2}",
         "majorDimension": "ROWS",     # Сначала заполнять строки, затем столбцы
         "values":list_dict}
             ]}).execute()

def disable_paint(num_tab, p1, p2):
    DATA = {'requests': [{'repeatCell': {'range':  { "sheetId": num_tab,'startRowIndex': p1,
            'endRowIndex': p1+2000, 'startColumnIndex': p2, 'endColumnIndex': p2+1},
            'cell':  {'userEnteredFormat': {'textFormat': {}}},'fields': 'userEnteredFormat' }}]}
    service.spreadsheets().batchUpdate(spreadsheetId = spreadsheetId, body=DATA).execute()

def send_paint(num_tab,l,p1,p2):
    for y,x in enumerate(l):
        DATA={}
        if x:
            DATA = {'requests': [{'repeatCell': {'range':  { "sheetId": num_tab,'startRowIndex': p1+y,
                    'endRowIndex': p1+1+y, 'startColumnIndex': p2, 'endColumnIndex': p2+1},
                    'cell':  {'userEnteredFormat': {'textFormat': {'foregroundColor': {'red': 1},
                    'foregroundColorStyle': {'rgbColor': {'red': 1}}}}},'fields': 'userEnteredFormat' }}]}
            service.spreadsheets().batchUpdate(spreadsheetId = spreadsheetId, body=DATA).execute()

def full_paint_price(list_dict_price, d):
    list_paint=[]
    for y in list_dict_price:
        if y[0]:
            list_paint.append(1) if y[0][1] else list_paint.append(0)
        else:
            list_paint.append(0)
    disable_paint(0, 5, d)
    send_paint(0, list_paint, 4, d)

def full_paint(list_dict, list_sheet, d):
    list_paint=[]
    for y in list_dict:
        if y[0]:
            list_paint.append(1) if y[0][1] else list_paint.append(0)
        else:
            list_paint.append(0)
    for x in list_sheet:
        disable_paint(x, 1, d)
        send_paint(x, list_paint, 1,d)

def com_list(d,l):
    for x,y in d.items():
        if x==l:
            return [d[x]]
    return ['']

def send_all(data, dict_it, list_get_list, d, wait=0):
    d_full={}
    for k in data.keys():
        list_dict = []
        list_dict_for_send = []
        for y in  data[k]:
            if y:
                list_dict.append(com_list(dict_it,y[1]))
            else:
                list_dict.append([''])
        d_full[k]=list_dict
        for x in list_dict:
            if len(x[0])>1:
                list_dict_for_send.append([x[0][0]])
            else:
                list_dict_for_send.append(x)

        if len(list_dict) == len(data[k]):
            full_paint(list_dict, [dict_per[k]],d[2]) if wait == 0 else None
            send_list(k, list_dict_for_send, d[0])
    list_dict_price = []
    list_dict_price_for_send = []
    for y in list_get_list:
        if y:
            list_dict_price.append(com_list(dict_it,y[0]))
        else:
            list_dict_price.append([''])

    for x in list_dict_price:
        if len(x[0])>1:
            list_dict_price_for_send.append([x[0][0]])
        else:
            list_dict_price_for_send.append(x)

    if len(list_dict_price) == len(list_get_list):
        full_paint_price(list_dict_price, d[3])
        send_list("Price", list_dict_price_for_send, d[1])
    return {'per': d_full,'price': list_dict_price}


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

def get_discr_categ_dc(data, data_key):
    # создает описание характеристик товара по его data_key(внутр id DC)
    data_to_temp_dict = dict()
    try:
        data_to_temp_dict['values'] = {val[0]: val[1] for val in data['values']}
        data_to_temp_dict['properties'] = {val[0]: val[1] for val in data['properties']}
        data_to_temp_dict['items'] = {val[0]: val[1] for val in data['items'][data_key]}

        dict_res = {
        v: data_to_temp_dict['values'][data_to_temp_dict['items'][k]] for k, v\
        in  data_to_temp_dict['properties'].items() if k in data_to_temp_dict['items']
        }
    except:
        dict_res = {}

    return {data_key: dict_res}

def get_from_xml(xml, DC_LOGIN, DC_PASSWORD, ff=True, periphery=False):
# 11 -mouse, 33-keyboards, 24-kovrik, 45-set filtr,
#54-webcam, 58, 648-cab, 125-kreslo, 968-komplekt, 1376- stol,
#25 akus sys,
    category_main = (
    '8', '3', '724', '1', '9', '27', '2', '23', '6',
    )

    category_periphery = (
    '11', '24', '33', '56', '125', '1410', '5', '255',
    '45', '54', '648', '125', '968', '1376', '25',
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
        return ([], {}, {})

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

def get_from_dc(content, CategoryID):
    url_item = 'https://opt.dclink.com.ua/item.htm?id='
    try:
        c = content.content
    except:
        print(f'not xml data')
        c = ''

    try:
        root = etree.fromstring(c)
    except:
        print('Wrong  data')
        return []

    l=root.getchildren()
    list_soup_dict = []
    list_index = []
    for x in l:
        d={}
        try:
            for y in x.getchildren():
                if not y.text:
                    d[y.tag] = 'None'
                else:
                    d[y.tag] = y.text
            if d['Code']:
                d['Url'] = url_item + d['Code']
            else:
                d['Url'] = ''
            if CategoryID:
                if d['CategoryID'] in CategoryID:
                    list_soup_dict.append(d)
                    list_index.append(d['Article'])
            else:
                list_soup_dict.append(d)
        except:
            print('error but next')

    return list_soup_dict, list_index


def get_from_html(filename, ff):
    try:
        with open(filename, 'rb') as fobj:
            xml = fobj.read()
    except:
        print(f'not xml file')
        xml=''

    soup = BeautifulSoup(xml, "html.parser")
    l=[]
    list_soup_dict=[]

    try:
        for x in soup.find('tr').find_all('td'):
            l.append(x.text)
        l.append('Url')
    except:
        #print('Wrong  data')
        return []

    list_soup=soup.find_all('tr')[1:]
    for x in list_soup:
        ll = []
        temp = ''
        try:
            for x,y in enumerate(x.find_all('td')):
                if x != 6:
                    ll.append(y.text)
                else:
                    ll.append(y.text)
                    temp = y.find('a').get('href')
            ll.append(temp)
        except:
            ll.append(None)
        dict_temp={}
        for n,m in zip(l,ll):
                dict_temp[n]=m
        if ff:
            if dict_temp['Article'] in ff: list_soup_dict.append(dict_temp)
        else:
            list_soup_dict.append(dict_temp)

    return list_soup_dict

def get_from_xml_brain(filename, ff):
    try:
        with open(filename, 'rb') as fobj:
            xml = fobj.read()
    except:
        print(f'not xml file')
        xml=''

    try:
        root = etree.fromstring(xml)
        rr=root.find('products')
        list1=[]
        list_soup_dict=[]

        for x in rr.getchildren():
            list1.append(x)
        for x in list1:
            di={}
            for k,v in x.attrib.items():
                if k in ['Article', 'Name', 'PriceUSD', 'Available', 'URL']:
                    di[k]=v
            if ff:
                if di['Article'] in ff: list_soup_dict.append(di)
            else:
                list_soup_dict.append(di)
    except:
        return []

    return list_soup_dict

"""def get_from_xml_asbis(filename):
    try:
        with open(filename, 'rb') as fobj:
            xml = fobj.read()
    except:
        print(f'not xml file')
        xml=''

    try:
        root = etree.fromstring(xml)
        rr=root.find('PRICES').findall('PRICE')
        list1=[]
        list_soup_dict=[]

        for x in rr:
            list1.append(x)
        for x in list1:
            di={}
            for k in x.getchildren():
                if k.tag in ['WIC', 'MY_PRICE', 'DESCRIPTION', 'AVAIL']:
                    if not k.text:
                        di[k.tag] = 'None'
                    else:
                        di[k.tag] = k.text
            list_soup_dict.append(di)
    except:
        return []

    return list_soup_dict"""

def quantity_to_avail(str_):
    # for get_from_json_elko2
    #пребразование из quantity в общий статус (yes, no)

    if str_.find('>') != -1:
        return 'yes'
    elif str_ == '0':
        return 'no'
    else:
        return 'q'

def get_from_json_elko2(r, r2,usd):
    try:
        #usd = float(usd) if usd != 0 else 1
        usd = 1
    except:
        usd = 1
    catalog = ('COC','CAS','LC3','MEM','WRA', 'MBA', 'HDS', 'VGP', 'PSU', 'SSM', 'MBI',
    'SSU', 'CPU', 'COS')
    try:
        elko = r.json()
    except:
        print(f'not json data')
        elko = ''
    try:
        elko2 = r2.json()
    except:
        print(f'not json data2')
        elko2 = ''
    list_soup_dict = []
    list_index = []

    try:
        for x in elko:
            di={}
            try:
                for k in x.keys():
                    if k in ['manufacturerCode', 'name', 'price', 'quantity',
                    'httpDescription', 'id', 'catalog', 'rrp']:
                        if not x[k]:
                            di[k] = 'None'
                        else:
                            if k != 'name':
                                di[k] = x[k]
                            else:
                                di['name_itm'] = x[k]
                try:
                    di['quantity'] = quantity_to_avail(di['quantity'])
                except:
                    di['quantity'] = 'no'
            except:
                print('error but next')
            if di:
                if di['catalog'] in catalog:
                    if di['manufacturerCode'] not in list_index:
                        di['price'] = round(float(price_test(di['price']))/usd, 1)
                        list_soup_dict.append(di)
                        list_index.append(di['manufacturerCode'])
    except:
        ptint('error in elko')
    try:
        for x in elko2:
            di={}
            try:
                for k in x.keys():
                    if k in ['manufacturerCode', 'name', 'price', 'quantity', 'httpDescription', 'id', 'catalog', 'rrp']:
                        if not x[k]:
                            di[k] = 'None'
                        else:
                            if k != 'name':
                                di[k] = x[k]
                            else:
                                di['name_itm'] = x[k]
            except:
                print('error but next')
            if di:
                if di['catalog'] in catalog:
                    if di['manufacturerCode'] not in list_index:
                        list_soup_dict.append(di)
                        list_index.append(di['manufacturerCode'])
    except:
        ptint('error in elko2')

    return list_soup_dict, list_index

def get_from_json_elko(filename, ff):
    try:
        with open('load_form_providers/elko-price.json', 'r') as write_file:
                elko=json.load(write_file)
    except:
        print(f'not json file')
        elko=''
    try:
        list_soup_dict=[]
        for x in elko:
            di={}
            for k in x.keys():
                if k in ['manufacturerCode', 'name', 'price', 'quantity', 'httpDescription', 'id']:
                    if not x[k]:
                        di[k] = 'None'
                    else:
                        di[k] = x[k]
            if ff:
                if di['manufacturerCode'] in ff:
                    di['name_itm']=di.pop('name')
                    list_soup_dict.append(di)
            else:
                list_soup_dict.append(di)
    except:
        return []

    return list_soup_dict

def get_from_xml_elko(filename, ff):
    try:
        with open(filename, 'rb') as fobj:
            xml = fobj.read()
    except:
        print(f'not xml file')
        xml=''

    try:
        root = etree.fromstring(xml)
        rr=root.find('XML').find('stock').findall('product')
        list1=[]
        list_soup_dict=[]

        for x in rr:
            list1.append(x)
        for x in list1:
            di={}
            for k in x.getchildren():
                if k.tag in ['manufacturerCode', 'productName', 'price', 'stockQuantity', 'httpDescription']:
                    if not k.text:
                        di[k.tag] = 'None'
                    else:
                        di[k.tag] = k.text
            if ff:
                if di['manufacturerCode'] in ff: list_soup_dict.append(di)
            else:
                list_soup_dict.append(di)
    except:
        return []

    return list_soup_dict

def get_from_xml_mti2(r, usd):
    url_s='https://products.mti.ua/'
    mti_dict = {
                '193': 'active_network_equipment/network_adapters/',
                '199': 'active_network_equipment/wireless_equipment/',
                '143': 'monitors/displays/', '119': 'pc_components/pc_psu/',
                '111': 'pc_components/video_cards/',
                '115': 'pc_components/hard_disks/', '118': 'pc_components/pc_cases/',
                '112': 'pc_components/motherboards/', '1668': 'pc_components/ram/',
                '116': 'pc_components/ssd_drives/', '114': 'pc_components/processors/',
                '121': 'pc_components/fan/',
                }
    try:
        xml = r.text
    except:
        print(f'not xml data')
        xml = ''

    try:
        root = etree.fromstring(xml)
        rr=root.find('result').findall('productgroup')
        list1 = []
        list_soup_dict = []
        list_index = []

        for x in rr:
            list_temp=[]
            list_temp=x.find('products').findall('product')
            for r in list_temp:
                di={}
                try:
                    for k in r.getchildren():
                        if k.tag in [
                            'prodname', 'partnum', 'price_uah', 'store', 'productgroup_id',
                            'rrp']:
                            if not k.text:
                                di[k.tag] = 'None'
                            else:
                                di[k.tag] = k.text
                    if di['productgroup_id'] in mti_dict.keys():
                        di['url'] = url_s + mti_dict[di['productgroup_id']] + '.html'
                    else:
                        di['url'] = []
                    if di['productgroup_id'] in mti_dict.keys():
                        di['price_uah'] = round(
                        float(price_test(di['price_uah']))/usd, 1)
                        list_soup_dict.append(di)
                        list_index.append(di['partnum'])
                except:
                    print('error but next')
    except Exception as e:
        print(e)
        return [],[]

    return list_soup_dict, list_index

def get_from_xml_mti(filename, ff):
    url_s='https://products.mti.ua/'
    mti_dict = {
                '193': 'active_network_equipment/network_adapters/',
                '199': 'active_network_equipment/wireless_equipment/',
                '143': 'monitors/displays/', '119': 'pc_components/pc_psu/',
                '133': 'printers_scanners/mfp/', '111': 'pc_components/video_cards/',
                '1687': 'small_computer_peripherals/insha_dribna_periferiya/',
                '115': 'pc_components/hard_disks/', '165': 'small_computer_peripherals/keyboards/',
                '118': 'pc_components/pc_cases/', '1241': 'goods_for_gamers/gamers_chairs/',
                '121': 'pc_components/housing_coolers/', '112': 'pc_components/motherboards/',
                '164': 'small_computer_peripherals/computer_mice/', '1668': 'pc_components/ram/',
                '166': 'small_computer_peripherals/keyboardmouse/',
                '171': 'small_computer_peripherals/head_microphones/',
                '134': 'printers_scanners/plotters/', '131': 'printers_scanners/printers/',
                '116': 'pc_components/ssd_drives/', '114': 'pc_components/processors/',
                '163': 'small_computer_peripherals/acoustic_speakers/'
                }
    try:
        with open(filename, 'rb') as fobj:
            xml = fobj.read()
    except:
        print(f'not xml file')
        xml=''

    try:
        root = etree.fromstring(xml)
        rr=root.find('result').findall('productgroup')
        list1=[]
        list_soup_dict=[]

        for x in rr:
            list_temp=[]
            list_temp=x.find('products').findall('product')
            for r in list_temp:
                di={}
                for k in r.getchildren():
                    if k.tag in [
                        'prodname', 'partnum', 'price_uah_order', 'store', 'productgroup_id', 'mticode'
                                ]:
                        if not k.text:
                            di[k.tag] = 'None'
                        else:
                            di[k.tag] = k.text
                if di['productgroup_id'] in mti_dict.keys() and di['mticode']:
                    di['url'] = url_s + mti_dict[di['productgroup_id']] + di['mticode'] + '.html'
                else:
                    di['url'] = []
                if ff:
                    if di['partnum'] in ff: list_soup_dict.append(di)
                else:
                    list_soup_dict.append(di)
    except Exception as e:
        print(e)
        return []

    return list_soup_dict

def get_from_xml_edg2(r):
    Subcategory = ('Блоки живлення ATX','Корпуси', 'Системи охолодження, Cooler')
    try:
        xml = r.content
    except:
        print(f'not xml data')
        xml=''

    try:
        root = etree.fromstring(xml)
        rr=root.find('items').findall('item')
        list_soup_dict = []
        list_index = []

        for x in rr:
            di={}
            try:
                for k in x.getchildren():
                    if k.tag in ['Code', 'Name', 'Price', 'StockName', 'Images', 'Subcategory', 'RRP']:
                        if k.tag == 'Images':
                            if k.getchildren():
                                temp_list = []
                                for i in k.getchildren():
                                    temp_list.append(i.text) if i.text else temp_list.append('None')
                                di[k.tag] = temp_list
                                continue
                            else:
                                di[k.tag] = []
                                continue

                        if not k.text:
                            di[k.tag] = 'None'
                        else:
                            di[k.tag] = k.text
                di['Url'] = ''
                if di['Subcategory'] in Subcategory:
                    list_soup_dict.append(di)
                    list_index.append(di['Code'])
            except:
                print('error but next')

    except:
        return []

    return list_soup_dict,list_index

def get_from_xml_edg(filename, ff):
    url_item = 'http://b2b.dako.ua/products/?brand=&word='
    try:
        with open(filename, 'rb') as fobj:
            xml = fobj.read()
    except:
        print(f'not xml file')
        xml=''

    try:
        root = etree.fromstring(xml)
        rr=root.find('items').findall('item')
        list1=[]
        list_soup_dict=[]

        for x in rr:
            list1.append(x)
        for x in list1:
            di={}
            for k in x.getchildren():
                if k.tag in ['Code', 'Name', 'Price', 'StockName', 'Images']:
                    if k.tag == 'Images':
                        if k.getchildren():
                            temp_list = []
                            for i in k.getchildren():
                                temp_list.append(i.text) if i.text else temp_list.append('None')
                            di[k.tag] = temp_list
                            continue
                        else:
                            di[k.tag] = []
                            continue

                    if not k.text:
                        di[k.tag] = 'None'
                    else:
                        di[k.tag] = k.text
            di['Url'] = url_item + re.sub(r' ', '+',di['Code'])
            if ff:
                if di['Code'] in ff: list_soup_dict.append(di)
            else:
                list_soup_dict.append(di)

    except:
        return []

    return list_soup_dict

def get_from_xml_erc(filename, ff):
    list_item = 'https://connect.erc.ua/dsk.aspx?w='
    try:
        with open(filename, 'rb') as fobj:
            xml = fobj.read()
    except:
        print(f'not xml file')
        xml=''

    try:
        root = etree.fromstring(xml)
        list1=[]
        list_soup_dict=[]

        for x in root.findall('vendor'):
            for y in x.findall('goods'):
                di={}
                for k in y.getchildren():
                    if k.tag in ['gname','code','rprice', 'sprice', 'swh']:
                        di[k.tag] = k.text
                di['url'] = list_item + di['code']
                if ff:
                    if di['code'] in ff: list_soup_dict.append(di)
                else:
                    list_soup_dict.append(di)
    except:
        return []

    return list_soup_dict

def get_from_xml_asbis(filename, ff):
    url_item = 'https://www.it4profit.com/shop/pages/catalog.xhtml?searchString='
    try:
        with open(filename, 'rb') as fobj:
            xml = fobj.read()
    except:
        print(f'not xml file')
        xml=''

    try:
        root = etree.fromstring(xml)
        rr=root.find('PRICES').findall('PRICE')
        list1=[]
        list_soup_dict=[]

        for x in rr:
            list1.append(x)
        for x in list1:
            di={}
            for k in x.getchildren():
                if k.tag in ['WIC', 'MY_PRICE', 'DESCRIPTION', 'AVAIL', 'SMALL_IMAGE', 'GROUP_NAME']:
                    if not k.text:
                        di[k.tag] = 'None'
                    else:
                        di[k.tag] = k.text
            di['Url'] = url_item + di['WIC']
            if ff:
                if di['WIC'] in ff: list_soup_dict.append(di)
            else:
                list_soup_dict.append(di)
    except:
        return []

    return list_soup_dict

def get_from_xml_asbis2(content, usd):
    GROUP_NAME = ['Monitor LCD', 'Cooling System', 'Monitor LED','CPU Desktop',
    'HDD Video Surveillance', 'SSD Client', 'Memory Desktop', 'Video Card', 'HDD NAS', 'HDD Desktop']
    url_item = 'https://www.it4profit.com/shop/pages/catalog.xhtml?searchString='
    try:
        c = content.content
    except:
        print(f'not xml data')
        c = ''

    try:
        root = etree.fromstring(c)
        rr=root.find('PRICES').findall('PRICE')
        list1 = []
        list_soup_dict = []
        list_index = []

        """for x in rr:
            list1.append(x)"""
        for x in rr:
            di={}
            try:
                for k in x.getchildren():
                    if k.tag in ['WIC', 'MY_PRICE', 'DESCRIPTION', 'AVAIL', 'SMALL_IMAGE', 'GROUP_NAME', 'RETAIL_PRICE']:
                        if not k.text:
                            di[k.tag] = 'None'
                        else:
                            if k.tag == 'MY_PRICE':
                                try:
                                    di[k.tag] = str(round(float(k.text) / usd, 1))
                                except:
                                    di[k.tag] = '0'
                            else:
                                di[k.tag] = k.text
                di['Url'] = url_item + di['WIC']
                if di['GROUP_NAME'] in GROUP_NAME:
                    list_soup_dict.append(di)
                    list_index.append(di['WIC'])
            except:
                print('error but next')
    except:
        return []

    return list_soup_dict, list_index
