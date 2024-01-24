from rest_framework.response import Response
from django.shortcuts import render,redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect,HttpResponse, HttpResponseNotFound, Http404
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Sum, Count, F, Min
import json


from .models import *
from .utils import *
from .forms import *


def test_assemblage(request, assm_slug):
    pass
    return HttpResponse(f"hello assm_slug")

def test_groups(request, gr_slug):
    pass
    return HttpResponse(f"hello gr_slug")

def admin_rivals_active(request, rivals_pk):
    usd = USD.objects.last().usd

    form = AssemblageForm()

    context = {
                'form': form,
                'rivals_pk': rivals_pk,
              }

    if request.method == 'POST':
        rivals_pk_ = rivals_pk.split(',')
        form = AssemblageForm(request.POST)
        if form.is_valid():
            is_active_ = form.cleaned_data['is_active']
            mes = 'вкл' if is_active_ else 'выкл'

            asmbl = Assemblage.objects.filter(pk__in=rivals_pk_)
            count = asmbl.update(is_active=is_active_)
            messages.success(request,f'Сборки ({count} шт): {mes}')
            return  HttpResponseRedirect(
                                        reverse('admin:rivals_assemblage_changelist')
                                        )

    return render(request, 'money/admin_test.html', context)


def rivals_to_results(rivals_, mes):
    #
    if not Results.objects.filter(who=rivals_).exists():
        r = Results(who=rivals_,
        who_desc=f'{rivals_}: {mes}')
        r.save()
    else:
        r = Results.objects.get(who=rivals_)
        r.who_desc = f'{rivals_}: {mes}'
        r.save()

def rivals_to_models(rivals_):
    #
    query_rivals = Assemblage.objects.filter(is_active=True).values('name')
    mes = 'нет ссылок'
    set_mes = set()

    if rivals_ == 'hotline':
        assemble =  Assemblage.objects.filter(hotline__isnull=False)
        for asml in assemble:
            riv = RivalsData(asml.hotline)
            data, mes = riv.hotline_data()
            if mes != 'ok':
                set_mes.add(asml.hotline)
            versum_data, versum_mes = riv.versum_portal_data(asml.name)
            asml.hot_price = data
            asml.ver_price = versum_data
            asml.ver_hot = versum_data - data if data else 0
            asml.save()
    if rivals_ == 'itblok':
        assemble =  Assemblage.objects.filter(itblok__isnull=False)
        for asml in assemble:
            riv = RivalsData(asml.itblok)
            data, mes = riv.itblok_data()
            if mes != 'ok':
                set_mes.add(asml.itblok)
            versum_data, versum_mes = riv.versum_portal_data(asml.name)
            asml.it_price = data
            asml.ver_price = versum_data
            asml.ver_it = versum_data - data if data else 0
            asml.save()
    if rivals_ == 'artline':
        assemble =  Assemblage.objects.filter(artline__isnull=False)
        for asml in assemble:
            riv = RivalsData(asml.artline)
            data, mes = riv.art_data()
            if mes != 'ok':
                set_mes.add(asml.artline)
            versum_data, versum_mes = riv.versum_portal_data(asml.name)
            asml.art_price = data
            asml.ver_price = versum_data
            asml.ver_art = versum_data - data if data else 0
            asml.save()
    if rivals_ == 'telemart':
        assemble =  Assemblage.objects.filter(telemart__isnull=False)
        for asml in assemble:
            riv = RivalsData(asml.telemart)
            data, mes = riv.telemart_data()
            if mes != 'ok':
                set_mes.add(asml.telemart)
            versum_data, versum_mes = riv.versum_portal_data(asml.name)
            asml.tel_price = data
            asml.ver_price = versum_data
            asml.ver_tel = versum_data - data if data else 0
            asml.save()
    if rivals_ == 'compx':
        assemble =  Assemblage.objects.filter(compx__isnull=False)
        for asml in assemble:
            riv = RivalsData(asml.compx)
            data, mes = riv.compx_data()
            if mes != 'ok':
                set_mes.add(asml.compx)
            versum_data, versum_mes = riv.versum_portal_data(asml.name)
            asml.com_price = data
            asml.ver_price = versum_data
            asml.ver_com = versum_data - data if data else 0
            asml.save()

    list_mes = list(set_mes)[:10]
    if not list_mes:
        rivals_to_results(rivals_, mes)
    else:
        mes = f'error_url({len(set_mes)}):' + ', '.join(list_mes)
        rivals_to_results(rivals_, mes)
