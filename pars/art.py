from cat.models import *
from eldorado_get_json import get_art
from comp_class import IT_LOTS,ART
import json,pickle,re
import pandas as pd
import time,datetime
from django.utils import timezone
from scrapy import get_video,get_cpu,get_mb,get_case,get_ps,get_cool,get_hdd_ssd,get_mem

#with open("dict_code.json", "r") as write_file:
#        dict_code=json.load(write_file)
#with open("load_form_providers/loads/art_price.json", "r") as write_file:
#        art=json.load(write_file)
try:
    usd = USD.objects.first().usd
except:
    with open('load_form_providers/usd_ua.pickle', 'rb') as f:
        usd = pickle.load(f)

def get_cpu_art(c):
    c = re.sub(r'amd \d+-core','',c.strip().lower())
    c = re.sub(r'intel \d+-core','',c.strip().lower())
    c = re.sub(r'\d\.\d+','',c.strip().lower())
    return get_cpu(c)

def get_xxx(k,itm):
    dict_parts = {'proc':'get_cpu_art(itm)','mb':'get_mb(itm)[:1]','video':'get_video(itm)[:1]','mem':'get_mem(itm)[:1]',
    'ps':'get_ps(itm)','case':'get_case(itm)','cool':'get_cool(itm)','hdd':'get_hdd_ssd(itm)[:2]'}
    try:
        if k == 'video' and get_video(itm) == 'hd graphics':
            return 'hd graphics'
        e = eval(dict_parts[k])
    except:
        e=[]
    return e

def to_article2(d,pr=1):
    if pr==1:
        if d['proc'].lower().find('core') !=-1:
            return 'iproc'
        elif d['proc'].lower().find('pentium') !=-1:
            return 'iproc'
        elif d['proc'].lower().find('celeron') !=-1:
            return 'iproc'
        else:
            return 'aproc'
    else:
        if d['proc'].lower().find('core') !=-1:
            return 'imb'
        elif d['proc'].lower().find('pentium') !=-1:
            return 'imb'
        elif d['proc'].lower().find('celeron') !=-1:
            return 'imb'
        else:
            return 'amb'

"""def to_comp(obj):
    dict_comp={}
    dict_comp['name_computers']=obj['name']
    dict_comp['url_computers']=obj.comp_url
    dict_comp['price_computers']=obj.price
    if  not isinstance(obj.proc, str):
        dict_comp['proc_computers']=obj.proc['Name']
    else:
        dict_comp['proc_computers']=obj.proc
    if  not isinstance(obj.mb, str):
        dict_comp['mb_computers']=obj.mb['Name']
    else:
        dict_comp['mb_computers']=obj.mb
    if  not isinstance(obj.mem, str):
        dict_comp['mem_computers']=obj.mem['Name']
    else:
        dict_comp['mem_computers']=obj.mem
    if  not isinstance(obj.video, str):
        dict_comp['video_computers']=obj.video['Name']
    else:
        dict_comp['video_computers']=obj.video
    if  not isinstance(obj.ps, str):
        dict_comp['ps_computers']=obj.ps['Name']
    else:
        dict_comp['ps_computers']=obj.ps
    if  not isinstance(obj.case, str):
        dict_comp['case_computers']=obj.case['Name']
    else:
        dict_comp['case_computers']=obj.case
    if  not isinstance(obj.cool, str):
        dict_comp['cool_computers']=obj.cool['Name']
    else:
        dict_comp['cool_computers']=obj.cool
    dict_comp['class_computers']=obj['class']
    dict_comp['warranty_computers']=obj.warranty
    temp=''
    for x in obj.hdd:
        if  not isinstance(x, str):
            temp+=x['Name']+';'
            dict_comp['hdd_computers']=temp[:-1]
    if 'hdd_computers' not in dict_comp:
        dict_comp['hdd_computers']=''
    return dict_comp"""

def load_art():
    try:
        """with open("load_form_providers/loads/art_price.json", "r") as write_file:
            art=json.load(write_file)"""
        art=get_art()
        """a=ART(dict_code)
        a._IT_LOTS__sheet=pd.DataFrame()
        a._IT_LOTS__basa=pd.DataFrame(columns=a._IT_LOTS__cil)
        a.set_panda_set(art)
        abasa=a.it_basa()
        abasa.to_json('load_form_providers/loads/art_basa.json')"""
    except:
        print('loaded art error but will be try load old assemly')
        #abasa = pd.read_json('load_form_providers/loads/art_basa.json')
        with open("load_form_providers/loads/art_price.json", "r") as write_file:
            art=json.load(write_file)

    #pcassembly_art=Pc_assembly.objects.get(name_assembly='art_all')
    comp_it=Computers.objects.filter(pc_assembly__sites__name_sites='art')
    if not comp_it.exists():
        site,p_ = Sites.objects.get_or_create(name_sites='art',more='https://artline.ua/')
        pcassembly_it,p_ = Pc_assembly.objects.get_or_create(name_assembly='art_all',sites=site)
        comp_it=Computers.objects.filter(pc_assembly__sites__name_sites='art')
    count_on = 0
    count_no = 0
    temp_comp_on=[]
    temp_comp_no=[]
    for x in art:
        if comp_it.filter(name_computers=x).exists():
            temp_comp_on.append(art[x]['name'])
        else:
            temp_comp_no.append(art[x]['name'])
    for x in temp_comp_on:
        try:
            temp = Computers.objects.filter(name_computers=x,pc_assembly__sites__name_sites='art')
            if temp.exists():
                te = temp.first()
                try:
                    hdd = re.sub(r';','',art[x]['Объем накопителя'])+';'+re.sub(r';','',art[x]['Объем второго накопителя'])
                except:
                    if 'Объем накопителя' in art[x]:
                        hdd = re.sub(r';','',art[x]['Объем накопителя'])
                    elif 'Объем второго накопителя' in art[x]:
                        hdd = re.sub(r';','',art[x]['Объем второго накопителя'])
                    else:
                        hdd = ''
                te.name_computers=art[x]["name"]
                te.url_computers=art[x]["comp_url"]
                te.price_computers=art[x]["price"]
                te.proc_computers=art[x]["Модель процессора"]
                te.mb_computers=art[x]["Модель материнской платы"]
                te.mem_computers=art[x]["Оперативная память"]
                te.video_computers=art[x]["Видеокарта"]
                te.hdd_computers=hdd
                te.ps_computers=art[x]["Блок питания"]
                te.case_computers=art[x]["Корпус"]
                te.cool_computers=art[x]["Охлаждение процессора"]
                te.wifi_computers=''
                te.vent_computers=''
                te.class_computers=''
                te.warranty_computers=''
                te.save()
                temp = temp[1:]
                for q in temp:
                    q.delete()
                count_on += 1
                try:
                    temp_=round(float(re.sub(r'\D','',te.price_computers))/usd)
                except:
                    temp_=te.price_computers
                cp=CompPrice.objects.filter(name_computers=te.name_computers)
                if not cp:
                    cf=CompPrice.objects.create(name_computers=te.name_computers,price_computers=temp_,computers=te)
                    cf.price_computers=temp_
                    cf.save()
                else:
                    cf=cp.first()
                    cf.price_computers=temp_
                    cf.save()
                    cp=cp[1:]
                    for q in cp:
                        q.delete()
        except:
            print(f'error in  on {x}')
    for x in temp_comp_on:
        try:
            comp = Computers.objects.get(name_computers=x,pc_assembly__sites__name_sites='art')
            cp=comp.compprice
        except:
            print(f'error in  on compprice or comp {x}')
        for k,v in comp.__dict__.items():
            if  k in ('proc_computers', 'mb_computers', 'mem_computers',
                     'video_computers', 'ps_computers',
                     'case_computers'
                    ):
                temp_a = re.sub('_computers','',k)
                partnumber_list = get_xxx(temp_a,v)
                cp.__dict__[k] = partnumber_list
                cp.save()
                #print(partnumber_list)
            if k == 'hdd_computers':
                hdd = v.split(';')
                cp.hdd_computers = get_xxx('hdd',hdd[0]) if hdd else ''
                cp.hdd2_computers = get_xxx('hdd',hdd[1]) if len(hdd) == 2 else ''
                cp.save()
    for y in temp_comp_no:
        pcassembly_art,p_=Pc_assembly.objects.get_or_create(name_assembly='art_all')
        try:
            if not Computers.objects.filter(name_computers=y,pc_assembly__sites__name_sites='art'):
                try:
                    hdd = re.sub(r';','',art[y]['Объем накопителя'])+';'+re.sub(r';','',art[y]['Объем второго накопителя'])
                except:
                    if 'Объем накопителя' in art[y]:
                        hdd = re.sub(r';','',art[y]['Объем накопителя'])
                    elif 'Объем второго накопителя' in art[y]:
                        hdd = re.sub(r';','',art[y]['Объем второго накопителя'])
                    else:
                        hdd = ''
                c=Computers(name_computers=y,url_computers=art[y]['comp_url'],
                price_computers=art[y]['price'],proc_computers=art[y]["Модель процессора"],
                mb_computers=art[y]["Модель материнской платы"],mem_computers=art[y]["Оперативная память"],
                video_computers=art[y]["Видеокарта"],hdd_computers=hdd,
                ps_computers=art[y]["Блок питания"],case_computers=art[y]["Корпус"],
                cool_computers=art[y]["Охлаждение процессора"],class_computers='',
                warranty_computers='',vent_computers='',wifi_computers='',
                vent_num_computers=1,mem_num_computers=1,
                video_num_computers=1,pc_assembly=pcassembly_art)
                c.save()
                try:
                    temp=round(float(re.sub(r'\D','',c.price_computers))/usd)
                except:
                    temp=c.price_computers
                cp=CompPrice.objects.filter(name_computers=c.name_computers)
                if not cp:
                    cf=CompPrice.objects.create(name_computers=c.name_computers,price_computers=temp,computers=c)
                    cf.price_computers=temp
                    cf.save()
                else:
                    cp=cp.first()
                    cp.price_computers=temp
                    cp.save()
                    cp=cp[1:]
                    for q in cp:
                        q.delete()
                count_no += 1
        except:
            print(f'error in  no {y}')
    """for x in abasa.iloc:
        try:
            t=to_comp(x)
            temp=Computers.objects.filter(name_computers=x.name)
        except:
            temp = []
            t = {}
            if not x.empty:
                try:
                    print(f'{x.name} error (wrong components)')
                except:
                    print(f'{x} error (no name)')
            else:
                print(f'{x} error (empty)')
        if temp:
            if t['name_computers'] and t['mem_computers'] and t['proc_computers'] and t['video_computers']:
                temp[0].name_computers=t['name_computers']
                temp[0].url_computers=t['url_computers']
                temp[0].price_computers=t['price_computers']
                temp[0].proc_computers=t['proc_computers']
                temp[0].mb_computers=t['mb_computers']
                temp[0].mem_computers=t['mem_computers']
                temp[0].video_computers=t['video_computers']
                temp[0].hdd_computers=t['hdd_computers']
                temp[0].ps_computers=t['ps_computers']
                temp[0].case_computers=t['case_computers']
                temp[0].cool_computers=t['cool_computers']
                temp[0].class_computers=t['class_computers']
                temp[0].warranty_computers=t['warranty_computers']
                temp[0].save()
                count_on+=1
            else:
                print('new errror in' + t['name_computers'])
                continue
        else:
            if t and not Computers.objects.filter(name_computers=t['name_computers']):
                c=Computers(name_computers=t['name_computers'],url_computers=t['url_computers'],
                price_computers=t['price_computers'],proc_computers=t['proc_computers'],
                mb_computers=t['mb_computers'],mem_computers=t['mem_computers'],
                video_computers=t['video_computers'],hdd_computers=t['hdd_computers'],
                ps_computers=t['ps_computers'],case_computers=t['case_computers'],
                cool_computers=t['cool_computers'],class_computers=t['class_computers'],
                warranty_computers=t['warranty_computers'],vent_computers='empty',
                vent_num_computers=1,mem_num_computers=1,
                video_num_computers=1,pc_assembly=pcassembly_art)
                c.save()
                count_no+=1"""
    print(f'art loaded with {count_on} changed in computers and add {count_no} computers')
    with open("load_form_providers/loads/log.json", "r") as write_file:
        dict_log=json.load(write_file)
    dict_art_log = {'time': timezone.now().strftime("%d-%m-%y,%H:%M"),
    'mes': f'Art loaded with {count_on} changed in computers and add {count_no} computers'}
    dict_log['dict_art_log'] = dict_art_log
    with open("load_form_providers/loads/log.json", "w") as write_file:
        json.dump(dict_log,write_file)
