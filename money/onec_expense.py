from money.models import *
from django.utils import timezone
from django.db.models import Sum, Count, F
from money.salary import Salary
import re


class ExpenseRules:
    # Расходы запланированные и оперативные

    month, year = None, None

    dict_expense = {
                    'versum_plan_mark': ('Версум запланированные', 1),
                    'versum_reklama_mark':('Версум реклама', 1),
                    'versum_var_mark': ('Версум оперативные', 1),
                    'all_plan_mark': ('Общие запланированные', 2),
                    'all_var_mark': ('Общие оперативные', 2),
                    'itblok_plan_mark': ('Ит-Блок запланированные', 1),
                    'itblok_reklama_mark': ('Ит-Блок реклама', 1),
                    'itblok_var_mark': ('Ит-Блок оперативные', 1)
                    }


    def __init__(self, month, year):
        self.month, self.year = month, year

    def get_exp(self, source, mark, group_=False, amount_=False, group_mark=False):
        # Расходы по versum, itblok, both, tenders, others (expense_ или expense_.amount)

        month, year = self.month, self.year

        if group_ and not group_mark:
            expense_ = Expense.objects.filter(date__month=month, date__year=year,
            expense_groups__name=group_,
            site=source, is_active=True)
        elif group_mark and group_:
            expense_ = Expense.objects.filter(date__month=month, date__year=year,
            discr=mark, expense_groups__name=group_,
            site=source, is_active=True)
        else:
            expense_ = Expense.objects.filter(date__month=month, discr=mark,
            date__year=year, site=source, is_active=True)

        if amount_:
            try:
                return round(expense_.distinct().aggregate(Total=Sum('amount'))['Total'])
            except:
                return 0
        else:
            return expense_

    def get_profit(self, source, amount_=False, quantity_=False, grossprofit_=False, rentability_=False):
        # Валовый доход по versum, itblok, both, tenders, others (query или query.атрибут)

        month, year = self.month, self.year

        query =  Gross_profit.objects.filter(date__month=month,
                        date__year=year, site=source).last()

        if amount_:
            try:
                return query.amount # Оборот_ПК
            except:
                return 0
        elif quantity_:
            try:
                return query.quantity # Колличество_ПК
            except:
                return 0
        elif grossprofit_:
            try:
                return query.grossprofit # Прибыль_ПК
            except:
                return 0
        elif rentability_:
            try:
                return query.rentability # Наценка
            except:
                return 0
        else:
            return query

    def get_av_chk(self, site_, price_=False, quantity_=False, hand_check_=False,
    plan_check_=False):
        # Средний чек по versum, itblok (query или query.атрибут)
        # quantity - ручной план(кол компов плана, но не влияет на компы окупаемости)

        month, year = self.month, self.year

        try:
            query =  Average_check.objects.filter(date__month=month,
                        date__year=year, site=site_).last()
        except:
            query = None

        if price_:
            try:
                return query.price # Средний чек
            except:
                return 0
        elif quantity_:
            try:
                return query.quantity # ПК план
            except:
                return 0
        elif hand_check_:
            try:
                return query.hand_check # Средние траты
            except:
                return 0
        elif plan_check_:
            try:
                return query.plan_check # Запланированные траты
            except:
                return 0
        else:
            return query
# 
    def count_comp_null_plan(self, site_):
        # Получение comp_plan, comp_null, profit_count_, y_plan, error

        month, year = self.month, self.year

        sal = Salary(month, year)
        sal_plan = sal.get_plan(site_, past_period=True, view_full=True)
        av_chk = self.get_av_chk(site_)

        if av_chk:
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

        else:
            return (0, 0, 0, 0, 'нет av_chk')

    def new_post(self, source):
        # НП расходы / все компы сайта versum, itblok, ...
        month, year = self.month, self.year

        count = self.get_profit(source, quantity_=True) # кол компов

        exp_site = Expense.objects.filter(
        date__month=month, date__year=year, discr__icontains='НП',
        site=source, is_active=True)
        try:
            exp_site_post = round(exp_site.distinct().aggregate(Total=Sum('amount'))['Total'])
        except:
            exp_site_post = 0
        exp_site_post = exp_site_post if exp_site_post else 0

        try:
            res = round(exp_site_post / count)
        except:
            res = 0
        return (f'{exp_site} / {count} = {res}', res)

    def reklama_managers(self):
        # Эфективность рекламы
        # Выдает список словарей results с title - для общей стат

        month, year = self.month, self.year
        results = [{'tittle': '----', 'versum': '----',
        'itblok': '----', 'dates': (month, year), 'mark': 0}]

        rentability_versum = self.get_profit('versum', rentability_=True) / 100
        profit_versum = self.get_profit('versum')
        profit_itblok = self.get_profit('itblok')

        bids = Bids.objects.filter(istocnikZakaza='Инстаграм',
        date_ch__month=month, date_ch__year=year, status='Успішно виконаний')

        sum_ = bids.distinct().select_related('goods').annotate(num=F('goods__amount'),
        suma=F('goods__summa')).aggregate(Total=Sum(F('num')*F('suma')))['Total']
        sum_ = sum_ if sum_ else 0

        """count_bids = bids.filter(
        goods__kind='Системный блок').distinct().select_related(
        'goods').annotate(num=F('goods__amount')).aggregate(Total=Sum(F('num')))['Total']
        count_bids = count_bids if count_bids else 0"""

        # блок СММ
        mark = 'VERSUM Facebook (Instagram, реклама, конкурсы):'
        group_v='Версум реклама'
        exp_cmm_man = self.get_exp('versum', mark, group_=group_v, amount_=True, group_mark=True)

        man_cmm, _ = Managers.objects.get_or_create(name='СММ менеджер')

        reklama_profit_cmm = round(sum_ * rentability_versum - man_cmm.cash_rate - exp_cmm_man)
        # конец блок СММ

        # блок СММ Google реклама
        exp_google_query = Expense.objects.filter(date__month=month, date__year=year,
        expense_groups__name='Версум реклама',
        is_active=True).exclude(discr__iregex=r'facebook|instagram')
        exp_google = exp_google_query.distinct().aggregate(Total=Sum('amount'))['Total']
        exp_google = exp_google if exp_google else 0

        #versum_comp = Gross_profit.objects.filter(date__month=month, date__year=year, site='versum').last()
        count_versum_comp = profit_versum.quantity if profit_versum else 0
        #itblok_comp = Gross_profit.objects.filter(date__month=month, date__year=year, site='itblok').last()
        count_itblok_comp = profit_itblok.quantity if profit_itblok else 0

        man_google, _ = Managers.objects.get_or_create(name='Google менеджер')

        try:
            sum_versum = profit_versum.grossprofit + profit_versum.grossprofitcomponents
        except:
            sum_versum = 0
        reklama_profit_google = sum_versum - sum_ * rentability_versum - man_google.cash_rate - exp_google
        # конец блок Google реклама

        # itblok реклама
        try:
            sum_itblok = profit_itblok.grossprofit + profit_itblok.grossprofitcomponents
        except:
            sum_itblok = 0
        rentability_itblok = self.get_profit('itblok', rentability_=True) / 100
        reklama_profit_itblok = sum_itblok * rentability_itblok -\
        self.get_reklama_expense('itblok') - self.fedoroff_exp()
        # конец itblok реклама

        try:
            part_cmm = round((man_cmm.cash_rate + exp_cmm_man) / count_versum_comp) # Доля трат к компам
        except:
            part_cmm = 0

        try:
            part_g = round((man_google.cash_rate + exp_google) / count_versum_comp) # Доля трат к компам
        except:
            part_g = 0

        # Доля трат itblok реклама к компам
        try:
            part_it = round((self.get_reklama_expense('itblok') +\
            self.fedoroff_exp()) / count_itblok_comp)
        except:
            part_it = 0

        results.append(
        {'tittle': 'Прибыль соцсети', 'versum': reklama_profit_cmm, 'itblok': '----',
        'dates': (month, year), 'mark': 0})
        results.append(
        {'tittle': 'Прибыль контекста и сео V', 'versum': reklama_profit_google, 'itblok': '----',
        'dates': (month, year), 'mark': 0})
        results.append(
        {'tittle': 'Прибыль контекста IT', 'versum': '----', 'itblok': reklama_profit_itblok,
        'dates': (month, year), 'mark': 0})
        results.append(
        {'tittle': 'Доля трат соцсети', 'versum': part_cmm, 'itblok': '----',
        'dates': (month, year), 'mark': 0})
        results.append(
        {'tittle': 'Доля трат контекста и сео V', 'versum': part_g, 'itblok': '----',
        'dates': (month, year), 'mark': 0})
        results.append(
        {'tittle': 'Доля трат контекста IT', 'versum': '----', 'itblok': part_it,
        'dates': (month, year), 'mark': 0})

        return results

    def var_exp_stats(self):
        # Статистика операционных трат
        # Выдает список словарей results с title - для общей стат
        month, year = self.month, self.year
        sal = Salary(month, year)
        results = [{'tittle': '----', 'versum': '----',
        'itblok': '----', 'dates': (month, year), 'mark': 0}]

        profit_versum = self.get_profit('versum', quantity_=True) # Колличество компов versum
        profit_itblok = self.get_profit('itblok', quantity_=True) # Колличество компов itblok
        count_comp = sal.get_count_comp() # Колличество компов versum + itblok

        nds_ver = self.get_exp('versum', '', group_='НДС', amount_=True)
        nds_it = self.get_exp('itblok', '', group_='НДС', amount_=True)
        try:
            nds_ver_per_comps = round(nds_ver / profit_versum, 1)
        except:
            nds_ver_per_comps = 0
        try:
            nds_it_per_comps = round(nds_it / profit_itblok, 1)
        except:
            nds_it_per_comps = 0

        bank_ver = self.get_exp('versum', 'Услуги банка VERSUM', amount_=True)
        bank_it = self.get_exp('itblok', 'Услуги банка IT-Blok', amount_=True)
        try:
            bank_ver_per_comps = round(bank_ver / profit_versum, 1)
        except:
            bank_ver_per_comps = 0
        try:
            bank_it_per_comps = round(bank_it / profit_itblok, 1)
        except:
            bank_it_per_comps = 0

        expense_a = Expense.objects.filter(date__month=month, date__year=year,
        discr='Авто ремонт, бензин', is_active=True)
        try:
            car_exp = round(expense_a.distinct().aggregate(Total=Sum('amount'))['Total'])
        except:
            car_exp = 0

        try:
            kurier = round(((sal.salary_kurier()['ЗП'] + car_exp) / count_comp) / 2, 1)
        except:
            kurier = 0

        tovar, sklad = 0, 0
        if count_comp:
            tovar = round((sal.salary_tovar()['ЗП'] / count_comp) / 2, 1)
            sklad = round((sal.salary_sklad()['ЗП'] / count_comp) / 2, 1)

        #one_c = round((sal.salary_one_c()['ЗП'] / count_comp) / 2, 1)
        #kurier_office = round((sal.get_service('простой',
        #'Курьер').cash_rate * sal.plan_stavka()['Процент_ставка'] / count_comp) /2)
        kurier_office = round(
        sal.office_man()['ЗП'] / 2
        )

        temp_remontnik, temp_sborsik = 0, 0
        if count_comp:
            #temp_remontnik = 0
            if Managers.objects.filter(remontnik=True).exists():
                for man_ in Managers.objects.filter(remontnik=True):
                    temp_remontnik += float(sal.salary_service_man(man_)['ЗП'])
            temp_remontnik = round((temp_remontnik / 2) / count_comp, 1)
            #temp_sborsik = 0
            if Managers.objects.filter(sborsik=True).exists():
                for man_ in Managers.objects.filter(sborsik=True):
                    temp_sborsik += float(sal.salary_service_man(man_)['ЗП'])
            temp_sborsik = round((temp_sborsik / 2) / count_comp, 1)

        results.append(
        {'tittle': 'НДС + налог на прибыль 30%', 'versum': nds_ver_per_comps, 'itblok': nds_it_per_comps,
        'dates': (month, year), 'mark': 0})
        results.append(
        {'tittle': 'Растраты по НП', 'versum': self.new_post('versum')[1],
        'itblok': self.new_post('itblok')[1], 'dates': (month, year), 'mark': 0})
        results.append(
        {'tittle': 'Услуги банка', 'versum': bank_ver_per_comps,
        'itblok': bank_it_per_comps, 'dates': (month, year), 'mark': 0})
        results.append(
        {'tittle': 'Курьерские', 'versum': kurier, 'itblok': kurier,
        'dates': (month, year), 'mark': 0})
        results.append(
        {'tittle': 'Закупщик', 'versum': tovar, 'itblok': tovar,
        'dates': (month, year), 'mark': 0})
        results.append(
        {'tittle': 'Зав. складом', 'versum': sklad, 'itblok': sklad,
        'dates': (month, year), 'mark': 0})
        results.append(
        {'tittle': 'Сборка', 'versum': temp_sborsik, 'itblok': temp_sborsik,
        'dates': (month, year), 'mark': 0})
        """results.append(
        {'tittle': 'Оператор 1С', 'versum': one_c, 'itblok': one_c,
        'dates': (month, year), 'mark': 0})"""
        results.append(
        {'tittle': 'Офис менеджер', 'versum': kurier_office, 'itblok': kurier_office,
        'dates': (month, year), 'mark': 0})
        results.append(
        {'tittle': 'Сервис', 'versum': temp_remontnik, 'itblok': temp_remontnik,
        'dates': (month, year), 'mark': 0})

        return results

    def gradation_comps(self):
        # Кол компов по сайтам разных ценовых категорий:
        # ...

        month, year = self.month, self.year

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
            count_temp = Goods.objects.filter(bids__pk__in=set_bids_versum,
            kind='Системный блок',summa__lt=comp['cash_rate']).annotate(
            num=F('amount')).aggregate(Total=Sum(F('num')))['Total']
            count_temp = count_temp if count_temp else 0
            count_this_grad_versum = count_temp - count_versum
            count_versum += count_this_grad_versum

            count_temp = Goods.objects.filter(bids__pk__in=set_bids_itblok,
            kind='Системный блок',summa__lt=comp['cash_rate']).annotate(
            num=F('amount')).aggregate(Total=Sum(F('num')))['Total']
            count_temp = count_temp if count_temp else 0
            count_this_grad_itblok = count_temp - count_itblok
            count_itblok += count_this_grad_itblok

            temp_list.append(
            {'tittle': comp['kind'] + '-' + comp['sloznostPK'],
            'versum': count_this_grad_versum, 'itblok': count_this_grad_itblok,
            'dates': (month, year)})

        return temp_list

    def get_nds(self, site_, mark='НДС'):
        # versum, itblok - "НДС + налог на прибыль 30%" трат Expense
        month, year = self.month, self.year

        exp = Expense.objects.filter(expense_groups__name=mark,
        date__month=month, date__year=year, is_active=True, site=site_)
        total_ = exp.aggregate(total=Sum('amount'))['total']
        total_ = total_ if total_ else 0

        return total_

    def get_allo_rozetka(self, site_, mark='Маркетплейсы'):
        # versum, itblok - "Алло/Розетка -10% от продажи" трат
        month, year = self.month, self.year

        exp = Expense.objects.filter(expense_groups__name=mark,
        date__month=month, date__year=year, is_active=True, site=site_)
        total_ = exp.aggregate(total=Sum('amount'))['total']
        total_ = total_ if total_ else 0

        return total_

    def get_reklama_expense(self, source):
        # рекламные расходы

        month, year = self.month, self.year

        dict_source = {
        'versum': 'Версум реклама', 'itblok': 'Ит-Блок реклама',
        'tenders': '', 'others': ''
        }

        exp = Expense.objects.filter(expense_groups__name=dict_source[source],
        date__month=month, date__year=year, is_active=True)
        total_ = exp.aggregate(total=Sum('amount'))['total']
        total_ = total_ if total_ else 0

        return total_

    def get_marketplace(self):
        # Маркетплейсы: Алло, Розетка, get_marketplace - сумма расходов от них
        month, year = self.month, self.year

        exp = Expense_groups.objects.filter(expense__date__month=month, name='Маркетплейсы',
        expense__date__year=year, expense__is_active=True
        )

        if exp.exists():
            sum = exp.select_related(
            'expense__amount').aggregate(total=Sum('expense__amount'))['total']
            sum = sum if sum else 0
            return sum
        else:
            return 0

    def get_plan_mark(self, key_):
        # versum - Получение key_ трат

        month, year = self.month, self.year
        try:
            mark, _ = self.dict_expense[key_] # группа, 1 - для 1сайта, 2 - для обоих, и тд
        except:
            return 0

        exp = Expense.objects.filter(expense_groups__name=mark,
        date__month=month, date__year=year, is_active=True)
        total_ = exp.aggregate(total=Sum('amount'))['total']
        total_ = total_ if total_ else 0

        return round(total_ / _ , 1)

    def get_sum_plan_mark_versum(self, salary_exp):
        # versum - Получение запланированных трат
        #salary_exp - сумма ставок-зп от работников salary-класса
        # + self.get_plan_mark('versum_reklama_mark') вычеркнул

        try:
            salary_exp_ = float(salary_exp)
        except:
            salary_exp_ = 0

        return round(self.get_plan_mark('versum_plan_mark') + salary_exp_ + self.get_plan_mark('all_plan_mark'))

    def get_sum_plan_mark_itblok(self, salary_exp):
        # itblok - Получение запланированных трат
        #salary_exp - сумма ставок-зп от работников salary-класса
        # + self.get_plan_mark('itblok_reklama_mark') вычеркнул

        try:
            salary_exp_ = float(salary_exp)
        except:
            salary_exp_ = 0

        return round(self.get_plan_mark('itblok_plan_mark') + salary_exp_ + self.get_plan_mark('all_plan_mark'))

    def get_sum_var_mark_versum(self, salary_exp, per_comps=False):
        # versum - Получение оперативных трат
        #salary_exp - сумма %-зп от работников salary-класса

        try:
            salary_exp_ = float(salary_exp)
        except:
            salary_exp_ = 0

        sum_ = self.get_nds('versum') +\
        self.get_allo_rozetka('versum') + self.get_plan_mark('all_var_mark') +\
        salary_exp_ + self.get_plan_mark('versum_var_mark')

        if per_comps:
            try:
                return round(sum_ / per_comps)
            except:
                return 30000

        return round(sum_)

    def get_sum_var_mark_itblok(self, salary_exp, per_comps=False):
        # itblok - Получение оперативных трат
        #salary_exp - сумма %-зп от работников salary-класса

        try:
            salary_exp_ = float(salary_exp)
        except:
            salary_exp_ = 0

        sum_ = self.get_nds('itblok') +\
        self.get_allo_rozetka('itblok') + self.get_plan_mark('all_var_mark') +\
        salary_exp_ + self.get_plan_mark('itblok_var_mark')

        if per_comps:
            try:
                return round(sum_ / per_comps)
            except:
                return 30000

        return round(sum_)

    def fedoroff_exp(self):
        # Расходы - доля по Федорову: 0.1 * оборот айтиблока - общ расходы
        # kurier_exp = (компы * (ставка * коэф плана + процент)/компы) / 2 пополам -устар
        month, year = self.month, self.year

        sal = Salary(month, year)
        stavka = sal.get_service('простой', 'Курьер').cash_rate
        rate_serve = sal.plan_stavka() # плановый пониж коэффициент
        stavka = rate_serve['Процент_ставка'] * stavka
        #kurier_exp = (sal.get_count_comp() * sal.salary_kurier(plan_stavka_=True, per_comps=True) -\
        #stavka) / 2
        kurier_exp = sal.salary_kurier(no_stavka=False)['ЗП']

        fedoroff_nenegative = self.get_plan_mark('all_var_mark') +\
        self.get_plan_mark('itblok_var_mark') + kurier_exp

        try:
            fedoroff_positve = 0.1 * (self.get_profit('itblok').amount +\
            self.get_profit('itblok').amountcomponents)
        except:
            return 0
        return round((fedoroff_positve - fedoroff_nenegative) / 2)
