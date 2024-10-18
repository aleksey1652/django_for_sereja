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
from .forms import RentabilityForm, SinglePackFewForm, AutoForm, IsActiveForm
# upload_edit_foto APIKEY change_few_things_obj change_auto_obj

def change_rentability_obj(request, obj_pack, obj_model):
    # массовая замена для синглс наценки

    dict_models ={
    'cooler_other': Cooler_OTHER.objects.all(),
    'cpu_other': CPU_OTHER.objects.all(),
    'mb_other': MB_OTHER.objects.all(),
    'ram_other': RAM_OTHER.objects.all(),
    'hdd_other': HDD_OTHER.objects.all(),
    'psu_other': PSU_OTHER.objects.all(),
    'gpu_other': GPU_OTHER.objects.all(),
    'fan_other': FAN_OTHER.objects.all(),
    'case_other': CASE_OTHER.objects.all(),
    'ssd_other': SSD_OTHER.objects.all(),
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
                                        f'admin:singleparts_{obj_model}_changelist'
                                        )
                                        )

    return render(request, 'money/admin_test.html', context)

def change_is_active_obj(request, obj_pack, obj_model):
    # массовая замена для синглс is_active

    dict_models ={
    'cooler_other': Cooler_OTHER.objects.all(),
    'cpu_other': CPU_OTHER.objects.all(),
    'mb_other': MB_OTHER.objects.all(),
    'ram_other': RAM_OTHER.objects.all(),
    'hdd_other': HDD_OTHER.objects.all(),
    'psu_other': PSU_OTHER.objects.all(),
    'gpu_other': GPU_OTHER.objects.all(),
    'fan_other': FAN_OTHER.objects.all(),
    'case_other': CASE_OTHER.objects.all(),
    'ssd_other': SSD_OTHER.objects.all(),
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
                                        f'admin:singleparts_{obj_model}_changelist'
                                        )
                                        )

    return render(request, 'money/admin_test.html', context)

def change_auto_obj(request, obj_pack, obj_model):
    # массовая замена для синглс ручной цены

    dict_models ={
    'cooler_other': Cooler_OTHER.objects.all(),
    'cpu_other': CPU_OTHER.objects.all(),
    'mb_other': MB_OTHER.objects.all(),
    'ram_other': RAM_OTHER.objects.all(),
    'hdd_other': HDD_OTHER.objects.all(),
    'psu_other': PSU_OTHER.objects.all(),
    'gpu_other': GPU_OTHER.objects.all(),
    'fan_other': FAN_OTHER.objects.all(),
    'case_other': CASE_OTHER.objects.all(),
    'ssd_other': SSD_OTHER.objects.all(),
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
                                        f'admin:singleparts_{obj_model}_changelist'
                                        )
                                        )

    return render(request, 'money/admin_test.html', context)

def change_few_things_obj(request, obj_pack, obj_model):
    # массовая замена для синглс доставки, хотлайн и лабела

    dict_models ={
    'cooler_other': Cooler_OTHER.objects.all(),
    'cpu_other': CPU_OTHER.objects.all(),
    'mb_other': MB_OTHER.objects.all(),
    'ram_other': RAM_OTHER.objects.all(),
    'hdd_other': HDD_OTHER.objects.all(),
    'psu_other': PSU_OTHER.objects.all(),
    'gpu_other': GPU_OTHER.objects.all(),
    'fan_other': FAN_OTHER.objects.all(),
    'case_other': CASE_OTHER.objects.all(),
    'ssd_other': SSD_OTHER.objects.all(),
    }

    form = SinglePackFewForm()

    context = {
                'form': form,
                'obj_pack': obj_pack,
              }

    if request.method == 'POST':
        form = SinglePackFewForm(request.POST)
        if form.is_valid():
            obj_pk = [int(c) for c in obj_pack.split(',')]
            #comps = Computers.objects.filter(pk__in=comps_pk)
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
                                        f'admin:singleparts_{obj_model}_changelist'
                                        )
                                        )

    return render(request, 'money/admin_test.html', context)

def escape_filename(filename):
    invalid_chars = r' \/:*?"<>|'  # Список запрещенных символов
    replacement_char = '_'  # Символ для замены

    for char in invalid_chars:
        filename = filename.replace(char, replacement_char)

    return filename

def rename_file(obj):
    # переимен файла по образцу (вынужденная доработка)
    string = str(obj.cover1)
    mask = re.sub(r'.+--', '', string).strip()
    try:
        os.rename(f'/usr/src/sereja/media/{string}', f'/usr/src/sereja/media/{mask}')
    except FileNotFoundError:
        return obj
    obj.cover1 = mask
    obj.save()

def loop_rename(tuple_obj):
    # for all obj переимен файла по образцу (вынужденная доработка)
    """tuple_obj = (
                'CPU_OTHER.objects(is_active=True)',
                'Cooler_OTHER.objects(is_active=True)',
                )"""
    for query in tuple_obj:
        query_from_eval = eval(query)
        for obj in query_from_eval:
            rename_file(obj)

def do_category():
    # для добавления категорий в модели(1разовая функция)
    SSD_OTHER.objects.all().update(category_ru='Накопитель', category_ua='Накопичувач')
    HDD_OTHER.objects.all().update(category_ru='Накопитель', category_ua='Накопичувач')
    Cooler_OTHER.objects.all().update(category_ru='Кулер процессорный',
    category_ua='Кулер процесорний')
    CPU_OTHER.objects.all().update(category_ru='Процессор', category_ua='Процесор')
    MB_OTHER.objects.all().update(category_ru='Материнская плата',
    category_ua='Материнська плата')
    RAM_OTHER.objects.all().update(category_ru='Модуль памяти',
    category_ua="Модуль пам'яті")
    PSU_OTHER.objects.all().update(category_ru='Блок питания',
    category_ua='Блок живлення')
    GPU_OTHER.objects.all().update(category_ru='Видеокарта', category_ua='Відеокарта')
    FAN_OTHER.objects.all().update(category_ru='Вентилятор', category_ua='Вентилятор')
    CASE_OTHER.objects.all().update(category_ru='Корпус', category_ua='Корпус')

    for obj in HDD_OTHER.objects.all():
        obj.name = re.sub(r'Накопитель', '', obj.name).strip()
        obj.save()



def upload_edit_foto(obj, apikey, url='https://www.cutout.pro/api/v1/matting?mattingType=6',
apikey_='APIKEY', file_='file', data_={'preview': True}, obj_cover=1):
    # https://api.remove.bg/v1.0/removebg
    # по ссылке в obj.cover1 скачиваем - редактируем, записывем в папку, в obj.cover1 - ссылку

    if obj_cover == 2:
        foto_from_obj = obj.cover2
    elif obj_cover == 3:
        foto_from_obj = obj.cover3
    else:
        foto_from_obj = obj.cover1
    #name_ = obj.name
    part_number_ = obj.part_number
    name_foto_row = f'{part_number_}_{obj_cover}.png'
    name_foto = escape_filename(name_foto_row)
    try:
        response = requests.get(str(foto_from_obj))
    except:
        return False

    if response.status_code == 200:
        with open('/usr/src/sereja/media/foto_dc.png', 'wb') as f:
            f.write(response.content)

    response_sdk = requests.post(
    url,
    headers={apikey_: apikey},
    files={file_: open('/usr/src/sereja/media/foto_dc.png', 'rb')},
    data = data_
    )

    if response_sdk.status_code == 200:

        with open(f'/usr/src/sereja/media/{name_foto}', 'wb') as f:
            f.write(response_sdk.content)

        if obj_cover == 2:
            obj.cover2 = name_foto
        elif obj_cover == 3:
            obj.cover3 = name_foto
        else:
            obj.cover1 = name_foto
        #obj.cover1 = name_foto
        obj.save()
        return True



"""class MediaUploadView(APIView):
    def post(self, request, format=None):
        serializer = MediaSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.validated_data['file']
            # Добавьте здесь вашу логику обработки файла
            # Например, сохраните файл на сервере или обновите запись в базе данных
            with open('media/photoroom-result-medium.png', 'wb') as f:
                f.write(file)

            CASE_OTHER.objects.create(name='test_case', part_number='test_case_',
            price_rent=100, r_price=100, price_ua=100, price_usd=100,
            case_color_ua='-', case_color_ru='-', cover1='media/photoroom-result-medium.png')
            return Response({'status': 'success'})
        else:
            return Response(serializer.errors, status=400)"""

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


class versum_single_parts(APIView):
    def get(self, request):
        #usd = USD.objects.last().usd
        Dict_full = {}
        cool = Cooler_OTHER.objects.filter(is_active=True, groups__isnull=True)
        serializer = CoolerSer(cool, many=True)
        Dict_full['cooler'] = do_full_path(serializer.data)
        cpu = CPU_OTHER.objects.filter(is_active=True, groups__isnull=True)
        serializer = CPUSer(cpu, many=True)
        Dict_full['cpu'] = do_full_path(serializer.data)
        mb = MB_OTHER.objects.filter(is_active=True, groups__isnull=True)
        serializer = MBSer(mb, many=True)
        Dict_full['mb'] = do_full_path(serializer.data)
        ram = RAM_OTHER.objects.filter(is_active=True, groups__isnull=True)
        serializer = RAMSer(ram, many=True)
        Dict_full['ram'] = do_full_path(serializer.data)
        hdd = HDD_OTHER.objects.filter(is_active=True, groups__isnull=True)
        serializer = HDDSer(hdd, many=True)
        Dict_full['hdd'] = do_full_path(serializer.data)
        psu = PSU_OTHER.objects.filter(is_active=True, groups__isnull=True)
        serializer = PSUSer(psu, many=True)
        Dict_full['psu'] = do_full_path(serializer.data)
        gpu = GPU_OTHER.objects.filter(is_active=True, groups__isnull=True)
        serializer = GPUSer(gpu, many=True)
        Dict_full['gpu'] = do_full_path(serializer.data)
        fan = FAN_OTHER.objects.filter(is_active=True, groups__isnull=True)
        serializer = FANSer(fan, many=True)
        Dict_full['fan'] = do_full_path(serializer.data)
        case = CASE_OTHER.objects.filter(is_active=True, groups__isnull=True)
        serializer = CASESer(case, many=True)
        Dict_full['case'] = do_full_path(serializer.data)
        ssd = SSD_OTHER.objects.filter(is_active=True, groups__isnull=True)
        serializer = SSDSer(ssd, many=True)
        Dict_full['ssd'] = do_full_path(serializer.data)
        #wifi = WiFi_OTHER.objects.filter(is_active=True, groups__isnull=True)
        #serializer = WiFiSer(wifi, many=True)
        Dict_full['wifi'] = []
        #cables = Cables_OTHER.objects.filter(is_active=True, groups__isnull=True)
        #serializer = CablesSer(cables, many=True)
        Dict_full['cables'] = []
        #soft = Soft_OTHER.objects.filter(is_active=True, groups__isnull=True)
        #serializer = SoftSer(soft, many=True)
        Dict_full['soft'] = []
        return Response({"parts": Dict_full})

def dop_foto(foto_url, part_number_, apikey='989508c456bf4e018c6322dffe0385d3',
obj_cover = 1):
    # вынужденная ручная гет-фото по урл-фото с инета

    result = False
    data_={'preview': True}
    file_='file'
    apikey_='APIKEY'
    url='https://www.cutout.pro/api/v1/matting?mattingType=6'
    name_foto_row = f'{part_number_}_{obj_cover}.png'
    name_foto = escape_filename(name_foto_row)
    foto_from_obj = foto_url
    response = requests.get(str(foto_from_obj))

    if response.status_code == 200:
        with open('media/foto_dc.png', 'wb') as f:
            f.write(response.content)

    response_sdk = requests.post(
    url,
    headers={apikey_: apikey},
    files={file_: open('media/foto_dc.png', 'rb')},
    data = data_
    )

    if response_sdk.status_code == 200:
        with open(f'media/{name_foto}', 'wb') as f:
            f.write(response_sdk.content)
        result = True

    return result
