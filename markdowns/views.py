from .models import *
from rest_framework.response import Response
from django.shortcuts import render,redirect
from django.urls import reverse
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework import serializers
from .serializers import *

def admin_rentability_chg(request, test_pk):

    from django.forms import ModelForm
    from django import forms

    class ShortSearchForm(ModelForm):
        class Meta:
            model = Mark_computers
            fields = ['rentability']
            labels = {'rentability': 'Наценка'}

    #form = ShortForm()
    form_hand = ShortSearchForm()

    context = {
                #'form': form,
                'form_hand': form_hand,
                'test_pk': test_pk,
              }

    if request.method == 'GET':
        messages.info(request,'Введите новую наценку')

    if request.method == 'POST':
        test_pk_ = test_pk.split(',')
        form_hand = ShortSearchForm(request.POST)
        if form_hand.is_valid():

            #from load_form_providers.load_element import get_distrib2

            rentability_ = form_hand.cleaned_data['rentability']
            comps = Mark_computers.objects.filter(pk__in=test_pk_)

            try:
                comps_ = Mark_computers.objects.update(rentability=rentability_)
            except:
                messages.error(request,f"Не удалось: {rentability_}")
                return  HttpResponseRedirect(
                                            reverse('admin:markdowns_mark_computers_changelist')
                                            )
            messages.success(
            request,
            f"В { ','.join(str(pk.name_computers) for pk in comps)} изменена наценка: {rentability_}"
            )

            return  HttpResponseRedirect(
                                        reverse('admin:markdowns_mark_computers_changelist')
                                        )

    return render(request, 'money/admin_test.html', context)

class mark_comps_parts(APIView):
    def get(self, request):

        Dict_full = dict()
        Dict_full_tradein = dict()
        Dict_full_main = {'pc': None, 'part': None, 'tradein': None}

        shorts_ok = Mark_short.objects.filter(trade_in=True)

        comps =Mark_computers.objects.filter(is_active=True)
        comps_ok = comps.filter(
        price_computers__isnull=False, mb__isnull=False,
        cpu__isnull=False, ram__isnull=False,
        gpu__isnull=False, hdd__isnull=False,
        ssd__isnull=False,
        psu__isnull=False, case__isnull=False,
        cooler__isnull=False, fan__isnull=False,
        wifi__isnull=False, cables__isnull=False,
        soft__isnull=False,
        )

        #serializer = Mark_shortSerializer(shorts_ok, many=True)
        #Dict_full_main['tradein'] = serializer.data

        serializer = CompsSerializer(comps_ok, many=True)
        Dict_full_main['pc'] = serializer.data

        # ниже for part
        cool = Cooler.objects.filter(
        is_active=True, mark_short__only_comp=False).exclude(name='пусто')
        serializer = CoolerSerializer(cool, many=True)
        Dict_full['cooler'] = serializer.data
        cpu = CPU.objects.filter(
        is_active=True, mark_short__only_comp=False).exclude(name='пусто')
        serializer = CpuSerializer(cpu, many=True)
        Dict_full['cpu'] = serializer.data
        mb = MB.objects.filter(
        is_active=True, mark_short__only_comp=False).exclude(name='пусто')
        serializer = MbSerializer(mb, many=True)
        Dict_full['mb'] = serializer.data
        ram = RAM.objects.filter(
        is_active=True, mark_short__only_comp=False)
        serializer = RamSerializer(ram, many=True)
        Dict_full['ram'] = serializer.data
        hdd = HDD.objects.filter(
        is_active=True, mark_short__only_comp=False).exclude(name='пусто')
        serializer = HddSerializer(hdd, many=True)
        Dict_full['hdd'] = serializer.data
        psu = PSU.objects.filter(
        is_active=True, mark_short__only_comp=False).exclude(name='пусто')
        serializer = PsuSerializer(psu, many=True)
        Dict_full['psu'] = serializer.data
        gpu = GPU.objects.filter(
        is_active=True, mark_short__only_comp=False).exclude(name='пусто')
        serializer = GpuSerializer(gpu, many=True)
        Dict_full['gpu'] = serializer.data
        fan = FAN.objects.filter(
        is_active=True, mark_short__only_comp=False).exclude(name='пусто')
        serializer = FanSerializer(fan, many=True)
        Dict_full['fan'] = serializer.data
        case = CASE.objects.filter(
        is_active=True, mark_short__only_comp=False).exclude(name='пусто')
        serializer = CaseSerializer(case, many=True)
        Dict_full['case'] = serializer.data
        ssd = SSD.objects.filter(
        is_active=True, mark_short__only_comp=False).exclude(name='пусто')
        serializer = SsdSerializer(ssd, many=True)
        Dict_full['ssd'] = serializer.data
        wifi = WiFi.objects.filter(
        is_active=True, mark_short__only_comp=False).exclude(name='пусто')
        serializer = WiFiSerializer(wifi, many=True)
        Dict_full['wifi'] = serializer.data
        cables = Cables.objects.filter(
        is_active=True, mark_short__only_comp=False).exclude(name='пусто')
        serializer = CablesSerializer(cables, many=True)
        Dict_full['cables'] = serializer.data
        soft = Soft.objects.filter(
        is_active=True, mark_short__only_comp=False).exclude(name='пусто')
        serializer = SoftSerializer(soft, many=True)
        Dict_full['soft'] = serializer.data

        Dict_full_main['part']=Dict_full

        # ниже for tradein
        cool_ = shorts_ok.filter(
        kind2=True, kind='cool').exclude(name_parts='пусто')
        serializer = Mark_shortSerializer(cool_, many=True)
        Dict_full_tradein['cooler'] = serializer.data
        cpu_ = shorts_ok.filter(
        kind2=True, kind__in=('aproc', 'iproc')).exclude(name_parts='пусто')
        serializer = Mark_shortSerializer(cpu_, many=True)
        Dict_full_tradein['cpu'] = serializer.data
        mb_ = shorts_ok.filter(
        kind2=True, kind__in=('amb', 'imb')).exclude(name_parts='пусто')
        serializer = Mark_shortSerializer(mb_, many=True)
        Dict_full_tradein['mb'] = serializer.data
        ram_ = shorts_ok.filter(
        kind2=True, kind='mem')
        serializer = Mark_shortSerializer(ram_, many=True)
        Dict_full_tradein['ram'] = serializer.data
        hdd_ = shorts_ok.filter(
        kind2=True, kind='hdd').exclude(name_parts='пусто')
        serializer = Mark_shortSerializer(hdd_, many=True)
        Dict_full_tradein['hdd'] = serializer.data
        psu_ = shorts_ok.filter(
        kind2=True, kind='ps').exclude(name_parts='пусто')
        serializer = Mark_shortSerializer(psu_, many=True)
        Dict_full_tradein['psu'] = serializer.data
        gpu_ = shorts_ok.filter(
        kind2=True, kind='video').exclude(name_parts='пусто')
        serializer = Mark_shortSerializer(gpu_, many=True)
        Dict_full_tradein['gpu'] = serializer.data
        fan_ = shorts_ok.filter(
        kind2=True, kind='vent').exclude(name_parts='пусто')
        serializer = Mark_shortSerializer(fan_, many=True)
        Dict_full_tradein['fan'] = serializer.data
        case_ = shorts_ok.filter(
        kind2=True, kind='case').exclude(name_parts='пусто')
        serializer = Mark_shortSerializer(case_, many=True)
        Dict_full_tradein['case'] = serializer.data
        ssd_ = shorts_ok.filter(
        kind2=True, kind='ssd').exclude(name_parts='пусто')
        serializer = Mark_shortSerializer(ssd_, many=True)
        Dict_full_tradein['ssd'] = serializer.data
        wifi_ = shorts_ok.filter(
        kind2=True, kind='wifi').exclude(name_parts='пусто')
        serializer = Mark_shortSerializer(wifi_, many=True)
        Dict_full_tradein['wifi'] = serializer.data
        cables_ = shorts_ok.filter(
        kind2=True, kind='cables').exclude(name_parts='пусто')
        serializer = Mark_shortSerializer(cables_, many=True)
        Dict_full_tradein['cables'] = serializer.data
        soft_ = shorts_ok.filter(
        kind2=True, kind='soft').exclude(name_parts='пусто')
        serializer = Mark_shortSerializer(soft_, many=True)
        Dict_full_tradein['soft'] = serializer.data

        Dict_full_main['tradein']=Dict_full_tradein

        return Response(Dict_full_main)

class mark_parts(APIView):
    def get(self, request):
        #usd = USD.objects.last().usd
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
        wifi = WiFi.objects.filter(is_active=True)
        serializer = WiFiSerializer(wifi, many=True)
        Dict_full['wifi'] = serializer.data
        cables = Cables.objects.filter(is_active=True)
        serializer = CablesSerializer(cables, many=True)
        Dict_full['cables'] = serializer.data
        soft = Soft.objects.filter(is_active=True)
        serializer = SoftSerializer(soft, many=True)
        Dict_full['soft'] = serializer.data
        return Response({"part": Dict_full})
