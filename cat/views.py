from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,HttpResponse
import itertools
import json,pickle,re
import os
import datetime,time
from django.utils import timezone
import random
#from scrapy import *
#from sheet_class import *
#from comp_class import IT_LOTS,pack_data
from .models import *
from django.db.models import Min
from django.views.generic import ListView
from django.core.paginator import Paginator
from django.db.models import Count
from .forms import *
from django.urls import reverse
from django.contrib import messages
from sereja.tasks import hello_world
from celery.schedules import crontab
from scrapy import get_video,get_cpu
from pars.views import need_comps
#from django.forms import modelformset_factory
#from django.views.generic.edit import CreateView, UpdateView
#
#hello_world.delay()
def comp_to_versum(obj):
    dict_={}
    cpu=CPU.objects.filter(name__iexact=obj.__dict__['proc_computers'])
    dict_['cpu']=(cpu.count(),cpu)
    mb=MB.objects.filter(name__iexact=obj.__dict__['mb_computers'])
    dict_['mb']=(mb.count(),mb)
    mem=RAM.objects.filter(name__iexact=obj.__dict__['mem_computers'])
    dict_['mem']=(mem.count(),mem)
    cool=Cooler.objects.filter(name__iexact=obj.__dict__['cool_computers'])
    if obj.__dict__['cool_computers'] in ('amd','intel'):
        dict_['cool']=(1,cool,'?')
    else:
        dict_['cool']=(cool.count(),cool)
    ps=PSU.objects.filter(name__iexact=obj.__dict__['ps_computers'])
    dict_['ps']=(ps.count(),ps)
    case=CASE.objects.filter(name__iexact=obj.__dict__['case_computers'])
    dict_['case']=(case.count(),case)
    vent=FAN.objects.filter(name__iexact=obj.__dict__['vent_computers'])
    dict_['vent']=(vent.count(),vent)
    video=GPU.objects.filter(name__iexact=obj.__dict__['video_computers'])
    dict_['video']=(video.count(),video)
    h=obj.__dict__['hdd_computers'].split(';')
    for x in h:
        if x.lower().find('ssd')!=-1:
            ssd=SSD.objects.filter(name__iexact=x)
            dict_['ssd']=(ssd.count(),ssd)
        elif x.lower().find('3,5')!=-1 or x.lower().find('hdd')!=-1:
            hdd=HDD.objects.filter(name__iexact=x)
            dict_['hdd']=(hdd.count(),hdd)
        elif x.lower().find('Не встановлено')!=-1:
            continue
    return dict_

def price(request):
    aa=Articles.objects.all().order_by('?')[:5]
    par = []
    for x in aa:
        p = Parts_full.objects.filter(providers__articles__article=x.article,
        partnumber_parts=x.article).order_by('providerprice_parts')
        if p.count():
            par.append(p)
    context = {
               'price': 'Main Price',
               'title': 'Main Price',
               'dict_code': aa,
               'par': par
              }
    #sh.__dict__['dc']
    #return HttpResponse('<h2>Hello</h2>')
    return render(request, 'cat/price.html', context)

def kind_price_item_all(request, pc_id, itm):
    itm_dict={
             100001:'proc_computers',100002:'mb_computers',100003:'mem_computers',100004:'video_computers',
             100005:'ps_computers',100006:'case_computers',100007:'cool_computers',1000010:'vent_computers',
             1000011:'mon_computers', 1000012:'wifi_computers', 1000013:'km_computers'
             }
    cc=Computers.objects.get(pk=pc_id)
    if itm in itm_dict:
        short = cc.__dict__[itm_dict[itm]]
        pp = Parts_short.objects.get(name_parts=short)
        kind_itm = pp.kind
        aa=Articles.objects.filter(item_price=kind_itm)
        for_assembly_0 = pp.name_parts
    elif itm == 100008:
        short = cc.__dict__['hdd_computers'].split(';')[0]
        pp = Parts_short.objects.get(name_parts=short)
        kind_itm = pp.kind
        aa=Articles.objects.filter(item_price=kind_itm)
        for_assembly_0 = pp.name_parts
    elif itm == 100009:
        try:
            short = cc.__dict__['hdd_computers'].split(';')[1]
        except:
            short = cc.__dict__['hdd_computers'].split(';')[0]
            messages.error(request, f"Maybe you only have one in {cc.__dict__['hdd_computers']}")
        pp = Parts_short.objects.get(name_parts=short)
        kind_itm = pp.kind
        aa=Articles.objects.filter(item_price=kind_itm)
        for_assembly_0 = pp.name_parts
    par = []
    for x in aa:
        p = Parts_full.objects.filter(partnumber_parts=x.article).distinct().order_by(
        'providers__name_provider')
        if p.count():
            par.append(p)
    form = PartsForm_code(initial={
    'procent': 1.19})
    #PartsForm = modelformset_factory(Parts_short, fields=('Advanced_parts', 'x_code'))
    #formset = PartsForm()
    paginator = Paginator(par, 40)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
               'price': pc_id,
               'price_id': kind_itm,
               'for_assembly': (for_assembly_0,Parts_short.objects.filter(kind=kind_itm).order_by('name_parts')),
               'itm': itm,
               'par': page_obj,
               'form': form
              }
    return render(request, 'cat/price.html', context)

def kind_price_item(request, pc_id, itm):
    #PartsForm = modelformset_factory(Parts_short, fields=('Advanced_parts', 'x_code'))
    dict_item={
             'aproc':100001, 'iproc':100001, 'imb':100002, 'amb':100002, 'mem':100003,
             'video':100004, 'ps':100005, 'case':100006,
             'cool':100007, 'hdd':100008, 'ssd':100009,
             'vent':1000010, 'mon':1000011,
             'wifi':1000012, 'km':1000013
             }
    kind2_dict = {'aproc':'proc_computers','iproc':'proc_computers','amb':'mb_computers',
                 'imb':'mb_computers','mem':'mem_computers','cool':'cool_computers','hdd':'hdd_computers',
                 'ssd':'hdd_computers','ps':'ps_computers','case':'case_computers','video':'video_computers',
                 'vent':'vent_computers','mon':'mon_computers', 'wifi':'wifi_computers', 'km':'km_computers'}
    itm_dict={
             100001:'proc_computers',100002:'mb_computers',100003:'mem_computers',100004:'video_computers',
             100005:'ps_computers',100006:'case_computers',100007:'cool_computers',1000010:'vent_computers',
             1000011:'mon_computers',1000012:'wifi_computers',1000013:'km_computers'
             }
    def Sub_hdd(obj,h,name):
        temp=[]
        if h=='ssd':
            for x in obj.split(';'):
                if x.lower().find('ssd')==-1:
                    temp.append(x)
                else:
                    temp.append(name)
        elif h=='hdd':
            for x in obj.split(';'):
                if x.lower().find('3,5')==-1 and x.lower().find('hdd')==-1:
                    temp.append(x)
                else:
                    temp.append(name)
        if len(temp)==1:
            return temp[0]
        elif len(temp)>1:
            return temp[0]+';'+temp[1]

    if request.method == 'GET':
        res = request.GET
        if 'search2' in res  or 'search' in res:
            if 'search2' in res:
                res = request.GET['search2']
                aa=Articles.objects.filter(article=res)
                delete = 1 if aa.count() == 1 else 0
            elif 'search' in res:
                res = request.GET['search']
                aa=Articles.objects.filter(item_name__icontains=res)
            if not aa:
                messages.success(request, f'This parts : {res} not exist in price')
                return  HttpResponseRedirect(
                                            reverse('assembly_item',
                                            kwargs={'pc_id':pc_id,
                                                    'itm':itm}
                                            )
                                            )
            par = []
            for x in aa:
                p = Parts_full.objects.filter(partnumber_parts=x.article).distinct().order_by(
                'providerprice_parts')
                if p.count():
                    pp = p.filter(providers__name_provider='-')
                    if pp.count() and pp.first().providerprice_parts:
                        par.append(p.order_by('providers__name_provider'))
                    else:
                        par.append(p)
            cc=Computers.objects.get(pk=pc_id)
            pp = Parts_short.objects.filter(name_parts=cc.__dict__[itm_dict[itm]])
            if pp:
                pp = pp[0]
                for_assembly_0 = pp.name_parts
                kind_itm = pp.kind
        #if itm.find('_computers') != -1  and pc_id:
        else:
            if itm in (100001,100002,100003,100004,100005,100006,100007,1000010,1000011,1000012,1000013):
                cc=Computers.objects.get(pk=pc_id)
                pp = Parts_short.objects.filter(name_parts=cc.__dict__[itm_dict[itm]])
                if pp:
                    pp = pp[0]
                    full = pp.parts_full.all()
                    if full:
                        if full.count()>1:
                            messages.error(request, f'{full} count:{full.count()}')
                        full = full.first()
                        messages.warning(request, f'{pp.name_parts} sticking with {full.name_parts}')
                    else:
                        messages.warning(request, f'{pp.name_parts} no sticking')
                    try:
                        aa=Articles.objects.filter(article__in=eval(pp.partnumber_list))
                    except:
                        aa=Articles.objects.filter(article__in=[])
                    for_assembly_0 = pp.name_parts
                    par = []
                    for x in aa:
                        p = Parts_full.objects.filter(partnumber_parts=x.article).distinct().order_by(
                        'providers__name_provider')
                        if p.count():
                            par.append(p)
            elif itm == 100008:
                cc=Computers.objects.get(pk=pc_id)
                pp = Parts_short.objects.filter(name_parts=(cc.hdd_computers).split(';')[0])
                if pp:
                    pp = pp[0]
                    full = pp.parts_full.all()
                    if full:
                        if full.count()>1:
                            messages.error(request, f'{full} count:{full.count()}')
                        full = full.first()
                        messages.warning(request, f'{pp.name_parts} sticking with {full.name_parts}')
                    else:
                        messages.warning(request, f'{pp.name_parts} no sticking')
                    try:
                        aa=Articles.objects.filter(article__in=eval(pp.partnumber_list))
                    except:
                        aa=Articles.objects.filter(article__in=[])
                    for_assembly_0 = pp.name_parts
                    par = []
                    for x in aa:
                        p = Parts_full.objects.filter(partnumber_parts=x.article).distinct().order_by(
                        'providers__name_provider')
                        if p.count():
                            par.append(p)
            elif itm == 100009:
                cc=Computers.objects.get(pk=pc_id)
                pp = Parts_short.objects.filter(name_parts=(cc.hdd_computers).split(';')[1])
                if pp:
                    pp = pp[0]
                    full = pp.parts_full.all()
                    if full:
                        if full.count()>1:
                            messages.error(request, f'{full} count:{full.count()}')
                        full = full.first()
                        messages.warning(request, f'{pp.name_parts} sticking with {full.name_parts}')
                    else:
                        messages.warning(request, f'{pp.name_parts} no sticking')
                    try:
                        aa=Articles.objects.filter(article__in=eval(pp.partnumber_list))
                    except:
                        aa=Articles.objects.filter(article__in=[])
                    for_assembly_0 = pp.name_parts
                """else:
                    cc=cc.name_computers
                    for x in it_basa.iloc:
                        if x['name']==cc:
                            comp_itm = x[itm.split('_')[0]]
                    if itm != 'hdd_computers' and itm != 'hdd_computers2':
                        aa=Articles.objects.filter(article__in=comp_itm.Partnumbers)
                        for_assembly_0 = comp_itm.Name
                    else:
                        aa=Articles.objects.filter(article__in=comp_itm[0].Partnumbers)
                        for_assembly_0 = comp_itm[0].Name"""
                par = []
                for x in aa:
                    p = Parts_full.objects.filter(partnumber_parts=x.article).distinct().order_by(
                    'providers__name_provider')
                    if p.count():
                        par.append(p)

            #elif itm.find('_computers') == -1:
            else:
                par = []
                #aa = eval(itm.partnumber_list)
                #short = Parts_short.objects.filter(name_parts=itm)
                short = Parts_short.objects.filter(pk=itm)
                if short:
                    if short.count()>1:
                        messages.error(request, f'{short.name_partsl} count:{short.count()}')
                    kind_itm = short[0].kind
                    #short = short[0]
                    #for_assembly_0 = itm
                    for_assembly_0 = short[0].name_parts
                    short = eval(short[0].partnumber_list)
                else:
                    short = []
                    for_assembly_0 = itm
                aa=Articles.objects.filter(article__in=short)
                for x in aa:
                    p = Parts_full.objects.filter(partnumber_parts=x.article).distinct().order_by(
                    'providers__name_provider')
                    if p.count():
                        par.append(p)
                itm = dict_item[kind_itm]
            short = Parts_short.objects.filter(name_parts=for_assembly_0)
            if short:
                short = short[0]
            kind_itm = short.kind
            if not kind_itm:
                messages.error(request, f'in {short.name_parts} not kind error')
                kind_itm = 'vent'
        form = PartsForm_code(initial={
        'procent': 1.19})
        #PartsForm = modelformset_factory(Parts_short, fields=('Advanced_parts', 'x_code'))
        #formset = PartsForm()
        paginator = Paginator(par, 40)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
                   'price': pc_id,
                   'price_id': kind_itm,
                   'for_assembly': (for_assembly_0,Parts_short.objects.filter(kind=kind_itm).order_by('name_parts')),
                   'itm': itm,
                   'par': page_obj,
                   'form': form
                  }
        return render(request, 'cat/price.html', context)
    if request.method == 'POST':
        if 'stick' in request.POST:
            param = request.POST['stick'].split(';')
            pp=Parts_full.objects.get(pk=param[2])
            pfull = Parts_full.objects.filter(partnumber_parts=pp.partnumber_parts,providers__name_provider='-')
            if pfull and pfull.count() == 1:
                pfull = pfull.first()
                pshort = Parts_short.objects.get(name_parts=param[1])
                pshort.parts_full.add(pfull)
                ex = pshort.parts_full.exclude(pk=pfull.pk)
                if ex:
                    for e in ex:
                        pshort.remove(e)
                pshort.x_code = pfull.providerprice_parts
                pshort.date_chg = timezone.now()
                pshort.save()
                comps = need_comps(pshort.name_parts)
                for c in comps:
                    cpr = c.compprice
                    itm_ = pshort.kind if pshort.kind[0] not in ('a','i') else pshort.kind[1:]
                    cpr.__dict__[f"{itm_}_computers"] = pfull.providerprice_parts
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
                    messages.success(request, f'Now {pshort.name_parts} sticking with {pfull.name_parts} in {c.name_computers}')
            else:
                messages.error(request, f'{pfull} error')
            return  HttpResponseRedirect(
                                        reverse('assembly',
                                        kwargs={'pc_id':param[0]}
                                        )
                                        )
            #return HttpResponse(f"{request.POST['stick']}")
        #if itm.find('_computers') != -1:
        if itm in (100001,100002,100003,100004,100005,100006,100007,1000010,1000011,1000012,1000013):
            cc=Computers.objects.get(pk=pc_id)
            short = Parts_short.objects.filter(name_parts=cc.__dict__[itm_dict[itm]])
            if short:
                short = short[0]
            else:
                return redirect('cat-home')
        elif itm == 100008:
            cc=Computers.objects.get(pk=pc_id)
            short = Parts_short.objects.filter(name_parts=(cc.hdd_computers).split(';')[0])
            if short:
                short = short[0]
            else:
                return redirect('cat-home')
        elif itm == 100009:
            cc=Computers.objects.get(pk=pc_id)
            short = Parts_short.objects.filter(name_parts=(cc.hdd_computers).split(';')[1])
            if short:
                short = short[0]
            else:
                return redirect('cat-home')
        #elif itm.find('_computers') == -1:
        else:
            #short = Parts_short.objects.filter(name_parts=itm)
            cc=Computers.objects.get(pk=pc_id)
            short = Parts_short.objects.filter(pk=itm)
            if short:
                short = short[0]
            else:
                return redirect('cat-home')
            if short.kind not in ('ssd','hdd'):
                cc.__dict__[kind2_dict[short.kind]] = short.name_parts
            else:
                cc.__dict__[kind2_dict[short.kind]] = Sub_hdd(cc.hdd_computers,short.kind,short.name_parts)

        form = PartsForm_code(request.POST)
        if form.is_valid():
            short.Advanced_parts = form.cleaned_data['procent']
            if short.kind =='video':
                cc.video_num_computers = form.cleaned_data['Advanced_parts']
            if short.kind =='mem':
                cc.mem_num_computers = form.cleaned_data['Advanced_parts']
            if short.kind =='vent':
                cc.vent_num_computers = form.cleaned_data['Advanced_parts']
            short.date_chg = timezone.now().strftime("%Y-%m-%d %H:%M")
            cc.save()
            short.save()
            #adv = form.cleaned_data['Advanced_parts']
            #x_code = form.cleaned_data['x_code']
            #messages.success(request, f'In {short.name_parts} has been somthing changed ')
            return  HttpResponseRedirect(
                                        reverse('assembly',
                                        kwargs={'pc_id':pc_id}
                                        )
                                        )
        else:
            messages.error(request, f'Error updating')
            return  HttpResponseRedirect(
                                        reverse('assembly_item',
                                        kwargs={'pc_id':pc_id,
                                        'itm': itm}
                                        )
                                        )

def test(request, itm, pc_id):
    #PartsForm = modelformset_factory(Parts_short, fields=('Advanced_parts', 'x_code'))
    if request.method == 'POST':
        short = Parts_short.objects.filter(name_parts=itm)
        if short:
            short = short[0]
            #formset = PartsForm(request.POST, instance=short)
            form = PartsForm(request.POST, instance=short)
            if form.is_valid():
                short.Advanced_parts = form.cleaned_data['Advanced_parts']
                short.x_code = form.cleaned_data['x_code']
                form.save()

    else:
        form = PartsForm()
        return render(request, 'cat/testform.html', {'form': form})

def kind_price(request, price_id):
    kind_dict = {'aproc':'Amd processors','iproc':'Intel processors','amb':'Amd motherboards',
                 'imb':'Intel motherboards','mem':'Memory','cool':'Coolers','hdd':'HDD',
                 'ssd':'SSD','ps':'Power Supplies','case':'Cases','wifi':'WIFI','mon':'Monitors',
                 'km':'Keyboards and Mouses','video':'Videocards'}
    if request.method == 'GET':
        #form = PfullForm()
        delete = 0
        res = request.GET
        if price_id and 'search' not in res and 'search2' not in res:
            aa=Articles.objects.filter(item_price=price_id)
            par = []
            for x in aa:
                p = Parts_full.objects.filter(partnumber_parts=x.article).distinct().order_by(
                'providerprice_parts')
                if p.count():
                    pp = p.filter(providers__name_provider='-')
                    if pp.count() and pp.first().providerprice_parts:
                        if not pp.first().url_parts:
                            q=pp.first()
                            q.url_parts = p.first().url_parts
                            q.save()
                        par.append(p.order_by('providers__name_provider'))
                    else:
                        par.append(p)
        else:
            if 'search2' in res:
                res = request.GET['search2']
                aa=Articles.objects.filter(article=res,item_price=price_id)
                delete = 1 if aa.count() == 1 else 0
            else:
                res = request.GET['search']
                aa=Articles.objects.filter(item_name__icontains=res,item_price=price_id)
            if not aa:
                messages.success(request, f'This parts : {res} not exist in price')
                return  HttpResponseRedirect(
                                            reverse('kind_price',
                                            kwargs={'price_id':price_id}
                                            )
                                            )
            par = []
            for x in aa:
                p = Parts_full.objects.filter(partnumber_parts=x.article).distinct().order_by(
                'providerprice_parts')
                if p.count():
                    pp = p.filter(providers__name_provider='-')
                    if pp.count() and pp.first().providerprice_parts:
                        par.append(p.order_by('providers__name_provider'))
                    else:
                        par.append(p)

        paginator = Paginator(par, 40)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
                   'price': kind_dict[price_id],
                   'price_id': price_id,
                   'for_assembly': None,
                   #'dict_code': aa,
                   'par': page_obj,
                   'delete':delete
                   #'form': form
                  }
    if request.method == 'POST':
        l=[]
        for x in request.POST:
            if x in ('dc', 'asbis', 'elko', 'mti', 'itlink', 'brain', 'edg', 'erc', '-'):
                l.append(x)
        #form = PfullForm()
        if price_id:
            aa=Articles.objects.filter(item_price=price_id)
            par = []
            for x in aa:
                if not l and 'no' in request.POST:
                    p = Parts_full.objects.filter(partnumber_parts=x.article).exclude(providerprice_parts=None).distinct().order_by(
                    'providerprice_parts')
                elif 'no' in request.POST and l:
                    p = Parts_full.objects.filter(partnumber_parts=x.article).filter(providers__name_provider__in=l).exclude(providerprice_parts=None).distinct().order_by(
                    'providerprice_parts')
                else:
                    p = Parts_full.objects.filter(partnumber_parts=x.article).filter(providers__name_provider__in=l).distinct().order_by(
                'providerprice_parts')
                if p.count():
                    pp = p.filter(providers__name_provider='-')
                    if pp.count() and pp.first().providerprice_parts:
                        par.append(p.order_by('providers__name_provider'))
                    else:
                        par.append(p)
        paginator = Paginator(par, 40)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
                   'price': kind_dict[price_id],
                   'price_id': price_id,
                   'for_assembly': None,
                   #'dict_code': aa,
                   'par': page_obj,
                   #'form': form
                  }
        #return HttpResponse(f"{l}")
    return render(request, 'cat/price.html', context)

def test_price(request, d):
    dict_v2 = {
    'proc':'CPU.objects.filter(part_number=p1.partnumber_parts)',
    'cool':'Cooler.objects.filter(part_number=p1.partnumber_parts)',
    'mb':'MB.objects.filter(part_number=p1.partnumber_parts)',
    'mem':'RAM.objects.filter(part_number=p1.partnumber_parts)',
    'hdd':'HDD.objects.filter(part_number=p1.partnumber_parts)',
    'ssd':'SSD.objects.filter(part_number=p1.partnumber_parts)',
    'video':'GPU.objects.filter(part_number=p1.partnumber_parts)',
    'ps':'PSU.objects.filter(part_number=p1.partnumber_parts)',
    'vent':'FAN.objects.filter(part_number=p1.partnumber_parts)',
    'case':'CASE.objects.filter(part_number=p1.partnumber_parts)',
            }
    if request.method == 'POST':
        if 'del' in request.POST:
            p1 = Parts_full.objects.get(pk=d)
            p2 = Parts_full.objects.filter(partnumber_parts=p1.partnumber_parts)
            a = Articles.objects.get(article=p1.partnumber_parts)
            a.delete()
            p2.delete()
            messages.success(request, f'Deleted parts : {p1.name_parts} is complite')
            return  HttpResponseRedirect(
                                        reverse('kind_price',
                                        kwargs={'price_id':a.item_price}
                                        )
                                        )
        form = PfullForm(request.POST)
        if form.is_valid():
            price = request.POST['price']
            price = re.sub(',' ,'.', price)
            prov = Providers.objects.get(name_provider='-')
            p1 = Parts_full.objects.get(pk=d)
            p2 = Parts_full.objects.filter(partnumber_parts=p1.partnumber_parts,providers__name_provider='-')
            a = Articles.objects.get(article=p1.partnumber_parts)
            date = timezone.now()
            if not p2.count():
                Parts_full.objects.create(providerprice_parts = price,name_parts = p1.name_parts,
                partnumber_parts = p1.partnumber_parts,providers=prov,date_chg = date)
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
                        messages.success(request, f'in {short_kind}: {d_short .name} was changed price: {price}')
                if p2.count()>1:
                    messages.error(request, f'{p1.name_parts} with {p1.partnumber_parts} > 1')
            #return HttpResponse(f'price:{price},id:{d}')
            if a.item_price:
                messages.success(request, f'Price in parts: {p1.name_parts} was changed: {price}')
                return  HttpResponseRedirect(
                                            reverse('kind_price',
                                            kwargs={'price_id':str(a.item_price)}
                                            )
                                            )
    messages.error(f'Error with price in {p1.name_parts}')
    return HttpResponse(f'price:{price},id:{d}')

def pc_assembly_page_advanced(request, page_id, price, grp):
    if request.method == 'GET':
        form = CompSearchForm()
        #list_temp = []
        p = Parts_short.objects.get(pk=int(page_id))
        """if p.kind == 'video':
            for x in Computers.objects.filter(pc_assembly__sites__name_sites=price):
                if get_video(x.video_computers) == get_video(p.name_parts):
                    list_temp.append(x.pk)
        if p.kind in ('aproc','iproc'):
            for x in Computers.objects.filter(pc_assembly__sites__name_sites=price):
                if get_cpu(x.proc_computers) == get_cpu(p.name_parts):
                    list_temp.append(x.pk)"""
        comps = need_comps(p.name_parts)
        if not grp:
            pc3 = comps.filter(pc_assembly__sites__name_sites=price)
            #pc3_ = pc3.filter(is_active=True)
            pc4 = pc3.filter(is_active=False)
        elif grp == 1:
            pc3,pc4 = [],[]
            messages.success(request, f'In comps will be group update, choose parts ')
        else:
            pc3,pc4 = [],[]
            short_new = Parts_short.objects.get(pk=grp)
            kind_ = short_new.kind
            #short_old = Parts_short.objects.get(pk=page_id)
            if kind_ and kind_[0] in ('a','i'):
                short_kind = kind_[1:]
            else:
                short_kind = kind_
            for pc in comps.filter(pc_assembly__sites__name_sites=price,is_active=True):
                pc.__dict__[f"{short_kind}_computers"] = short_new.name_parts
                pc.save()
                cpr = pc.compprice
                price_ = short_new.x_code
                cpr.__dict__[f"{short_kind}_computers"] = price_
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
                for m in comps.filter(pc_assembly__sites__name_sites=price,is_active=True):
                    messages.success(request, f'Comps: {m.name_computers} was changed: new parts{short_new.name_parts} old parts {p.name_parts}')

        Icpu = Parts_short.objects.filter(kind='iproc')
        Acpu = Parts_short.objects.filter(kind='aproc')
        Vid = Parts_short.objects.filter(kind='video')
        Imb = Parts_short.objects.filter(kind='imb')
        Amb = Parts_short.objects.filter(kind='amb')
        Mem = Parts_short.objects.filter(kind='mem')
        Ps = Parts_short.objects.filter(kind='ps')
        Case = Parts_short.objects.filter(kind='case')
        context = {
                   'price': price,
                   'page_id':page_id,
                   #'par': pc2,
                   #'form': form,
                   'act': pc3,
                   'reserve': pc4,
                   'Icpu':Icpu,
                   'Acpu':Acpu,
                   'Vid':Vid,
                   'Imb':Imb,
                   'Amb':Amb,
                   'Mem':Mem,
                   'Ps':Ps,
                   'Case':Case,
                   'grp':grp
                  }
        return render(request, 'cat/pc_assembly_page_advanced.html', context)
    if request.method == 'POST':
        dict_temp = {}
        for x in request.POST:
            if x != 'csrfmiddlewaretoken':
                cc = Computers.objects.get(pk=int(x))
                if cc.is_active:
                    cc.is_active = False
                    dict_temp[cc.name_computers]=cc.is_active
                    cc.save()
                else:
                    cc.is_active = True
                    dict_temp[cc.name_computers]=cc.is_active
                    cc.save()
        #return HttpResponse(f'Short id:{dict_temp},{price}')

    #return HttpResponse(f'Short id:{page_id},kind:{p.kind},{list_temp}')
    return  HttpResponseRedirect(
                                reverse('assembly_page',
                                kwargs={'page_id':price}
                                )
                                )

def pc_assembly_page(request, page_id):
    list_ver_templ=['speedster','silver','platinum','panzer','paladin','omega','nuker','msi',
    'mini','lich','level','legendary-nuker','king-lich','great-crusader','gold','gigabyte',
    'galaxy','epic-nuker','crusader','archlich','rainbow','ratchet','ultra-magnus',
    'metroplex','february']
    if request.method == 'GET':
        form = CompSearchForm()
        if page_id not in ('itblok','versum'):
            c1=Computers.objects.get(pk=int(page_id))
            c1.is_active = False if c1.is_active else True
            c1.save()
            messages.success(request, f'Status {c1.name_computers}  :Active = {c1.is_active} ')
            page_id = c1.pc_assembly.sites.name_sites
        if page_id == 'itblok':
            amd = Pc_assembly.objects.filter(name_assembly='amd',sites__name_sites='itblok')
            intel = Pc_assembly.objects.filter(name_assembly='intel',sites__name_sites='itblok')
            msi = Pc_assembly.objects.filter(name_assembly='msi',sites__name_sites='itblok')
            aorus = Pc_assembly.objects.filter(name_assembly='aorus',sites__name_sites='itblok')
            pc2 = list(itertools.zip_longest(amd,intel,msi,aorus))
            pc3 = Computers.objects.filter(pc_assembly__sites__name_sites=page_id)
        elif page_id == 'versum':
            amd = Pc_assembly.objects.filter(name_assembly__in=list_ver_templ,sites__name_sites='versum').annotate(
            c=Count('computers')).filter(c__gte=1)
            msi = Pc_assembly.objects.filter(kind_assembly='msi',sites__name_sites='versum').annotate(
            c=Count('computers')).filter(c__gte=1)
            """intel = Pc_assembly.objects.filter(kind_assembly='intel',sites__name_sites='versum').annotate(
            c=Count('computers')).filter(c__gte=1)
            msi = Pc_assembly.objects.filter(kind_assembly='msi',sites__name_sites='versum').annotate(
            c=Count('computers')).filter(c__gte=1)
            #pc = list(zip(amd,intel))
            pc2 = list(itertools.zip_longest(amd,intel,msi))"""
            pc2 = list(itertools.zip_longest(amd,msi))
            pc3 = Computers.objects.filter(pc_assembly__sites__name_sites=page_id)
        Icpu = Parts_short.objects.filter(kind='iproc')
        Acpu = Parts_short.objects.filter(kind='aproc')
        Vid = Parts_short.objects.filter(kind='video')
        Imb = Parts_short.objects.filter(kind='imb')
        Amb = Parts_short.objects.filter(kind='amb')
        Mem = Parts_short.objects.filter(kind='mem')
        Ps = Parts_short.objects.filter(kind='ps')
        Case = Parts_short.objects.filter(kind='case')
            #return HttpResponse(f'comp:{c1.name_computers}')
        """elif page_id == 'fury':
            pcassembly_fury=Pc_assembly.objects.filter(name_assembly='fury_all')
            pc2 = list(itertools.zip_longest(pcassembly_fury,))"""
        pc4 = pc3.filter(is_active=False)
        context = {
                   'price': page_id,
                   'par': pc2,
                   'form': form,
                   'act': pc3,
                   'reserve': pc4,
                   'Icpu':Icpu,
                   'Acpu':Acpu,
                   'Vid':Vid,
                   'Imb':Imb,
                   'Amb':Amb,
                   'Mem':Mem,
                   'Ps':Ps,
                   'Case':Case,
                   'grp':0
                  }
        return render(request, 'cat/pc_assembly_page.html', context)
    elif request.method == 'POST':
        form = CompSearchForm(request.POST)
        if form.is_valid():
            search = form.cleaned_data['name_computers']
            c=Computers.objects.filter(name_computers=search)
            if c.count() > 1:
                messages.warning(request, f'Warning: Comps > 1')
                return  HttpResponseRedirect(
                                            reverse('assembly_page',
                                            kwargs={'page_id':page_id}
                                            )
                                            )
            if c:
                """name_computer = c.first().name_computers
                name_assembly_ = c.first().pc_assembly.name_assembly
                name_site = c.first().pc_assembly.sites.name_sites
                pcassembly_=Pc_assembly.objects.filter(sites__name_sites=name_site).filter(name_assembly=name_assembly_).filter(computers__name_computers=name_computer)
                pc2 = list(itertools.zip_longest(pcassembly_,))"""
                return  HttpResponseRedirect(
                                            reverse('assembly',
                                            kwargs={'pc_id':c.first().pk}
                                            )
                                            )
            else:
                #messages.error(request, 'No such computer')
                if page_id == 'itblok':
                    act=Computers.objects.filter(name_computers__icontains=search,pc_assembly__sites__name_sites=page_id)
                else:
                    act=Computers.objects.filter(proc_computers__icontains=search,pc_assembly__sites__name_sites=page_id)
                    if not act:
                        messages.warning(request, 'Search per video')
                        act=Computers.objects.filter(video_computers__icontains=search,pc_assembly__sites__name_sites=page_id)
                if not act:
                    messages.error(request, 'No such computer')
                    return  HttpResponseRedirect(
                                                reverse('assembly_page',
                                                kwargs={'page_id':page_id}
                                                )
                                                )
                else:
                    context = {
                               'price': page_id,
                               #'par': pc2,
                               #'form': form,
                               'act': act,
                               'page_id':0,
                               'grp':0
                               #'reserve': pc4,
                               #'Icpu':Icpu,
                               #'Acpu':Acpu,
                               #'Vid':Vid
                              }
                    return render(request, 'cat/pc_assembly_page_advanced.html', context)
        else:
            messages.error(request, 'Empty form')
            return  HttpResponseRedirect(
                                        reverse('assembly_page',
                                        kwargs={'page_id':page_id}
                                        )
                                        )

        context = {
                   'price': page_id,
                   'par': pc2,
                   'form': form,
                   'act': pc3,
                   'reserve': pc4
                  }
        return render(request, 'cat/pc_assembly_page.html', context)



def home(request):
    context = {
               #'price': 'Home',
              }
    #hello_world.delay()
    return render(request, 'cat/home.html', context)

def pc_assembly(request, pc_id):

    def if_empty(n):
        list_assembly = ['','','mem','video','hdd','hdd','ps','case','cool','vent','mon','wifi','km']
        if n in (4,5):
            return Parts_short.objects.filter(kind__in=('hdd','ssd'))
        elif n == 0:
            return Parts_short.objects.filter(kind__in=('aproc','iproc'))
        elif n == 1:
            return Parts_short.objects.filter(kind__in=('amb','imb'))
        else:
            return Parts_short.objects.filter(kind=list_assembly[n])


    def Find(obj):
        """template=['hd graphics','amd hd','vega','amd radeon r5']
        for x in template:
            if obj.lower().find(x)!=-1:
                return ''"""
        return obj

    def fun1(x,xn, y, pc, m, u,upars,el_price,comp,multi=1):
        try:
            m = float(m)
        except:
            m = 1.19
        try:
            u = float(u)
        except:
            u = upars
        try:
            y = Find(y)
        except:
            messages.error(request, f'Error {xn}')
            y = ''
        short = Parts_short.objects.filter(name_parts=y)
        if short:
            short = short[0]
            if short.Advanced_parts:
                try:
                    short.Advanced_parts=float(short.Advanced_parts)
                    if short.Advanced_parts != m and short.Advanced_parts != 1:
                        m = short.Advanced_parts
                        #short.Advanced_parts = 1
                        #short.save()
                except:
                    short.Advanced_parts = 1
                    short.save()
            else:
                short.Advanced_parts = 1
                short.save()
            """if short.x_code:
                try:
                    short.x_code = float(short.x_code)
                except :
                    short.x_code = 0
                min_price_short = Parts_full.objects.filter(
                partnumber_parts__in=eval(short.partnumber_list)).aggregate(a=Min('providerprice_parts'))['a']
                if min_price_short:
                    try:
                        short.min_price = float(min_price_short)
                        short.save()
                    except :
                        short.min_price = 0
                        short.save()
                if short.x_code == short.min_price:
                    pc.append([x,xn,short,multi,short.x_code,
                    (short.x_code)*u*m*multi,(short.x_code)*m*multi,'',short.date_chg])
                else:
                    pc.append([x,xn,short,multi,short.x_code,
                    (short.x_code)*u*m*multi,(short.x_code)*m*multi,
                    short.min_price,short.date_chg])"""
            if el_price:
                try:
                    el_price = re.sub(',','.',el_price)
                    el_price = float(el_price)
                except :
                    el_price = 0
                if not short.x_code:
                    try:
                        main_price_short = Parts_full.objects.filter(
                            partnumber_parts__in=eval(short.partnumber_list),providers__name_provider='-')
                        main_price = main_price_short.aggregate(a=Min('providerprice_parts'))['a'] if main_price_short else 0
                    except:
                        main_price_short = Parts_full.objects.filter(
                            partnumber_parts__in=[],providers__name_provider='-')
                        main_price = main_price_short.aggregate(a=Min('providerprice_parts'))['a'] if main_price_short else 0
                else:
                    main_price = short.x_code
                if main_price:
                    try:
                        main_price = float(main_price)
                    except :
                        main_price = 0
                    if el_price == main_price:
                        pc.append([x,xn,short,multi,el_price,
                        (el_price)*u*m*multi,(el_price)*m*multi,'',short.date_chg])
                    else:
                        pc.append([x,xn,short,multi,el_price,
                        (el_price)*u*m*multi,(el_price)*m*multi,
                        main_price,short.date_chg])
                else:
                    pc.append([x,xn,short,multi,el_price,
                    (el_price)*u*m*multi,(el_price)*m*multi,0,0])
            else:
                if not short.x_code:
                    try:
                        main_price_short = Parts_full.objects.filter(
                           partnumber_parts__in=eval(short.partnumber_list),providers__name_provider='-')
                        main_price = main_price_short.aggregate(a=Min('providerprice_parts'))['a'] if main_price_short else 0
                    except:
                        main_price_short = Parts_full.objects.filter(
                           partnumber_parts__in=[],providers__name_provider='-')
                        main_price = main_price_short.aggregate(a=Min('providerprice_parts'))['a'] if main_price_short else 0
                else:
                    main_price = short.x_code
                if main_price:
                    try:
                        main_price = re.sub(',' ,'.', main_price)
                        main_price = float(main_price)
                    except :
                        main_price = 0
                    if short.kind2:
                        el_price = main_price
                        pc.append([x,xn,short,multi,el_price,
                        (el_price)*u*m*multi,(el_price)*m*multi,
                        main_price,short.date_chg])
                        cp = comp.compprice
                        if x != 100009:
                            cp.xn = el_price
                            cp.save()
                        else:
                            cp.hdd2_computers = el_price
                            cp.save()
                        procent = comp.class_computers if comp.class_computers else 1.19
                        try:
                            procent = float(procent)
                        except:
                            procent = 1.19
                        summa = 0
                        for k,v in cp.__dict__.items():
                            if k in ('vent_computers', 'proc_computers', 'mb_computers', 'mem_computers', 'video_computers', 'hdd_computers', 'hdd2_computers', 'ps_computers', 'case_computers', 'cool_computers', 'mon_computers', 'wifi_computers', 'km_computers'):
                                try:
                                    summa+=float(v)
                                except:
                                    summa+=0
                        summa = round(procent*summa)
                        cp.price_computers = summa
                        cp.save()
                    else:
                        pc.append([x,xn,short,multi,0,
                        0,0,main_price,short.date_chg])
                else:
                    pc.append([x,xn,short,multi,0,
                    0,0,0,0])
            """else:
                #short.computers.add(Computers.objects.get(pk=pc_id))
                min_price_short = Parts_full.objects.filter(
                partnumber_parts__in=eval(short.partnumber_list)).aggregate(a=Min('providerprice_parts'))['a']
                if min_price_short:
                    try:
                        short.x_code = float(min_price_short)
                        short.min_price = float(min_price_short)
                    except :
                        short.x_code = 0
                        short.min_price = 0
                        #short.Advanced_parts = 1
                    #short.Advanced_parts = 1
                    short.save()
                else:
                    short.x_code = 0
                    short.min_price = 0
                    #short.Advanced_parts = 1
                    short.save()
                pc.append([x,xn,short,multi,short.x_code,
                (short.x_code)*u*m*multi,(short.x_code)*m*multi])"""
        else:
            print((y,short))
            pc.append([x,xn,None,0,0,0,0])
        return pc

    if pc_id:
        try:
            usd = USD.objects.first().usd
            usd = round(float(usd),2)
        except:
            with open('load_form_providers/usd_ua.pickle', "rb") as f:
                    usd=pickle.load(f)
            usd = round(float(usd),2)
        itm_dict={
                 'proc_computers':100001,'mb_computers':100002,'mem_computers':100003,
                 'video_computers':100004,'ps_computers':100005,'case_computers':100006,
                 'cool_computers':100007,'hdd_computers':100008,'hdd_computers2':100009,
                 'vent_computers':1000010,'mon_computers':1000011,'wifi_computers':1000012,
                 'km_computers':1000013
                 }
        if request.method == 'GET':
            c = Computers.objects.get(pk=pc_id)
            try:
                cp=c.compprice
            except:
                cp = CompPrice.objects.create(name_computers=c.name_computers,computers=c)
            pc=[]
            for x,y in Computers.objects.get(pk=pc_id).__dict__.items():
                if x in ('proc_computers', 'mb_computers', 'mem_computers',
                         'video_computers', 'ps_computers',
                         'case_computers', 'cool_computers','vent_computers',
                         'mon_computers', 'wifi_computers', 'km_computers'
                         ):
                    if x=='mem_computers' and c.mem_num_computers and int(c.mem_num_computers) > 1:
                        multi_ = int(c.mem_num_computers)
                        pc = fun1(itm_dict[x],x,y,pc,m=c.class_computers,u=c.warranty_computers,upars=usd,el_price=cp.__dict__[x],comp=c,multi=multi_)
                    elif x=='video_computers' and c.video_num_computers and int(c.video_num_computers) > 1:
                        multi_ = int(c.video_num_computers)
                        pc = fun1(itm_dict[x],x,y,pc,m=c.class_computers,u=c.warranty_computers,upars=usd,el_price=cp.__dict__[x],comp=c,multi=multi_)
                    elif x=='vent_computers' and c.vent_num_computers and int(c.vent_num_computers) > 1:
                        multi_ = int(c.vent_num_computers)
                        pc = fun1(itm_dict[x],x,y,pc,m=c.class_computers,u=c.warranty_computers,upars=usd,el_price=cp.__dict__[x],comp=c,multi=multi_)
                    elif x in ('mon_computers', 'wifi_computers', 'km_computers') and y:
                        pc = fun1(itm_dict[x],x,y,pc,m=c.class_computers,u=c.warranty_computers,upars=usd,el_price=cp.__dict__[x],comp=c,multi=1)
                    else:
                        pc = fun1(itm_dict[x],x,y,pc,m=c.class_computers,u=c.warranty_computers,upars=usd,el_price=cp.__dict__[x],comp=c,multi=1)
                elif x == 'hdd_computers':
                    h = y.split(';')
                    if len(h)>1:
                        pc = fun1(itm_dict[x],x,h[0],pc,m=c.class_computers,u=c.warranty_computers,el_price=cp.__dict__['hdd_computers'],upars=usd,comp=c)
                        pc = fun1(100009,x,h[1],pc,m=c.class_computers,u=c.warranty_computers,el_price=cp.__dict__['hdd2_computers'],upars=usd,comp=c)
                        #pc.append(['hdd_computers',h[0]])
                        #pc.append(['hdd_computers2',h[1]])
                    else:
                        pc = fun1(itm_dict[x],x,h[0],pc,m=c.class_computers,u=c.warranty_computers,el_price=cp.__dict__['hdd_computers'],upars=usd,comp=c)
                        pc = fun1(100009,x,'',pc,m=c.class_computers,u=c.warranty_computers,el_price=cp.__dict__['hdd2_computers'],upars=usd,comp=c)
                        #pc.append(['hdd_computers',h[0]])
            t1,t2,t3=0,0,0
            for x in pc:
                t1+=x[4]
                t2+=x[5]
                t3+=x[6]
            try:
                cp_price_usd = float(cp.price_computers)
            except:
                cp_price_usd = 0
            pc2 = [t1,t2,t3,cp_price_usd]
            list_for_short = []
            syte = c.pc_assembly.sites.name_sites
            for e,x in enumerate(pc):
                if isinstance(x[2],Parts_short) and x[2].kind != '':
                    if x[2].kind in ('ssd','hdd'):
                        temp = Parts_short.objects.filter(kind__in=('ssd','hdd'))
                    else:
                        temp = Parts_short.objects.filter(kind=x[2].kind)
                elif c.__dict__[x[1]] in ('empty_iproc','empty_aproc','empty_imb','empty_amb'):
                    atr = c.__dict__[x[1]]
                    atr = re.sub('empty_','',atr)
                    temp = Parts_short.objects.filter(kind=atr)
                else:
                    temp = if_empty(e)
                if syte == 'itblok' and c.pc_assembly.name_assembly in ('amd','intel'):
                    if temp.first().kind in ('cool','vent','case'):
                        list_for_short.append((x,temp))
                    else:
                        list_for_short.append((x,temp.filter(kind2=True)))
                else:
                    list_for_short.append((x,temp))

            procent_ = Computers.objects.get(pk=pc_id).class_computers
            default = procent_ if procent_ else 1.19
            try:
                default = float(default)
            except:
                default = 1.19
            form = ComputersForm(initial={
            'class_computers': default,
            'warranty_computers': usd,
            })
            form2 = PfullForm()
            form2.id='2'
            context = {
                        'pc': pc_id,
                        'price': c.name_computers,
                        #'par': pc,
                        'par': list_for_short,
                        'par2': pc2,
                        'form': form,
                        'form2': form2,
                        'site_price': c,
                        #'short_for_falled_list': list_for_short
                       }
            return render(request, 'cat/pc_assembly.html', context)
        elif request.method == 'POST':
            c = Computers.objects.get(pk=pc_id)
            if "forall" in request.POST:
                forall = request.POST['forall']
                messages.success(request, f'default={forall} procent')
                Computers.objects.filter(pc_assembly__sites__name_sites=c.pc_assembly.sites.name_sites).update(class_computers=forall)
                return  HttpResponseRedirect(
                                            reverse('assembly',
                                            kwargs={'pc_id':pc_id}
                                            )
                                            )
            form = ComputersForm(request.POST, instance=c)
            if form.is_valid():
                c.class_computers = form.cleaned_data['class_computers']
                c.warranty_computers = form.cleaned_data['warranty_computers']
                form.save()
                #adv = form.cleaned_data['Advanced_parts']
                #x_code = form.cleaned_data['x_code']
                #messages.success(request, f'In {itm} has been somthing changed ')
                return  HttpResponseRedirect(
                                            reverse('assembly',
                                            kwargs={'pc_id':pc_id}
                                            )
                                            )
            else:
                messages.error(request, f'Error code')
                return  HttpResponseRedirect(
                                            reverse('assembly',
                                            kwargs={'pc_id':pc_id}
                                            )
                                            )

    #return render(request, 'cat/pc_assembly.html', context)

def test_assembly(request, short_id, id_, pc_id):
    itm_dict={
             100001:'proc_computers',100002:'mb_computers',100003:'mem_computers',100004:'video_computers',
             100005:'ps_computers',100006:'case_computers',100007:'cool_computers',
             100008:'hdd_computers',100009:'hdd2_computers',1000010:'vent_computers',
             1000011:'mon_computers', 1000012:'wifi_computers', 1000013:'km_computers'
             }
    kind_dict = {'aproc':'proc_computers','iproc':'proc_computers','amb':'mb_computers',
                 'imb':'mb_computers','mem':'mem_computers','cool':'cool_computers','hdd':'hdd_computers',
                 'ssd':'hdd_computers','ps':'ps_computers','case':'case_computers',
                 'vent':'vent_computers','video':'video_computers',
                 'mon': 'mon_computers', 'wifi': 'wifi_computers', 'km': 'km_computers'}
    if request.method == 'GET':
        if short_id == 1111111:
            c =  Computers.objects.get(pk=pc_id)
            dict_ = comp_to_versum(c)
            messages.warning(request,f'{dict_}')
            return  HttpResponseRedirect(
                                        reverse('assembly',
                                        kwargs={'pc_id': pc_id}
                                        )
                                        )
        c = Computers.objects.get(pk=pc_id)
        short = Parts_short.objects.get(pk=short_id)

        if short.kind not in ('hdd','ssd'):
            ind = kind_dict[short.kind]
            c.__dict__[ind] = short.name_parts
            c.save()
        else:
            if int(id_) == 100008:
                h = c.__dict__['hdd_computers']
                hh = h.split(';')
                hh[0] = short.name_parts
                h = ';'.join(hh)
                c.__dict__['hdd_computers'] = h
                c.save()
            elif int(id_) == 100009:
                h = c.__dict__['hdd_computers']
                hh = h.split(';')
                hh[1] = short.name_parts
                h = ';'.join(hh)
                c.__dict__['hdd_computers'] = h
                c.save()
        procent = c.class_computers if c.class_computers else 1.19
        try:
            procent = float(procent)
        except:
            procent = 1.19
        cpr = c.compprice
        if int(id_) != 100009:
            cpr.__dict__[f"{itm_dict[int(id_)]}"] = short.x_code
        else:
            cpr.__dict__["hdd2_computers"] = short.x_code
        cpr.save()
        summa = 0
        for x,y in cpr.__dict__.items():
            if x in ('vent_computers', 'proc_computers', 'mb_computers', 'mem_computers', 'video_computers', 'hdd_computers', 'hdd2_computers', 'ps_computers', 'case_computers', 'cool_computers','mon_computers', 'wifi_computers', 'km_computers'):
                try:
                    y = re.sub(',' ,'.', y)
                    summa+=float(y)
                except:
                    summa+=0
        summa = round(procent*summa)
        cpr.price_computers = summa
        cpr.save()
        return  HttpResponseRedirect(
                                    reverse('assembly',
                                    kwargs={'pc_id': pc_id}
                                    )
                                    )
    if request.method == 'POST':
        form = PfullForm(request.POST)
        if form.is_valid():
            price = request.POST['price']
            price = re.sub(',' ,'.', price)
            c =  Computers.objects.get(pk=pc_id)
            cc=c.compprice
            if id_ != 2222222:
                cc.__dict__[itm_dict[int(id_)]] = price
                short = Parts_short.objects.get(pk=short_id)
                short.date_chg = timezone.now()
                short.save()
                cc.save()
                messages.success(request, f'In CompPrice: {cc.name_computers} was changed: {itm_dict[int(id_)]} new price: {price}')
            else:
                cc.price_computers = price
                cc.save()
                messages.success(request, f'To CompPrice: {cc.name_computers} was changed new price: {price}')
            return  HttpResponseRedirect(
                                        reverse('assembly',
                                        kwargs={'pc_id': pc_id}
                                        )
                                        )
    #messages.error(f'Error with price in {p1.name_parts}')
    return HttpResponse(f'short_id:{short_id},pc_id:{pc_id}')

password = 'fdg45lk!'
"""class Views_pc_assembly_page(ListView):
    def get_context_data(self,**kwards):
        ctx = super(Views_pc_assembly_page,self).get_context_data(**kwards)
        page_id=self.kwargs['page_id']
        if page_id:
            ctx['page_id'] = page_id
            ctx['price'] = page_id
        else:
            ctx['page_id'] = 'itblok'
            ctx['price'] = 'itblok'
        return ctx
    #page_id='itblok'

    queryset = Pc_assembly.objects.filter(sites__name_sites=ctx['page_id'])
    template_name = 'cat/pc_assembly_page.html'
    context_object_name = 'par'"""

"""class Views_kind_price(ListView):
    model = Parts_full
    template_name = 'cat/price.html'
    context_object_name = 'par'
    paginate_by = 5

    def get_context_data(self,**kwards):
        ctx = super(Views_kind_price,self).get_context_data(**kwards)
        price_id=self.kwargs['price_id']
        kind_dict = {'aproc':'Amd processors','iproc':'Intel processors','amb':'Amd motherboards',
                     'imb':'Intel motherboards','mem':'Memory','cool':'Coolers','hdd':'HDD',
                     'ssd':'SSD','ps':'Power Supplies','case':'Cases','wifi':'WIFI','mon':'Monitors',
                     'km':'Keyboards and Mouses','video':'Videocards'}
        if price_id:
            aa=Articles.objects.filter(item_price=price_id)
            par = []
            for x in aa:
                p = Parts_full.objects.filter(providers__articles__item_price=price_id,
                partnumber_parts=x.article).distinct().order_by('providerprice_parts')
                if p.count():
                    par.append(p)
        ctx['price'] = kind_dict[price_id]
        ctx['par'] = par
        return ctx"""
"""
  <div class="dropdown-menu" aria-labelledby="dropdown05">
{% for p in for_assembly.1 %}
<a class="dropdown-item" href="{% url 'assembly_item' price p.pk %}">{{p.name_parts|truncatechars:40}}</a>
{% endfor %}
</div>
"""
def main_password(request):
    if request.method == 'GET':
        form = PasswordForm()
        context = {
                   'form': form
                  }
        return render(request, 'pars/main_password.html', context)
    elif request.method == 'POST':
        form = PasswordForm(request.POST)
        context = {
                   'form': form
                  }
        if form.is_valid():
            p = form.cleaned_data['name_parts']
            if p == password and random.randrange(0,3)==1:
                return  HttpResponseRedirect(
                                            reverse('cat-home'
                                            )
                                            )
            else:
                messages.error(request, 'Wrong password')
                return  HttpResponseRedirect(
                                            reverse('main_password'
                                            )
                                            )

def main_password2(request):
    if request.method == 'GET':
        form = PasswordForm()
        context = {
                   'form': form
                  }
        return render(request, 'pars/main_password.html', context)
    elif request.method == 'POST':
        form = PasswordForm(request.POST)
        context = {
                   'form': form
                  }
        if form.is_valid():
            p = form.cleaned_data['name_parts']
            if p == password:
                return  HttpResponseRedirect(
                                            reverse('uploader',
                                            kwargs={'w':'-'}
                                            )
                                            )
            else:
                messages.error(request, 'Wrong password')
                return  HttpResponseRedirect(
                                            reverse('main_password'
                                            )
                                            )

def computercreate(request, pc_ass):
    if request.method == 'GET':
        form = CompSearchForm()
        context = {
                   'form': form
                  }
        messages.warning(request,'First letter must be i or a (intel,amd)')
        return render(request, 'cat/computer_created.html', context)
    elif request.method == 'POST':
        form = CompSearchForm(request.POST)
        context = {
                   'form': form
                  }
        if form.is_valid():
            comp_name = form.cleaned_data['name_computers']
            l = comp_name[0]
            if l not in ('i','a'):
                messages.error(request,' Error, First letter must be i or a (intel,amd)')
            else:
                comp_name = comp_name[1:]
            assembly = Pc_assembly.objects.get(pk=pc_ass)
            c=Computers(name_computers=comp_name,url_computers='url',
            price_computers='1',proc_computers=f"empty_{l}proc",
            mb_computers=f"empty_{l}mb",mem_computers='empty_mem',
            video_computers='empty_video',hdd_computers='empty_hdd;empty_ssd',
            ps_computers='empty_ps',case_computers='empty_case',
            cool_computers='empty_cool',class_computers=' ',
            warranty_computers=' ', mon_computers=' ',wifi_computers=' ',km_computers=' ',
            vent_computers='empty',vent_num_computers=1,mem_num_computers=1,
            video_num_computers=1,pc_assembly=assembly)
            c.save()
            cp = CompPrice.objects.create(name_computers=c.name_computers,price_computers='1',computers=c)
            pc_id = c.id
            messages.success(request, f'Computer was created with name {comp_name} ')
            return  HttpResponseRedirect(
                                        reverse('assembly',
                                        kwargs={'pc_id':pc_id}
                                        )
                                        )

def forversum_adv_add(request,a,n,k):
    if not Articles.objects.filter(article=a):
        Articles.objects.create(article=a,item_name=n,item_price=k)
        messages.success(request, f'Article {a} was created with name {n} kind {k}')
    prov=Providers.objects.get(name_provider='-')
    if not Parts_full.objects.filter(partnumber_parts=a,providers=prov):
        Parts_full.objects.create(name_parts=n,partnumber_parts=a,providers=prov)
        messages.success(request, f'Parts_full {a} was created with name {n}')

def forversum(request,i,id):
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
    '-':CPU.objects.all()}

    dict_v3 = {
    'cpu':'CPU.objects.get(pk=id)',
    'cooler':'Cooler.objects.get(pk=id)',
    'mb':'MB.objects.get(pk=id)',
    'ram':'RAM.objects.get(pk=id)',
    'hdd':'HDD.objects.get(pk=id)',
    'ssd':'SSD.objects.get(pk=id)',
    'gpu':'GPU.objects.get(pk=id)',
    'psu':'PSU.objects.get(pk=id)',
    'fan':'FAN.objects.get(pk=id)',
    'case':'CASE.objects.get(pk=id)',
            }

    dict_form = {
    'cpu':"CpuForm(initial={'name':n.name, 'part_number':n.part_number,                'vendor':n.vendor,'price':n.price,'desc_ukr':n.desc_ukr,'desc_ru':n.desc_ru,                'f_name':n.f_name,'more':n.more,'cpu_c_t':n.cpu_c_t,'f_cpu_c_t':n.f_cpu_c_t,                'cpu_b_f':n.cpu_b_f,'cpu_cache':n.cpu_cache,'cpu_i_g_ua':n.cpu_i_g_ua,      'cpu_i_g_rus':n.cpu_i_g_rus,'depend_from':n.depend_from,                'depend_from_type':n.depend_from_type})",
    'cooler':"CoolForm(initial={'name':n.name, 'part_number':n.part_number,                'vendor':n.vendor,'price':n.price,'desc_ukr':n.desc_ukr,'desc_ru':n.desc_ru,                'fan_type_ua':n.fan_type_ua,'fan_type_rus':n.fan_type_rus,                'fan_spd_ua':n.fan_spd_ua,'fan_spd_rus':n.fan_spd_rus,'fan_noise_level':n.fan_noise_level,                'fan_size':n.fan_size,'more':n.more})",
    'mb':"MbForm(initial={'name':n.name, 'part_number':n.part_number,                'vendor':n.vendor,'price':n.price,'desc_ukr':n.desc_ukr,'desc_ru':n.desc_ru,                'main_category':n.main_category,'more':n.more,'mb_chipset':n.mb_chipset,                'mb_max_ram':n.mb_max_ram,'depend_to':n.depend_to,'depend_to_type':n.depend_to_type})",
    'ram':"RamForm(initial={'name':n.name, 'part_number':n.part_number,                'vendor':n.vendor,'price':n.price,'desc_ukr':n.desc_ukr,'desc_ru':n.desc_ru,                'f_name':n.f_name,'more':n.more,'mem_s':n.mem_s,'mem_spd':n.mem_spd,'mem_l':n.mem_l})",
    'hdd':"HddForm(initial={'name':n.name, 'part_number':n.part_number,                'vendor':n.vendor,'price':n.price,'desc_ukr':n.desc_ukr,'desc_ru':n.desc_ru,                'f_name':n.f_name,'more':n.more,'hdd_s':n.hdd_s,'hdd_spd_ua':n.hdd_spd_ua,                'hdd_spd_rus':n.hdd_spd_rus,'hdd_ca':n.hdd_ca})",
    'psu':"PsuForm(initial={'name':n.name, 'part_number':n.part_number,                'vendor':n.vendor,'price':n.price,'desc_ukr':n.desc_ukr,'desc_ru':n.desc_ru,                'psu_p':n.psu_p,'more':n.more,'psu_c':n.psu_c,'psu_f':n.psu_f})",                'gpu':"GpuForm(initial={'name':n.name, 'part_number':n.part_number,                'vendor':n.vendor,'price':n.price,'desc_ukr':n.desc_ukr,'desc_ru':n.desc_ru,                'f_name':n.f_name,'more':n.more,'main_category':n.main_category,                'gpu_fps':n.gpu_fps,'gpu_m_s':n.gpu_m_s,'gpu_b':n.gpu_b,'gpu_cpu_spd':n.gpu_cpu_spd,                'gpu_mem_spd':n.gpu_mem_spd})",
    'fan':"FanForm(initial={'name':n.name, 'part_number':n.part_number,                'vendor':n.vendor,'price':n.price,'desc_ukr':n.desc_ukr,'desc_ru':n.desc_ru,                'case_fan_spd_ua':n.case_fan_spd_ua,'case_fan_spd_rus':n.case_fan_spd_rus,                'case_fan_noise_level':n.case_fan_noise_level,                'case_fan_size':n.case_fan_size,'more':n.more})",
    'case':"CaseForm(initial={'name':n.name, 'part_number':n.part_number,                'vendor':n.vendor,'price':n.price,'desc_ukr':n.desc_ukr,'desc_ru':n.desc_ru,                'case_s':n.case_s,'more':n.more})",
    'ssd':"SsdForm(initial={'name':n.name, 'part_number':n.part_number,                'vendor':n.vendor,'price':n.price,'desc_ukr':n.desc_ukr,'desc_ru':n.desc_ru,                'f_name':n.f_name,'more':n.more,'ssd_s':n.ssd_s,'ssd_spd':n.ssd_spd,                'ssd_r_spd':n.ssd_r_spd,'ssd_type_cells':n.ssd_type_cells})"
                }
    form_no_initial ={
    'cpu':CpuForm(),
    'cooler':CoolForm(),
    'mb':MbForm(),
    'ram':RamForm(),
    'hdd':HddForm(),
    'ssd':SsdForm(),
    'gpu':GpuForm(),
    'psu':PsuForm(),
    'fan':FanForm(),
    'case':CaseForm(),
    '-':CpuForm()
                     }
    if request.method == 'GET':
        if 'name' in request.GET:
            dict_v = {
            'cpu':CPU.objects.filter(name__iexact=request.GET["name"]),
            'cooler':Cooler.objects.filter(name__iexact=request.GET["name"]),
            'mb':MB.objects.filter(name__iexact=request.GET["name"]),
            'ram':RAM.objects.filter(name__iexact=request.GET["name"]),
            'hdd':HDD.objects.filter(name__iexact=request.GET["name"]),
            'ssd':SSD.objects.filter(name__iexact=request.GET["name"]),
            'gpu':GPU.objects.filter(name__iexact=request.GET["name"]),
            'psu':PSU.objects.filter(name__iexact=request.GET["name"]),
            'fan':FAN.objects.filter(name__iexact=request.GET["name"]),
            'case':CASE.objects.filter(name__iexact=request.GET["name"]),
                    }
            #n = CASE.objects.filter(name=request.GET["name"])
            n = dict_v[i]
            if n:
                n = n.first()
                form = eval(dict_form[i])
                context = {
                           'i':i,
                           'n':n,
                           'i2':dict_base[i],
                           'form':form
                          }
                return render(request, 'cat/forversum.html', context)
            else:
                context = {
                           'i':i,
                           'i2':dict_base[i],
                           'form':form_no_initial[i]
                          }
                messages.warning(request, f"{request.GET['name']} is not exist")
                return render(request, 'cat/forversum.html', context)
        if 'part_number' in request.GET:
            dict_v2 = {
            'cpu':CPU.objects.filter(part_number=request.GET["part_number"]),
            'cooler':Cooler.objects.filter(part_number=request.GET["part_number"]),
            'mb':MB.objects.filter(part_number=request.GET["part_number"]),
            'ram':RAM.objects.filter(part_number=request.GET["part_number"]),
            'hdd':HDD.objects.filter(part_number=request.GET["part_number"]),
            'ssd':SSD.objects.filter(part_number=request.GET["part_number"]),
            'gpu':GPU.objects.filter(part_number=request.GET["part_number"]),
            'psu':PSU.objects.filter(part_number=request.GET["part_number"]),
            'fan':FAN.objects.filter(part_number=request.GET["part_number"]),
            'case':CASE.objects.filter(part_number=request.GET["part_number"]),
                    }
            n = dict_v2[i]
            if n:
                n = n.first()
                form = eval(dict_form[i])
                context = {
                           'i':i,
                           'n':n,
                           'i2':dict_base[i],
                           'form':form
                          }
                return render(request, 'cat/forversum.html', context)
            else:
                context = {
                           'i':i,
                           'i2':dict_base[i],
                           'form':form_no_initial[i]
                          }
                messages.warning(request, f"{request.GET['part_number']} is not exist")
                return render(request, 'cat/forversum.html', context)
        if id == 0:
            context = {
                   'i':i,
                   'i2':dict_base[i],
                   'form':form_no_initial[i]
                  }
        else:
            n = eval(dict_v3[i])
            form = eval(dict_form[i])
            context = {
                       'i':i,
                       'n':n,
                       'i2':dict_base[i],
                       'form':form
                      }
        return render(request, 'cat/forversum.html', context)
    if request.method == 'POST' and id != 0:
        if 'delete' in request.POST.keys():
            res = eval(dict_v3[i])
            res.delete()
            messages.success(request, f"Deleted {res.name} ")
        if 'reserve' in request.POST.keys():
            res = eval(dict_v3[i])
            res.is_active = False
            res.save()
            #return HttpResponse(f':{i},:{res.part_number}')
            messages.success(request, f"Reserved {res.name} ")
        if 'active' in request.POST.keys():
            res = eval(dict_v3[i])
            res.is_active = True
            res.save()
            #return HttpResponse(f':{i},:{res.part_number}')
            messages.success(request, f"Activated {res.name} ")
        return  HttpResponseRedirect(
                                    reverse('forversum',
                                    kwargs={'i':i,'id':0}
                                    )
                                    )
        #reserve = request.POST.keys()
        return HttpResponse(f':{i},:{reserve}')
    if request.method == 'POST' and i=='case':
        form = CaseForm(request.POST)
        if form.is_valid():
            name_obj = form.cleaned_data['name']
            c = CASE.objects.filter(name__iexact=name_obj)
            if not c:
                CASE.objects.create(name=name_obj, part_number=form.cleaned_data['part_number'],
                vendor=form.cleaned_data['vendor'],price=form.cleaned_data['price'],
                desc_ukr=form.cleaned_data['desc_ukr'],desc_ru=form.cleaned_data['desc_ru'],
                case_s=form.cleaned_data['case_s'],more=form.cleaned_data['more'],is_active = True)
                messages.success(request, f"{name_obj} is created")
            else:
                c = CASE.objects.get(name__iexact=name_obj)
                c.part_number=form.cleaned_data['part_number']
                c.vendor=form.cleaned_data['vendor']
                c.price=form.cleaned_data['price']
                c.desc_ukr=form.cleaned_data['desc_ukr']
                c.desc_ru=form.cleaned_data['desc_ru']
                c.case_s=form.cleaned_data['case_s']
                c.more=form.cleaned_data['more']
                c.save()
                messages.success(request, f"{name_obj} is update")
            return  HttpResponseRedirect(
                                        reverse('forversum',
                                        kwargs={'i':i,'id':0}
                                        )
                                        )
        return  HttpResponseRedirect(
                                    reverse('forversum',
                                    kwargs={'i':i,'id':0}
                                    )
                                    )
    if request.method == 'POST' and i=='cpu':
        form = CpuForm(request.POST)
        if form.is_valid():
            name_obj = request.POST['name']
            c = CPU.objects.filter(name__iexact=name_obj)
            if not c:
                CPU.objects.create(name=name_obj, part_number=form.cleaned_data['part_number'],
                vendor=form.cleaned_data['vendor'],price=form.cleaned_data['price'],
                desc_ukr=form.cleaned_data['desc_ukr'],desc_ru=form.cleaned_data['desc_ru'],
                f_name=form.cleaned_data['f_name'],cpu_c_t=form.cleaned_data['cpu_c_t'],
                f_cpu_c_t=form.cleaned_data['f_cpu_c_t'],cpu_b_f=form.cleaned_data['cpu_b_f'],
                cpu_cache=form.cleaned_data['cpu_cache'],cpu_i_g_ua=form.cleaned_data['cpu_i_g_ua'],
                cpu_i_g_rus=form.cleaned_data['cpu_i_g_rus'],more=form.cleaned_data['more'],
                depend_from=form.cleaned_data['depend_from'],depend_from_type=form.cleaned_data['depend_from_type'],is_active = True)
                messages.success(request, f"{name_obj} is created")
            else:
                c = CPU.objects.get(name__iexact=name_obj)
                c.part_number=form.cleaned_data['part_number']
                c.vendor=form.cleaned_data['vendor']
                c.price=form.cleaned_data['price']
                c.desc_ukr=form.cleaned_data['desc_ukr']
                c.desc_ru=form.cleaned_data['desc_ru']
                c.f_name=form.cleaned_data['f_name']
                c.cpu_c_t=form.cleaned_data['cpu_c_t']
                c.f_cpu_c_t=form.cleaned_data['f_cpu_c_t']
                c.cpu_b_f=form.cleaned_data['cpu_b_f']
                c.cpu_cache=form.cleaned_data['cpu_cache']
                c.cpu_i_g_ua=form.cleaned_data['cpu_i_g_ua']
                c.cpu_i_g_rus=form.cleaned_data['cpu_i_g_rus']
                c.depend_from=form.cleaned_data['depend_from']
                c.depend_from_type=form.cleaned_data['depend_from_type']
                c.more=form.cleaned_data['more']
                c.save()
                messages.success(request, f"{name_obj} is update")
            return  HttpResponseRedirect(
                                        reverse('forversum',
                                        kwargs={'i':i,'id':0}
                                        )
                                        )
        return  HttpResponseRedirect(
                                    reverse('forversum',
                                    kwargs={'i':i,'id':0}
                                    )
                                    )
    if request.method == 'POST' and i=='cooler':
        form = CpuForm(request.POST)
        if form.is_valid():
            name_obj = request.POST['name']
            c = Cooler.objects.filter(name__iexact=name_obj)
            if not c:
                CPU.objects.create(name=name_obj, part_number=form.cleaned_data['part_number'],
                vendor=form.cleaned_data['vendor'],price=form.cleaned_data['price'],
                desc_ukr=form.cleaned_data['desc_ukr'],desc_ru=form.cleaned_data['desc_ru'],
                fan_type_ua=form.cleaned_data['fan_type_ua'],fan_type_rus=form.cleaned_data['fan_type_rus'],
                fan_spd_ua=form.cleaned_data['fan_spd_ua'],fan_spd_rus=form.cleaned_data['fan_spd_rus'],
                fan_noise_level=form.cleaned_data['fan_noise_level'],fan_size=form.cleaned_data['fan_size'],
                more=form.cleaned_data['more'],is_active = True)
                messages.success(request, f"{name_obj} is created")
            else:
                c = Cooler.objects.get(name__iexact=name_obj)
                c.part_number=form.cleaned_data['part_number']
                c.vendor=form.cleaned_data['vendor']
                c.price=form.cleaned_data['price']
                c.desc_ukr=form.cleaned_data['desc_ukr']
                c.desc_ru=form.cleaned_data['desc_ru']
                c.fan_type_ua=form.cleaned_data['fan_type_ua']
                c.fan_type_rus=form.cleaned_data['fan_type_rus']
                c.fan_spd_ua=form.cleaned_data['fan_spd_ua']
                c.fan_spd_rus=form.cleaned_data['fan_spd_rus']
                c.fan_noise_level=form.cleaned_data['fan_noise_level']
                c.fan_size=form.cleaned_data['fan_size']
                c.more=form.cleaned_data['more']
                c.save()
                messages.success(request, f"{name_obj} is update")
            return  HttpResponseRedirect(
                                        reverse('forversum',
                                        kwargs={'i':i,'id':0}
                                        )
                                        )
        return  HttpResponseRedirect(
                                    reverse('forversum',
                                    kwargs={'i':i,'id':0}
                                    )
                                    )
    if request.method == 'POST' and i=='mb':
        form = MbForm(request.POST)
        if form.is_valid():
            name_obj = request.POST['name']
            c = MB.objects.filter(name__iexact=name_obj)
            if not c:
                MB.objects.create(name=name_obj, part_number=form.cleaned_data['part_number'],
                vendor=form.cleaned_data['vendor'],price=form.cleaned_data['price'],
                desc_ukr=form.cleaned_data['desc_ukr'],desc_ru=form.cleaned_data['desc_ru'],
                main_category=form.cleaned_data['main_category'],mb_chipset=form.cleaned_data['mb_chipset'],
                mb_max_ram=form.cleaned_data['mb_max_ram'],depend_to=form.cleaned_data['depend_to'],
                depend_to_type=form.cleaned_data['depend_to_type'],more=form.cleaned_data['more'],is_active = True)
                messages.success(request, f"{name_obj} is created")
            else:
                c = MB.objects.get(name__iexact=name_obj)
                c.part_number=form.cleaned_data['part_number']
                c.vendor=form.cleaned_data['vendor']
                c.price=form.cleaned_data['price']
                c.desc_ukr=form.cleaned_data['desc_ukr']
                c.desc_ru=form.cleaned_data['desc_ru']
                c.main_category=form.cleaned_data['main_category']
                c.mb_chipset=form.cleaned_data['mb_chipset']
                c.mb_max_ram=form.cleaned_data['mb_max_ram']
                c.depend_to=form.cleaned_data['depend_to']
                c.depend_to_type=form.cleaned_data['depend_to_type']
                c.more=form.cleaned_data['more']
                c.save()
                messages.success(request, f"{name_obj} is update")
            return  HttpResponseRedirect(
                                        reverse('forversum',
                                        kwargs={'i':i,'id':0}
                                        )
                                        )
        return  HttpResponseRedirect(
                                    reverse('forversum',
                                    kwargs={'i':i,'id':0}
                                    )
                                    )
    if request.method == 'POST' and i=='ram':
        form = RamForm(request.POST)
        if form.is_valid():
            name_obj = request.POST['name']
            c = RAM.objects.filter(name__iexact=name_obj)
            if not c:
                RAM.objects.create(name=name_obj, part_number=form.cleaned_data['part_number'],
                vendor=form.cleaned_data['vendor'],price=form.cleaned_data['price'],
                desc_ukr=form.cleaned_data['desc_ukr'],desc_ru=form.cleaned_data['desc_ru'],
                f_name=form.cleaned_data['f_name'],mem_s=form.cleaned_data['mem_s'],
                mem_spd=form.cleaned_data['mem_spd'],mem_l=form.cleaned_data['mem_l'],
                more=form.cleaned_data['more'],is_active = True)
                messages.success(request, f"{name_obj} is created")
            else:
                c = RAM.objects.get(name__iexact=name_obj)
                c.part_number=form.cleaned_data['part_number']
                c.vendor=form.cleaned_data['vendor']
                c.price=form.cleaned_data['price']
                c.desc_ukr=form.cleaned_data['desc_ukr']
                c.desc_ru=form.cleaned_data['desc_ru']
                c.f_name=form.cleaned_data['f_name']
                c.mem_s=form.cleaned_data['mem_s']
                c.mem_spd=form.cleaned_data['mem_spd']
                c.mem_l=form.cleaned_data['mem_l']
                c.more=form.cleaned_data['more']
                c.save()
                messages.success(request, f"{name_obj} is update")
            return  HttpResponseRedirect(
                                        reverse('forversum',
                                        kwargs={'i':i,'id':0}
                                        )
                                        )
        return  HttpResponseRedirect(
                                    reverse('forversum',
                                    kwargs={'i':i,'id':0}
                                    )
                                    )
    if request.method == 'POST' and i=='hdd':
        form = HddForm(request.POST)
        if form.is_valid():
            name_obj = request.POST['name']
            c = HDD.objects.filter(name__iexact=name_obj)
            if not c:
                HDD.objects.create(name=name_obj,part_number=form.cleaned_data['part_number'],
                vendor=form.cleaned_data['vendor'],price=form.cleaned_data['price'],
                desc_ukr=form.cleaned_data['desc_ukr'],desc_ru=form.cleaned_data['desc_ru'],
                f_name=form.cleaned_data['f_name'],hdd_s=form.cleaned_data['hdd_s'],
                hdd_spd_ua=form.cleaned_data['hdd_spd_ua'],hdd_spd_rus=form.cleaned_data['hdd_spd_rus'],
                more=form.cleaned_data['more'],hdd_ca=form.cleaned_data['hdd_ca'],is_active = True)
                messages.success(request, f"{name_obj} is created")
            else:
                c = HDD.objects.get(name__iexact=name_obj)
                c.part_number=form.cleaned_data['part_number']
                c.vendor=form.cleaned_data['vendor']
                c.price=form.cleaned_data['price']
                c.desc_ukr=form.cleaned_data['desc_ukr']
                c.desc_ru=form.cleaned_data['desc_ru']
                c.f_name=form.cleaned_data['f_name']
                c.hdd_s=form.cleaned_data['hdd_s']
                c.hdd_spd_ua=form.cleaned_data['hdd_spd_ua']
                c.hdd_spd_rus=form.cleaned_data['hdd_spd_rus']
                c.hdd_ca=form.cleaned_data['hdd_ca']
                c.more=form.cleaned_data['more']
                c.save()
                messages.success(request, f"{name_obj} is update")
            return  HttpResponseRedirect(
                                        reverse('forversum',
                                        kwargs={'i':i,'id':0}
                                        )
                                        )
        return  HttpResponseRedirect(
                                    reverse('forversum',
                                    kwargs={'i':i,'id':0}
                                    )
                                    )
    if request.method == 'POST' and i=='psu':
        form = PsuForm(request.POST)
        if form.is_valid():
            name_obj = request.POST['name']
            c = PSU.objects.filter(name__iexact=name_obj)
            if not c:
                PSU.objects.create(name=name_obj, part_number=form.cleaned_data['part_number'],
                vendor=form.cleaned_data['vendor'],price=form.cleaned_data['price'],
                desc_ukr=form.cleaned_data['desc_ukr'],desc_ru=form.cleaned_data['desc_ru'],
                psu_p=form.cleaned_data['psu_p'],psu_c=form.cleaned_data['psu_c'],
                psu_f=form.cleaned_data['psu_f'],
                more=form.cleaned_data['more'],is_active = True)
                messages.success(request, f"{name_obj} is created")
            else:
                c = PSU.objects.get(name__iexact=name_obj)
                c.part_number=form.cleaned_data['part_number']
                c.vendor=form.cleaned_data['vendor']
                c.price=form.cleaned_data['price']
                c.desc_ukr=form.cleaned_data['desc_ukr']
                c.desc_ru=form.cleaned_data['desc_ru']
                c.psu_p=form.cleaned_data['psu_p']
                c.psu_c=form.cleaned_data['psu_c']
                c.psu_f=form.cleaned_data['psu_f']
                c.more=form.cleaned_data['more']
                c.save()
                messages.success(request, f"{name_obj} is update")
            forversum_adv_add(request,form.cleaned_data['part_number'],name_obj,'ps')
            return  HttpResponseRedirect(
                                        reverse('forversum',
                                        kwargs={'i':i,'id':0}
                                        )
                                        )
        return  HttpResponseRedirect(
                                    reverse('forversum',
                                    kwargs={'i':i,'id':0}
                                    )
                                    )
    if request.method == 'POST' and i=='gpu':
        form = GpuForm(request.POST)
        if form.is_valid():
            name_obj = request.POST['name']
            c = GPU.objects.filter(name__iexact=name_obj)
            if not c:
                GPU.objects.create(name=name_obj, part_number=form.cleaned_data['part_number'],
                vendor=form.cleaned_data['vendor'],price=form.cleaned_data['price'],
                desc_ukr=form.cleaned_data['desc_ukr'],desc_ru=form.cleaned_data['desc_ru'],
                f_name=form.cleaned_data['f_name'],main_category=form.cleaned_data['main_category'],
                gpu_fps=form.cleaned_data['gpu_fps'],gpu_m_s=form.cleaned_data['gpu_m_s'],
                gpu_b=form.cleaned_data['gpu_b'],gpu_cpu_spd=form.cleaned_data['gpu_cpu_spd'],
                gpu_mem_spd=form.cleaned_data['gpu_mem_spd'],more=form.cleaned_data['more'],is_active = True)
                messages.success(request, f"{name_obj} is created")
            else:
                c = GPU.objects.get(name__iexact=name_obj)
                c.part_number=form.cleaned_data['part_number']
                c.vendor=form.cleaned_data['vendor']
                c.price=form.cleaned_data['price']
                c.desc_ukr=form.cleaned_data['desc_ukr']
                c.desc_ru=form.cleaned_data['desc_ru']
                c.f_name=form.cleaned_data['f_name']
                c.main_category=form.cleaned_data['main_category']
                c.gpu_fps=form.cleaned_data['gpu_fps']
                c.gpu_m_s=form.cleaned_data['gpu_m_s']
                c.gpu_b=form.cleaned_data['gpu_b']
                c.gpu_cpu_spd=form.cleaned_data['gpu_cpu_spd']
                c.gpu_mem_spd=form.cleaned_data['gpu_mem_spd']
                c.more=form.cleaned_data['more']
                c.save()
                messages.success(request, f"{name_obj} is update")
            return  HttpResponseRedirect(
                                        reverse('forversum',
                                        kwargs={'i':i,'id':0}
                                        )
                                        )
        return  HttpResponseRedirect(
                                    reverse('forversum',
                                    kwargs={'i':i,'id':0}
                                    )
                                    )
    if request.method == 'POST' and i=='fan':
        form = FanForm(request.POST)
        if form.is_valid():
            name_obj = request.POST['name']
            c = FAN.objects.filter(name__iexact=name_obj)
            if not c:
                FAN.objects.create(name=name_obj, part_number=form.cleaned_data['part_number'],
                vendor=form.cleaned_data['vendor'],price=form.cleaned_data['price'],
                desc_ukr=form.cleaned_data['desc_ukr'],desc_ru=form.cleaned_data['desc_ru'],
                case_fan_spd_ua=form.cleaned_data['case_fan_spd_ua'],
                case_fan_spd_rus=form.cleaned_data['case_fan_spd_rus'],
                case_fan_noise_level=form.cleaned_data['case_fan_noise_level'],
                case_fan_size=form.cleaned_data['case_fan_size'],
                more=form.cleaned_data['more'],is_active = True)
                messages.success(request, f"{name_obj} is created")
            else:
                c = FAN.objects.get(name__iexact=name_obj)
                c.part_number=form.cleaned_data['part_number']
                c.vendor=form.cleaned_data['vendor']
                c.price=form.cleaned_data['price']
                c.desc_ukr=form.cleaned_data['desc_ukr']
                c.desc_ru=form.cleaned_data['desc_ru']
                c.case_fan_spd_ua=form.cleaned_data['case_fan_spd_ua']
                c.case_fan_spd_rus=form.cleaned_data['case_fan_spd_rus']
                c.case_fan_noise_level=form.cleaned_data['case_fan_noise_level']
                c.case_fan_size=form.cleaned_data['case_fan_size']
                c.more=form.cleaned_data['more']
                c.save()
                messages.success(request, f"{name_obj} is update")
            return  HttpResponseRedirect(
                                        reverse('forversum',
                                        kwargs={'i':i,'id':0}
                                        )
                                        )
        return  HttpResponseRedirect(
                                    reverse('forversum',
                                    kwargs={'i':i,'id':0}
                                    )
                                    )
    if request.method == 'POST' and i=='ssd':
        form = SsdForm(request.POST)
        if form.is_valid():
            name_obj = request.POST['name']
            c = SSD.objects.filter(name__iexact=name_obj)
            if not c:
                SSD.objects.create(name=name_obj, part_number=form.cleaned_data['part_number'],
                vendor=form.cleaned_data['vendor'],price=form.cleaned_data['price'],
                desc_ukr=form.cleaned_data['desc_ukr'],desc_ru=form.cleaned_data['desc_ru'],
                f_name=form.cleaned_data['f_name'],ssd_s=form.cleaned_data['ssd_s'],
                ssd_spd=form.cleaned_data['ssd_spd'],ssd_r_spd=form.cleaned_data['ssd_r_spd'],
                more=form.cleaned_data['more'],ssd_type_cells=form.cleaned_data['ssd_type_cells'],is_active = True)
                messages.success(request, f"{name_obj} is created")
            else:
                c = SSD.objects.get(name__iexact=name_obj)
                c.part_number=form.cleaned_data['part_number']
                c.vendor=form.cleaned_data['vendor']
                c.price=form.cleaned_data['price']
                c.desc_ukr=form.cleaned_data['desc_ukr']
                c.desc_ru=form.cleaned_data['desc_ru']
                c.f_name=form.cleaned_data['f_name']
                c.ssd_s=form.cleaned_data['ssd_s']
                c.ssd_spd=form.cleaned_data['ssd_spd']
                c.ssd_r_spd=form.cleaned_data['ssd_r_spd']
                c.ssd_type_cells=form.cleaned_data['ssd_type_cells']
                c.more=form.cleaned_data['more']
                c.save()
                messages.success(request, f"{name_obj} is update")
            return  HttpResponseRedirect(
                                        reverse('forversum',
                                        kwargs={'i':i,'id':0}
                                        )
                                        )
        return  HttpResponseRedirect(
                                    reverse('forversum',
                                    kwargs={'i':i,'id':0}
                                    )
                                    )

def for_itblok(request,id):
    atr_list = ('aproc', 'iproc', 'amb', 'imb', 'video', 'mem', 'ssd', 'hdd', 'ps', 'cool', 'case', 'vent','mon', 'wifi', 'km','cool')
    short_itblok = Parts_short.objects.filter(kind2=True)
    short_itblok2 = []
    for x in atr_list:
        q = short_itblok.filter(kind=x) if x not in ('vent',) else Parts_short.objects.filter(kind=x)
        short_itblok2.append(q)
    if request.method == 'GET' and id == 0:
        context = {
               'itblok': short_itblok2
              }
        return render(request, 'cat/for_itblok.html', context)
    if request.method == 'GET' and id != 0:
        res = request.GET
        short = Parts_short.objects.get(pk=id)
        try:
            aa=Articles.objects.filter(article__in=eval(short.partnumber_list))
        except:
            aa=Articles.objects.filter(article__in=[])
        if 'search' in res:
            res = request.GET['search']
            aa=Articles.objects.filter(item_name__icontains=res)
        par = []
        for x in aa:
            p = Parts_full.objects.filter(partnumber_parts=x.article).distinct().order_by(
            'providerprice_parts')
            if p.count():
                pp = p.filter(providers__name_provider='-')
                if pp.count() and pp.first().providerprice_parts:
                    if not pp.first().url_parts:
                        q=pp.first()
                        q.url_parts = p.first().url_parts
                        q.save()
                    par.append(p.order_by('providers__name_provider'))
                else:
                    par.append(p)
        context = {
               'itblok': short_itblok2,
               'par': par,
               'short': short
              }
        return render(request, 'cat/for_itblok.html', context)
    if request.method == 'POST':
        if 'price' in request.POST:
            price = request.POST['price']
            price = re.sub(',' ,'.', price)
            short = Parts_short.objects.get(pk=id)
            short_kind = short.kind
            if short_kind and short_kind[0] in ('a','i'):
                short_kind2 = short_kind[1:]
            else:
                short_kind2 = short_kind
            comps = need_comps(short.name_parts)
            for c in comps:
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
                    if x in ('vent_computers', 'proc_computers', 'mb_computers', 'mem_computers', 'video_computers', 'hdd_computers', 'hdd2_computers', 'ps_computers', 'case_computers', 'cool_computers','mon_computers','wifi_computers','km_computers'):
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
            messages.success(request, f"Price in {short.name_parts} is update new price: {price}")
            list_for_index = [x.pk for x in Parts_short.objects.filter(kind=short_kind)]
            try:
                id = list_for_index.index(id)
                id = list_for_index[id+1]
            except:
                id = 0
                messages.success(request, "Update is ending")
        return  HttpResponseRedirect(
                                    reverse('for_itblok',
                                    kwargs={'id':id}
                                    )
                                    )
