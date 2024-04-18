from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponseRedirect,HttpResponse
import json
from money.models import *
from cat.models import *
from cat.forms import *
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from money.service import *
from load_form_providers.load_element import  to_article2_1
from django.contrib.auth.decorators import login_required, permission_required
from money.forms import *
from money.onec_transforms import yes_div_per_man, plan_stavka
from cat.forms_admin_comps import *
from cat.calc_comp import get_comp_parts, catch_to_calc_forms, calc_comp_context, message_block, start_to_calc,calc_to_view
from django.contrib import messages
from django.db.models import Sum, Count, F, Min
from django.views import generic
from django.urls import reverse
import re
import math
from money.salary import *
from money.onec_transforms_advance import StatsRules
#promotions_admin_edit x_code catch_to_admin_forms admin_test catch_to_calc_forms webhook Офис ПК витрина 2% ПК_витрина catch_to_admin_forms admin_margin_exch admin_special_price
#Gross_profit Expense admin_test promotions_admin_edit change_assembly cash_rate_already


def catch_to_admin_shorts(request, comp_pk):
    # в окне ред компа: ручное добавление детали 
    form = Form_text_input(request.POST)
    if form.is_valid():
        short_name = form.cleaned_data['new']
    comp = Computers.objects.get(pk=comp_pk)
    try:
        short = Parts_short.objects.get(name_parts=short_name, kind2=False)
        kind_ = short.kind
    except:
        messages.error(request,f"Ошибка в детали:{short_name}")
        return  HttpResponseRedirect(
                                    reverse(f'admin:cat_computers_change',
                                    args=(comp_pk,))
                                    )

    if kind_ in ('ssd', 'hdd'):
        comp.hdd_computers = f'пусто;{short_name}'
        comp.save()
    elif kind_ in ('aproc', 'iproc', 'amb', 'imb'):
        comp.__dict__[kind_[1:] + '_computers'] = short_name
        comp.save()
    else:
        comp.__dict__[kind_ + '_computers'] = short_name
        comp.save()

    messages.success(request,f"In {comp.name_computers} was update:{short_name}")
    return  HttpResponseRedirect(
                                reverse(f'admin:cat_computers_change',
                                args=(comp_pk,))
                                )

class BidsDetailView(generic.DetailView):
    model = Bids

def change_assembly(request, comp_pk):
    #from cat.models import Computers, Pc_assembly, Sites
    #from cat.forms_admin_comps import Pc_assemblyForm

    comp = Computers.objects.get(pk=comp_pk)

    name_ass = Pc_assembly.objects.filter(
    sites__name_sites='versum').values_list('name_assembly',flat=True).distinct()
    CHOISE_name_ass = set([(short, short) for short in name_ass])

    kind_ass = Pc_assembly.objects.filter(
    sites__name_sites='versum').values_list('kind_assembly',flat=True).distinct()
    CHOISE_kind_ass = set([(short, short) for short in kind_ass])

    form = Pc_assemblyForm(initial={'name_assembly': comp.pc_assembly.name_assembly,
                            'kind_assembly': comp.pc_assembly.kind_assembly,
                            })

    form.base_fields['kind_assembly'].choices = CHOISE_kind_ass
    form.base_fields['name_assembly'].choices = CHOISE_name_ass

    context = {
                'form': form,
                'comp_pk': comp_pk,
              }

    if request.method == 'POST':
        form = Pc_assemblyForm(request.POST)
        if form.is_valid():
            name_ass = form.cleaned_data['name_assembly']
            kind_ass = form.cleaned_data['kind_assembly']
            #sites_ass = form.cleaned_data['sites']
            sites_ = Sites.objects.get(name_sites='versum')
            assembly,_ = Pc_assembly.objects.get_or_create(name_assembly=name_ass,
            kind_assembly=kind_ass, sites=sites_)
            comp.pc_assembly = assembly
            comp.save()
            messages.success(request,f"In {comp.name_computers} was update series:{kind_ass}, group:{name_ass}")
            return  HttpResponseRedirect(
                                        reverse(f'admin:cat_computers_change',
                                        args=(comp.pk,))
                                        )

    return render(request, 'money/admin_test.html', context)

def change_comp_name(request, comp_pk):
    # метод для переименование компа

    comp = Computers.objects.get(pk=comp_pk)


    form = CompSearchForm(initial={'name_computers': comp.name_computers})

    context = {
                'form': form,
                'comp_pk': comp_pk,
              }

    if request.method == 'POST':
        form = CompSearchForm(request.POST)
        if form.is_valid():
            name_comp = form.cleaned_data['name_computers']

            comp.name_computers = name_comp
            comp.save()
            messages.success(request,f"Новое имя компа {name_comp}")
            return  HttpResponseRedirect(
                                        reverse(f'admin:cat_computers_change',
                                        args=(comp.pk,))
                                        )

    return render(request, 'money/admin_test.html', context)

def activate_change_comp(request, comp_pk):
    #from cat.models import Computers, Promotion
    comp = Computers.objects.get(pk=comp_pk)
    if comp.is_active:
        comp.is_active = False
        comp.save()
        messages.success(request,f"{comp.name_computers} в резерв")
    else:
        comp.is_active = True
        comp.save()
        messages.success(request,f"{comp.name_computers} вновь активирован")

    return  HttpResponseRedirect(
                                reverse(f'admin:cat_computers_change',
                                args=(comp.pk,))
                                )

def promotions_admin_edit(request, comp_pk, prom_pk):
    #from cat.models import Computers, Promotion
    if prom_pk and comp_pk:
        prom = Promotion.objects.get(pk=prom_pk)
        comp = Computers.objects.get(pk=comp_pk)
        comp.promotion_set.remove(prom)
        messages.success(request,f"{comp.name_computers} was deleted promotion:{prom}")
        return  HttpResponseRedirect(
                                    reverse(f'admin:cat_computers_change',
                                    args=(comp.pk,))
                                    )
    from cat.forms_admin_comps import Form_promotion

    form = Form_promotion()
    try:
        promotion = Promotion.objects.all().values_list('prom',flat=True)
        CHOISE_promotion = [(short, short) for short in promotion]
    except:
        CHOISE_promotion = [('AMD', 'AMD')]
    key_ = list(form.fields.keys())[0]
    form.base_fields[key_].choices = CHOISE_promotion

    context = {
                'form': form,
                'comp_pk': comp_pk,
              }
    if request.method == 'POST':
        form = Form_promotion(request.POST)
        if form.is_valid():
            promotion = form.cleaned_data['promotion']
            prom = Promotion.objects.get(prom=promotion)
            comp = Computers.objects.get(pk=comp_pk)
            comp.promotion_set.add(prom)
            messages.success(request,f"In {comp.name_computers} was add promotion:{prom}")

            #comp.promotion_set.add(prom)
            messages.success(request,f"{comp.name_computers} was add promotion:{prom}")
            return  HttpResponseRedirect(
                                        reverse(f'admin:cat_computers_change',
                                        args=(comp.pk,))
                                        )

    return render(request, 'money/admin_test.html', context)

def admin_margin_exch(request, test_pk):
    #from cat.forms import ComputersForm
    #from cat.models import Computers, USD admin_test
    usd = USD.objects.last().usd

    comps_pk = test_pk.split(',')
    form = ComputersForm(initial={'warranty_computers': usd})

    context = {
                'form': form,
                'test_pk': test_pk,
              }

    if request.method == 'POST':
        comps_pk = test_pk.split(',')
        form = ComputersForm(request.POST)
        if form.is_valid():
            margin = form.cleaned_data['class_computers']
            margin = round(margin, 2)
            exch = form.cleaned_data['warranty_computers']

            comp = Computers.objects.filter(pk__in=comps_pk)

            if comp.first().pc_assembly.kind_assembly == 'Other':
                comp.update(class_computers=margin, warranty_computers=exch)
                messages.success(
                request,f'В {comp.first()}  наценка: {margin}, курс: {exch}')
                return  HttpResponseRedirect(
                                            reverse('calc_to_view',
                                            kwargs={'comp_pk':test_pk}
                                            )
                                            )
            else:
                comp.update(class_computers=margin)
                messages.success(request,f'В выбранных компах наценка теперь: {margin}')
            return  HttpResponseRedirect(
                                        reverse('admin:cat_computers_changelist')
                                        )

    return render(request, 'money/admin_test.html', context)

def admin_special_price(request, test_pk):
    usd, margin_default = USD.objects.last().usd, USD.objects.last().margin
    margin_default = margin_default if margin_default else 1

    comps_pk = test_pk.split(',')
    form = ComputersSpecialPrice(initial={
    'warranty_computers': 0,
    'class_computers': margin_default,
    'exch': usd,
    })

    context = {
                'form': form,
                'test_pk': test_pk,
              }

    if request.method == 'POST':
        comps_pk = test_pk.split(',')
        form = ComputersSpecialPrice(request.POST)
        if form.is_valid():
            margin = form.cleaned_data['class_computers']
            special_price = form.cleaned_data['warranty_computers']
            exch = form.cleaned_data['exch']
            try:
                special_price = float(special_price)
            except:
                messages.error(request,f'Спеццена должна быть числом')

                return  HttpResponseRedirect(
                                            reverse('admin:cat_computers_changelist')
                                            )

            #sp_to_bd = round(special_price * margin * exch)
            sp_to_bd = round(special_price) # поменяли алгоритм

            comp = Computers.objects.filter(pk__in=comps_pk)
            comp.update(warranty_computers=sp_to_bd)
            messages.success(request,f'В выбранных компах спеццена теперь: {sp_to_bd}')

            return  HttpResponseRedirect(
                                        reverse('admin:cat_computers_changelist')
                                        )

    return render(request, 'money/admin_test.html', context)

def admin_change(request, test_pk):
    #from cat.forms import ComputersForm_advanced, Pc_assemblyForm_advanced
    #from cat.models import Computers, Pc_assembly

    model_, _ = test_pk.split(',')[-1], test_pk.split(',')[:-1]
    if model_ == 'Computers':
        form = ComputersForm_advanced()
    else:
        form = Pc_assemblyForm_advanced()

    context = {
                'form': form,
                'test_pk': test_pk,
              }

    if request.method == 'POST':
        model_, test_pk = test_pk.split(',')[-1], test_pk.split(',')[:-1]
        form = ComputersForm_advanced(request.POST) if model_== 'Computers' else Pc_assemblyForm_advanced(request.POST)
        if form.is_valid():
            if model_ == 'Computers':
                you_vid = form.cleaned_data['you_vid']
                perm_conf = form.cleaned_data['perm_conf']
                elite_conf = form.cleaned_data['elite_conf']

                comp = Computers.objects.filter(pk__in=test_pk)
                comp.update(you_vid=you_vid, perm_conf=perm_conf, elite_conf=elite_conf)

                comp_full = ','.join(str(c.name_computers) for c in comp)
                messages.success(request,f'In {model_} :{comp_full} ---  was changed you_vid, perm_conf, elite_conf')
                return  HttpResponseRedirect(
                                            reverse('admin:cat_computers_changelist')
                                            )
            else:
                desc_ru = form.cleaned_data['desc_ru']
                desc_ukr = form.cleaned_data['desc_ukr']

                assembly = Pc_assembly.objects.filter(pk__in=test_pk)
                assembly_first = assembly.first()
                assembly.update(desc_ru=desc_ru,desc_ukr=desc_ukr)

                assembly_full = ','.join(str(c.name_assembly) for c in assembly)
                messages.success(request,f'In {assembly_first.kind_assembly} :{assembly_full} ---  was changed desc_ru, desc_ukr')
                return  HttpResponseRedirect(
                                            reverse('admin:cat_pc_assembly_changelist')
                                            )

    return render(request, 'money/admin_test.html', context)

def admin_delete_relate(request, test_pk):

    from django.forms import ModelForm
    from django import forms

    """_ = test_pk.split(',')
    kind = Parts_short.objects.filter(pk__in=_).first().kind
    full_ = Parts_full.objects.filter(kind=kind,providers__name_provider='-').values_list('name_parts',
    'providerprice_parts', 'availability_parts')
    CHOISE = [
    ('---'.join(
    [str(f) for f in full]
    ), '---'.join([str(f) for f in full])) for full in full_ if full[2] in ('yes', 'hand')
    ]"""

    """class ShortForm(forms.Form):
        short = forms.ChoiceField(
            choices=CHOISE,
            label='Parts_full'
        )"""

    class ShortSearchForm(ModelForm):
        class Meta:
            model = Parts_short
            fields = ['name_parts']
            labels = {'name_parts': 'Ручной подбор по партнамберу'}

    #form = ShortForm()
    form_hand = ShortSearchForm()

    context = {
                #'form': form,
                'form_hand': form_hand,
                'test_pk': test_pk,
              }

    if request.method == 'GET':
        messages.info(request,'Выберите партнамбер для удаления')

    if request.method == 'POST':
        model_, test_pk_ = test_pk.split(',')[-1], test_pk.split(',')[:-1]
        form_hand = ShortSearchForm(request.POST)
        if form_hand.is_valid():

            #from load_form_providers.load_element import get_distrib2

            name = form_hand.cleaned_data['name_parts'].strip()
            short = Parts_short.objects.filter(pk__in=test_pk_)

            try:
                full = Parts_full.objects.get(partnumber_parts=name,providers__name_provider='-')
            except:
                messages.error(request,f"Не удалось найти:{name}")
                return  HttpResponseRedirect(
                                            reverse('admin:cat_parts_short_changelist')
                                            )
            for sh in short:
                sh.parts_full.remove(full)
                sh_full = sh.parts_full.filter(
                availability_parts='yes').exclude(providerprice_parts=0
                ).order_by('providerprice_parts').first()
                if sh_full:
                    if sh.auto == False:
                        # меняет цену только при выключенной ручной цене
                        sh.x_code = sh_full.providerprice_parts
                        sh.date_chg = timezone.now()
                sh.save()
            messages.success(
            request,f"В { ','.join(str(pk.name_parts) for pk in short)} удален: {full.name_parts}"
            )

            return  HttpResponseRedirect(
                                        reverse('admin:cat_parts_short_changelist')
                                        )

    return render(request, 'money/admin_test.html', context)


def admin_test(request, test_pk):
    #from cat.forms import PfullForm_kind
    #from cat.models import Parts_full, Articles, Parts_short
    from django.forms import ModelForm

    model_, _ = test_pk.split(',')[-1], test_pk.split(',')[:-1]
    if model_.find('Parts_short') != -1:
        from django import forms
        kind = Parts_short.objects.filter(pk__in=_).first().kind
        full_ = Parts_full.objects.filter(kind=kind,providers__name_provider='-').values_list('name_parts',
        'providerprice_parts', 'availability_parts')
        CHOISE = [('---'.join([str(f) for f in full]), '---'.join([str(f) for f in full])) for full in full_ if full[2] in ('yes', 'hand')]

        class ShortForm(forms.Form):
            short = forms.ChoiceField(
                choices=CHOISE,
                label='Parts_full'
            )

        class ShortSearchForm(ModelForm):
            class Meta:
                model = Parts_short
                fields = ['name_parts']
                labels = {'name_parts': 'Ручной подбор по партнамберу'}

        form = ShortForm()
        form_hand = ShortSearchForm()

    else:
        form = PfullForm_kind()

    context = {
                'form': form,
                'form_hand': form_hand,
                'test_pk': test_pk,
              }
    if request.method == 'POST':
        model_, test_pk = test_pk.split(',')[-1], test_pk.split(',')[:-1]
        form = ShortForm(request.POST) if model_.find('Parts_short') != -1 else PfullForm_kind(request.POST)
        form_hand = ShortSearchForm(request.POST)
        if form_hand.is_valid():

            #from load_form_providers.load_element import get_distrib2

            name = form_hand.cleaned_data['name_parts'].strip()
            short = Parts_short.objects.filter(pk__in=test_pk)

            try:
                full = Parts_full.objects.get(partnumber_parts=name,providers__name_provider='-')
            except:
                if model_ == 'Parts_short':
                    messages.error(request,f"Не удалось подключить:{name}")
                    return  HttpResponseRedirect(
                                                reverse('admin:cat_parts_short_changelist')
                                                )
                else:
                    try:
                        pk_ = int(re.findall(r'\d+',model_)[0])
                    except:
                        messages.error(request,f"Не удалось подключить:{name}")
                        return  HttpResponseRedirect(
                                                    reverse(f'admin:cat_computers_changelist')
                                                    )
                    return  HttpResponseRedirect(
                                                reverse(f'admin:cat_computers_change',
                                                args=(pk_,))
                                                )
            for sh in short:
                if not Parts_short.objects.filter(kind2=False, parts_full__partnumber_parts=full.partnumber_parts).exists():
                    #sh.parts_full.clear()
                    sh.parts_full.add(full)
                    sh_full = sh.parts_full.filter(
                    availability_parts='yes').exclude(providerprice_parts=0
                    ).order_by('providerprice_parts').first()
                    if sh_full:
                        if sh.auto == False:
                            # меняет цену только при выключенной ручной цене
                            sh.x_code = sh_full.providerprice_parts
                            sh.date_chg = timezone.now()
                            sh.save()
                else:
                    messages.error(request,f"This partnumber is exists: {full.partnumber_parts}")
                #get_distrib2(full.kind, full.partnumber_parts, se=sh.name_parts)
            messages.success(request,f"In { ','.join(str(pk.name_parts) for pk in short)} :{full.name_parts}")
            if model_ == 'Parts_short':
                return  HttpResponseRedirect(
                                            reverse('admin:cat_parts_short_changelist')
                                            )
            else:
                try:
                    pk_ = int(re.findall(r'\d+',model_)[0])
                except:
                    messages.error(request,f"In {model_}")
                    return  HttpResponseRedirect(
                                                reverse(f'admin:cat_computers_changelist')
                                                )
                return  HttpResponseRedirect(
                                            reverse(f'admin:cat_computers_change',
                                            args=(pk_,))
                                            )
        if form.is_valid():
            try:
                kind = form.cleaned_data['kind']
            except:
                kind = form.cleaned_data['short']
            if model_ == 'Parts_full':
                full = Parts_full.objects.filter(pk__in=test_pk)
                full.update(kind=kind)
                test_full = ','.join(str(pk.name_parts) for pk in full)
                messages.success(request,f'In {model_} :{test_full} --- kind was changed, now: {kind} ')
                return  HttpResponseRedirect(
                                            reverse('admin:cat_parts_full_changelist')
                                            )
            if model_ == 'Articles':
                full = Articles.objects.filter(pk__in=test_pk)
                full.update(kind=kind)
                test_full = ','.join(str(pk.item_name) for pk in full)
                messages.success(request,f'In {model_} :{test_full} --- kind was changed, now: {kind} ')
                return  HttpResponseRedirect(
                                            reverse('admin:cat_articles_changelist')
                                            )
            if model_.find('Parts_short') != -1:

                #from load_form_providers.load_element import get_distrib2

                short = Parts_short.objects.filter(pk__in=test_pk)
                name = kind.split('---')[0]

                full = Parts_full.objects.get(name_parts=name,providers__name_provider='-')
                for sh in short:
                    #sh.parts_full.clear()
                    sh.parts_full.add(full)
                    sh_full = sh.parts_full.filter(
                    availability_parts='yes').exclude(providerprice_parts=0
                    ).order_by('providerprice_parts').first()
                    if sh_full:
                        if sh.auto == False:
                            # меняет цену только при выключенной ручной цене
                            sh.x_code = sh_full.providerprice_parts
                            sh.date_chg = timezone.now()
                            sh.save()
                    #get_distrib2(full.kind, full.partnumber_parts, se=sh.name_parts)
                messages.success(request,f"In { ','.join(str(pk.name_parts) for pk in short)} :{full.name_parts}")
                if model_ == 'Parts_short':
                    return  HttpResponseRedirect(
                                                reverse('admin:cat_parts_short_changelist')
                                                )
                else:
                    try:
                        pk_ = int(re.findall(r'\d+',model_)[0])
                    except:
                        messages.error(request,f"In {model_}")
                        return  HttpResponseRedirect(
                                                    reverse(f'admin:cat_computers_changelist')
                                                    )
                    return  HttpResponseRedirect(
                                                reverse(f'admin:cat_computers_change',
                                                args=(pk_,))
                                                )

            #return HttpResponse(f"full: {test_full}, kind: {kind}")
        return render(request, 'money/admin_test.html', context)
    return render(request, 'money/admin_test.html', context)
    #return HttpResponse(f"{test_pk}")

def get_discr_for_admin(request, test_pk):

    from load_form_providers.load_element import dict_kind_to_discr, dict_kind_to_discr_kind, get_distrib2
    from descriptions.models import Cooler,CPU,MB,RAM,HDD,PSU,GPU,FAN,CASE,SSD,WiFi,Cables,Soft
    from pars.ecatalog import get_by_filter, get_dict, get_url_parts, get_discr_ecatalog, get_res_ecatalog, dict_kind_id, dict_kind_key, dict_form, dict_base, dict_v3, mem_edition, mem_create,cpu_edition, cpu_create, cooler_edition, cooler_create, mb_create, mb_edition, hdd_create, hdd_edition, ssd_create, ssd_edition, gpu_create, gpu_edition, fan_create, fan_edition, psu_create, psu_edition, case_create, case_edition

    model_, short_pk = test_pk.split(',')[-1], test_pk.split(',')[0]
    short = Parts_short.objects.get(pk=short_pk)
    pfull = short.parts_full.order_by(
    'providerprice_parts').first()
    try:
        comp_pk = int(re.findall(r'\d+',model_)[0])
    except:
        messages.error(request,f"Error In {model_}")
        return  HttpResponseRedirect(
                                    reverse(f'admin:cat_computers_changelist')
                                    )
    if not pfull:
        messages.error(request,f"In {short.name_parts} not related")
        return  HttpResponseRedirect(
                                    reverse(f'admin:cat_computers_change',
                                    args=(comp_pk,))
                                    )
    art = pfull.partnumber_parts

    if eval(dict_kind_to_discr[pfull.kind]).exists():
        some_obj = eval(dict_kind_to_discr[pfull.kind])
        if some_obj.filter(name=short.name_parts).exists():
            discr_obj = some_obj.filter(name=short.name_parts).first()
            discr_obj.is_active = True
            discr_obj.save()
        else:
            some_obj = eval(dict_kind_to_discr[pfull.kind])
            some_obj = some_obj.first()
            some_obj.name = short.name_parts
            some_obj.is_active = True
            some_obj.save()
        messages.success(request, f'{short.name_parts} with {art} is exist in discr and active')
    else:
        kind_ = dict_kind_to_discr_kind[pfull.kind]
        dict_for_db = get_res_ecatalog(art, kind_)
        if dict_for_db:
            dict_for_db['name'] = short.name_parts
            key_ = 'pc_parts'
            count_obj,obj_pk = eval(dict_kind_key[kind_])
            messages.success(request, f'Now {short.name_parts} with {art} upload and add to discr')
        else:
            messages.success(request, f"Sorry not exist in ecatalog {art}")
    get_distrib2(pfull.kind, pfull.partnumber_parts, se=short.name_parts)

    return  HttpResponseRedirect(
                                reverse(f'admin:cat_computers_change',
                                args=(comp_pk,))
                                )

def catch_to_admin_forms(request, what,short_name):
    #from cat.models import Computers, CompPrice, Parts_short

    comp = Computers.objects.get(pk=int(short_name))
    if comp.pc_assembly.sites.name_sites == 'art':
        try:
            comp_price = comp.compprice
        except:
            comp_price = CompPrice(name_computers=comp.name_computers, computers=comp)
            comp_price.save()
        if what == 'hdd_computers':
            parts = request.POST['hdd_ssd']
        elif what == 'hdd2_computers':
            parts = request.POST['hdd_ssd2']
        elif what in ('proc_computers', 'mem_computers', 'video_computers'):
            parts = request.POST[what[:-10]]
            short = Parts_short.objects.filter(name_parts=parts).select_related('parts_full')
            if short.values_list('parts_full__providerprice_parts', flat=True).exists():
                comp_price.__dict__[what] = short.values_list('parts_full__providerprice_parts', flat=True).first()
                #comp_price.__dict__[what] = parts
                comp_price.save()
            messages.success(request,f"{comp.name_computers} was no update,but price update(this parts are need in filter):{parts}")
            return  HttpResponseRedirect(
                                        reverse(f'admin:cat_computers_change',
                                        args=(comp.pk,)))
        else:
            parts = request.POST[what[:-10]]
        short = Parts_short.objects.filter(name_parts=parts).select_related('parts_full')
        if short.values_list('parts_full__providerprice_parts', flat=True).exists():
            comp_price.__dict__[what] = short.values_list('parts_full__providerprice_parts', flat=True).first()
            #comp_price.__dict__[what] = parts
            comp_price.save()


    if what == 'hdd_computers':
        parts = request.POST['hdd_ssd']
        temp = comp.hdd_computers.split(';')
        temp[0] = parts
        comp.hdd_computers = ';'.join(temp)
        comp.save()
    elif what == 'hdd2_computers':
        parts = request.POST['hdd_ssd2']
        temp = comp.hdd_computers.split(';')
        try:
            temp[1] = parts
        except:
            temp.append(parts)
        comp.hdd_computers = ';'.join(temp)
        comp.save()
    else:
        parts = request.POST[what[:-10]]
        comp.__dict__[what] = parts
        comp.save()
    if comp.pc_assembly.kind_assembly == 'Other':
        messages.success(request,f"В {what} добавлено: {parts}")
        return  HttpResponseRedirect(
                                    reverse('calc_to_view',
                                    kwargs={'comp_pk':short_name}
                                    )
                                    )
    messages.success(request,f"{comp.name_computers} was update:{parts}")
    return  HttpResponseRedirect(
                                reverse(f'admin:cat_computers_change',
                                args=(comp.pk,))
                                )

def catch_to_admin_forms_num(request, what,short_name):
    #from cat.models import Computers

    num_dict = {'video_computers': 'video_num_computers', 'vent_computers': 'vent_num_computers',
    'mem_computers': 'mem_num_computers'}

    comp = Computers.objects.get(pk=int(short_name))
    try:
        if what == 'video_computers':
            num = request.POST['video_num']
        elif what == 'vent_computers':
            num = request.POST['vent_num']
        elif what == 'mem_computers':
            num = request.POST['mem_num']
        comp.__dict__[num_dict[what]] = num
        comp.save()
    except:
        if comp.pc_assembly.kind_assembly == 'Other':
            return  HttpResponseRedirect(
                                        reverse('calc_to_view',
                                        kwargs={'comp_pk':int(short_name)}
                                        )
                                        )
        return  HttpResponseRedirect(
                                    reverse(f'admin:cat_computers_change',
                                    args=(comp.pk,))
                                    )

    messages.success(request,f"{comp.name_computers} was update:{num_dict[what]}---{num}")
    if comp.pc_assembly.kind_assembly == 'Other':
        return  HttpResponseRedirect(
                                    reverse('calc_to_view',
                                    kwargs={'comp_pk':int(short_name)}
                                    )
                                    )
    return  HttpResponseRedirect(
                                reverse(f'admin:cat_computers_change',
                                args=(comp.pk,))
                                )

def del_servise(request, serv_pk):
    pk_, serv_ = serv_pk.split('-')
    if serv_ == 'st':
        serv = Statistics_service.objects.get(pk=int(pk_))
        serv.delete()
        messages.success(request,f"{serv}-запись удалена")
    else:
        serv = Expense.objects.get(pk=int(pk_))
        nalog_back = serv.discr
        try:
            how = round(float(re.findall(r'\): (\d+)',nalog_back)[0]) / 0.3)
        except:
            how = 0
        serv_year = Expense.objects.filter(discr='Налог на прибыль').last()
        serv_year.amount -= how
        serv_year.save()
        serv.delete()
        messages.success(request,f"{serv}-запись удалена, налог на прибыль годовой - {how}")
    return  HttpResponseRedirect(
                                reverse('family')
                                )

def salary(team,my):
    w1, w2 = 160, 0
    try:
        team, my = float(team), float(my)
    except:
        team, my = 0, 0
    if team and my and (team + my) != 0:
        w2 = (my * w1)/(team + my)
        w1 = w1 - 2 * w2

    return (f'{round(w1)}px', f'{round(w2)}px')

def service_stats_per_period(m, service_set, month, year):
    dict_context = dict()
    sal = Salary(month, year)
    service_kind = ('Ремонт ПК', 'Обслуживание')
    count = 0
    rate = 0

    if m.sborsik:
        try:
            rate = Service.objects.filter(kind='Сборка').first().cash_rate
        except:
            rate = 0
    if m.remontnik:
        try:
            rate = Service.objects.filter(kind='Ремонт ПК').first().cash_rate
        except:
            rate = 0

    if service_set:
        for stat in service_set.values('service__kind',
        'service__sloznostPK', 'sborka_count', 'date', 'service__summa', 'pk'):
            if stat['service__kind'] == 'Сборка':
                dict_context[f"Сборка (компьютер {stat['service__sloznostPK']}, {stat['date'].strftime('%m:%Y--%H:%M')})"] = {'st':(stat['sborka_count'], stat['service__summa']), 'st_pk': f"{stat['pk']}-st"}
                count += stat['sborka_count'] * stat['service__summa']
    if m.remontnik:
        all_serve = Service.objects.filter(kind__in=('Обслуживание',
        'Ремонт ПК')).values('kind', 'sloznostPK', 'summa')
        dict_context['Тарифы'] = [{f"{k['kind']}-{k['sloznostPK']}": k['summa']} for k in list(all_serve)]
        for stat in service_set.values('service__kind', 'service__sloznostPK',
        'remont_count', 'date', 'service__summa', 'pk'):
            if stat['service__kind'] == 'Ремонт ПК':
                dict_context[f"{stat['service__kind']} (компьютер {stat['service__sloznostPK']}, {stat['date'].strftime('%m:%Y--%H:%M')})"] = {'st': (stat['remont_count'], stat['service__summa']), 'st_pk': f"{stat['pk']}-st"}
                count += stat['remont_count'] * stat['service__summa']
        for stat in service_set.values('service__kind', 'service__sloznostPK','obsluj_count',
        'date', 'service__summa', 'pk'):
            if stat['service__kind'] == 'Обслуживание':
                dict_context[f"{stat['service__kind']} (компьютер {stat['service__sloznostPK']}, {stat['date'].strftime('%m:%Y--%H:%M')})"] = {'st': (stat['obsluj_count'], stat['service__summa']), 'st_pk': f"{stat['pk']}-st"}
                count += stat['obsluj_count'] * stat['service__summa']
    stavka = sal.plan_stavka()
    stavka_service = round(rate * stavka['Процент_ставка'], 1)
    dict_context['Версум_план'] = stavka['Версум_план']
    dict_context['Версум_план_минимум'] = stavka['Версум_план_минимум']
    dict_context['Айтиблок_план'] = stavka['Айтиблок_план']
    dict_context['Айтиблок_план_минимум'] = stavka['Айтиблок_план_минимум']
    dict_context['Версум_оборот'] = stavka['Версум_оборот']
    dict_context['Айтиблок_оборот'] = stavka['Айтиблок_оборот']
    dict_context['Процент_ставка'] = stavka['Процент_ставка']
    dict_context['Ставка:'] = stavka_service
    dict_context['Итого:'] = {'st': count + stavka_service} if count + stavka_service else {'st': '0'}
    #dict_context['Уже получил'] = {'st': m.cash_rate_already} if m.cash_rate_already else {'st': '0'}
    man_cash_rate_already = sal.st_cash_rate_already(m)
    dict_context['Уже получил'] = {'st': man_cash_rate_already} if man_cash_rate_already else {'st': '0'}
    return dict_context

def manager_stats_per_period(m, bids_set, month, year, s=('versum', 'komputeritblok')):
    #site_ = 'versum' if m.site == 'versum' else 'komputeritblok'
    sal = Salary(month, year)
    dict_context = dict()
    if m.super:
        dict_salary = sal.salary_super(plan_stavka_=True, no_stavka=False)
    else:
        dict_salary = sal.salary_manager(m)
    bids_status = (
    'Відвантажено', 'Підтверджено', 'Діалог триває',
    'Чекаємо на оплату', 'Замовлення товару',
    'В черзі на збірку', 'Успішно виконаний'
    )
    bids_kind = ('Системный блок', 'Комплектующие')
    dict_context['Все'] = bids_set.distinct().count()
    for status_ in bids_status:
        if status_ == 'Отказ':

            summa_otkaz = bids_set.filter(
            status='Отказ').distinct().select_related('goods').annotate(num=F('goods__amount'),
            suma=F('goods__summa')).aggregate(Total=Sum(F('num')*F('suma')))['Total']

            count_otkaz = bids_set.filter(status=status_).distinct().count()

            dict_context[status_] = (count_otkaz, summa_otkaz)
        else:
            dict_context[status_] = bids_set.filter(status=status_).distinct().count()

    """for kind_ in bids_kind:
        dict_context[kind_] = bids_set.filter(status='Выкуплен',
        goods__kind=kind_).distinct().select_related('goods').annotate(num=F('goods__amount'),
        suma=F('goods__summa')).aggregate(Total=Sum(F('num')*F('suma')))['Total']"""

    #warning: for all kind
    from_office = bids_set.filter(status='Успішно виконаний',
    istocnikZakaza='ПК вітрина 2%').distinct()
    offise_list = list(from_office.values_list('ID', flat=True))
    from_office_sum = from_office.select_related('goods').annotate(num=F('goods__amount'),
    suma=F('goods__summa')).aggregate(Total=Sum(F('num')*F('suma')))['Total']
    from_office_sum = from_office_sum if from_office_sum else 0
    dict_context['ПК_витрина'] = from_office_sum
    dict_context['Заявки ПК_витрина'] = offise_list

    dicr_res = {**dict_context, **dict_salary}
    if not m.super:
        dicr_res['ЗП'] += f", Итого: {dict_salary['sum']}"

    return dicr_res

    for kind_ in bids_kind:
        if m.site == 'both':
            dict_context['team ' + kind_] = Bids.objects.filter(date_ch__month=month,date_ch__year=year,
            site__in=('versum', 'komputeritblok'), status='Успішно виконаний',
            goods__kind=kind_).distinct().select_related('goods').annotate(num=F('goods__amount'),
            suma=F('goods__summa')).aggregate(Total=Sum(F('num')*F('suma')))['Total']
        else:
            dict_context['team ' + kind_] = bids_set.filter(managers__site=m.site, status='Успішно виконаний',
            goods__kind=kind_).distinct().select_related('goods').annotate(num=F('goods__amount'),
            suma=F('goods__summa')).aggregate(Total=Sum(F('num')*F('suma')))['Total']

        """Goods.objects.filter(bids__managers__family__groups__name='test_group',
        kind=kind_,bids__site=site_,bids__date_ch__month=month,
        bids__date_ch__year=year,bids__status='Выкуплен').distinct().annotate(num=F('amount'),
        suma=F('summa')).aggregate(Total=Sum(F('num')*F('suma')))['Total']"""

    plan_ = Plan.objects.filter(date__month=month, date__year=year, site=m.site)
    plan_now = plan_.last().plan if plan_.exists() else 100000000
    yes = 0
    if dict_context['team ' + 'Системный блок']:
        man = Managers.objects.filter(family__groups__name='test_group')
        yes = sal.yes_div_per_man(m, plan_now)
    soft_bonus = Goods.objects.first().software_bonus
    comp = dict_context['Системный блок'] if dict_context['Системный блок'] else 0
    parts = dict_context['Комплектующие'] if dict_context['Комплектующие'] else 0
    #soft = dict_context['ПО'] if dict_context['ПО'] else 0
    super_pk = dict_context['team ' + 'Системный блок'] * 0.005 if dict_context['team ' + 'Системный блок'] else 0
    super_parts = dict_context['team ' + 'Комплектующие'] * 0.005 if dict_context['team ' + 'Комплектующие'] else 0
    #dict_context['Ставка'] = m.cash_rate
    if m.cash_rate:
        stavka = sal.plan_stavka()
        stavka_service = round(m.cash_rate * stavka['Процент_ставка'], 1)
        dict_context['Версум_план'] = stavka['Версум_план']
        dict_context['Версум_план_минимум'] = stavka['Версум_план_минимум']
        dict_context['Айтиблок_план'] = stavka['Айтиблок_план']
        dict_context['Айтиблок_план_минимум'] = stavka['Айтиблок_план_минимум']
        dict_context['Версум_оборот'] = stavka['Версум_оборот']
        dict_context['Айтиблок_оборот'] = stavka['Айтиблок_оборот']
        dict_context['Процент_ставка'] = stavka['Процент_ставка']
        dict_context['Ставка'] = stavka_service
        cash_rate = stavka_service
    else:
        dict_context['Ставка'] = 0
        cash_rate = 0
    dict_context['План'] = plan_now
    if not m.super:
        cash_sum = round(comp * (0.01 + yes) + parts * 0.01 + from_office_sum * 0.01 + cash_rate)
        dict_context['ЗП'] = f'Сис блоки: {comp} * (0.01 + {yes}), Компл: {parts} * 0.01, ПК_витрина: {from_office_sum} * 0.01, Ставка: {cash_rate}, Всего: {cash_sum}'
    else:
        cash_sum = round(super_pk + super_parts + cash_rate)
        dict_context['ЗП'] = f'Сис блоки {super_pk}: , Компл: {super_parts}, Ставка: {cash_rate}, Всего: {cash_sum}'

    #dict_context['Уже получил'] = m.cash_rate_already
    man_cash_rate_already = sal.st_cash_rate_already(m)
    dict_context['Уже получил'] = man_cash_rate_already

    dict_context['px'] = salary(team=dict_context['team Системный блок'],my=dict_context['Системный блок'])


    return dict_context

def personal_sklad(request, now, context):
    person = request.user
    dict_temp = dict()
    M = Managers.objects.get(family__pk=person.pk)
    month, year = now.strftime("%m"), now.strftime("%Y")

    sal = Salary(month, year)
    context['manager_stats_per_period'] = sal.salary_sklad(plan_stavka_=True, no_stavka=False)
    return context

    #dict_temp['Уже получил/а'] = M.cash_rate_already
    man_cash_rate_already = sal.st_cash_rate_already(M)
    dict_temp['Уже получил/а'] = man_cash_rate_already
    try:
        count_comp = Gross_profit.objects.get(date__month=month,date__year=year, site='both').quantity
    except:
        count_comp = 0
    service,_ = Service.objects.get_or_create(kind='Зав склада')
    tarif = service.summa
    stavka = service.cash_rate
    dict_temp['Ставка'] = M.cash_rate
    if count_comp * tarif  > stavka:
        dict_temp['ЗП'] = f'Ставка: {stavka} < Кол компов: {count_comp} * {tarif}, Итого: {count_comp * tarif}'
    else:
        dict_temp['ЗП'] = f'Ставка: {stavka} > Кол компов: {count_comp} * {tarif}, Итого: {stavka}'
    context['manager_stats_per_period'] = dict_temp

    return context

def personal_one_c(request, now, context, st_pk):
    person = request.user
    dict_temp = dict()
    count = 0
    M = Managers.objects.get(family__pk=person.pk)
    st_period = set([x.date.strftime("%m: %Y") for x in Statistics_service.objects.filter(managers=M)])
    st_period.add(now.strftime("%m: %Y"))
    month_ = int(now.strftime("%m")) - 1
    year = now.strftime("%Y")
    if month_ > 0:
        month_, year_ = str(month_), year
    else:
        month_, year_ = '12', str(int(year) - 1)
    st_period.add(f'{month_}: {year_}')
    context['st_period'] = st_period if st_pk else now.strftime("%m: %Y")
    if st_pk != 0:
        messages.warning(request,f'Период:{st_pk}')
        m_y = re.split(':',st_pk)
        try:
            month, year = m_y[0].strip(), m_y[1].strip()
        except:
            month, year = now.strftime("%m"), now.strftime("%Y")
    else:
        month, year = now.strftime("%m"), now.strftime("%Y")
        messages.warning(request,f'Период:{month}: {year}')

    form = One_C_Form()
    context['form_st'] = form
    if request.method == 'POST':
        form = One_C_Form(request.POST)
        if form.is_valid():
            service_sloznostPK = form.cleaned_data['service_sloznostPK']
            zayavka_count = form.cleaned_data['sborka_count']

            service,_ = Service.objects.get_or_create(sloznostPK=service_sloznostPK, kind='Оператор 1С')
            if Statistics_service.objects.filter(managers=M, service=service,
            date__month=month, date__year=year).exists():
                try:
                    st = Statistics_service.objects.get(managers=M, service=service,
                    date__month=month, date__year=year)
                except:
                    st = Statistics_service.objects.filter(managers=M, service=service,
                    date__month=month, date__year=year).last()
                st.sborka_count += zayavka_count
                st.date = now
                st.save()
            else:
                st = Statistics_service.objects.create(managers=M, service=service,
                sborka_count=zayavka_count, date=now)
            messages.warning(request,f'Период:{now.strftime("%m: %Y")}, {zayavka_count} добавлено, тариф: {service.summa}')

    sal = Salary(month, year)
    context['manager_stats_per_period'] = sal.salary_one_c(plan_stavka_=True, no_stavka=False)
    return context

    try:
        count_comp = Gross_profit.objects.get(date__month=month,date__year=year, site='both').quantity
    except:
        count_comp = 0
    service,_ = Service.objects.get_or_create(sloznostPK='простой',kind='Оператор 1С')
    stavka = service.cash_rate
    tarif = service.summa
    all_serve = Service.objects.filter(kind='Оператор 1С').values('sloznostPK', 'summa')

    stavka_ = sal.plan_stavka()
    dict_temp = stavka_
    dict_temp['Тарифы'] = [{k['sloznostPK']: k['summa']} for k in list(all_serve)]
    stavka_service = round(stavka * stavka_['Процент_ставка'], 1)
    dict_temp['Ставка'] = stavka_service
    #dict_temp['Уже получил'] = M.cash_rate_already
    man_cash_rate_already = sal.st_cash_rate_already(M)
    dict_temp['Уже получил'] = man_cash_rate_already

    service_set = Statistics_service.objects.filter(managers=M, date__month=month, date__year=year)

    for stat in service_set.values(
    'service__sloznostPK', 'sborka_count', 'date', 'service__summa', 'pk'):
        dict_temp[f"Добавлены/а заявки/а {stat['service__sloznostPK']}, {stat['date'].strftime('%m:%Y--%H:%M')} кол/тариф"] = {'st':(stat['sborka_count'], stat['service__summa']), 'st_pk': f"{stat['pk']}-st"}
        count += stat['sborka_count'] * stat['service__summa']

    dict_temp['Дополнительно добавленные'] = count
    summa = stavka_service + (count_comp * tarif) + count
    dict_temp['ЗП'] = f'Ставка: {stavka_service} + Кол компов: {count_comp} * {tarif} + {count}, Итого: {summa}'
    context['manager_stats_per_period'] = dict_temp

    return context

def personal_tovar(request, now, context):
    person = request.user
    dict_temp = dict()
    M = Managers.objects.get(family__pk=person.pk)
    month, year = now.strftime("%m"), now.strftime("%Y")

    sal = Salary(month, year)
    context['manager_stats_per_period'] = sal.salary_tovar(plan_stavka_=True, no_stavka=False)
    return context

    dict_temp['Ставка'] = M.cash_rate
    #dict_temp['Уже получил/а'] = M.cash_rate_already
    man_cash_rate_already = sal.st_cash_rate_already(M)
    dict_temp['Уже получил/а'] = man_cash_rate_already
    try:
        count_comp = Gross_profit.objects.get(date__month=month,date__year=year, site='both').quantity
    except:
        count_comp = 0
    service,_ = Service.objects.get_or_create(kind='Заказ товара')
    tarif = service.summa
    stavka = service.cash_rate
    if count_comp * tarif  > stavka:
        dict_temp['ЗП'] = f'Ставка: {stavka} < Кол компов: {count_comp} * {tarif}, Итого: {count_comp * tarif}'
    else:
        dict_temp['ЗП'] = f'Ставка: {stavka} > Кол компов: {count_comp} * {tarif}, Итого: {stavka}'
    context['manager_stats_per_period'] = dict_temp

    return context

def personal_glav_buh(request, now, context):
    person = request.user
    M = Managers.objects.get(family__pk=person.pk)
    dict_temp = dict()
    month, year = now.strftime("%m"), now.strftime("%Y")
    form = Form_glav_buh()
    context['form_st'] = form
    #dict_temp['Ставка'] = M.cash_rate
    #dict_temp['Уже получил/а'] = M.cash_rate_already
    sal = Salary(month, year)
    dict_temp = sal.salary_glav_buh(plan_stavka_=True, no_stavka=False)

    if request.method == 'POST':
        form = Form_glav_buh(request.POST)
        if form.is_valid():
            bids_type = form.cleaned_data['bids_type']
            bids_id = form.cleaned_data['bids_id']
            dohod = form.cleaned_data['dohod']
            zatrati = form.cleaned_data['zatrati']
            #pribil = form.cleaned_data['pribil']
            #nalog_na_pribil = form.cleaned_data['nalog_na_pribil']
            #nds = form.cleaned_data['nds']
            #chistaja_pribil = form.cleaned_data['chistaja_pribil']
            pribil = dohod - zatrati
            if pribil >= 0:
                pribil_ = math.ceil(pribil)

                ratio_, _ = Ratios.objects.get_or_create()
                nalog_na_pribil = math.ceil(pribil * ratio_.tax_ratio * 0.3)

                nds = math.ceil(pribil * 0.2)
                sum_two_nalog = nds + nalog_na_pribil

                try:
                    bids = Bids.objects.get(ID=bids_id)
                    bids_date = bids.date_ch
                    month, year = bids_date.strftime("%m"), bids_date.strftime("%Y")
                    bids_type_ = bids.site
                    bids_type_ = 'itblok' if bids_type_ == 'komputeritblok' else 'versum'
                except:
                    bids_type_ = bids_type
                    bids_date = now

                discr_ = f"ID: {bids_id}, тип заявки: {bids_type_}, доход: {dohod}, затраты: {zatrati}, прибыль: {pribil_}, налог на пр(30%): {nalog_na_pribil}, НДС: {nds}"

                gr,_ = Expense_groups.objects.get_or_create(name='НДС')
                exp = Expense.objects.create(date=bids_date, site=bids_type_, discr=discr_, amount=sum_two_nalog,
                expense_groups=gr)
                if Expense.objects.filter(date__year=year, site='both', discr='Налог на прибыль',
                is_active=False).exists():
                    try:
                        exp_nalog_na_pribil = Expense.objects.get(date__year=year, site='both',
                        discr='Налог на прибыль', is_active=False)
                    except:
                        exp_nalog_na_pribil = Expense.objects.filter(date__year=year,
                        site='both', discr='Налог на прибыль', is_active=False).last()
                    exp_nalog_na_pribil.amount += nalog_na_pribil
                    exp_nalog_na_pribil.date = now
                    exp_nalog_na_pribil.save()
                else:
                    exp_nalog_na_pribil = Expense.objects.create(site='both',
                    discr='Налог на прибыль', amount=nalog_na_pribil, is_active=False, expense_groups=gr)
                messages.warning(request,f'Добавлено: {discr_}, За этот год Налог на прибыль: {exp_nalog_na_pribil.amount}')
            else:
                messages.warning(request,f'Неверно: прибыль: {pribil}')
    dict_expense = Expense.objects.filter(date__month=month, date__year=year, expense_groups__name='НДС')
    for k in dict_expense.values('date', 'discr', 'pk'):
        dict_temp[k['discr']] = {'st': k['date'].strftime("%d") + ':' + k['date'].strftime("%m"),
        'st_pk': f"{k['pk']}-exp"}
    context['manager_stats_per_period'] = dict_temp

    return context

def personal_kurier(request, now, context, st_pk):
    person = request.user
    M = Managers.objects.get(family__pk=person.pk)
    #context['Ставка'] = M.cash_rate
    #context['Уже получил'] = M.cash_rate_already
    date_for_stats = now
    month, year = now.strftime("%m"), now.strftime("%Y")
    month_before = int(month) - 1
    year_before = year
    if int(month) - 1 == 0:
        month_before, year_before = 12, int(year) - 1
    if month_before < 10:
        month_before = f'0{month_before}'
    form = KurierForm()
    context['form_st'] = form
    if request.method == 'POST':
        form = KurierForm(request.POST)
        if form.is_valid():
            if st_pk != 0:
                m_y = re.split(':',st_pk)
                month, year = m_y[0].strip(), m_y[1].strip() # для опред даты под стат
                #date_for_stats = Bids.objects.filter(
                #date_ch__month=month,date_ch__year=year).first().date_ch
            #km = form.cleaned_data['km']  km - старое обозн, сейчас номер заявки
            bids = form.cleaned_data['bids']
            summa = form.cleaned_data['summa']
            try:
                bid = Bids.objects.get(ID=bids,
                date_ch__month=now.strftime("%m"), date_ch__year=now.strftime("%Y"))
                bid.kurier_summa = summa
                bid.family = M.family
                bid.save()
                messages.warning(
                request,f'Добалено--период: {month}:{year}, заявка: {bids} = {summa}')
            except:
                #bid = Bids.objects.create(ID=bids, managers=M, status='Выкуплен',
                #family=M.family, kurier_summa=summa)
                messages.warning(
                request,f'Заявки {bids} за период: {now.strftime("%m")}:{now.strftime("%Y")} нету (Возможна запись только в тек период)')
            #service,_ = Service.objects.get_or_create(kind='Курьер')
            """if Statistics_service.objects.filter(managers=M, service=service,
            date__month=month, date__year=year).exists():
                try:
                    st = Statistics_service.objects.get(managers=M, service=service,
                    date__month=month, date__year=year)
                except:
                    st = Statistics_service.objects.filter(managers=M, service=service,
                    date__month=month, date__year=year).last()
                st_temp = st.km_count
                st_temp += km
                st.km_count = st_temp if st_temp > 0 else 0
                st.date = date_for_stats
                st.save()
            else:
                st = Statistics_service.objects.create(managers=M, service=service,
                km_count=km, date=date_for_stats)
            messages.warning(request,f'Период:{date_for_stats.strftime("%m: %Y")}, {km}km добавлено, всего км: {st.km_count}')"""
    st_period = set([x.date.strftime("%m: %Y") for x in Statistics_service.objects.filter(managers=M)])
    st_period.add(f"{month}: {year}")
    st_period.add(f"{month_before}: {year_before}")
    context['st_period'] = st_period
    if st_pk != 0:
        messages.warning(request,f'Период:{st_pk}')
        m_y = re.split(':',st_pk)
        try:
            month, year = m_y[0].strip(), m_y[1].strip()
        except:
            month, year = now.strftime("%m"), now.strftime("%Y")
        """try:
            Statistics_per_period = Statistics_service.objects.get(date__month=month,
            date__year=year, managers=M)
        except:
            Statistics_per_period = Statistics_service.objects.filter(date__month=month,
            date__year=year, managers=M).distinct().first()"""
    else:
        #now = timezone.now()
        month, year = now.strftime("%m"), now.strftime("%Y")
        messages.warning(request,f'Период:{month}:{year}')
        """try:
            Statistics_per_period = Statistics_service.objects.get(date__month=month,date__year=year,
            managers=M)
        except:
            Statistics_per_period = Statistics_service.objects.filter(date__month=month,
            date__year=year, managers=M).distinct().first()
    try:
        km = Statistics_per_period.km_count
    except:
        km = 0"""
    """service,_ = Service.objects.get_or_create(kind='Курьер')
    stavka = plan_stavka(M, month, year)
    service_stavka = round(service.cash_rate * stavka['Процент_ставка'], 1)
    dict_for_stats = {
                    'Версум_план': stavka['Версум_план'],
                    'Версум_план_минимум': stavka['Версум_план_минимум'],
                    'Айтиблок_план': stavka['Айтиблок_план'],
                    'Айтиблок_план_минимум': stavka['Айтиблок_план_минимум'],
                    'Версум_оборот': stavka['Версум_оборот'],
                    'Айтиблок_оборот': stavka['Айтиблок_оборот'],
                    'Процент_ставка': stavka['Процент_ставка'],
                    'дата': st_pk,
                    'km': km,
                    'ставка': service_stavka,
                    'ЗП': round(service_stavka + km * service.summa),
                    'Уже получил': M.cash_rate_already
                    }"""
    sal = Salary(month, year)
    context['manager_stats_per_period'] = sal.salary_kurier(plan_stavka_=True, no_stavka=False)

    #context['manager_stats_per_period'] = dict_for_stats
    context['bids_per_period'] = [] #must be clear!

    return context

def expense_marketplace(bids_id, bids_sum, site_, who):

    site_dict = {'komputeritblok': 'itblok', 'versum': 'versum', 'itblok': 'itblok'}

    if not Expense.objects.filter(discr__startswith=bids_id).exists():
        gr,_ = Expense_groups.objects.get_or_create(name='Маркетплейсы')
        Expense.objects.create(discr=f"{bids_id}---{who}---{site_}",expense_groups=gr,
        site=site_dict[site_], amount=bids_sum)
    else:
        exp_ = Expense.objects.filter(discr__startswith=bids_id).last()
        exp_.amount = bids_sum
        exp_.save()

@login_required
def Family(request,st_pk=0):
    now = timezone.now()
    u = request.user
    try:
        gr = u.groups.first().name
        name = Managers.objects.get(family__pk=u.pk).name
    except:
        gr, name = '', ''
    context = {
                'w2': '60px',
                'w1': '100px',
                'w3': '180px',
              }

    if u.groups.filter(name='glav_buh_group').exists():
        context = personal_glav_buh(request, now, context)

        return render(request, 'money/family.html', context)

    if u.groups.filter(name='kurier_group').exists():
        context = personal_kurier(request, now, context, st_pk)

        return render(request, 'money/family.html', context)

    if u.groups.filter(name='sklad_group').exists():
        context = personal_sklad(request, now, context)

        return render(request, 'money/family.html', context)

    if u.groups.filter(name='one_c_group').exists():
        context = personal_one_c(request, now, context, st_pk)

        return render(request, 'money/family.html', context)

    if u.groups.filter(name='tovar_group').exists():
        context = personal_tovar(request, now, context)

        return render(request, 'money/family.html', context)

    if gr == 'sborsik_group':
        M = Managers.objects.get(family__pk=u.pk)
        if M.remontnik:
            form_st = Statistics_serviceForm()
            context['form_st'] = form_st
            if request.method == 'POST':
                form_st = Statistics_serviceForm(request.POST)
                if form_st.is_valid():
                    service_sloznostPK = form_st.cleaned_data['service_sloznostPK']
                    obsluj_count_ = form_st.cleaned_data['obsluj_count']
                    service_kind = form_st.cleaned_data['service_kind']
                    service,_ = Service.objects.get_or_create(kind=service_kind, sloznostPK=service_sloznostPK)
                    #statistics_service_,_ = Statistics_service.objects.get_or_create(managers=M, service=service)
                    if service_kind == 'Обслуживание':
                        statistics_service_ = Statistics_service.objects.create(managers=M, service=service,
                        obsluj_count=obsluj_count_)
                    else:
                        statistics_service_ = Statistics_service.objects.create(managers=M, service=service,
                        remont_count=obsluj_count_)
                    #statistics_service_.obsluj_count += obsluj_count_
                    #statistics_service_.save()
                    messages.warning(request,f'{statistics_service_}; count: +{obsluj_count_}')
                    return  HttpResponseRedirect(
                                                reverse('family')
                                                )
        else:
            form_sb = Statistics_serviceForm_sborsik()
            context['form_sb'] = form_sb
            if request.method == 'POST':
                form_sb = Statistics_serviceForm_sborsik(request.POST)
                if form_sb.is_valid():
                    service_sloznostPK = form_sb.cleaned_data['service_sloznostPK']
                    sborka_count = form_sb.cleaned_data['sborka_count']
                    if service_sloznostPK == 'лед таблички':
                        service,_ = Service.objects.get_or_create(
                        kind='Установка лед табличек',
                        sloznostPK='простой')
                    else:
                        service,_ = Service.objects.get_or_create(kind='Сборка',
                        sloznostPK=service_sloznostPK)
                    #statistics_service_,_ = Statistics_service.objects.get_or_create(managers=M, service=service)
                    statistics_service_ = Statistics_service.objects.create(managers=M,
                    service=service,
                    sborka_count=sborka_count)
                    #statistics_service_.sborka_count += sborka_count
                    #statistics_service_.save()
                    messages.warning(request,f'{statistics_service_}; count: +{sborka_count}')
                    return  HttpResponseRedirect(
                                                reverse('family')
                                                )

        st_period = set(
        [x.date.strftime("%m: %Y") for x in Statistics_service.objects.filter(managers=M)]
        )
        context['st_period'] = st_period
        if st_pk != 0:
            messages.warning(request,f'Period:{st_pk}')
            m_y = re.split(':',st_pk)
            try:
                month, year = m_y[0].strip(), m_y[1].strip()
            except:
                month, year = now.strftime("%m"), now.strftime("%Y")
            Statistics_per_period = Statistics_service.objects.filter(
            date__month=month, date__year=year, managers=M).distinct()
        else:
            #now = timezone.now()
            month, year = now.strftime("%m"), now.strftime("%Y")
            Statistics_per_period = Statistics_service.objects.filter(date__month=month,date__year=year, managers=M).distinct()
        context['Statistics_per_period'] = Statistics_per_period
        context['bids_site'] = ('versum', 'komputeritblok')
        #context['manager_stats_per_period'] = service_stats_per_period(M, Statistics_per_period, month, year)
        sal = Salary(month, year)
        context['manager_stats_per_period'] = sal.salary_service_man(
        M, plan_stavka_=True, no_stavka=False)


    if gr == 'test_group':
        form_b = BidsSearchForm()
        form_s = SiteSearchForm()
        context['form_b'] = form_b
        context['form_s'] = form_s
        bids_site = None
        if request.method == 'GET':
            form_b = BidsSearchForm(request.GET)
            form_s = SiteSearchForm(request.GET)
            if form_b.is_valid():
                bid = form_b.cleaned_data['nds']
                get_bid = Bids.objects.filter(ID=int(bid))
                get_bid = get_bid.first() if get_bid else None
                if get_bid:
                    return  HttpResponseRedirect(
                                                reverse('bids-detail',
                                                kwargs={'pk': get_bid.pk})
                                                )
                else:
                    messages.warning(request,f'Bids:{bid} not exist')
            if form_s.is_valid():
                bids_site = form_s.cleaned_data['site']
                bids_site = ('versum', 'komputeritblok') if bids_site == 'both' else (bids_site,)

        M = Managers.objects.get(family__pk=u.pk)
        #st = Statistics_service.objects.filter(managers=M)
        #context['st'] = st
        st_period = set([x.date_ch.strftime("%m: %Y") for x in Bids.objects.filter(managers=M)])
        context['st_period'] = st_period
        if st_pk != 0:
            messages.warning(request,f'Period:{st_pk}')
            m_y = re.split(':',st_pk)
            try:
                month, year = m_y[0].strip(), m_y[1].strip()
            except:
                month, year = now.strftime("%m"), now.strftime("%Y")
            bids_per_period = Bids.objects.filter(date_ch__month=month, date_ch__year=year, managers=M)
        else:
            #now = timezone.now()
            month, year = now.strftime("%m"), now.strftime("%Y")
            bids_per_period = Bids.objects.filter(date_ch__month=month,date_ch__year=year, managers=M)
        context['bids_per_period'] = bids_per_period

        """if bids_site:
            bids_per_period = bids_per_period.filter(site__in=bids_site)
            context['manager_stats_per_period'] = manager_stats_per_period(M, bids_per_period, month, year,s=bids_site)
        else:
            context['manager_stats_per_period'] = manager_stats_per_period(M, bids_per_period, month, year)
        w1, w2 = context['manager_stats_per_period']['px']"""
        #sal = Salary(month, year)
        context['manager_stats_per_period'] = manager_stats_per_period(M, bids_per_period, month, year)
        w1, w2 = 0, 0
        context['w1'], context['w2'] = w1, w2
        context['bids_site'] = bids_site if bids_site else ('versum', 'komputeritblok')

    return render(request, 'money/family.html', context)

def save_create_data(data, only_sborka=False, only_remont=False):
    st = ('Успішно виконаний',)
    st_q = ('Відвантажено', 'Підтверджено', 'Діалог триває',
    'Чекаємо на оплату', 'Замовлення товару',
    'В черзі на збірку',)

    if only_remont == True and data['status'] in st:
        man = Managers.objects.get(name=data['manager'])
        bids,_ = Bids.objects.get_or_create(
        ID=data['ID'],
        site=data['account'],
        status=data['status'],
        sposobOplaty=data['sposobOplaty'],
        istocnikZakaza=data['istocnikZakaza'],
        managers=man
        )
        '''service,_ = Service.objects.get_or_create(kind='Ремонт ПК')
        Statistics_service_,_ = Statistics_service.objects.get_or_create(managers=man, service=service)
        if Statistics_service_.date.strftime("%B %Y") != timezone.now().strftime("%B %Y"):
            Statistics_service_ = Statistics_service.objects.create(managers=man, service=service)
        Statistics_service_.remont_count += 1
        Statistics_service_.date = timezone.now()
        Statistics_service_.save()'''
        return (None, 'only_remont')

    if only_sborka == True and data['status'] in st:
        for prod in data['products']:
            if prod[2][0] and data['sborsik']:
                sloznostPK, num_PK = prod[2]
                '''sborsik,_ = Managers.objects.get_or_create(name=data['sborsik'][0], sborsik=True)
                service,_ = Service.objects.get_or_create(kind='Сборка', sloznostPK=sloznostPK)
                if not sborsik.service_set.filter(pk=service.pk).exists():
                    sborsik.service_set.add(service)
                Statistics_service_,_ = Statistics_service.objects.get_or_create(managers=sborsik, service=service)
                if Statistics_service_.date.strftime("%B %Y") != timezone.now().strftime("%B %Y"):
                    Statistics_service_ = Statistics_service.objects.create(managers=sborsik, service=service)
                Statistics_service_.sborka_count += num_PK
                Statistics_service_.date = timezone.now()
                Statistics_service_.save()'''
        if data['sborsik'] and len(data['sborsik']) > 1:
            man,_ = Managers.objects.get_or_create(name=data['manager'])
            bids,_ = Bids.objects.get_or_create(
            ID=data['ID'],
            site=data['account'],
            status=data['status'],
            sposobOplaty=data['sposobOplaty'],
            istocnikZakaza=data['istocnikZakaza'],
            managers=man
            )
            bids.few_sborsik = ','.join(data['sborsik'][1:])
            bids.save()
        return (None, 'only_sborka')

    if not Bids.objects.filter(
    ID=data['ID']).exists() and data['account'] and data['ch_status'] == False:

        man = Managers.objects.get(name=data['manager'])

        bids = Bids.objects.create(
        ID=data['ID'],
        site=data['account'],
        status=data['status'],
        sposobOplaty=data['sposobOplaty'],
        istocnikZakaza=data['istocnikZakaza'],
        managers=man
        )
        if data['status'] in st_q or data['status'] == 'Успішно виконаний':
            save_create_data(data)
        return (bids, 'create')

    elif data['account'] and data['status'] in st_q:

        man = Managers.objects.get(name=data['manager'])

        if not Bids.objects.filter(ID=data['ID']).exists():
            bids = Bids.objects.create(
            ID=data['ID'],
            site=data['account'],
            status=data['status'],
            sposobOplaty=data['sposobOplaty'],
            istocnikZakaza=data['istocnikZakaza'],
            managers=man
            )
            res_tuple = (bids, 'create')
        else:
            bids = Bids.objects.get(ID=data['ID'])
            res_tuple = (bids, 'update')
            bids.ID=data['ID']
            bids.site=data['account']
            bids.status=data['status']
            bids.sposobOplaty=data['sposobOplaty']
            bids.istocnikZakaza=data['istocnikZakaza']
            bids.managers=man
            bids.save()

        Goods.objects.filter(bids__ID=bids.ID).delete()
        for prod in data['products']:
            Goods.objects.create(discr=prod[0], kind=prod[1], summa=round(prod[3]), bids=bids, amount=prod[2][1])
            """if not Goods.objects.filter(discr=prod[0], bids__ID=bids.ID).exists():
                Goods.objects.create(discr=prod[0], kind=prod[1], summa=round(prod[3]), bids=bids, amount=prod[2][1])
            elif Goods.objects.filter(discr=prod[0], bids__ID=bids.ID).count() == 1:
                goods_ = Goods.objects.get(discr=prod[0], kind=prod[1])
                goods_.amount = prod[2][1]
                goods_.kind = prod[1]
                goods_.summa = round(prod[3])
                goods_.save()"""
        return res_tuple

    elif data['account'] and data['status'] in st:

        man = Managers.objects.get(name=data['manager'])

        if not Bids.objects.filter(ID=data['ID']).exists():
            bids = Bids.objects.create(
            ID=data['ID'],
            site=data['account'],
            status=data['status'],
            sposobOplaty=data['sposobOplaty'],
            istocnikZakaza=data['istocnikZakaza'],
            managers=man
            )
            res_tuple = (bids, 'create')
        else:
            bids = Bids.objects.get(ID=data['ID'])
            res_tuple = (bids, 'update')
            bids.ID=data['ID']
            bids.site=data['account']
            bids.status=data['status']
            bids.sposobOplaty=data['sposobOplaty']
            bids.istocnikZakaza=data['istocnikZakaza']
            bids.managers=man
            bids.save()

        Goods.objects.filter(bids__ID=bids.ID).delete()
        count = 0
        for prod in data['products']:
            count += (round(prod[3]) * prod[2][1])
            Goods.objects.create(discr=prod[0], kind=prod[1], summa=round(prod[3]), bids=bids,
            amount=prod[2][1])
            if prod[2][0] and data['sborsik']:
                sloznostPK, num_PK = prod[2]
                '''sborsik,_ = Managers.objects.get_or_create(name=data['sborsik'][0], sborsik=True)
                service,_ = Service.objects.get_or_create(kind='Сборка', sloznostPK=sloznostPK)
                if not sborsik.service_set.filter(pk=service.pk).exists():
                    sborsik.service_set.add(service)
                Statistics_service_,_ = Statistics_service.objects.get_or_create(managers=sborsik, service=service)
                if Statistics_service_.date.strftime("%B %Y") != timezone.now().strftime("%B %Y"):
                    Statistics_service_ = Statistics_service.objects.create(managers=sborsik, service=service)
                Statistics_service_.sborka_count += num_PK
                Statistics_service_.date = timezone.now()
                Statistics_service_.save()
        if data['sborsik'] and len(data['sborsik']) > 1:
            bids.few_sborsik = ','.join(data['sborsik'][1:])
            bids.save()'''
        if data['istocnikZakaza'] in ('Алло', 'Rozetka'):
            try:
                count = round(count * 0.1)
                expense_marketplace(data['ID'], count, data['account'], data['istocnikZakaza'])
            except:
                pass

        return res_tuple

        """for prod in data['products']:
            if not Goods.objects.filter(discr=prod[0], bids__ID=bids.ID).exists():
                Goods.objects.create(discr=prod[0], kind=prod[1], summa=round(prod[3]), bids=bids, amount=prod[2][1])
            elif Goods.objects.filter(discr=prod[0], bids__ID=bids.ID).count() == 1:
                goods_ = Goods.objects.get(discr=prod[0], kind=prod[1])
                goods_.amount = prod[2][1]
                goods_.kind = prod[1]
                goods_.summa = round(prod[3])
                goods_.save()"""

@csrf_exempt
@require_POST
def webhook(request):
    jsondata = request.body
    data = json.loads(jsondata)
    '''name_ = timezone.now().strftime("%d %B %Y, %H:%M")
    r = One_C.objects.create(name='name_')
    r.json_data = data
    r.save()'''
    dict_data = bid(data)

    if dict_data['manager'] in [m.name for m in Managers.objects.filter(is_active=True)]:
        res = save_create_data(dict_data)
    elif dict_data['manager'] and dict_data['manager'] in [m.name for m in Managers.objects.filter(remontnik=True)] + ['Сервис Сборка']:
        res = save_create_data(dict_data, only_remont=True)
    elif dict_data['products'] and dict_data['manager']:
        res = save_create_data(dict_data, only_sborka=True)
        #messages.success(request,f'{res}')
        try:
            bids_ = res[0].ID if res[0] else 'bad_0'
            ist = res[0].istocnikZakaza if res[0] else 'bad_ist'
            st = res[1] if res[1] else 'bad_1'
            print(f'ok: {bids_} {ist} {st}')
        except:
            print(f"bad in zayvka: {dict_data['ID']}")
    else:
        #messages.success(request,f'{dict_data.keys()}')
        print(f'bad: {dict_data.keys()}')
    if 'account' in dict_data:
        return HttpResponse(f"Site: ")
    else:
        return HttpResponse(f"not good")


def stats_rules(request, site, param, month, year):
    # раздел статистики: детальная инфа по расходам, доходам
    summa = '0'
    list_result = []

    if param == 2:
        stats = StatsRules(site, month, year)
        list_result = stats.all_plan_exp(summa)
    if param == 3:
        stats = StatsRules(site, month, year)
        list_result = stats.exp_var_per_comps(summa)
    if param == 4:
        stats = StatsRules(site, month, year)
        list_result = stats.stavka_plan_stavka(summa)
    if param == 5:
        stats = StatsRules(site, month, year)
        list_result = stats.exp_reklama(summa)
    if param == 6:
        stats = StatsRules(site, month, year)
        list_result = stats.fedoroff(summa)[0]
    if param == 7:
        stats = StatsRules(site, month, year)
        list_result = stats.site_profit(summa)
    if param == 1:
        stats = StatsRules(site, month, year)
        list_result = stats.plan_z_plan(summa)
    if param == 8:
        stats = StatsRules(site, month, year)
        list_result = stats.gross_profit_info(summa)

    context = {'list_result': list_result,
                'site': site,
                'month': month,
                'year': year,
                }
    if param == 1:
        context.update({'plan_detale': True})
    if param == 8:
        context.update({'gross_profit_detale': True})

    return render(request, 'money/stats_detail.html', context)

def plan_change(request, site_, month_, year_):
    # утановка плана
    context = dict()

    month = int(month_) - 1
    if month > 0:
        month, year = str(month), year_
    else:
        month, year = '12', str(int(year_) - 1)

    if request.method == 'GET':
        messages.info(request, "Установите план и выход в 0")

        our_plan = Plan.objects.get(site=site_, date__month=month,date__year=year)

        form = PlanForm(initial={
        'plan': our_plan.plan,
        'zero_plan': our_plan.zero_plan
        })

        context['form_plan'] = form

        return render(request, 'money/admin_test.html', context)

    if request.method == 'POST':
        form = PlanForm(request.POST)
        if form.is_valid():

            plan_ = form.cleaned_data['plan']
            zero_plan_ = form.cleaned_data['zero_plan']

            our_plan = Plan.objects.get(site=site_, date__month=month,date__year=year)
            our_plan.plan = plan_
            our_plan.zero_plan = zero_plan_
            our_plan.save()

            messages.warning(request,
            f'План ({month}: {year}) изменен: {plan_}; Выход в 0: {zero_plan_}')

            return  HttpResponseRedirect(
                                        reverse('stats_rules',
                                        args=(site_, 1, month_, year_))
                                        )
def gross_profit_change(request, site_, month_, year_):
    # утановка плана
    context = dict()

    if request.method == 'GET':
        messages.info(request, "Установите наценку, оборот_ПК, кол_ПК")

        our_profit = Gross_profit.objects.get(site=site_, date__month=month_,date__year=year_)

        form = GrossprofitForm(initial={
        'rentability': our_profit.rentability,
        'amount': our_profit.amount,
        'quantity':our_profit.quantity
        })

        context['form_profit'] = form

        return render(request, 'money/admin_test.html', context)

    if request.method == 'POST':
        form = GrossprofitForm(request.POST)
        if form.is_valid():

            rentability_ = form.cleaned_data['rentability']
            amount_ = form.cleaned_data['amount']
            quantity_ = form.cleaned_data['quantity']

            our_profit = Gross_profit.objects.get(site=site_, date__month=month_,date__year=year_)
            our_profit.rentability = rentability_
            our_profit.amount = amount_
            our_profit.quantity = quantity_
            our_profit.save()

            messages.warning(request,
            f'В Валовой прибыли ({month_}: {year_}) изменена наценка: {rentability_}; оборот_ПК: {amount_}; кол_ПК: {quantity_}')

            return  HttpResponseRedirect(
                                        reverse('stats_rules',
                                        args=(site_, 8, month_, year_))
                                        )
