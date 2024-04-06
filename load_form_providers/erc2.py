import os, django, pickle, json, re
#from load_form_providers.sheet_class import *
#os.environ.setdefault('DJANGO_SETTINGS_MODULE','sereja.settings')
#django.setup() clear_status_if_not_exists get_bequiet
from cat.models import *
from django.contrib import messages
from django.db.models import Min
import pandas as pd
from sereja.settings import BASE_DIR
from django.utils import timezone

def get_status_bequiet(str_):
    # для get_DiWeave и bequiet
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

def get_kind_DW(str_):
    # для get_DiWeave из имени в кайнд

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

def get_distrib2(kind, art, se=0):
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
    if dict_base[kind].exists() and Parts_full.objects.filter(partnumber_parts=art,providers=prov).exists():
        obj =  dict_base[kind].first()
        if dict_base[kind].count() > 1:
            for c in dict_base[kind][1:]:
                c.delete()
        full = Parts_full.objects.filter(partnumber_parts=art,providers=prov).first()
        try:
            obj.price = full.providerprice_parts
        except:
            obj.r_price = full.providerprice_parts
        if se:
            obj.name = se
            obj.part_number = full.partnumber_parts
        obj.save()
        count += 1
    return count

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

def status_erc(av):
    temp = [x for x in re.findall('\d*',av) if x]
    temp = int(temp[0]) if temp else 0
    if temp <= 1 and temp != 0:
        return 'q'
    elif temp > 1:
        return 'yes'
    else:
        return 'no'

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

    # new code - обновление цен по жесткой привязке к партнамберу
    now = timezone.now()

    if short.parts_full.all().exists():
        full = short.parts_full.filter(
        availability_parts='yes').exclude(providerprice_parts=0
        ).order_by('providerprice_parts').first()
        if full:
            if short.auto == False:
                # меняет цену только при выключенной ручной цене
                short.x_code = full.providerprice_parts
            else:
                short.x_code = short.min_price
                short.auto = True
            short.date_chg = now
            short.save()

def Short_per_x_code_single(short):
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
    CHOISE = ('cool', 'imb', 'amb', 'case', 'ssd', 'hdd', 'aproc',
    'iproc', 'video', 'ps', 'mem', 'vent', 'mon', 'wifi', 'km', 'soft', 'cables')
    now = timezone.now()
    short_all = Parts_short.objects.exclude(name_parts='пусто').filter(kind2=False, kind__in = CHOISE)
    for short in short_all:
        Short_per_price_update(short) # new code
        #Short_per_x_code_single(short) old

def get_erc(usd_ex):
    usd_ex = usd_ex if usd_ex > 0 else 1
    set_erc = set()
    count_no, count_on = 0, 0
    dict1={'Накопичувачі SSD':'ssd',
           'Корпуси ПК':'case',
            'Материнські плати':0,
            "Накопичувачі HDD внутрішні комп'ютерів":'hdd',
            'Відеокарти':'video',
            'Кулери та радіатори ПК': 'cool',
            "Пам'ять оперативна DDR ПК":'mem',
            'Блоки живлення ПК':'ps',
            'Накопичувачі SSD':'ssd',
            }

    try:
        MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    except:
        print('error in MEDIA_ROOT')
    try:
        #p1 = pd.read_excel(MEDIA_ROOT+'/1c.xlsx', usecols=cols,header=None)
        erc = pd.read_excel(MEDIA_ROOT+'/прайс_erc.xls',
        usecols=[2, 3, 4, 6, 9, 10, 13],header=None)
    except Exception as e:
        print(e.__class__)
        return 0, 0, 0

    erc_=erc.rename(columns={2:'subcategory', 3:'name_parts',
            4:'partnumber_parts', 6: 'rrp', 9:'providerprice_parts',
            10: 'usd', 13:'availability_parts'})

    for x in erc_.iloc:
        if isinstance(x['subcategory'],str) and x['subcategory'] in dict1:
            temp=dict1[x['subcategory']]
            try:
                price = float(x['providerprice_parts'])
            except:
                price = 0
            try:
                rrp = float(x['rrp'])
            except:
                rrp = 0
            price = price if x['usd'] == '0' else price / usd_ex
            price = round(price, 1)
            x['subcategory']=temp if temp != 0 else to_article2_1(x["name_parts"],pr=temp)
            if x['subcategory'] in (
            'ssd','hdd','video','cool','ps','case','iproc','aproc','imb','amb','mem'):
                kind = x['subcategory']
                try:
                    pa = re.sub('\*$','',x["partnumber_parts"])[:49].strip()
                    av = status_erc(x["availability_parts"])
                except:
                    continue
                #dict_erc[key]=(x["name_parts"],x["providerprice_parts"],status_erc(x["availability_parts"]))
                if pa:
                    set_erc.add(pa)
                    try:
                        n,pr = x['name_parts'][:99].strip(), price
                    except:
                        continue
                    prov,_ = Providers.objects.get_or_create(name_provider='erc')
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
                        temp2.availability_parts = av
                        temp2.providerprice_parts = pr
                        temp2.rrprice_parts = rrp
                        temp2.date_chg = timezone.now()
                        temp2.kind = kind
                        temp2.save()
                        count_on += 1
                        if p1.count() > 1:
                            print(f'count:{p1.count()} ')
                            for x in p1[1:]:
                                x.delete()
                    if Parts_full.objects.filter(partnumber_parts=pa,providers=prov1).exists():
                        if av == 'yes':
                            pl = Parts_full.objects.filter(partnumber_parts=pa,providers=prov1)[0]
                            try:
                                if float(pl.providerprice_parts) != 0 and float(pl.providerprice_parts) >= float(pr):
                                    pl.providerprice_parts = pr
                                    pl.rrprice_parts = rrp
                                    pl.name_parts_main = 'erc'
                                    pl.availability_parts = av
                                    pl.date_chg=timezone.now()
                                    pl.save()
                                    get_distrib2(pl.kind, pl.partnumber_parts)
                                elif float(pl.providerprice_parts) == 0 and float(pr):
                                    pl.providerprice_parts = pr
                                    pl.rrprice_parts = rrp
                                    pl.name_parts_main = 'erc'
                                    pl.availability_parts = av
                                    pl.date_chg=timezone.now()
                                    pl.save()
                                    get_distrib2(pl.kind, pl.partnumber_parts)
                            except:
                                print(f'error in erc element:{pa}')
                    else:
                        pr = pr if av == 'yes' else 0
                        name_parts_main = 'erc' if av == 'yes' else None
                        p_main = Parts_full.objects.create(name_parts=n,
                        partnumber_parts=pa,providers=prov1,
                        providerprice_parts=pr,date_chg=timezone.now(),
                        availability_parts=av,kind=kind,name_parts_main=name_parts_main,
                        rrprice_parts=rrp)
                        a1.parts_full.add(p_main)
                        get_distrib2(kind,pa)
                else:
                    continue

    pp = Parts_full.objects.exclude(partnumber_parts__in=set_erc).filter(providers__name_provider='erc')
    pp.update(availability_parts='no',providerprice_parts=0,date_chg = timezone.now())
    if not Results.objects.filter(who='erc').exists():
        r = Results(who='erc',
        who_desc=f'count_no: {count_no}, count_on: {count_on}')
        r.save()
    else:
        r = Results.objects.get(who='erc')
        r.who_desc = f'ERC add: {count_no} obj, update: {count_on} obj'
        r.save()

    Short_per_x_code()

    return count_no, count_on, pp


def get_bequiet(usd_ex):
    usd_ex = usd_ex if usd_ex > 0 else 1
    set_be = set()
    count_no, count_on = 0, 0
    dict_kind = {'Блок живлення':'ps',
                'Корпус для ПК':'case',
                'Охолодження процесора':'cool',
                "Вентилятор для ПК":'vent',
                'кабель-адаптер':'cables',
                'Термопаста': 'cool',
                "Охолодження для SSD накопичувача":'vent',
                }

    try:
        MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    except:
        print('error in MEDIA_ROOT')
    try:
        #p1 = pd.read_excel(MEDIA_ROOT+'/1c.xlsx', usecols=cols,header=None)
        be = pd.read_excel(MEDIA_ROOT+'/прайс_be.xls', usecols=[0, 1, 2, 3, 4, 8],
        header=None)
    except Exception as e:
        print(e.__class__)
        return 0, 0, 0

    be_=be.rename(columns={0:'partnumber_parts', 1:'name_parts',
            2:'providerprice_parts', 3: 'rrp', 4:'availability_parts', 8: 'kind'})

    for index, x in be_.iloc[1:].iterrows():
        try:
            price = float(x['providerprice_parts'])
        except:
            price = 0
        try:
            rrp = float(x['rrp'])
        except:
            rrp = 0
        price = price / usd_ex
        price = round(price, 1)
        if isinstance(x['kind'], str) and x['kind'].strip() in dict_kind:
            kind = dict_kind[x['kind'].strip()]
            try:
                pa = re.sub('\*$','',x["partnumber_parts"]).strip()
                av = get_status_bequiet(x["availability_parts"])
            except:
                continue
            #dict_erc[key]=(x["name_parts"],x["providerprice_parts"],status_erc(x["availability_parts"]))
            if pa:
                set_be.add(pa)
                try:
                    n,pr = x['name_parts'][:99].strip(), price
                except:
                    continue
                prov,_ = Providers.objects.get_or_create(name_provider='be')
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
                    temp2.availability_parts = av
                    temp2.providerprice_parts = pr
                    temp2.rrprice_parts = rrp
                    temp2.date_chg = timezone.now()
                    temp2.kind = kind
                    temp2.save()
                    count_on += 1
                    if p1.count() > 1:
                        print(f'count:{p1.count()} ')
                        for x in p1[1:]:
                            x.delete()
                if Parts_full.objects.filter(partnumber_parts=pa,providers=prov1).exists():
                    if av == 'yes':
                        pl = Parts_full.objects.filter(partnumber_parts=pa,providers=prov1)[0]
                        try:
                            if float(pl.providerprice_parts) != 0 and float(pl.providerprice_parts) >= float(pr):
                                pl.providerprice_parts = pr
                                pl.rrprice_parts = rrp
                                pl.name_parts_main = 'be'
                                pl.availability_parts = av
                                pl.date_chg=timezone.now()
                                pl.save()
                                get_distrib2(pl.kind, pl.partnumber_parts)
                            elif float(pl.providerprice_parts) == 0 and float(pr):
                                pl.providerprice_parts = pr
                                pl.rrprice_parts = rrp
                                pl.name_parts_main = 'be'
                                pl.availability_parts = av
                                pl.date_chg=timezone.now()
                                pl.save()
                                get_distrib2(pl.kind, pl.partnumber_parts)
                        except:
                            print(f'error in be element:{pa}')
                else:
                    pr = pr if av == 'yes' else 0
                    name_parts_main = 'be' if av == 'yes' else None
                    p_main = Parts_full.objects.create(name_parts=n,
                    partnumber_parts=pa,providers=prov1,
                    providerprice_parts=pr,date_chg=timezone.now(),
                    availability_parts=av,kind=kind,name_parts_main=name_parts_main,
                    rrprice_parts=rrp)
                    a1.parts_full.add(p_main)
                    get_distrib2(kind,pa)
            else:
                continue

    pp = Parts_full.objects.exclude(partnumber_parts__in=set_be).filter(
    providers__name_provider='be')
    pp.update(availability_parts='no',providerprice_parts=0,date_chg = timezone.now())
    if not Results.objects.filter(who='be').exists():
        r = Results(who='be',
        who_desc=f'count_no: {count_no}, count_on: {count_on}')
        r.save()
    else:
        r = Results.objects.get(who='be')
        r.who_desc = f'Be_quiet add: {count_no} obj, update: {count_on} obj'
        r.save()

    Short_per_x_code()

    return count_no, count_on, pp


def get_DiWeave(usd_ex):
    usd_ex = usd_ex if usd_ex > 0 else 1
    set_be = set()
    count_no, count_on = 0, 0

    try:
        MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    except:
        print('error in MEDIA_ROOT')
    try:
        #p1 = pd.read_excel(MEDIA_ROOT+'/1c.xlsx', usecols=cols,header=None)
        dw = pd.read_excel(MEDIA_ROOT+'/прайс_DiWeave.xlsx',
        usecols=[0, 3, 4, 5, 7],header=None)
    except Exception as e:
        print(e.__class__)
        return 0, 0, 0

    be_=dw.rename(columns={0:'partnumber_parts', 3:'name_parts',
            4:'providerprice_parts', 5: 'rrp', 7:'availability_parts'})

    for index, x in be_.iloc[1:].iterrows():
        try:
            price = float(x['providerprice_parts'])
        except:
            price = 0
        try:
            rrp = float(x['rrp'])
        except:
            rrp = 0
        price = price / usd_ex
        price = round(price, 1)
        kind_ = get_kind_DW(x['name_parts'])
        if kind_:
            kind = kind_
            try:
                pa = re.sub('\*$','',x["partnumber_parts"]).strip()
                av = get_status_bequiet(x["availability_parts"])
            except:
                continue
            #dict_erc[key]=(x["name_parts"],x["providerprice_parts"],status_erc(x["availability_parts"]))
            if pa:
                set_be.add(pa)
                try:
                    n,pr = x['name_parts'][:99].strip(), price
                except:
                    continue
                prov,_ = Providers.objects.get_or_create(name_provider='dw')
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
                    temp2.availability_parts = av
                    temp2.providerprice_parts = pr
                    temp2.rrprice_parts = rrp
                    temp2.date_chg = timezone.now()
                    temp2.kind = kind
                    temp2.save()
                    count_on += 1
                    if p1.count() > 1:
                        print(f'count:{p1.count()} ')
                        for x in p1[1:]:
                            x.delete()
                if Parts_full.objects.filter(partnumber_parts=pa,providers=prov1).exists():
                    if av == 'yes':
                        pl = Parts_full.objects.filter(partnumber_parts=pa,providers=prov1)[0]
                        try:
                            if float(pl.providerprice_parts) != 0 and float(pl.providerprice_parts) >= float(pr):
                                pl.providerprice_parts = pr
                                pl.rrprice_parts = rrp
                                pl.name_parts_main = 'dw'
                                pl.availability_parts = av
                                pl.date_chg=timezone.now()
                                pl.save()
                                get_distrib2(pl.kind, pl.partnumber_parts)
                            elif float(pl.providerprice_parts) == 0 and float(pr):
                                pl.providerprice_parts = pr
                                pl.rrprice_parts = rrp
                                pl.name_parts_main = 'dw'
                                pl.availability_parts = av
                                pl.date_chg=timezone.now()
                                pl.save()
                                get_distrib2(pl.kind, pl.partnumber_parts)
                        except:
                            print(f'error in dw element:{pa}')
                else:
                    pr = pr if av == 'yes' else 0
                    name_parts_main = 'dw' if av == 'yes' else None
                    p_main = Parts_full.objects.create(name_parts=n,
                    partnumber_parts=pa,providers=prov1,
                    providerprice_parts=pr,date_chg=timezone.now(),
                    availability_parts=av,kind=kind,name_parts_main=name_parts_main,
                    rrprice_parts=rrp)
                    a1.parts_full.add(p_main)
                    get_distrib2(kind,pa)
            else:
                continue

    pp = Parts_full.objects.exclude(partnumber_parts__in=set_be).filter(
    providers__name_provider='dw')
    pp.update(availability_parts='no',providerprice_parts=0,date_chg = timezone.now())
    if not Results.objects.filter(who='dw').exists():
        r = Results(who='dw',
        who_desc=f'count_no: {count_no}, count_on: {count_on}')
        r.save()
    else:
        r = Results.objects.get(who='dw')
        r.who_desc = f'DiWeave add: {count_no} obj, update: {count_on} obj'
        r.save()

    Short_per_x_code()

    return count_no, count_on, pp
