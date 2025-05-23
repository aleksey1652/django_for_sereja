import re

from django.db import models
from django.db.models import Sum, Count, F, Q
from django.db.models import signals

from cat.models import Parts_short as short
#from cat.models import USD
#


class PackFilters(models.Model):
    # для фильтров в адимнке айтибл компов (процы, видео, ОЗУ)

    CHOISE = (
        ('-', '-'),
        ('Тип_ОЗУ', 'Тип_ОЗУ'),
        ('Обьем_ОЗУ', 'Обьем_ОЗУ'),
        ('Видеокарты', 'Видеокарты'),
        ('AMDCPU', 'AMDCPU'),
        ('IntelCPU', 'IntelCPU'),
    )

    filter_name = models.CharField(max_length=50,
    db_index=True, verbose_name='Фильтр')
    filter_kind = models.CharField(default='-', max_length=50, db_index=True,
    verbose_name='Тип_фильтра', choices=CHOISE)

    def __str__(self):
        return self.filter_name

    class Meta:
        verbose_name_plural = 'Проц_видео_фильтры'
        verbose_name = 'Проц_видео_фильтр'
        unique_together = ('filter_name', 'filter_kind',)

class Series(models.Model):
    # в ItblokComputers есть отдельно серии компа

    series_name = models.CharField(default='Основной', max_length=50, db_index=True,
    verbose_name='Серия')
    desc_ru = models.CharField(null=True, blank=True, max_length=500, db_index=True,
    verbose_name='Описание_рус')
    desc_ukr = models.CharField(null=True, blank=True, max_length=500, db_index=True,
    verbose_name='Описание_укр')

    def __str__(self):
        return self.series_name

    class Meta:
        verbose_name_plural = 'Серии'
        verbose_name = 'Серия'

class Grups(models.Model):
    # в ItblokComputers есть отдельно группы компа

    group_name = models.CharField(default='Основной', max_length=50, db_index=True,
    verbose_name='Группа')
    desc_ru = models.CharField(null=True, blank=True, max_length=500, db_index=True,
    verbose_name='Описание_рус')
    desc_ukr = models.CharField(null=True, blank=True, max_length=500, db_index=True,
    verbose_name='Описание_укр')

    def __str__(self):
        return self.group_name

    class Meta:
        verbose_name_plural = 'Группы'
        verbose_name = 'Группа'


CHOISE_RU = (
    ('Да', 'Да'),
    ('Нет', 'Нет'),
)

CHOISE_UA = (
    ('Так', 'Так'),
    ('Нi', 'Нi'),
)

class ItblokComputers(models.Model):
    is_active = models.BooleanField(default=True)
    date_computers = models.DateTimeField(auto_now=True)
    name_computers = models.TextField(max_length=300, db_index=True,
    verbose_name='Название ру', unique=True)
    name_computers_ua = models.TextField(max_length=300, db_index=True,
    verbose_name='Название укр', null=True, blank=True)

    price_parts = models.FloatField(default=0, db_index=True,
    verbose_name='Вход')
    price_special = models.FloatField(default=0, db_index=True,
    verbose_name='Спец')
    rentability = models.FloatField(default=20, db_index=True,
    verbose_name='Нац')
    procent_prom = models.FloatField(default=10, db_index=True,
    verbose_name='Акц_ц%')
    price_prom = models.FloatField(default=0, db_index=True,
    verbose_name='Рез_ц_акц')
    price_main = models.FloatField(default=0, db_index=True,
    verbose_name='Рез_ц')

    hend_input = models.CharField(max_length=300, db_index=True,
    verbose_name='Ручной ввод детали', null=True, blank=True)

    cpu = models.ForeignKey(
    short,
    on_delete=models.CASCADE,
    limit_choices_to=Q(kind__in=('aproc', 'iproc')),
    related_name='cpu',
    #related_query_name='comp',
    verbose_name='Проц',
    null=True,
    blank=True,
    )

    cooler = models.ForeignKey(
    short,
    on_delete=models.CASCADE,
    limit_choices_to={'kind': 'cool'},
    related_name='cooler',
    #related_query_name='comp',
    verbose_name='Кулер',
    null=True,
    blank=True,
    )

    mb = models.ForeignKey(
    short,
    on_delete=models.CASCADE,
    limit_choices_to=Q(kind__in=('amb', 'imb')),
    related_name='mb',
    #related_query_name='comp',
    verbose_name='Мат плата',
    null=True,
    blank=True,
    )

    ram = models.ForeignKey(
    short,
    on_delete=models.CASCADE,
    limit_choices_to={'kind': 'mem'},
    related_name='ram',
    #related_query_name='comp',
    verbose_name='ОЗУ',
    null=True,
    blank=True,
    )

    gpu = models.ForeignKey(
    short,
    on_delete=models.CASCADE,
    limit_choices_to={'kind': 'video'},
    related_name='gpu',
    #related_query_name='comp',
    verbose_name='Видео',
    null=True,
    blank=True,
    )

    hdd = models.ForeignKey(
    short,
    on_delete=models.CASCADE,
    limit_choices_to={'kind': 'hdd'},
    related_name='hdd',
    #related_query_name='comp',
    verbose_name='НДД',
    null=True,
    blank=True,
    )

    ssd = models.ForeignKey(
    short,
    on_delete=models.CASCADE,
    limit_choices_to={'kind': 'ssd'},
    related_name='ssd',
    #related_query_name='comp',
    verbose_name='ССД',
    null=True,
    blank=True,
    )

    psu = models.ForeignKey(
    short,
    on_delete=models.CASCADE,
    limit_choices_to={'kind': 'ps'},
    related_name='psu',
    #related_query_name='comp',
    verbose_name='БП',
    null=True,
    blank=True,
    )

    case = models.ForeignKey(
    short,
    on_delete=models.CASCADE,
    limit_choices_to={'kind': 'case'},
    related_name='case',
    #related_query_name='comp',
    verbose_name='Корпус',
    null=True,
    blank=True,
    )

    fan = models.ForeignKey(
    short,
    on_delete=models.CASCADE,
    limit_choices_to={'kind': 'vent'},
    related_name='fan',
    #related_query_name='comp',
    verbose_name='Вентилятор',
    null=True,
    blank=True,
    )

    wifi = models.ForeignKey(
    short,
    on_delete=models.CASCADE,
    limit_choices_to={'kind': 'wifi'},
    related_name='wifi',
    #related_query_name='comp',
    verbose_name='ВайФай',
    null=True,
    blank=True,
    )

    cables = models.ForeignKey(
    short,
    on_delete=models.CASCADE,
    limit_choices_to={'kind': 'cables'},
    related_name='cables',
    #related_query_name='comp',
    verbose_name='Кабеля',
    null=True,
    blank=True,
    )

    soft = models.ForeignKey(
    short,
    on_delete=models.CASCADE,
    limit_choices_to={'kind': 'soft'},
    related_name='soft',
    #related_query_name='comp',
    verbose_name='ПО',
    null=True,
    blank=True,
    )

    mem_num_computers = models.PositiveIntegerField(default=1, db_index=True,
    verbose_name='ОЗУ кол')
    vent_num_computers = models.PositiveIntegerField(default=1, db_index=True,
    verbose_name='Вентиляторы кол')

    warr_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='Гарантия укр')
    warr_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='Гарантия ру')

    label = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='Ярлыки') # !!!! в действия компа обязат добавить мас доб ярлыков
    # и в фильтры тоже !!!!#

    series = models.ForeignKey(
                               'Series', on_delete=models.PROTECT,
                               null=True, blank=True, verbose_name='Серия'
                               )

    grups = models.ForeignKey(
                               'Grups', on_delete=models.PROTECT,
                               null=True, blank=True, verbose_name='Группа'
                               )

    description = models.TextField(
    default="[{'name_parts': 'пока пусто', 'price': 0}]",
    verbose_name='Описание'
    )
#
    def comp_name_plus(self):
        #

        try:
            mem = '_'.join(re.findall(r'^\d+gb|ddr\d', self.ram.name_parts.lower()))
        except:
            mem = ''
        try:
            mb = re.findall(r'^\w+', self.mb.name_parts)[0]
        except:
            mb = ''
        try:
            ssd = re.findall(r'\s(\d+[tg]b)', self.ssd.name_parts.lower())[0]
        except:
            ssd = ''
        try:
            ps = re.findall(r'\s(\d{2,4})w', self.psu.name_parts.lower())[0] + 'w'
        except:
            ps = ''
        if self.case.name_parts.lower().find('white') != -1:
            return f'{mem}-{mb}-{ssd}-{ps}-white'
        return f'{mem}-{mb}-{ssd}-{ps}'


    comp_name_plus.short_description = 'Конфиг'

    def __str__(self):
        return self.name_computers

    class Meta:
        verbose_name_plural = 'КОМПЬЮТЕРЫ_ITBLOK'
        verbose_name = 'КОМПЬЮТЕР_ITBLOK'
        ordering = ['-name_computers']


    def save(self, *args, **kwargs):
            # Пересчитываем price- ы перед сохранением,
            # меняем description (деталь --- цена, ...)
            # в поле hend_input (ручн ввод детали) можно новую деталь,
            # потом поле очищаем

            #usd_j = USD.objects.last()
            #usd =  usd_j.usd if usd_j.usd else 0

            if self.hend_input:
                # если что-то ввели - добавляем новую деталь
                short_name = self.hend_input
                #
                try:
                    short_ = short.objects.get(name_parts=short_name, kind2=False)
                    kind_ = short_.kind
                except:
                    super().save(*args, **kwargs)
                    return False

                if kind_ in ('aproc', 'iproc',):
                    self.cpu = short_
                if kind_ in ('amb', 'imb',):
                    self.mb = short_
                if kind_ == 'cool':
                    self.cooler = short_
                if kind_ == 'mem':
                    self.ram = short_
                if kind_ == 'video':
                    self.gpu = short_
                if kind_ == 'hdd':
                    self.hdd = short_
                if kind_ == 'ssd':
                    self.ssd = short_
                if kind_ == 'ps':
                    self.psu = short_
                if kind_ == 'case':
                    self.case = short_
                if kind_ == 'vent':
                    self.fan = short_
                if kind_ == 'wifi':
                    self.wifi = short_
                if kind_ == 'cables':
                    self.cables = short_
                if kind_ == 'soft':
                    self.soft = short_

                self.hend_input = '' # после ввода очищаем поле

            fan = self.fan.x_code if self.fan else 0
            ram = self.ram.x_code if self.ram else 0
            cpu = self.cpu.x_code if self.cpu else 0
            cooler = self.cooler.x_code if self.cooler else 0
            mb = self.mb.x_code if self.mb else 0
            gpu = self.gpu.x_code if self.gpu else 0
            hdd = self.hdd.x_code if self.hdd else 0
            ssd = self.ssd.x_code if self.ssd else 0
            psu = self.psu.x_code if self.psu else 0
            case = self.case.x_code if self.case else 0
            wifi = self.wifi.x_code if self.wifi else 0
            cables = self.cables.x_code if self.cables else 0
            soft = self.soft.x_code if self.soft else 0

            parts = round(fan * self.vent_num_computers + \
            ram * self.mem_num_computers + \
            cpu + cooler + mb + gpu + \
            hdd + ssd + psu + case + \
            wifi + cables + soft)

            self.price_parts = parts
            rent = 1 + (self.rentability / 100)
            procent_prom_ = 1 + (self.procent_prom / 100)
            self.price_main = round(parts * rent)
            self.price_prom = round(parts * rent * procent_prom_)

            description_list = [
            {'name_parts': str(self.cpu), 'price': str(cpu)},
            {'name_parts': str(self.cooler), 'price': str(cooler)},
            {'name_parts': str(self.mb), 'price': str(mb)},
            {'name_parts': str(self.ram), 'price': f'{ram} * {self.mem_num_computers}'},
            {'name_parts': str(self.gpu), 'price': str(gpu)},
            {'name_parts': str(self.hdd), 'price': str(hdd)},
            {'name_parts': str(self.ssd), 'price': str(ssd)},
            {'name_parts': str(self.psu), 'price': str(psu)},
            {'name_parts': str(self.case), 'price': str(case)},
            {'name_parts': str(self.fan), 'price': f'{fan} * {self.vent_num_computers}'},
            {'name_parts': str(self.wifi), 'price': str(wifi)},
            {'name_parts': str(self.cables), 'price': str(cables)},
            {'name_parts': str(self.soft), 'price': str(soft)},
                                ]

            self.description = str(description_list) # структура для правильного
            # вывода в админке

            super().save(*args, **kwargs)
#
