from load_form_providers.dc import DC
from load_form_providers.asbis import ASBIS
from load_form_providers.elko import ELKO
from load_form_providers.mti import MTI
from load_form_providers.itlink import ITLINK
from load_form_providers.brain import BRAIN
from load_form_providers.edg import EDG
from load_form_providers.erc import  ERC
from django.utils import timezone
import os, django, pickle, json, re
from load_form_providers.sheet_class import *
#os.environ.setdefault('DJANGO_SETTINGS_MODULE','sereja.settings')
#django.setup()
from cat.models import *
from descriptions.models import *
from django.contrib import messages
from django.db.models import Min
import pandas as pd
from sereja.settings import BASE_DIR
import time as tme
from load_form_providers.erc2 import *
from django.db.models import Q
from django.db.models import Min
from load_form_providers.dc_descr_catalog import to_model_price_from_dc, to_tech_price_from_dc
from descriptions.views import shorts_in_comps

from load_form_providers.providers_to_price import *
#providerprice_parts x_code price aall remainder test_comp in_comps prov

def for_clear_status(part):
    """
    """
    now = timezone.now()
    list_providers = ['dc','asbis','elko','mti','brain','edg',
    'itlink','erc', 'be', 'dw', 'pccooler']
    if not Parts_full.objects.filter(partnumber_parts=part.partnumber_parts,
    providers__name_provider__in=list_providers,availability_parts='yes'
    ).exists():
        part.availability_parts = 'no'
        part.providerprice_parts = 0
        part.rrprice_parts = 0
        part.name_parts_main = None
        part.date_chg = now
        return part
    return None


def clear_status_if_not_exists():
    tuple_kind = ('cool', 'imb', 'amb', 'case', 'ssd', 'hdd', 'aproc','iproc',
    'video', 'ps', 'mem', 'vent', 'cables')

    full_update_status_no = Parts_full.objects.filter(kind__in = tuple_kind,
    providers__name_provider='-', availability_parts='yes', remainder__isnull=True)

    parts = list(full_update_status_no)

    updated_parts_ = [
        for_clear_status(part)
        for part in parts
    ]

    updated_parts = [part for part in updated_parts_ if part]

    try:
        with transaction.atomic():
            Parts_full.objects.filter(providers__name_provider='-').bulk_update(
            updated_parts, ['providerprice_parts', 'availability_parts',
            'rrprice_parts', 'date_chg', 'name_parts_main']
            )
    except:
        updated_parts = []

    return len(updated_parts)

def short_procent_diff(pr1, pr2):
    #for Short_per_x_code_single
    #pr1 = min_price,pr2 = short.parts_full.first().providerprice_parts
    try:
        pr1 = float(pr1)
        pr2 = float(pr2)
    except (ValueError, TypeError):
        return False
    if pr1 == 0:
        return True
    if pr2 == 0:
        return False
    if pr1 / pr2 < 1.15 and pr2 <= pr1 * 1.1:
        return True
    else:
        return False

def short_kind_discr(short, descr):
    kind_ = short.kind
    if kind_ in ('iproc', 'aproc'):
        short.cpu_shorts = descr
    if kind_ in ('imb', 'amb'):
        short.mb_shorts = descr
    if kind_  == 'mem':
        short.ram_shorts = descr
    if kind_  == 'cool':
        short.cooler_shorts = descr
    if kind_  == 'hdd':
        short.hdd_shorts = descr
    if kind_  == 'ssd':
        short.ssd_shorts = descr
    if kind_  == 'ps':
        short.psu_shorts = descr
    if kind_  == 'video':
        short.gpu_shorts = descr
    if kind_  == 'vent':
        short.fan_shorts = descr
    if kind_  == 'case':
        short.case_shorts = descr
    if kind_  == 'wifi':
        short.wifi_shorts = descr
    if kind_  == 'soft':
        short.soft_shorts = descr
    short.save()

dict_kind_to_discr = {
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
'soft':'Soft.objects.filter(part_number=art)'
                    }
dict_kind_to_discr_kind = {
'iproc':'cpu',
'aproc':'cpu',
'cool':'cooler',
'imb':'mb',
'amb':'mb',
'mem':'ram',
'hdd':'hdd',
'ssd':'ssd',
'video':'gpu',
'ps':'psu',
'vent':'fan',
'case':'case',
'wifi':'wifi',
'soft':'soft'
#'wifi':WiFi.objects.filter(part_number=art),
#'cables':Cables.objects.filter(part_number=art),
#'soft':Soft.objects.filter(part_number=art)   Parts_short
                    }

def remainder_price(price_):
    try:
        price = re.findall(r':(.+);', price_)[0]
        price = float(re.sub(r',','.', price))
    except:
        return 0
    return price

def test_comp(c):
    test_dict = {}
    comp_dict = {
                'proc_computers': ("CPU.objects.filter(name=c.proc_computers, is_active=True)",('aproc','iproc')),
                'mb_computers': ("MB.objects.filter(name=c.mb_computers, is_active=True)",('amb','imb')),
                'mem_computers': ("RAM.objects.filter(name=c.mem_computers, is_active=True)",('mem',)),
                'video_computers': ("GPU.objects.filter(name=c.video_computers, is_active=True)",('video',)),
                'ps_computers': ("PSU.objects.filter(name=c.ps_computers, is_active=True)",('ps',)),
                'case_computers': ("CASE.objects.filter(name=c.case_computers, is_active=True)",('case',)),
                'cool_computers': ("Cooler.objects.filter(name=c.cool_computers, is_active=True)",('cool',)),
                'vent_computers': ("FAN.objects.filter(name=c.vent_computers, is_active=True)",('vent',)),
                'wifi_computers': ("WiFi.objects.filter(name=c.wifi_computers, is_active=True)",('wifi',)),
                'soft_computers': ("Soft.objects.filter(name=c.soft_computers, is_active=True)",('soft',)),
                }
    for k,v in c.__dict__.items():
        if k in comp_dict:
            if Parts_short.objects.filter(name_parts=v,kind__in=comp_dict[k][1]):
                try:
                    short = Parts_short.objects.get(name_parts=v, kind__in=comp_dict[k][1], kind2=False)
                    stick = short.parts_full.all().count()
                    part_number = short.parts_full.first().partnumber_parts if stick else '-'
                except:
                    stick = 'bad'
                    part_number = '-'
            else:
                test_dict[k] = {'stick': 'bad', 'discr': 0, 'discr_price': 0}
                continue
            if eval(comp_dict[k][0]).exists():
                discr = eval(comp_dict[k][0]).count()
                discr_price = eval(comp_dict[k][0]).first().price
            else:
                discr, discr_price = 0, 0
            test_dict[k] = {'stick': stick, 'discr': discr, 'discr_price': discr_price, 'name': v,
            'part_number': part_number}
        if k == 'hdd_computers' and isinstance(v, str):
            for r in v.split(';'):
                try:
                    short = Parts_short.objects.get(name_parts=r,kind__in=('ssd','hdd'), kind2=False)
                    stick = short.parts_full.all().count()
                    part_number = short.parts_full.first().partnumber_parts if stick else '-'
                except:
                    stick = 'bad'
                    part_number = '-'
                if stick != 'bad' and short.kind == 'ssd':
                    discr = SSD.objects.filter(name=r, is_active=True).count()
                    discr_price = SSD.objects.filter(name=r, is_active=True).first().price if discr > 0 else 0
                elif stick != 'bad' and short.kind == 'hdd':
                    discr = HDD.objects.filter(name=r, is_active=True).count()
                    discr_price = HDD.objects.filter(name=r, is_active=True).first().price if discr > 0 else 0
                else:
                    discr, discr_price = 0, 0

                if not 'hdd1' in test_dict:
                    test_dict['hdd1'] = {'stick': stick, 'discr': discr, 'discr_price': discr_price, 'name': r,
                    'part_number': part_number}
                else:
                    test_dict['hdd2'] = {'stick': stick, 'discr': discr, 'discr_price': discr_price, 'name': r,
                    'part_number': part_number}

    return test_dict

def need_comps_update(k,k_new):
    if not isinstance(k, str):
        k = k.name_parts
    ff = Computers.objects.filter(cool_computers=k)
    if ff:
        return ff.update(cool_computers=k_new)
    ff = Computers.objects.filter(case_computers=k)
    if ff:
        return ff.update(case_computers=k_new)
    ff = Computers.objects.filter(ps_computers=k)
    if ff:
        return ff.update(ps_computers=k_new)
    ff = Computers.objects.filter(proc_computers=k)
    if ff:
        return ff.update(proc_computers=k_new)
    ff = Computers.objects.filter(mb_computers=k)
    if ff:
        return ff.update(mb_computers=k_new)
    ff = Computers.objects.filter(mem_computers=k)
    if ff:
        return ff.update(mem_computers=k_new)
    ff = Computers.objects.filter(video_computers=k)
    if ff:
        return ff.update(video_computers=k_new)
    ff = Computers.objects.filter(hdd_computers__icontains=k)
    if ff:
        for f in ff:
            temp = re.sub(k,k_new,f.hdd_computers)
            f.hdd_computers = temp
            f.save()
            return ff.count()
    return ff.count()
#
def status(avail, avail_prov):
    try:
        avail = str(avail)
    except:
        return 'no'
    dict_prov = {
                'asbis':{'звоните':'no','достаточно':'yes','мало':'q'},
                'dc':{'*****':'yes','****':'yes','***':'yes','**':'yes','*':'yes','z':'q','w':'q'},
                'elko':{'yes':'yes','no':'no', 'q': 'q'},
                'edg':{'Зарезервовано':'q','В наявності':'yes','Немає в наявності':'no', 'Очікується': 'q'},
                'brain':{'1':'q','2':'yes','3':'yes','0':'no'},
                'mti':{'8':'yes', '4':'yes', '1':'q', '9':'yes',
                '7':'yes', '5':'yes', '3':'yes',
                '50 и более':'yes', '6':'yes', '10 и более':'yes', '2':'yes'}
                }
    if avail_prov in dict_prov:
        if not avail or avail == '':
            return 'no'
        if avail_prov == 'elko':
            try:
                return dict_prov['elko'][avail]
            except:
                try:
                    temp = 'q' if int(avail) < 10 else 'yes'
                    return temp
                except:
                    return 'no'
        else:
            try:
                return dict_prov[avail_prov][avail]
            except:
                return 'no'
    else:
        return 'no'

def get_min_short(short):
    try:
        #f = float(short.parts_full.first().providerprice_parts)
        f = float(short.x_code)
        f = f if f else 100000
    except:
        return 100000
    return f

def get_min_full(full):
    try:
        if full.availability_parts == 'yes' and full.providerprice_parts:
            f = float(full.providerprice_parts)
            f = f if f else 100000
        else:
            return 100000
    except:
        return 100000
    return f

def get_min(q, s=0):
    try:
        #pr_name = Providers.objects.get(pk=q['providers_id']).name_provider
        #st = status(q['availability_parts'],pr_name)
        st = q['availability_parts']
    except:
        st = 'no'
    if s != 0:
        return st
    if st == 'yes':
        try:
            f = float(q['providerprice_parts'])
            if f == 0:
                return 100000
        except:
            return 100000
        return f
    else:
        return 100000

def get_min_price(q,art=0):
    if art != 0:
        p = q.parts_full.first().providerprice_parts
    else:
        p = q.first().providerprice_parts
    try:
        f = float(p)
    except:
        return 100000
    if f > 0:
        return f
    else:
        return 100000

def to_vent(d):
    if d.lower().find('вентилятор') != -1:
        # dc, edg
        return 'vent'
    if d.lower().find('комплект') != -1:
        #edg
        return 'vent'
    if d.lower().find('case fan') != -1:
        #elko
        return 'vent'
    if d.lower().find('кулер для корпуса') != -1:
        # brain
        return 'vent'
    return 'cool'

def to_article2_1(d,pr=1):
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
        if re.findall(r'fm3|fm2|am3|am4|9830|320|450|x470|x570|a68|x399|trx40|550|520|amd|x670|650',d.lower()):
            return 'amb'
        if re.findall(r'4005|1800|1900|61|41|81|110|310|365|360|z390|x299|410|z490|b460|z590|z690|370|470|510|b560|1200|h570|h610|b660|670|710|760|790|b750|intel',
                    d.lower()):
            return 'imb'
        else:
            return 'amb'

def get_xls():
    count = 0
    cols = [1, 2, 3,4]
    try:
        MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    except:
        print('error in MEDIA_ROOT')
    try:
        p1 = pd.read_excel(MEDIA_ROOT+'/1c.xlsx', usecols=cols,header=None)
    except Exception as e:
        print(e.__class__)
        return 1
    list_article = []
    if not Providers.objects.all().exists():
        list_prov = ['dc', 'asbis', 'elko', 'mti', 'itlink',
        'brain', 'edg', 'erc','-', 'dw', 'be', 'pccooler']
        for l in list_prov:
            Providers.objects.create(name_provider=l)
    for x in p1.iloc:
        if isinstance(x[2],str):
            pp=Parts_full.objects.filter(partnumber_parts=x[2],providers__name_provider='-')
            if pp:
                list_article.append(x[2])
                for p in pp:
                    p.remainder=f'price:{round(x[3])}; {x[4]}'
                    p.date_chg = timezone.now()
                    p.save()
                    count += 1
    pfnon=Parts_full.objects.exclude(partnumber_parts__in=list_article).exclude(remainder=None)
    for x in pfnon:
        x.remainder=None
        x.date_chg = timezone.now()
        x.save()
    print(f'1c obj add: {count}')
    if not Results.objects.filter(who='1c').exists():
        r = Results(who='1c',
        who_desc=f'1c obj add: {count}')
        r.save()
    else:
        r = Results.objects.get(who='1c')
        r.who_desc = f'1c obj add: {count}'
        r.save()
    return f'1c obj add: {count}'


def get_distrib2(kind, art, se=0,new_name=0):
    count = 0
    prov,_ = Providers.objects.get_or_create(name_provider='-')
    dict_base = {'aproc':CPU.objects.filter(part_number=art),
                'iproc':CPU.objects.filter(part_number=art),
                'amb':MB.objects.filter(part_number=art),
                'imb':MB.objects.filter(part_number=art),
                'mem':RAM.objects.filter(part_number=art),
                'hdd':HDD.objects.filter(part_number=art),
                'ssd':SSD.objects.filter(part_number=art),
                'video':GPU.objects.filter(part_number=art),
                'ps':PSU.objects.filter(part_number=art),
                'vent':FAN.objects.filter(part_number=art),
                'case':CASE.objects.filter(part_number=art),
                'wifi':WiFi.objects.filter(part_number=art),
                'cables':Cables.objects.filter(part_number=art),
                'soft':Soft.objects.filter(part_number=art),
                'cool':Cooler.objects.filter(part_number=art),
                'mon':CPU.objects.none(),
                'km':CPU.objects.none()
                }
    dict_base_name = {'aproc':CPU.objects.filter(name=se),
                'iproc':CPU.objects.filter(name=se),
                'amb':MB.objects.filter(name=se),
                'imb':MB.objects.filter(name=se),
                'mem':RAM.objects.filter(name=se),
                'hdd':HDD.objects.filter(name=se),
                'ssd':SSD.objects.filter(name=se),
                'video':GPU.objects.filter(name=se),
                'ps':PSU.objects.filter(name=se),
                'vent':FAN.objects.filter(name=se),
                'case':CASE.objects.filter(name=se),
                'wifi':WiFi.objects.filter(name=se),
                'cables':Cables.objects.filter(name=se),
                'soft':Soft.objects.filter(name=se),
                'cool':Cooler.objects.filter(name=se),
                'mon':CPU.objects.none(),
                'km':CPU.objects.none()
                }
    #if dict_base[kind].exists() and Parts_full.objects.filter(partnumber_parts=art,providers=prov).exists():
    if dict_base[kind].exists() or dict_base_name[kind] and Parts_full.objects.filter(partnumber_parts=art,providers=prov).exists():
        full = Parts_full.objects.filter(partnumber_parts=art,providers=prov).first()
        if dict_base_name[kind].count() > 1:
            for c in dict_base[kind][1:]:
                c.delete()
        if dict_base[kind].count() > 1:
            for d in dict_base[kind].all():
                try:
                    d.price = full.providerprice_parts
                except:
                    d.r_price = full.providerprice_parts
                if se:
                    d.part_number = full.partnumber_parts
                    #print(f'test get_distrib2: {full.partnumber_parts} name:{d.name},se:{se}')
                d.save()
                count += 1
        obj =  dict_base[kind].first() if not se else dict_base_name[kind].first()
        if not obj:
            return 0
        try:
            obj.price = full.providerprice_parts
        except:
            obj.r_price = full.providerprice_parts
        if se:
            obj.name = se if not new_name else new_name
            obj.part_number = full.partnumber_parts
            #print(f'test get_distrib2: {full.partnumber_parts} name:{obj.name},se:{se}')
        obj.save()
        count += 1
    return count

def price_to_distrib2():
    count_distrib = 0
    count_reserve = 0
    prov,_ = Providers.objects.get_or_create(name_provider='-')
    dict_base = {'cpu':CPU.objects.all(),
                'cooler':Cooler.objects.all(),
                'mb':MB.objects.all(),
                'ram':RAM.objects.all(),
                'hdd':HDD.objects.all(),
                'ssd':SSD.objects.all(),
                'gpu':GPU.objects.all(),
                'psu':PSU.objects.all(),
                'fan':FAN.objects.all(),
                'case':CASE.objects.all(),
                'wifi':WiFi.objects.all(),
                'cables':Cables.objects.all(),
                'soft':Soft.objects.all()}
    for x in Parts_full.objects.filter(providers=prov):
        if x.kind:
            count_distrib += get_distrib2(x.kind, x.partnumber_parts)

    for k,v in dict_base.items():
        for vv in v:
            if not Parts_full.objects.filter(partnumber_parts=vv.part_number,providers=prov).exists():
                vv.is_active = False
                vv.save()
                count_reserve += 1
    return {'count_distrib':count_distrib, 'count_reserve':count_reserve}

def exclue_string_filter(queryset, list_filter):
    video_parts_set = ('xt', 'ti', 'super')
    if not queryset.exists():
        return queryset
    kind_ = queryset.first().kind
    if kind_ in ('amb', 'imb') and 'atx' in list_filter:
        return queryset.exclude(name_parts__icontains = 'atx').exclude(name_parts__iregex=r'\d{3}m')
    if kind_ == 'video':
        res = tuple(set(video_parts_set) - set(list_filter))
        if len(res) == 3:
            return queryset.exclude(name_parts__icontains = res[0]).exclude(name_parts__icontains=res[1]).exclude(name_parts__icontains=res[2])
        elif len(res) == 2:
            return queryset.exclude(name_parts__icontains = res[0]).exclude(name_parts__icontains=res[1])
        else:
            return queryset
    else:
        return queryset

def full_from_string_filter(string_filter,queryset):

    if string_filter and string_filter.strip():
        list_filter = string_filter.split(' ')
        list_filter = [list_ for list_ in list_filter if list_]
        if list_filter:
            full = queryset.filter(name_parts__icontains = list_filter[0])
            if full.exists() and full.first().kind in ('aproc', 'iproc'):
                list_filter[-1] += ' ' #search no nessesary things'
            if full.exists() and full.first().kind == 'video':
                full = exclue_string_filter(full, list_filter) #delete no nessesary things: 'xt', 'ti', 'super'

            if full.exists() and full.first().kind in ('amb', 'imb') and 'atx' in list_filter:
                full = exclue_string_filter(full, list_filter) #delete no nessesary things: 'atx', 'M'
                for fil in [x for x in list_filter if x != 'atx'][1:]:
                    full = full.intersection(queryset.filter(name_parts__icontains=fil))
            else:
                for fil in list_filter[1:]:
                    full = full.intersection(queryset.filter(name_parts__icontains=fil))

            try:
                full_min = min(full,key=get_min_full)
            except:
                #print(string_filter)
                full_min = None
        try:
            full_min_price = full_min.providerprice_parts if full_min else 0
        except:
            #print({'error in full_min': string_filter})
            return 0, None
        full_min_price = full_min_price if full_min_price else 0
        return (full_min_price, full_min)
    else:
        return 0, None

def Short_per_price_update(short):
    # для Short_per_x_code
    # new code - обновление цен по жесткой привязке к партнамберу
    # и без short.save(), но + return short для одноврем записи в бд
    now = timezone.now()
    if short.parts_full.all().exists():
        full = short.parts_full.filter(
        availability_parts='yes').exclude(providerprice_parts=0
        ).order_by('providerprice_parts').first()
        if full:
            if short.auto == False:
                # меняет цену только при выключенной ручной цене
                short.x_code = round(full.providerprice_parts)
            else:
                short.x_code = round(short.min_price)
                short.auto = True
            short.kind2 = False # включаем если есть товар
            short.date_chg = now
            #short.save()
        else:
            search_term = short.name_parts
            queryset = Computers.objects.filter(
            Q(video_computers__exact=search_term)|
            Q(proc_computers__exact=search_term) |Q (mem_computers__exact=search_term)|
            Q(mb_computers__exact=search_term) | Q(vent_computers__exact=search_term)|
            Q(hdd_computers__icontains=search_term) | Q(cool_computers__exact=search_term)|
            Q(case_computers__exact=search_term) | Q(ps_computers__exact=search_term)|
            Q(wifi_computers__exact=search_term) | Q(soft_computers__exact=search_term)|
            Q(cables_computers__exact=search_term)
            ) # чтоб деталь из "For Today"  не отключать (см еще descriptions/views.py)
            if not queryset.exists():
            #if short.in_comps == False: # чтоб деталь из "For Today"  не отключать
                short.kind2 = True # выключаем если нет товара и не в сборке
                # инструкция для работников: ставить "в сборке" для детали
                # вручную при добавлении в комп (чтоб избежать рассинхр!)
                #short.save()
    return short

def Short_per_x_code_single(short):

    # old code - поиск замена цен по мин цене с разными партнамберами

    now = timezone.now()
    full = Parts_full.objects.filter(kind=short.kind, providers__name_provider='-', availability_parts='yes')
    price, full_min = full_from_string_filter(short.partnumber_list, full)
    if price and not Parts_short.objects.filter(kind2=False,
    parts_full__partnumber_parts=full_min.partnumber_parts).exclude(pk=short.pk).count() > 0:
        if short_procent_diff(short.min_price, price):
            short.x_code = price
            short.auto = False
        else:
            short.x_code = short.min_price
            short.auto = True
        short.date_chg = now
        short.parts_full.clear()
        short.parts_full.add(full_min)
        short.save()
    else:
        if short.parts_full.first() and short.parts_full.first().providerprice_parts and short.parts_full.first().availability_parts == 'yes':
            price = short.parts_full.first().providerprice_parts
            if short_procent_diff(short.min_price, price):
                short.x_code = price
                short.auto = False
            else:
                short.x_code = short.min_price
                short.auto = True
            short.date_chg = now
            short.save()
        else:
            short.x_code = short.min_price
            short.auto = True
            #short.parts_full.clear()
            short.date_chg = now
            short.save()

def Short_per_x_code():
    #  цены в комп детали

    CHOISE = ('cool', 'imb', 'amb', 'case', 'ssd', 'hdd', 'aproc',
    'iproc', 'video', 'ps', 'mem', 'vent', 'mon', 'wifi', 'km', 'soft', 'cables')
    #now = timezone.now()
    short_all = Parts_short.objects.exclude(
    name_parts='пусто').filter(kind__in = CHOISE)
    short_list = list(short_all)
    """for short in short_all:
        #Short_per_x_code_single(short) old code with var part_number
        Short_per_price_update(short) #new code with no var part_number
    """
    update = [Short_per_price_update(short) for short in short_list]

    with transaction.atomic():
        short_all.bulk_update(
        update, ['auto', 'x_code', 'kind2', 'date_chg']
        )

    len_ = len(update) if update else 0

    return len_


def get_itlink():
    usd = USD.objects.last()
    usd_cuurency = usd.usd if usd.usd else 37
    set_itlink = set()
    count_no, count_on = 0, 0
    dict1={'SSD':'ssd', 'Корпуса для ПК':'case',
    'Адаптери, перехідники':None, 'Аудіо- та відеопристрої': None,
    'Повербанки': None, 'Зарядні пристрої': None, 'Кишені и Rack пристрої': None,
    'Электроинструменты': None, 'Мыши': None, 'Кулери': 'cool',
    'Контроллеры, интерфейсные платы PCI, PCIE':None, 'Ноутбуки': None,
    'Клавиатуры':None, 'Хаби USB и кард-рідери':None, 'Материнські плати': 0,
    'Электросамокаты': None, 'Карманы и Rack устройства': None,
    'Вентилятори': 'vent', 'Подставки для ноутбуков': None,
    'Інше': None, 'Жорсткі диски': 'hdd', 'Портативні зарядні станції': None,
    'Відеокарти':'video', "Модулі пам'яті": 'mem', 'Ноутбуки': None,
    'Майнинг - райзери, адаптери': None, 'Маніпулятори': None,
    'Процесори': 1, 'Джерело живлення': 'ps', 'Манипуляторы': None}

    #itlink = pd.read_excel('/home/aleksey1652/Загрузки/прайс.xls', usecols=[0,2,3,6,7],header=None) erc
    try:
        MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    except:
        print('error in MEDIA_ROOT')
    try:
        #p1 = pd.read_excel(MEDIA_ROOT+'/1c.xlsx', usecols=cols,header=None)
        itlink = pd.read_excel(MEDIA_ROOT+'/прайс.xls', usecols=[0,2,3,6,8,9],header=None)
    except Exception as e:
        print(e.__class__)
        return 0, 0, 0
    itlink_=itlink.rename(columns={2:'partnumber_parts', 3:'name_parts',
            8:'providerprice_parts',6:'availability_parts',
            0:'subcategory',9:'rrp'})
    for x in itlink_.iloc:
        if isinstance(x['subcategory'],str) and x['subcategory'] in dict1:
            temp=dict1[x['subcategory']]
        elif isinstance(x['subcategory'],int):
            try:
                x['subcategory']=temp if temp not in (0,1) else to_article2_1(x["name_parts"],pr=temp)
            except:
                print(f" without category: {x['subcategory']}")
                continue
            if x['subcategory'] in ('ssd','hdd','video','cool','ps','case','iproc',
            'aproc','imb','amb','mem','vent'):
                set_itlink.add(x['partnumber_parts'])
                try:
                    pa,n,pr,av,kind,rrp = (
                    x['partnumber_parts'].strip(),
                    x['name_parts'].strip(),
                    x['providerprice_parts'],
                    x['availability_parts'],
                    x['subcategory'],
                    x['rrp'],)
                except Exception as e:
                    print(e.__class__)
                    continue
                try:
                    pr = round(float(pr))
                except:
                    pr = 0
                try:
                    rrp = round(float(rrp))
                except:
                    rrp = 0
                if isinstance(av,str) and av in (
                'есть', '10', '9', '8', '7', '6', '5', '4', '3', '2', '1'):
                    av = 'yes'
                elif isinstance(av,int) and av != 0:
                    av = 'yes'
                else:
                    av = 'q'
                #print((pa,av),end=' ')
                prov,_ = Providers.objects.get_or_create(name_provider='itlink')
                prov1 = Providers.objects.get(name_provider='-')
                p1 = Parts_full.objects.filter(partnumber_parts=pa,providers=prov)
                try:
                    a1,_ = Articles.objects.get_or_create(article=pa,item_name=n,item_price=kind)
                except:
                    a1 = Articles.objects.get(article=pa)
                if not p1:
                    p_itl = Parts_full.objects.create(name_parts=n,
                    partnumber_parts=pa,providers=prov,
                    providerprice_parts=pr,date_chg=timezone.now(),
                    availability_parts=av,kind=kind, rrprice_parts=rrp)
                    a1.parts_full.add(p_itl)
                    count_no += 1
                elif p1.count() > 0:
                    temp2 = p1.first()
                    if not a1.parts_full.filter(pk=temp2.pk):
                        a1.parts_full.add(temp2)
                    temp2.availability_parts = av
                    temp2.providerprice_parts = pr
                    temp2.rrprice_parts = rrp
                    temp2.date_chg = timezone.now()
                    temp2.kind = kind
                    temp2.save()
                    count_on += 1
                    if p1.count() > 1:
                        #print(f'count:{p1.count()} ')
                        for x in p1[1:]:
                            x.delete()
                if Parts_full.objects.filter(partnumber_parts=pa,providers=prov1).exists():
                    if av == 'yes':
                        pl = Parts_full.objects.filter(partnumber_parts=pa,providers=prov1)[0]
                        try:
                            if float(pl.providerprice_parts)!= 0 and float(pl.providerprice_parts) >= float(pr):
                                pl.providerprice_parts = pr
                                pl.rrprice_parts = rrp
                                pl.name_parts_main = 'itlink'
                                pl.availability_parts = av
                                pl.date_chg=timezone.now()
                                pl.save()
                                get_distrib2(pl.kind, pl.partnumber_parts)
                            elif float(pl.providerprice_parts) == 0 and float(pr):
                                pl.providerprice_parts = pr
                                pl.rrprice_parts = rrp
                                pl.name_parts_main = 'itlink'
                                pl.availability_parts = av
                                pl.date_chg=timezone.now()
                                pl.save()
                                get_distrib2(pl.kind, pl.partnumber_parts)
                        except:
                            print(f'error in itlink element:{pa}')
                else:
                    pr = pr if av == 'yes' else 0
                    name_parts_main = 'itlink' if av == 'yes' else None
                    p_main = Parts_full.objects.create(name_parts=n,
                    partnumber_parts=pa,providers=prov1,
                    providerprice_parts=pr,date_chg=timezone.now(),
                    availability_parts=av,kind=kind,name_parts_main=name_parts_main,
                    rrprice_parts=rrp)
                    a1.parts_full.add(p_main)
                    get_distrib2(kind,pa)
    pp = Parts_full.objects.exclude(
    partnumber_parts__in=set_itlink).filter(providers__name_provider='itlink')
    pp.update(availability_parts='no',providerprice_parts=0,date_chg = timezone.now())
    if not Results.objects.filter(who='itlink').exists():
        r = Results(who='itlink',
        who_desc=f'Itlink add: {count_no} objects, and update: {count_on} objects')
        r.save()
    else:
        r = Results.objects.get(who='itlink')
        r.who_desc = f'Itlink add: {count_no} objects, and update: {count_on} objects'
        r.save()

    Short_per_x_code()

    return count_no, count_on, pp


def Parsing_from_providers():
    """
    новый прайс-агрегатор
    сначала выключаем прайс от постачей: prov_
    потом скачиваем и формируем dict_full
    записываем в бд на основе dict_full (сначала для всех в prov_, потом для '-')
    результат проделанной работы в dict_message
    возвращаем dict_message
    доработать обязательно remainder_price !!!

    подключить:
    shorts_in_comps()
    #проверка есть ли шортс в сборках(in_comps в Parts_short)
    #to_tech_price_from_dc(for_brain=dict_) # цены-наличие в tech
    Short_per_x_code() #  цены в комп детали (после shorts_in_comps)
    """

    prov_ = ('dc', 'asbis', 'elko', 'brain', 'mti', 'edg') # кортеж для Parts_full

    Parts_full.objects.filter( # выключаем все детали из prov_ + '-'
    providers__name_provider__in=prov_ + ('-',)).update(
    availability_parts='no', providerprice_parts=0,
    rrprice_parts=0, name_parts_main=None)
    #.exclude(remainder__isnull=False) ???? исключая склад

    usd = USD.objects.last()
    usd_ua = usd.usd # курс установленный вручную из админки

    # dict_full полная библиотека от всех постачей для записи в бд
    dict_full = {
    'dc': {},
    'asbis': {},
    'elko': {},
    'brain': {},
    'mti': {},
    'edg': {},
    }

    # dict_message библиотека от всех постачей с результатами конечной работы
    dict_message = {
    'dc': '',
    'asbis': '',
    'elko': '',
    'brain': '',
    'mti': '',
    'edg': '',
    '-': '',
    }

    # dict_attr для общего доступа к методам класса From_provders_to_dict
    dict_attr = {
    'dc': 'getDC',
    'asbis': 'getASBIS',
    'elko': 'getELKO',
    'brain': 'getBRAIN',
    'mti': 'getMTI',
    'edg': 'getEDG',
    }

    # class_prov для работы с циклом обьектов класса From_provders_to_dict
    class_prov = {
    'dc': DC(),
    'asbis': ASBIS(usd_ua),
    'elko': ELKO(usd_ua),
    'brain': BRAIN(),
    'mti': MTI(usd_ua),
    'edg': EDG(),
    }

    start = timezone.now()

    for key, value in class_prov.items():
        try:
            res = value.get_sort_basa2() # скачиваем сырые данные от постачей
        except:
            tme.sleep(60)
            try:
                res = value.get_sort_basa2() # скачиваем еще раз(2-я попытка)
            except:
                res = None
        print(f'{key} data_upload: {type(res)}')
        f = From_provders_to_dict(usd_ua, res)
        dict_ = f.GetPriceAll(dict_attr[key]) # словарь с данными для отправки в бд
        print(f'{key} data_edited size: {len(dict_)}')
        dict_full[key] = dict_ # потом используем для обновл/созд '-' постача Parts_full
        dict_message[key] = currentProvToBd(dict_, key) # обновляем/создаем бд,
        # записывем в dict_message message по работе для текущего key

    dict_message['-'] = mainProvToBd(dict_full) # для '-' обновляем/создаем бд

    end = timezone.now()
    duration = str(end-start)[2:7]
    print(f'{duration} min')

    short_in  = shorts_in_comps() #проверка есть ли шортс в сборках(in_comps в Parts_short)
    print(f'shorts_in_comps: {short_in}')

    short_all = Short_per_x_code() #  цены в комп детали (после shorts_in_comps)
    print(f'Short_per_x_code: {short_all}')

    sklsdWith, sklsdOnly = bdRemainder() # обрабатываем склад
    # (из "price:2.42; 8" в providerprice_parts при надобности)
    print(f'кол склад_с_постач: {sklsdWith}, кол склад_только: {sklsdOnly}')

    count_clear = clear_status_if_not_exists() #  очистка "-" пустых
    test_sklad = f'{sklsdOnly}--clear: {count_clear}' # пока для теста очистки

    updateResults(dict_message, duration, short_all, short_in, sklsdWith, test_sklad
    ) #записываем в бд(Results.objects) dict_message и доп

    return (dict_message, duration)

# remainder
"""

"""
