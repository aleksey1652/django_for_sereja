from cat.models import *
from cat.forms_admin_comps import *
from cat.forms import ComputersSpecialPrice
from load_form_providers.load_element import  to_article2_1
from django.db.models import Min
from django.contrib import messages
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
import re
#start_to_calc catch_to_calc_forms calc_to_view catch_to_admin_forms edit_parts_pack
#change_assembly edit_parts_pack

def special_price(request, pc_pk):
    # изменение Спеццены для одного компа(вызов внутри компа)
    usd, margin_default = USD.objects.last().usd, USD.objects.last().margin
    margin_default = margin_default if margin_default else 1

    form = ComputersSpecialPrice(initial={
    'warranty_computers': 0,
    'class_computers': margin_default,
    'exch': usd,
    })

    context = {
                'form': form,
                'pc_pk': pc_pk,
              }

    if request.method == 'POST':
        comp = Computers.objects.get(pk=pc_pk)
        form = ComputersSpecialPrice(request.POST)
        if form.is_valid():
            margin = form.cleaned_data['class_computers']
            margin = round(margin, 2)
            special_price = form.cleaned_data['warranty_computers']
            exch = form.cleaned_data['exch']
            try:
                special_price = float(special_price)
            except:
                messages.error(request,f'Спеццена должна быть числом')

                return  HttpResponseRedirect(
                                            reverse(f'admin:cat_computers_change',
                                            args=(comp.pk,))
                                            )

            #sp_to_bd = round(special_price * margin * exch)
            sp_to_bd = round(special_price) # поменяли алгоритм

            comp.warranty_computers = sp_to_bd
            comp.class_computers = margin
            comp.save()
            messages.success(
            request,f'В {comp.name_computers} спеццена теперь: {sp_to_bd}, наценка:{margin}')

            return  HttpResponseRedirect(
                                        reverse(f'admin:cat_computers_change',
                                        args=(comp.pk,))
                                        )

    return render(request, 'money/admin_test.html', context)

def change_promotin_for_comps(request, comp_pack):
    # добавление ярлыка (выбранной в админ-действии Computers) группе компов

    form = Form_promotion()

    context = {
                'form': form,
                'comp_pack': comp_pack,
              }

    if request.method == 'POST':
        form = Form_promotion(request.POST)
        if form.is_valid():
            comps_pk = [int(c) for c in comp_pack.split(',')]
            comps = Computers.objects.filter(pk__in=comps_pk)
            comps_name = list(comps.values_list('name_computers', flat=True))

            prom_name = form.cleaned_data['promotion']
            prom = Promotion.objects.get(prom=prom_name)

            for comp in comps:
                comp.promotion_set.add(prom)

            messages.success(
            request,
            f"В {comps_name} добавлен ярлык: {prom_name}")
            return  HttpResponseRedirect(
                                        reverse(f'admin:cat_computers_changelist')
                                        )

    return render(request, 'money/admin_test.html', context)

def change_time_assembly(request, comp_pack):

    form = Comps_time_assemblyForm()

    context = {
                'form': form,
                'comp_pack': comp_pack,
              }

    if request.method == 'POST':
        form = Comps_time_assemblyForm(request.POST)
        if form.is_valid():
            comps_pk = [int(c) for c in comp_pack.split(',')]
            comps = Computers.objects.filter(pk__in=comps_pk)

            time_ru = form.cleaned_data['time_assembly_ru']
            time_ukr = form.cleaned_data['time_assembly_ukr']

            count_comps = comps.update(
            time_assembly_ru=time_ru,
            time_assembly_ukr=time_ukr)
            messages.success(
            request,
            f"In {count_comps} comps was update : {time_ru}, : {time_ukr}")
            return  HttpResponseRedirect(
                                        reverse(f'admin:cat_computers_changelist')
                                        )

    return render(request, 'money/admin_test.html', context)

def get_keys_from_post(dict_):
    set_kind = {'proc', 'mb', 'case', 'hdd_ssd', 'cool', 'video', 'mem', 'ps', 'vent',
    'mon', 'wifi', 'km', 'soft', 'cables'}
    for s in set_kind:
        if s in dict_:
            return (dict_[s], dict_form_to_short[s])
    return (None, None)

def edit_parts_pack(request, comp_pack):
    #comps_pk = comp_pack.split(',')

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
            short = Parts_short.objects.get(name_parts=short_name, kind2=False)
            kind_ = short.kind
        except:
            messages.error(request,f"Ошибка в детали:{short_name}")
            return  HttpResponseRedirect(
                                        reverse(f'admin:cat_computers_changelist')
                                        )
        if kind_ in ('ssd', 'hdd'):
            short_name = f'пусто;{short_name}'
            kind_ = 'hdd_computers'
        elif kind_ in ('aproc', 'iproc', 'amb', 'imb'):
            kind_ = kind_[1:] + '_computers'
        else:
            kind_ = kind_ + '_computers'

        comps_pk = [int(c) for c in comp_pack.split(',')]
        comps = Computers.objects.filter(pk__in=comps_pk)
        comps_str = f"comps.update({kind_}='{short_name}')"
        count = eval(comps_str)
        messages.success(request,f"Изменены  {count} компов: {short_name}")
        return  HttpResponseRedirect(
                                    reverse(f'admin:cat_computers_changelist')
                                    )
        #return HttpResponse(f"{request.POST['kind']}")

    return render(request, 'admin/start_calc.html', context)

def edit_parts_num(request, comp_pack):
    #comps_pk = comp_pack.split(',')

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
        comps = Computers.objects.filter(pk__in=comps_pk)
        if num_vent == 'пусто':
            count = comps.update(vent_computers=num_vent, vent_num_computers=1)
        else:
            count = comps.update(vent_num_computers=num_vent)
        messages.success(request,f"Изменены  {count} компов: вентиляторы: {num_vent}")
        return  HttpResponseRedirect(
                                    reverse(f'admin:cat_computers_changelist')
                                    )
        #return HttpResponse(f"{request.POST['kind']}")

    return render(request, 'admin/start_calc.html', context)


def get_new_comp(amd_intel, comp_pk, name_new):

    comp = Computers.objects.get(pk=comp_pk)

    try:
        kind_proc = Parts_short.objects.get(
        name_parts=comp.proc_computers).kind
    except:
        kind_proc = None

    if amd_intel == 'AMD':
        if kind_proc == 'aproc':
            proc = comp.proc_computers
            mb = comp.mb_computers
        else:
            proc = Parts_short.objects.filter(kind2=False, kind='aproc').last()
            mb = Parts_short.objects.filter(kind2=False, kind='amb').last()
    else:
        if kind_proc == 'iproc':
            proc = comp.proc_computers
            mb = comp.mb_computers
        else:
            proc = Parts_short.objects.filter(kind2=False, kind='iproc').last()
            mb = Parts_short.objects.filter(kind2=False, kind='imb').last()

    comp_copy = comp
    comp_copy.name_computers = name_new
    comp_copy.proc_computers = proc
    comp_copy.mb_computers = mb
    comp_copy.is_active = False
    comp_copy.pk = None
    comp_copy.save()

    return comp_copy


def get_start_comp(amd_intel):
    assembly = Pc_assembly.objects.get(kind_assembly='Other', name_assembly='Other_group')

    if amd_intel == 'AMD':
        proc = Parts_short.objects.filter(kind2=False, kind='aproc').last()
        mb = Parts_short.objects.filter(kind2=False, kind='amb').last()
    else:
        proc = Parts_short.objects.filter(kind2=False, kind='iproc').last()
        mb = Parts_short.objects.filter(kind2=False, kind='imb').last()

    c=Computers(name_computers=comp_name,url_computers='url',
    price_computers='1',proc_computers=proc,
    mb_computers=mb,mem_computers='пусто',
    video_computers='пусто',hdd_computers='пусто;пусто',
    ps_computers='пусто',case_computers='пусто',
    cool_computers='пусто',
    warranty_computers=' ', pc_assembly=assembly)
    c.save()

def start_to_calc(request, comp_pk):

    form = Form_amd_intel() if not comp_pk else Form_new_comp()

    if request.method == 'GET':
        context = {
                   'form': form
                  }
        if comp_pk:
            return render(request, 'admin/start_new_comp.html', context)
        return render(request, 'admin/start_calc.html', context)
    if request.method == 'POST':

        form = Form_amd_intel(request.POST) if not comp_pk else Form_new_comp(request.POST)

        if comp_pk:
            if form.is_valid():

                amd_intel = form.cleaned_data['calc']
                name_new = form.cleaned_data['new']

                comp_copy = get_new_comp(amd_intel, comp_pk, name_new)
                #return HttpResponse(f"{request.POST['calc']}, {request.POST['new']}")
                messages.success(request,f"Создан {comp_copy.name_computers}")
                return  HttpResponseRedirect(
                                            reverse(f'admin:cat_computers_change',
                                            args=(comp_copy.pk,))
                                            )

        if form.is_valid():
            amd_intel = form.cleaned_data['calc']
            if amd_intel == 'AMD':
                try:
                    comp = Computers.objects.get(name_computers='AMD_calc')
                except:
                    comp = get_start_comp(amd_intel)
            else:
                try:
                    comp = Computers.objects.get(name_computers='Intel_calc')
                except:
                    comp = get_start_comp(amd_intel)
            return  HttpResponseRedirect(
                                        reverse('calc_to_view',
                                        kwargs={'comp_pk':comp.pk}
                                        )
                                        )
        return HttpResponse(f"{request.POST}")

def get_comp_parts(name_parts_, kind_):
    if isinstance(kind_, str):
        short = Parts_short.objects.filter(kind=kind_, kind2=False, name_parts=name_parts_)
        if short.exists():
            return ('short', short)
        #full = Parts_full.objects.filter(kind=kind_, name_parts__icontains=name_parts_,
        #availability_parts__in=('yes', 'q'), providers__name_provider='-', providerprice_parts__gt=0)
        #if full.exists():
        if name_parts_.find('$') != -1:
            return ('full', name_parts_)
    else:
        short = Parts_short.objects.filter(kind__in=('hdd', 'ssd'), kind2=False, name_parts=name_parts_)
        if short.exists():
            return ('short', short)
        #full = Parts_full.objects.filter(kind__in=('hdd', 'ssd'), name_parts__icontains=name_parts_,
        #availability_parts__in=('yes', 'q'),providerprice_parts__gt=0)
        #if full.exists():
            #return ('full', full)
        if name_parts_.find('$') != -1:
            return ('full', name_parts_)
    return ('short', Parts_short.objects.filter(kind=kind_, kind2=False, name_parts='пусто'))

"""def get_context_for_message_block(short_name, short_kind):
    if short_kind ==

    full_or_short = get_comp_parts(short_name, short_kind)

    if full_or_short[0] == 'short':
        parts_main = full_or_short[1].values_list('parts_full__name_parts_main',flat=True)[0]
        if not parts_main:
            parts_main = 'склад' if full_or_short[1].values_list('parts_full__remainder',
            flat=True)[0] else None
    else:
        parts_main = full_or_short[1].values_list('name_parts_main',flat=True)[0]
        if not parts_main:
            parts_main = 'склад' if full_or_short[1].values_list('remainder',flat=True)[0] else None

    string_name = short_name + ' ' + parts_main if parts_main else short_name

    return string_name"""

def message_block(comp_pk, price):
    comp = Computers.objects.filter(pk=comp_pk).values(
    'price_computers', 'mb_computers', 'proc_computers', 'mem_computers', 'video_computers',
    'hdd_computers', 'case_computers', 'ps_computers', 'cool_computers','vent_computers',
    'wifi_computers','cables_computers','soft_computers'
                                                        )
    comp_get = Computers.objects.get(pk=comp_pk)

    dict_atr = {
    'price_computers': 'Цiна',
    'mb_computers': 'Материнська плата',
    'proc_computers': 'Процесор',
    'mem_computers': 'Оперативна пам’ять',
    'video_computers': 'Відеокарта',
    'hdd_computers': 'Накопичувач ССД/Накопичувач HDD',
    'case_computers': 'Корпус',
    'ps_computers': 'Блок живлення',
    'cool_computers': 'Кулер',
    'vent_computers': 'Вентилятор',
    'wifi_computers': 'wifi',
    'cables_computers': 'Кабеля',
    'soft_computers': 'Програмне забезпечення',
                }
    dict_comp = dict()
    for k, v in comp[0].items():
        if v != 'пусто':
            try:
                v = re.sub(r'\$.+', '', v).strip()
            except:
                v = v
            dict_comp[dict_atr[k]] = v
    try:
        dict_comp['Оперативна пам’ять'] = dict_comp['Оперативна пам’ять'] + f' x{comp_get.mem_num_computers}'
    except:
        dict_comp['Оперативна пам’ять'] = 'mem!'
    try:
        if comp_get.video_num_computers != '1':
            dict_comp['Відеокарта'] = dict_comp['Відеокарта'] + f' x{comp_get.video_num_computers}'
    except:
        pass
    try:
        dict_comp['Вентилятор'] = dict_comp['Вентилятор'] + f' x{comp_get.vent_num_computers}'
    except:
        pass

    dict_comp_client = {k: v if k != 'Цiна' else price  for k, v in dict_comp.items()}

    return (dict_comp_client, dict_comp)


def catch_to_calc_forms(request, what,short_name):
    comp = Computers.objects.get(pk=int(short_name))

    parts = request.POST['full']
    price_parts = request.POST['price_full']
    parts_price_parts = parts + ' $ ' + str(price_parts)

    if what == 'hdd_computers':
        temp = comp.hdd_computers.split(';')
        temp[0] = parts_price_parts
        comp.hdd_computers = ';'.join(temp)
        comp.save()
    elif what == 'hdd2_computers':
        temp = comp.hdd_computers.split(';')
        try:
            temp[1] = parts_price_parts
        except:
            temp.append(parts_price_parts)
        comp.hdd_computers = ';'.join(temp)
        comp.save()
    else:
        comp.__dict__[what] = parts_price_parts
        comp.save()

    messages.success(request,f"В {what} добавлено: {parts}")
    return  HttpResponseRedirect(
                                reverse('calc_to_view',
                                kwargs={'comp_pk':short_name}
                                )
                                )
    """return  HttpResponseRedirect(
                                reverse(f'admin:cat_computers_change',
                                args=(comp.pk,))
                                )"""

def calc_comp_context(pk_):
    comp = Computers.objects.filter(pk=pk_)
    for_comp_price = comp.first()

    #usd = USD.objects.last()
    #for_comp_price.warranty_computers = usd.usd
    #for_comp_price.save()

    form_full = FullForm()

    comp_parts = comp.values(
    'proc_computers', 'cool_computers', 'mb_computers',
    'mem_computers', 'video_computers', 'hdd_computers',
    'ps_computers', 'case_computers', 'vent_computers',
    'vent_computers', 'mon_computers', 'wifi_computers',
    'km_computers', 'cables_computers', 'soft_computers')[0]
    try:
        comp_parts['hdd2_computers'] = comp_parts['hdd_computers'].split(';')[1]
    except:
        comp_parts['hdd2_computers'] = 'пусто'
    comp_parts['hdd_computers'] = comp_parts['hdd_computers'].split(';')[0]

    comp_num = comp.values('mem_num_computers', 'video_num_computers', 'vent_num_computers')[0]

    list_form = []
    price_count = 0
    amd_intel = to_article2_1(comp[0].proc_computers)
    for k, v in comp_parts.items():
        v = v if v else 'пусто'
        if k not in ('hdd2_computers', 'hdd_computers'):
            try:
                if k in ('mb_computers', 'proc_computers') and amd_intel == 'aproc':
                    kind_ = 'a' + k[:-10]
                    full_or_short = get_comp_parts(v, kind_)
                elif k in ('mb_computers', 'proc_computers') and amd_intel == 'iproc':
                    kind_ = 'i' + k[:-10]
                    full_or_short = get_comp_parts(v, kind_)
                else:
                    kind_ = k[:-10]
                    full_or_short = get_comp_parts(v, kind_)
                try:
                    if full_or_short[0] == 'short':
                        price = round(float(full_or_short[1].values_list('x_code',flat=True)[0]), 1)
                    else:
                        try:
                            price = float(full_or_short[1].split('$')[-1].strip())
                        except:
                            price = 0
                        #price = round(float(full_or_short[1].aggregate(mini=Min('providerprice_parts'))['mini']),1)
                except:
                    price = 0
                if k == 'mem_computers':
                    try:
                        n, m = price, int(comp_num['mem_num_computers'])
                        price = f"({price} x{comp_num['mem_num_computers']})"
                    except:
                        n, m = price, 1
                        price = f"({price} x1)"
                if k == 'video_computers':
                    try:
                        n, m = price, int(comp_num['video_num_computers'])
                        price = f"({price} x{comp_num['video_num_computers']})"
                    except:
                        n, m = price, 1
                        price = f"({price} x1)"
                if k == 'vent_computers':
                    try:
                        n, m = price, int(comp_num['vent_num_computers'])
                        price = f"({price} x{comp_num['vent_num_computers']})"
                    except:
                        n, m = price, 1
                        price = f"({price} x1)"
            except:
                price = 0
                price = 0
            try:
                price_count += price
            except:
                price_count += n*m
        else:
            try:
                full_or_short = get_comp_parts(v, ('hdd', 'ssd'))
                try:
                    if full_or_short[0] == 'short':
                        price = round(float(full_or_short[1].values_list('x_code',flat=True)[0]), 1)
                    else:
                        #price = round(float(full_or_short[1].aggregate(mini=Min('providerprice_parts'))['mini']),1)
                        try:
                            price = float(full_or_short[1].split('$')[-1].strip())
                        except:
                            price = 0
                except:
                    price = 0
            except:
                price = 0
            price_count += price
        if full_or_short[0] == 'short':
            short_ = Parts_short.objects.filter(kind=kind_,kind2=False).values_list('name_parts',flat=True)
            CHOISE_ = [(short, short) for short in short_]
        else:
            short_short = Parts_short.objects.filter(kind=kind_,kind2=False).values_list('name_parts',flat=True)
            #short_ = full_or_short[1].values_list('name_parts',flat=True)
            #CHOISE_ = [(short, short) for short in short_] + [(short, short) for short in short_short]
            split_name = full_or_short[1]
            CHOISE_ = [(split_name, split_name)] + [(short, short) for short in short_short]

        if k in ('proc_computers', 'mb_computers'):
            if amd_intel == 'aproc':
                form_ = eval(dict_form[k][0])
                key_ = list(form_.fields.keys())[0]
                form_.base_fields[key_].choices = CHOISE_
                list_form.append((form_, price, form_full, k))
                #list_form.append((eval(dict_form[k][0]), price, link_, k))
            else:
                form_ = eval(dict_form[k][1])
                key_ = list(form_.fields.keys())[0]
                form_.base_fields[key_].choices = CHOISE_
                list_form.append((form_, price, form_full, k))
                #list_form.append((eval(dict_form[k][1]), price, link_, k))
        elif k in ('hdd2_computers', 'hdd_computers'):
            if full_or_short[0] == 'short':
                short_ = Parts_short.objects.filter(kind__in=('hdd',
                'ssd'),kind2=False).values_list('name_parts',flat=True)
                CHOISE_ = [(short, short) for short in short_]
            else:
                short_short = Parts_short.objects.filter(kind__in=('hdd',
                'ssd'),kind2=False).values_list('name_parts',flat=True)
                #short_ = full_or_short[1].values_list('name_parts',flat=True)
                #CHOISE_ = [(short, short) for short in short_] + [(short, short) for short in short_short]
                split_name = full_or_short[1]
                CHOISE_ = [(split_name, split_name)] + [(short, short) for short in short_short]
            form_ = eval(dict_form[k])
            key_ = list(form_.fields.keys())[0]
            form_.base_fields[key_].choices = CHOISE_
            list_form.append((form_, price, form_full, k))
        else:
            try:
                form_ = eval(dict_form[k])
                key_ = list(form_.fields.keys())[0]
                form_.base_fields[key_].choices = CHOISE_
                list_form.append((form_, price, form_full, k, dict_form[k + '_num']))
                #list_form.append((eval(dict_form[k]), price, link_, k, dict_form[k + '_num']))
            except:
                form_ = eval(dict_form[k])
                key_ = list(form_.fields.keys())[0]
                form_.base_fields[key_].choices = CHOISE_
                list_form.append((form_, price, form_full, k))
                #list_form.append((eval(dict_form[k]), price, link_, k))
    temp = list_form.pop(-1)
    list_form.insert(5, temp)
    for_comp_price.price_computers = round(price_count)
    for_comp_price.save()
    try:
        exchange = float(for_comp_price.warranty_computers)
        margin = float(for_comp_price.class_computers)
    except:
        exchange = USD.objects.last().usd
        margin = 0
    price_count = round(price_count * exchange * margin)

    return (list_form, price_count)

def calc_to_view(request, comp_pk):
    #from cat.models import Computers

    _, count_price = calc_comp_context(comp_pk)
    comp = Computers.objects.get(pk=comp_pk)
    mes = message_block(comp_pk, count_price)

    context = {
               #'mail_sender': mail_sender,
               'extra_data': (_, comp_pk, mes, comp, count_price)
              }

    return render(request, 'admin/calc_form_my.html', context)
