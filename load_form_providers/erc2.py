import os, django, pickle, json, re
#from load_form_providers.sheet_class import *
#os.environ.setdefault('DJANGO_SETTINGS_MODULE','sereja.settings')
#django.setup()
from cat.models import *
from django.contrib import messages
from django.db.models import Min
import pandas as pd
from sereja.settings import BASE_DIR
from django.utils import timezone

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

def status_erc(av):
    temp = [x for x in re.findall('\d*',av) if x]
    temp = int(temp[0]) if temp else 0
    if temp <= 20 and temp != 0:
        return 'q'
    elif temp >= 20:
        return 'yes'
    else:
        return 'no'

def get_erc():
    set_erc = set()
    count_no, count_on = 0, 0
    dict1={'Накопичувачі SSD':'ssd',
           'Корпуси для ПК':'case',
            'Материнські плати':0,
            'Накопичувачі HDD для комп`ютерів':'hdd',
            'Відеокарти':'video',
            "Пам'ять DDR для ПК":'mem',
            'Блоки живлення':'ps',
            'Монітори':'mon',
            'Накопители SSD':'ssd',
            'Корпуса к ПК':'case',
            'Материнские платы':0,
            'Накопители HDD для компьютеров':'hdd',
            'Видеокарты':'video',
            "Память DDR для ПК":'mem',
            'Блоки питания':'ps',
            'Мониторы':'mon'}

    try:
        MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    except:
        print('error in MEDIA_ROOT')
    try:
        #p1 = pd.read_excel(MEDIA_ROOT+'/1c.xlsx', usecols=cols,header=None)
        erc = pd.read_excel(MEDIA_ROOT+'/прайс_erc.xls', usecols=[2,3,4,8,12],header=None)
    except Exception as e:
        print(e.__class__)
        return 1

    erc_=erc.rename(columns={2:'subcategory', 3:'name_parts',
            4:'partnumber_parts',8:'providerprice_parts',
            12:'availability_parts'})

    for x in erc_.iloc:
        if isinstance(x['subcategory'],str) and x["partnumber_parts"] and x['subcategory'] in dict1:
            kind = dict1[x['subcategory']] if dict1[x['subcategory']] != 0 else to_article2_1(x["name_parts"],pr=0)
            pa = re.sub('\*$','',x["partnumber_parts"])[:49]
            av = status_erc(x["availability_parts"])
            #dict_erc[key]=(x["name_parts"],x["providerprice_parts"],status_erc(x["availability_parts"]))
            if pa:
                set_erc.add(pa)
                n,pr = x['name_parts'][:99],x['providerprice_parts']
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
                    availability_parts=av,kind=kind)
                    a1.parts_full.add(p_itl)
                    count_no += 1
                elif p1.count() > 0:
                    temp2 = p1.first()
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
                                pl.name_parts_main = 'erc'
                                pl.save()
                            elif float(pl.providerprice_parts) == 0 and float(pr):
                                pl.providerprice_parts = pr
                                pl.name_parts_main = 'erc'
                                pl.save()
                        except:
                            print(f'error in erc element:{pa}')
                else:
                    pr = pr if av == 'yes' else 0
                    name_parts_main = 'erc' if av == 'yes' else None
                    p_main = Parts_full.objects.create(name_parts=n,
                    partnumber_parts=pa,providers=prov1,
                    providerprice_parts=pr,date_chg=timezone.now(),
                    availability_parts=av,kind=kind,name_parts_main=name_parts_main)
                    a1.parts_full.add(p_main)
            else:
                continue
    pp = Parts_full.objects.exclude(partnumber_parts__in=set_erc).filter(providers__name_provider='erc')
    pp.update(availability_parts='no',providerprice_parts='0',date_chg = timezone.now())
    if not Results.objects.filter(who='erc').exists():
        r = Results(who='erc',
        who_desc=f'count_no: {count_no}, count_on: {count_on}')
        r.save()
    else:
        r = Results.objects.get(who='erc')
        r.who_desc = f'ERC add: {count_no} obj, update: {count_on} obj'
        r.save()

    return count_no, count_on, pp
