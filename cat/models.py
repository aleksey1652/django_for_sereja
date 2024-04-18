from django.db import models
from datetime import datetime, date, time
import re
from django.db.models import signals
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from sereja.tasks_for_models import send_mail_task
#from httplib2 import Http
#from json import dumps
from django.db.models.functions import Length
from django.db.models import CharField
from descriptions.models import *
CharField.register_lookup(Length)

'''def pre_hook():
    """Hangouts Chat incoming webhook quickstart."""
    url = 'http://127.0.0.1:8000/pars/example'
    bot_message = {
        'text' : 'Hello from a Python script!'}

    message_headers = {'Content-Type': 'application/json; charset=UTF-8'}

    http_obj = Http()

    response = http_obj.request(
        uri=url,
        method='POST',
        headers=message_headers,
        body=dumps(bot_message),
    )

    print(response)'''


class USD(models.Model):
    usd = models.FloatField(db_index=True, verbose_name='usd')
    margin = models.FloatField(null=True, blank=True,
    db_index=False, verbose_name='наценка')
    #file_1c = models.FileField(upload_to='media')
    date_ch = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (self.date_ch).strftime("%d %B %Y") + ':' + str(self.usd)

    class Meta:
        verbose_name_plural = 'USD'
        verbose_name = 'USD'

class Parts_full(models.Model):

    CHOISE = (
        ('cool', 'cool'),
        ('imb', 'imb'),
        ('amb', 'amb'),
        ('case', 'case'),
        ('ssd', 'ssd'),
        ('hdd', 'hdd'),
        ('aproc', 'aproc'),
        ('iproc', 'iproc'),
        ('video', 'video'),
        ('ps', 'ps'),
        ('mem', 'mem'),
        ('vent', 'vent'),
        ('mon', 'mon'),
        ('wifi', 'wifi'),
        ('km', 'km'),
        ('soft', 'soft'),
        ('cables', 'cables'),
    )

    CHOISE2 = (
        ('yes', 'yes'),
        ('no', 'no'),
        ('q', 'q'),
        ('hand', 'hand'),
    )

    name_parts = models.CharField(max_length=300, db_index=True, verbose_name='Имя')
    partnumber_parts = models.CharField(null=True, blank=True,max_length=300,
    db_index=True, verbose_name='Артикул')
    availability_parts = models.CharField(null=True, blank=True,max_length=50, db_index=True,
    verbose_name='Наличие или авто-руч', choices=CHOISE2)
    providerprice_parts = models.FloatField(null=True, blank=True, db_index=False,
    max_length=50, verbose_name='Цена')
    rrprice_parts = models.FloatField(null=True, blank=True, db_index=False,
    max_length=50, verbose_name='Рекоменд')
    url_parts = models.CharField(null=True, blank=True,max_length=200, db_index=True,
    verbose_name='Url_parts')
    item_price = models.CharField(null=True, blank=True,max_length=50, db_index=True,
    verbose_name='Item_price')
    remainder = models.CharField(null=True, blank=True,max_length=50, db_index=True,
    verbose_name='Склад')
    providers = models.ForeignKey('Providers', on_delete=models.CASCADE,null=True,
    verbose_name='Поставщики')
    date_chg = models.DateTimeField(null=True, blank=True,
    verbose_name='Дата посл. изменения')
    is_hot = models.BooleanField(default=True)
    kind = models.CharField(null=True, blank=True,max_length=50,
    db_index=True, verbose_name='Вид', choices=CHOISE)
    name_parts_main = models.CharField(null=True, blank=True,max_length=300,
    db_index=True, verbose_name='1 поставщик')

    def get_short(self):
        try:
            short = self.parts_short_set.first().name_parts
        except:
            short = '--'

        return short

    get_short.short_description = 'комп-деталь'

    def __str__(self):
        return self.name_parts

    class Meta:
        verbose_name_plural = 'Прайс'
        verbose_name = 'Прайс'
        #ordering = ['-name_parts']
        ordering = ['providers__name_provider']

class Parts_short(models.Model):

    CHOISE = (
        ('cool', 'cool'),
        ('imb', 'imb'),
        ('amb', 'amb'),
        ('case', 'case'),
        ('ssd', 'ssd'),
        ('hdd', 'hdd'),
        ('aproc', 'aproc'),
        ('iproc', 'iproc'),
        ('video', 'video'),
        ('ps', 'ps'),
        ('mem', 'mem'),
        ('vent', 'vent'),
        ('mon', 'mon'),
        ('wifi', 'wifi'),
        ('km', 'km'),
        ('soft', 'soft'),
        ('cables', 'cables'),
    )

    name_parts = models.CharField(max_length=300, db_index=True, verbose_name='Имя')
    partnumber_list = models.CharField(null=True, blank=True,max_length=300,
    db_index=True, verbose_name='Служ код')
    x_code = models.FloatField(default=0,max_length=50, db_index=True, verbose_name='Цена')
    Advanced_parts = models.CharField(null=True, blank=True,max_length=50,
    db_index=True, verbose_name='Колличество')
    min_price = models.FloatField(default=0,max_length=50, db_index=True,
    verbose_name='ручная')
    special_price = models.FloatField(default=0, db_index=True, verbose_name='скидка')
    auto = models.BooleanField(default=False, verbose_name='руч/п')
    kind2 = models.BooleanField(default=False, verbose_name='выкл/вкл')
    config = models.BooleanField(default=True, verbose_name='конфиг')
    in_comps = models.BooleanField(default=False, verbose_name='в_сборке')
    date_chg = models.DateTimeField(null=True, blank=True,
    verbose_name='Дата посл. изменения')
    kind = models.CharField(null=True, blank=True,max_length=50,
    db_index=True, verbose_name='Вид', choices=CHOISE)
    parts_full = models.ManyToManyField('Parts_full', verbose_name='Прайс')
    computer_shorts = models.ManyToManyField('Computers', verbose_name='Комп')
    cooler_shorts = models.OneToOneField(Cooler,null=True, blank=True,
    on_delete=models.SET_NULL, verbose_name='Кулер')
    cpu_shorts = models.OneToOneField(CPU, null=True, blank=True,on_delete=models.SET_NULL,
    verbose_name='Проц')
    mb_shorts = models.OneToOneField(MB, null=True, blank=True,on_delete=models.SET_NULL,
    verbose_name='Мать')
    ram_shorts = models.OneToOneField(RAM, null=True, blank=True,on_delete=models.SET_NULL,
    verbose_name='Память')
    hdd_shorts = models.OneToOneField(HDD, null=True, blank=True,on_delete=models.SET_NULL,
    verbose_name='Ждиск')
    ssd_shorts = models.OneToOneField(SSD, null=True, blank=True,on_delete=models.SET_NULL,
    verbose_name='ССД')
    psu_shorts = models.OneToOneField(PSU, null=True, blank=True,on_delete=models.SET_NULL,
    verbose_name='БП')
    gpu_shorts = models.OneToOneField(GPU, null=True, blank=True,on_delete=models.SET_NULL,
    verbose_name='Видео')
    fan_shorts = models.OneToOneField(FAN, null=True, blank=True,on_delete=models.SET_NULL,
    verbose_name='Вентлтр')
    case_shorts = models.OneToOneField(CASE, null=True, blank=True,on_delete=models.SET_NULL,
    verbose_name='Корпус')
    wifi_shorts = models.OneToOneField(WiFi, null=True, blank=True,on_delete=models.SET_NULL,
    verbose_name='ВайФай')
    cables_shorts = models.OneToOneField(Cables, null=True,
    blank=True,on_delete=models.SET_NULL, verbose_name='Кабеля')
    soft_shorts = models.OneToOneField(Soft, null=True, blank=True,on_delete=models.SET_NULL,
    verbose_name='Софт')

    """def get_full(self):
        # получаем детали прайса
        return self.parts_full.all()"""

    def parts_full_price(self):
        try:
            price = round(self.parts_full.filter(
            availability_parts='yes').exclude(providerprice_parts=0
            ).order_by('providerprice_parts').first().providerprice_parts)
        except:
            price = 0

        return str(price)

    parts_full_price.short_description = 'пост'

    def parts_full_view(self):
        if self.parts_full.exists():
            return '; '.join(self.parts_full.all().order_by(
            'providerprice_parts').values_list('partnumber_parts', flat=True)[:3])
        else:
            return 'No relations'

    parts_full_view.short_description = 'Связь с прайсом'

    def get_providers(self):
        try:
            prov = self.parts_full.filter(
            availability_parts='yes').exclude(providerprice_parts=0
            ).order_by('providerprice_parts').first().name_parts_main
        except:
            prov = '--'

        return prov

    get_providers.short_description = 'Пост'

    def sklad_view(self):
        try:
            return round(float(
            re.findall(r':(.+);',
            self.parts_full.filter(
            providerprice_parts__gt=0).order_by('providerprice_parts'
            ).first().remainder)[0]))
        except:
            return '-'

    sklad_view.short_description = 'склад'

    def itblok_versum_view(self):
        view_ = '+' if self.kind2 == False else '--'
        return view_

    itblok_versum_view.short_description = '+/-'


    def description_view(self):
        descr = None
        from descriptions.models import Cooler,CPU,MB,RAM,HDD,PSU,GPU,FAN,CASE,SSD,WiFi,Cables,Soft
        from pars.ecatalog import dict_name_to_discr

        try:
            name_ = self.name_parts
            descr = eval(dict_name_to_discr[self.kind])
        except:
            descr = False
        try:
            descr = descr.filter(is_active=True).exists()
        except:
            descr = False
        descr = '+' if descr else '-'

        return descr
    description_view.short_description = 'Опис'


    def __str__(self):
        return self.name_parts

    class Meta:
        unique_together = ('name_parts', 'kind', 'kind2')
        verbose_name_plural = 'Компьютерные детали'
        verbose_name = 'Компьютерная деталь'
        ordering = ['-name_parts']

def post_saves_or_update_to_change_form(sender, instance, created, **kwargs):
    descr = None
    from descriptions.models import Cooler,CPU,MB,RAM,HDD,PSU,GPU,FAN,CASE,SSD,WiFi,Cables,Soft
    from pars.ecatalog import dict_name_to_discr, create_discr_from_cat_models, create_relation_from_cat_models

    try:
        name_ = instance.name_parts
        descr = eval(dict_name_to_discr[instance.kind])
    except:
        descr = None
    descr = descr.first() if descr else None
    if descr and instance.parts_full.exists():
        try:
            descr.is_active = True if instance.kind2 == False else False
            descr.config = True if instance.config == True else False
            descr.special_price = instance.special_price
            descr.name = instance.name_parts
            descr.part_number = instance.parts_full.order_by(
            'providerprice_parts').first().partnumber_parts
            price_ = instance.x_code if instance.x_code else 0
            try:
                descr.price = price_
            except:
                descr.r_price = price_
            #descr.is_active = True
            descr.save()
        except:
            pass
    elif descr and not instance.parts_full.exists():
        try:
            descr.is_active = False
            descr.save()
        except:
            pass

    create_relation_from_cat_models(instance)
    create_discr_from_cat_models(instance)

signals.post_save.connect(receiver=post_saves_or_update_to_change_form, sender=Parts_short)

"""def post_del_or_update_to_change_form(sender, instance, **kwargs):
    from cat.forms_admin_comps import ShortForm_aproc
    short_aproc = Parts_short.objects.filter(kind='aproc',kind2=False).values_list('name_parts',flat=True)
    CHOISE_aproc = [(short, short) for short in short_aproc]
    #kind_ = instance.kind
    ff = ShortForm_aproc()

signals.post_delete.connect(receiver=post_del_or_update_to_change_form, sender=Parts_short)"""

class Computers(models.Model):

    CHOISE_ru = (
        ('Готов к отправке', 'Готов к отправке'),
        ('Сборка 1-2 дня', 'Сборка 1-2 дня'),
        ('Сборка 3-5 дней', 'Сборка 3-5 дней'),)

    CHOISE_ukr = (
        ('Готовий до відправки', 'Готовий до відправки'),
        ('Збірка 1-2 днів', 'Збірка 1-2 днів'),
        ('Збірка 3-5 днів', 'Збірка 3-5 днів'),)

    name_computers = models.CharField(max_length=300, db_index=True,
    verbose_name='Имя компьютера')
    url_computers = models.CharField(max_length=300, db_index=True, verbose_name='Url')
    price_computers = models.FloatField(default=0, db_index=True, verbose_name='Сумма')
    proc_computers = models.CharField(max_length=300, db_index=True, verbose_name='Процессор')
    mb_computers = models.CharField(max_length=300, db_index=True,
    verbose_name='Материнская плата')
    mem_computers = models.CharField(max_length=300, db_index=True, verbose_name='ОЗУ')
    video_computers = models.CharField(max_length=300, db_index=True,
    verbose_name='Видеокарта')
    hdd_computers = models.CharField(max_length=300, db_index=True, verbose_name='HDD_SSD')
    ps_computers = models.CharField(max_length=300, db_index=True, verbose_name='БП')
    case_computers = models.CharField(max_length=300, db_index=True, verbose_name='Корпус')
    cool_computers = models.CharField(max_length=300, db_index=True, verbose_name='Кулер')
    class_computers = models.FloatField(max_length=30, db_index=True,
    default=1.17, verbose_name='Спецнаценка')
    warranty_computers = models.CharField(max_length=300, db_index=True,
    verbose_name='Спеццена')
    vent_computers = models.CharField(default='пусто',max_length=300, db_index=True,
    verbose_name='Вентилятор')
    mem_num_computers = models.CharField(default='1',max_length=300, db_index=True,
    verbose_name='ОЗУ кол')
    video_num_computers = models.CharField(default='1',max_length=300, db_index=True,
    verbose_name='Видеокарты кол')
    vent_num_computers = models.CharField(default='1',max_length=300, db_index=True,
    verbose_name='Вентиляторы кол')
    is_active = models.BooleanField(default=True)
    date_computers = models.DateTimeField(auto_now=True)
    mon_computers = models.CharField(default='пусто',max_length=300, db_index=True,
    verbose_name='Монитор')
    wifi_computers = models.CharField(default='пусто',max_length=300, db_index=True,
    verbose_name='WIFI')
    km_computers = models.CharField(default='пусто',max_length=300, db_index=True,
    verbose_name='Клав. мышь')
    cables_computers = models.CharField(default='пусто',max_length=300,db_index=True,
    verbose_name='Кабеля')
    soft_computers = models.CharField(default='пусто',max_length=300, db_index=True,
    verbose_name='Софт')
    you_vid = models.CharField(default='пусто',max_length=300, db_index=True,
    verbose_name='you_vid')
    perm_conf = models.CharField(default='пусто',max_length=300, db_index=True,
    verbose_name='perm_conf')
    elite_conf = models.CharField(default='пусто',max_length=300, db_index=True,
    verbose_name='elite_conf')

    time_assembly_ru = models.CharField(default='Сборка 3-5 дней', max_length=50,
    db_index=True, verbose_name='Срок сборки(ру)', choices=CHOISE_ru)
    time_assembly_ukr = models.CharField(default='Збірка 3-5 днів', max_length=50,
    db_index=True, verbose_name='Срок сборки(укр)', choices=CHOISE_ukr)

    pc_assembly = models.ForeignKey(
                               'Pc_assembly',on_delete=models.PROTECT,
                               null=True,verbose_name='Серия'
                               )
#
    def comp_name_plus(self):
        proc = re.sub(
        r'Ryzen|Athlon|Threadripper|Core|Pentium|Celeron', '', self.proc_computers).strip()
        try:
            gpu = re.findall('\w+ ', self.video_computers)[0].strip()
            if self.video_computers.lower().find(' super') != -1:
                gpu += '_SUPER'
        except:
            gpu = self.video_computers
        mem = '_'.join(re.findall(r'^\d+gb|ddr\d', self.mem_computers.lower()))
        try:
            mb = re.findall(r'^\w+', self.mb_computers)[0]
        except:
            mb = ''
        try:
            hdd_ssd = re.findall(r'\s(\d+[tg]b)', self.hdd_computers.lower())[0]
        except:
            hdd_ssd = ''
        try:
            ps = re.findall(r'\s(\d{2,4})w', self.ps_computers.lower())[0] + 'w'
        except:
            ps = ''
        if self.case_computers.lower().find('white') != -1:
            return f'{self.name_computers}---({proc}-{gpu}-{mem}-{mb}-{hdd_ssd}-{ps}-white)'
        return f'{self.name_computers}---({proc}-{gpu}-{mem}-{mb}-{hdd_ssd}-{ps})'


    comp_name_plus.short_description = 'Имя---(конфигурация)'

    def __str__(self):
        return self.name_computers

    class Meta:
        verbose_name_plural = 'Компьютеры'
        verbose_name = 'Компьютер'
        ordering = ['-name_computers']

class Computer_code(models.Model):
    comp = models.OneToOneField(
        Computers,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='code',
    )
    cpu_code = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='код процессора')
    video_code = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='код видео')
    mem_code = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='код памяти')
    video_html_code = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='код видео нтмл')

    code_is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.comp.name_computers + '_code'

    class Meta:
        verbose_name_plural = 'Фильтры для сравнения конкурентов'
        verbose_name = 'Фильтр для сравнения конкурентов'

class CompPrice(models.Model):
    name_computers = models.CharField(max_length=300, db_index=True, verbose_name='Name_computers')
    vent_computers = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='Url_computers')
    price_computers = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='Price_computers')
    proc_computers = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='Proc_computers')
    mb_computers = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='Mb_computers')
    mem_computers = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='Mem_computers')
    video_computers = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='Video_computers')
    hdd_computers = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='Hdd_computers')
    hdd2_computers = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='Hdd_computers')
    ps_computers = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='Ps_computers')
    case_computers = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='Case_computers')
    cool_computers = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='Cool_computers')
    mon_computers = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='mon_computers')
    wifi_computers = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='wifi_computers')
    km_computers = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='km_computers')
    cables_computers = models.CharField(null=True, blank=True,max_length=300,
    db_index=True, verbose_name='cables_computers')
    soft_computers = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='soft_computers')

    computers = models.OneToOneField(
        Computers,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    def __str__(self):
        return self.name_computers

    class Meta:
        verbose_name_plural = 'CompPrices'
        verbose_name = 'CompPrice'
        ordering = ['-name_computers']

class Sites(models.Model):
    CHOISE = (
        ('itblok', 'it-blok'),
        ('versum', 'versum'),
        ('fury', 'digitalfury'),
        ('ua', 'uastore'),
        ('art', 'artline'),
    )
    name_sites =  models.CharField(max_length=50, db_index=True, choices=CHOISE,default='itblok', verbose_name='Name_sites')
    more = models.TextField(null=True, blank=True, verbose_name='More_about_site')

    def __str__(self):
        return self.name_sites

    class Meta:
        verbose_name_plural = 'Sites'
        verbose_name = 'Site'

class Promotion(models.Model):
    prom = models.CharField(max_length=300, db_index=True, verbose_name='Ярлык', default='пусто')
    english_prom = models.CharField(null=True,blank=True,max_length=300, db_index=True, verbose_name='Ярлык(англ)', default='empty')

    computers = models.ManyToManyField('Computers',
    limit_choices_to={'pc_assembly__sites__name_sites': 'versum'}, verbose_name='Компьютеры')

    def display_computers(self):
        return ', '.join(str(genre.name_computers) for genre in self.computers.all())

    display_computers.short_description = 'Компьютеры'

    def __str__(self):
        return self.english_prom

    class Meta:
        verbose_name_plural = 'Компьютерные ярлыки'
        verbose_name = 'Компьютерный ярлык'
        ordering = ['prom__length']

class Providers(models.Model):
    CHOISE = (
        ('dc', 'dc-link'),
        ('itlink', 'it-link'),
        ('asbis', 'asbis'),
        ('elko', 'elko'),
        ('mti', 'mti'),
        ('brain', 'brain'),
        ('edg', 'edg'),
        ('erc', 'erc'),
        ('be', 'be'),
        ('dw', 'dw'),
        ('-', '-'),
    )
    # choices=CHOISE2,default='dc'
    name_provider =  models.CharField(max_length=50, db_index=True,
    choices=CHOISE,
    default='-', verbose_name='Name_provider')
    more = models.TextField(null=True, blank=True, verbose_name='More_about_provider')

    def __str__(self):
        return self.name_provider

    class Meta:
        verbose_name_plural = 'Provider'
        verbose_name = 'Providers+'

class Articles(models.Model):
    CHOISE = (
        ('cool', 'cool'),
        ('imb', 'imb'),
        ('amb', 'amb'),
        ('case', 'case'),
        ('ssd', 'ssd'),
        ('hdd', 'hdd'),
        ('aproc', 'aproc'),
        ('iproc', 'iproc'),
        ('video', 'video'),
        ('ps', 'ps'),
        ('mem', 'mem'),
        ('vent', 'vent'),
        ('mon', 'mon'),
        ('wifi', 'wifi'),
        ('km', 'km'),
        ('soft', 'soft'),
        ('cables', 'cables'),
    )
    article = models.CharField(max_length=50, db_index=True, verbose_name='Артикул', unique=True)
    providers = models.ManyToManyField(Providers)
    item_name = models.CharField(null=True, blank=True,max_length=100, db_index=True,
    verbose_name='Имя')
    item_price = models.CharField(null=True, blank=True,max_length=50, db_index=True,
    verbose_name='Вид', choices=CHOISE)
    #computers = models.ForeignKey(Computers, null=True,on_delete=models.CASCADE)
    parts_full = models.ManyToManyField('Parts_full')

    def __str__(self):
        return self.article

    class Meta:
        verbose_name_plural = 'Артикулы'
        verbose_name = 'Артикул'

class Pc_assembly(models.Model):
    name_assembly = models.CharField(max_length=300, db_index=True, verbose_name='Группы')
    kind_assembly = models.CharField(null=True, blank=True,max_length=50, db_index=True,
    verbose_name='Серии')
    desc_ru = models.CharField(null=True, blank=True,max_length=500, db_index=True,
    verbose_name='Описание_рус')
    desc_ukr = models.CharField(null=True, blank=True,max_length=500, db_index=True,
    verbose_name='Описание_укр')

    sites = models.ForeignKey(
                               'Sites',on_delete=models.PROTECT,
                               null=True,verbose_name='Сайт',
                               related_query_name='entry'
                               )

    def __str__(self):
        return self.name_assembly

    class Meta:
        verbose_name_plural = 'Серии сайта'
        verbose_name = 'Серии сайта'
        ordering = ['kind_assembly']

class Results(models.Model):
    who = models.CharField(null=True, blank=True,max_length=50, db_index=True,
    verbose_name='От кого')
    who_desc = models.TextField(null=True, blank=True, db_index=True, verbose_name='Инфо')
    json_data = models.JSONField(null=True,blank=True,verbose_name='Инфо+')
    date_ch = models.DateTimeField(auto_now=True, verbose_name='Дата')

    def __str__(self):
        return (self.date_ch).strftime("%d %B %Y, %H:%M:%S") + ':' + str(self.who)

    class Meta:
        verbose_name_plural = '_Результаты выгрузок'
        verbose_name = '_Результаты выгрузок'
        ordering = ['date_ch']

#def result_saves(sender, instance, created, **kwargs):
#    if Senders.objects.last() and Senders.objects.last().send_or_not:
#        r = Results.objects.last()
#        send_mail_task.delay(subject='Versum_results', message=r.who_desc,
#        from_email='peregonnata@gmail.com', recipients=Senders.objects.last().mail_from)
#    else:
#        print("don't send")

#signals.post_save.connect(receiver=result_saves, sender=Results)

class Senders(models.Model):
    send_or_not = models.BooleanField(default=True)
    mail_from = models.CharField(max_length=100, db_index=True, verbose_name='Mail_from')
    who = models.CharField(max_length=100, db_index=True, verbose_name='Who')
    date_ch = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (self.date_ch).strftime("%d %B %Y, %H:%M:%S") + ':' + str(self.mail_from)

    class Meta:
        ordering = ['date_ch']

class One_C(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Name',
    default='somebody')
    text_test = models.TextField(null=True, blank=True,max_length=5000, db_index=True,
    verbose_name='text_test')
    json_data = models.JSONField(null=True,blank=True,verbose_name='json_data')
    date_ch = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date_ch']

    def __str__(self):
        return str(self.name) + ':' + (self.date_ch).strftime("%d %B %Y, %H:%M")
