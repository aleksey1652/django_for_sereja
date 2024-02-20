from money.models import *
import datetime
from django.utils import timezone
from django.db.models import Sum, Count, F
from django.contrib import messages
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
#from cat.models import One_C, Providers, Parts_full
import re
#from load_form_providers.load_element import to_article2_1
#from money.service import trans_remainder_category_dict
from money.salary import Salary
from money.onec_expense import ExpenseRules

class StatsRules:
    # раздел статистики: детальная инфа по расходам, доходам, планам

    month, year, site = None, None, None

    def __init__(self, site, month, year):
        self.site, self.month, self.year =\
        site, month, year


    def get_managers_and_exp(self):
        # Возвращает man_no_plan_stavka_, man_plan_stavka_, exp_, exp_all
        # используя данные от иницмализации класса

        mark = 'Версум запланированные' if self.site == 'versum' else 'Ит-Блок запланированные'
        groups_name_ = (
                        'buh_group', 'glav_buh_group', 'razrab_group',
                        'sklad_group', 'tovar_group'
                        )

        groups_plan_stavka_ = (
                        'kurier_group', 'one_c_group', 'test_group',
                        'sborsik_group'
                        )
        man_no_plan_stavka_ = Managers.objects.filter(
        family__groups__name__in=groups_name_).distinct() # ЗП-ставки

        man_plan_stavka_ = Managers.objects.filter(
        family__groups__name__in=groups_plan_stavka_).distinct() # ЗП-ставки с учетом плана

        exp_ = Expense.objects.filter(expense_groups__name=mark,
        date__month=self.month, date__year=self.year, is_active=True) # Плановые расх сайта

        exp_all = Expense.objects.filter(expense_groups__name='Общие запланированные',
        date__month=self.month, date__year=self.year, is_active=True) # Плановые расх общие

        return (man_no_plan_stavka_, man_plan_stavka_, exp_, exp_all)


    def sales_plan(self):
        # детальная инфа по ЗП-ставки/ЗП-ставки с учетом плана (используется как отдельная
        # стат, так и для Общие запл. Растраты)
        list_result = []
        sal = Salary(self.month, self.year)

        rate_serve = sal.plan_stavka() # плановый пониж коэффициент
        stavka = rate_serve['Процент_ставка']

        man_no_plan_stavka_, man_plan_stavka_, exp_, exp_all = self.get_managers_and_exp()

        dict_res = {'title': 'ЗП-фиксированные ставки'}
        list_res = man_no_plan_stavka_.values('family__groups__name', 'cash_rate')
        temp = {x['family__groups__name']: x['cash_rate'] for x in list_res}
        dict_res.update(temp)
        sum_no_plan = man_no_plan_stavka_.aggregate(Total=Sum('cash_rate'))['Total']
        sum_no_plan = sum_no_plan if sum_no_plan else 0
        dict_res['Сумма ЗП-фиксированные ставки'] = sum_no_plan
        list_result.append(dict_res)

        dict_res = {'title': 'ЗП-ставки зав от выполнения плана'}
        dict_res['Процент_ставка'] = stavka
        list_res = man_plan_stavka_.values('name', 'cash_rate')
        temp = {x['name']: x['cash_rate'] for x in list_res}
        dict_res.update(temp)
        sum_plan = man_plan_stavka_.aggregate(Total=Sum('cash_rate')*stavka)['Total']
        sum_plan = sum_plan if sum_plan else 0
        dict_res['Сумма ЗП-ставки зав от выполнения плана'] = sum_plan
        list_result.append(dict_res)

        return (list_result, sum_no_plan, sum_plan, exp_, exp_all)


    def all_plan_exp(self, summa):
        # детальная инфа по Общие запл. Растраты
        # if param == 'Общие запл. Растраты'

        sal = Salary(self.month, self.year)
        exp = ExpenseRules(self.month, self.year)
        stavka_sum_half = sal.salary_for_plan_exp(half=True)
        # рассчет summa, как параметр не используется
        if self.site == 'versum':
            summa = exp.get_sum_plan_mark_versum(stavka_sum_half)
        else:
            summa = exp.get_sum_plan_mark_itblok(stavka_sum_half)

        list_result, sum_no_plan, sum_plan, exp_, exp_all = self.sales_plan() # ЗП-ставки

        stavka_sum = (sum_no_plan + sum_plan) / 2

        dict_res = {'title': f'Итого сумма ставок-зп: ({sum_no_plan} + {sum_plan})/2'}
        dict_res['сумма ставок-зп'] = stavka_sum
        list_result.append(dict_res)

        dict_res = {'title': f'Траты плановые {self.site}'}
        list_res = exp_.values('discr', 'amount')
        temp = {x['discr']: x['amount'] for x in list_res}
        dict_res.update(temp)
        sum_exp = exp_.aggregate(total=Sum('amount'))['total']
        sum_exp = sum_exp if sum_exp else 0
        dict_res[f'Траты плановые {self.site}, сумма'] = sum_exp
        list_result.append(dict_res)

        dict_res = {'title': 'Траты all_plan_mark(общ на 2 проэкта) / 2'}
        list_res = exp_all.values('discr', 'amount')
        temp = {x['discr']: x['amount'] for x in list_res}
        dict_res.update(temp)
        sum_exp_all = exp_all.aggregate(total=Sum('amount'))['total']
        sum_exp_all = sum_exp_all if sum_exp_all else 0
        dict_res['Траты плановые на 2 проэкта, сумма/2'] = sum_exp_all / 2
        list_result.append(dict_res)

        dict_res = dict()
        dict_res['title'] = f'ставки-зп: {stavka_sum} + траты плановые {self.site}: {sum_exp} + Траты общ на 2 проэкта / 2: {sum_exp_all / 2}'
        dict_res['Итого общ запл. траты, сумма'] = summa
        list_result.append(dict_res)

        return list_result


    def var_sales(self):
        # ЗП-проценты (сумма процентных ставок)

        sal = Salary(self.month, self.year)
        temp_remontnik, temp_sborsik = 0, 0

        if Managers.objects.filter(remontnik=True).exists():
            for man_ in Managers.objects.filter(remontnik=True):
                temp_remontnik += float(sal.salary_service_man(man_)['ЗП'])
        temp_sborsik = 0
        if Managers.objects.filter(sborsik=True).exists():
            for man_ in Managers.objects.filter(sborsik=True):
                temp_sborsik += float(sal.salary_service_man(man_)['ЗП'])

        dict_res = {'title': 'Сумма процентных ставок'}
        dict_res['marketplace'] = sal.get_marketplace()
        dict_res['one_c'] = sal.salary_one_c()['ЗП']
        dict_res['kurier'] = sal.salary_kurier()['ЗП']
        dict_res['category_manager'] = sal.salary_category()['ЗП']
        dict_res['remontnik'] = temp_remontnik
        dict_res['sborsik'] = temp_sborsik
        sum = sal.sum_salary_no_stavka()
        dict_res['Итого по процентным ставкам'] = sum

        return (dict_res, sum)


    def exp_var_per_comps(self, summa):
        # детальная инфа по Траты оперативные/компы
        # if param == 'Траты оперативные/компы'

        list_result = []

        sal = Salary(self.month, self.year)
        exp = ExpenseRules(self.month, self.year)

        count_comp_v = exp.get_profit('versum', quantity_=True)
        count_comp_it = exp.get_profit('itblok', quantity_=True)

        # рассчет summa, как параметр не используется
        prozent_sum = (sal.sum_salary_no_stavka()) / 2
        if self.site == 'versum':
            summa = exp.get_sum_var_mark_versum(prozent_sum, per_comps=count_comp_v)
        else:
            summa = exp.get_sum_var_mark_itblok(prozent_sum, per_comps=count_comp_it)

        dict_res, sum = self.var_sales() # ЗП-проценты, sum = сумма процентных ставок
        list_result.append(dict_res)

        dict_res = {'title': 'Траты оперативные/компы (сумма строк ниже/компы)'}
        if self.site == 'versum':
            dict_res['компы'] = count_comp_v
            dict_res['Сумма процентных ставок / 2'] = sum / 2
            dict_res['nds'] = exp.get_nds('versum')
            dict_res['allo_rozetka'] = exp.get_allo_rozetka('versum')
            dict_res['Общие оперативные / 2'] = exp.get_plan_mark('all_var_mark')
            dict_res['Versum оперативные расходы'] = exp.get_plan_mark('versum_var_mark')
            dict_res['Траты оперативные/компы (versum), итого'] = summa
        else:
            dict_res['компы'] = count_comp_it
            dict_res['Сумма процентных ставок / 2'] = sum / 2
            dict_res['nds'] = exp.get_nds('itblok')
            dict_res['allo_rozetka'] = exp.get_allo_rozetka('itblok')
            dict_res['Общие оперативные / 2'] = exp.get_plan_mark('all_var_mark')
            dict_res['Itblok оперативные расходы'] = exp.get_plan_mark('itblok_var_mark')
            dict_res['Траты оперативные/компы (itblok), итого'] = summa
        list_result.append(dict_res)

        return list_result


    def stavka_plan_stavka(self, summa):
        # детальная инфа по ОЗП-ставки/ЗП-проценты
        # if param == 'ЗП-ставки/ЗП-проценты'

        list_result, sum_no_plan, sum_plan, exp_, exp_all = self.sales_plan()
        stavka_sum = (sum_no_plan + sum_plan) / 2 # ЗП-ставки

        dict_res = {'Сумма ставок / 2': stavka_sum}
        list_result.append(dict_res)

        dict_res, sum = self.var_sales() # ЗП-проценты, sum = сумма процентных ставок
        dict_res['Сумма процентных ставок / 2'] = sum / 2
        list_result.append(dict_res)

        return list_result


    def exp_reklama(self, summa):
        # детальная инфа по Реклама
        # if param == 'Реклама'

        list_result = []

        dict_source = {
        'versum': 'Версум реклама', 'itblok': 'Ит-Блок реклама',
        'tenders': '', 'others': ''
        }

        exp_source = Expense.objects.filter(expense_groups__name=dict_source[self.site],
        date__month=self.month, date__year=self.year, is_active=True)
        total_ = exp_source.aggregate(total=Sum('amount'))['total']
        total_ = total_ if total_ else 0

        dict_res = {'title': 'детальная инфа по Реклама'}
        list_res = exp_source.values('discr', 'amount')
        temp = {x['discr']: x['amount'] for x in list_res}
        dict_res.update(temp)
        dict_res['Итого, реклама'] = total_
        list_result.append(dict_res)

        return list_result


    def fedoroff(self, summa):
        # детальная инфа по Федоров
        # if param == 'Федоров'

        list_result = []

        sal = Salary(self.month, self.year)
        exp = ExpenseRules(self.month, self.year)

        try:
            kurier_man = Managers.objects.get(family__groups__name='kurier_group')
        except:
            kurier_man = None
        service = sal.get_service('простой', 'Курьер')
        if Statistics_service.objects.filter(managers=kurier_man, service=service,
        date__month=self.month, date__year=self.year).exists():
            try:
                st = Statistics_service.objects.get(managers=kurier_man, service=service,
                date__month=self.month, date__year=self.year)
            except:
                st = Statistics_service.objects.filter(managers=kurier_man, service=service,
                date__month=self.month, date__year=self.year).last()
            km_ = st.km_count
        else:
            km_ = 0
        kurir_summa = km_ * service.summa

        dict_res = {'title': 'курьерские расх / 2'}
        dict_res['sum_(/2)'] = kurir_summa / 2
        list_result.append(dict_res)

        dict_res = {'title': 'fedoroff_positve'}
        comps = exp.get_profit('itblok').amount
        comp_parts = exp.get_profit('itblok').amountcomponents
        dict_res['Оборот_ПК'] = comps
        dict_res['Оборот_деталиПК'] = comp_parts
        sum_positve = 0.1 * (comps + comp_parts)
        dict_res['Итого: 0.1 * (Оборот_деталиПК + Оборот_деталиПК)'] = round(sum_positve)
        list_result.append(dict_res)

        dict_res = {'title': 'fedoroff_nenegative'}
        all_var_mark =  exp.get_plan_mark('all_var_mark')
        itblok_var_mark = exp.get_plan_mark('itblok_var_mark')
        dict_res['Общие оперативные / 2'] = all_var_mark
        dict_res['Itblok оперативные расходы'] = round(itblok_var_mark)
        dict_res['Курьер / 2'] = kurir_summa / 2
        sum_nenegative = all_var_mark + itblok_var_mark + (kurir_summa / 2)
        dict_res['Итого, fedoroff_nenegative:'] = round(sum_nenegative)
        list_result.append(dict_res)

        dict_res = {'title': 'fedoroff_positve - fedoroff_nenegative'}
        dict_res['Итого'] = round(sum_positve - sum_nenegative)
        list_result.append(dict_res)

        return (list_result, round(sum_positve - sum_nenegative))


    def site_profit(self, summa):
        # детальная инфа по Прибыль
        # if param == 'Прибыль'

        sal = Salary(self.month, self.year)
        exp = ExpenseRules(self.month, self.year)

        list_result = []
        _, fedoroff_sum = self.fedoroff(0)

        if self.site == 'versum':
            dict_res = {'title': '1С прибыль Versum'}
            comps = exp.get_profit('versum').grossprofit
            comp_parts = exp.get_profit('versum').grossprofitcomponents
            versum_sum = comps + comp_parts
            dict_res['1С_ПК'] = comps
            dict_res['1С_ДеталиПК'] = comp_parts
            dict_res['1С_versum'] = versum_sum
        else:
            dict_res = {'title': '1С прибыль Itblok'}
            comps = exp.get_profit('itblok').grossprofit
            comp_parts = exp.get_profit('itblok').grossprofitcomponents
            itblok_sum = comps + comp_parts
            dict_res['1С_ПК'] = comps
            dict_res['1С_ДеталиПК'] = comp_parts
            dict_res['1С_itblok'] = itblok_sum
        list_result.append(dict_res)

        if self.site == 'versum':
            dict_res = {'title': 'Траты оперативные Versum'}
            prozent_sum = (sal.sum_salary_no_stavka()) / 2
            versum_var = exp.get_sum_var_mark_versum(prozent_sum)
            dict_res['sum_versum'] = versum_var
        else:
            dict_res = {'title': 'Траты оперативные Itblok'}
            prozent_sum = (sal.sum_salary_no_stavka()) / 2
            itblok_var = exp.get_sum_var_mark_itblok(prozent_sum)
            dict_res['sum_itblok'] = itblok_var
        list_result.append(dict_res)

        if self.site == 'versum':
            dict_res = {'title': 'Общие запл. Растраты Versum'}
            stavka_sum_half = sal.salary_for_plan_exp(half=True)
            versum_plan = exp.get_sum_plan_mark_versum(stavka_sum_half)
            dict_res['sum_versum'] = versum_plan
        else:
            dict_res = {'title': 'Общие запл. Растраты Itblok'}
            stavka_sum_half = sal.salary_for_plan_exp(half=True)
            itblok_plan = exp.get_sum_plan_mark_itblok(stavka_sum_half)
            dict_res['sum_itblok'] = itblok_plan
        list_result.append(dict_res)

        if self.site == 'versum':
            dict_res = {'title': 'Реклама Versum'}
            versum_reklama = exp.get_reklama_expense('versum')
            dict_res['reklama_versum'] = versum_reklama
        else:
            dict_res = {'title': 'Реклама Itblok'}
            itblok_reklama = exp.get_reklama_expense('itblok')
            dict_res['reklama_itblok'] = itblok_reklama
        list_result.append(dict_res)

        if self.site == 'versum':
            dict_res = {'title': 'Прибыль Versum'}
            versum_summa = versum_sum - versum_var - versum_plan - versum_reklama
            dict_res['1С прибыль Versum - Траты оперативные Versum - Общие запл. Растраты Versum - Реклама Versum'] = versum_summa
        else:
            dict_res = {'title': 'Прибыль Itblok'}
            dict_res['fedoroff'] = fedoroff_sum
            itblok_summa = itblok_sum - itblok_var - itblok_plan - itblok_reklama - fedoroff_sum
            dict_res['1С прибыль Itblok - Траты оперативные Itblok - Общие запл. Растраты Itblok - Реклама Itblok - fedoroff'] = itblok_summa
        list_result.append(dict_res)

        return list_result


    def plan_z_plan(self, summa):
        # детальная инфа по План/План_окупаемость за прощлый месяц!!!
        # if param == 'План/План_окупаемость'

        list_full = []

        month = int(self.month) - 1
        if month > 0:
            month, year = str(month), self.year
        else:
            month, year = '12', str(int(self.year) - 1)

        sal = Salary(month, year)
        exp = ExpenseRules(month, year)
        ratio_, _ = Ratios.objects.get_or_create() # коэф для ручных трат
        salary_exp_var = sal.sum_salary_no_stavka() / 2 # сумма процентных ставок | 2
        salary_exp_plan = sal.salary_for_plan_exp() # зп-ставки для плановых трат | 2

        if self.site == 'versum':
            plan_from_bd = sal.get_plan('versum', past_period=False, view_full=True) # план из бд(словарь)
            avg_chk = exp.get_av_chk('versum', price_=True) # ср чек
            rent = exp.get_profit('versum', rentability_=True) # наценка
            rent = rent /100 if rent else 1
            count_ = sal.get_count_comp(site_='versum') # кол компов
            hand_check_ = exp.get_sum_var_mark_versum(salary_exp_var, per_comps=count_)
            temp_result = self.exp_var_per_comps(hand_check_)
            # hand_check_, exp_var_per_comps --- оперативныe траты|компы(summa), детальная инфа
            # по оперативныe траты|компы
            list_full += temp_result
            plan_check_ = exp.get_sum_plan_mark_versum(salary_exp_plan)
            # плановые траты(статьи + ставки)
            temp_result = self.all_plan_exp(plan_check_)
            list_full += temp_result

            summa_hand = round((avg_chk * ratio_.versum_ratio)) # ручные траты
            profit_count_plan = avg_chk * rent - summa_hand - hand_check_ #прибыль расчётная
            #для плана
            try:
                count_comp_null_plan = plan_check_ / profit_count_plan
            except:
                count_comp_null_plan = 0
            #количество компов для
            #окупаемости для плана

            try:
                y_plan = 25 * plan_check_ / (count_comp_null_plan * (25 * profit_count_plan - avg_chk))
                #коефициент наценки для выполнения плана
            except:
                y_plan = 1

            plan_ = round((count_comp_null_plan * (y_plan + 0.01)) * avg_chk, 2)
            # План

            plan_z = round(count_comp_null_plan * avg_chk, 2)
            # План_окупаемость

            temp_result = []
            dict_res = {'title': 'Итоговые цифры для плана'}
            dict_res['Ср. чек'] = avg_chk
            dict_res['Наценка'] = rent
            dict_res['Наценка'] = rent
            dict_res[f'Ручные траты: Ср. чек * {ratio_.versum_ratio}'] = summa_hand
            dict_res['Прибыль расчётная: Ср. чек * Наценка - Ручные траты - Траты оперативные/компы'] =\
            round(profit_count_plan)
            dict_res['Количество компов для окупаемости: Плановые траты / Прибыль расчётная'] =\
            round(count_comp_null_plan)
            dict_res['Коефициент наценки для выполнения плана: y_plan'] =\
            '25 * Плановые траты / (Количество компов для оку * (25 * Прибыль расчётная - Ср. чек))'
            dict_res['y_plan'] = round(y_plan, 2)
            dict_res['План'] =\
            '(Количество компов для оку * (y_plan + 0.01)) * Ср. чек'
            dict_res['Итого: План (рассчетный)'] = plan_
            dict_res['План_окупаемость (рассчетный): Количество компов для оку * Ср. чек'] =\
            plan_z
            dict_res['Итого: План'] = plan_from_bd['plan_now']
            dict_res['План_окупаемость: Количество компов для оку * Ср. чек'] =\
            plan_from_bd['zero_plan']

            temp_result.append(dict_res)

            list_full += temp_result

        else:
            plan_from_bd = sal.get_plan('itblok', past_period=False, view_full=True) # план из бд(словарь)
            avg_chk = exp.get_av_chk('itblok', price_=True) # ср чек
            rent = exp.get_profit('itblok', rentability_=True) # наценка
            rent = rent /100 if rent else 1
            count_ = sal.get_count_comp(site_='itblok')
            hand_check_ = exp.get_sum_var_mark_itblok(salary_exp_var, per_comps=count_)
            temp_result = self.exp_var_per_comps(hand_check_)
            # hand_check_, exp_var_per_comps --- оперативныe траты|компы(summa), детальная инфа
            # по оперативныe траты|компы
            list_full += temp_result
            plan_check_ = exp.get_sum_plan_mark_itblok(salary_exp_plan)
            # плановые траты(статьи + ставки)
            temp_result = self.all_plan_exp(plan_check_)
            list_full += temp_result

            summa_hand = round((avg_chk * ratio_.itblok_ratio)) # ручные траты
            profit_count_plan = avg_chk * rent - summa_hand - hand_check_ #прибыль расчётная
            #для плана
            try:
                count_comp_null_plan = plan_check_ / profit_count_plan
            except:
                count_comp_null_plan = 0
            #количество компов для
            #окупаемости для плана

            try:
                y_plan = 25 * plan_check_ / (count_comp_null_plan * (25 * profit_count_plan - avg_chk))
                #коефициент наценки для выполнения плана
            except:
                y_plan = 1

            plan_ = round((count_comp_null_plan * (y_plan + 0.01)) * avg_chk, 2)
            # План

            plan_z = round(count_comp_null_plan * avg_chk, 2)
            # План_окупаемость

            temp_result = []
            dict_res = {'title': 'Итоговые цифры для плана'}
            dict_res['Ср. чек'] = avg_chk
            dict_res['Наценка'] = rent
            dict_res['Наценка'] = rent
            dict_res[f'Ручные траты: Ср. чек * {ratio_.itblok_ratio}'] = summa_hand
            dict_res['Прибыль расчётная: Ср. чек * Наценка - Ручные траты - Траты оперативные/компы'] =\
            round(profit_count_plan)
            dict_res['Количество компов для окупаемости: Плановые траты / Прибыль расчётная'] =\
            round(count_comp_null_plan)
            dict_res['Коефициент наценки для выполнения плана: y_plan'] =\
            '25 * Плановые траты / (Количество компов для оку * (25 * Прибыль расчётная - Ср. чек))'
            dict_res['y_plan'] = round(y_plan, 2)
            dict_res['План'] =\
            '(Количество компов для оку * (y_plan + 0.01)) * Ср. чек'
            dict_res['Итого: План (рассчетный)'] = plan_
            dict_res['План_окупаемость (рассчетный): Количество компов для оку * Ср. чек'] =\
            plan_z
            dict_res['Итого: План'] = plan_from_bd['plan_now']
            dict_res['План_окупаемость: Количество компов для оку * Ср. чек'] =\
            plan_from_bd['zero_plan']

            temp_result.append(dict_res)

            list_full += temp_result

        return list_full


    def gross_profit_info(self, summa):
        # инфа по Валовая прибыль
        # if param == 'Оборот/Колличество ПК' или 'Ср чек/Наценка'

        list_result = []
        exp = ExpenseRules(self.month, self.year)

        amount_site = exp.get_profit(self.site, amount_=True) # оборот ПК
        quantity_site = exp.get_profit(self.site, quantity_=True) # кол ПК
        rentability_site = exp.get_profit(self.site, rentability_=True) # наценка

        dict_res = {'title': 'Инфа по валовой прибыли'}
        dict_res['оборот ПК'] = amount_site
        dict_res['кол ПК'] = quantity_site
        dict_res['наценка'] = rentability_site
        list_result.append(dict_res)

        return list_result
