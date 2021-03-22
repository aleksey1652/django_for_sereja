from cat.models import *
from eldorado_get_json import get_itblok
from comp_class import IT_LOTS
import json,pickle,re
import pandas as pd
import time,datetime
from django.utils import timezone
from scrapy import get_video,get_cpu,get_mb,get_case,get_ps,get_cool,get_hdd_ssd,get_mem

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

"""with open("dict_code.json", "r") as write_file:
        dict_code=json.load(write_file)"""
try:
    usd = USD.objects.first().usd
except:
    with open('load_form_providers/usd_ua.pickle', 'rb') as f:
        usd = pickle.load(f)

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

def load_itblok():
    try:
        itbasa=get_itblok()
        """it=IT_LOTS(dict_code)
        it._IT_LOTS__sheet=pd.DataFrame()
        it._IT_LOTS__basa=pd.DataFrame(columns=it._IT_LOTS__cil)
        it.set_panda_set(itblok)
        itbasa=it.it_basa()
        itbasa.to_json('load_form_providers/loads/it_basa.json')"""
    except:
        """print('loaded itblok error but will be try load old assemly')
        itbasa = pd.read_json('load_form_providers/loads/it_basa.json')"""
        with open("load_form_providers/loads/it_blok_price2.json", "r") as write_file:
            itbasa = json.load(write_file)
    #itbasa = pd.read_json('load_form_providers/loads/it_basa.json')
    temp_comp_on=[]
    temp_comp_no=[]
    comp_it=Computers.objects.filter(pc_assembly__sites__name_sites='itblok')
    if not comp_it.exists():
        site,p_ = Sites.objects.get_or_create(name_sites='itblok',more='https://it-blok.com.ua')
        pcassembly_it,p_ = Pc_assembly.objects.get_or_create(name_assembly='amd',sites=site)
        pcassembly_it,p_ = Pc_assembly.objects.get_or_create(name_assembly='intel',sites=site)
        comp_it=Computers.objects.filter(pc_assembly__sites__name_sites='itblok')

    for i in itbasa:
        for k,v in itbasa[i].items():
            if k in ('proc','mb','mem','video','ps','case','cool'):
                if not Parts_short.objects.filter(name_parts=v):
                    if k == 'proc':
                        temp_a = to_article2(itbasa[i])
                    elif k == 'mb':
                        temp_a = to_article2(itbasa[i],pr=0)
                    else:
                        temp_a = k
                    partnumber_list = get_partnumber_list(temp_a,v)
                    p=Parts_short(name_parts=v,partnumber_list=partnumber_list,kind=temp_a,kind2=True)
                    p.save()
            elif k == 'hdd':
                for h in v.split(';'):
                    if h.find('ssd') != -1 or h.find('vme') != -1:
                        temp_a = 'ssd'
                    else:
                        temp_a = 'hdd'
                    if not Parts_short.objects.filter(name_parts=h):
                        p=Parts_short(name_parts=h,partnumber_list="[]",kind=temp_a,kind2=True)
                        p.save()

    for x in itbasa:
        if comp_it.filter(name_computers=x.strip()).exists():
            temp_comp_on.append(itbasa[x]['name'])
        else:
            temp_comp_no.append(itbasa[x]['name'])
    count_no = 0
    for y in temp_comp_no:
        y_name = y
        if y_name.lower().find('msi') !=-1:
            try:
                pcassembly_it = Pc_assembly.objects.get(name_assembly='msi',sites__name_sites='itblok')
            except:
                site,p_ = Sites.objects.get_or_create(name_sites='itblok',more='https://it-blok.com.ua')
                pcassembly_it = Pc_assembly.objects.create(name_assembly='msi',sites=site)
        elif y_name.lower().find('aorus') !=-1:
            try:
                pcassembly_it = Pc_assembly.objects.get(name_assembly='aorus',sites__name_sites='itblok')
            except:
                site,p_ = Sites.objects.get_or_create(name_sites='itblok',more='https://it-blok.com.ua')
                pcassembly_it = Pc_assembly.objects.create(name_assembly='aorus',sites=site)
        elif y_name.lower().find('gigabyte') !=-1:
            try:
                pcassembly_it = Pc_assembly.objects.get(name_assembly='aorus',sites__name_sites='itblok')
            except:
                site,p_ = Sites.objects.get_or_create(name_sites='itblok',more='https://it-blok.com.ua')
                pcassembly_it = Pc_assembly.objects.create(name_assembly='aorus',sites=site)
        else:
            kind = to_article2(itbasa[y_name])
            kind_ = {'aproc':'amd','iproc':'intel'}
            site,p_ = Sites.objects.get_or_create(name_sites='itblok',more='https://it-blok.com.ua')
            pcassembly_it,p_ = Pc_assembly.objects.get_or_create(name_assembly=kind_[kind],sites=site)
        if not Computers.objects.filter(name_computers=y_name,pc_assembly__sites__name_sites='itblok'):
            try:
                c = Computers.objects.create(name_computers=y_name,url_computers=itbasa[y_name]['comp_url'],
                price_computers=itbasa[y_name]['price'],proc_computers=itbasa[y_name]['proc'],
                mb_computers=itbasa[y_name]['mb'],mem_computers=itbasa[y_name]['mem'],
                video_computers=itbasa[y_name]['video'],hdd_computers=itbasa[y_name]['hdd'],
                ps_computers=itbasa[y_name]['ps'],case_computers=itbasa[y_name]['case'],
                cool_computers=itbasa[y_name]['cool'],class_computers='',
                warranty_computers='',
                vent_computers='empty',vent_num_computers=1,mem_num_computers=1,
                video_num_computers=1,pc_assembly=pcassembly_it)
                try:
                    temp=round(float(re.sub(r'\D','',c.price_computers))/usd)
                except:
                    temp=c.price_computers
                cp=CompPrice.objects.filter(name_computers=c.name_computers)
                if not cp:
                    CompPrice.objects.create(name_computers=c.name_computers,price_computers=temp,computers=c)
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
    count_on =0
    for x in temp_comp_on:
        try:
            temp = Computers.objects.filter(name_computers=x,pc_assembly__sites__name_sites='itblok')
            if temp.exists():
                te = temp.first()
                te.name_computers=itbasa[x]["name"]
                te.url_computers=itbasa[x]["comp_url"]
                te.price_computers=itbasa[x]["price"]
                te.proc_computers=itbasa[x]["proc"]
                te.mb_computers=itbasa[x]["mb"]
                te.mem_computers=itbasa[x]["mem"]
                te.video_computers=itbasa[x]["video"]
                te.hdd_computers=itbasa[x]['hdd']
                te.ps_computers=itbasa[x]["ps"]
                te.case_computers=itbasa[x]["case"]
                te.cool_computers=itbasa[x]["cool"]
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
                    CompPrice.objects.create(name_computers=te.name_computers,price_computers=temp_,computers=te)
                else:
                    cf=cp.first()
                    cf.price_computers=temp_
                    cf.save()
                    cp=cp[1:]
                    for q in cp:
                        q.delete()
        except:
            print(f'error in  on {x}')

    """for x in itbasa.iloc:
        dict_ = {'proc':x.proc,'mb':x.mb,'mem':x.mem,
        'video':x.video,'ps':x.ps,'case':x.case,'cool':x.cool}
        for k,d in dict_.items():
            if not isinstance(d,str) and not Parts_short.objects.filter(name_parts=d['Name']):
                temp_a = ''
                if isinstance(d['Partnumbers'],list) and len(d['Partnumbers'])>0:
                    a=Articles.objects.filter(article=d['Partnumbers'][0])
                    if a:
                        temp_a = a.first().item_price
                    else:
                        if k not in ('proc','mb'):
                            temp_a = k
                        elif k == 'proc':
                            temp_a = to_article(d,pr=1)
                        elif k == 'mb':
                            temp_a = to_article(x.proc,pr=0)
                p=Parts_short(name_parts=d['Name'],partnumber_list=f"{d['Partnumbers'][:10]}",kind=temp_a,kind2=False)
                p.save()
        for h in x.hdd:
            if not isinstance(h,str) and not Parts_short.objects.filter(name_parts=h['Name']):
                temp_a = ''
                if isinstance(h['Partnumbers'],list) and len(h['Partnumbers'])>0:
                    a=Articles.objects.filter(article=h['Partnumbers'][0])
                    if a:
                        temp_a = a.first().item_price
                p=Parts_short(name_parts=h['Name'],partnumber_list=f"{h['Partnumbers'][:10]}",kind=temp_a,kind2=False)
                p.save()"""

    """for x in itbasa.iloc:
        temp=''
        for y in comp_it:
            if x['name']==y.name_computers:
                temp_comp_on.append(x.name)
                temp='1'
                break
        if not temp:
            temp_comp_no.append(x.name)

    count_on = 0
    for x in temp_comp_on:
        try:
            t=to_comp(itbasa.loc[x])
            #temp = Computers.objects.filter(name_computers=itbasa.loc[x]['name'])
            temp = Computers.objects.filter(name_computers=x,pc_assembly__sites__name_sites='itblok')
            if temp.count()>=1:
                te = temp.first()
                te.name_computers=t['name_computers']
                te.url_computers=t['url_computers']
                te.price_computers=t['price_computers']
                te.proc_computers=t['proc_computers']
                te.mb_computers=t['mb_computers']
                te.mem_computers=t['mem_computers']
                te.video_computers=t['video_computers']
                te.hdd_computers=t['hdd_computers']
                te.ps_computers=t['ps_computers']
                te.case_computers=t['case_computers']
                te.cool_computers=t['cool_computers']
                te.class_computers=t['class_computers']
                te.warranty_computers=t['warranty_computers']
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
                    CompPrice.objects.create(name_computers=te.name_computers,price_computers=temp_,computers=te)
                else:
                    cf=cp.first()
                    cf.price_computers=temp_
                    cf.save()
                    cp=cp[1:]
                    for q in cp:
                        q.delete()
        except:
            print(f'error in  on {x}')

    count_no =0
    for y in temp_comp_no:
        y_name = y
        if y_name.lower().find('msi') !=-1:
            pcassembly_it = Pc_assembly.objects.get(name_assembly='msi',sites__name_sites='itblok')
        elif y_name.lower().find('aorus') !=-1:
            pcassembly_it = Pc_assembly.objects.get(name_assembly='aorus',sites__name_sites='itblok')
        elif y_name.lower().find('gigabyte') !=-1:
            pcassembly_it = Pc_assembly.objects.get(name_assembly='aorus',sites__name_sites='itblok')
        else:
            if  not isinstance(itbasa.loc[y].proc, str):
                pa = Parts_short.objects.filter(name_parts=itbasa.loc[y].proc['Name'])
                if pa:
                    pak = pa[0].kind
                    if pak == 'aproc':
                        pcassembly_it = Pc_assembly.objects.get(name_assembly='amd',sites__name_sites='itblok')
                    elif pak == 'iproc':
                        pcassembly_it = Pc_assembly.objects.get(name_assembly='intel',sites__name_sites='itblok')
                    else:
                        if pa[0].name_parts.lower().find('i') != -1 and pa[0].name_parts.lower().find('i') <12:
                            pcassembly_it = Pc_assembly.objects.get(name_assembly='intel',sites__name_sites='itblok')
                        else:
                            pcassembly_it = Pc_assembly.objects.get(name_assembly='amd',sites__name_sites='itblok')
                else:
                    continue
            else:
                continue
        try:
            t=to_comp(itbasa.loc[y])
            if not Computers.objects.filter(name_computers=t['name_computers'],pc_assembly__sites__name_sites='itblok'):
                c = Computers.objects.create(name_computers=t['name_computers'],url_computers=t['url_computers'],
                price_computers=t['price_computers'],proc_computers=t['proc_computers'],
                mb_computers=t['mb_computers'],mem_computers=t['mem_computers'],
                video_computers=t['video_computers'],hdd_computers=t['hdd_computers'],
                ps_computers=t['ps_computers'],case_computers=t['case_computers'],
                cool_computers=t['cool_computers'],class_computers=t['class_computers'],
                warranty_computers=t['warranty_computers'],
                vent_computers='empty',vent_num_computers=1,mem_num_computers=1,
                video_num_computers=1,pc_assembly=pcassembly_it)
                try:
                    temp=round(float(re.sub(r'\D','',c.price_computers))/usd)
                except:
                    temp=c.price_computers
                cp=CompPrice.objects.filter(name_computers=c.name_computers)
                if not cp:
                    CompPrice.objects.create(name_computers=c.name_computers,price_computers=temp,computers=c)
                else:
                    cp=cp.first()
                    cp.price_computers=temp
                    cp.save()
                    cp=cp[1:]
                    for q in cp:
                        q.delete()
                count_no += 1
        except:
            print(f'error in  no {y}')"""

    """ps_it = Pc_assembly.objects.filter(sites__name_sites='itblok')
    count_no =0
    for y in temp_comp_no:
        for x in ps_it:
            temp=x.computers_set.first()
            if temp:
                if  not isinstance(itbasa.loc[y].proc, str) and not isinstance(itbasa.loc[y].video, str):
                    try:
                        if itbasa.loc[y].proc['Name']==temp.proc_computers and itbasa.loc[y].video['Name']==temp.video_computers:
                            t=to_comp(itbasa.loc[y])
                            pcassembly_it = x
                            if not Computers.objects.filter(name_computers=t['name_computers']):
                                c=Computers(name_computers=t['name_computers'],url_computers=t['url_computers'],
                                price_computers=t['price_computers'],proc_computers=t['proc_computers'],
                                mb_computers=t['mb_computers'],mem_computers=t['mem_computers'],
                                video_computers=t['video_computers'],hdd_computers=t['hdd_computers'],
                                ps_computers=t['ps_computers'],case_computers=t['case_computers'],
                                cool_computers=t['cool_computers'],class_computers=t['class_computers'],
                                warranty_computers=t['warranty_computers'],
                                vent_computers='empty',vent_num_computers=1,mem_num_computers=1,
                                video_num_computers=1,pc_assembly=pcassembly_it)
                                c.save()
                                count_no += 1
                    except:
                        print(f'error in  no {y}')"""
    print(f'Itblok changes were added to {len(temp_comp_on)} comps , and {count_no} comps were created in bd')
    with open("load_form_providers/loads/log.json", "r") as write_file:
        dict_log=json.load(write_file)
    dict_it_log = {'time': timezone.now().strftime("%d-%m-%y,%H:%M"),
    'mes': f'Itblok changes were added to {len(temp_comp_on)} comps , and {count_no} comps were created in bd'}
    dict_log['dict_it_log'] = dict_it_log
    with open("load_form_providers/loads/log.json", "w") as write_file:
        json.dump(dict_log,write_file)

"""def get_params(obj1,obj2):
    return (
            (obj1.proc_computers,obj2.proc_computers),
            (obj1.mb_computers,obj2.mb_computers),
            (obj1.mem_computers,obj2.mem_computers),
            (obj1.video_computers,obj2.video_computers),
            (obj1.hdd_computers,obj2.hdd_computers),
            (obj1.case_computers,obj2.case_computers),
            (obj1.ps_computers,obj2.ps_computers),
            (obj1.cool_computers,obj2.cool_computers),
            (obj1.price_computers,obj2.price_computers)
            )

def compare_it_art():
    try:
        with open('load_form_providers/loads/it_basa.pickle', "rb") as f:
                ibasa=pickle.load(f)
        with open('load_form_providers/loads/art_basa.pickle', "rb") as f:
                abasa=pickle.load(f)
    except:
        print('not files from sites')
        return 0

    print('Prepare to compare')
    art_it = []
    for_our_site = []
    params =[]
    for x in ibasa.iloc:
        for y in abasa.iloc:
            if  not isinstance(x.proc, str) and not isinstance(x.video, str) and not isinstance(x.mem, str) and not isinstance(y.proc, str) and not isinstance(y.video, str) and not isinstance(y.mem, str):
                if x.proc.X_code==y.proc.X_code and x.video.X_code==y.video.X_code and x.mem.X_code[:2]==y.mem.X_code[:2]:
                    art_it.append((x.name,y.name))
                    break
    print('Compare is ending')

    for x,y in art_it:
        it=Computers.objects.filter(pc_assembly__sites__name_sites='itblok').filter(name_computers=ibasa.loc[x]['name'])
        art=Computers.objects.filter(pc_assembly__sites__name_sites='art').filter(name_computers=abasa.loc[y]['name'])
        if it and art:
            for_our_site.append((it.first(),art.first(),get_params(it.first(),art.first())))

    if for_our_site:
        s1,s2 = for_our_site[0][0],for_our_site[0][1]

    else:
        s1,s2 = None,None

    context = {
               'comps': for_our_site,
               'site_1': s1,
               'site_2': s2
              }
    print('go to site')

    return context"""
