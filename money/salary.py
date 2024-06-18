from money.models import *
from django.utils import timezone
from django.db.models import Sum, Count, F
import re

class Salary:
    # ЗП + кол компов + сервисы по категориям

    month, year = None, None

    def __init__(self, month, year):
        self.month, self.year = month, year

    def st_cash_rate_already(self, man):
        # метод для получения по периоду в Statistics_service "уже получил"
        month, year = self.month, self.year

        if Statistics_service.objects.filter(
        date__month=month,date__year=year, managers__name=man.name).exists():
            st_last = Statistics_service.objects.filter(
            date__month=month,date__year=year, managers__name=man.name
            ).last()
            return st_last.cash_rate_already
        else:
            return 0

    def yes_div_per_man(self, man, plan):
        # делим бонус на всех менеджеров сайта (man_test_group)
        month, year = self.month, self.year
        yes = 0.01
        count_ = 1
        if man.site in ('versum', 'itblok'):
            man_test_group = Managers.objects.filter(family__groups__name='test_group')
            count_ = man_test_group.filter(site=man.site).count()
            try:
                amount_ = Gross_profit.objects.get(date__month=dateqs.strftime("%m"),
                                date__year=dateqs.strftime("%Y"), site=man.site).amount
                # оборот версум, itblok
            except:
                amount_ = 0
            if amount_ >= plan:
                yes = 0.01
            else:
                yes = 0
            try:
                return round(yes / count_, 4)
            except:
                return 0
        else:
            return 0


    def get_count_comp(self, site_='both'):
        # Колличество компов
        month, year = self.month, self.year
        try:
            count_comp = Gross_profit.objects.get(date__month=month,date__year=year, site=site_).quantity
        except:
            count_comp = 0
        return count_comp

    def get_service(self, sloznostPK_, kind_):
        # Сервисы по категориям
        service,_ = Service.objects.get_or_create(sloznostPK=sloznostPK_,kind=kind_)

        return service

    def get_plan(self, site_, past_period=True, view_full=False):
        # План для прошлого периода(True), текущего(False)
        month, year = self.month, self.year
        if site_ == 'both':
            return 100000000
        if past_period:
            month = int(month) - 1
            if month > 0:
                month, year = str(month), year
            else:
                month, year = '12', str(int(year) - 1)
        plan_ = Plan.objects.filter(date__month=month, date__year=year, site=site_)

        plan_now = plan_.last().plan if plan_.exists() else 100000000
        zero_plan_ = plan_.last().zero_plan if plan_.exists() else 100000000
        profit_plan_ = plan_.last().profit_plan if plan_.exists() else 0
        y_plan_ = plan_.last().y_plan if plan_.exists() else 2

        if view_full:
            return {
                    'plan_now': plan_now, 'zero_plan': zero_plan_,
                    'profit_plan': profit_plan_, 'y_plan': y_plan_, 'date': (month, year)
                    }

        return plan_now

    def plan_stavka(self, past_period=True):
        # Процент_ставка для менеджеров both
        # План(только план) для прошлого периода(True), текущего(False)
        month, year = self.month, self.year
        count = 0

        if past_period:
            month_plan = int(month) - 1
            if month_plan > 0:
                month_plan, year_plan = str(month_plan), year
            else:
                month_plan, year_plan = '12', str(int(year) - 1)

        try:
            plan_versum = Plan.objects.get(date__month=month_plan, date__year=year_plan, site='versum')
            plan_itblok = Plan.objects.get(date__month=month_plan, date__year=year_plan, site='itblok')
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

    def get_marketplace(self):
        # Маркетплейсы: Алло, Розетка, get_marketplace - сумма расходов от них
        month, year = self.month, self.year

        exp = Expense_groups.objects.filter(expense__date__month=month, name='Маркетплейсы',
        expense__date__year=year, expense__is_active=True
        )

        if exp.exists():
            sum = exp.select_related('expense__amount').aggregate(total=Sum('expense__amount'))['total']
            sum = sum if sum else 0
            return sum
        else:
            return 0

    def salary_for_plan_exp(self, half=True, plan_stavka_=True):
        # зп-ставки для плановых трат

        if plan_stavka_:
            rate_serve = self.plan_stavka()
        else:
            rate_serve = {'Процент_ставка': 1}
        stavka = rate_serve['Процент_ставка']

        groups_name_ = (
                        'buh_group', 'glav_buh_group', 'razrab_group',
                        'sklad_group', 'tovar_group', 'office_group',
                        )

        groups_plan_stavka_ = (
                        'one_c_group', 'test_group', 'category_group',
                        'sborsik_group'
                        )
        man_no_plan_stavka_ = Managers.objects.filter(family__groups__name__in=groups_name_).distinct()
        stavka_man = man_no_plan_stavka_.aggregate(Total=Sum('cash_rate'))['Total']
        stavka_man_ = stavka_man if stavka_man else 0

        man_plan_stavka_ = Managers.objects.filter(
        family__groups__name__in=groups_plan_stavka_).distinct()
        stavka_man_stavka = man_plan_stavka_.aggregate(Total=Sum('cash_rate')*stavka)['Total']
        stavka_man_stavka_ = stavka_man_stavka if stavka_man_stavka else 0

        if half:
            return round((stavka_man_ + stavka_man_stavka_) / 2)
        else:
            return stavka_man_ + stavka_man_stavka_

    def salary_manager(self, man):
        # ЗП менеджеров включая категорийного category_group
        month, year = self.month, self.year

        bids_set = Bids.objects.filter(date_ch__month=month,date_ch__year=year,
        status='Успішно виконаний', managers=man)

        price_pc = bids_set.filter(goods__kind='Системный блок'
        ).distinct().select_related('goods').annotate(num=F('goods__amount'),
        suma=F('goods__summa')).aggregate(Total=Sum(F('num')*F('suma')))['Total']
        price_pc = price_pc if price_pc else 0

        price_parts = bids_set.filter(goods__kind='Комплектующие'
        ).distinct().select_related('goods').annotate(num=F('goods__amount'),
        suma=F('goods__summa')).aggregate(Total=Sum(F('num')*F('suma')))['Total']
        price_parts = price_parts if price_parts else 0

        price_office = bids_set.filter(istocnikZakaza='ПК вітрина 2%'
        ).select_related('goods').annotate(num=F('goods__amount'),
        suma=F('goods__summa')).aggregate(Total=Sum(F('num')*F('suma')))['Total']
        price_office = price_office if price_office else 0

        plan = self.get_plan(man.site)
        yes = self.yes_div_per_man(man, plan)
        if man.cash_rate:
            rate_serve = self.plan_stavka()
            rate = round(man.cash_rate * rate_serve['Процент_ставка'])
        else:
            rate = 0
        salary_dict = self.salary_team_manager(man)
        salary_dict['sum'] = round(price_pc * (0.01 + yes) + price_parts * 0.01 + price_office * 0.01 + rate)
        salary_dict['ЗП'] = f'Сис блоки: {price_pc} * (0.01 + {yes}), Компл: {price_parts} * 0.01, ПК_витрина: {price_office} * 0.01, Ставка: {rate}'
        salary_dict['Уже получил'] = self.st_cash_rate_already(man)

        """salary_dict = {
                        'sum': round(price_pc * (0.01 + yes) + price_parts * 0.01 + price_office * 0.01),
                        'ЗП': f'Сис блоки: {price_pc} * (0.01 + {yes}), Компл: {price_parts} * 0.01, ПК_витрина: {price_office}'
                        }"""
        return salary_dict

    def salary_team_manager(self, man):
        # общие (командные) продажи(сис блоки и комплектующие)
        # возможен подсчет при 'both' сайт
        month, year = self.month, self.year
        bids_kind = ('Системный блок', 'Комплектующие')
        dict_context = self.plan_stavka()

        for kind_ in bids_kind:
            if man.site == 'both':
                dict_context['team ' + kind_] = Bids.objects.filter(date_ch__month=month,date_ch__year=year,
                site__in=('versum', 'komputeritblok'), status='Успішно виконаний',
                goods__kind=kind_).distinct().select_related('goods').annotate(num=F('goods__amount'),
                suma=F('goods__summa')).aggregate(Total=Sum(F('num')*F('suma')))['Total']
            else:
                dict_context['team ' + kind_] = Bids.objects.filter(
                managers__site=man.site, status='Успішно виконаний',
                goods__kind=kind_).distinct().select_related('goods').annotate(
                num=F('goods__amount'),
                suma=F('goods__summa')).aggregate(Total=Sum(F('num')*F('suma')))['Total']

        return dict_context

    def salary_service_man(self, man, plan_stavka_=None, no_stavka=True, site_='both'):
        # ЗП сборщиков ремонтников
        month, year = self.month, self.year
        service_kind = ('Ремонт ПК', 'Обслуживание')
        dict_context = dict()
        count = 0
        rate = 0

        Statistics_per_period = Statistics_service.objects.filter(date__month=month,
        date__year=year, managers=man).distinct()

        if man.sborsik:
            try:
                rate = Service.objects.filter(kind='Сборка').first().cash_rate
            except:
                rate = 0
        if man.remontnik:
            try:
                rate = Service.objects.filter(kind='Ремонт ПК').first().cash_rate
            except:
                rate = 0

        if Statistics_per_period.exists():
            for stat in Statistics_per_period.values('service__kind',
            'service__sloznostPK', 'sborka_count', 'date', 'service__summa', 'pk'):
                if stat['service__kind'] == 'Сборка':
                    dict_context[f"Сборка ({stat['service__sloznostPK']}, {stat['date'].strftime('%m:%Y')}, №{stat['pk']})"] = {'st':(stat['sborka_count'], stat['service__summa']), 'st_pk': f"{stat['pk']}-st"}
                    count += stat['sborka_count'] * stat['service__summa']
                if stat['service__kind'] == 'Установка лед табличек':
                    dict_context[f"Лед таблички ({stat['service__sloznostPK']}, {stat['date'].strftime('%m:%Y')}, №{stat['pk']})"] = {'st':(stat['sborka_count'], stat['service__summa']), 'st_pk': f"{stat['pk']}-st"}
                    count += stat['sborka_count'] * stat['service__summa']
        if man.remontnik:
            all_serve = Service.objects.filter(kind__in=('Обслуживание',
            'Ремонт ПК')).values('kind', 'sloznostPK', 'summa')
            dict_context['Тарифы'] = [{f"{k['kind']}-{k['sloznostPK']}": k['summa']} for k in list(all_serve)]

            for stat in Statistics_per_period.values('service__kind', 'service__sloznostPK',
            'remont_count', 'date', 'service__summa', 'pk'):
                if stat['service__kind'] == 'Ремонт ПК':
                    dict_context[f"{stat['service__kind']} ({stat['service__sloznostPK']}, {stat['date'].strftime('%m:%Y')}, №{stat['pk']})"] = {'st': (stat['remont_count'], stat['service__summa']), 'st_pk': f"{stat['pk']}-st"}
                    count += stat['remont_count'] * stat['service__summa']

            for stat in Statistics_per_period.values('service__kind', 'service__sloznostPK','obsluj_count',
            'date', 'service__summa', 'pk'):
                if stat['service__kind'] == 'Обслуживание':
                    dict_context[f"{stat['service__kind']} ({stat['service__sloznostPK']}, {stat['date'].strftime('%m:%Y')}, №{stat['pk']})"] = {'st': (stat['obsluj_count'], stat['service__summa']), 'st_pk': f"{stat['pk']}-st"}
                    count += stat['obsluj_count'] * stat['service__summa']
        if plan_stavka_:
            stavka = self.plan_stavka()
        else:
            stavka = {'Процент_ставка': 1}
        stavka = self.plan_stavka()
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
        dict_context['ЗП'] = count + stavka_service if not no_stavka else count
        man_cash_rate_already = self.st_cash_rate_already(man)
        dict_context['Уже получил'] = {'st': man_cash_rate_already} if man_cash_rate_already else {'st': '0'}

        return dict_context

    def salary_one_c(self, plan_stavka_=None, no_stavka=True, site_='both'):
        # зп-1C, plan_stavka_=True - полная инфа и пониж коэф, None - краткая и без пониж коэф
        # plan_stavka_=True - полная инфа и пониж коэф, None - краткая и без пониж коэф
        # при no_stavka=True - только процент
        month, year = self.month, self.year
        try:
            one_man = Managers.objects.get(family__groups__name='one_c_group')
        except:
            one_man = None
        if one_man:
            if plan_stavka_:
                rate_serve = self.plan_stavka()
            else:
                rate_serve = {'Процент_ставка': 1}
            count = 0
            rate_serve['name'] =  one_man.name
            count_comp = self.get_count_comp()
            service = self.get_service('простой', 'Оператор 1С')

            stavka = round(service.cash_rate * rate_serve['Процент_ставка'])
            tarif = service.summa

            service_set = Statistics_service.objects.filter(managers=one_man, date__month=month, date__year=year)

            for stat in service_set.values(
            'service__sloznostPK', 'sborka_count', 'date', 'service__summa', 'pk'):
                count += stat['sborka_count'] * stat['service__summa']

            summa = stavka + (count_comp * tarif) + count

            if plan_stavka_:
                all_serve = Service.objects.filter(kind='Оператор 1С').values('sloznostPK', 'summa')
                rate_serve['Тарифы'] = [{k['sloznostPK']: k['summa']} for k in list(all_serve)]
                rate_serve['Ставка'] = service.cash_rate
                man_cash_rate_already = self.st_cash_rate_already(one_man)
                rate_serve['получил'] = man_cash_rate_already
                #rate_serve['получил'] = one_man.cash_rate_already
                rate_serve['Дополнительно добавленные'] = count
                rate_serve['ЗП'] = f'Ставка: {stavka} + Кол компов: {count_comp} * {tarif} + {count},\
                Итого: {summa}'
            else:
                rate_serve['ЗП'] = summa if not no_stavka else (count_comp * tarif) + count
            return rate_serve

        else:
            return {'ЗП': 0}

    def salary_glav_buh(self, plan_stavka_=None, no_stavka=True):
        # зп-главбух, plan_stavka_=True - полная инфа и пониж коэф, None - краткая и без пониж коэф
        # no_stavka=True - пока не используется
        month, year = self.month, self.year
        try:
            glav_buh_man = Managers.objects.get(family__groups__name='glav_buh_group')
        except:
            glav_buh_man = None
        if glav_buh_man:
            if plan_stavka_:
                rate_serve = {'Процент_ставка': 1}
            else:
                rate_serve = {'Процент_ставка': 1}
            count = 0
            rate_serve['name'] =  glav_buh_man.name
            service = self.get_service('простой', 'Глав бух')
            stavka = round(service.cash_rate * rate_serve['Процент_ставка'])

            rate_serve['ЗП'] = stavka
            man_cash_rate_already = self.st_cash_rate_already(glav_buh_man)
            rate_serve['получил'] = man_cash_rate_already
            #rate_serve['получил'] = glav_buh_man.cash_rate_already

            return rate_serve
        else:
            return {'ЗП': 0}

    def salary_buh(self, plan_stavka_=None, no_stavka=True):
        # зп-бух, plan_stavka_=True - полная инфа и пониж коэф, None - краткая и без пониж коэф
        # no_stavka=True - пока не используется
        month, year = self.month, self.year
        try:
            buh_man = Managers.objects.get(family__groups__name='buh_group')
        except:
            buh_man = None
        if buh_man:
            if plan_stavka_:
                rate_serve = {'Процент_ставка': 1}
            else:
                rate_serve = {'Процент_ставка': 1}
            count = 0
            rate_serve['name'] =  buh_man.name
            service = self.get_service('простой', 'Бухгалтерия')
            stavka = round(service.cash_rate * rate_serve['Процент_ставка'])

            rate_serve['ЗП'] = stavka
            man_cash_rate_already = self.st_cash_rate_already(buh_man)
            rate_serve['получил'] = man_cash_rate_already
            #rate_serve['получил'] = buh_man.cash_rate_already

            return rate_serve

        else:
            return {'ЗП': 0}

    def salary_razrab(self, plan_stavka_=None, no_stavka=True):
        # зп-бух, plan_stavka_=True - полная инфа и пониж коэф, None - краткая и без пониж коэф
        # no_stavka=True - пока не используется
        month, year = self.month, self.year
        try:
            razrab_man = Managers.objects.get(family__groups__name='razrab_group')
        except:
            razrab_man = None
        if razrab_man:
            if plan_stavka_:
                rate_serve = {'Процент_ставка': 1}
            else:
                rate_serve = {'Процент_ставка': 1}
            count = 0
            rate_serve['name'] =  razrab_man.name
            service = self.get_service('простой', 'Разработка ПО')
            stavka = round(service.cash_rate * rate_serve['Процент_ставка'])

            rate_serve['ЗП'] = stavka
            man_cash_rate_already = self.st_cash_rate_already(razrab_man)
            rate_serve['получил'] = man_cash_rate_already
            #rate_serve['получил'] = razrab_man.cash_rate_already

            return rate_serve

        else:
            return {'ЗП': 0}

    def salary_kurier(
        self, plan_stavka_=None, no_stavka=True, per_comps=False,
        week=1):
        # week - неделя(по умолчанию 1)
        # зп-курьер, plan_stavka_=True - полная инфа без!!! пониж коэф, None - краткая и без
        # пониж коэф
        # при no_stavka=True - только процент
        month, year = self.month, self.year
        try:
            kurier_man = Managers.objects.get(family__groups__name='kurier_group')
        except:
            kurier_man = None
        if kurier_man:
            if plan_stavka_:
                #rate_serve = self.plan_stavka()
                rate_serve = {'Процент_ставка': 1} # изменил: план не влияет
            else:
                rate_serve = {'Процент_ставка': 1}
            rate_serve['name'] =  kurier_man.name
            #count_comp = self.get_count_comp()
            service = self.get_service('простой', 'Курьер')

            stavka = round(service.cash_rate * rate_serve['Процент_ставка'])
            tarif = service.summa

            ss_our = Statistics_service.objects.filter(
            week_count=week,
            managers=kurier_man,
            date__month=month, date__year=year)
            bids_kurier = ss_our.aggregate(
            Total=Sum(F('bidskurier__kurier_summa')))['Total']

            ss_all_week = Statistics_service.objects.filter(
            managers=kurier_man,
            date__month=month, date__year=year)
            bids_kurier_all_week = ss_all_week.aggregate(
            Total=Sum(F('bidskurier__kurier_summa')))['Total']

            summa_bids = bids_kurier if bids_kurier else 0
            summa_bids_bonus = summa_bids * tarif

            summa_bids_all_week = bids_kurier_all_week if bids_kurier_all_week else 0
            summa_bids_bonus_all_week = summa_bids_all_week * tarif

            ss_our_with_bonus = ss_our.distinct().values(
            'bidskurier__date_ch', 'bidskurier__ID','bidskurier__kurier_summa',
            'bidskurier__pk'
            ).annotate(
            bonus=F('bidskurier__kurier_summa') * tarif)

            last_row = {
            'bidskurier__date_ch': '',
            'bidskurier__ID': 'Всего',
            'bidskurier__kurier_summa': summa_bids,
            'bonus': summa_bids_bonus,
            'color': True
            }

            if ss_our_with_bonus.exists() and ss_our_with_bonus[0]['bidskurier__pk']:
                bids_summa_kurier = list(ss_our_with_bonus)
            else:
                bids_summa_kurier = []
            bids_summa_kurier.append(last_row)

            #bids_kurier = Bids.objects.filter(family=kurier_man.family,
            #date_ch__month=month, date_ch__year=year)
            #summa_bids_ = bids_kurier.distinct().aggregate(
            #Total=Sum(F('kurier_summa')))['Total']
            #summa_bids = summa_bids_ if summa_bids_ else 0

            #bids_summa_kurier = list(bids_kurier.distinct().values('ID', 'kurier_summa'))

            #summa = stavka + (summa_bids * tarif)
            summa = stavka + summa_bids_bonus_all_week
            #summa_str = f"Ставка:{stavka} + {km_}км * {tarif} Итого: {summa}"
            #summa_str = f"Ставка:{stavka} + сумма заявок: {summa_bids} * {tarif} Итого: {summa}"
            summa_str = f"Ставка:{stavka} + сумма заявок: {summa_bids_all_week} * {tarif} Итого: {summa}"

            if per_comps:
                try:
                    return round(summa / count_comp)
                except:
                    return summa

            if plan_stavka_:
                rate_serve['дата'] = f"{month}: {year}"
                rate_serve['заявки'] = bids_summa_kurier
                #rate_serve['km'] = km_
                #rate_serve['сумма заявок'] = summa_bids

                rate_serve['ставка'] = service.cash_rate
                #rate_serve['ЗП'] = summa_str if not no_stavka else summa_bids * tarif
                rate_serve['ЗП'] = summa_str if not no_stavka else summa_bids_bonus_all_week

                man_cash_rate_already = self.st_cash_rate_already(kurier_man)
                rate_serve['получил'] = man_cash_rate_already
                rate_serve['получил'] = kurier_man.cash_rate_already
            else:
                rate_serve['ЗП'] = summa if not no_stavka else summa_bids_bonus_all_week

            return rate_serve

        else:
            return {'ЗП': 0}

    def office_man(self, plan_stavka_=None):
        # зп офис-менеджера (раньше была с курьером)
        month, year = self.month, self.year

        service = self.get_service('простой', 'Офисный менеджер')
        if service.cash_rate == 0:
            service.cash_rate == 15000
            service.save()
        try:
            office_man_ = Managers.objects.get(family__groups__name='office_group')
        except:
            office_man_ = None

        if plan_stavka_:
            rate_serve = self.plan_stavka()
        else:
            rate_serve = {'Процент_ставка': 1}

        if plan_stavka_ and office_man_:
            rate_serve['дата'] = f"{month}: {year}"
            rate_serve['ставка'] = service.cash_rate
            rate_serve['ЗП'] = service.cash_rate * rate_serve['Процент_ставка']
            man_cash_rate_already = self.st_cash_rate_already(office_man_)
            rate_serve['получил'] = man_cash_rate_already
            #rate_serve['получил'] = office_man_.cash_rate_already
        else:
            rate_serve['ЗП'] = service.cash_rate

        return rate_serve

    def salary_category(self, plan_stavka_=None, no_stavka=True):
        # зп-категорийного менеджера
        # последнее обновление правил:
        # 0.35% от оборота вер, айти + бонус, вносимый вручную, ставки нет
        # plan_stavka_=True - полная инфа и пониж коэф, None - краткая и без пониж коэф
        # при no_stavka=True - только процент
        month, year = self.month, self.year
        try:
            category_man = Managers.objects.get(family__groups__name='category_group')
        except:
            category_man = None
        if category_man:
            if plan_stavka_:
                rate_serve = self.plan_stavka()
            else:
                rate_serve = {'Процент_ставка': 1}
            count = 0
            rate_serve['name'] =  category_man.name
            service = self.get_service('простой', 'Категорийный менеджер')
            stavka = round(service.cash_rate * rate_serve['Процент_ставка'])
            # ставки нет, но в админке остав возм поставить cash_rate != 0
            summa_procent = service.summa # % от оборота вер, айти
            if summa_procent:
                #
                salary_rate = self.salary_team_manager(category_man)
                try:
                    comp = salary_rate['team ' + 'Системный блок'] * summa_procent
                except:
                    comp = 0
                try:
                    parts = salary_rate['team ' + 'Комплектующие'] * summa_procent
                except:
                    parts = 0
                summa = stavka + comp + parts
                if plan_stavka_:
                    rate_serve['ЗП'] = f'Сис блоки: {comp}: , Компл: {parts},\
                    Ставка: {stavka}, Всего: {summa}'
                    rate_serve['ставка'] = category_man.cash_rate
                    man_cash_rate_already = self.st_cash_rate_already(category_man)
                    rate_serve['получил'] = man_cash_rate_already
                    #rate_serve['получил'] = category_man.cash_rate_already
                else:
                    rate_serve['ЗП'] = summa if not no_stavka else comp + parts

                return rate_serve

            """salary_rate = self.salary_manager(category_man)
            summa = stavka + salary_rate['sum']
            if plan_stavka_:
                rate_serve['ставка'] = service.cash_rate
                rate_serve['ЗП'] = salary_rate['ЗП'] + f", Ставка: {stavka}, Всего: {salary_rate['sum']}"
                man_cash_rate_already = self.st_cash_rate_already(category_man)
                rate_serve['получил'] = man_cash_rate_already
                #rate_serve['получил'] = category_man.cash_rate_already
            else:
                # используем rate_serve с пониж коэф чтобы компенсировать
                # в salary_manager ставку(с пон коэф), поэтому минусуем соотв stavka
                rate_serve = self.plan_stavka()
                stavka = round(service.cash_rate * rate_serve['Процент_ставка'])
                rate_serve['ЗП'] = salary_rate['sum'] if not no_stavka else salary_rate['sum'] - stavka"""

            # not summa_procent значит нет процента от оборота, но возможно есть ставка
            if plan_stavka_:
                rate_serve['ЗП'] = f'Сис блоки: 0: , Компл: 0,\
                Ставка: {stavka}, Всего: {stavka}'
                rate_serve['ставка'] = category_man.cash_rate
                man_cash_rate_already = self.st_cash_rate_already(category_man)
                rate_serve['получил'] = man_cash_rate_already
                #rate_serve['получил'] = category_man.cash_rate_already
            else:
                rate_serve['ЗП'] = stavka if not no_stavka else 0

            return rate_serve

        else:
            return {'ЗП': 0}

    def salary_super(self, plan_stavka_=None, no_stavka=True):
        # зп-главного менеджера,
        # ставка, если ставка > тариф * компы, тариф * компы, если наоборот
        # при no_stavka=True - только процент
        month, year = self.month, self.year
        try:
            super_man = Managers.objects.get(super=True)
        except:
            super_man = None
        if super_man:
            if plan_stavka_:
                rate_serve = self.plan_stavka()
            else:
                rate_serve = {'Процент_ставка': 1}
            count = 0
            rate_serve['name'] =  super_man.name
            stavka = round(super_man.cash_rate * rate_serve['Процент_ставка'])

            salary_rate = self.salary_team_manager(super_man)
            try:
                comp = salary_rate['team ' + 'Системный блок'] * 0.005
            except:
                comp = 0
            try:
                parts = salary_rate['team ' + 'Комплектующие'] * 0.005
            except:
                parts = 0
            summa = stavka + comp + parts
            if plan_stavka_:
                rate_serve['ЗП'] = f'Сис блоки: {comp}: , Компл: {parts},\
                Ставка: {stavka}, Всего: {summa}'
                rate_serve['ставка'] = super_man.cash_rate
                man_cash_rate_already = self.st_cash_rate_already(super_man)
                rate_serve['получил'] = man_cash_rate_already
                #rate_serve['получил'] = super_man.cash_rate_already
            else:
                rate_serve['ЗП'] = summa if not no_stavka else comp + parts

            return rate_serve

        else:
            return {'ЗП': 0}

    def salary_sklad(self, plan_stavka_=None, no_stavka=True, site_='both'):
        # зп-курьер, plan_stavka_=True - полная инфа и пониж коэф, None - краткая и без пониж коэф
        # ставка, если ставка > тариф * компы, тариф * компы, если наоборот
        # при no_stavka=True - summa(алглритм)
        month, year = self.month, self.year
        try:
            sklad_man = Managers.objects.get(family__groups__name='sklad_group')
        except:
            sklad_man = None
        if sklad_man:
            if plan_stavka_:
                #rate_serve = self.plan_stavka()
                rate_serve = {'Процент_ставка': 1}
            else:
                rate_serve = {'Процент_ставка': 1}
            count = 0
            rate_serve['name'] =  sklad_man.name
            count_comp = self.get_count_comp()
            service = self.get_service('простой', 'Зав склада')

            stavka = round(service.cash_rate * rate_serve['Процент_ставка'])
            tarif = service.summa

            stavka_service = count_comp * tarif
            if stavka_service  > stavka:
                summa = stavka_service
            else:
                summa = stavka
            if plan_stavka_:
                rate_serve['ЗП'] = f'Ставка: {stavka} Кол компов: {count_comp} * {tarif}, Итого: {summa}'
                man_cash_rate_already = self.st_cash_rate_already(sklad_man)
                rate_serve['получил'] = man_cash_rate_already
                #rate_serve['получил'] = sklad_man.cash_rate_already
            else:
                rate_serve['ЗП'] = summa

            return rate_serve

        else:
            return {'ЗП': 0}

    def salary_tovar(self, plan_stavka_=None, no_stavka=True, site_='both'):
        # зп-завсклада, plan_stavka_=True - полная инфа и пониж коэф, None - краткая и без пониж коэф
        # ставка, если ставка > тариф * компы, тариф * компы, если наоборот
        # при no_stavka=True - summa(алглритм)
        month, year = self.month, self.year
        try:
            tovar_man = Managers.objects.get(family__groups__name='tovar_group')
        except:
            tovar_man = None
        if tovar_man:
            if plan_stavka_:
                #rate_serve = self.plan_stavka()
                rate_serve = {'Процент_ставка': 1}
            else:
                rate_serve = {'Процент_ставка': 1}
            count = 0
            rate_serve['name'] =  tovar_man.name
            count_comp = self.get_count_comp()
            service = self.get_service('простой', 'Заказ товара')

            stavka = round(service.cash_rate * rate_serve['Процент_ставка'])
            tarif = service.summa

            stavka_service = count_comp * tarif
            if stavka_service  > stavka:
                summa = stavka_service
            else:
                summa = stavka

            if plan_stavka_:
                rate_serve['ЗП'] = f'Ставка: {stavka} Кол компов: {count_comp} * {tarif}, Итого: {summa}'
                man_cash_rate_already = self.st_cash_rate_already(tovar_man)
                rate_serve['получил'] = man_cash_rate_already
                #rate_serve['получил'] = tovar_man.cash_rate_already
            else:
                rate_serve['ЗП'] = summa

            return rate_serve

        else:
            return {'ЗП': 0}

    def sum_salary_no_stavka(self, site_='both'):
        # сумма процентных ставок salary_category
        month, year = self.month, self.year
        temp_remontnik = 0
        if Managers.objects.filter(remontnik=True).exists():
            for man_ in Managers.objects.filter(remontnik=True):
                temp_remontnik += float(self.salary_service_man(man_)['ЗП'])
        temp_sborsik = 0
        if Managers.objects.filter(sborsik=True).exists():
            for man_ in Managers.objects.filter(sborsik=True):
                temp_sborsik += float(self.salary_service_man(man_)['ЗП'])

        return self.get_marketplace() + self.salary_one_c()['ЗП'] + \
            self.salary_kurier()['ЗП'] + self.salary_category()['ЗП'] + \
            temp_remontnik + temp_sborsik
