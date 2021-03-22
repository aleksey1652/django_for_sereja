from load_form_providers.dc import DC
from load_form_providers.asbis import ASBIS
from load_form_providers.elko import ELKO
from load_form_providers.mti import MTI
from load_form_providers.itlink import ITLINK
from load_form_providers.brain import BRAIN
from load_form_providers.edg import EDG
from load_form_providers.erc import  ERC
import time,schedule,datetime
from django.utils import timezone
import os,django,pickle, json
from load_form_providers.sheet_class import *
#os.environ.setdefault('DJANGO_SETTINGS_MODULE','sereja.settings')
#django.setup()
from cat.models import *
from django.contrib import messages
from django.db.models import Min
import pandas as pd

def get_xls():
    count = 0
    cols = [1, 2, 3,4]
    try:
        p1 = pd.read_excel('media/1c.xlsx', usecols=cols,header=None)
    except:
        print('not xls file ("media/1c.xlsx")')
        return f'1c obj add: {count}'
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
    pfnon=Parts_full.objects.exclude(partnumber_parts__in=list_article,providers__name_provider__in=('dc','itlink','asbis','elko','mti','brain','erc','edg')).exclude(remainder=None)
    for x in pfnon:
        x.remainder=None
        x.date_chg = timezone.now()
        x.save()
    print(f'1c obj add: {count}')
    return f'1c obj add: {count}'

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

    Str_ = ['dc', 'asbis', 'elko', 'mti', 'itlink', 'brain', 'edg', 'erc']
    error_list=[]
    l = [DC(), ASBIS(), ELKO(usd_ua), MTI(usd_ua), ITLINK(), BRAIN(), EDG(), ERC(usd_ua)]

    for y,x in enumerate(l):
        try:
            dict_set[Str_[y]] = x.get_sort_basa()
            count+=1
            print(f'{Str_[y]} is complite')
        except:
            print(f"Somthing wrong in {Str_[y]}")
            error_list.append(y)
            continue
    if error_list:
        time.sleep(60)
        for a,b in enumerate(l):
            if a in error_list:
                try:
                    l[a].get_sort_basa()
                    print(f'{Str_[a]} is complite')
                    time.sleep(20)
                except:
                    try:
                        l[a].get_sort_basa()
                    except:
                        print(f"Somthing wrong in {Str_[a]}")
                        count-=1
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
    p=Panda()
    p.set_panda_set(dict_set)
    #basa = p.full_panda_set()

    return (p,count)

def Parsing_from_providers():
    count_on,count_no = 0,0
    t2=timezone.now()
    r,count_provider = RUN()
    #os.environ.setdefault('DJANGO_SETTINGS_MODULE','sereja.settings')
    #django.setup()
    #from cat.models import *
    aall=Articles.objects.all()
    if not aall.exists():
        from load_form_providers.load_element_to_zero_db import main
        main()
    list_providers = ['dc','itlink','asbis','elko','mti','brain','edg','erc']
    if not Providers.objects.all().exists():
        for l in list_providers + ['-']:
            Providers.objects.create(name_provider=l)
    for a in aall:
        list_get_providers = []
        #partf = Parts_full.objects.filter(partnumber_parts=a.article)
        try:
            res = r.get_element_panda_partnum(a.article)
        except:
            print(f'false article  {a.article}')
            res={}
        if res:
            for x in list_providers:
                if  x in res.__dict__ and not res[x].empty:
                    list_get_providers.append(x)
        for partf in Parts_full.objects.filter(partnumber_parts=a.article).distinct().select_related('providers'):
            if partf:
                if partf.providers.name_provider in list_get_providers + ['-']:
                    continue
                else:
                    partf.availability_parts = 0
                    partf.providerprice_parts = None
                    partf.save()
        for p in list_get_providers:
            temp = Parts_full.objects.filter(partnumber_parts=a.article,providers__name_provider=p).distinct()
            if temp:
                temp[0].availability_parts = res[p].Availability
                temp[0].providerprice_parts = res[p].Price
                temp[0].date_chg = timezone.now()
                temp[0].save()
                count_on += 1
                #print('update: ',res[p].Name,p,res[p].Price)
            else:
                prov = Providers.objects.get(name_provider=p)
                Parts_full.objects.create(availability_parts = res[p].Availability,
                providerprice_parts = res[p].Price,name_parts = res[p].Name,
                partnumber_parts = res[p].Partnumber,url_parts = res[p].Url,providers=prov,
                date_chg=timezone.now())
                #print(res[p].Name,p,res[p].Price)
                count_no += 1
    get_xls()
    """for x in Parts_short.objects.all():
        temp_list = Parts_full.objects.filter(
            partnumber_parts__in=eval(x.partnumber_list))
        #temp_list_x = temp_list.filter(providers__name_provider='-')
        temp = temp_list.aggregate(a=Min('providerprice_parts'))['a'] if temp_list else '0'
        if temp:
            x.min_price = temp
            #if temp_list_x:
                #x.x_code = temp_list_x.aggregate(a=Min('providerprice_parts'))['a']
            count_ += 1
            a = x.save()"""
    print( f'From {count_provider} providers price update {count_on} and in {count_no} Parts_short add new min_price')
    with open("load_form_providers/loads/log.json", "r") as write_file:
        dict_log=json.load(write_file)
    print(f'log keys: {dict_log.keys()}')
    dict_load_element = {'time': timezone.now().strftime("%d-%m-%y,%H:%M"),
    'mes': f'From {count_provider} providers price update {count_on} and in {count_no} Parts_short add new min_price'}
    dict_log['dict_load_element'] = dict_load_element
    with open("load_form_providers/loads/log.json", "w") as write_file:
        json.dump(dict_log,write_file)
    #my_time = datetime.datetime.today()
    t1=timezone.now()
    #t2=time.strptime(my_time, "%H:%M")

    print(f"Work time {str(t1-t2)[2:4]}  minuts")
    #print(f"Program will start at {my_time}")
    #return f"Work time {(t1.tm_hour)*60+t1.tm_min-(t2.tm_hour)*60-t2.tm_min}  minuts"

"""if __name__ == '__main__':
    my_time = "09:20"
    schedule.clear('d')
    schedule.every().day.at(my_time).do(lambda: Parsing_from_providers(my_time)).tag('d')
    print(f"Program will start at {my_time}")

    while True:
        schedule.run_pending()
        time.sleep(1)"""
"""my_time = "11:25"
schedule.clear('d')
schedule.every().day.at(my_time).do(lambda: Parsing_from_providers(my_time)).tag('d')
print(f"Program will start at {my_time}")

while True:
    schedule.run_pending()
    time.sleep(1)"""
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
"""def fun2():
    cver = Computers.objects.filter(pc_assembly__sites__name_sites='versum')
    for c in cver:
        try:
            cc=CompPrice.objects.get(name_computers=c.name_computers)
        except:
            print(c.name_computers)
            continue
        for x,y in c.__dict__.items():
            if x in ('proc_computers', 'mb_computers', 'mem_computers',
                     'video_computers', 'ps_computers',
                     'case_computers', 'cool_computers','vent_computers'):
                try:
                    short1=Parts_short.objects.get(name_parts=y)
                except:
                    print(c.name_computers,y)
                    continue
                #pp=Parts_full.objects.filter(name_parts=x,providers__name_provider='-')
                pp=Parts_full.objects.filter(
                    partnumber_parts__in=eval(short1.partnumber_list),providers__name_provider='-')
                if pp:
                    pr=pp.first().providerprice_parts
                    if pr:
                        cc.__dict__[x]=pr
                        print(cc.__dict__[x])
            elif x == 'hdd_computers':
                h = y.split(';')
                if len(h)>1:
                    try:
                        short1=Parts_short.objects.get(name_parts=h[0])
                    except:
                        print(c.name_computers,y)
                        continue
                    pp=Parts_full.objects.filter(
                        partnumber_parts__in=eval(short1.partnumber_list),providers__name_provider='-')
                    if pp:
                        pr=pp.first().providerprice_parts
                        if pr:
                            cc.__dict__['hdd_computers']=pr
                            print(cc.__dict__[x])
                    try:
                        short1=Parts_short.objects.get(name_parts=h[1])
                    except:
                        print(c.name_computers,y)
                        continue
                    pp=Parts_full.objects.filter(
                        partnumber_parts__in=eval(short1.partnumber_list),providers__name_provider='-')
                    if pp:
                        pr=pp.first().providerprice_parts
                        if pr:
                            cc.__dict__['hdd2_computers']=pr
                            print(cc.__dict__[x])
                else:
                    try:
                        short1=Parts_short.objects.get(name_parts=h[0])
                    except:
                        print(c.name_computers,y)
                        continue
                    pp=Parts_full.objects.filter(
                        partnumber_parts__in=eval(short1.partnumber_list),providers__name_provider='-')
                    if pp:
                        pr=pp.first().providerprice_parts
                        if pr:
                            cc.__dict__['hdd_computers']=pr
                            print(cc.__dict__[x])
        cc.save()

for x in Parts_full.objects.all():
	p2 = Parts_full.objects.filter(partnumber_parts=x.partnumber_parts,providers__name_provider='-')
	if not p2:
		price=Parts_full.objects.filter(
                partnumber_parts=x.partnumber_parts).aggregate(a=Min('providerprice_parts'))['a']
		if price:
			z=Parts_full.objects.create(providerprice_parts = price,name_parts = x.name_parts,
                partnumber_parts = x.partnumber_parts,providers=Providers.objects.get(name_provider='-'))

for x in Parts_full.objects.all():
    p2 = Parts_full.objects.filter(partnumber_parts=x.partnumber_parts,providers__name_provider='-')
    if p2:
        p2=p2.first()
        p2.providerprice_parts=Parts_full.objects.filter(
                partnumber_parts=x.partnumber_parts).aggregate(a=Min('providerprice_parts'))['a']
        p2.save()
    else:
        price=Parts_full.objects.filter(
        partnumber_parts=x.partnumber_parts).aggregate(a=Min('providerprice_parts'))['a']
        if price:
            z=Parts_full.objects.create(providerprice_parts = price,name_parts = x.name_parts,
            partnumber_parts = x.partnumber_parts,providers=Providers.objects.get(name_provider='-'))
        else:
            z=Parts_full.objects.create(providerprice_parts = 0,name_parts = x.name_parts,
            partnumber_parts = x.partnumber_parts,providers=Providers.objects.get(name_provider='-'))
for x in Computers.objects.all():
	if
	CompPrice.objects.create(name_computers=x.name_computers,price_computers=x.price_computers,computers=x)

    Parts_full.objects.create(name_parts='Core i5 9600KF BOX',partnumber_parts='BX80684I59600KF')

    for x in res[234:263]:
	if len(x)>1 and x[0] and x[1] and not Articles.objects.filter(article=x[1]) and (x[1] in list_cool):
		Articles.objects.create(article=x[1],item_name=x[0],item_price='cool')

    for x in res[234:263]:
	if len(x)>1 and x[0] and x[1] and not Articles.objects.filter(article=x[1]):
		list_cool2.append(x[1])

for x in Articles.objects.filter(item_price='cool'):
	if not Parts_full.objects.filter(partnumber_parts=x.article):
		Parts_full.objects.create(name_parts = x.item_name,partnumber_parts = x.article,providers=prov)

for x in Articles.objects.filter(item_price='video'):
    try:
        p=Parts_full.objects.get(partnumber_parts=x.article,providers=prov)
    except:
        print(x.article)
    p.providerprice_parts=Parts_full.objects.filter(partnumber_parts=x.article).aggregate(a=Min('providerprice_parts'))['a']
   p.save()

for x in call:
    try:
        if get_cpu(x.__dict__['proc_computers'])==[3, 2200, 'g']:
            c_set.add(x.pk)
    except:
        print(x.pk)
        continue
for x in cpuv:
    try:
        p=Parts_short.objects.get(name_parts=x)
        pp=Parts_full.objects.filter(
            partnumber_parts__in=eval(p.partnumber_list),providers__name_provider='-')
        dict_cpuv[x]=pp
    except:
        print(x,end ' ')

for k,v in dict_cpuv.items():
    if not v:
        try:
            p=Parts_full.objects.get(name_parts=v)
            dict_cpuv2[k]=p
        except:
            print(k,end=' ')

procent = c.class_computers if c.class_computers else 1.19
try:
    procent = float(procent)
except:
    procent = 1.19
cpr = c.compprice
cpr.__dict__[f"{short_kind2}_computers"] = price
cpr.save()
summa = 0
for x,y in cpr.__dict__.items():
    if x in ('vent_computers', 'proc_computers', 'mb_computers', 'mem_computers', 'video_computers', 'hdd_computers', 'hdd2_computers', 'ps_computers', 'case_computers', 'cool_computers'):
        try:
            summa+=float(y)
        except:
            summa+=0
summa = round(procent*summa)
cpr.price_computers = summa
cpr.save()
short.x_code=price
short.date_chg = timezone.now()
short.save()
100009

for x,y in dict_our.items():
    try:
        p=Parts_full.objects.get(partnumber_parts=x,providers__name_provider='-')
    except:
        print(x)
    try:
        p.providerprice_parts=float(f(y))
        p.save()
        comps = need_comps(s.name_parts)
        for c in comps:
            procent = c.class_computers if c.class_computers.exists() else 1.19
            cpr = c.compprice
            cpr.__dict__[f"{short_kind2}_computers"] = price
            cpr.save()
            summa = 0
            for x,y in cpr.__dict__.items():
                if x in ('vent_computers', 'proc_computers', 'mb_computers', 'mem_computers', 'video_computers', 'hdd_computers', 'hdd2_computers', 'ps_computers', 'case_computers', 'cool_computers', 'mon_computers', 'wifi_computers', 'km_computers'):
                    try:
                        y = re.sub(',' ,'.', y)
                        summa+=float(y)
                    except:
                        summa+=0
            try:
                procent = float(procent)
            except:
                procent = 1.19
            summa = round(procent*summa)
            cpr.price_computers = summa
            cpr.save()
    except:
        print((x,y))

for x in cver:
	for k,v in x.__dict__.items():
		if k in ('proc_computers', 'mb_computers', 'mem_computers',
                         'video_computers', 'ps_computers',
                         'case_computers', 'cool_computers','vent_computers',
                         'mon_computers', 'wifi_computers', 'km_computers'
                         ):
			if not ver(k,v):
				temp=[]
				temp.append(v)
			dict_ver[x.name_computers]=temp

def content_for_google_sheet(obj,p):
    dict_ver={}
    list_atr = ['mb_computers', 'proc_computers', 'mem_computers', 'video_computers',
    'hdd_computers', 'case_computers', 'ps_computers', 'cool_computers','vent_computers']
    if p == 'versum':
        for x in list_atr:
            temp=[]
            if x != 'hdd_computers':
                if obj.__dict__[x]:
                    if not content_versum(obj,x):
                        temp.append(obj.__dict__[x])
            else:
                for y in obj.hdd_computers.split(';'):
                    if not content_versum(obj,y):
                        temp.append(obj.__dict__[x])
        if temp:
            dict_ver[obj.name_computers]=temp
        return dict_ver
for x in cff:
    try:
        print(x.compprice)
    except:
        print(x.pk,end=' ')

with open("load_form_providers/list_articles.json", "r") as write_file:
                    list_get_list2=json.load(write_file)
for k,v in list_get_list2:
    if not Articles.objects.filter(article=k).exists():
        try:
            Articles.objects.create(article=k,item_name=v[1],item_price=v[0])
        except:
            print(f'error in {k}')
for x in g:
    if x and len(x)==4 and x[1] and x[0]:
        try:
            prov=Providers.objects.get(name_provider='-')
        except:
            prov=Providers.objects.create(name_provider='-')
        if not Parts_full.objects.filter(partnumber_parts=x[1],providers=prov):
            if Parts_full.objects.filter(name_parts=x[0],providers=prov).exists():
                Parts_full.objects.filter(name_parts=x[0],providers=prov).delete()
                messages.success(request, f'Parts_full old was deleted: {x[0]}')
            if x[3]:
                try:
                    price = round(float(x[3]),1)
                except:
                    temp = re.sub(r',','.',x[3])
                    price = re.sub(r'\xa0','',temp)
                    try:
                        price = round(float(price),1)
                    except:
                        price = 0
            Parts_full.objects.create(name_parts=x[0],partnumber_parts=x[1],providers=prov,providerprice_parts=price)



  """
