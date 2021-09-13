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
from django.contrib import messages
from django.db.models import Min
import pandas as pd
from sereja.settings import BASE_DIR
import time as tme
from load_form_providers.erc2 import *

def status(avail, avail_prov):
    try:
        avail = str(avail)
    except:
        return 'no'
    dict_prov = {
                'asbis':{'звоните':'no','достаточно':'yes','мало':'q'},
                'dc':{'*****':'yes','****':'yes','***':'yes','**':'yes','*':'yes','z':'q','w':'q'},
                'elko':{'> 50':'yes','0':'no'},
                'edg':{'Зарезервировано':'q','Есть в наличии':'yes','Нет в наличии':'no'},
                'brain':{'1':'q','2':'yes','3':'yes','0':'no'},
                'mti':{'8':'q', '4':'q', '1':'q', '9':'q', '7':'q', '5':'q', '3':'q',
                '50 и более':'yes', '6':'q', '10 и более':'yes', '2':'q'}
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
        if re.findall(r'fm3|fm2|am3|am4|9830|320|450|x470|x570|a68|x399|trx40|550|520|amd',d.lower()):
            return 'amb'
        if re.findall(r'4005|1800|1900|61|81|110|310|365|360|z390|x299|410|z490|b460|z590|370|470|510|b560|1200|h570|intel',
                    d.lower()):
            return 'imb'
        else:
            return ''

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
        list_prov = ['dc', 'asbis', 'elko', 'mti', 'itlink', 'brain', 'edg', 'erc','-']
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
    if dict_base[kind].exists() and Parts_full.objects.filter(partnumber_parts=art,providers=prov).exists():
        if dict_base[kind].count() > 1:
            for c in dict_base[kind][1:]:
                c.delete()
        obj =  dict_base[kind].first() if not se else dict_base_name[kind].first()
        full = Parts_full.objects.filter(partnumber_parts=art,providers=prov).first()
        try:
            obj.price = full.providerprice_parts
        except:
            obj.r_price = full.providerprice_parts
        if se:
            obj.name = se
            obj.part_number = full.partnumber_parts
            print(f'test get_distrib2: {full.partnumber_parts} name:{obj.name},se:{se}')
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

def get_itlink():
    set_itlink = set()
    count_no, count_on = 0, 0
    dict1={'SSD':'ssd', 'Корпуса для ПК':'case', 'Адаптеры, переходники':None,
    'Мыши':None, 'Кулеры':'cool', 'Контроллеры, интерфейсные платы PCI, PCIE':None,
    'Клавиатуры':None, 'Хабы USB и кард-ридеры':None, 'Материнские платы':0,
    'Карманы и Rack устройства':None, 'Вентиляторы':None, 'Подставки для ноутбуков':None,
    'Жесткие диски':'hdd', 'Видеокарты':'video', 'Модули памяти':'mem', 'Процессоры':1, 'Источники питания':'ps'}

    #itlink = pd.read_excel('/home/aleksey1652/Загрузки/прайс.xls', usecols=[0,2,3,6,7],header=None)
    try:
        MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    except:
        print('error in MEDIA_ROOT')
    try:
        #p1 = pd.read_excel(MEDIA_ROOT+'/1c.xlsx', usecols=cols,header=None)
        itlink = pd.read_excel(MEDIA_ROOT+'/прайс.xls', usecols=[0,2,3,6,7],header=None)
    except Exception as e:
        print(e.__class__)
        return 1
    itlink_=itlink.rename(columns={2:'partnumber_parts', 3:'name_parts',
            7:'providerprice_parts',6:'availability_parts',
            0:'subcategory'})
    for x in itlink_.iloc:
        if isinstance(x['subcategory'],str) and x['subcategory'] in dict1:
            temp=dict1[x['subcategory']]
        elif isinstance(x['subcategory'],int) :
            x['subcategory']=temp if temp not in (0,1) else to_article2_1(x["name_parts"],pr=temp)
            if x['subcategory'] in ('ssd','hdd','video','cool','ps','case','iproc',
            'aproc','imb','amb','mem'):
                set_itlink.add(x['partnumber_parts'])
                pa,n,pr,av,kind = x['partnumber_parts'],x['name_parts'],x['providerprice_parts'],x['availability_parts'],x['subcategory']
                if isinstance(av,str) and av == 'есть':
                    av = 'yes'
                elif isinstance(av,int) and av == 10:
                    av = 'yes'
                else:
                    av = 'q'
                print((pa,av),end=' ')
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
                    availability_parts=av,kind=kind)
                    a1.parts_full.add(p_itl)
                    count_no += 1
                elif p1.count() > 0:
                    temp2 = p1.first()
                    if not a1.parts_full.filter(pk=temp2.pk):
                        a1.parts_full.add(temp2)
                    temp2.availability_parts = av
                    temp2.providerprice_parts = pr
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
                            if float(pl.providerprice_parts) != 0 and float(pl.providerprice_parts) > float(pr):
                                pl.providerprice_parts = pr
                                pl.name_parts_main = 'itlink'
                                pl.save()
                                get_distrib2(pl.kind, pl.partnumber_parts)
                            elif float(pl.providerprice_parts) == 0 and float(pr):
                                pl.providerprice_parts = pr
                                pl.name_parts_main = 'itlink'
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
                    availability_parts=av,kind=kind,name_parts_main=name_parts_main)
                    a1.parts_full.add(p_main)
                    get_distrib2(kind,pa)
    pp = Parts_full.objects.exclude(partnumber_parts__in=set_itlink).filter(providers__name_provider='itlink')
    pp.update(availability_parts='no',providerprice_parts='0',date_chg = timezone.now())
    if not Results.objects.filter(who='itlink').exists():
        r = Results(who='itlink',
        who_desc=f'Itlink add: {count_no} objects, and update: {count_on} objects')
        r.save()
    else:
        r = Results.objects.get(who='itlink')
        r.who_desc = f'Itlink add: {count_no} objects, and update: {count_on} objects'
        r.save()

    return count_no, count_on, pp


def RUN():
    count = 0
    d = DC()
    dict_set = {}
    try:
        usd_ua = round(d.get_exch(), 2)
        print(f'Dc Dollar/UAH : {usd_ua}')
    except:
        usd_ua = False
        print('no ua price')

    Str_ = ['dc', 'asbis', 'elko', 'mti', 'brain', 'edg']
    ok_dict = {}
    error_list=[]
    l = [DC(), ASBIS(), ELKO(usd_ua), MTI(usd_ua), BRAIN(), EDG()]

    for y,x in enumerate(l):
        try:
            #dict_set[Str_[y]] = x.get_sort_basa()
            #from load_form_providers.load_element import RUN
            test = x.get_sort_basa2()
            if not test.empty:
                dict_set[Str_[y]] = test
                count+=1
                print(f'{Str_[y]} is complite')
                ok_dict[Str_[y]] = 1
            else:
                print(f'{Str_[y]} is empty')
        except:
            print(f"Somthing wrong in {Str_[y]}")
            ok_dict[Str_[y]] = 0
            error_list.append(y)
            continue
    if error_list:
        tme.sleep(60)
        for a,b in enumerate(l):
            if a in error_list:
                try:
                    test = l[a].get_sort_basa2()
                    if not test.empty:
                        dict_set[Str_[a]] = test
                        count+=1
                        print(f'{Str_[a]} is complite')
                        ok_dict[Str_[a]] = 1
                        time.sleep(20)
                except:
                    try:
                        test = l[a].get_sort_basa2()
                        if not test.empty:
                            dict_set[Str_[a]] = test
                            count+=1
                            print(f'{Str_[a]} is complite')
                            ok_dict[Str_[a]] = 1
                            time.sleep(20)
                    except:
                        print(f"Somthing wrong in {Str_[a]}")
                        continue
    print(f'Got {str(count)} objects')
    with open('load_form_providers/dict_sort.pickle', 'wb') as f:
        pickle.dump(dict_set, f)
    print('pickle file saved')
    with open('load_form_providers/usd_ua.pickle', 'wb') as f:
        pickle.dump(usd_ua, f)
    u = USD.objects.first()
    u.usd = usd_ua
    u.save()
    print('usd_ua saved')
    print('pickle file saved')
    try:
        with open("load_form_providers/dict_sort.pickle", "rb") as f:
            dict_set=pickle.load(f)
    except:
        print('not file dict_sort.pickle')
    p=Panda_db(dict_set)
    #p.set_panda_set(dict_set)
    #basa = p.full_panda_set()

    return (p, count, ok_dict)

def Parsing_from_providers():
    brain_cat={'Процессоры':"to_article2_1(n)",'Модули памяти':"'mem'",
    'Накопители HDD - 3.5", 2.5", внутренние':"'hdd'",'Мониторы':"'mon'",
    'Материнские платы':"to_article2_1(n,pr=0)",'Корпуса':"'case'",
    'Видеокарты':"'video'",'Системы охлаждения':"'cool'",'Накопители SSD':"'ssd'",
    'Сетевое оборудование активное':"'wifi'",'Корпуса  имп.':"'ps'"}
    mti_cat={'114':"to_article2_1(n)",'1668':"'mem'",'115':"'hdd'",
    '143':"'mon'",'112':"to_article2_1(n,pr=0)",'118':"'case'",
    '111':"'video'",'116':"'ssd'",'193':"'wifi'",'119':"'ps'",'199':"'wifi'"}
    dc_cat={'1':"to_article2_1(n)",'2':"'mem'",'3':"'hdd'",
    '5':"'mon'",'6':"to_article2_1(n,pr=0)",'8':"'case'",
    '9':"'video'",'23':"'cool'",'27':"'ssd'",'255':"'wifi'",'724':"'ps'"}
    edg_cat={'Системы охлаждения, Cooler':"'cool'",'Блоки питания ATX':"'ps'",'Корпуса':"'case'"}
    elko_cat={'CPU':"to_article2_1(n)",'MEM':"'mem'",'HDS':"'hdd'",
    'LC3':"'mon'",'MBA':"'amb'",'CAS':"'case'",'VGP':"'video'",'COC':"'cool'",
    'SSM':"'ssd'",'WRA':"'wifi'",'SSU':"'ssd'",'PSU':"'ps'",'MBI':"'imb'"}
    asbis_cat={'CPU Desktop':"to_article2_1(n)",'Memory Desktop':"'mem'",
    'HDD Video Surveillance':"'hdd'",'Monitor LED':"'mon'",'Monitor LCD':"'mon'",
    'HDD NAS':"'hdd'",'Video Card':"'video'",'Cooling System':"'cool'",
    'SSD Client':"'ssd'",'HDD Desktop':"'hdd'"}
    all_cat = {'brain':brain_cat,'mti':mti_cat,'dc':dc_cat,
                'edg':edg_cat,'elko':elko_cat,'asbis':asbis_cat}
    count_on,count_no = 0,0
    count_provider = 0
    t2=timezone.now()
    r,count_provider,ok_dict = RUN()
    #os.environ.setdefault('DJANGO_SETTINGS_MODULE','sereja.settings')
    #django.setup()
    #from cat.models import *
    aall=Articles.objects.all()
    if not aall.exists():
        from load_form_providers.load_element_to_zero_db import main
        main()
    list_providers = ['dc','asbis','elko','mti','brain','edg','itlink','erc']
    if not Providers.objects.all().exists():
        for l in list_providers + ['-']:
            Providers.objects.create(name_provider=l)

    for a in aall:
        dd = Parts_full.objects.filter(partnumber_parts=a.article,providers__name_provider='-')
        if dd.count()>1:
            d = dd.delete()

    for a in aall:
        res_search = r.search(a.article)
        if res_search:
            for k,v in res_search.items():
                if isinstance(v.partnumber_parts,str):
                    try:
                        pa = v.partnumber_parts[:49]
                        n = v.name_parts[:99]
                        av = status(str(v.availability_parts), k)
                        pr = v.providerprice_parts
                    except:
                        print('error data')
                        continue
                    prov = Providers.objects.get(name_provider=k)
                    p1 = Parts_full.objects.filter(partnumber_parts=pa,providers=prov)
                    if not p1:
                        p1 = Parts_full.objects.create(name_parts=n,
                        partnumber_parts=pa,providers=prov,
                        providerprice_parts=pr,date_chg=timezone.now(),
                        availability_parts=av,kind=a.item_price)
                        a.parts_full.add(p1)
                        count_no += 1
                    elif p1.count() > 0:
                        temp = p1.first()
                        temp.availability_parts = av
                        temp.providerprice_parts = pr
                        temp.date_chg = timezone.now()
                        temp.kind = a.item_price
                        temp.save()
                        temp3 = Parts_full.objects.filter(partnumber_parts=pa,providers__name_provider='-')
                        if temp3:
                            temp3 = temp3.first()
                            temp3.date_chg = timezone.now()
                            temp3.save()
                        count_on += 1
                        if p1.count() > 1:
                            print(f'count:{p1.count()} ')
                            for x in p1[1:]:
                                x.delete()
                        if not a.parts_full.filter(providers__name_provider=k,partnumber_parts=pa).exists():
                            a.parts_full.add(temp)
            set_on=set(list_providers)
            set_search = set(res_search.keys())
            set_sub = set_on.symmetric_difference(set_search)
            no = Parts_full.objects.filter(partnumber_parts=pa,providers__name_provider__in=set_sub)
            temp3 = Parts_full.objects.filter(partnumber_parts=pa,providers__name_provider='-') if no else None
            if temp3:
                temp3 = temp3.first()
                temp3.date_chg = timezone.now()
                temp3.save()
            for n in no:
                nn = n
                nn.availability_parts = 'no'
                nn.providerprice_parts = 0
                nn.date_chg = timezone.now()
                nn.save()
                #no_set_sub.append((n.partnumber_parts,n.providers))
        else:
            p0 = Parts_full.objects.filter(partnumber_parts=a.article,providers__name_provider__in=list_providers)
            temp3 = Parts_full.objects.filter(partnumber_parts=a.article,providers__name_provider='-') if p0 else None
            if temp3:
                temp3 = temp3.first()
                temp3.date_chg = timezone.now()
                temp3.save()
            for p in p0:
                pp = p
                pp.availability_parts = 'no'
                pp.providerprice_parts = 0
                pp.date_chg = timezone.now()
                pp.save()
                #no_prov.append((p.partnumber_parts,p.providers))
        try:
            pp = Parts_full.objects.get(partnumber_parts=a.article,providers__name_provider='-')
        except:
            pp = Parts_full.objects.filter(partnumber_parts=a.article,providers__name_provider='-').first()
        if pp:
            if pp.availability_parts != 'hand':
                p_prov = Parts_full.objects.filter(partnumber_parts=a.article,
                providers__name_provider__in=('dc','asbis','elko',
                'mti','brain','edg')).values()
                p_prov_min =  min(p_prov, key=get_min) if p_prov else {'providerprice_parts':'0','availability_parts':'no'}
                price = p_prov_min['providerprice_parts'] if p_prov_min['availability_parts'] not in ('q','no','') else 0
                name_parts_main = Parts_full.objects.get(pk=p_prov_min['id']).providers.name_provider if p_prov_min['availability_parts'] not in ('q','no','') else None
                st = p_prov_min['availability_parts'] if p_prov else 'no'
                pp.providerprice_parts = price
                pp.availability_parts = st
                pp.name_parts_main = name_parts_main
                pp.save()
        else:
            p_prov = Parts_full.objects.filter(partnumber_parts=a.article,
            providers__name_provider__in=('dc','asbis','elko',
            'mti','brain','edg','itlink','erc')).values()
            p_prov_min =  min(p_prov, key=get_min) if p_prov else {'providerprice_parts':'0','availability_parts':'no'}
            price = p_prov_min['providerprice_parts'] if p_prov_min['availability_parts'] not in ('q','no','') else 0
            name_parts_main = Parts_full.objects.get(pk=p_prov_min['id']).providers.name_provider if p_prov_min['availability_parts'] not in ('q','no','') else None
            st = p_prov_min['availability_parts'] if p_prov else 'no'

            prov1 = Providers.objects.get(name_provider='-')
            if p_prov and not Parts_full.objects.filter(partnumber_parts=a.article,providers=prov1):
                kind = p_prov[0]['kind'] if p_prov[0]['kind'] else ''
                pmain = Parts_full.objects.create(name_parts=p_prov_min['name_parts'],
                partnumber_parts=a.article,providers=prov1,
                providerprice_parts=price,date_chg=timezone.now(),
                availability_parts=st,kind=kind,name_parts_main=name_parts_main)
                a.parts_full.add(pmain)

    dict_for_db = r.for_db()
    set_main_no = set()
    for k,vv in dict_for_db.items():
        for v in vv:
            try:
                pa = v.partnumber_parts[:49]
                n = v.name_parts[:99]
                av = status(str(v.availability_parts), k)
                pr = v.providerprice_parts
            except:
                print('error data')
                continue
            aa = Articles.objects.filter(article=pa)
            kind = eval(all_cat[k][v.subcategory])
            if not aa:
                a1 = Articles.objects.create(article=pa,item_name=n,item_price=kind)
            else:
                a1 = aa.first()
            prov2 = Providers.objects.get(name_provider=k)
            if not a1.parts_full.filter(partnumber_parts=pa,providers=prov2).exists() and Parts_full.objects.filter(partnumber_parts=pa,providers=prov2).exists():
                for pp in Parts_full.objects.filter(partnumber_parts=pa,providers=prov2):
                    a1.parts_full.add(pp)
                    set_main_no.add(pa)
            if not Parts_full.objects.filter(partnumber_parts=pa,providers=prov2):
                p1 = Parts_full.objects.create(name_parts=n,
                partnumber_parts=pa,providers=prov2,
                providerprice_parts=pr,date_chg=timezone.now(),
                availability_parts=av,kind=kind)
                a1.parts_full.add(p1)
                set_main_no.add(pa)
                count_no += 1
    sete = r.get_set_no()
    sete.update(set_main_no)
    #print(set_main_no)
    prov1 = Providers.objects.get(name_provider='-')
    for v in sete:
        if not Parts_full.objects.filter(partnumber_parts=v,providers=prov1):
            aa = Articles.objects.filter(article=v)
            a1 = aa.first()
            p_prov = Parts_full.objects.filter(partnumber_parts=v,
            providers__name_provider__in=('dc','asbis','elko',
            'mti','brain','edg')).values()
            p_prov_min =  min(p_prov, key=get_min) if p_prov else {'providerprice_parts':'0','availability_parts':'no'}
            price = p_prov_min['providerprice_parts'] if p_prov_min['availability_parts'] not in ('q','no','') else 0
            name_parts_main = Parts_full.objects.get(pk=p_prov_min['id']).providers.name_provider if p_prov_min['availability_parts'] not in ('q','no','') else None
            st = p_prov_min['availability_parts'] if p_prov else 'no'
            if p_prov:
                kind = p_prov[0]['kind'] if p_prov[0]['kind'] else ''
                pff = Parts_full.objects.create(name_parts=p_prov_min['name_parts'],
                partnumber_parts=v,providers=prov1,
                providerprice_parts=price,date_chg=timezone.now(),
                availability_parts=st,kind=kind,name_parts_main=name_parts_main)
                if a1:
                    a1.parts_full.add(pff)
                else:
                    a1 = Articles.objects.create(article=v,item_name=p_prov_min['name_parts'],item_price=kind)
                    a1.parts_full.add(pff)
                count_no += 1


    get_xls()
    dict_distrib = price_to_distrib2()


    print( f'From {count_provider} providers price update {count_on} and in {count_no} Parts_short add new min_price')
    with open("load_form_providers/loads/log.json", "r") as write_file:
        dict_log=json.load(write_file)
    print(f'log keys: {dict_log.keys()}')
    print(dict_distrib)
    dict_load_element = {'time': timezone.now().strftime("%d-%m-%y,%H:%M"),
    'mes': f'From {count_provider} providers price update {count_on} and in {count_no} Parts_short add new min_price'}
    dict_log['dict_load_element'] = dict_load_element
    t1=timezone.now()
    prov_message = ''
    for k,w in ok_dict.items():
        if w:
            prov_message = prov_message + f'{k} ok, '
        else:
            prov_message = prov_message + f'{k} bad, '
    if not Results.objects.filter(who='prov').exists():
        r = Results(who='prov',
        who_desc=f'Providers loads result: count_provider: {count_provider} *** {prov_message} ***, update: {count_on} obj, add: {count_no} obj, time :{str(t1-t2)[2:4]} min')
        r.save()
    else:
        r = Results.objects.get(who='prov')
        r.who_desc = f'Providers loads result: count_provider: {count_provider} *** {prov_message} ***, update: {count_on} obj, add: {count_no} obj, time :{str(t1-t2)[2:4]} min'
        r.save()
    r_oher = Results.objects.filter(who__in=('erc','itlink'))
    r_oher.update(who_desc='')
    with open("load_form_providers/loads/log.json", "w") as write_file:
        json.dump(dict_log,write_file)
    #my_time = datetime.datetime.today()
    #t2=time.strptime(my_time, "%H:%M")

    print(f"Work time {str(t1-t2)[2:4]}  minuts")
    #print(f"Program will start at {my_time}")
    #return f"Work time {(t1.tm_hour)*60+t1.tm_min-(t2.tm_hour)*60-t2.tm_min}  minuts"

def Cooler_to_db():
    pcool = pd.read_excel('load_form_providers/loads/cool_versum.xls', header=None)
    for x in pcool.iloc:
        if not isinstance(x[0],float) and not Cooler.objects.filter(name=x[2]).exists():
            Cooler.objects.create(name=x[2],part_number=x[0],vendor=x[1],price=x[3],
            desc_ukr=x[4],desc_ru=x[5],fan_type_ua=x[6],fan_type_rus=x[7],fan_spd_ua=x[8],
            fan_spd_rus=x[9],fan_noise_level=x[10],fan_size=x[11])
            print(f'created new obj: {x[2]}')

def Cpu_to_db():
    cols=[0,1,2,3,4,5,6,7,8,9,10,11,12,14,15]
    pcpu = pd.read_excel('load_form_providers/loads/cpu_versum.xls', usecols=cols,header=None)
    for x in pcpu.iloc:
        if not isinstance(x[0],float) and not CPU.objects.filter(name=x[2]).exists():
            CPU.objects.create(name=x[2],part_number=x[0],vendor=x[1],f_name=x[3],
            price=x[4],desc_ukr=x[5],desc_ru=x[6],cpu_c_t=x[7],f_cpu_c_t=x[8],
            cpu_b_f=x[9],cpu_cache=x[10],cpu_i_g_ua=x[11],cpu_i_g_rus=x[12],
            depend_from=x[14],depend_from_type=x[15])
            print(f'created new obj: {x[2]}')

def Mb_to_db():
    cols=[0,1,2,3,4,5,6,7,8,10,11]
    pmb = pd.read_excel('load_form_providers/loads/mb_versum.xls', usecols=cols,header=None)
    for x in pmb.iloc:
        if not isinstance(x[0],float) and not MB.objects.filter(name=x[3]).exists():
            MB.objects.create(part_number=x[0],vendor=x[1],main_category=x[2],name=x[3],
            price=x[4],desc_ukr=x[5],desc_ru=x[6],mb_chipset=x[7],mb_max_ram=x[8],
            depend_to=x[10],depend_to_type=x[11])
            print(f'created new obj: {x[3]}')

def Ram_to_db():
    cols=[0,1,2,3,4,5,6,7,8,9]
    pram = pd.read_excel('load_form_providers/loads/ram_versum.xls', usecols=cols,header=None)
    for x in pram.iloc:
        if not isinstance(x[0],float) and not RAM.objects.filter(name=x[2]).exists():
            RAM.objects.create(name=x[2],part_number=x[0],vendor=x[1],f_name=x[3],
            price=x[4],desc_ukr=x[5],desc_ru=x[6],
            mem_s=x[7],mem_spd=x[8],mem_l=x[9])
            print(f'created new obj: {x[2]}')

def Hdd_to_db():
    cols=[0,1,2,3,4,5,6,7,8,9,10]
    phdd = pd.read_excel('load_form_providers/loads/hdd_versum.xls', usecols=cols,header=None)
    for x in phdd.iloc:
        if not isinstance(x[0],float) and not HDD.objects.filter(name=x[2]).exists():
            HDD.objects.create(name=x[2],part_number=x[0],vendor=x[1],f_name=x[3],
            price=x[4],desc_ukr=x[5],desc_ru=x[6],
            hdd_s=x[7],hdd_spd_ua=x[8],hdd_spd_rus=x[9],hdd_ca=x[10])
            print(f'created new obj: {x[2]}')

def Psu_to_db():
    cols=[0,1,2,3,4,5,6,7,8]
    ppsu = pd.read_excel('load_form_providers/loads/psu_versum.xls', usecols=cols,header=None)
    for x in ppsu.iloc:
        if not isinstance(x[0],float) and not PSU.objects.filter(name=x[2]).exists():
            PSU.objects.create(name=x[2],part_number=x[0],vendor=x[1],price=x[3],
            desc_ukr=x[4],desc_ru=x[5],psu_p=x[6],psu_c=x[7],psu_f=x[8])
            print(f'created new obj: {x[2]}')

def Gpu_to_db():
    pgpu = pd.read_excel('load_form_providers/loads/gpu_versum.xls', header=None)
    for x in pgpu.iloc:
        if not isinstance(x[0],float) and not GPU.objects.filter(name=x[3]).exists():
            GPU.objects.create(part_number=x[0],vendor=x[1],main_category=x[2],name=x[3],
            f_name=x[4],gpu_fps=x[5],price=x[6],desc_ukr=x[7],desc_ru=x[8],
            gpu_m_s=x[9],gpu_b=x[10],gpu_cpu_spd=x[11],gpu_mem_spd=x[12])
            print(f'created new obj: {x[3]}')

def Fan_to_db():
    pfan = pd.read_excel('load_form_providers/loads/fan_versum.xls', header=None)
    for x in pfan.iloc:
        if not isinstance(x[0],float) and not FAN.objects.filter(name=x[2]).exists():
            FAN.objects.create(name=x[2],part_number=x[0],vendor=x[1],price=x[3],
            desc_ukr=x[4],desc_ru=x[5],case_fan_spd_ua=x[6],case_fan_spd_rus=x[7],
            case_fan_noise_level=x[8],case_fan_size=x[9])
            print(f'created new obj: {x[2]}')

def Case_to_db():
    pcase = pd.read_excel('load_form_providers/loads/case_versum.xls', header=None)
    for x in pcase.iloc:
        if not isinstance(x[0],float) and not CASE.objects.filter(name=x[2]).exists():
            CASE.objects.create(name=x[2],part_number=x[0],vendor=x[1],price=x[3],
            desc_ukr=x[4],desc_ru=x[5],case_s=x[6])
            print(f'created new obj: {x[2]}')

def Ssd_to_db():
    pssd = pd.read_excel('load_form_providers/loads/ssd_versum.xls', header=None)
    for x in pssd.iloc:
        if not isinstance(x[0],float) and not SSD.objects.filter(name=x[2]).exists():
            SSD.objects.create(name=x[2],part_number=x[0],vendor=x[1],f_name=x[3],
            price=x[4],desc_ukr=x[5],desc_ru=x[6],
            ssd_s=x[7],ssd_spd=x[8],ssd_r_spd=x[9],ssd_type_cells=x[10])
            print(f'created new obj: {x[2]}')
#celery -A sereja beat -l INFO
"""

terminal:
python3 manage.py runserver 0.0.0.0:8000
python3 manage.py dumpdata --exclude auth.permission --exclude contenttypes > db.json
  git:
    #git clone https://github.com/aleksey1652/django_for_sereja

    # if need
    git init

    git add -A
      #git add [file]
      #git commit -m "Commit message"
      #git push origin [master]
    git commit -m "Second version of application moved into github"
      #git remote
      #git remote remove django_for_sereja
    git remote add django_for_sereja https://github.com/aleksey1652/django_for_sereja
    git checkout -b master2 #create branch (ветка)
    #git push django_for_sereja master2
    git push --set-upstream https://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@github.com/aleksey1652/django_for_sereja.git master31
    #git fetch django_for_sereja

    #info
    git branch -r

    git branch -vv
  server:
    mc
    #git clone -b master --single-branch https://github.com/aleksey1652/django_for_sereja
    git clone -b master31 --single-branch https://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@github.com/aleksey1652/django_for_sereja.git
    cd /work/django_for_sereja
    docker-compose -f docker-compose.prod.yml down -v
    #in settings add 'versum.site' to allowed host,more: env file!!!
    docker-compose -f docker-compose.prod.yml up -d --build




docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --no-input
docker-compose -f docker-compose.prod.yml exec web bash
ssh root@185.65.245.22
docker cp /home/aleksey1652/sereja/1c.xlsx f42cc87524d6:/usr/src/sereja/media
docker-compose -f docker-compose.prod.yml up --build
docker-compose -f docker-compose.prod.yml down -v
docker-compose -f docker-compose.prod.yml up -d --build

IR-XR3000D464L16S/16GDC
*01021979a*
nC83xlpuHRjl
#token: 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
token: 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
    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
sendgrid: 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
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
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

for c in GPU.objects.all():
    if GPU.objects.filter(part_number=c.part_number).count()>1:
        print(c)
for c in Cooler.objects.filter(part_number='AQUA 240')[1:]:
    c.delete()
def prom():
    dict_base = {'aproc':CPU.objects.all(),
                'iproc':CPU.objects.all(),
                'amb':MB.objects.all(),
                'imb':MB.objects.all(),
                'mem':RAM.objects.all(),
                'hdd':HDD.objects.all(),
                'ssd':SSD.objects.all(),
                'video':GPU.objects.all(),
                'ps':PSU.objects.all(),
                'vent':FAN.objects.all(),
                'case':CASE.objects.all(),
                'wifi':WiFi.objects.all(),
                'cables':Cables.objects.all(),
                'soft':Soft.objects.all(),
                'cool':Cooler.objects.all()
                }
    for k,v in dict_base.items():
        for vv in v:
            full = Parts_full.objects.filter(partnumber_parts=vv.part_number,providers__name_provider='-')
            full = full.first()
            if full:
                if full.parts_short_set.first():
                    short = full.parts_short_set.first()
                    vv.name = short.name_parts
                    vv.save()
                    if full.parts_short_set.all().count()>1:
                        print(short)
            else:
                print(f'full error: {vv}')

def test():
    dict_base = {'aproc':CPU.objects.all(),
                'iproc':CPU.objects.all(),
                'amb':MB.objects.all(),
                'imb':MB.objects.all(),
                'mem':RAM.objects.all(),
                'hdd':HDD.objects.all(),
                'ssd':SSD.objects.all(),
                'video':GPU.objects.all(),
                'ps':PSU.objects.all(),
                'vent':FAN.objects.all(),
                'case':CASE.objects.all(),
                'wifi':WiFi.objects.all(),
                'cables':Cables.objects.all(),
                'soft':Soft.objects.all(),
                'cool':Cooler.objects.all()
                }
    for k,v in dict_base.items():
        for vv in v:
            if v.filter(part_number=vv.part_number).count()>1:
                for c in v.filter(part_number=vv.part_number)[1:]:
                    c.delete()
                    print(vv)



if dict_base[kind].count() > 1:
    for c in dict_base[kind][1:]:
        c.delete()

for c in Computers.objects.filter(pc_assembly__sites__name_sites='versum',video_computers__icontains='vega'):
    temp = c
    temp.video_computers = 'Radeon RX Vega Graphics'
    temp.save()
    print(c,c.pk, end = '       ')
for c in Computers.objects.filter(pc_assembly__sites__name_sites='versum',video_computers__icontains='hd'):
    if c.pk in list_uhd:
        c.video_computers='Intel UHD Graphics'
        c.save()
for c in Computers.objects.filter(pc_assembly__sites__name_sites='versum',pk__in=list_hd):
    print(c.name_computers)

for c in Computers.objects.filter(pc_assembly__sites__name_sites='versum',name_computers__icontains='Максимальный Игровой'):
    if c.cool_computers=='Gamemax GAMMA300 Rainbow':
        print(c)
Parts_full.objects.create(name_parts='Gamemax SX632CR 400W',
partnumber_parts='SX632CR-400W',providers=prov1,
providerprice_parts=43,date_chg=timezone.now(),
availability_parts='q',kind='case')

p_prov = Parts_full.objects.filter(partnumber_parts='YD160BBBM6IAE',
providers__name_provider__in=('dc','asbis','elko',
'mti','brain','edg','itlink','erc')).order_by('providerprice_parts')
p2 = Parts_full.objects.filter(partnumber_parts='YD160BBBM6IAE',providers__name_provider='-')
status(p_prov[0].availability_parts,p_prov[0].providers.name_provider)

Core i7 9700K BOX
BX80684I79700K
BX80684I79700KF
  """
