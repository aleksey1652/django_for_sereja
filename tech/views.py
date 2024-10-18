from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from django.contrib import messages
import itertools
import json,pickle
import os,re
import datetime
import time as tme
from django.utils import timezone
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import serializers
import requests

from .serializers import *
from sereja.settings import *
from .models import *
from singleparts.forms import RentabilityForm, SinglePackFewForm, AutoForm, IsActiveForm

#change_auto_obj

def change_rentability_tech(request, obj_pack, obj_model):
    # массовая замена для tech наценки

    dict_models ={
    'monitors': Monitors.objects.all(),
    'km': KM.objects.all(),
    'keyboards': Keyboards.objects.all(),
    'mouses': Mouses.objects.all(),
    'pads': Pads.objects.all(),
    'headsets': Headsets.objects.all(),
    'webcams': Webcams.objects.all(),
    'wifis': WiFis.objects.all(),
    'acoustics': Acoustics.objects.all(),
    'tables': Tables.objects.all(),
    'chairs': Chairs.objects.all(),
    'accessories': Accessories.objects.all(),
    'cabelsplus': Cabelsplus.objects.all(),
    'filters': Filters.objects.all(),
    'others': Others.objects.all(),
    }

    form = RentabilityForm()

    context = {
                'form': form,
                'obj_pack': obj_pack,
              }

    if request.method == 'POST':
        form = RentabilityForm(request.POST)
        if form.is_valid():
            obj_pk = [int(c) for c in obj_pack.split(',')]
            #comps = Computers.objects.filter(pk__in=comps_pk)
            objs = dict_models[obj_model].filter(pk__in=obj_pk)

            rent = form.cleaned_data['rentability']

            count_objs = objs.update(
            rentability=rent
            )
            messages.success(
            request,
            f"In {count_objs} {obj_model} was update : {rent}")
            return  HttpResponseRedirect(
                                        reverse(
                                        f'admin:tech_{obj_model}_changelist'
                                        )
                                        )

    return render(request, 'money/admin_test.html', context)

def change_is_active_tech(request, obj_pack, obj_model):
    # массовая замена для tech is_active

    dict_models ={
    'monitors': Monitors.objects.all(),
    'km': KM.objects.all(),
    'keyboards': Keyboards.objects.all(),
    'mouses': Mouses.objects.all(),
    'pads': Pads.objects.all(),
    'headsets': Headsets.objects.all(),
    'webcams': Webcams.objects.all(),
    'wifis': WiFis.objects.all(),
    'acoustics': Acoustics.objects.all(),
    'tables': Tables.objects.all(),
    'chairs': Chairs.objects.all(),
    'accessories': Accessories.objects.all(),
    'cabelsplus': Cabelsplus.objects.all(),
    'filters': Filters.objects.all(),
    'others': Others.objects.all(),
    }

    form = IsActiveForm()

    context = {
                'form': form,
                'obj_pack': obj_pack,
              }

    if request.method == 'POST':
        form = IsActiveForm(request.POST)
        if form.is_valid():
            obj_pk = [int(c) for c in obj_pack.split(',')]
            #
            objs = dict_models[obj_model].filter(pk__in=obj_pk)

            is_active_ = form.cleaned_data['is_active']
            str_ = {'вкл': True, 'выкл': False}

            count_objs = objs.update(
            is_active=str_[is_active_]
            )
            messages.success(
            request,
            f"В {count_objs} {obj_model[:-6]} статус : {is_active_}")
            return  HttpResponseRedirect(
                                        reverse(
                                        f'admin:tech_{obj_model}_changelist'
                                        )
                                        )

    return render(request, 'money/admin_test.html', context)

def change_auto_tech(request, obj_pack, obj_model):
    # массовая замена для tech ручной цены

    dict_models ={
    'monitors': Monitors.objects.all(),
    'km': KM.objects.all(),
    'keyboards': Keyboards.objects.all(),
    'mouses': Mouses.objects.all(),
    'pads': Pads.objects.all(),
    'headsets': Headsets.objects.all(),
    'webcams': Webcams.objects.all(),
    'wifis': WiFis.objects.all(),
    'acoustics': Acoustics.objects.all(),
    'tables': Tables.objects.all(),
    'chairs': Chairs.objects.all(),
    'accessories': Accessories.objects.all(),
    'cabelsplus': Cabelsplus.objects.all(),
    'filters': Filters.objects.all(),
    'others': Others.objects.all(),
    }

    form = AutoForm()

    context = {
                'form': form,
                'obj_pack': obj_pack,
              }

    if request.method == 'POST':
        form = AutoForm(request.POST)
        if form.is_valid():
            obj_pk = [int(c) for c in obj_pack.split(',')]
            #comps = Computers.objects.filter(pk__in=comps_pk)
            objs = dict_models[obj_model].filter(pk__in=obj_pk)

            auto_ = form.cleaned_data['auto']

            count_objs = objs.update(
            auto=auto_
            )
            messages.success(
            request,
            f"In {count_objs} {obj_model} was update : {auto_}")
            return  HttpResponseRedirect(
                                        reverse(
                                        f'admin:tech_{obj_model}_changelist'
                                        )
                                        )

    return render(request, 'money/admin_test.html', context)

def change_few_things_obj_tech(request, obj_pack, obj_model):
    # массовая замена для tech доставки, хотлайн и лабела

    dict_models ={
    'monitors': Monitors.objects.all(),
    'km': KM.objects.all(),
    'keyboards': Keyboards.objects.all(),
    'mouses': Mouses.objects.all(),
    'pads': Pads.objects.all(),
    'headsets': Headsets.objects.all(),
    'webcams': Webcams.objects.all(),
    'wifis': WiFis.objects.all(),
    'acoustics': Acoustics.objects.all(),
    'tables': Tables.objects.all(),
    'chairs': Chairs.objects.all(),
    'accessories': Accessories.objects.all(),
    'cabelsplus': Cabelsplus.objects.all(),
    'filters': Filters.objects.all(),
    'others': Others.objects.all(),
    }

    form = SinglePackFewForm()

    context = {
                'form': form,
                'obj_pack': obj_pack,
              }
#
    if request.method == 'POST':
        form = SinglePackFewForm(request.POST)
        if form.is_valid():
            obj_pk = [int(c) for c in obj_pack.split(',')]
            objs = dict_models[obj_model].filter(pk__in=obj_pk)

            hotline = form.cleaned_data['hotline']
            delivery = form.cleaned_data['delivery']
            label_ = form.cleaned_data['label_']
            creditoff = form.cleaned_data['creditoff']
            only_thing = form.cleaned_data['only_thing']

            if only_thing == 'hotline':
                count_objs = objs.update(
                hotline=hotline
                )
                thing = hotline
            elif only_thing == 'delivery':
                count_objs = objs.update(
                delivery=delivery
                )
                thing = delivery
            elif only_thing == 'creditoff':
                count_objs = objs.update(
                creditoff=creditoff
                )
                thing = creditoff
            else:
                label_ = label_ if label_ else None
                count_objs = objs.update(
                label=label_
                )
                thing = label_

            messages.success(
            request,
            f"In {count_objs} {obj_model} was update : {only_thing}: {thing}")
            return  HttpResponseRedirect(
                                        reverse(
                                        f'admin:tech_{obj_model}_changelist'
                                        )
                                        )

    return render(request, 'money/admin_test.html', context)

def do_full_path(data_set):
    # добавляет в пути фото1,2,3 полный путь

    for ser in data_set:
        try:
            ser['cover1'] = 'http://versum.site:5222' + ser['cover1']
        except:
            pass
        try:
            ser['cover2'] = 'http://versum.site:5222' + ser['cover2']
        except:
            pass
        try:
            ser['cover3'] = 'http://versum.site:5222' + ser['cover3']
        except:
            pass

    return data_set


class distrib_tech(APIView):
    def get(self, request):
        #usd = USD.objects.last().usd
        Dict_full = {}
        monitors = Monitors.objects.filter(is_active=True, groups__isnull=True)
        serializer = MonitorsSer(monitors, many=True)
        Dict_full['monitors'] = do_full_path(serializer.data)
        km = KM.objects.filter(is_active=True, groups__isnull=True)
        serializer = KMSer(km, many=True)
        Dict_full['km'] = do_full_path(serializer.data)
        kb = Keyboards.objects.filter(is_active=True, groups__isnull=True)
        serializer = KeyboardsSer(kb, many=True)
        Dict_full['kb'] = do_full_path(serializer.data)
        mouse = Mouses.objects.filter(is_active=True, groups__isnull=True)
        serializer = MousesSer(mouse, many=True)
        Dict_full['mouse'] = do_full_path(serializer.data)
        pads = Pads.objects.filter(is_active=True, groups__isnull=True)
        serializer = PadsSer(pads, many=True)
        Dict_full['pads'] = do_full_path(serializer.data)
        headsets = Headsets.objects.filter(is_active=True, groups__isnull=True)
        serializer = HeadsetsSer(headsets, many=True)
        Dict_full['headsets'] = do_full_path(serializer.data)
        web = Webcams.objects.filter(is_active=True, groups__isnull=True)
        serializer = WebcamsSer(web, many=True)
        Dict_full['web'] = do_full_path(serializer.data)
        wifi = WiFis.objects.filter(is_active=True, groups__isnull=True)
        serializer = WiFisSer(wifi, many=True)
        Dict_full['wifi'] = do_full_path(serializer.data)
        acoustics = Acoustics.objects.filter(is_active=True, groups__isnull=True)
        serializer = AcousticsSer(acoustics, many=True)
        Dict_full['acoustics'] = do_full_path(serializer.data)
        tables = Tables.objects.filter(is_active=True, groups__isnull=True)
        serializer = TablesSer(tables, many=True)
        Dict_full['tables'] = do_full_path(serializer.data)
        chairs = Chairs.objects.filter(is_active=True, groups__isnull=True)
        serializer = ChairsSer(chairs, many=True)
        Dict_full['chairs'] = do_full_path(serializer.data)
        access = Accessories.objects.filter(is_active=True, groups__isnull=True)
        serializer = AccessoriesSer(access, many=True)
        Dict_full['access'] = do_full_path(serializer.data)
        cab = Cabelsplus.objects.filter(is_active=True, groups__isnull=True)
        serializer = CabelsplusSer(cab, many=True)
        Dict_full['cab'] = do_full_path(serializer.data)
        filters = Filters.objects.filter(is_active=True, groups__isnull=True)
        serializer = FiltersSer(filters, many=True)
        Dict_full['filters'] = do_full_path(serializer.data)
        other = Others.objects.filter(is_active=True, groups__isnull=True)
        serializer = OthersSer(other, many=True)
        Dict_full['other'] = do_full_path(serializer.data)
        return Response({"parts": Dict_full})
