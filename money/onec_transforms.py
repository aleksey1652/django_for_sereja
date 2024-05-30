from money.models import *
import datetime
from django.utils import timezone
from django.db.models import Sum, Count, F
from cat.models import One_C, Providers, Parts_full
import re
from load_form_providers.load_element import to_article2_1
from money.service import trans_remainder_category_dict
from money.salary import Salary
from money.onec_expense import ExpenseRules
#providerprice_parts transformations Expense get_dict_to_bids_advanced Офис ПК витрина 2% Bids
#Gross_profit Expense cash_rate_already Выкуплен витрина

for_Customer = {'IT-Blok': 'itblok', 'Versum': 'versum', 'both': 'both', 'tenders': 'tenders'}

def salary_for_plan_exp(site_):
    # зп-ставки для плановых трат
    groups_name_ = (
                    'buh_group', 'glav_buh_group', 'razrab_group', 'kurier_group',
                    'one_c_group', 'sborsik_group', 'test_group'
                    )
    man = Managers.objects.filter(family__groups__name__in=groups_name_, site='both')
    stavka_man = man.aggregate(Total=Sum('cash_rate'))['Total']
    try:
        man_q = Managers.objects.get(name='Игорь Пасичник').cash_rate
    except:
        man_q = 0
    return (stavka_man + man_qs)

def salary_for_var_exp(site_):
    # зп для оперативных трат
    groups_name_ = (
                    'buh_group', 'glav_buh_group', 'razrab_group', 'kurier_group',
                    'one_c_group', 'sborsik_group', 'test_group'
                    )
    #ЗП Богдан Вольвин

    man = Managers.objects.filter(family__groups__name__in=groups_name_, site='both')
    stavka_man = man.aggregate(Total=Sum('cash_rate'))['Total']
    try:
        man_q = Managers.objects.get(name='Игорь Пасичник').cash_rate
    except:
        man_q = 0
    return stavka_man + man_qs

def get_exp_avg_relations():
    pass

def trans_remainder_category(item_dict):
    if isinstance(item_dict, dict) and 'category' in item_dict and 'product' in item_dict:
        if item_dict['category'] == 'Процессоры':
            kind_ = to_article2_1(item_dict['product'])
        elif item_dict['category'] == 'Материнские платы':
            kind_ = to_article2_1(item_dict['product'], pr=0)
        else:
            kind_ = trans_remainder_category_dict[item_dict['category']]
        return kind_
    else:
        return 'cables'

def plan_stavka(m, month, year):
    count = 0
    try:
        plan_versum = Plan.objects.get(date__month=month,date__year=year, site='versum')
        plan_itblok = Plan.objects.get(date__month=month,date__year=year, site='itblok')
        plan_versum_plan, plan_versum_zero_plan = plan_versum.plan, plan_versum.zero_plan
        plan_itblok_plan, plan_itblok_zero_plan = plan_itblok.plan, plan_itblok.zero_plan

        profit_versum = Gross_profit.objects.get(date__month=month, date__year=year, site='versum')
        profit_itblok = Gross_profit.objects.get(date__month=month, date__year=year, site='itblok')
        profit_versum_amount = profit_versum.amount
        profit_itblok_amount = profit_itblok.amount
    except:
        plan_versum_plan, plan_versum_zero_plan, plan_itblok_plan, plan_itblok_zero_plan = 0, 0, 0, 0
        profit_versum_amount, profit_itblok_amount = 0, 0

    if profit_versum_amount > plan_versum_zero_plan:
        count += 0.25
    if profit_itblok_amount > plan_itblok_zero_plan:
        count += 0.25
    if profit_versum_amount > plan_versum_plan:
        count += 0.25
    if profit_itblok_amount > plan_itblok_plan:
        count += 0.25
    dict_res = {
                'Версум_план': plan_versum_plan,
                'Версум_план_минимум': plan_versum_zero_plan,
                'Айтиблок_план': plan_itblok_plan,
                'Айтиблок_план_минимум': plan_itblok_zero_plan,
                'Версум_оборот': profit_versum_amount,
                'Айтиблок_оборот': profit_itblok_amount,
                'Процент_ставка': count
                }
    return dict_res


def yes_div_per_man(man, m, plan, bids_):
    yes = 0.01
    count_ = 1
    if m.site == 'versum':
        count_ = man.filter(site='versum').count()
        try:
            amount_versum = Gross_profit.objects.get(date__month=dateqs.strftime("%m"),
                            date__year=dateqs.strftime("%Y"), site='versum').amount
            # оборот версум
        except:
            amount_versum = 0
        #total = bids_.filter(goods__kind='Системный блок',
        #site='versum').distinct().select_related('goods').annotate(num=F('goods__amount'),
        #suma=F('goods__summa')).aggregate(Total=Sum(F('num')*F('suma')))['Total']
        if amount_versum >= plan:
            yes = 0.01
        else:
            yes = 0
    if m.site == 'itblok':
        count_ = man.filter(site='itblok').count()
        try:
            amount_itblok = Gross_profit.objects.get(date__month=dateqs.strftime("%m"),
                            date__year=dateqs.strftime("%Y"), site='itblok').amount
            # оборот itblok
        except:
            amount_versum = 0
        #total = bids_.filter(goods__kind='Системный блок',
        #site='komputeritblok').distinct().select_related('goods').annotate(num=F('goods__amount'),
        #suma=F('goods__summa')).aggregate(Total=Sum(F('num')*F('suma')))['Total']
        if amount_versum >= plan:
            yes = 0.01
        else:
            yes = 0
    else:
        return 0

    try:
        return round(yes / count_, 2)
    except:
        return 0


def salary_admin_managers(dateqs, kw, bids_, man):
    sal = Salary(dateqs.strftime("%m"), dateqs.strftime("%Y"))
    super_manager_option = 0
    salary_dict = {'versum': 0, 'itblok': 0}
    goods__kind = 0
    salary_editions = kw[:]
    plan_ = Plan.objects.filter(date__month=dateqs.strftime("%m"),date__year=dateqs.strftime("%Y"))
    #plan_now = plan_.last().plan if plan_.exists() else 10000000
    #yes = 0.01 if salary_editions[-1]['Системный_блок'] >= plan_now else 0
    soft_bonus = Goods.objects.first().software_bonus
    for k in salary_editions:
        try:
            m = Managers.objects.get(name=k['name'])
        except:
            continue
        #already = m.cash_rate_already
        already = sal.st_cash_rate_already(m)
        k['Получил'] = already
        if 'ПК_витрина' not in k:
            k['ПК_витрина'] = 0
        if m.cash_rate:
            rate_serve = sal.plan_stavka()
            rate = round(m.cash_rate * rate_serve['Процент_ставка'])
        else:
            rate = m.cash_rate
        if m.super:
            #k['ЗП'] = round(salary_editions[-1]['Системный_блок'] * 0.005 + k['Комплектующие'] * 0.005 + k['ПО'] * soft_bonus + k['ПК_витрина'] * 0.01)
            zp = round(salary_editions[-1]['Системный_блок'] * 0.005 + salary_editions[-1]['Комплектующие'] * 0.005 + rate)
            k['ЗП'] = f"{salary_editions[-1]['Системный_блок']}*0.005 + {salary_editions[-1]['Комплектующие']} * 0.005 + ставка: {rate} = {zp}"

            #super_manager_option = k['ЗП']
            super_manager_option = zp
            #salary_negative = bids_.filter(managers__name=k['name']).distinct().annotate(num=F('goods__amount'),
            #suma=F('goods__summa')).aggregate(Total=Sum(F('num')*F('suma')))['Total']
            '''try:
                salary_negative = float(salary_negative * 0.005)
            except:
                salary_negative = 0'''
        else:
            if m.site == 'versum':
                plan_now = sal.get_plan('versum')
                yes = sal.yes_div_per_man(m, plan_now)
                """try:
                    plan_now = plan_.filter(site='versum').last().plan
                except:
                    plan_now = 10000000
                yes = yes_div_per_man(man, m, plan_now, bids_)"""
            if m.site == 'itblok':
                plan_now = sal.get_plan('itblok')
                yes = sal.yes_div_per_man(m, plan_now)
                """try:
                    plan_now = plan_.filter(site='itblok').last().plan
                except:
                    plan_now = 10000000
                yes = yes_div_per_man(man, m, plan_now, bids_)"""
            try:
                zp = round(k['Системный_блок'] * (0.01 + yes) + k['Комплектующие'] * 0.01 + k['ПК_витрина'] * 0.01 + rate)
                k['ЗП'] = f"{k['Системный_блок']} * (0.01 + {yes}) + {k['Комплектующие']} * 0.01 + {k['ПК_витрина']}* 0.01 ставка:{rate} = {zp}"
                #k['ЗП'] = round(k['Системный_блок'] * (0.01 + yes) + k['Комплектующие'] * 0.005 + k['ПО'] * soft_bonus + k['ПК_витрина'] * 0.01)
            except:
                zp = round(k['Системный_блок'] * 0.01 + k['Комплектующие'] * 0.01 + k['ПК_витрина'] * 0.01)
                k['ЗП'] = f"{k['Системный_блок']} * 0.01 + {k['Комплектующие']} * 0.005 + {k['ПК_витрина']}* 0.01 = {zp}"
                #k['ЗП'] = round(k['Системный_блок'] * 0.01 + k['Комплектующие'] * 0.005 + k['ПО'] * soft_bonus + k['ПК_витрина'] * 0.01)
            if m.site == 'versum':
                salary_dict['versum'] += zp
            else:
                salary_dict['itblok'] += zp
    """if super_manager_option:
        try:
            temp_zp = float(salary_editions[-1]['ЗП'].split('=')[-1].strip())
        except:
            temp_zp = 0
        #salary_editions[-1]['ЗП'] += (super_manager_option - salary_negative)
        salary_editions[-1]['ЗП'] = temp_zp + (super_manager_option - salary_negative)"""
    salary_dict['versum'] += (super_manager_option / 2)
    salary_dict['itblok'] += (super_manager_option / 2)
    salary_editions[-1]['ЗП'] = f"{salary_dict}"
    salary_editions[-1]['Получил'] = ''
    return salary_editions

def count_comp_null_plan(av_chk, plan_site, site_, dateqs):
    month, year = dateqs.strftime("%m"), dateqs.strftime("%Y")
    sal = Salary(month, year)
    sal_plan = sal.get_plan(site_, past_period=True, view_full=True)

    if av_chk.quantity:
        comp_plan_ = av_chk.quantity
        comp_null_ = round(sal_plan['zero_plan'] / av_chk.price, 1)
    else:
        comp_plan_ = round(sal_plan['plan_now'] / av_chk.price, 1)
        comp_null_ = round(sal_plan['zero_plan'] / av_chk.price, 1)

    comp_plan, comp_null, profit_count_, y_plan = (
                                                comp_plan_,
                                                comp_null_,
                                                sal_plan['profit_plan'],
                                                sal_plan['y_plan'],
                                                  )
    error = 'ok'
    if y_plan < 0:
        error = 'k комп окупаемость bad'
    if profit_count_ < 0:
        error = 'прибыль расч bad'
    if not comp_null:
        error = 'комп окупаемость bad'
    if not comp_plan:
        error = 'план bad'

    return (comp_plan, comp_null, profit_count_, y_plan, error)

    if av_chk.quantity:
        comp_plan = av_chk.quantity
    else:
        comp_plan = round(plan_site / av_chk.price, 1)
    hand_check_ = av_chk.hand_check

    if Gross_profit.objects.filter(date__month=month,date__year=year,
    site=site_).exists():
        expense_site = Expense.objects.filter(expense_groups__name='Ручные поля',
        date__month=month, date__year=year, site=site_, is_active=True)
        summa_site = round(expense_site.distinct().aggregate(Total=Sum('amount'))['Total'])
        summa_one_c = summa_site if summa_site else 0
        ratio_, _ = Ratios.objects.get_or_create()
        if av_chk.site == 'versum':
            summa_hand = round((av_chk.price) * ratio_.versum_ratio)
        else:
            summa_hand = round((av_chk.price) * ratio_.itblok_ratio)
        #summa_all = summa_one_c + summa_hand # Траты
        count_comp = Gross_profit.objects.filter(date__month=month,date__year=year,
        site=site_).last().quantity
        try:
            summa_all_ono_comp = summa_one_c / count_comp + summa_hand + hand_check_ #Траты на однин заказ
        except:
            #print('error count_comp')
            error = 'нет продаж'
            return (comp_plan, comp_null, profit_count_, y_plan, error)

        rentability_ = Gross_profit.objects.filter(date__month=month,date__year=year,
        site=site_).last().rentability #наценка
        rentability_ = (rentability_) /100 if rentability_ else 1
        profit_count_ = round(av_chk.price * rentability_ - summa_all_ono_comp, 1) #прибыль расчётная реал
        profit_count = round(av_chk.price * rentability_ - summa_hand - hand_check_, 1)  #прибыль расчётная
        if profit_count < 0:
            error = 'прибыль расч bad'
            return (comp_plan, comp_null, profit_count_, y_plan, error)

        try:
            #comp_null = round(summa_all_ono_comp * count_comp / (av_chk.price * rentability_),1)
            comp_null = round(summa_one_c / profit_count, 1)
            #количество компов для
            #окупаемости
        except:
            error = 'комп окупаемость bad'
            return (comp_plan, comp_null, profit_count_, y_plan, error)

        try:
            y_plan = 25 * summa_one_c / (comp_null * (25 * profit_count - av_chk.price))
            y_plan = round(y_plan, 2)
            #коефициент наценки для выполнения плана
            if y_plan < 0:
                error = 'k комп окупаемость bad'
        except:
            error = 'k комп окупаемость bad'
            return (comp_plan, comp_null, profit_count_, y_plan, error)

    return (comp_plan, comp_null, profit_count_, y_plan, error)

def personal_data(dateqs):
    month, year = dateqs.strftime("%m"), dateqs.strftime("%Y")
    sal = Salary(month, year)
    list_personal = []
    try:
        tovar_man = Managers.objects.get(family__groups__name='tovar_group')
    except:
        tovar_man = None
    if tovar_man:
        temp_dict = sal.salary_tovar(plan_stavka_=True, no_stavka=False)
        #temp_dict = dict()
        #temp_dict['name'] =  tovar_man.name

        list_personal.append(temp_dict)
    try:
        buh_man = Managers.objects.get(family__groups__name='buh_group')
    except:
        buh_man = None
    if buh_man:
        temp_dict = sal.salary_buh(plan_stavka_=True, no_stavka=False)
        #temp_dict['name'] =  buh_man.name
        list_personal.append(temp_dict)
    try:
        glav_buh_man = Managers.objects.get(family__groups__name='glav_buh_group')
    except:
        glav_buh_man = None
    if glav_buh_man:
        temp_dict = sal.salary_glav_buh(plan_stavka_=True, no_stavka=False)
        list_personal.append(temp_dict)
    try:
        kurier_man = Managers.objects.get(family__groups__name='kurier_group')
    except:
        kurier_man = None
    if kurier_man:
        temp_dict = sal.salary_kurier(plan_stavka_=True, no_stavka=False)
        list_personal.append(temp_dict)
    """try:
        one_man = Managers.objects.get(family__groups__name='one_c_group')
    except:
        one_man = None
    if one_man:
        temp_dict = sal.salary_one_c(plan_stavka_=True, no_stavka=False)
        list_personal.append(temp_dict)"""
    try:
        razrab_man = Managers.objects.get(family__groups__name='razrab_group')
    except:
        razrab_man = None
    if razrab_man:
        temp_dict = sal.salary_razrab(plan_stavka_=True, no_stavka=False)
        list_personal.append(temp_dict)
    try:
        sklad_man = Managers.objects.get(family__groups__name='sklad_group')
    except:
        sklad_man = None
    if sklad_man:
        temp_dict = sal.salary_sklad(plan_stavka_=True, no_stavka=False)
        list_personal.append(temp_dict)

    return list_personal

def kurier_per_comps(dateqs):
    month, year = dateqs.strftime("%m"), dateqs.strftime("%Y")
    service,_ = Service.objects.get_or_create(kind='Курьер')
    try:
        count_comp = Gross_profit.objects.get(date__month=month,date__year=year, site='both').quantity
    except:
        count_comp = 0
    try:
        st = Statistics_service.objects.filter(service=service, date__month=month, date__year=year).last()
    except:
        st = 0
    try:
        try:
            km = st.km_count
        except:
            km = 0
        res = round((service.cash_rate + km * service.summa)/count_comp, 1)
    except:
        res = 0
    return f"{service.cash_rate} + {km * service.summa} / {count_comp} = {res}"

def count_per_group_expense(dateqs):
    list_groups = [{'title': '----', 'versum': '----', 'itblok': '----'},] #пустая строка перед гр расходов
    month, year = dateqs.strftime("%m"), dateqs.strftime("%Y")

    list_ = list(Expense_groups.objects.filter(expense__date__month=month,
    expense__date__year=year, expense__is_active=True
    ).select_related('expense__amount').annotate(total=Sum('expense__amount')).values('name',
    'expense__site', 'total'))

    for exp_dict in list_:
        temp_dict = {'title': None, 'versum': '-', 'itblok': '-'}
        temp_dict['title'] = exp_dict['name']
        if exp_dict['expense__site'] == 'versum':
            temp_dict['versum'] = round(float(exp_dict['total']))
        elif exp_dict['expense__site'] == 'itblok':
            temp_dict['itblok'] = round(float(exp_dict['total']))
        elif exp_dict['expense__site'] == 'both':
            temp_dict['versum'], temp_dict['itblok'] = (round(float(exp_dict['total']) / 2),
            round(float(exp_dict['total']) / 2))
        list_groups.append(temp_dict)
    return list_groups

def new_post(profit_, expense_, site):
    try:
        profit = profit_.quantity
    except:
        profit = 0
    try:
        if site == 'versum':
            exp_site = expense_.filter(discr='Растраты по НП VERSUM').last().amount
        else:
            exp_site = expense_.filter(discr='Растраты по НП It-Blok').last().amount
    except:
        exp_site = 0
    try:
        res = round(int(round(exp_site)) / profit)
    except:
        res = 0
    return f'{exp_site} / {profit} = {res}'

def gradation_comps(dateqs):
    month, year = dateqs.strftime("%m"), dateqs.strftime("%Y")

    bids_versum = Bids.objects.filter(site='versum', status='Успішно виконаний',
    goods__kind='Системный блок', date_ch__month=month, date_ch__year=year)
    set_bids_versum = set(bids_versum.values_list('pk', flat=True))

    bids_itblok = Bids.objects.filter(site='komputeritblok', status='Успішно виконаний',
    goods__kind='Системный блок', date_ch__month=month, date_ch__year=year)
    set_bids_itblok = set(bids_itblok.values_list('pk', flat=True))

    temp_list = []
    count_versum, count_itblok = 0, 0

    comps = Service.objects.filter(kind__in=('Офисный комп', 'Игровой комп'))
    comps_dict = comps.values('kind', 'sloznostPK', 'cash_rate').order_by('cash_rate')
    for comp in comps_dict:
        #temp_versum = bids_versum.distinct().filter(goods__summa__lt=comp['cash_rate'])
        count_temp = Goods.objects.filter(bids__pk__in=set_bids_versum,
        kind='Системный блок',summa__lt=comp['cash_rate']).annotate(
        num=F('amount')).aggregate(Total=Sum(F('num')))['Total']
        #count_temp = temp_versum.select_related('goods').annotate(
        #num=F('goods__amount')).aggregate(Total=Sum(F('num')))['Total']
        count_temp = count_temp if count_temp else 0
        count_this_grad_versum = count_temp - count_versum
        count_versum += count_this_grad_versum

        #temp_itblok = bids_itblok.distinct().filter(goods__summa__lt=comp['cash_rate'])
        count_temp = Goods.objects.filter(bids__pk__in=set_bids_itblok,
        kind='Системный блок',summa__lt=comp['cash_rate']).annotate(
        num=F('amount')).aggregate(Total=Sum(F('num')))['Total']
        #count_temp = temp_itblok.select_related('goods').annotate(
        #num=F('goods__amount')).aggregate(Total=Sum(F('num')))['Total']
        count_temp = count_temp if count_temp else 0
        count_this_grad_itblok = count_temp - count_itblok
        count_itblok += count_this_grad_itblok

        temp_list.append(
        {'title': comp['kind'] + '-' + comp['sloznostPK'],
        'versum': count_this_grad_versum, 'itblok': count_this_grad_itblok})

    return temp_list

def reklama_managers(dateqs, type_):
    month, year = dateqs.strftime("%m"), dateqs.strftime("%Y")

    bids = Bids.objects.filter(istocnikZakaza='Инстаграм',
    date_ch__month=month, date_ch__year=year)

    count_bids = bids.filter(
    goods__kind='Системный блок').distinct().select_related(
    'goods').annotate(num=F('goods__amount')).aggregate(Total=Sum(F('num')))['Total']
    count_bids = count_bids if count_bids else 0

    if type_ == 'cmm_man':
        man, _ = Managers.objects.get_or_create(name='СММ менеджер')
        try:
            res = round(man.cash_rate / count_bids)
        except:
            res = 0
    else:
        all_comp = Gross_profit.objects.filter(date__month=month, date__year=year, site='both').last()
        count_all_comp = all_comp.quantity if all_comp else 0
        man, _ = Managers.objects.get_or_create(name='Google менеджер')
        try:
            res = round(man.cash_rate / (count_all_comp - count_bids))
        except:
            res = 0
    return res

"""def km_one_bid(st, profit_both):
    try:
        profit = profit_both.quantity
    except:
        profit = 0
    km_per_period = st.filter(managers__family__groups__name='kurier_group').annotate(km=F('km_count')).aggregate(Total=Sum(F('km')))['Total']
    if km_per_period:
        km_per_period_ = float(km_per_period)
    else:
        km_per_period_ = 0
    try:
        tarif = Service.objects.get(kind='Курьер').summa
    except:
        tarif = 0
    try:
        res = round((km_per_period_ *  tarif) / profit)
    except:
        res = 0
    return f'Расходы по курьерам km: {km_per_period_} * тариф: {tarif}: / кол компов: {profit} = {res}'"""

def get_dict_to_bids_advanced(qs):
    man = Managers.objects.filter(family__groups__name='test_group')
    sborsik = Managers.objects.filter(sborsik=True)
    remontnik = Managers.objects.filter(remontnik=True)
    personal = Managers.objects.filter(family__groups__name='personal_group')
    bids_ = qs.filter(status='Успішно виконаний')
    date_temp = qs.filter(status='Успішно виконаний')
    dateqs = date_temp.last().date_ch if date_temp else timezone.now()
    month, year = dateqs.strftime("%m"), dateqs.strftime("%Y")
    sal = Salary(dateqs.strftime("%m"), dateqs.strftime("%Y"))
    exp = ExpenseRules(dateqs.strftime("%m"), dateqs.strftime("%Y"))
    st = Statistics_service.objects.filter(
    date__month=dateqs.strftime("%m"),date__year=dateqs.strftime("%Y"))
    summary = {'main': [], 'personal': [], 'sborsik': [], 'remontnik': [], 'advanced': []}
    dict_all_man = {'name': 'Все', 'Системный_блок': 0, 'ПО': 0, 'Комплектующие': 0, 'ПК_витрина': 0}

    summary['personal'] = personal_data(dateqs)

    for m in man:
        dict_temp = dict()
        dict_temp['name'] = m.name
        for k in ('Системный блок', 'ПО', 'Комплектующие'):
            temp = bids_.filter(managers=m,
            goods__kind=k).distinct().select_related('goods').annotate(num=F('goods__amount'),
            suma=F('goods__summa')).aggregate(Total=Sum(F('num')*F('suma')))['Total']
            dict_temp[re.sub(' ', '_', k)] = temp if temp else 0
            if temp:
                dict_all_man[re.sub(' ', '_', k)] += temp
        temp = bids_.filter(managers=m,
        istocnikZakaza='ПК вітрина 2%').distinct().select_related('goods').annotate(
        num=F('goods__amount'),
        suma=F('goods__summa')).aggregate(Total=Sum(F('num')*F('suma')))['Total']
        dict_temp['ПК_витрина'] = temp if temp else 0
        if temp:
            dict_all_man['ПК_витрина'] += temp
        summary['main'].append(dict_temp)
    summary['main'].append(dict_all_man)
    summary_temp = summary['main'][:]
    summary['main'] = salary_admin_managers(dateqs, summary_temp, bids_, man)
# get_dict_to_bids_advanced
    for m in sborsik:
        try:
            rate = Service.objects.filter(kind='Сборка').first().cash_rate
        except:
            rate = 0
        dict_temp = dict()
        dict_temp['name'] = m.name
        dict_temp['ЗП'] = rate
        already = sal.st_cash_rate_already(m)
        dict_temp['получил'] = already
        for k in ('простой_офисный', 'простой', 'обычный', 'сложный', 'ультра'):
            temp = st.filter(managers=m, service__kind='Сборка',
            service__sloznostPK=k).distinct().select_related('sborka_count').aggregate(
            Total=Sum('sborka_count'))['Total']
            dict_temp[k] = temp if temp else 0
            service_ = Service.objects.filter(kind='Сборка',sloznostPK=k)
            if service_.exists() and temp:
                dict_temp['ЗП'] += service_.first().summa * temp
        if st.filter(managers=m, service__kind='Установка лед табличек').exists():
            service_led,_ = Service.objects.get_or_create(
            kind='Установка лед табличек',
            sloznostPK='простой')
            count_led = st.filter(managers=m, service__kind='Установка лед табличек'
            ).distinct().select_related('sborka_count').aggregate(
            Total=Sum('sborka_count'))['Total']
            dict_temp['ЗП'] += service_led.summa * count_led
        summary['sborsik'].append(dict_temp)

    for m in remontnik:
        rate_serve = sal.plan_stavka()
        try:
            rate = Service.objects.filter(kind='Ремонт ПК').first().cash_rate
            rate = round(rate * rate_serve['Процент_ставка'])
        except:
            rate = 0
        dict_temp = dict()
        dict_temp['name'] = m.name
        dict_temp['ЗП'] = rate
        already = sal.st_cash_rate_already(m)
        dict_temp['получил'] = already
        for k in ('простой', 'обычный', 'сложный', 'ультра'):
            temp = st.filter(managers=m,
            service__sloznostPK=k).distinct().aggregate(Total_rem=Sum('remont_count'), Total_obsl=Sum('obsluj_count'))
            temp_html = '--'.join([str(total) for total in list(temp.values()) if total])
            dict_temp[k] = temp_html if temp_html else 0
            service_ = Service.objects.filter(kind='Обслуживание',sloznostPK=k)
            if service_.exists() and temp['Total_obsl']:
                dict_temp['ЗП'] += service_.first().summa * temp['Total_obsl']
            service_ = Service.objects.filter(kind='Ремонт ПК',sloznostPK=k)
            if service_.exists() and temp['Total_rem']:
                dict_temp['ЗП'] += service_.first().summa * temp['Total_rem']
        summary['remontnik'].append(dict_temp)

    #plan_ = Plan.objects.filter(date__month=dateqs.strftime("%m"),date__year=dateqs.strftime("%Y"))
    #plan_versum = plan_.filter(site='versum')
    #plan_itblok = plan_.filter(site='itblok')
    #plan_now_versum = plan_versum.last().plan if plan_versum.exists() else 100000000
    #plan_now_itblok = plan_itblok.last().plan if plan_itblok.exists() else 100000000
    plan_versum = sal.get_plan('versum', view_full=True) # План для прошлого периода !
    plan_now_versum, plan_zero_versum = plan_versum['plan_now'], plan_versum['zero_plan']
    plan_itblok = sal.get_plan('itblok', view_full=True) # План для прошлого периода !
    plan_now_itblok, plan_zero_itblok = plan_itblok['plan_now'], plan_itblok['zero_plan']

    profit_versum_amount_and_quantity =\
    f"{exp.get_profit('versum', amount_=True)}/{exp.get_profit('versum', quantity_=True)}"
    #profit_versum_grossprofit_and_rentability =\
    #f"{exp.get_profit('versum', grossprofit_=True)}/{exp.get_profit('versum', rentability_=True)}"

    profit_itblok_amount_and_quantity =\
    f"{exp.get_profit('itblok', amount_=True)}/{exp.get_profit('itblok', quantity_=True)}"
    #profit_itblok_grossprofit_and_rentability =\
    #f"{exp.get_profit('itblok', grossprofit_=True)}/{exp.get_profit('itblok', rentability_=True)}"

    av_chk_versum_price_and_rentability =\
    f"{exp.get_av_chk('versum', price_=True)}/{exp.get_profit('versum', rentability_=True)}"

    av_chk_itblok_price_and_rentability =\
    f"{exp.get_av_chk('itblok', price_=True)}/{exp.get_profit('itblok', rentability_=True)}"

    stavka_sum_half, prozent_sum = sal.salary_for_plan_exp(half=True), (sal.sum_salary_no_stavka()) / 2
    zp_stavka_half_and_zp_var = f"{stavka_sum_half}/{prozent_sum}"

    profit_versum = exp.get_profit('versum')
    count_comp_v = profit_versum.quantity if profit_versum else 0
    try:
        sum_versum = profit_versum.grossprofit + profit_versum.grossprofitcomponents
        One_C_profit_comps_parts_ver =\
        f"{sum_versum}/{profit_versum.grossprofit}/{profit_versum.grossprofitcomponents}"
    except:
        One_C_profit_comps_parts_ver = "0/0/0"
        sum_versum = 0

    profit_itblok = exp.get_profit('itblok')
    count_comp_it = profit_itblok.quantity if profit_itblok else 0
    try:
        sum_itblok = profit_itblok.grossprofit + profit_itblok.grossprofitcomponents
        One_C_profit_comps_parts_it =\
        f"{sum_itblok}/{profit_itblok.grossprofit}/{profit_itblok.grossprofitcomponents}"
    except:
        One_C_profit_comps_parts_it = "0/0/0"
        sum_itblok = 0

    Sum_profit_comps_parts_ver = sum_versum - exp.get_sum_var_mark_versum(prozent_sum) -\
    exp.get_sum_plan_mark_versum(stavka_sum_half) - exp.get_reklama_expense('versum')

    Sum_profit_comps_parts_it = sum_itblok - exp.get_sum_var_mark_itblok(prozent_sum) -\
    exp.get_sum_plan_mark_itblok(stavka_sum_half) - exp.get_reklama_expense('itblok') -\
    exp.fedoroff_exp()


    #versum_comp_plan, versum_comp_null, versum_profit, versum_y_plan, versum_err = count_comp_null_plan(
    #exp.get_av_chk('versum', price_=True), plan_now_versum, 'versum', dateqs)
    versum_comp_plan, versum_comp_null, versum_profit, versum_y_plan, versum_err =\
    exp.count_comp_null_plan(
    'versum')
    itblok_comp_plan, itblok_comp_null, itblok_profit, itblok_y_plan, itblok_err =\
    exp.count_comp_null_plan(
    'itblok')

    #itblok_comp_plan, itblok_comp_null, itblok_profit, itblok_y_plan, itblok_err = count_comp_null_plan(
    #exp.get_av_chk('itblok', price_=True), plan_now_itblok, 'itblok', dateqs)

    """try:
        versum_salary_per_comp = round(eval(summary['main'][-1]['ЗП'])['versum'] / profit_versum.quantity)
    except:
        versum_salary_per_comp = 0
    try:
        itblok_salary_per_comp = round(eval(summary['main'][-1]['ЗП'])['itblok'] / profit_itblok.quantity)
    except:
        itblok_salary_per_comp = 0"""

    #data_new_post_versum = new_post(profit_versum, expense_versum, 'versum')
    #data_new_post_itblok = new_post(profit_itblok, expense_itblok, 'itblok')
    #kurier_stats = kurier_per_comps(dateqs)

    #km_per_one_bid = km_one_bid(st, profit_both)
    #reklama_cmm_managers = reklama_managers(dateqs, 'cmm_man')
    #reklama_google_managers = reklama_managers(dateqs, 'google')

    #gradation_comps_ = gradation_comps(dateqs)


    list_advanced = [
    {'tittle': 'Оборот/Колличество ПК',
    'versum': profit_versum_amount_and_quantity,
    'itblok': profit_itblok_amount_and_quantity,
    'dates': (month, year),
    'mark': 8},
    {'tittle': 'Ср чек/Наценка',
    'versum': av_chk_versum_price_and_rentability,
    'itblok': av_chk_itblok_price_and_rentability,
    'dates': (month, year),
    'mark': 8},
    {'tittle': 'Компы план/окупаемость',
    'versum': f'{versum_comp_plan}/{versum_comp_null}',
    'itblok': f'{itblok_comp_plan}/{itblok_comp_null}',
    'dates': (month, year),
    'mark': 0},
    {'tittle': 'План/План_окупаемость',
    'versum': f"{plan_now_versum}/{plan_zero_versum}",
    'itblok': f"{plan_now_itblok}/{plan_zero_itblok}",
    'dates': (month, year),
    'mark': 1},
    {'tittle': 'Общие запл. Растраты',
    'versum': exp.get_sum_plan_mark_versum(stavka_sum_half),
    'itblok': exp.get_sum_plan_mark_itblok(stavka_sum_half),
    'dates': (month, year),
    'mark': 2},
    {'tittle': 'Траты оперативные/компы',
    'versum': exp.get_sum_var_mark_versum(prozent_sum, per_comps=count_comp_v),
    'itblok': exp.get_sum_var_mark_itblok(prozent_sum, per_comps=count_comp_it),
    'dates': (month, year),
    'mark': 3},
    {'tittle': 'ЗП-ставки/ЗП-проценты',
    'versum': zp_stavka_half_and_zp_var,
    'itblok': zp_stavka_half_and_zp_var,
    'dates': (month, year),
    'mark': 4},
    {'tittle': 'Реклама',
    'versum': exp.get_reklama_expense('versum'),
    'itblok': exp.get_reklama_expense('itblok'),
    'dates': (month, year),
    'mark': 5},
    {'tittle': 'Федоров',
    'versum': 0,
    'itblok': exp.fedoroff_exp(),
    'dates': (month, year),
    'mark': 6},
    {'tittle': 'Прибыль1С(Сум/ПК/Компл)',
    'versum': One_C_profit_comps_parts_ver,
    'itblok': One_C_profit_comps_parts_it,
    'dates': (month, year),
    'mark': 0},
    {'tittle': 'Прибыль',
    'versum': Sum_profit_comps_parts_ver,
    'itblok': Sum_profit_comps_parts_it,
    'dates': (month, year),
    'mark': 7},

    #{'title': 'Коэф плана/ошибки?', 'versum': f'{versum_y_plan}/{versum_err}',
    #'itblok': f'{itblok_y_plan}/{itblok_err}'},
    #{'title': 'Чис приб с компа/Доля менеджера с компа', 'versum': f'{versum_profit}/{versum_salary_per_comp}',
    #'itblok': f'{itblok_profit}/{itblok_salary_per_comp}'},
    #{'title': 'НП/компы', 'versum': data_new_post_versum,
    #'itblok': data_new_post_itblok},
    #{'title': 'Курьер/компы', 'versum': kurier_stats,
    #'itblok': '<---'},
    #{'title': 'СММ+таргетолог', 'versum': reklama_cmm_managers,
    #'itblok': '<---'},
    #{'title': 'Kонтекст + СЕО', 'versum': reklama_google_managers,
    #'itblok': '<---'},
                    ]

    list_advanced += exp.reklama_managers()
    list_advanced += exp.var_exp_stats()
    #list_advanced += gradation_comps_
    #list_advanced += count_per_group_expense(dateqs)
    summary['advanced'] = list_advanced

    return summary

def get_rentability_avg(amount_list, rentability_list):
    try:
        procent = min(amount_list)/max(amount_list)
        razniza = rentability_list[0]-rentability_list[1]
        if amount_list[0] > amount_list[1]:
            avg = rentability_list[0] - (razniza*procent)/2
        else:
            avg = rentability_list[1] + (razniza*procent)/2
        return avg
    except:
        return 1

def get_sum_profit(month, year, TotalSales, TotalProfit, Total_, SumSales, SumProfit):
    #now = timezone.now()
    #month, year = now.strftime("%m"), now.strftime("%Y")
    all_agents = ('itblok', 'versum', 'tenders')
    dict_profit = dict()
    both = Gross_profit.objects.filter(date__month=month, date__year=year, site__in=('itblok', 'versum'))
    all = Gross_profit.objects.filter(date__month=month, date__year=year, site__in=all_agents)
    now = both.last().date

    if all.exists():
        all_sum = all.distinct().aggregate(Total=Sum('quantity'))['Total']
        all_sum = all_sum if all_sum else 0

        other_quantity = Total_ - all_sum
        if other_quantity > 0:
            all_amount = all.distinct().aggregate(Total=Sum('amount'))['Total']
            all_amount = all_amount if all_amount else 0

            #all_amountcomponents = all.distinct().aggregate(Total=Sum('amountcomponents'))['Total']
            #all_amountcomponents = all_amountcomponents if all_amountcomponents else 0

            all_grossprofit = all.distinct().aggregate(Total=Sum('grossprofit'))['Total']
            all_grossprofit = all_grossprofit if all_grossprofit else 0

            #all_grossprofitcomponents = all.distinct().aggregate(Total=Sum('grossprofitcomponents'))['Total']
            #all_grossprofitcomponents = all_grossprofitcomponents if all_grossprofitcomponents else 0

            other_amount = TotalSales - all_amount
            other_amount_ = round(other_amount)
            other_profit = TotalProfit - all_grossprofit

            try:
                other_rentability = round(other_profit / other_amount * 100, 1)
            except:
                other_rentability = 0
            try:
                other_profit_ = round(other_profit)
            except:
                other_profit_ = 0
            if Gross_profit.objects.filter(date__month=month,date__year=year,
            site='others').exists():
                gr = Gross_profit.objects.get(date__month=month,date__year=year,
                site='others')
                gr.amount = other_amount_
                gr.quantity = other_quantity
                gr.amountcomponents = 0
                gr.grossprofit = other_profit_
                gr.grossprofitcomponents = 0
                gr.rentability = other_rentability
                gr.totalSales = TotalSales
                gr.totalProfit = TotalProfit
                gr.sumSales = SumSales
                gr.sumProfit = SumProfit
                gr.quantity_total = Total_
                gr.date = now
                gr.save()
            else:
                gr = Gross_profit.objects.create(date=now,
                site='others',rentability=other_rentability,
                amount=other_amount_, quantity=other_quantity, grossprofit=other_profit_,
                amountcomponents=0, totalSales=TotalSales, totalProfit=TotalProfit,
                grossprofitcomponents=0, quantity_total=Total_,
                sumSales=SumSales, sumProfit=SumProfit)

    if both.exists():
        dict_profit['amount'] = both.distinct().aggregate(Total=Sum('amount'))['Total']
        dict_profit['quantity'] = both.distinct().aggregate(Total=Sum('quantity'))['Total']
        dict_profit['grossprofit'] = both.distinct().aggregate(Total=Sum('grossprofit'))['Total']
        dict_profit['rentability'] = get_rentability_avg(
        list(both.distinct().values_list('amount',flat=True)),
        list(both.distinct().values_list('rentability',flat=True))
        )
        return dict_profit
    else:
        return dict_profit

def stats_cash_rate_already(man, sum, month, year):
    # метод для записи по периоду в Statistics_service "уже получил"
    if not Statistics_service.objects.filter(
    date__month=month,date__year=year, managers__name=man.name).exists():
        if Statistics_service.objects.filter(managers__name=man.name).exists():
            st_last = Statistics_service.objects.filter(managers__name=man.name).last()
            st = Statistics_service.objects.create(
            managers=man, service=st_last.service, site=man.site, cash_rate_already=sum)
        else:
            serv = Service.objects.get_or_create(kind='Офисный менеджер')
            st = Statistics_service.objects.create(
            managers=man, service=serv[0], site=man.site, cash_rate_already=sum)
    else:
        st_period = Statistics_service.objects.filter(managers__name=man.name,
        date__month=month,date__year=year)
        st_period.update(cash_rate_already=sum, date=timezone.now())

def versum_or_it(item, sum, month, year):
    if item.find('ЗП') != -1:
        try:
            name_ = item.split('ЗП')[-1].strip()
            man = Managers.objects.get(name=name_)
            man.cash_rate_already = sum # может уже не нужно (есть stats_cash_rate_already)
            stats_cash_rate_already(man, sum, month, year)
            man.save()
            site_ = man.site
            return site_
        except:
            return 'both'
    if re.findall(r'versum|версум',item.lower()):
        return 'versum'
    elif re.findall(r'ит-блок|it-blok|фёдоров',item.lower()):
        return 'itblok'
    else:
        return 'both'

def get_avg_check(site_, price_, month, year, now):

    sal = Salary(month, year)
    exp = ExpenseRules(month, year)
    salary_exp_var = sal.sum_salary_no_stavka() / 2 # сумма процентных ставок | 2
    salary_exp_plan = sal.salary_for_plan_exp() # зп-ставки для плановых трат | 2

    if site_ == 'versum':
        count_ = sal.get_count_comp(site_='versum')
        hand_check_ = exp.get_sum_var_mark_versum(salary_exp_var, per_comps=count_) #оперативныe траты|компы
        plan_check_ = exp.get_sum_plan_mark_versum(salary_exp_plan) # плановые траты(статьи + ставки)
    elif site_ == 'itblok':
        count_ = sal.get_count_comp(site_='itblok')
        hand_check_ = exp.get_sum_var_mark_itblok(salary_exp_var, per_comps=count_) #оперативныe траты|компы
        plan_check_ = exp.get_sum_plan_mark_itblok(salary_exp_plan) # плановые траты(статьи + ставки)
    else:
        return 0
    if not Average_check.objects.filter(date__month=month,date__year=year, site=site_).exists():
        if Average_check.objects.filter(site=site_).exists():
            avg_last = Average_check.objects.filter(site=site_).last()
            average_check_versum = Average_check.objects.create(site=site_, quantity=avg_last.quantity,
            price=price_, hand_check=hand_check_, plan_check=plan_check_, date=now)
        else:
            average_check_versum = Average_check.objects.create(site=site_, price=price_,
            date=now, hand_check=hand_check_, plan_check=plan_check_)
    else:
        avg = Average_check.objects.filter(date__month=month,date__year=year, site=site_).last()
        avg.price = price_
        avg.hand_check = hand_check_
        avg.plan_check = plan_check_
        avg.date = now
        avg.save()

def transformations(data_one):
    now = timezone.now()
    try:
        data_one_date = data_one['StartDate']
        data_one_date_list = data_one_date.split('-')
        a,b,c = [int(x) for x in data_one_date_list[:]]
        now = datetime.datetime(a, b, c)
        month, year = data_one_date_list[1], data_one_date_list[0]
    except:
        month, year = now.strftime("%m"), now.strftime("%Y")

    name_ = now.strftime("%d %B %Y, %H:%M")
    r = One_C.objects.create(name='name_')
    r.json_data = data_one
    r.save()

    if not isinstance(data_one, dict) or 'error' in data_one:
        return None

    if 'Chapter' in data_one and data_one['Chapter'] == 'Остатки' and 'remainder' in data_one and isinstance(data_one['remainder'], list):
        remainder_old = Parts_full.objects.exclude(remainder=None)
        data_one_set = set()
        count_update = 0
        count_create = 0
        for e in data_one['remainder']:
            try:
                data_one_set.add(e['product_id'].strip())
                try:
                    cost = float(re.sub(r',','.', e['cost']))
                except:
                    cost = 0
                product_id = e['product_id'].strip()
                product = e['product'].strip()
                if Parts_full.objects.filter(partnumber_parts=product_id, providers__name_provider='-').exists():
                    full = Parts_full.objects.filter(partnumber_parts=product_id, providers__name_provider='-')
                    full.filter(availability_parts='yes').update(remainder=f"price:{cost}; {e['quantity']}", date_chg=now)
                    full.filter(availability_parts__in=('no', 'q')).update(remainder=f"price:{cost}; {e['quantity']}",
                    date_chg=now, availability_parts='yes', providerprice_parts=cost)
                    count_update += 1
                else:
                    kind_ = trans_remainder_category(e)
                    prov_main = Providers.objects.get(name_provider='-')
                    Parts_full.objects.create(name_parts=product,
                    partnumber_parts=product_id, providers=prov_main,
                    date_chg=now, providerprice_parts=cost, kind=kind_,
                    availability_parts='yes',remainder=f"price:{cost}; {e['quantity']}")
                    count_create += 1
            except:
                pass
        remainder_old.exclude(partnumber_parts__in=data_one_set).update(remainder=None)

    if 'Chapter' in data_one and data_one['Chapter'] == 'Расходы' and 'expense' in data_one and isinstance(data_one['expense'], list):
        for e in data_one['expense']:
            e['item'] = e['item'].strip()
            e['sum'] = e['sum']
            site_ = versum_or_it(e['item'], e['sum'], month, year)
            if Expense.objects.filter(date__month=month,date__year=year,discr=e['item']).exists():
                try:
                    ex = Expense.objects.get(date__month=month,date__year=year,discr=e['item'])
                    ex.amount = e['sum']
                    ex.date = now
                    ex.save()
                except:
                    group_name = Expense.objects.filter(date__month=month,date__year=year,
                    discr=e['item']).first().expense_groups
                    group_name = group_name.name if group_name else 'Другие растраты'
                    Expense.objects.filter(date__month=month,date__year=year,discr=e['item']).delete()
                    gr,_ = Expense_groups.objects.get_or_create(name=group_name)
                    Expense.objects.create(date=now, amount=e['sum'],discr=e['item'],expense_groups=gr,
                    site=site_)
            else:
                group_name = Expense.objects.filter(discr=e['item']).first()
                if group_name:
                    gr = group_name.expense_groups
                else:
                    gr,_ = Expense_groups.objects.get_or_create(name='Другие растраты')
                try:
                    Expense.objects.create(date=now, amount=e['sum'],discr=e['item'],expense_groups=gr, site=site_)
                except:
                    Expense.objects.create(date=now, amount=0,discr='error',expense_groups=gr, site=site_)
        if not Expense.objects.filter(date__month=month,date__year=year,expense_groups__name='Ручные поля').exists():
            gr,_ = Expense_groups.objects.get_or_create(name='Ручные поля')
            for s in set(Expense.objects.filter(expense_groups__name='Ручные поля').values_list('discr', flat=True)):
                exp_last = Expense.objects.filter(expense_groups__name='Ручные поля', discr=s).last()
                Expense.objects.create(date=now,discr=s,expense_groups=gr,
                site=exp_last.site, amount=exp_last.amount)

        expense_all = Expense.objects.filter(is_active=True, date__month=month,date__year=year)
        expense_both = expense_all.filter(site='both')
        expense_versum = expense_all.filter(site='versum')
        expense_itblok = expense_all.filter(site='itblok')
        summa_both = round(expense_both.distinct().aggregate(Total=Sum('amount'))['Total'])
        summa_versum = round(expense_versum.distinct().aggregate(Total=Sum('amount'))['Total'])
        summa_itblok = round(expense_itblok.distinct().aggregate(Total=Sum('amount'))['Total'])
        expense_both.update(summa=summa_both)
        expense_versum.update(summa=summa_versum)
        expense_itblok.update(summa=summa_itblok)

    if 'Chapter' in data_one and data_one['Chapter'] == 'Валовая прибыль' and 'data' in data_one and isinstance(data_one['data'], list):
        if 'TotalSales' in data_one and 'TotalProfit' in data_one and 'Total' in data_one and \
        'SumSales' in data_one and 'SumProfit' in data_one:
            TotalSales, TotalProfit, Total_, SumSales, SumProfit = (data_one['TotalSales'],
            data_one['TotalProfit'], data_one['Total'], data_one['SumSales'], data_one['SumProfit'])
        else:
            TotalSales, TotalProfit, Total_ = 0, 0, 0
        for d in data_one['data']:
            d['Customer'] = for_Customer[d['Customer']]
            if Gross_profit.objects.filter(date__month=month,date__year=year,
            site=d['Customer']).exists():
                gr = Gross_profit.objects.get(date__month=month,date__year=year,
                site=d['Customer'])
                gr.amount = round(d['amount'])
                gr.quantity = d['Quantity']
                gr.amountcomponents = d['amountcomponents']
                gr.grossprofit = round(d['grossprofit'])
                gr.grossprofitcomponents = round(d['grossprofitcomponents'])
                gr.rentability = round(d['rentability'], 1)
                gr.totalSales = TotalSales
                gr.totalProfit = TotalProfit
                gr.sumSales = SumSales
                gr.sumProfit = SumProfit
                gr.quantity_total = Total_
                gr.date = now
                gr.save()
            else:
                gr = Gross_profit.objects.create(date=now,
                site=d['Customer'],rentability=round(d['rentability'], 1),
                amount=round(d['amount']), quantity=d['Quantity'], grossprofit=round(d['grossprofit']),
                amountcomponents=d['amountcomponents'],
                grossprofitcomponents=round(d['grossprofitcomponents']), quantity_total=Total_,
                totalSales=TotalSales, totalProfit=TotalProfit,
                sumSales=SumSales, sumProfit=SumProfit)
            try:
                price_ = round(d['amount'] / d['Quantity'])
            except:
                try:
                    price_ = Average_check.objects.filter(site=site_).last().price
                except:
                    price_ = 30000
            get_avg_check(d['Customer'], price_, month, year, now)

        data_avg = get_sum_profit(month, year, TotalSales, TotalProfit, Total_, SumSales, SumProfit)
        if data_avg:
            if Gross_profit.objects.filter(date__month=month,date__year=year,
            site='both').exists():
                gr = Gross_profit.objects.get(date__month=month,date__year=year,
                site='both')
                gr.amount = round(data_avg['amount'])
                gr.quantity = data_avg['quantity']
                gr.grossprofit = round(data_avg['grossprofit'])
                gr.rentability = round(data_avg['rentability'], 1)
                gr.totalSales = TotalSales
                gr.totalProfit = TotalProfit
                gr.sumSales = SumSales
                gr.sumProfit = SumProfit
                gr.quantity_total = Total_
                gr.date = now
                gr.save()
            else:
                gr = Gross_profit.objects.create(date=now,
                site='both', rentability=round(data_avg['rentability'], 1),
                amount=round(data_avg['amount']), quantity=data_avg['quantity'],
                grossprofit=round(data_avg['grossprofit']), quantity_total=Total_,
                totalSales=TotalSales, totalProfit=TotalProfit,
                sumSales=SumSales, sumProfit=SumProfit)

    if not Average_check.objects.filter(date__month=month,date__year=year, site='versum').exists():
        if Average_check.objects.filter(site='versum').exists():
            avg_last = Average_check.objects.filter(site='versum').last()
            average_check_versum = Average_check.objects.create(site='versum', quantity=avg_last.quantity,
            price=avg_last.price, hand_check=avg_last.hand_check, date=now)
        else:
            average_check_versum = Average_check.objects.create(site='versum', date=now)
        print(average_check_versum)
    if not Average_check.objects.filter(date__month=month,date__year=year, site='itblok').exists():
        if Average_check.objects.filter(site='itblok').exists():
            avg_last = Average_check.objects.filter(site='itblok').last()
            average_check_itblok = Average_check.objects.create(site='itblok', quantity=avg_last.quantity,
            price=avg_last.price, hand_check=avg_last.hand_check, date=now)
        else:
            average_check_itblok = Average_check.objects.create(site='itblok', date=now)
        print(average_check_itblok)

    if not Plan.objects.filter(date__month=month,date__year=year,
    site='versum').exists():
        if Plan.objects.filter(site='versum').exists():
            plan_last = Plan.objects.filter(site='versum').last()
            p = Plan.objects.create(plan=plan_last.plan, zero_plan=plan_last.zero_plan,
            profit_plan=plan_last.profit_plan, y_plan=plan_last.y_plan, site='versum', date=now)
        else:
            p = Plan.objects.create(site='versum', date=now)
    if not Plan.objects.filter(date__month=month,date__year=year,
    site='itblok').exists():
        if Plan.objects.filter(site='itblok').exists():
            plan_last = Plan.objects.filter(site='itblok').last()
            p = Plan.objects.create(plan=plan_last.plan, zero_plan=plan_last.zero_plan,
            profit_plan=plan_last.profit_plan, y_plan=plan_last.y_plan, site='itblok', date=now)
        else:
            p = Plan.objects.create(site='itblok', date=now)

    """if Expense.objects.filter(date__month=month, date__year=year).exists():
        ex = Expense.objects.filter(date__month=month,
        date__year=year).last().summa
    else:
        ex = 0
    if Gross_profit.objects.filter(date__month=month,date__year=year,
    site='both').exists():
        profit = Gross_profit.objects.get(date__month=month,date__year=year,
        site='both').rentability
    else:
        profit = 0
    if Koefficient.objects.all().exists():
        k = Koefficient.objects.last()
    else:
        k = Koefficient.objects.create(date=timezone.now())
    if Plan.objects.all().exists():
        p = Plan.objects.last()
    else:
        p = Plan.objects.create(date=timezone.now())
    p.plan = round((ex*100*k.hand)/profit) if profit else 0
    p.date = timezone.now()
    p.save()"""
