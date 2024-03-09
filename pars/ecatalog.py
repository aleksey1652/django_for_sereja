import requests, re
from bs4 import BeautifulSoup
from cat.models import *
from descriptions.models import *
from pars.ecatalog_adv import *
from django.utils import timezone
#create_discr_from_cat_models
dict_name_to_discr = {
'iproc':'CPU.objects.filter(name=name_)',
'aproc':'CPU.objects.filter(name=name_)',
'cool':'Cooler.objects.filter(name=name_)',
'imb':'MB.objects.filter(name=name_)',
'amb':'MB.objects.filter(name=name_)',
'mem':'RAM.objects.filter(name=name_)',
'hdd':'HDD.objects.filter(name=name_)',
'ssd':'SSD.objects.filter(name=name_)',
'video':'GPU.objects.filter(name=name_)',
'ps':'PSU.objects.filter(name=name_)',
'vent':'FAN.objects.filter(name=name_)',
'case':'CASE.objects.filter(name=name_)',
'wifi':'WiFi.objects.filter(name=name_)',
'cables':'Cables.objects.filter(name=name_)',
'soft':'Soft.objects.filter(name=name_)',
'mon':'WiFi.objects.none()',
'km': 'WiFi.objects.none()',
'name': 'WiFi.objects.none()',
                    }

dict_art = {
'iproc':'CPU.objects.filter(part_number=art)',
'aproc':'CPU.objects.filter(part_number=art)',
'cool':'Cooler.objects.filter(part_number=art)',
'imb':'MB.objects.filter(part_number=art)',
'amb':'MB.objects.filter(part_number=art)',
'mem':'RAM.objects.filter(part_number=art)',
'hdd':'HDD.objects.filter(part_number=art)',
'ssd':'SSD.objects.filter(part_number=art)',
'video':'GPU.objects.filter(part_number=art)',
'ps':'PSU.objects.filter(part_number=art)',
'vent':'FAN.objects.filter(part_number=art)',
'case':'CASE.objects.filter(part_number=art)',
'wifi':'WiFi.objects.filter(part_number=art)',
'cables':'Cables.objects.filter(part_number=art)',
'soft':'Soft.objects.filter(part_number=art)',
'mon':'WiFi.objects.none()',
'km': 'WiFi.objects.none()',
'name': 'WiFi.objects.none()',
        }

dict_name_all = {
'iproc':'CPU.objects.all()',
'aproc':'CPU.objects.all()',
'cool':'Cooler.objects.all()',
'imb':'MB.objects.all()',
'amb':'MB.objects.all()',
'mem':'RAM.objects.all()',
'hdd':'HDD.objects.all()',
'ssd':'SSD.objects.all()',
'video':'GPU.objects.all()',
'ps':'PSU.objects.all()',
'vent':'FAN.objects.all()',
'case':'CASE.objects.all()',
'wifi':'WiFi.objects.all()',
'cables':'Cables.objects.all()',
'soft':'Soft.objects.all()',
'mon': 'WiFi.objects.none()',
'km': 'WiFi.objects.none()',
'name': 'WiFi.objects.none()',
                    }

dict_kind_to_id = {
'iproc': 'cpu_shorts',
'aproc':'cpu_shorts',
'cool':'cooler_shorts',
'imb':'mb_shorts',
'amb':'mb_shorts',
'mem':'ram_shorts',
'hdd':'hdd_shorts',
'ssd':'ssd_shorts',
'video':'gpu_shorts',
'ps':'psu_shorts',
'vent':'fan_shorts',
'case':'case_shorts',
'wifi':'wifi_shorts',
'cables':'cables_shorts',
'soft':'soft_shorts',
'mon': '',
'km': '',
'name': '',
                }

dict_name_exact = {
'iproc':'CPU.objects.filter(name__icontains=name_for_obj_last)',
'aproc':'CPU.objects.filter(name__icontains=name_for_obj_last)',
'cool':'Cooler.objects.filter(name__icontains=name_for_obj_last)',
'imb':'MB.objects.filter(name__icontains=name_for_obj_last)',
'amb':'MB.objects.filter(name__icontains=name_for_obj_last)',
'mem':'RAM.objects.filter(name__icontains=name_for_obj_last)',
'hdd':'HDD.objects.filter(name__icontains=name_for_obj_last)',
'ssd':'SSD.objects.filter(name__icontains=name_for_obj_last)',
'video':'GPU.objects.filter(name__icontains=name_for_obj_last)',
'ps':'PSU.objects.filter(name__icontains=name_for_obj_last)',
'vent':'FAN.objects.filter(name__icontains=name_for_obj_last)',
'case':'CASE.objects.filter(name__icontains=name_for_obj_last)',
'wifi':'WiFi.objects.filter(name__icontains=name_for_obj_last)',
'cables':'Cables.objects.filter(name__icontains=name_for_obj_last)',
'soft':'Soft.objects.filter(name__icontains=name_for_obj_last)',
'mon':'WiFi.objects.none()',
'km': 'WiFi.objects.none()',
'name': 'WiFi.objects.none()',
                    }

def get_by_filter(**kwargs):
    if 'name' in kwargs:
        name = kwargs['name']

        dict_v = {
        'cpu':CPU.objects.filter(name__iexact=name),
        'cooler':Cooler.objects.filter(name__iexact=name),
        'mb':MB.objects.filter(name__iexact=name),
        'ram':RAM.objects.filter(name__iexact=name),
        'hdd':HDD.objects.filter(name__iexact=name),
        'ssd':SSD.objects.filter(name__iexact=name),
        'gpu':GPU.objects.filter(name__iexact=name),
        'psu':PSU.objects.filter(name__iexact=name),
        'fan':FAN.objects.filter(name__iexact=name),
        'case':CASE.objects.filter(name__iexact=name),
        'wifi':WiFi.objects.filter(name__iexact=name),
        'cables':Cables.objects.filter(name__iexact=name),
        'soft':Soft.objects.filter(name__iexact=name)
                }

        return dict_v[kwargs['kind']]

    if 'art' in kwargs:
        art = kwargs['art']

        dict_v2 = {
        'cpu':CPU.objects.filter(part_number=art),
        'cooler':Cooler.objects.filter(part_number=art),
        'mb':MB.objects.filter(part_number=art),
        'ram':RAM.objects.filter(part_number=art),
        'hdd':HDD.objects.filter(part_number=art),
        'ssd':SSD.objects.filter(part_number=art),
        'gpu':GPU.objects.filter(part_number=art),
        'psu':PSU.objects.filter(part_number=art),
        'fan':FAN.objects.filter(part_number=art),
        'case':CASE.objects.filter(part_number=art),
        'wifi':WiFi.objects.filter(part_number=art),
        'cables':Cables.objects.filter(part_number=art),
        'soft':Soft.objects.filter(part_number=art)
                }

        return dict_v2[kwargs['kind']]

"""def get_data_by_part_number(art,kind,who):
    if who == 'pc_parts':
        pass"""

def create_discr_from_cat_models(short):
    name_ = short.name_parts
    try:
        name_for_obj_last = name_.strip().split(' ')[0]
    except:
        name_for_obj_last = 'пусто'
    try:
        art = short.partnumber_list.strip()
    except:
        art = 'пусто'
    if not short.kind:
        return 0
    descr = eval(dict_name_to_discr[short.kind])
    descr_art = eval(dict_art[short.kind])

    if not descr.exists() and not descr_art.exists():
        obj = eval(dict_name_exact[short.kind])
        try:
            obj_last = obj.first()
        except:
            obj_last = None
        if obj_last and art != 'пусто':
            object_copy = obj_last
            object_copy.name = name_
            object_copy.part_number = art
            try:
                object_copy.price = short.x_code if short.x_code else 0
            except:
                object_copy.r_price = short.x_code if short.x_code else 0
            object_copy.is_active = True
            object_copy.parts_short = short
            object_copy.pk = None #for clone object!
            object_copy.save()
            #short.__dict__[dict_kind_to_id[short.kind]] = object_copy
            #short.save()
            #print(object_copy.name)

def create_short_from_descr(name_descr, kind_descr, price_descr, art_descr):
    if not Parts_short.objects.filter(kind=kind_descr, kind2=False, name_parts=name_descr).exists():
        try:
            now = timezone.now()
            short = Parts_short.objects.create(kind=kind_descr, kind2=False, name_parts=name_descr,
            x_code=price_descr, min_price=price_descr, auto=True, partnumber_list=name_descr,
            Advanced_parts=1, date_chg = now)

            if not Parts_short.objects.filter(kind=kind_descr, kind2=False,
            parts_full__partnumber_parts=art_descr).exists():
                create_relation_from_cat_models(short)
        except:
            pass

def create_relation_from_cat_models(short):
    try:
        art = short.partnumber_list.strip()
    except:
        art = None
    if not short.parts_full.all().exists() and art:
        full = Parts_full.objects.filter(partnumber_parts=art,providers__name_provider='-')
        if full.exists():
            short.parts_full.add(full.first())
            short.save()


def get_dict(obj,dict1):
    for f in obj.findAll('tr',valign='top'):
        temp_key = f.find(class_='op1')
        temp_values = f.find(class_='op3')
        if temp_key and temp_values:
            try:
                temp_key = re.sub(r'\W+', ' ', temp_key.text)
                temp_values = re.sub(r'\W+', ' ', temp_values.text)
                dict1[temp_key] = temp_values
            except:
                print(f.find(class_='op1'),f.find(class_='op3'))
                continue

def get_url_parts(art,id_):
    url = f'https://ek.ua/ek-list.php?search_={art}&katalog_from_search_={id_}'
    response = requests.get(url)
    if response.ok:
        soup = BeautifulSoup(response.text, "html.parser")
        s_main = soup.find(class_='main-part-content') if soup else None
        s_desc=s_main.find(class_='model-short-description') if s_main else None
        if s_desc and 'data-url' in s_desc.attrs:
            return s_desc.attrs['data-url']
        else:
            return 'error: something tug exchenged'
    else:
        return 'response error'

def get_discr_ecatalog(url_parts):
    dict_parts = {}
    url = f'https://ek.ua{url_parts}'
    response = requests.get(url)
    if response.ok:
        soup = BeautifulSoup(response.text, "html.parser")
        s_main = soup.find(class_='main-part-content') if soup else None
        title = s_main.find(class_='page-title') if soup else None
        if title and 'data-txt-title' in title.attrs:
            dict_parts['титл'] =  title.attrs['data-txt-title']
        s_desc1 = s_main.find(class_='op01')
        s_desc2 = s_main.find(class_='op02')
        if s_desc1 and s_desc2:
            get_dict(s_desc1,dict_parts)
            get_dict(s_desc2,dict_parts)
        else:
            cm = s_main.find(class_='m-c-f2')
            if cm:
                for f in cm.findAll(class_='m-s-f3'):
                    temp = f.text.split(':')
                    if len(temp) == 2:
                        try:
                            temp_0 = re.sub(r'\W+', ' ', temp[0]) if isinstance(temp[0], str) else 'error'
                            temp_1 = re.sub(r'\W+', ' ', temp[1]) if isinstance(temp[1], str) else 'error'
                        except:
                            temp_0, temp_1 = 'error', 'error'
                            #print(temp[0],temp[1])
                        dict_parts[temp_0] = temp_1
            cmem = s_main.find(class_='one-col')
            if cmem:
                for f in cmem.findAll('tr',valign='top'):
                    temp = list(f.children) if f else []
                    if len(temp) == 2:
                        temp_0 = re.sub(r'\W+', ' ', temp[0].text) if isinstance(temp[0].text, str) else 'error'
                        temp_1 = re.sub(r'\W+', ' ', temp[1].text) if isinstance(temp[1].text, str) else 'error'
                        dict_parts[temp_0] = temp_1
                color = cmem.find(class_='small-col-plate2')
                try:
                    l1 = list(color.children) if color else  []
                    l1 = [l.attrs['title'] for l in l1]
                except:
                    l1 = []
                temp_color = '+'.join(l1)
                dict_parts['Цвет'] = temp_color

    return dict_parts

def get_res_ecatalog(art,kind):
    id_, fun = dict_kind_id[kind]
    url_parts = get_url_parts(art,id_)
    if url_parts and url_parts not in ('error: something tug exchenged','response error'):
        dict_ =  get_discr_ecatalog(url_parts)
        dict_for_db = eval(fun)
        return dict_for_db
    else:
        return {}
