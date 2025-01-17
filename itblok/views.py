from django.shortcuts import render
from django.utils import timezone
from django.contrib import messages
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from django.db.models import F, Q, Value, Func, FloatField, ExpressionWrapper
from django.db.models.functions import Coalesce, Concat, Round
from rest_framework.response import Response
from rest_framework.views import APIView

import re, json


from .models import *
from cat.models import Parts_short as short
from cat.models import USD
from cat.forms import ComputersForm
from cat.forms_admin_comps import Form_num_vent, Form_text_input
from singleparts.forms import labelsForm
from .serializers import ITSer



def it_margin_exch(request, it_pk):
    # массовое изм наценки для Itblok компов, используется в админке action: set_margin
    usd = USD.objects.last().usd

    comps_pk = it_pk.split(',')
    form = ComputersForm(initial={'warranty_computers': usd, 'class_computers': 20})

    context = {
                'form': form,
                'it_pk': it_pk,
              }

    if request.method == 'POST':
        comps_pk = it_pk.split(',')
        form = ComputersForm(request.POST)
        if form.is_valid():
            margin = form.cleaned_data['class_computers']
            margin = round(margin, 2)
            exch = form.cleaned_data['warranty_computers']

            comp = ItblokComputers.objects.filter(pk__in=comps_pk)

            comp.update(rentability=margin)
            messages.success(
            request,f'В {comp.first()}  наценка: {margin}, курс: {exch}')
            return  HttpResponseRedirect(
                                        reverse(f'admin:itblok_itblokcomputers_changelist')
                                        )

    return render(request, 'money/admin_test.html', context)


def edit_it_num_fan(request, comp_pack):
    # массовое изм кол вент для Itblok компов, используется в админке action:
    # edit_parts_num_admin

    form = Form_num_vent()

    context = {
               'form': form,
               'comp_pack': comp_pack
              }

    if request.method == 'POST':
        form = Form_num_vent(request.POST)
        if form.is_valid():
            num_vent = form.cleaned_data['num']
        else:
            num_vent = '1'


        comps_pk = [int(c) for c in comp_pack.split(',')]
        comps = ItblokComputers.objects.filter(pk__in=comps_pk)
        if num_vent == 'пусто':
            fan_parts, _ = short.objects.get_or_create(kind='vent', name_parts='пусто')
            count = comps.update(fan=fan_parts, vent_num_computers=1)
        else:
            count = comps.update(vent_num_computers=num_vent)
        messages.success(request,f"Изменены  {count} компов: вентиляторы: {num_vent}")
        return  HttpResponseRedirect(
                                    reverse(f'admin:itblok_itblokcomputers_changelist')
                                    )
        #return HttpResponse(f"{request.POST['kind']}")

    return render(request, 'admin/start_calc.html', context)


def change_label(request, obj_pack):
    # массовая замена ярлыков в компах

    form = labelsForm()

    context = {
                'form': form,
                'obj_pack': obj_pack,
              }

    if request.method == 'POST':
        form = labelsForm(request.POST)
        count_objs = 0
        if form.is_valid():
            obj_pk = [int(c) for c in obj_pack.split(',')]
            objs = ItblokComputers.objects.filter(pk__in=obj_pk)

            label_ = form.cleaned_data['label_']

            label_ = label_ if label_ else None
            if label_ is None:
                count_objs = objs.update(
                label=label_
                )

                messages.success(
                request,
                f"В группе компов ({count_objs}шт) поменяли ярлык на: пусто")
                return  HttpResponseRedirect(
                                            reverse(
                                            f'admin:itblok_itblokcomputers_changelist'
                                            )
                                            )

            count_objs += objs.exclude(Q(label="") | Q(label__isnull=True)
            ).exclude(label__icontains=label_
            ).update(
            label = Concat(F('label'), Value(f', {label_}'))
            )

            if objs.filter(Q(label="") | Q(label__isnull=True)).exists():
                count_objs += objs.filter(
                Q(label="") | Q(label__isnull=True)
                ).update(
                label=label_
                )

            messages.success(
            request,
            f"В группе компов ({count_objs}шт) добавили ярлык на: {label_}")
            return  HttpResponseRedirect(
                                        reverse(
                                        f'admin:itblok_itblokcomputers_changelist'
                                        )
                                        )

    return render(request, 'money/admin_test.html', context)


def edit_parts_pack(request, comp_pack):
    # массовое изм деталей(Parts_short) для itblok компов

    form = Form_text_input()

    context = {
               'form': form,
               'comp_pack': comp_pack
              }

    if request.method == 'POST':
        form = Form_text_input(request.POST)
        if form.is_valid():
            short_name = form.cleaned_data['new']
        else:
            short_name = 'noname'
        try:
            short_ = short.objects.get(name_parts=short_name, kind2=False)
            kind_ = short_.kind
        except:
            messages.error(request,f"Ошибка в детали:{short_name}")
            return  HttpResponseRedirect(
                                        reverse(f'admin:itblok_itblokcomputers_changelist')
                                        )

        comps_pk = [int(c) for c in comp_pack.split(',')]
        comps = ItblokComputers.objects.filter(pk__in=comps_pk)

        count = 0
        if kind_ in ('aproc', 'iproc',):
            count = comps.update(cpu=short_)
        if kind_ in ('amb', 'imb',):
            count = comps.update(mb=short_)
        if kind_ == 'cool':
            count = comps.update(cooler=short_)
        if kind_ == 'mem':
            count = comps.update(ram=short_)
        if kind_ == 'video':
            count = comps.update(gpu=short_)
        if kind_ == 'hdd':
            count = comps.update(hdd=short_)
        if kind_ == 'ssd':
            count = comps.update(ssd=short_)
        if kind_ == 'ps':
            count = comps.update(psu=short_)
        if kind_ == 'case':
            count = comps.update(case=short_)
        if kind_ == 'vent':
            count = comps.update(fan=short_)
        if kind_ == 'wifi':
            count = comps.update(wifi=short_)
        if kind_ == 'cables':
            count = comps.update(cables=short_)
        if kind_ == 'soft':
            count = comps.update(soft=short_)

        messages.success(request,f"Изменены  {count} компов: {short_name}")
        return  HttpResponseRedirect(
                                    reverse(f'admin:itblok_itblokcomputers_changelist')
                                    )
        #return HttpResponse(f"{request.POST['kind']}")

    return render(request, 'admin/start_calc.html', context)


class ItComps(APIView):
    def get(self, request):
        # Аннотация с округлением до целых
        comps = ItblokComputers.objects.filter(is_active=True).annotate(
            price_parts_new=Round(
                ExpressionWrapper(
                    (1 + (Coalesce(F('rentability'), Value(0)) / 100)) * (
                        Coalesce(F('fan__x_code'), Value(0)) * F('vent_num_computers') +
                        Coalesce(F('ram__x_code'), Value(0)) * F('mem_num_computers') +
                        Coalesce(F('cpu__x_code'), Value(0)) +
                        Coalesce(F('cooler__x_code'), Value(0)) +
                        Coalesce(F('mb__x_code'), Value(0)) +
                        Coalesce(F('gpu__x_code'), Value(0)) +
                        Coalesce(F('hdd__x_code'), Value(0)) +
                        Coalesce(F('ssd__x_code'), Value(0)) +
                        Coalesce(F('psu__x_code'), Value(0)) +
                        Coalesce(F('case__x_code'), Value(0)) +
                        Coalesce(F('wifi__x_code'), Value(0)) +
                        Coalesce(F('cables__x_code'), Value(0)) +
                        Coalesce(F('soft__x_code'), Value(0))
                    ),
                    output_field=FloatField()
                )
            )
        )

        # Сериализация данных
        serializer = ITSer(comps, many=True)
        return Response(serializer.data)
