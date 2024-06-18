from cat.models import *
from eldorado_get_json import get_fury
from comp_class import IT_LOTS,Fury
import json,pickle,re
import pandas as pd
import time,datetime
from django.utils import timezone
from scrapy import get_video,get_cpu,get_mb,get_case,get_ps,get_cool,get_hdd_ssd,get_mem
#from sereja.tasks import send_mail_task

#with open("dict_code.json", "r") as write_file:
#        dict_code=json.load(write_file)

try:
    usd = USD.objects.first().usd
except:
    with open('load_form_providers/usd_ua.pickle', 'rb') as f:
        usd = pickle.load(f)

def get_xxx(k,itm):
    dict_parts = {'proc':'get_cpu(itm)','mb':'get_mb(itm)[:1]','video':'get_video(itm)[:1]','mem':'get_mem(itm)[:1]',
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

def get_partnumber_list(k,p):
    list_ = []
    #dict_ = {'proc':('aproc','iproc'),'mb':('imb','amb'),'video':('video',),'mem':('mem',),
    #'ps':('ps',),'case':('case',),'cool':('cool',),'hdd':('hdd','ssd')}
    a = Articles.objects.filter(item_price=k)
    if k not in ('case','cool'):
        for x in a:
            if get_xxx(k,p) == get_xxx(k,x.item_name):
                list_.append(x.article)
    else:
        for x in a:
            list_.append(x.article)
    return f"{list_[:10]}"

def to_comp_fury(obj):
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
    return dict_comp

def load_fury():
    try:
        fury=get_fury()
        """f=Fury(dict_code)
        f._IT_LOTS__sheet=pd.DataFrame()
        f._IT_LOTS__basa=pd.DataFrame(columns=f._IT_LOTS__cil)
        f.set_panda_set(fury)
        fbasa=f.it_basa()
        fbasa.to_json('load_form_providers/loads/fury_basa.json')"""
    except:
        print('Bad panda data but try with old price')
        #fbasa = pd.read_json('load_form_providers/loads/fury_basa.json')
        with open("load_form_providers/loads/fury_price.json", "r") as write_file:
            fury = json.load(write_file)
    site,p_ = Sites.objects.get_or_create(name_sites='fury')
    pcassembly_fury,p_=Pc_assembly.objects.get_or_create(name_assembly='fury_all',sites=site)
    comp_it=Computers.objects.filter(pc_assembly__sites__name_sites='fury')
    if not comp_it.exists():
        site,p_ = Sites.objects.get_or_create(name_sites='fury')
        pcassembly_it,p_ = Pc_assembly.objects.get_or_create(name_assembly='art_all',sites=site)
        comp_it=Computers.objects.filter(pc_assembly__sites__name_sites='fury')
    temp_comp_on,temp_comp_no=[],[]

    for x in fury:
        if comp_it.filter(name_computers=x.strip()).exists():
            temp_comp_on.append(fury[x]['name'])
        else:
            temp_comp_no.append(fury[x]['name'])
    count_on = 0
    for x in temp_comp_on:
        x = x.strip()
        try:
            temp = Computers.objects.filter(name_computers=x,pc_assembly__sites__name_sites='fury')
            if temp.count() >= 1:
                te = temp.first()
                try:
                    hdd = fury[x]['hdd'][0] + ';' + fury[x]['hdd'][1] if len(fury[x]['hdd']) == 2 else fury[x]['hdd'][0]
                except:
                    hdd = ''
                te.name_computers=fury[x]["name"]
                te.url_computers=fury[x]["comp_url"]
                te.price_computers=fury[x]["price"]
                te.proc_computers=fury[x]["proc"]
                te.mb_computers=fury[x]["mb"]
                te.mem_computers=fury[x]["mem"]
                te.video_computers=fury[x]["video"]
                te.hdd_computers=hdd
                te.ps_computers=fury[x]["ps"]
                te.case_computers=fury[x]["case"]
                te.cool_computers=''
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
        x = x.strip()
        try:
            comp = Computers.objects.get(name_computers=x.strip(),pc_assembly__sites__name_sites='fury')
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
            if k == 'hdd_computers':
                hdd = v.split(';')
                cp.hdd_computers = get_xxx('hdd',hdd[0]) if hdd else ''
                cp.hdd2_computers = get_xxx('hdd',hdd[1]) if len(hdd) == 2 else ''
                cp.save()
    for y in temp_comp_no:
        site,p_ = Sites.objects.get_or_create(name_sites='fury')
        pcassembly_art,p_=Pc_assembly.objects.get_or_create(name_assembly='fury_all',sites=site)
        try:
            if not Computers.objects.filter(name_computers=y,pc_assembly__sites__name_sites='fury'):
                try:
                    hdd = fury[x]['hdd'][0] + ';' + fury[x]['hdd'][1] if len(fury[x]['hdd']) == 2 else fury[x]['hdd'][0]
                except:
                    hdd = ''
                c=Computers(name_computers=y,url_computers=fury[y]['comp_url'],
                price_computers=fury[y]['price'],proc_computers=fury[y]["proc"],
                mb_computers=fury[y]["mb"],mem_computers=fury[y]["mem"],
                video_computers=fury[y]["video"],hdd_computers=hdd,
                ps_computers=fury[y]["ps"],case_computers=fury[y]["case"],
                cool_computers=fury[y]["cool"],class_computers='',
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
    print(f'fury loaded with {count_on} computers')
    if not Results.objects.filter(who='fury').exists():
        r = Results(who='fury',
        who_desc=f'DigitalFury update: {count_on} comps')
        r.save()
    else:
        r = Results.objects.get(who='fury')
        r.who_desc = f'DigitalFury update: {count_on} comps'
        r.save()
    """send_mail_task.delay(subject='Versum_results', message='Test from Alex',
    from_email='aleksey1652@ukr.net', recipients='peregonnata@gmail.com')"""
    with open("load_form_providers/loads/log.json", "r") as write_file:
        dict_log=json.load(write_file)
    dict_fury_log = {'time': timezone.now().strftime("%d-%m-%y,%H:%M"),
    'mes': f'Fury loaded with {count_on} computers'}
    dict_log['dict_fury_log'] = dict_fury_log
    with open("load_form_providers/loads/log.json", "w") as write_file:
        json.dump(dict_log,write_file)
