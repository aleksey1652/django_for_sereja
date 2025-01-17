from django.utils import timezone
import os, django, pickle, json, re
from django.shortcuts import render,redirect
from django.urls import reverse
from django.http import HttpResponseRedirect,HttpResponse
from sereja.tasks import *
from cat.models import *
from descriptions.models import *
from django.contrib import messages
from django.db.models import Min
import pandas as pd
import time
#from pars.views import content_versum2
from .forms import Pc_assemblyForm
from descriptions.views import test_distrib_price_none
from load_form_providers.load_element import to_article2_1
from load_form_providers.dc_descr_catalog import from_price_get_new_models, from_price_get_new_tech
#providerprice_parts test_group price_get_new_models test_group

def content_versum2(name_parts,kind,num={}):
    # переделанная фун от(см 6 строки выше): если нет привязки к шорт от прайса,
    # но есть дискрипшин, передавать в АПИ но сигнализировать об ошибке
    # content_versum2 в этом модуле - ошибка, content_versum2 в pars -нет
    # переделка в if short2.parts_full.first(): else (после else)
    from descriptions.views import test_distrib

    bit = {'content_versum2':True}
    if kind in ('soft','wifi','cables', 'vent') and (name_parts == None or name_parts == ''):
        name_parts = 'пусто'
    if name_parts == 'пусто' and kind in ('soft','wifi','cables', 'ps', 'vent'):
        return ['', '1'],bit
    elif name_parts == 'пусто' and kind not in ('soft','wifi','cables', 'ps'):
        return ['', '1'],{'content_versum2':False}
    if not isinstance(kind,tuple):
        short = Parts_short.objects.filter(name_parts=name_parts,kind=kind, kind2=False)
    else:
        if name_parts == 'пусто':
            short = Parts_short.objects.filter(name_parts=name_parts,kind='hdd', kind2=False)
        else:
            short = Parts_short.objects.filter(name_parts=name_parts,kind__in=kind,
            kind2=False)
    if short.exists():
        short2 = short.first()
        full = short2.parts_full
        full2 = full.first()
        if short.count() > 1 or not test_distrib(short2.kind, short2.name_parts):
            bit['content_versum2'] = False
        """    for s in short:
                if not s.parts_full.first():
                    s.delete()
                else:
                    bit['content_versum2'] = False"""
        if short2.parts_full.first():
            if not num:
                return [full2.partnumber_parts, '1'], bit
            else:
                num_ = num[short2.kind] if short2.kind in num else '1'
                return [full2.partnumber_parts, num_], bit
        else:
            return ['', '1'],{'content_versum2':False}
    else:
        return ['', '1'],{'content_versum2':False}

def content_for_google_sheet_se(obj,p):

    dict_error_in_moduls = dict()
    bit = {'content_for_google_sheet':True, 'error_parts': dict_error_in_moduls, 'comp': obj}

    list_atr = ['mb_computers', 'proc_computers', 'mem_computers', 'video_computers',
    'hdd_computers', 'case_computers', 'ps_computers', 'cool_computers','vent_computers',
    'wifi_computers','cables_computers','soft_computers']

    dict_atr = {'mb_computers':'mb', 'proc_computers':'cpu', 'mem_computers':'ram',
    'video_computers':'gpu',
    'hdd_computers':'hdd', 'case_computers':'case', 'ps_computers':'ps',
    'cool_computers':'cooler',
    'vent_computers':'vent','wifi_computers':'wifi','cables_computers':'cables',
    'soft_computers':'soft'}

    if p == 'versum':
        for k,v in dict_atr.items():
            if k != 'hdd_computers':
                if not obj.__dict__[k] or obj.__dict__[k].lower().find('встановлено') != -1:
                    thing = 'пусто'
                else:
                    thing = obj.__dict__[k]
                if k == 'proc_computers':
                    kind = to_article2_1(thing)
                elif k == 'mb_computers':
                    kind = to_article2_1(thing,pr=0)
                else:
                    #list_full.append([x,obj.__dict__[x],1]+content_versum(obj,x))
                    kind = re.sub('_computers','',k)
                cont = content_versum2(thing, kind)
                if cont[1]['content_versum2'] == True:
                    continue
                else:
                    dict_error_in_moduls[k] = thing
            else:
                if obj.hdd_computers == 'пусто;пусто':
                    dict_error_in_moduls[k] = 'hdd_computers'
                for y in obj.hdd_computers.split(';'):
                    if not y or y.lower().find('встановлено') != -1:
                        y = 'пусто'
                    #list_full.append([x,y,1]+content_versum(obj,x))
                    if y.lower().find('ssd') != -1:
                        kind = ('ssd',)
                    elif y.lower().find('3,5') != -1:
                        kind = ('hdd',)
                    else:
                        continue
                    cont = content_versum2(y, kind)
                    if cont[1]['content_versum2'] == True:
                        continue
                    else:
                        dict_error_in_moduls[k] = y
        if len(dict_error_in_moduls) == 0:
            return bit
            #return list_full,list_error_in_moduls
        else:
            #print(list_error_in_moduls)
            return {'content_for_google_sheet':False, 'error_parts': dict_error_in_moduls, 'comp': obj}
            #return list_full,list_error_in_moduls

def rename_group(request,page, pc_ass):
    if request.method == 'GET':
        form = Pc_assemblyForm()
        context = {
                   'form': form,
                   'pc_ass': pc_ass
                  }
    if request.method == 'GET' and page == 'del' and pc_ass > 2:
        assembly = Pc_assembly.objects.get(pk=pc_ass)
        if not Computers.objects.filter(pc_assembly=assembly):
            assembly.delete()
            messages.warning(request,f'{assembly.name_assembly} group is delete')
        else:
            messages.warning(request,f'{assembly.name_assembly} group is not empty (only for clear groups!)')
        return  HttpResponseRedirect(
                                    reverse('assembly_page',
                                    kwargs={'page_id':'versum'}
                                    )
                                    )
    if request.method == 'GET' and pc_ass > 2 and page == 'group':
        assembly = Pc_assembly.objects.get(pk=pc_ass)
        messages.warning(request,f'Enter new group name (old: {assembly.name_assembly})')
        context = {
                   'form': form,
                   'pc_ass': pc_ass,
                   'page': 'group'
                  }
        return render(request, 'cat/computer_created.html', context)
    elif request.method == 'GET' and pc_ass == 0 and page in ('versum','itblok'):
        messages.warning(request,'Enter group name')
        return render(request, 'cat/computer_created.html', context)
    elif request.method == 'GET' and pc_ass == 2 and page in ('versum','itblok'):
        messages.warning(request,'Enter series name')
        return render(request, 'cat/computer_created.html', context)
    elif request.method == 'GET' and pc_ass > 2 and page in ('versum','itblok', 'aaa'):
        c = Computers.objects.get(pk=pc_ass)
        messages.warning(request,f'Enter new computer name(old: {c.name_computers})')
        return render(request, 'cat/computer_created.html', context)
    elif request.method == 'GET' and pc_ass  > 2 and page not in ('versum','itblok','aaa','group','del'):
        pc_assembly_ver=Pc_assembly.objects.filter(sites__name_sites='versum').prefetch_related('sites')
        pc_assembly_ver_set = {x['kind_assembly'] for x in pc_assembly_ver.values() if x}
        pc_assembly_ver_set2 = {re.sub(' ', '_', x) for x in pc_assembly_ver_set if x}
        #messages.warning(request,f'realy {page})')
        if page in pc_assembly_ver_set:
            context = {
                       'form': form,
                       'pc_ass': pc_ass,
                       'page': page,
                       'pc_assembly_ver_set': pc_assembly_ver_set2
                      }
            return render(request, 'cat/computer_created.html', context)
        c = Computers.objects.get(pk=pc_ass)
        pcassembly_ver=Pc_assembly.objects.filter(sites__name_sites='versum')
        messages.warning(request,f'Change computer group or leave as it was(old: {page})')
        """for x in pcassembly_ver:
            messages.warning(request,f'Yout choise: {x.name_assembly}')"""
        context = {
                   'form': form,
                   'pc_ass': pc_ass,
                   'page': page,
                   'pcassembly_ver': pcassembly_ver
                  }
        return render(request, 'cat/computer_created.html', context)

    elif request.method == 'POST':
        if page == 'pc_out':
            c = Computers.objects.get(pk=pc_ass)
            #pc_assembly_ver=Pc_assembly.objects.filter(sites=c.pc_assembly.sites)
            #c_assembly_ver_set = {int(x['id']) for x in pc_assembly_ver.values()}
            if len(request.POST.keys()) == 2:
                id = list(request.POST.keys())[1]
                try:
                    id = int(id)
                except:
                    id = None
                if id:
                    c.pc_assembly = Pc_assembly.objects.get(pk=id)
                    c.save()
                    #messages.warning(request,f'{c_assembly_ver_set,id}')
            #l1 = [x for x in list(request.POST.keys()) if x != 'csrfmiddlewaretoken']
            #messages.warning(request,f'{request.POST.keys(),id}')
            return  HttpResponseRedirect(
                                        reverse('assembly_page',
                                        kwargs={'page_id':'versum'}
                                        )
                                        )
        if page == 'kind_out':
            assembly = Pc_assembly.objects.get(pk=pc_ass)
            pc_assembly_ver=Pc_assembly.objects.filter(sites=assembly.sites).prefetch_related('sites')
            pc_assembly_ver_set = {x['kind_assembly'] for x in pc_assembly_ver.values()}
            if len(request.POST.keys()) == 2:
                dop = re.sub('_', ' ' , list(request.POST.keys())[1])
                if dop in pc_assembly_ver_set:
                    assembly.kind_assembly = dop
                    assembly.save()
            #l1 = [x for x in list(request.POST.keys()) if x != 'csrfmiddlewaretoken']
            #messages.warning(request,f'{request.POST.keys(),dop}')
            return  HttpResponseRedirect(
                                        reverse('assembly_page',
                                        kwargs={'page_id':'versum'}
                                        )
                                        )
        form = Pc_assemblyForm(request.POST)
        context = {
                   'form': form,
                   'pc_ass': pc_ass
                  }
        if form.is_valid() and pc_ass > 2 and page == 'group':
            name_assembly = form.cleaned_data['name_assembly']
            assembly = Pc_assembly.objects.get(pk=pc_ass)
            #site = assembly.sites.name_sites
            #c = Computers.objects.filter(pc_assembly=assembly)
            assembly.name_assembly = name_assembly
            assembly.save()
            messages.success(request, f'New group name {assembly.name_assembly}')
            #pc_assembly_ver=Pc_assembly.objects.filter(sites__name_sites='versum').prefetch_related('sites')
            #pc_assembly_ver_set = {x['kind_assembly'] for x in pc_assembly_ver.values()}
            messages.warning(request,f'Change computer series or leave as it was(old: {assembly.kind_assembly})')
            """for x in pc_assembly_ver_set:
                messages.warning(request,f'Yout choise: {x}')"""
            return  HttpResponseRedirect(
                                        reverse('rename_group',
                                        kwargs={'page':assembly.kind_assembly,
                                                'pc_ass':pc_ass}
                                        )
                                        )
        if form.is_valid() and pc_ass == 0 and page in ('versum','itblok','aaa'):
            """name_assembly = form.cleaned_data['name_assembly']
            assembly = Pc_assembly.objects.get(pk=pc_ass)
            #site = assembly.sites.name_sites
            #c = Computers.objects.filter(pc_assembly=assembly)
            assembly.name_assembly = name_assembly
            assembly.save()
            messages.success(request, f'New group name {assembly.name_assembly}')
            pc_assembly_ver=Pc_assembly.objects.filter(sites__name_sites='versum').prefetch_related('sites')
            pc_assembly_ver_set = {x['kind_assembly'] for x in pc_assembly_ver.values()}
            messages.warning(request,f'Change computer series or leave as it was(old: {assembly.kind_assembly})')
            for x in pc_assembly_ver_set:
                messages.warning(request,f'Yout choise: {x}')
            return  HttpResponseRedirect(
                                        reverse('rename_group',
                                        kwargs={'page':assembly.kind_assembly,
                                                'pc_ass':pc_ass}
                                        )
                                        )"""
            name_assembly = form.cleaned_data['name_assembly']
            site,p_ = Sites.objects.get_or_create(name_sites=page)
            if  not Pc_assembly.objects.filter(name_assembly=name_assembly,sites=site).exists():
                Pc_assembly.objects.create(name_assembly=name_assembly,sites=site)
                messages.success(request, f'New group name: {name_assembly}')
            else:
                messages.success(request, f'This group name is exist: {name_assembly}')
            assembly = Pc_assembly.objects.get(name_assembly=name_assembly,sites=site)
            pc_assembly_ver=Pc_assembly.objects.filter(sites__name_sites='versum').prefetch_related('sites')
            pc_assembly_ver_set = {x['kind_assembly'] for x in pc_assembly_ver.values()}
            messages.warning(request,'Change computer series')
            for x in pc_assembly_ver_set:
                messages.warning(request,f'Yout choise: {x}')
            return  HttpResponseRedirect(
                                        reverse('rename_group',
                                        kwargs={'page':'Other',
                                                'pc_ass':assembly.pk}
                                        )
                                        )
            """return  HttpResponseRedirect(
                                        reverse('assembly_page',
                                        kwargs={'page_id':page}
                                        )
                                        )"""
        if form.is_valid() and pc_ass == 2 and page in ('versum','itblok','aaa'):
            name_series = form.cleaned_data['name_assembly']
            site,p_ = Sites.objects.get_or_create(name_sites=page)
            if Pc_assembly.objects.filter(kind_assembly=name_series).exists():
                messages.error(request, f'This series ({name_series}) already exists, join the groups')
                return  HttpResponseRedirect(
                                            reverse('add_series',
                                            kwargs={'pc_ass':pc_ass,
                                                    'page':name_series}
                                            )
                                            )
            Pc_assembly.objects.create(kind_assembly=name_series,name_assembly='noname',sites=site)
            messages.success(request, f'New series name: {name_series}')
            """return  HttpResponseRedirect(
                                        reverse('assembly_page',
                                        kwargs={'page_id':page}
                                        )
                                        )"""
            return  HttpResponseRedirect(
                                        reverse('add_series',
                                        kwargs={'pc_ass':pc_ass,
                                                'page':name_series}
                                        )
                                        )
        if form.is_valid() and pc_ass > 2 and page in ('versum','itblok','aaa'):
            name_comp = form.cleaned_data['name_assembly']
            c = Computers.objects.get(pk=pc_ass)
            c.name_computers = name_comp
            c.save()
            c_compprice = c.compprice
            c_compprice.name_computers = name_comp
            c_compprice.save()
            name_assembly = c.pc_assembly.name_assembly
            messages.success(request, f'New computer name: {c.name_computers}')
            return  HttpResponseRedirect(
                                        reverse('rename_group',
                                        kwargs={'page':name_assembly,
                                                'pc_ass':pc_ass}
                                        )
                                        )
        if form.is_valid() and pc_ass > 2 and page not in ('versum','itblok','aaa','group'):
            pc_assembly_ver = Pc_assembly.objects.filter(sites__name_sites='versum').prefetch_related('sites')
            pc_assembly_ver_set = {x['kind_assembly'] for x in pc_assembly_ver.values()}
            if page in pc_assembly_ver_set:
                kind_assembly = form.cleaned_data['name_assembly']
                assembly = Pc_assembly.objects.get(pk=pc_ass)
                assembly.kind_assembly = kind_assembly if kind_assembly in pc_assembly_ver_set else pc_assembly_ver_set[0]
                assembly.save()
                messages.success(request, f'New computer series: {kind_assembly}')
                return  HttpResponseRedirect(
                                            reverse('assembly_page',
                                            kwargs={'page_id':'versum'}
                                            )
                                            )
            name_assembly = form.cleaned_data['name_assembly']
            pc = Pc_assembly.objects.filter(name_assembly=name_assembly,sites__name_sites='versum')
            if not pc:
                messages.error(request, f'{name_assembly} not exist ')
                return  HttpResponseRedirect(
                                            reverse('rename_group',
                                            kwargs={'page':name_assembly,
                                                    'pc_ass':pc_ass}
                                            )
                                            )
            pc = pc.first()
            c = Computers.objects.get(pk=pc_ass)
            c.pc_assembly = pc
            c.save()
            name_assembly = c.pc_assembly.name_assembly
            messages.success(request, f'New computer group: {name_assembly}')
            return  HttpResponseRedirect(
                                        reverse('assembly',
                                        kwargs={'pc_id':pc_ass}
                                        )
                                        )
        return  HttpResponseRedirect(
                                    reverse('assembly_page',
                                    kwargs={'page_id':page}
                                    )
                                    )

def add_series(request,page,pc_ass):
    if request.method == 'GET':
        #c = Computers.objects.get(pk=pc_ass)
        #p = Pc_assembly.objects.filter(sites__name_sites=c.pc_assembly.sites.name_sites)
        a= Pc_assembly.objects.filter(kind_assembly=page)
        site = a.first().sites.name_sites
        p = Pc_assembly.objects.filter(sites__name_sites=site)
        return render(request, 'pars/add_series.html',{'group':p,'pc_ass':pc_ass,'page':page})
    if request.method == 'POST':
        l1 = [x for x in list(request.POST.keys()) if x != 'csrfmiddlewaretoken']
        Pc_assembly.objects.filter(name_assembly__in=l1).update(kind_assembly=page)
        messages.warning(request,f'Now in series: {page} exists {l1} groups')
        return  HttpResponseRedirect(
                                    reverse('assembly_page',
                                    kwargs={'page_id':'versum'}
                                    )
                                    )
def rename_series(request,page):
    if request.method == 'GET':
        form = Pc_assemblyForm()
        context = {
                   'form': form
                  }
        if Pc_assembly.objects.filter(kind_assembly=page).exists():
            #Pc_assembly.objects.filter(kind_assembly=page).update(kind_assembly=page)
            messages.warning(request,'Enter new series name')
            return render(request, 'cat/computer_created.html', context)
    if request.method == 'POST':
        form = Pc_assemblyForm(request.POST)
        context = {
                   'form': form
                  }
        if form.is_valid():
            name_series = form.cleaned_data['name_assembly']
            if Pc_assembly.objects.filter(kind_assembly=page).exists():
                Pc_assembly.objects.filter(kind_assembly=page).update(kind_assembly=name_series)
        messages.success(request, f'New series name {name_series} ')
        return  HttpResponseRedirect(
                                    reverse('assembly_page',
                                    kwargs={'page_id':'versum'}
                                    )
                                    )
#
def asinc_test_comps():
    cver=Computers.objects.filter(pc_assembly__sites__name_sites='versum',is_active=True)
    set_list = []

    for comp in cver:
        comp_chec = content_for_google_sheet_se(comp,'versum')
        if not comp_chec['content_for_google_sheet']:
            set_list.append(comp_chec)

    r, _ = Results.objects.get_or_create(who='test_comps')
    if set_list:
        set_list = [f"Wrong comps: {s['comp'].name_computers},'error_parts':{s['error_parts']}" for s in set_list]
        try:
            r.who_desc = ';\n'.join(set_list)
            r.save()
        except:
            r.who_desc = 'Many wrong comps'
            r.save()
    else:
        r.who_desc = "All comps goods"
        r.save()
    return ';\n'.join(set_list)
        #messages.success(request,"All comps goods")

@app.task
def tasc_test_comps():
    asinc_test_comps()

@app.task
def tasc_new_parts_from_prov(prov_):
    from_price_get_new_models(prov_)

@app.task
def tasc_tech_parts_from_prov(prov_):
    from_price_get_new_tech(prov_)

def price_get_tech_models(request,prov):
    tasc_tech_parts_from_prov.delay(prov_=prov)

    return  HttpResponseRedirect(
                                reverse('assembly_page',
                                kwargs={'page_id': 'versum'}
                                )
                                )

def price_get_new_models(request,prov):
    tasc_new_parts_from_prov.delay(prov_=prov)

    return  HttpResponseRedirect(
                                reverse('assembly_page',
                                kwargs={'page_id': 'versum'}
                                )
                                )


def test_group(request,kind):
    tasc_test_comps.delay()

    if kind ==1:
        set_er2=test_distrib_price_none()

        messages.warning(request,f'Not price in comps: {set_er2}')

    return  HttpResponseRedirect(
                                reverse('assembly_page',
                                kwargs={'page_id': 'versum'}
                                )
                                )

def promotion(request,site,prom_id):
    set_series = ['Original series','Epic series','Legendary series',
    'Mini series','Custom series','Brand series','SE series',
    'Business series','Marketplace','Other']
    """tempo = []
    for s in Pc_assembly.objects.filter(sites__name_sites='versum'):
        if s.kind_assembly not in set_series and s.kind_assembly != '':
            tempo.append(s.kind_assembly)
    set_series = set_series + tempo"""
    set_prom = Promotion.objects.all().order_by('prom')
    cver = Computers.objects.filter(pc_assembly__sites__name_sites=site)
    choise = []
    if prom_id != 0:
        choise = cver.filter(pk=prom_id)
    if request.method == 'GET':
        if 'search' in request.GET.keys():
            search = request.GET['search']
            choise = cver.filter(name_computers__icontains=search)
        set_labels = set()
        for r in request.GET.keys():
            if r != 'csrfmiddlewaretoken' and r != 'empty' and r != 'search':
                #messages.warning(request,f'{request.GET[r]}')
                try:
                    pr = Promotion.objects.get(pk=int(request.GET[r]))
                    set_labels.add(pr)
                except:
                    messages.error(request,f'error in {request.GET[r]}')
            elif r == 'empty':
                pr = Promotion.objects.get(pk=request.GET[r])
                choise = cver.exclude(promotion__in=set_prom)
                #messages.warning(request,f'In {c.name_computers} not labels')
        qs = None
        if set_labels:
            #choise = cver.filter(promotion__in=set_labels)
            for s in set_labels:
                if not qs:
                    qs = cver.filter(promotion=s)
                else:
                    q = cver.filter(promotion=s)
                    qs = qs.intersection(q)
            choise = qs

        context = {
                   'set_prom': set_prom,
                   'site': site,
                   'cver': cver,
                   'choise': choise
                  }
        messages.warning(request,'For RENAME label!!! old_name_:new_name')
        return render(request, 'pars/prom.html', context)
    if request.method == 'POST':
        if 'add' in request.POST.keys():
            add = request.POST['add']
            if not Promotion.objects.filter(prom=add).exists():
                Promotion.objects.create(prom='empty')
                messages.warning(request,f'Added label: {add}')
            else:
                messages.warning(request,f'{add} already exists')
        if 'rename' in request.POST.keys():
            rename = request.POST['rename']
            l1 = rename.split(':')
            if len(l1) == 2:
                if Promotion.objects.filter(prom=l1[0]).exists():
                    try:
                        pr = Promotion.objects.get(prom=l1[0])
                        pr.update(prom=l1[1])
                    except:
                        messages.error(request,f'error in update: {l1[0]}')
                else:
                    messages.error(request,f'{l1[0]} not exist')
            else:
                messages.error(request,f'Wrong,try: old_name_:new_name')
        if prom_id != 0:
            set_labels = set()
            c = cver.get(pk=prom_id)
            for r in request.POST.keys():
                if r != 'csrfmiddlewaretoken' and r != 'empty':
                    #messages.warning(request,f'{request.POST[r]}')
                    try:
                        set_labels.add(r)
                        pc = Promotion.objects.get(pk=request.POST[r])
                        c = cver.get(pk=prom_id)
                        c.promotion_set.add(pc)
                    except:
                        messages.error(request,f'error in {pc.prom}')
                elif r == 'empty':
                    c = cver.get(pk=prom_id)
                    c.promotion_set.clear()
                    messages.warning(request,f'In {c.name_computers} not labels')
            messages.warning(request,f'In {c.name_computers} labels:{set_labels}')
    context = {
               'set_prom': set_prom,
               'site': site,
               'cver': cver,
               'choise': choise
              }
    messages.warning(request,'For RENAME label!!! old_name_:new_name')
    return render(request, 'pars/prom.html', context)
