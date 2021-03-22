from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,HttpResponse
import itertools
import json,pickle
import os,re
import datetime,time
from django.utils import timezone
import pandas as pd
from get_service import Service
from load_form_providers.load_element import *
from pars.fury import *
from pars.itblok import *
from pars.versum import *
from pars.ua import *
from pars.art import *
from scrapy import get_video,get_cpu,get_mb,get_case,get_ps,get_cool,get_hdd_ssd,get_mem
#from sheet_class import *
#from comp_class import IT_LOTS,pack_data
#from cat.models import Parts_full,Articles,Providers,Pc_assembly,Computers,Parts_short
#from django.db.models import Min
#from django.views.generic import ListView
#from django.core.paginator import Paginator
#from django.db.models import Count
#from cat.forms import PartsForm_code, ComputersForm_code
from django.urls import reverse
from django.contrib import messages
from sereja.tasks import hello_world,task_providers,task_fury,task_itblok,task_versum,task_ua,task_art,after
from celery.schedules import crontab
from cat.models import *
from django.contrib import messages
from django.db.models import Min
from cat.forms import ShortSearchForm,ArticleCreateForm,ShortCreateForm,ShortdeForm
from django.db.models import Q
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from .serializers import *

#from django.core.files.storage import FileSystemStorage

#from pars.itblok import compare_it_art
#from django.core.paginator import Paginator

def handle_uploaded_file(f):
    with open('media/1c.xlsx', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def uploader(request,w):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        handle_uploaded_file(myfile)
        #fs = FileSystemStorage()
        #filename = fs.save(myfile.name, myfile)
        #uploaded_file_url = fs.url(filename)
        messages.success(request, f'Uploaded file: {myfile.name} to our site ')
        return  HttpResponseRedirect(
                                reverse('uploader',
                                kwargs={'w':'-'}
                                )
                                )
    context = {
               #'price': 'Home',
              }
    if w == 'update':
        try:
            task_providers.delay()
        except:
            Parsing_from_providers()
            messages.success(request, 'Price updating without tasc'+timezone.now().strftime("%m/%d--%H:%M"))
        messages.success(request, 'Price updating '+timezone.now().strftime("%m/%d--%H:%M"))
    if w == 'fury':
        try:
            task_fury.delay()
        except:
            load_fury()
            messages.success(request, 'Digitalfury updating without tasc'+timezone.now().strftime("%m/%d--%H:%M"))
        messages.success(request, 'Digitalfury updating '+timezone.now().strftime("%m/%d--%H:%M"))
    if w == 'itblok':
        try:
            task_itblok.delay()
        except:
            load_itblok()
            messages.success(request, 'Itblok updating without tasc'+timezone.now().strftime("%m/%d--%H:%M"))
        messages.success(request, 'Itblok updating '+timezone.now().strftime("%m/%d--%H:%M"))
    if w == 'versum':
        try:
            task_versum.delay()
        except:
            load_versum()
            messages.success(request, 'Versum updating without tasc'+timezone.now().strftime("%m/%d--%H:%M"))
        messages.success(request, 'Versum updating '+timezone.now().strftime("%m/%d--%H:%M"))
    """if w == 'ua':
        try:
            task_ua.delay()
        except:
            load_ua()
            messages.success(request, 'Uastore updating without tasc'+datetime.datetime.now().strftime("%m/%d--%H:%M"))
        messages.success(request, 'Uastore updating '+datetime.datetime.now().strftime("%m/%d--%H:%M"))"""
    if w == 'art':
        try:
            task_art.delay()
        except:
            load_art()
            messages.success(request, 'Art updating without tasc'+timezone.now().strftime("%m/%d--%H:%M"))
        messages.success(request, 'Artline updating '+timezone.now().strftime("%m/%d--%H:%M"))
    if w == 'hello':
        try:
            hello_world.delay()
        except:
            messages.success(request, 'Hello without tasc')
    if w == 'result':
        """res=hello_world.delay()
        r=res.ready()
        #r=str(res.state)
        #res2=after.delay()
        #r=res2['mes']
        messages.success(request, f'{r}')"""
        with open("load_form_providers/loads/log.json", "r") as write_file:
            dict_log=json.load(write_file)
        for x,y in dict_log.items():
            if 'time' in y and 'mes' in y:
                messages.success(request, f"{y['time']} : {y['mes']}")
    return render(request, 'pars/parsing.html', context)

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

def get_params(obj1,obj2):
    return (
            (obj1.proc_computers,obj2.computers.proc_computers),
            (obj1.mb_computers,obj2.computers.mb_computers),
            (obj1.mem_computers,obj2.computers.mem_computers),
            (obj1.video_computers,obj2.computers.video_computers),
            (obj1.hdd_computers,obj2.computers.hdd_computers),
            (obj1.case_computers,obj2.computers.case_computers),
            (obj1.ps_computers,obj2.computers.ps_computers),
            (obj1.cool_computers,obj2.computers.cool_computers),
            (obj1.price_computers,obj2.computers.price_computers)
            )

def get_params_1(obj):
    return get_xxx('proc',obj.proc_computers),get_xxx('video',obj.video_computers),get_xxx('mem',obj.mem_computers)

def compare_do(site1_name,site2_name,site1,site2,v=0):
    try:
        #basa1 = pd.read_json(f'load_form_providers/loads/{site1_name}.json')
        #basa2 = pd.read_json(f'load_form_providers/loads/{site2_name}.json')
        """with open(f'load_form_providers/loads/{site1_name}.pickle', "rb") as f:
                basa1=pickle.load(f)
        with open(f'load_form_providers/loads/{site2_name}.pickle', "rb") as f:
                basa2=pickle.load(f)"""
    except:
        print('not files from sites')
        return 0

    print('Prepare to compare')
    site1_site2 = []
    for_our_site = []
    params =[]
    var1=Computers.objects.filter(pc_assembly__sites__name_sites=site1)
    var2=Computers.objects.filter(pc_assembly__sites__name_sites=site2)
    #list_var1=[x.name_computers for x in var1]
    list_var2=[x.name_computers for x in var2]
    for c in var1:
        par_proc,par_video,par_mem = get_params_1(c)
        var2_filter = CompPrice.objects.filter(name_computers__in=list_var2,proc_computers=par_proc,video_computers=par_video,mem_computers=par_mem)
        for v in var2_filter:
            for_our_site.append((c,v.computers,get_params(c,v)))
            #site1_site2.append((c.name_computers,v.name_computers))
    print('Compare is ending')

    """if not v:
        for x in basa1.iloc:
            for y in basa2.iloc:
                if  not isinstance(x.proc, str) and not isinstance(x.video, str) and not isinstance(x.mem, str) and not isinstance(y.proc, str) and not isinstance(y.video, str) and not isinstance(y.mem, str):
                    if x.proc['X_code']==y.proc['X_code'] and x.video['X_code']==y.video['X_code'] and x.mem['X_code'][:1]==y.mem['X_code'][:1]:
                        site1_site2.append((x.name,y.name))
        print('Compare is ending')
    else:
        for x in basa1.iloc:
            if isinstance(x.video['X_code'], list) and (x.video['X_code'][-1] in ('gigabyte','msi','asus')):
                x.video['X_code'][-1] = ''
        for x in basa1.iloc:
            for y in basa2.iloc:
                if  not isinstance(x.proc, str) and not isinstance(x.video, str) and not isinstance(x.mem, str) and not isinstance(y.proc, str) and not isinstance(y.video, str) and not isinstance(y.mem, str):
                    if x.proc['X_code']==y.proc['X_code'] and x.video['X_code']==y.video['X_code'] and x.mem['X_code'][:1]==y.mem['X_code'][:1]:
                        site1_site2.append((x.name,y.name))
        print('Compare is ending')

    for x,y in site1_site2:
        v1=Computers.objects.filter(pc_assembly__sites__name_sites=site1).filter(name_computers=basa1.loc[x]['name'])
        v2=Computers.objects.filter(pc_assembly__sites__name_sites=site2).filter(name_computers=basa2.loc[y]['name'])
        if v1 and v2:
            for_our_site.append((v1.first(),v2.first(),get_params(v1.first(),v2.first())))"""

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

    return context

def compare_sites(request,duo):
    if duo == 'it_art':
        context = compare_do('it_basa','art_basa','itblok','art')
    #if duo == 'it_ua':
    #    context = compare_do('it_basa','ua_basa','itblok','ua')
    if duo == 'it_fury':
        context = compare_do('it_basa','fury_basa','itblok','fury')
    if duo == 'ver_art':
        context = compare_do('versum_basa','art_basa','versum','art',v=1)
    #if duo == 'ver_ua':
    #    context = compare_do('versum_basa','ua_basa','versum','ua',v=1)
    if duo == 'ver_fury':
        context = compare_do('versum_basa','fury_basa','versum','fury',v=1)
    #print(context)
    result = len(context['comps'])
    messages.success(request, f'comparison result : {result} comps')

    #paginator = Paginator(context['comps'], 40)
    #page_number = request.GET.get('page')
    #page_obj = paginator.get_page(page_number)
    #context['comps'] = page_obj

    return render(request, 'pars/compare.html', context)

def get_parts_on_site(request,p,w):
    dict_site = {
                'itblok':'it',
                'versum':'versum',
                'art':'art',
                #'ua':'ua',
                'fury':'fury'
                }
    dict_for_site = {
                'itblok':[],
                'versum':[],
                'art':[],
                #'ua':[],
                'fury':[],
                'other':[]
                }

    try:
        comp = Computers.objects.get(pk=p)
    except:
        print('not pk')
        messages.error(request, 'Not pk')
        return  HttpResponseRedirect(
                                    reverse('get_hdd_on_site',
                                    kwargs={'p':p}
                                    )
                                    )
    #parts = comp.__dict__[f'{w}_computers']
    try:
        site_parts = comp.pc_assembly.sites.name_sites
    except:
        site_parts = 'other'
    if w in ('proc','mb','video','mem','ps','case','cool'):
        itm = comp.__dict__[f'{w}_computers']
    elif w in ('1','0'):
        try:
            itm = comp.__dict__['hdd_computers'].split(';')[eval(w)]
        except:
            itm = ''
    else:
        itm = ''
    citm = need_comps(k=itm)
    if w in ('proc','mb','video','mem','ps','case','cool','1','0'):
        c_set = set()
        for x in Computers.objects.all():
            try:
                if w not in ('1','0'):
                    if get_xxx(w,x.__dict__[f"{w}_computers"]) == get_xxx(w,itm):
                        c_set.add(x.pk)
                else:
                    for y in x.__dict__["hdd_computers"].split(';'):
                        if get_xxx('hdd',y) == get_xxx('hdd',itm):
                            c_set.add(x.pk)
            except:
                print(x.pk,end=' ')
                continue
        for q in c_set:
            ca=Computers.objects.get(pk=q)
            try:
                dict_for_site[ca.pc_assembly.sites.name_sites].append(ca)
            except:
                dict_for_site['other'].append(ca)
    context = {
               'comps': dict_for_site
              }
    return render(request, 'pars/parts_on_site.html', context)


def get_hdd_on_site(request,p):
    comp = Computers.objects.get(pk=p)
    site_parts = comp.pc_assembly.sites.name_sites
    hdd = comp.hdd_computers
    hdd = hdd.split(';')
    hdd_list = []
    #hdd_dict = {'itblok':hdd_list,'versum':hdd_list,'art':hdd_list,'ua':hdd_list,'fury':hdd_list}
    for x in hdd:
        if x:
            hdd_list.append(x)
    context = {
               'hdd': hdd_list,
               'd': comp
              }
    return render(request, 'pars/hdd_on_site.html', context)

def get_price_on_site(request,p0,p1):
    try:
        comp_0 = Computers.objects.get(pk=p0)
        compprice_0 = comp_0.compprice
    except:
        print('not pk0 or him CompPrice')
    try:
        comp_1 = Computers.objects.get(pk=p1)
        compprice_1 = comp_1.compprice
    except:
        print('not pk0 or him CompPrice')
    #parts = comp.__dict__[f'{w}_computers']
    site_parts_0 = comp_0.pc_assembly.sites.name_sites
    site_parts_1 = comp_1.pc_assembly.sites.name_sites
    dict_site = {
                'itblok':'it',
                'versum':'versum',
                'art':'art',
                'ua':'ua',
                'fury':'fury'
                }
    dict_comp_0 = {'proc_computers':'','mb_computers':'','video_computers':'','mem_computers':'','ps_computers':'','case_computers':'','cool_computers':''}
    dict_comp_1 = {'proc_computers':'','mb_computers':'','video_computers':'','mem_computers':'','ps_computers':'','case_computers':'','cool_computers':''}
    dict_for_site = {}
    try:
        #var1=Computers.objects.filter(pc_assembly__sites__name_sites=site1)
        #var2=Computers.objects.filter(pc_assembly__sites__name_sites=site2)
        #basa_0 = pd.read_json(f'load_form_providers/loads/{dict_site[site_parts_0]}_basa.json')
        #basa_1 = pd.read_json(f'load_form_providers/loads/{dict_site[site_parts_1]}_basa.json')
        """with open(f'load_form_providers/loads/{dict_site[site_parts_0]}_basa.pickle', "rb") as f:
            basa_0=pickle.load(f)
        with open(f'load_form_providers/loads/{dict_site[site_parts_1]}_basa.pickle', "rb") as f:
            basa_1=pickle.load(f)"""
        usd = USD.objects.first().usd
    except:
        with open('load_form_providers/usd_ua.pickle', "rb") as f:
                usd=pickle.load(f)
        print('not basa file`')
    """if site_parts_0 != 'itblok':
        x = basa_0.loc[comp_0.name_computers]
    else:
        for i in basa_0.iloc:
            if i['name'] == comp_0.name_computers:
                x = i
                break"""
    """for i in basa_0.iloc:
        if i['name'] == comp_0.name_computers:
            x = i
            break"""
    for k,v in comp_0.__dict__.items():
        if k in ('proc_computers', 'mb_computers', 'mem_computers',
                'video_computers', 'ps_computers',
                'case_computers', 'cool_computers'):
            try:
                temp_short = Parts_short.objects.filter(name_parts=v)[0].partnumber_list
            except:
                temp_short = '[]'
            temp_list = Parts_full.objects.filter(
            partnumber_parts__in=eval(temp_short))
            temp = temp_list.aggregate(a=Min('providerprice_parts'))['a']
            temp2 = compprice_0.__dict__[k]
            dict_comp_0[k] = (v,temp_list,temp,temp2)
        elif k == 'hdd_computers':
            for h in v.split(';'):
                try:
                    temp_short = Parts_short.objects.filter(name_parts=h)[0].partnumber_list
                except:
                    temp_short = '[]'
                temp_list = Parts_full.objects.filter(
                partnumber_parts__in=eval(temp_short))
                temp = temp_list.aggregate(a=Min('providerprice_parts'))['a']
                if 'hdd1' not in dict_comp_0:
                    temp2 = compprice_0.__dict__["hdd_computers"]
                    dict_comp_0['hdd1'] = (h,temp_list,temp,temp2)
                else:
                    temp2 = compprice_0.__dict__["hdd2_computers"]
                    dict_comp_0['hdd2'] = (h,temp_list,temp,temp2)
    """for d in dict_comp_0:
        if not isinstance(x[d], str) and isinstance(x[d]['Partnumbers'], list):
            temp_list = Parts_full.objects.filter(
            partnumber_parts__in=x[d]['Partnumbers'])
            temp = temp_list.aggregate(a=Min('providerprice_parts'))['a']
            #pf = Parts_short.objects.filter(name_parts=x[d]['Name'])
            #temp2 = pf.first() if pf.count()==1 else ''
            temp2 = compprice_0.__dict__[f"{d}_computers"]
            dict_comp_0[d] = (x[d]['Name'],temp_list,temp,temp2)
        else:
            dict_comp_0[d] = (d,[],'')
    if isinstance(x['hdd'], list):
        for h in x['hdd']:
            if not isinstance(h, str):
                temp_list = Parts_full.objects.filter(
                partnumber_parts__in=h['Partnumbers'])
                temp = temp_list.aggregate(a=Min('providerprice_parts'))['a']
                if 'hdd1' not in dict_comp_0:
                    #pf = Parts_short.objects.filter(name_parts=h['Name'])
                    #temp2 = pf.first() if pf.count()==1 else ''
                    temp2 = compprice_0.__dict__["hdd_computers"]
                    dict_comp_0['hdd1'] = (h['Name'],temp_list,temp,temp2)
                else:
                    #pf = Parts_short.objects.filter(name_parts=h['Name'])
                    #temp2 = pf.first() if pf.count()==1 else ''
                    temp2 = compprice_0.__dict__["hdd2_computers"]
                    dict_comp_0['hdd2'] = (h['Name'],temp_list,temp,temp2)
    else:
        dict_comp_0['hdd1'] = ('hdd1',[],'','')
    if site_parts_1 == 'ua':
        x = basa_1.loc[comp_1.name_computers]
        x.case = 'case'
    else:
        x = basa_1.loc[comp_1.name_computers]"""
    for k,v in comp_1.__dict__.items():
        if k in ('mem_computers',
                'video_computers', 'ps_computers',
                'case_computers', 'cool_computers'):
            try:
                temp_short = get_partnumber_list(k[:-10],v)
            except:
                temp_short = '[]'
            temp_list = Parts_full.objects.filter(
            partnumber_parts__in=eval(temp_short))
            temp = temp_list.aggregate(a=Min('providerprice_parts'))['a']
            #temp2 = compprice_0.__dict__[k]
            dict_comp_1[k] = (v,temp_list,temp)
        elif k == 'proc_computers':
            try:
                temp_short = get_partnumber_list(to_article2(d),v)
            except:
                temp_short = '[]'
            temp_list = Parts_full.objects.filter(
            partnumber_parts__in=eval(temp_short))
            temp = temp_list.aggregate(a=Min('providerprice_parts'))['a']
            #temp2 = compprice_0.__dict__[k]
            dict_comp_1[k] = (v,temp_list,temp)
        elif k == 'mb_computers':
            try:
                temp_short = get_partnumber_list(to_article2(comp_1.proc_computers,pr=0),v)
            except:
                temp_short = '[]'
            temp_list = Parts_full.objects.filter(
            partnumber_parts__in=eval(temp_short))
            temp = temp_list.aggregate(a=Min('providerprice_parts'))['a']
            #temp2 = compprice_0.__dict__[k]
            dict_comp_1[k] = (v,temp_list,temp)
        elif k == 'hdd_computers':
            for h in v.split(';'):
                try:
                    temp_short = Parts_short.objects.filter(name_parts=h)[0].partnumber_list
                except:
                    temp_short = '[]'
                temp_list = Parts_full.objects.filter(
                partnumber_parts__in=eval(temp_short))
                temp = temp_list.aggregate(a=Min('providerprice_parts'))['a']
                if 'hdd1' not in dict_comp_1:
                    #temp2 = compprice_0.__dict__["hdd_computers"]
                    dict_comp_1['hdd1'] = (h,temp_list,temp,temp2)
                else:
                    #temp2 = compprice_0.__dict__["hdd2_computers"]
                    dict_comp_1['hdd2'] = (h,temp_list,temp,temp2)
    """for d in dict_comp_1:
        if not isinstance(x[d], str) and isinstance(x[d]['Partnumbers'], list):
            temp = Parts_full.objects.filter(
            partnumber_parts__in=x[d]['Partnumbers']).aggregate(a=Min('providerprice_parts'))['a']
            dict_comp_1[d] = (x[d]['Name'],[],temp)
        else:
            dict_comp_1[d] = (d,[],'')
    if isinstance(x['hdd'], list):
        for h in x['hdd']:
            if not isinstance(h, str):
                temp_list = Parts_full.objects.filter(
                partnumber_parts__in=h['Partnumbers'])
                temp = temp_list.aggregate(a=Min('providerprice_parts'))['a']
                if 'hdd1' not in dict_comp_1:
                    dict_comp_1['hdd1'] = (h['Name'],temp_list,temp)
                else:
                    dict_comp_1['hdd2'] = (h['Name'],temp_list,temp)
    else:
        dict_comp_1['hdd1'] = ('hdd1',[],'')"""
    try:
        usd1 = compprice_0.price_computers
        usd2 = compprice_1.price_computers
    except:
        usd = 1
        usd2 = 1

    context = {
               'comp1': dict_comp_0,
               'comp2': dict_comp_1,
               'comp1_' :comp_0,
               'comp2_' :comp_1,
               'usd1': usd1,
               'usd2': usd2
              }
    return render(request, 'pars/price_on_site.html', context)

def need_comps(k):
    if not isinstance(k, str):
        k = k.name_parts
    ff = Computers.objects.filter(cool_computers=k)
    if ff:
        return ff
    ff = Computers.objects.filter(case_computers=k)
    if ff:
        return ff
    ff = Computers.objects.filter(ps_computers=k)
    if ff:
        return ff
    ff = Computers.objects.filter(proc_computers=k)
    if ff:
        return ff
    ff = Computers.objects.filter(mb_computers=k)
    if ff:
        return ff
    ff = Computers.objects.filter(mem_computers=k)
    if ff:
        return ff
    ff = Computers.objects.filter(video_computers=k)
    if ff:
        return ff
    ff = Computers.objects.filter(cool_computers=k)
    if ff:
        return ff
    ff = Computers.objects.filter(hdd_computers__icontains=k)
    if ff:
        return ff
    return ff


def get_negative_margin(request):
    dict_el={'cool':[],'imb':[],'case':[],'ssd':[],'hdd':[],
    'aproc':[],'iproc':[],'amb':[],'video':[],'ps':[],'mem':[]}
    if request.method == 'GET':
        form = ShortSearchForm()
        for x in Parts_short.objects.all():
            if x.min_price and x.x_code and float(x.min_price) > float(x.x_code):
                c = need_comps(x)
                if x.kind:
                    if c:
                        dict_el[x.kind].append((x,c))
                    else:
                        dict_el[x.kind].append((x,[]))
        context = {
                   'short': dict_el,
                   'pos_neg':'name_parts',
                   'form': form
                  }
        return render(request, 'pars/neg_marg.html', context)
    elif request.method == 'POST':
        form = ShortSearchForm(request.POST)
        if form.is_valid():
            search = form.cleaned_data['name_parts']
            p=Parts_short.objects.filter(name_parts__icontains=search)
            if p:
                for pp in p:
                    c=need_comps(pp)
                    if pp.kind:
                        if c:
                            dict_el[pp.kind].append((pp,c))
                        else:
                            dict_el[pp.kind].append((pp,[]))
            else:
                messages.warning(request, 'Nothing')
        else:
            messages.error(request, 'Empty form')
            return  HttpResponseRedirect(
                                        reverse('get_negative_margin'
                                        )
                                        )

        context = {
                   'short': dict_el,
                   'pos_neg':'name_parts',
                   'form': form
                  }
        return render(request, 'pars/neg_marg.html', context)

def get_positive_margin(request):
    dict_el={'cool':[],'imb':[],'case':[],'ssd':[],'hdd':[],
    'aproc':[],'iproc':[],'amb':[],'video':[],'ps':[],'mem':[]}
    if request.method == 'GET':
        form = ShortSearchForm()
        context = {
                   'short': dict_el,
                   'pos_neg':'procent',
                   'form': form
                  }
        return render(request, 'pars/neg_marg.html', context)
    elif request.method == 'POST':
        form = ShortSearchForm(request.POST)
        if form.is_valid():
            search = form.cleaned_data['name_parts']
            try:
                float(search)
            except:
                messages.error(request, 'Only digit')
                return  HttpResponseRedirect(
                                            reverse('get_positive_margin'
                                            )
                                            )
            for x in Parts_short.objects.all():
                if x.min_price and x.min_price != '' and float(x.min_price) > 0:
                    if x.min_price and x.x_code and (float(x.x_code)/float(x.min_price)-1) > 0.01*float(search):
                        c = need_comps(x)
                        if x.kind:
                            if c:
                                dict_el[x.kind].append((x,c))
                            else:
                                dict_el[x.kind].append((x,[]))
        else:
            messages.error(request, 'Empty form')
            return  HttpResponseRedirect(
                                        reverse('get_positive_margin'
                                        )
                                        )

        context = {
                   'short': dict_el,
                   'pos_neg':'procent',
                   'form': form
                  }
        return render(request, 'pars/neg_marg.html', context)

def articlestart(request,p):
    if p == 0:
        from load_form_providers.load_element_to_zero_db import main
        main(request)
    if p == 1:
        from load_form_providers.load_element import Cooler_to_db,Mb_to_db,Cooler_to_db,Cpu_to_db,Ram_to_db,Hdd_to_db,Psu_to_db,Gpu_to_db,Fan_to_db,Case_to_db,Ssd_to_db
        list_ = (Cooler_to_db(),Mb_to_db(),Cooler_to_db(),Cpu_to_db(),Ram_to_db(),Hdd_to_db(),Psu_to_db(),Gpu_to_db(),Fan_to_db(),Case_to_db(),Ssd_to_db())
        for l in list_:
            try:
                l
            except:
                print(f'error in ')
    return  HttpResponseRedirect(
                                reverse('articlecreate'
                                )
                                )

def articlecreate(request):
    if request.method == 'GET':
        formd = ShortdeForm()
        form = ArticleCreateForm()
        form2 = ShortCreateForm(initial={
        'update': 'no'})
        kind_no = Parts_short.objects.filter(kind='')
        for k in kind_no:
            messages.info(request, f'This parts without kind {k.name_parts}')
        context = {
                   'form': form,
                   'form2': form2,
                   'formd': formd
                  }
        #messages.info(request, 'For new article used kind: cool, imb, case, ssd, hdd, aproc, iproc, amb, video, ps, mem')
        return render(request, 'pars/article_created.html', context)
    elif request.method == 'POST':
        if 'del' in request.POST:
            pp=Parts_short.objects.get(pk=int(request.POST['del']))
            need = need_comps(pp)
            pp.delete()
            for m in need:
                messages.success(request, f'{pp.name_parts} is deleted but they in:{m}')
            return  HttpResponseRedirect(
                                        reverse('articlecreate'
                                        )
                                        )
        if 'stick' in request.POST:
            param = request.POST['stick'].split(';')
            pp=Parts_full.objects.get(pk=int(param[0]))
            pfull = Parts_full.objects.filter(partnumber_parts=pp.partnumber_parts,providers__name_provider='-')
            if pfull and pfull.count() == 1:
                pfull = pfull.first()
                pshort = Parts_short.objects.get(pk=int(param[1]))
                pshort.parts_full.add(pfull)
                messages.success(request, f'Now {pshort.name_parts} sticking with {pfull.name_parts}')
            else:
                messages.error(request, f'{pfull} error')
            return  HttpResponseRedirect(
                                        reverse('articlecreate'
                                        )
                                        )
        form = ArticleCreateForm(request.POST)
        form2 = ShortCreateForm(request.POST)
        formd = ShortdeForm(request.POST)
        context = {
                   'form': form,
                   'form2': form2,
                   'formd': formd
                  }
        if form2.is_valid():
            temp = []
            parts = form2.cleaned_data['name_parts']
            fkind = form2.cleaned_data['kind']
            fkind2 = form2.cleaned_data['kind2']
            update = form2.cleaned_data['update']
            if_search = Parts_short.objects.filter(name_parts=parts)
            if not if_search:
                short = Parts_short.objects.create(name_parts=parts,kind=fkind,kind2=fkind2)
                temp = []
                if fkind[0] in ('a','i'):
                    fkind_ = fkind[1:]
                else:
                    fkind_ = fkind
                if fkind not in ('mon','wifi','km','case','vent','cool'):
                    for x in Parts_full.objects.filter(providers__name_provider='-'):
                        if get_xxx(fkind_,x.name_parts) == get_xxx(fkind_,parts):
                            temp.append(x.partnumber_parts)
                    if temp:
                        short.partnumber_list = f"{temp[:10]}"
                        short.save()
                    else:
                        short.partnumber_list = "[]"
                        short.save()
                else:
                    short.partnumber_list = "[]"
                    short.save()
                messages.success(request,f"Parts: {parts} is created")
            elif update =='no' and if_search:
                messages.warning(request,f"Parts: {parts} is exist for update enter (yes)")
                return  HttpResponseRedirect(
                                            reverse('articlecreate'
                                            )
                                            )
            elif update == 'yes' and if_search:
                try:
                    short = Parts_short.objects.get(name_parts=parts)
                except:
                    messages.error(request,'error meybe more then one parts')
                    return  HttpResponseRedirect(
                                                reverse('articlecreate'
                                                )
                                                )
                if not fkind2:
                    temp = []
                    if fkind[0] in ('a','i'):
                        fkind_ = fkind[1:]
                    else:
                        fkind_ = fkind
                    for x in Parts_full.objects.filter(providers__name_provider='-'):
                        if get_xxx(fkind_,x.name_parts) == get_xxx(fkind_,parts):
                            temp.append(x.partnumber_parts)
                short.kind = fkind
                short.kind2 = fkind2
                short.date_chg = timezone.now()
                short.partnumber_list = f"{temp[:10]}"
                short.save()
                messages.success(request,f"Parts: {parts} is update")
            if temp:
                par = []
                for x in temp:
                    p = Parts_full.objects.filter(partnumber_parts=x).distinct().order_by(
                    'providers__name_provider')
                    if p.count():
                        par.append(p)
                form = ArticleCreateForm()
                form2 = ShortCreateForm()
                context = {
                           'form': form,
                           'form2': form2,
                           'formd': formd,
                           'par': par,
                           'short': short.pk
                          }
                return render(request, 'pars/article_created.html', context)
            return  HttpResponseRedirect(
                                        reverse('articlecreate'
                                        )
                                        )
            #return HttpResponse(f"{name_parts}{partnumber_list}{kind2}{update}")

        if form.is_valid():
            article_art = form.cleaned_data['article']
            article_name = form.cleaned_data['item_name']
            article_kind = form.cleaned_data['item_price']
            """if Articles.objects.filter(article=article_art):
                messages.error(request, f'Article {article_art} already exists')
                return  HttpResponseRedirect(
                                            reverse('articlecreate'
                                            )
                                            )"""
            Articles.objects.create(article=article_art,item_name=article_name,item_price=article_kind)
            prov=Providers.objects.get(name_provider='-')
            if not Parts_full.objects.filter(partnumber_parts=article_art,providers=prov):
                if Parts_full.objects.filter(name_parts=article_name,providers=prov):
                    Parts_full.objects.filter(name_parts=article_name,providers=prov).delete()
                    messages.success(request, f'Parts_full old was deleted: {article_name}')
                Parts_full.objects.create(name_parts=article_name,partnumber_parts=article_art,providers=prov)
                messages.success(request, f'Parts_full {article_art} was created with name {article_name}')
            messages.success(request, f'Article {article_art} was created with name {article_name} kind {article_kind}')
            try:
                with open("load_form_providers/list_articles.json", "r") as write_file:
                    list_get_list2=json.load(write_file)
                list_get_list2[str(article_art)]=(str(article_kind),str(article_name))
                with open("load_form_providers/list_articles.json", "w") as write_file:
                    json.dump(list_get_list2, write_file)
            except:
                messages.error(request, f'Article {article_art} was not writed in a file with name {article_name} kind {article_kind}')

            return  HttpResponseRedirect(
                                        reverse('articlecreate'
                                        )
                                        )
        if formd.is_valid():
            parts = formd.cleaned_data['name_parts']
            if_search = Parts_short.objects.filter(name_parts__icontains=parts)
            context = {
                       'form': form,
                       'form2': form2,
                       'formd': formd,
                       'if_search': if_search
                      }
            return render(request, 'pars/article_created.html', context)
        return render(request, 'pars/article_created.html', context)

def parts_content_versum(l, obj):
    prov=Providers.objects.get(name_provider='-')
    temp1 = [l]
    for x in obj:
        temp=[]
        for v in l:
            if v not in ('price',):
                temp.append(x.__dict__[v])
            elif v == 'price':
                tt=Parts_full.objects.filter(partnumber_parts=x.part_number,providers=prov)
                if tt:
                    tt=tt.first()
                    tt_=tt.providerprice_parts
                    if tt_:
                        temp.append(tt_)
                    else:
                        temp.append(0)
                else:
                    temp.append(0)
        temp1.append(temp)
    return temp1

def send_sheet_parts(request):
    try:
        service, CREDENTIALS_FILE, spreadsheetId = Service()
    except:
        messages.error(request, 'not access to google sheet')
    list_versum_parts = [(CPU.objects.all(),['part_number', 'vendor', 'name', 'f_name', 'price', 'desc_ukr', 'desc_ru', 'cpu_c_t', 'f_cpu_c_t', 'cpu_b_f', 'cpu_cache', 'cpu_i_g_ua', 'cpu_i_g_rus', 'more', 'depend_from', 'depend_from_type'],'cpu_for_versum'),
    (Cooler.objects.all(),['part_number', 'vendor','name',  'price', 'desc_ukr', 'desc_ru', 'fan_type_ua', 'fan_type_rus', 'fan_spd_ua', 'fan_spd_rus', 'fan_noise_level', 'fan_size', 'more'],'cool_for_versum'),
    (MB.objects.all(),['part_number', 'vendor', 'main_category','name',  'price', 'desc_ukr', 'desc_ru', 'mb_chipset', 'mb_max_ram', 'more', 'depend_to', 'depend_to_type'],'mb_for_versum'),
    (RAM.objects.all(),['part_number', 'vendor','name',  'f_name', 'price', 'desc_ukr', 'desc_ru', 'mem_s', 'mem_spd', 'mem_l', 'more'],'mem_for_versum'),
    (HDD.objects.all(),['part_number', 'vendor','name','f_name', 'price', 'desc_ukr', 'desc_ru', 'hdd_s', 'hdd_spd_ua', 'hdd_spd_rus', 'hdd_ca', 'more'],'hdd_for_versum'),
    (SSD.objects.all(),['part_number', 'vendor','name', 'f_name', 'price', 'desc_ukr', 'desc_ru', 'ssd_s', 'ssd_spd', 'ssd_r_spd', 'ssd_type_cells', 'more'],'ssd_for_versum'),
    (GPU.objects.all(),['part_number', 'vendor', 'main_category','name', 'f_name', 'price', 'desc_ukr', 'desc_ru', 'gpu_fps', 'gpu_m_s', 'gpu_b', 'gpu_cpu_spd', 'gpu_mem_spd', 'more'],'video_for_versum'),
    (PSU.objects.all(),['part_number', 'vendor','name', 'price', 'desc_ukr', 'desc_ru', 'psu_p', 'psu_c', 'psu_f', 'more'],'psu_for_versum'),
    (FAN.objects.all(),['part_number', 'vendor','name', 'price', 'desc_ukr', 'desc_ru', 'case_fan_spd_ua', 'case_fan_spd_rus', 'case_fan_noise_level', 'case_fan_size', 'more'],'fan_for_versum'),
    (CASE.objects.all(),['part_number', 'vendor','name', 'price', 'desc_ukr', 'desc_ru', 'case_s', 'more'],'case_for_versum')
    ]
    for p in list_versum_parts:
        l1,l2 = p[2], 'A2:Z520'
        list_dict = parts_content_versum(p[1], p[0])
        """l11 = ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
        list_dict2 = [l11 for x in list_dict]
        results = service.spreadsheets().values().batchUpdate(spreadsheetId = spreadsheetId, body = {
        "valueInputOption": "USER_ENTERED",
        "data": [
        {"range": f"{l1}!{l2}",
        "majorDimension": "ROWS",
        "values":list_dict2}
        ]}).execute()"""
        service.spreadsheets().values().clear(spreadsheetId = spreadsheetId,range=l1).execute()
        time.sleep(1)
        results = service.spreadsheets().values().batchUpdate(spreadsheetId = spreadsheetId, body = {
        "valueInputOption": "USER_ENTERED",
        "data": [
        {"range": f"{l1}!{l2}",
        "majorDimension": "ROWS",
        "values":list_dict}
        ]}).execute()
    messages.success(request, 'Sended parts for versum')
    return  HttpResponseRedirect(
                                reverse('uploader',
                                kwargs={'w':'-'}
                                )
                                )

def content_versum(obj,atr):
    try:
        cc=obj.compprice
    except:
        print('In obj no  compprice')
        return []
    temp = []
    dict_v = {
    'proc_computers':CPU.objects.filter(name__iexact=obj.__dict__[atr]),
    'cool_computers':Cooler.objects.filter(name__iexact=obj.__dict__[atr]),
    'mb_computers':MB.objects.filter(name__iexact=obj.__dict__[atr]),
    'mem_computers':RAM.objects.filter(name__iexact=obj.__dict__[atr]),
    'video_computers':GPU.objects.filter(name__iexact=obj.__dict__[atr]),
    'ps_computers':PSU.objects.filter(name__iexact=obj.__dict__[atr]),
    'vent_computers':FAN.objects.filter(name__iexact=obj.__dict__[atr]),
    'case_computers':CASE.objects.filter(name__iexact=obj.__dict__[atr]),
            }
    if atr == 'hdd_computers':
        h=obj.__dict__['hdd_computers'].split(';')
        for x in h:
            if x.lower().find('ssd')!=-1:
                ssd=SSD.objects.filter(name=x)
                if ssd:
                    ssd=ssd.first()
                    for x in ssd.__dict__.keys():
                        if x not in ('_state','id'):
                            temp.append(ssd.__dict__[x])
                        elif x == 'price':
                            temp2 = ssd.__dict__[atr]
                            if temp2:
                                temp.append(temp2)
                            else:
                                temp.append(0)
            elif x.lower().find('3,5')!=-1 or x.lower().find('hdd')!=-1:
                hdd=HDD.objects.filter(name=x)
                if hdd:
                    hdd=hdd.first()
                    for x in hdd.__dict__.keys():
                        if x not in ('_state','id'):
                            temp.append(hdd.__dict__[x])
                        elif x == 'price':
                            temp2 = hdd.__dict__[atr]
                            if temp2:
                                temp.append(temp2)
                            else:
                                temp.append(0)
            elif x.lower().find('Не встановлено')!=-1:
                continue
    elif atr != 'hdd_computers' and dict_v[atr]:
        v = dict_v[atr].first()
        for x in v.__dict__.keys():
            if x not in ('_state','id','price'):
                temp.append(v.__dict__[x])
            elif x == 'price':
                temp2 = cc.__dict__[atr]
                if temp2:
                    temp.append(temp2)
                else:
                    temp.append(0)
    return temp

def content_for_google_sheet(obj,p):
    list_full = [[obj.name_computers,'','',obj.price_computers]]
    list_atr = ['mb_computers', 'proc_computers', 'mem_computers', 'video_computers',
    'hdd_computers', 'case_computers', 'ps_computers', 'cool_computers','vent_computers']
    if p == 'versum':
        for x in list_atr:
            if x != 'hdd_computers':
                list_full.append([x,obj.__dict__[x],1]+content_versum(obj,x))
            else:
                for y in obj.hdd_computers.split(';'):
                    list_full.append([x,y,1]+content_versum(obj,x))
        list_full.append([])
        return list_full
    else:
        list_atr+=['mon_computers','wifi_computers','km_computers']
        for x in list_atr:
            if x != 'hdd_computers':
                if obj.__dict__[x]:
                    list_full.append([x,obj.__dict__[x],1])
                elif x not in ('mon_computers','wifi_computers','km_computers') and not obj.__dict__[x]:
                    list_full.append([x,'',1])
            else:
                for y in obj.hdd_computers.split(';'):
                    list_full.append([x,y,1])
        list_full.append([])
        return list_full

def send_sheet(request,p):
    try:
        service, CREDENTIALS_FILE, spreadsheetId = Service()
    except:
        messages.error(request, 'not access to google sheet')
    list_full = []
    if p in ('versum','itblok'):
        for x in Computers.objects.filter(pc_assembly__sites__name_sites=p,is_active=True):
            list_full += content_for_google_sheet(x,p)
    #send_list(f'for_{p}',list_full,'A2:D12000',service)
    l = f'for_{p}'
    l2 = 'A2:Z12000'
    list_dict = list_full
    service.spreadsheets().values().clear(spreadsheetId = spreadsheetId,range=l).execute()
    time.sleep(3)
    results = service.spreadsheets().values().batchUpdate(spreadsheetId = spreadsheetId, body = {
    "valueInputOption": "USER_ENTERED",
    "data": [
    {"range": f"{l}!{l2}",
     "majorDimension": "ROWS",
     "values":list_dict}
         ]}).execute()
    messages.success(request, f'Sended comps for {p} site ok ')
    return  HttpResponseRedirect(
                                reverse('uploader',
                                kwargs={'w':'-'}
                                )
                                )
class versum_api(APIView):
    def get(self, request):
        Dict_full = {}
        cver = Computers.objects.filter(pc_assembly__sites__name_sites='versum',is_active=True)
        for x in cver:
            Dict_full[x.name_computers] = content_for_google_sheet(x,'versum')
        #serializer = CompsSerializer(cver, many=True)
        #return Response({"versum": serializer.data})
        return Response({"versum": Dict_full})

class itblok_api(APIView):
    def get(self, request):
        Dict_full = {}
        cit = Computers.objects.filter(pc_assembly__sites__name_sites='itblok',is_active=True)
        for x in cit:
            Dict_full[x.name_computers] = content_for_google_sheet(x,'itblok')
        #serializer = CompsSerializer(cver, many=True)
        #return Response({"versum": serializer.data})
        return Response({"itblok": Dict_full})

class versum_api_parts(APIView):
    def get(self, request):
        Dict_full = {}
        cool = Cooler.objects.filter(is_active=True)
        serializer = CoolerSerializer(cool, many=True)
        Dict_full['cooler'] = serializer.data
        cpu = CPU.objects.filter(is_active=True)
        serializer = CpuSerializer(cpu, many=True)
        Dict_full['cpu'] = serializer.data
        mb = MB.objects.filter(is_active=True)
        serializer = MbSerializer(mb, many=True)
        Dict_full['mb'] = serializer.data
        ram = RAM.objects.filter(is_active=True)
        serializer = RamSerializer(ram, many=True)
        Dict_full['ram'] = serializer.data
        hdd = HDD.objects.filter(is_active=True)
        serializer = HddSerializer(hdd, many=True)
        Dict_full['hdd'] = serializer.data
        psu = PSU.objects.filter(is_active=True)
        serializer = PsuSerializer(psu, many=True)
        Dict_full['psu'] = serializer.data
        gpu = GPU.objects.filter(is_active=True)
        serializer = GpuSerializer(gpu, many=True)
        Dict_full['gpu'] = serializer.data
        fan = FAN.objects.filter(is_active=True)
        serializer = FanSerializer(fan, many=True)
        Dict_full['fan'] = serializer.data
        case = CASE.objects.filter(is_active=True)
        serializer = CaseSerializer(case, many=True)
        Dict_full['case'] = serializer.data
        ssd = SSD.objects.filter(is_active=True)
        serializer = SsdSerializer(ssd, many=True)
        Dict_full['ssd'] = serializer.data
        return Response({"versum_parts": Dict_full})
