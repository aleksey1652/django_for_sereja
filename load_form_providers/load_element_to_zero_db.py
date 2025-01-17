from get_service import Service
import os,django,pickle, json,re
from cat.models import *
import time,datetime
from django.contrib import messages
from pars.views import need_comps
from django.utils import timezone

def status(avail, avail_prov):
    dict_prov = {
                'asbis':{'звоните':'q','достаточно':'yes','мало':'q'},
                'dc':{'*****':'yes','****':'yes','***':'yes','**':'yes','*':'yes','z':'q','w':'q'},
                'elko':{'> 50':'yes','0':'no'},
                'edg':{'Зарезервировано':'q','Есть в наличии':'yes','Нет в наличии':'no'},
                'brain':{'1':'q','2':'yes','3':'yes'},
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

def main(request):
    dict_v2 = {
    'proc':'CPU.objects.filter(part_number=p21.partnumber_parts)',
    'cool':'Cooler.objects.filter(part_number=p21.partnumber_parts)',
    'mb':'MB.objects.filter(part_number=p21.partnumber_parts)',
    'mem':'RAM.objects.filter(part_number=p21.partnumber_parts)',
    'hdd':'HDD.objects.filter(part_number=p21.partnumber_parts)',
    'ssd':'SSD.objects.filter(part_number=p21.partnumber_parts)',
    'video':'GPU.objects.filter(part_number=p21.partnumber_parts)',
    'ps':'PSU.objects.filter(part_number=p21.partnumber_parts)',
    'vent':'FAN.objects.filter(part_number=p21.partnumber_parts)',
    'case':'CASE.objects.filter(part_number=p21.partnumber_parts)',
    'wifi':'WiFi.objects.filter(part_number=p21.partnumber_parts)',
    'cables':'Cables.objects.filter(part_number=p21.partnumber_parts)',
    'soft':'Soft.objects.filter(part_number=p21.partnumber_parts)'
            }
    service,CREDENTIALS_FILE,spreadsheetId=Service()
    def get_list_sheet(l, l2):
        results = service.spreadsheets().values().batchGet(spreadsheetId = spreadsheetId,
                                         ranges = f"{l}!{l2}",
                                         valueRenderOption = 'FORMATTED_VALUE',
                                         dateTimeRenderOption = 'FORMATTED_STRING').execute()
        return results['valueRanges'][0]['values']

    g=get_list_sheet('Price', 'A4:D900')
    with open("load_form_providers/list_articles.json", "r") as write_file:
                        list_get_list2=json.load(write_file)
    for k,v in list_get_list2.items():
        if not Articles.objects.filter(article=k).exists():
            try:
                Articles.objects.create(article=k,item_name=v[1],item_price=v[0])
                #print(f'article created article:{k},item_name:{v[1]},item_price:{v[0]}')
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
                #print(f'Parts_full created: name_parts:{x[0]},partnumber_parts:{x[1]},providerprice_parts:{price}')
            else:
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
                    p2 = Parts_full.objects.filter(partnumber_parts=x[1],providers=prov)
                    #a = Articles.objects.get(article=p2.first().partnumber_parts)
                    date = timezone.now()
                    if p2.count() > 1 :
                        messages.error(request, f'{p1.name_parts} with {p1.partnumber_parts} > 1')
                    else:
                        p21 = p2.first()
                        p21.providerprice_parts = price
                        p21.date_chg = date
                        p21.save()
                        for s in p21.parts_short_set.all():
                            short_kind = s.kind
                            s.x_code = price
                            s.date_chg = date
                            s.save()
                            if short_kind and short_kind[0] in ('a','i'):
                                short_kind2 = short_kind[1:]
                            else:
                                short_kind2 = short_kind
                            comps = need_comps(s.name_parts)
                            for c in comps:
                                procent = c.class_computers if c.class_computers else 1.19
                                cpr = c.compprice
                                if short_kind2 in ('ssd','hdd'):
                                    temp = c.hdd_computers
                                    temp = temp.split(';')
                                    if s.name_parts == temp[0]:
                                        cpr.hdd_computers = price
                                        cpr.save()
                                    elif len(temp) > 1 and temp[1] == s.name_parts:
                                        cpr.hdd2_computers = price
                                        cpr.save()
                                else:
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
                            d_short = eval(dict_v2[short_kind2])
                            if d_short:
                                d_short = d_short.first()
                                d_short.price = price
                                d_short.save()
                                #messages.success(request, f'in {short_kind}: {d_short .name} was changed price: {price}')
                        #if p2.count()>1:
                        #    messages.error(request, f'{p1.name_parts} with {p1.partnumber_parts} > 1')
