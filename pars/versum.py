from cat.models import *
from eldorado_get_json import get_versum
from comp_class import VERSUM_LOTS, IT_LOTS
import json,pickle,re
import pandas as pd
import time,datetime
from django.utils import timezone
from scrapy import get_video,get_cpu,get_mb,get_case,get_ps,get_cool,get_hdd_ssd,get_mem

""""with open("dict_code.json", "r") as write_file:
        dict_code=json.load(write_file)"""
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
        if d.lower().find('core') !=-1:
            return 'iproc'
        elif d.lower().find('pentium') !=-1:
            return 'iproc'
        elif d.lower().find('celeron') !=-1:
            return 'iproc'
        else:
            return 'aproc'
    else:
        if d.lower().find('core') !=-1:
            return 'imb'
        elif d.lower().find('pentium') !=-1:
            return 'imb'
        elif d.lower().find('celeron') !=-1:
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

def to_article(d,pr=1):
    if pr==1:
        if d['Name'].lower().find('core') !=-1:
            return 'iproc'
        elif d['Name'].lower().find('pentium') !=-1:
            return 'iproc'
        elif d['Name'].lower().find('celeron') !=-1:
            return 'iproc'
        else:
            return 'aproc'
    else:
        if d['Name'].lower().find('core') !=-1:
            return 'imb'
        elif d['Name'].lower().find('pentium') !=-1:
            return 'imb'
        elif d['Name'].lower().find('celeron') !=-1:
            return 'imb'
        else:
            return 'amb'

def to_comp(obj):
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

def load_versum():
    def get_asml(comp,templ):
        comp,templ = comp.lower(),templ.lower()
        if comp.find(f'{templ}-iii')!=-1:
            return f'{templ}-iii'
        if comp.find(f'{templ}-ii')!=-1:
            return f'{templ}-ii'
        if comp.find(f'{templ}-i')!=-1:
            return f'{templ}-i'

    list_ver_templ=['speedster','silver','platinum','panzer','paladin','omega','msi',
    'mini','level','legendary-nuker','king-lich','great-crusader','gold','gigabyte',
    'galaxy','epic-nuker','crusader','archlich','rainbow','ratchet','ultra-magnus',
    'metroplex','february']
    list_ver_templ2=['nuker','lich']

    try:
        versum=get_versum()
        """ver=VERSUM_LOTS(dict_code)
        ver._IT_LOTS__sheet=pd.DataFrame()
        ver._IT_LOTS__basa=pd.DataFrame(columns=ver._IT_LOTS__cil)
        ver.set_panda_set(versum)
        verbasa=ver.it_basa()
        verbasa.to_json('load_form_providers/loads/versum_basa.json')"""
    except:
        print('loaded fury error but will be try load old assemly')
        #verbasa = pd.read_json('load_form_providers/loads/versum_basa.json')
        with open("load_form_providers/loads/versum_price.json", "r") as write_file:
            versum = json.load(write_file)
    #verbasa = pd.read_json('load_form_providers/loads/versum_basa.json')
    temp_comp_on=[]
    temp_comp_no=[]
    comp_ver=Computers.objects.filter(pc_assembly__sites__name_sites='versum')
    set_load = set(versum.keys())
    #versum_reserve = comp_ver.exclude(name_computers__in=set_load).filter(pc_assembly__sites__name_sites='versum')
    #versum_reserve.update(is_active=False)
    if not comp_ver.exists():
        site,p_ = Sites.objects.get_or_create(name_sites='versum',more='https://versum.ua')
        pcassembly_it,p_ = Pc_assembly.objects.get_or_create(name_assembly='Other',kind_assembly='msi',sites=site)
        comp_ver=Computers.objects.filter(pc_assembly__sites__name_sites='versum')
    dict_v = {"Оперативна пам’ять:":'mem',"Відеокарта:":'video',"Кулер:":'cool',
    "Накопичувач SSD:":'ssd',"Накопичувач HDD:":'hdd',"Wi-Fi адаптер:":'wifi',
    "Блок живлення:":'ps',"Вентилятори:":'vent',"Корпус:":'case'}

    for i in versum:
        for k,v in versum[i].items():
            if k in ("Процесор:","Материнська плата:","Оперативна пам’ять:","Відеокарта:","Кулер:","Накопичувач SSD:",
            "Накопичувач HDD:","Wi-Fi адаптер:","Блок живлення:","Вентилятори:","Корпус:"):
                if not Parts_short.objects.filter(name_parts=v):
                    if k == "Процесор:":
                        temp_a = to_article2(versum[i][k])
                    elif k == "Материнська плата:":
                        temp_a = to_article2(versum[i]["Процесор:"],pr=0)
                    else:
                        temp_a = dict_v[k]
                    partnumber_list = get_partnumber_list(temp_a,v)
                    p=Parts_short(name_parts=v,partnumber_list=partnumber_list,kind=temp_a,kind2=False)
                    p.save()

    for x in versum:
        if comp_ver.filter(name_computers=x.strip()).exists():
            temp_comp_on.append(versum[x]['name'])
        else:
            temp_comp_no.append(versum[x]['name'])
    count_no = 0
        #else:
    for y in temp_comp_no:
        site_versum,p_ = Sites.objects.get_or_create(name_sites='versum')
        pc_if_in,_ = Pc_assembly.objects.get_or_create(name_assembly='Other_group',kind_assembly='Other',sites=site_versum)
        try:
            pcassembly_ver = pc_if_in
            if not Computers.objects.filter(name_computers=y,pc_assembly__sites__name_sites='versum'):
                try:
                    hdd = versum[y]['Накопичувач SSD:']+';'+versum[y]['Накопичувач HDD:']
                except:
                    if 'Накопичувач SSD:' in versum[y]:
                        hdd = versum[y]['Накопичувач SSD:']
                    elif 'Накопичувач HDD:' in versum[x]:
                        hdd = versum[y]['Накопичувач HDD:']
                    else:
                        hdd = ''
                c=Computers(name_computers=y,url_computers=versum[y]['comp_url'],
                price_computers=versum[y]['price'],proc_computers=versum[y]["Процесор:"],
                mb_computers=versum[y]["Материнська плата:"],mem_computers=versum[y]["Оперативна пам’ять:"],
                video_computers=versum[y]["Відеокарта:"],hdd_computers=hdd,
                ps_computers=versum[y]["Блок живлення:"],case_computers=versum[y]["Корпус:"],
                cool_computers=versum[y]["Кулер:"],class_computers='',
                warranty_computers='',vent_computers=versum[y]["Вентилятори:"],wifi_computers=versum[y]["Wi-Fi адаптер:"],
                vent_num_computers=1,mem_num_computers=1,
                video_num_computers=1,pc_assembly=pcassembly_ver)
                c.save()
                try:
                    temp=round(float(re.sub(r'\D','',str(c.price_computers)))/usd)
                except:
                    temp=c.price_computers
                cp=CompPrice.objects.filter(name_computers=c.name_computers)
                if not cp:
                    CompPrice.objects.create(name_computers=c.name_computers,price_computers=temp,computers=c)
                else:
                    cpf=cp.first()
                    cpp.price_computers=temp
                    cpf.save()
                    cp=cp[1:]
                    for q in cp:
                        q.delete()
                count_no += 1
        except:
            print(f'error in  no {y}')

    count_on =0
    for x in temp_comp_on:
        try:
            temp = Computers.objects.filter(name_computers=x,pc_assembly__sites__name_sites='versum')
            if temp.count() >= 1:
                te = temp.first()
                try:
                    hdd = versum[x]['Накопичувач SSD:']+';'+versum[x]['Накопичувач HDD:']
                except:
                    if 'Накопичувач SSD:' in versum[x]:
                        hdd = versum[x]['Накопичувач SSD:']
                    elif 'Накопичувач HDD:' in versum[x]:
                        hdd = versum[x]['Накопичувач HDD:']
                    else:
                        hdd = ''
                te.name_computers=versum[x]["name"]
                te.url_computers=versum[x]["comp_url"]
                te.price_computers=versum[x]["price"]
                te.proc_computers=versum[x]["Процесор:"]
                te.mb_computers=versum[x]["Материнська плата:"]
                te.mem_computers=versum[x]["Оперативна пам’ять:"]
                te.video_computers=versum[x]["Відеокарта:"]
                te.hdd_computers=hdd
                te.ps_computers=versum[x]["Блок живлення:"]
                te.case_computers=versum[x]["Корпус:"]
                te.cool_computers=versum[x]["Кулер:"]
                te.wifi_computers=versum[x]["Wi-Fi адаптер:"]
                te.vent_computers=versum[x]["Вентилятори:"]
                te.class_computers=''
                te.warranty_computers=''
                te.save()
                temp = temp[1:]
                for q in temp:
                    q.delete()
                count_on += 1
                try:
                    temp_=round(float(re.sub(r'\D','',str(te.price_computers)))/usd)
                except:
                    temp_=te.price_computers
                #cp=CompPrice.objects.filter(name_computers=te.name_computers)
                cp=te.compprice
                if not cp:
                    cp=CompPrice.objects.create(name_computers=te.name_computers,price_computers=temp_,computers=te)
                else:
                    cp.price_computers=temp_
                    cp.save()
        except:
            print(f'error in  on {x}')


    print(f'Versum changes were added to {count_on} comps , and {count_no} comps were created in bd')
    with open("load_form_providers/loads/log.json", "r") as write_file:
        dict_log=json.load(write_file)
    dict_versum_log = {'time': timezone.now().strftime("%d-%m-%y,%H:%M"),
    'mes': f'Versum changes were added to {count_on} comps , and {count_no} comps were created in bd'}
    dict_log['dict_versum_log'] = dict_versum_log
    if not Results.objects.filter(who='versum').exists():
        r = Results(who='versum',
        who_desc=f'Versum add: {count_no} comps, update: {count_on} comps')
        r.save()
    else:
        r = Results.objects.get(who='versum')
        r.who_desc = f'Versum add: {count_no} comps, update: {count_on} comps'
        r.save()
    with open("load_form_providers/loads/log.json", "w") as write_file:
        json.dump(dict_log,write_file)
#if ver.loc[x].proc.Name==temp.proc_computers and ver.loc[x].video.Name==temp.video_computers:
