from django.db import models
from datetime import datetime, date, time
from django.utils import timezone
from django.contrib.auth.models import User, Group
from django.db.models import signals
from django.db.models import Sum

class Ratios(models.Model):
    date = models.DateTimeField(auto_now=True, verbose_name='Дата')
    tax_ratio = models.FloatField(db_index=True, verbose_name='Налог на прибыль',
    default=0.18)
    itblok_ratio = models.FloatField(db_index=True,
    verbose_name='Айтиблок_расход_на_один_комп', default=0.065)
    versum_ratio = models.FloatField(db_index=True,
    verbose_name='Версум_расход_на_один_комп', default=0.015)

    def __str__(self):
        return str(self.tax_ratio) + '--' + (self.date).strftime("%B %Y")

    class Meta:
        verbose_name_plural = 'Слежебные коэф'
        verbose_name = 'Слежебные коэф'

class Bids(models.Model):
    CHOISE = (
        ('Відвантажено', 'Відвантажено'), #('Отправлен', 'Отправлен'),
        ('Підтверджено', 'Підтверджено'), #('Подтверждён', 'Подтверждён'),
        ('Діалог триває', 'Діалог триває'), #('Идёт диалог', 'Идёт диалог'),
        ('Чекаємо на оплату', 'Чекаємо на оплату') ,#('Ожидаем оплату', 'Ожидаем оплату'),
        ('Замовлення товару', 'Замовлення товару'), #('Заказ товара', 'Заказ товара'),
        ('В черзі на збірку', 'В черзі на збірку'), #('Идёт сборка', 'Идёт сборка'),
        ('Успішно виконаний', 'Успішно виконаний'), #('Выкуплен', 'Выкуплен'),
        ('Сервіс', 'Сервіс'), #('Сервис', 'Сервис'),
        ('Ремонт ПК', 'Ремонт ПК'),
        ('Відмова', 'Відмова'), #('Отказ', 'Отказ'),
    )

    CHOISE1 = (
        ('Корзина', 'Корзина'), #('КОРЗИНА', 'КОРЗИНА'),
        ('Telegram', 'Telegram'), #('Rozetka', 'Rozetka'),
        ('Чат', 'Чат'), #('Алло', 'Алло'),
        ('Телефон', 'Телефон'), #('Телефон_Чат', 'Телефон_Чат'),
        ('Офіс', 'Офіс'), #('Офис', 'Офис'),
        ('ПК вітрина 2%', 'ПК вітрина 2%'), #('ПК витрина 2%', 'ПК витрина 2%'),
        ('Instagram', 'Instagram'), #('Инстаграм', 'Инстаграм'),
        ('Інше джерело', 'Інше джерело'), #('Другой', 'Другой'),
        ('OLX', 'OLX'),
        ('Тендер', 'Тендер'),
        ('Сервіс', 'Сервіс'),
    )

    CHOISE2 = (
        ('versum', 'versum'),
        ('komputeritblok', 'komputeritblok'),
        ('both', 'both'),
    )

    CHOISE3 = (
        ('Другой способ оплаты', 'Другой способ оплаты'),
        #('Другой способ оплаты', 'Другой способ оплаты'),
        ('Криптовалюта', 'Криптовалюта'),
        #('Кредит Альфа Банк', 'Кредит Альфа Банк'),
        ('На ФОП', 'На ФОП'),
        #('Оплата на ФОП', 'Оплата на ФОП'),
        ('На карту Visa/MasterCard', 'На карту Visa/MasterCard'),
        #('Оплата картой Visa/MasterCard', 'Оплата картой Visa/MasterCard'),
        ('Оплата частинами (ПриватБанк)', 'Оплата частинами (ПриватБанк)'),
        ('Миттєва розстрочка (ПриватБанк)', 'Миттєва розстрочка (ПриватБанк)'),
        ('Онлайн-карткою (LiqPay)', 'Онлайн-карткою (LiqPay)'),
        ('Без оплати', 'Без оплати'),
        ('Кредит Плати Пізніше', 'Кредит Плати Пізніше'),
        #('Оплата онлайн-картой (LiqPay)', 'Оплата онлайн-картой (LiqPay)'),
        ('Безготівковий з ПДВ', 'Безготівковий з ПДВ'),
        #('Безналичный с НДС', 'Безналичный с НДС'),
        ('На карту', 'На карту'),
        #('На карту', 'На карту'),
        ('Кредит Монобанк', 'Кредит Монобанк'),
        #('Кредит Монобанк', 'Кредит Монобанк'),
        ('Готівкою', 'Готівкою'),
        #('Готівкою', 'Готівкою'),
    )

    ID = models.PositiveIntegerField(unique=True, verbose_name='ID')
    site = models.CharField(max_length=20, db_index=True, verbose_name='Сайт',
    choices=CHOISE2, default='versum')
    status = models.CharField(max_length=50, db_index=True,
    verbose_name='Статус', choices=CHOISE, default='Діалог триває')
    sposobOplaty = models.CharField(null=True, blank=True,max_length=100, db_index=True,
    verbose_name='Способ оплаты', choices=CHOISE3)
    istocnikZakaza = models.CharField(max_length=20, db_index=True,
    verbose_name='Исочник заказа',
    choices=CHOISE1, default='Телефон')
    date_ch = models.DateTimeField(auto_now=True, verbose_name='Дата')
    nds = models.PositiveIntegerField(db_index=True, verbose_name='НДС', default=0)
    nalog_na_pribil = models.PositiveIntegerField(db_index=True,
    verbose_name='Налог на прибыль', default=0)
    managers = models.ForeignKey('Managers',
    on_delete=models.CASCADE,null=True, verbose_name='Менеджер')
    first_sborsik = models.CharField(max_length=100, db_index=True,
    verbose_name='first_sborsik', default='')
    few_sborsik = models.CharField(max_length=100, db_index=True,
    verbose_name='few_sborsik', default='')
    family = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    kurier_summa = models.FloatField(db_index=True, verbose_name='Курьер нал', default=0)

    def display_goods(self):
        return ', '.join(
        [ genre.discr[:50] + '   *' + str(genre.amount) for genre in self.goods_set.all()[:3]]
        )

    display_goods.short_description = 'Товары'

    def __str__(self):
        return str(self.ID)

    class Meta:
        verbose_name_plural = 'Заявки'
        verbose_name = 'Заявка'
        ordering = ['date_ch']
        permissions = (("only_managers", "only managers"),("only_sereja","only sereja"))

class Bids_advanced(Bids):
    class Meta:
        proxy = True
        verbose_name = 'Статистика'
        verbose_name_plural = 'Статистика'

class Managers(models.Model):

    CHOISE = (
        ('versum', 'versum'),
        ('itblok', 'itblok'),
        ('both', 'both'),
    )

    name = models.CharField(max_length=100, db_index=True,
    verbose_name='Имя', default='somebody')
    sborsik = models.BooleanField(default=False, verbose_name='Сборщик')
    remontnik = models.BooleanField(default=False, verbose_name='Ремонтник')
    is_active = models.BooleanField(default=False, verbose_name='Менеджер')
    super = models.BooleanField(default=False, verbose_name='Главный менеджер')
    site = models.CharField(max_length=20, db_index=True, verbose_name='сайт', choices=CHOISE,
    default='versum')
    cash_rate = models.PositiveIntegerField(db_index=True, verbose_name='Ставка', default=0)
    cash_rate_already = models.PositiveIntegerField(db_index=True,
    verbose_name='Уже получил', default=0)
    family = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
    verbose_name='Имя для своей страницы ')


    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Менеджеры'
        verbose_name = 'Менеджер'
        ordering = ['name']
        permissions = (("only_managers", "only managers"),("only_sereja","only sereja"))

class Goods(models.Model):
    CHOISE = (
        ('Системный блок', 'Системный блок'),
        ('ПО', 'ПО'),
        ('Комплектующие', 'Комплектующие'),
    )

    summa = models.PositiveIntegerField(db_index=True, verbose_name='Сумма', default=0)
    software_bonus = models.PositiveIntegerField(db_index=True,
    verbose_name='software_bonus', default=100)
    discr = models.TextField(null=True, blank=True,max_length=5000,
    db_index=True, verbose_name='Описание')
    kind = models.CharField(max_length=100, db_index=True, verbose_name='Вид',
    choices=CHOISE, default='Системный блок')
    bids = models.ForeignKey(Bids, on_delete=models.CASCADE, verbose_name='Заявка')
    amount = models.PositiveIntegerField(db_index=True, verbose_name='Колличество', default=1)

    def display_managers(self):
        return str(
        self.bids.managers.name) + ': ' + str(self.bids.date_ch.strftime("%B %Y"))

    display_managers.short_description = 'Менеджер'

    def __str__(self):
        return str(self.bids.ID) + ': ' + self.discr

    class Meta:
        verbose_name_plural = 'Товары из заявок'
        verbose_name = 'Товар из заявки'
        ordering = ['summa']

class Service(models.Model):
    CHOISE = (
        ('Ремонт ПК', 'Ремонт ПК'),
        ('Сборка', 'Сборка'),
        ('Установка лед табличек', 'Установка лед табличек'),
        ('Обслуживание', 'Обслуживание'),
        ('Заказ товара', 'Заказ товара'),
        ('Глав бух', 'Глав бух'),
        ('Бухгалтерия', 'Бухгалтерия'),
        ('Разработка ПО', 'Разработка ПО'),
        ('Зав склада', 'Зав склада'),
        ('Курьер', 'Курьер'),
        ('Оператор 1С', 'Оператор 1С'),
        ('Офисный менеджер', 'Офисный менеджер'),
        ('Категорийный менеджер', 'Категорийный менеджер'),
        ('Офисный комп', 'Офисный комп'),
        ('Игровой комп', 'Игровой комп'),
    )

    CHOISE2 = (
        ('-', '-'),
        ('простой', 'простой'),
        ('обычный', 'обычный'),
        ('сложный', 'сложный'),
        ('ультра', 'ультра'),
    )

    summa = models.FloatField(db_index=True, verbose_name='Оплата за этот вид работ', default=0)
    kind = models.CharField(max_length=50, db_index=True,
    verbose_name='Вид работ', choices=CHOISE, default='Сборка')
    sloznostPK = models.CharField(max_length=50, db_index=True,
    verbose_name='Сложность', choices=CHOISE2,
    default='простой')
    cash_rate = models.PositiveIntegerField(db_index=True, verbose_name='Ставка', default=0)
    managers = models.ManyToManyField(Managers)

    def __str__(self):
        return self.kind + ', сложность: ' + self.sloznostPK

    class Meta:

        verbose_name_plural = 'Сервисы'
        verbose_name = 'Сервис'
        ordering = ['summa']

def check_saves_service(sender, instance, created, **kwargs):

    dict_groups__name = {
        'Ремонт ПК': 'sborsik_group',
        'Сборка': 'sborsik_group',
        'Обслуживание': 'sborsik_group',
        'Заказ товара': 'tovar_group',
        'Глав бух': 'glav_buh_group',
        'Бухгалтерия': 'buh_group',
        'Разработка ПО': 'razrab_group',
        'Зав склада': 'sklad_group',
        'Курьер': 'kurier_group',
        'Оператор 1С': 'one_c_group',
        'Категорийный менеджер': 'category_group',
                        }

    cash_rate_ = instance.cash_rate
    kind_ = instance.kind

    if kind_ == 'Сборка':
        man = Managers.objects.filter(
        family__groups__name=dict_groups__name[kind_], sborsik=True
        )
        man.update(cash_rate=cash_rate_)
        return True
    if kind_ == 'Ремонт ПК':
        man = Managers.objects.filter(
        family__groups__name=dict_groups__name[kind_], remontnik=True
        )
        man.update(cash_rate=cash_rate_)
        return True
    if kind_ == 'Обслуживание':
        man = Managers.objects.filter(
        family__groups__name=dict_groups__name[kind_], remontnik=True
        )
        man.update(cash_rate=cash_rate_)
        return True

    try:
        man = Managers.objects.get(family__groups__name=dict_groups__name[kind_])
    except:
        man = None
    if man:
        man.cash_rate = cash_rate_
        man.save()

signals.post_save.connect(receiver=check_saves_service, sender=Service)

class Statistics_service(models.Model):

    CHOISE = (
        ('versum', 'versum'),
        ('itblok', 'itblok'),
        ('both', 'both'),
    )

    managers = models.ForeignKey(Managers, on_delete=models.CASCADE, verbose_name='Имя')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name='Вид')
    site = models.CharField(max_length=20, db_index=True, verbose_name='сайт', choices=CHOISE,
    default='both')
    date = models.DateTimeField(default=timezone.now, verbose_name='Дата')
    sborka_count = models.PositiveIntegerField(default=0, verbose_name='Кол сборок')
    remont_count = models.PositiveIntegerField(default=0, verbose_name='Кол ремонтов')
    obsluj_count = models.PositiveIntegerField(default=0, verbose_name='Кол обслуживаний')
    km_count = models.PositiveIntegerField(default=0, verbose_name='km')
    #kurier_count = models.PositiveIntegerField(default=0,
    #verbose_name='Курьерская сумма')
    cash_rate_already = models.PositiveIntegerField(db_index=True,
    verbose_name='Уже получил', default=0)
    family = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Статистика сотрудников'
        verbose_name = 'Статистика сотрудников'
        ordering = ['managers__name']
        permissions = (("only_managers", "only managers"),("only_sereja","only sereja"))

    def __str__(self):
        return self.managers.name + '+' + self.service.kind + '+'\
        + self.service.sloznostPK + '+' + (self.date).strftime("%B %Y--%H:%M")

class Statistics_bid(models.Model):
    date = models.DateTimeField(auto_now=True)
    bid_count = models.PositiveIntegerField(default=0, verbose_name='bid_count')
    idet_dialog_count = models.PositiveIntegerField(default=0, verbose_name='idet_dialog_count')
    ojidaem_oplatu_count = models.PositiveIntegerField(default=0,
    verbose_name='ojidaem_oplatu_count')
    otkaz_count = models.PositiveIntegerField(default=0, verbose_name='otkaz_count')
    positive_count = models.PositiveIntegerField(default=0, verbose_name='positive_count')
    negative_sum = models.IntegerField(default=0, verbose_name='negative_sum')
    managers = models.ForeignKey(Managers, on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.managers.name + '+' + (self.date).strftime("%B %Y")

    class Meta:
        verbose_name_plural = 'Сборщики-ремонтники'
        verbose_name = 'Сборщики-ремонтники'
        ordering = ['date']

class Statistics(models.Model):
    CHOISE0 = (
        ('Другой способ оплаты', 'Другой способ оплаты'),
        ('Кредит Альфа Банк', 'Кредит Альфа Банк'),
        ('Оплата на ФОП', 'Оплата на ФОП'),
        ('Оплата картой Visa/MasterCard', 'Оплата картой Visa/MasterCard'),
        ('Оплата онлайн-картой (LiqPay)', 'Оплата онлайн-картой (LiqPay)'),
        ('Безналичный с НДС', 'Безналичный с НДС'),
        ('На карту', 'На карту'),
        ('Кредит Монобанк', 'Кредит Монобанк'),
        ('Готівкою', 'Готівкою'),
    )

    CHOISE1 = (
        ('КОРЗИНА', 'КОРЗИНА'),
        ('Rozetka', 'Rozetka'),
        ('Алло', 'Алло'),
        ('Телефон_Чат', 'Телефон_Чат'),
        ('Офис', 'Офис'),
        ('Другой', 'Другой'),
    )

    CHOISE = (
        ('Системный блок', 'Системный блок'),
        ('ПО', 'ПО'),
        ('Комплектующие', 'Комплектующие'),
    )

    CHOISE2 = (
        ('versum', 'versum'),
        ('itblok', 'itblok'),
    )

    date = models.DateTimeField(auto_now=True)
    site = models.CharField(max_length=10, db_index=True, verbose_name='site',
    choices=CHOISE2, default='versum')
    sposobOplaty = models.CharField(null=True, blank=True,max_length=100,
    db_index=True, verbose_name='sposobOplaty', choices=CHOISE0)
    istocnikZakaza = models.CharField(max_length=20, db_index=True,
    verbose_name='istocnikZakaza',
    choices=CHOISE1, default='Телефон_Чат')
    kind = models.CharField(max_length=100, db_index=True, verbose_name='kind',
    choices=CHOISE, default='Системный блок')
    summa = models.PositiveIntegerField(db_index=True, verbose_name='summa', default=0)
    managers = models.ForeignKey(Managers, on_delete=models.CASCADE,null=True)

    def __str__(self):
        return f'{self.managers.name}-{self.kind}-{self.istocnikZakaza}-{self.sposobOplaty}-{self.site}-{(self.date).strftime("%B %Y")}'

    class Meta:
        verbose_name_plural = 'Statistic'
        verbose_name = 'Statistics'
        ordering = ['date']

class Gross_profit(models.Model):
    CHOISE = (
        ('versum', 'versum'),
        ('itblok', 'itblok'),
        ('tenders', 'tenders'),
        ('others', 'others'),
        ('both', 'both'),
    )

    site = models.CharField(max_length=10, db_index=True, verbose_name='Сайт', choices=CHOISE,
    default='versum')
    amount = models.FloatField(db_index=True, verbose_name='Оборот_ПК', default=0)
    amountcomponents = models.FloatField(db_index=True,
    verbose_name='Оборот_детали_ПК', default=0)
    quantity = models.PositiveIntegerField(db_index=True,
    verbose_name='Колличество_ПК', default=0)
    grossprofit = models.FloatField(db_index=True, verbose_name='Прибыль_ПК', default=0)
    grossprofitcomponents = models.FloatField(db_index=True,
    verbose_name='Прибыль_детали_ПК', default=0)
    rentability = models.FloatField(db_index=True, verbose_name='Наценка', default=0)
    totalSales = models.FloatField(db_index=True, verbose_name='Оборот_ПК_Сумма ', default=0)
    totalProfit = models.FloatField(db_index=True, verbose_name='Прибыль_ПК_Сумма ', default=0)
    sumSales = models.FloatField(db_index=True, verbose_name='Оборот_Сумма', default=0)
    sumProfit = models.FloatField(db_index=True, verbose_name='Прибыль_Сумма', default=0)
    quantity_total = models.FloatField(db_index=True,
    verbose_name='Колличество_ПК_Сумма ', default=0)
    date = models.DateTimeField(default=timezone.now, verbose_name='Дата')

    class Meta:
        verbose_name_plural = 'Валовая прибыль'
        verbose_name = 'Валовая прибыль'
        ordering = ['date']

    def __str__(self):
        return 'Показатели--' + self.site + '--' + (self.date).strftime("%B %Y")
#Expense
class Expense_groups(models.Model):
    name = models.CharField(null=True, blank=True, db_index=True,
    verbose_name='Группы расходов',max_length=300)

    class Meta:
        verbose_name_plural = 'Группы расходов'
        verbose_name = 'Группы расходов'
        ordering = ['name']

    def __str__(self):
        return self.name

class Expense(models.Model):

    CHOISE = (
        ('versum', 'versum'),
        ('itblok', 'itblok'),
        ('tenders', 'tenders'),
        ('others', 'others'),
        ('both', 'both'),
    )

    """CHOISE = (
        ('Версум реклама', 'Версум реклама'),
        ('Версум расстраты текущие', 'Версум расстраты текущие'),
        ('Ит-Блок расстраты текущие', 'Ит-Блок расстраты текущие'),
        ('Андрей Мишутин расстраты текущие', 'Андрей Мишутин расстраты текущие'),
        ('Расстраты на оба проэкта', 'Расстраты на оба проэкта'),
        ('Ручные поля', 'Ручные поля'),
        ('Другие растраты', 'Другие растраты'),
    )"""

    site = models.CharField(max_length=20, db_index=True, verbose_name='сайт', choices=CHOISE,
    default='versum')
    amount = models.FloatField(db_index=True, verbose_name='Расходы по статье', default=0)
    summa = models.FloatField(db_index=True, verbose_name='Сумма расходов сайта', default=0)
    discr = models.CharField(null=True, blank=True, db_index=True,
    verbose_name='Статья расходов',max_length=300)
    date = models.DateTimeField(default=timezone.now, verbose_name='Дата')
    is_active = models.BooleanField(default=True)
    #kind = models.CharField(max_length=100, db_index=True, verbose_name='Вид трат',
    #choices=CHOISE, default='Другие растраты')
    expense_groups = models.ForeignKey(Expense_groups, on_delete=models.SET_NULL,null=True,
    verbose_name='Вид трат')

    class Meta:
        verbose_name_plural = 'Расходы'
        verbose_name = 'Расходы'
        ordering = ['date']

    def __str__(self):
        return self.discr + '--' + (self.date).strftime("%B %Y")
#
class Average_check(models.Model):

    CHOISE = (
        ('versum', 'versum'),
        ('itblok', 'itblok'),
    )

    date = models.DateTimeField(default=timezone.now, verbose_name='Дата')
    quantity = models.PositiveIntegerField(db_index=True, verbose_name='ПК план', default=0)
    site = models.CharField(max_length=20, db_index=True, verbose_name='сайт',
    choices=CHOISE, default='versum')
    price = models.FloatField(db_index=True, verbose_name='Чек', default=35000.0)
    hand_check = models.FloatField(db_index=True, verbose_name='Средние траты',
    default=1500.0)
    plan_check = models.FloatField(db_index=True, verbose_name='Запланированные траты',
    default=75000.0)

    class Meta:
        verbose_name_plural = 'Средний чек'
        verbose_name = 'Средний чек'
        ordering = ['date']

    def __str__(self):
        return str(self.site) + '--' + str(self.price) + '--' + (self.date).strftime("%B %Y")

def check_saves(sender, instance, created, **kwargs):
    site_ = instance.site
    now = instance.date
    hand_check_ = instance.hand_check # Средние траты (oперативныe траты|компы)
    summa_site = instance.plan_check # Запланированные траты
    month, year = now.strftime("%m"), now.strftime("%Y")

    if instance.quantity:
        if Plan.objects.filter(date__month=month,date__year=year,
        site=site_).exists():
            p = Plan.objects.filter(date__month=month,date__year=year,
            site=site_).last()
        else:
            if Plan.objects.filter(site=site_).exists():
                plan_last = Plan.objects.filter(site=site_).last()
                p = Plan.objects.create(plan=plan_last.plan, site=site_, date=now)
            else:
                p = Plan.objects.create(site=site_, date=now)
        p.plan = round(instance.quantity * instance.price, 1)
        p.date = now
        p.save()
        return 0
    if Plan.objects.filter(date__month=month,date__year=year,
    site=site_).exists():
        p = Plan.objects.filter(date__month=month,date__year=year,
        site=site_).last()
    else:
        if Plan.objects.filter(site=site_).exists():
            plan_last = Plan.objects.filter(site=site_).last()
            p = Plan.objects.create(plan=plan_last.plan, site=site_, date=now)
        else:
            p = Plan.objects.create(site=site_, date=now)

    if Gross_profit.objects.filter(date__month=month,date__year=year,
    site=site_).exists():

        #expense_site = Expense.objects.filter(expense_groups__name='Ручные поля',
        #date__month=month, date__year=year, site=site_, is_active=True)

        #summa_site = round(expense_site.distinct().aggregate(Total=Sum('amount'))['Total'])

        summa_one_c = summa_site if summa_site else 0 # Траты запланированные

        ratio_, _ = Ratios.objects.get_or_create()
        if instance.site == 'versum':
            summa_hand = round((instance.price) * ratio_.versum_ratio)
        else:
            summa_hand = round((instance.price) * ratio_.itblok_ratio)
        #summa_all = summa_one_c + summa_hand # Траты
        #count_comp = Gross_profit.objects.filter(date__month=month,date__year=year,
        #site=site_).last().quantity

        rentability_ = Gross_profit.objects.filter(date__month=month,date__year=year,
        site=site_).last().rentability #наценка
        rentability_ = (rentability_) /100 if rentability_ else 1

        profit_count_plan = instance.price * rentability_ - summa_hand - hand_check_#прибыль расчётная
                                                                                    #для плана
        if profit_count_plan < 0:
            print('error profit_count')
            return 0

        try:
            count_comp_null_plan = summa_one_c / profit_count_plan
            #количество компов для
            #окупаемости для плана
        except:
            print('error profit_count')
            return 0

        try:
            y_plan = 25 * summa_one_c / (count_comp_null_plan * (25 * profit_count_plan - instance.price))
            #коефициент наценки для выполнения плана
        except:
            print('error count_comp_null')
            return 0

        if y_plan < 0:
            print('error y_plan')
            return 0

        """try:
            summa_all_ono_comp = summa_one_c / count_comp + summa_hand + hand_check_#Траты на однин заказ
        except:
            print('error count_comp')
            return 0

        profit_count = instance.price * rentability_ - summa_all_ono_comp  #прибыль расчётная
        if profit_count < 0:
            print('error profit_count')
            return 0

        try:
            count_comp_null = round(summa_all_ono_comp * count_comp / (instance.price * rentability_),1)
            #количество компов для
            #окупаемости
        except:
            print('error profit_count')
            return 0

        try:
            y_plan = 25 * summa_all_ono_comp * count_comp / (count_comp_null * (25 * profit_count - instance.price))
            #коефициент наценки для выполнения плана
        except:
            print('error count_comp_null')
            return 0

        if y_plan < 0:
            print('error y_plan')
            return 0"""

        p.plan = round((count_comp_null_plan * (y_plan + 0.01)) * instance.price, 2) if y_plan else 10000000
        p.zero_plan = round(count_comp_null_plan * instance.price, 2) if y_plan else 10000000
        p.profit_plan = round(profit_count_plan, 1)
        p.y_plan = round(y_plan, 2)
        p.date = now
        p.save()

signals.post_save.connect(receiver=check_saves, sender=Average_check)


class Plan(models.Model):

    CHOISE = (
        ('versum', 'versum'),
        ('itblok', 'itblok'),
    )

    date = models.DateTimeField(default=timezone.now, verbose_name='Дата')
    plan = models.FloatField(db_index=True, verbose_name='План', default=0)
    zero_plan = models.FloatField(db_index=True, verbose_name='Выход в 0', default=0)
    profit_plan = models.FloatField(db_index=True, verbose_name='Прибыль расчётная', default=0)
    y_plan = models.FloatField(db_index=True, verbose_name='Коефициент наценки', default=2)
    site = models.CharField(max_length=20, db_index=True, verbose_name='сайт',
    choices=CHOISE, default='versum')

    class Meta:
        verbose_name_plural = 'План'
        verbose_name = 'План'
        ordering = ['date']

    def __str__(self):
        return str(self.site) + '--' + (self.date).strftime("%B %Y")

class Koefficient(models.Model):
    date = models.DateTimeField(default=timezone.now)
    hand = models.FloatField(db_index=True, verbose_name='Коэффициент', default=1.18)

    class Meta:
        verbose_name_plural = 'Коэффициент'
        verbose_name = 'Коэффициент'
        ordering = ['date']

    def __str__(self):
        return str(self.hand) + '--' + (self.date).strftime("%B %Y")

def result_saves(sender, instance, created, **kwargs):
    now = timezone.now()
    month, year = now.strftime("%m"), now.strftime("%Y")
    if Koefficient.objects.last() and Expense.objects.filter(date__month=month,
    date__year=year).exists() and Gross_profit.objects.filter(date__month=month,date__year=year,
    site='both').exists():
        ex = Expense.objects.filter(date__month=month,
        date__year=year).last().summa
        profit = Gross_profit.objects.get(date__month=month,date__year=year,
        site='both').rentability
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
        p.save()
    else:
        print("don't")

#signals.post_save.connect(receiver=result_saves, sender=Koefficient)
