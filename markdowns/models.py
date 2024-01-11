from django.db import models
from datetime import datetime, date, time
from django.db.models import signals
#from sereja.tasks_for_models import send_mail_task
#from httplib2 import Http
#from json import dumps
from django.db.models import Q
from django.db.models.functions import Length
from django.db.models import CharField
CharField.register_lookup(Length)
import re
#CharField.register_lookup(Length) providerprice_parts x_code

class Mark_short(models.Model):
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

    name_parts = models.CharField(max_length=300, db_index=True, verbose_name='Название')
    x_code = models.FloatField(default=0,max_length=50, db_index=True, verbose_name='Цена')
    trade_in_price = models.FloatField(default=0,max_length=50, db_index=True,
    verbose_name='Цена_trade_in')
    date_chg = models.DateTimeField(null=True, blank=True, verbose_name='Дата посл. изменения')
    kind = models.CharField(null=True, blank=True,max_length=50, db_index=True,
    verbose_name='Вид', choices=CHOISE)
    cooler_shorts = models.OneToOneField('Cooler',null=True, blank=True,
    on_delete=models.SET_NULL, verbose_name='Кулер')
    cpu_shorts = models.OneToOneField('CPU', null=True, blank=True,
    on_delete=models.SET_NULL, verbose_name='Проц')
    mb_shorts = models.OneToOneField('MB', null=True, blank=True,
    on_delete=models.SET_NULL, verbose_name='Мать')
    ram_shorts = models.OneToOneField('RAM', null=True, blank=True,
    on_delete=models.SET_NULL, verbose_name='Память')
    hdd_shorts = models.OneToOneField('HDD', null=True, blank=True,
    on_delete=models.SET_NULL, verbose_name='Ждиск')
    ssd_shorts = models.OneToOneField('SSD', null=True, blank=True,
    on_delete=models.SET_NULL, verbose_name='ССД')
    psu_shorts = models.OneToOneField('PSU', null=True, blank=True,
    on_delete=models.SET_NULL, verbose_name='БП')
    gpu_shorts = models.OneToOneField('GPU', null=True, blank=True,
    on_delete=models.SET_NULL, verbose_name='Видео')
    fan_shorts = models.OneToOneField('FAN', null=True, blank=True,
    on_delete=models.SET_NULL, verbose_name='Вентлтр')
    case_shorts = models.OneToOneField('CASE', null=True, blank=True,
    on_delete=models.SET_NULL, verbose_name='Корпус')
    wifi_shorts = models.OneToOneField('WiFi', null=True, blank=True,
    on_delete=models.SET_NULL, verbose_name='ВайФай')
    cables_shorts = models.OneToOneField('Cables', null=True,
    blank=True,on_delete=models.SET_NULL, verbose_name='Кабеля')
    soft_shorts = models.OneToOneField('Soft', null=True, blank=True,
    on_delete=models.SET_NULL, verbose_name='Софт')


    kind2 = models.BooleanField(default=True, verbose_name='active/deactive')
    only_comp = models.BooleanField(default=False, verbose_name='только в комп/везде')
    trade_in = models.BooleanField(default=False, verbose_name='trade_in')

    def __str__(self):
        return self.name_parts

    class Meta:
        unique_together = ('name_parts', 'kind')
        verbose_name_plural = 'АКЦИОННЫЕ_ДЕТАЛИ'
        verbose_name = 'Акция_деталь'
        ordering = ['-name_parts']

def post_saves_or_update_to_change_form(sender, instance, created, **kwargs):

    tuple_descr = {
    'cool': 'cooler_shorts_id', 'aproc': 'cpu_shorts_id', 'iproc': 'cpu_shorts_id',
    'amb': 'mb_shorts_id', 'imb': 'mb_shorts_id', 'mem': 'ram_shorts_id',
    'hdd': 'hdd_shorts_id', 'ssd':'ssd_shorts_id', 'ps': 'psu_shorts_id',
    'video': 'gpu_shorts_id', 'vent': 'fan_shorts_id', 'case': 'case_shorts_id',
    'wifi': 'wifi_shorts_id', 'cables': 'cables_shorts_id', 'soft': 'soft_shorts_id',
    }
    tuple_comps = {
    'cool': 'cooler_id', 'aproc': 'cpu_id', 'iproc': 'cpu_id',
    'amb': 'mb_id', 'imb': 'mb_id', 'mem': 'ram_id',
    'hdd': 'hdd_id', 'ssd':'ssd_id', 'ps': 'psu_id',
    'video': 'gpu_id', 'vent': 'fan_id', 'case': 'case_id',
    'wifi': 'wifi_id', 'cables': 'cables_id', 'soft': 'soft_id',
    }

    comps = Mark_computers.objects.filter(
    Q(cpu_id=instance.pk)|Q(ram_id=instance.pk)|
    Q(gpu_id=instance.pk)|Q(hdd_id=instance.pk)|
    Q(ssd_id=instance.pk)|
    Q(psu_id=instance.pk)|Q(case_id=instance.pk)|
    Q(cooler_id=instance.pk)|Q(fan_id=instance.pk)|
    Q(wifi_id=instance.pk)|Q(cables_id=instance.pk)|
    Q(soft_id=instance.pk)
    )
    for comp in comps:
        comp.__dict__[tuple_comps[instance.kind]] = instance.pk
        comp.save()

    if instance.__dict__[tuple_descr[instance.kind]]:
        temp = tuple_descr[instance.kind][:-3]
        try:
            instance_descr = eval(f"instance.{temp}")
        except:
            instance_descr = None
        if not instance_descr:
            return 0
        instance_descr.name = instance.name_parts
        instance_descr.is_active = instance.kind2
        try:
            instance_descr.price = instance.x_code
        except:
            instance_descr.r_price = instance.x_code
        instance_descr.save()

signals.post_save.connect(receiver=post_saves_or_update_to_change_form, sender=Mark_short)


class Category(models.Model):

    kind_assembly = models.CharField(default='Акционный', max_length=50, db_index=True,
    verbose_name='Серия')
    desc_ru = models.CharField(null=True, blank=True, max_length=500, db_index=True,
    verbose_name='Описание_рус')
    desc_ukr = models.CharField(null=True, blank=True, max_length=500, db_index=True,
    verbose_name='Описание_укр')

    def __str__(self):
        return self.kind_assembly

    class Meta:
        verbose_name_plural = 'Серии сайта'
        verbose_name = 'Серии сайта'


CHOISE_RU = (
    ('Да', 'Да'),
    ('Нет', 'Нет'),
)

CHOISE_UA = (
    ('Так', 'Так'),
    ('Нi', 'Нi'),
)

class Cooler(models.Model):
    name = models.CharField(max_length=300, unique=True, verbose_name='Name_cooler')
    part_number = models.CharField(max_length=300, db_index=True,
    verbose_name='Part_number', default='-')
    vendor = models.CharField(max_length=300, db_index=True,
    verbose_name='Vendor', default='-')
    price = models.FloatField(max_length=300, db_index=True,
    verbose_name='Price', default=0)
    rentability = models.FloatField(default=40, db_index=True, verbose_name='Наценка')
    desc_ukr = models.TextField(db_index=True, verbose_name='Desc_ukr', default='-')
    desc_ru = models.TextField(db_index=True, verbose_name='Desc_ru', default='-')
    fan_type_ua = models.CharField(max_length=300, db_index=True,
    verbose_name='Fan_type_ua', default='-')
    fan_type_rus = models.CharField(max_length=300, db_index=True,
    verbose_name='fan_type_rus', default='-')
    fan_spd_ua = models.CharField(max_length=300, db_index=True,
    verbose_name='Fan_spd_ua', default='-')
    fan_spd_rus = models.CharField(max_length=300, db_index=True,
    verbose_name='Fan_spd_rus', default='-')
    fan_noise_level = models.CharField(max_length=300, db_index=True,
    verbose_name='Fan_noise_level', default='-')
    fan_size = models.CharField(max_length=300, db_index=True,
    verbose_name='Fan_size', default='-')
    depend_to = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='Depend_to', default='-')
    depend_to_type = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='Depend_to_type', default='-')
    cooler_height = models.CharField(null=True,blank=True,
    max_length=30,db_index=True,verbose_name='cooler_height', default='-')
    fan_triple_wcs_rus = models.CharField(null=True, blank=True,
    verbose_name='СВО 3х куллерная(ру)',
    max_length=50, db_index=True, choices=CHOISE_RU, default='Нет')
    fan_triple_wcs_ua = models.CharField(null=True, blank=True,
    verbose_name='СВО 3х куллерная(укр)',
    max_length=50, db_index=True, choices=CHOISE_UA, default='Нi')
    label = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='label')
    fan_warr_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='гарантия укр')
    fan_warr_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='гарантия ру')
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('part_number', 'is_active')
        ordering = ['name']
        verbose_name = 'Кулер_уценка'
        verbose_name_plural = 'Кулеры_уценка'


class CPU(models.Model):
    name = models.CharField(max_length=300, unique=True, verbose_name='Name_cpu')
    part_number = models.CharField(max_length=300, db_index=True,
    verbose_name='Part_number', default='-')
    vendor = models.CharField(max_length=300, db_index=True,
    verbose_name='Vendor', default='-')
    price = models.FloatField(max_length=300, db_index=True,
    verbose_name='Price', default=0)
    rentability = models.FloatField(default=40, db_index=True, verbose_name='Наценка')
    desc_ukr = models.TextField(db_index=True, verbose_name='Desc_ukr', default='-')
    desc_ru = models.TextField(db_index=True, verbose_name='Desc_ru', default='-')
    f_name = models.CharField(max_length=300, db_index=True,
    verbose_name='f_name', default='-')
    cpu_c_t = models.CharField(max_length=300, db_index=True,
    verbose_name='Cpu_c_t', default='-')
    f_cpu_c_t = models.CharField(max_length=300, db_index=True,
    verbose_name='F_cpu_c_t', default='-')
    cpu_b_f = models.CharField(max_length=300, db_index=True,
    verbose_name='Cpu_b_f', default='-')
    cpu_cache = models.CharField(max_length=300, db_index=True,
    verbose_name='Cpu_cache', default='-')
    cpu_i_g_ua = models.CharField(max_length=300, db_index=True,
    verbose_name='Cpu_i_g_ua', default='-')
    cpu_i_g_rus = models.CharField(max_length=300, db_index=True,
    verbose_name='Cpu_i_g_rus', default='-')
    depend_from = models.CharField(max_length=300, db_index=True,
    verbose_name='Depend_from', default='-')
    depend_from_type = models.CharField(max_length=300, db_index=True,
    verbose_name='Depend_from_type', default='-')
    label = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='label')
    cpu_warr_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='гарантия укр')
    cpu_warr_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='гарантия ру')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('part_number', 'is_active')
        ordering = ['name']
        verbose_name = 'Проц_уценка'
        verbose_name_plural = 'Проц_уценка'


class MB(models.Model):

    CHOISE = (
        ('2', '2'),
        ('4', '4'),
        ('8', '8'),
    )

    CHOISE1 = (
        ('DDR3', 'DDR3'),
        ('DDR4', 'DDR4'),
        ('DDR5', 'DDR5'),
    )

    name = models.CharField(max_length=300, unique=True, verbose_name='Name_mb')
    part_number = models.CharField(max_length=300, db_index=True,
    verbose_name='Part_number', default='-')
    vendor = models.CharField(max_length=300, db_index=True,
    verbose_name='Vendor', default='-')
    main_category = models.CharField(max_length=300, db_index=True,
    verbose_name='Main_category', default='-')
    price = models.FloatField(max_length=300, db_index=True,
    verbose_name='Price', default=0)
    rentability = models.FloatField(default=40, db_index=True, verbose_name='Наценка')
    desc_ukr = models.TextField(db_index=True,
    verbose_name='Desc_ukr', default='-')
    desc_ru = models.TextField(db_index=True,
    verbose_name='Desc_ru', default='-')
    mb_chipset = models.CharField(max_length=300, db_index=True,
    verbose_name='Mb_chipset', default='-')
    mb_max_ram = models.CharField(max_length=300, db_index=True,
    verbose_name='Mb_max_ram', default='-')
    mb_count_slot = models.CharField(null=True, blank=True,
    verbose_name='Кол слотов памяти',
    max_length=50, db_index=True, choices=CHOISE, default='2')
    mb_type_memory = models.CharField(null=True, blank=True, verbose_name='Тип памяти',
    max_length=50, db_index=True, choices=CHOISE1, default='DDR4')
    depend_to = models.CharField(max_length=300, db_index=True,
    verbose_name='Depend_to', default='-')
    depend_to_type = models.CharField(max_length=300, db_index=True,
    verbose_name='Depend_to_type', default='-')
    depend_from = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='Depend_from', default='-')
    depend_from_type = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='Depend_from_type', default='-')
    label = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='label')
    mb_warr_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='гарантия укр')
    mb_warr_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='гарантия ру')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('part_number', 'is_active')
        ordering = ['name']
        verbose_name = 'Мат_плата_уценка'
        verbose_name_plural = 'Мат_платы_уценка'

class RAM(models.Model):

    CHOISE1 = (
        ('DDR3', 'DDR3'),
        ('DDR4', 'DDR4'),
        ('DDR5', 'DDR5'),
    )

    name = models.CharField(max_length=300, unique=True, verbose_name='Name_ram')
    part_number = models.CharField(max_length=300, db_index=True,
    verbose_name='Part_number', default='-')
    vendor = models.CharField(max_length=300, db_index=True,
    verbose_name='Vendor', default='-')
    f_name = models.CharField(max_length=300, db_index=True,
    verbose_name='f_name', default='-')
    price = models.FloatField(max_length=300, db_index=True,
    verbose_name='Price', default=0)
    rentability = models.FloatField(default=40, db_index=True, verbose_name='Наценка')
    desc_ukr = models.TextField(db_index=True, verbose_name='Desc_ukr', default='-')
    desc_ru = models.TextField(db_index=True, verbose_name='Desc_ru', default='-')
    mem_s = models.CharField(max_length=300, db_index=True,
    verbose_name='Mem_s', default='-')
    mem_spd = models.CharField(max_length=300, db_index=True,
    verbose_name='Mem_spd', default='-')
    mem_type = models.CharField(null=True, blank=True, verbose_name='Тип памяти',
    max_length=50, db_index=True, choices=CHOISE1, default='DDR4')
    mem_l = models.CharField(max_length=300, db_index=True,
    verbose_name='Mem_l', default='-')
    depend_from = models.CharField(null=True, blank=True, max_length=300,
    db_index=True,verbose_name='depend_from', default='-')
    depend_from_type = models.CharField(null=True, blank=True, max_length=300,
    db_index=True, verbose_name='depend_from_type', default='-')
    depend_to = models.CharField(null=True, blank=True, max_length=300,
    db_index=True,verbose_name='depend_to', default='-')
    depend_to_type = models.CharField(null=True, blank=True, max_length=300,
    db_index=True, verbose_name='depend_to_type', default='-')
    label = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='label')
    mem_warr_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='гарантия укр')
    mem_warr_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='гарантия ру')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('part_number', 'is_active')
        ordering = ['name']
        verbose_name = 'Память_уценка'
        verbose_name_plural = 'Память_уценка'


class HDD(models.Model):
    name = models.CharField(max_length=300, unique=True, verbose_name='Name_hdd')
    part_number = models.CharField(max_length=300, db_index=True,
    verbose_name='Part_number', default='-')
    vendor = models.CharField(max_length=300, db_index=True, verbose_name='Vendor', default='-')
    f_name = models.CharField(max_length=300, db_index=True, verbose_name='f_name', default='-')
    price = models.FloatField(max_length=300, db_index=True, verbose_name='Price', default=0)
    rentability = models.FloatField(default=40, db_index=True, verbose_name='Наценка')
    desc_ukr = models.TextField(db_index=True, verbose_name='Desc_ukr', default='-')
    desc_ru = models.TextField(db_index=True, verbose_name='Desc_ru', default='-')
    hdd_s = models.CharField(max_length=300, db_index=True,
    verbose_name='Hdd_s', default='-')
    hdd_spd_ua = models.CharField(max_length=300, db_index=True,
    verbose_name='Hdd_spd_ua', default='-')
    hdd_spd_rus = models.CharField(max_length=300, db_index=True, verbose_name='Hdd_spd_rus',
    default='-')
    hdd_ca = models.CharField(max_length=300, db_index=True, verbose_name='Hdd_ca',
    default='-')
    label = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='label')
    hdd_warr_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='гарантия укр')
    hdd_warr_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='гарантия ру')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('part_number', 'is_active')
        ordering = ['name']
        verbose_name = 'Жест_диск_уценка'
        verbose_name_plural = 'Жест_диски_уценка'


class PSU(models.Model):
    name = models.CharField(max_length=300, unique=True, verbose_name='Name_psu')
    part_number = models.CharField(max_length=300, db_index=True,
    verbose_name='Part_number', default='-')
    vendor = models.CharField(max_length=300, db_index=True, verbose_name='Vendor', default='-')
    price = models.FloatField(max_length=300, db_index=True, verbose_name='Price', default=0)
    rentability = models.FloatField(default=40, db_index=True, verbose_name='Наценка')
    desc_ukr = models.TextField(db_index=True, verbose_name='Desc_ukr', default='-')
    desc_ru = models.TextField(db_index=True, verbose_name='Desc_ru', default='-')
    psu_p = models.CharField(max_length=300, db_index=True, verbose_name='Psu_p', default='-')
    psu_c = models.CharField(max_length=300, db_index=True, verbose_name='Psu_c', default='-')
    psu_f = models.CharField(max_length=300, db_index=True, verbose_name='Psu_f', default='-')
    label = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='label')
    psu_warr_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='гарантия укр')
    psu_warr_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='гарантия ру')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('part_number', 'is_active')
        ordering = ['name']
        verbose_name = 'БП_уценка'
        verbose_name_plural = 'БП_уценка'


class GPU(models.Model):
    name = models.CharField(max_length=300, unique=True, verbose_name='Name_gpu')
    part_number = models.CharField(max_length=300, db_index=True,
    verbose_name='Part_number', default='-')
    vendor = models.CharField(max_length=300, db_index=True,
    verbose_name='Vendor', default='-')
    main_category = models.CharField(max_length=300, db_index=True,
    verbose_name='Main_category', default='-')
    f_name = models.CharField(max_length=300, db_index=True, verbose_name='f_name',
    default='-')
    price = models.FloatField(max_length=300, db_index=True, verbose_name='Price', default=0)
    rentability = models.FloatField(default=40, db_index=True, verbose_name='Наценка')
    desc_ukr = models.TextField(db_index=True, verbose_name='Desc_ukr', default='-')
    desc_ru = models.TextField(db_index=True, verbose_name='Desc_ru', default='-')
    gpu_fps = models.CharField(max_length=300, db_index=True, verbose_name='Gpu_fps',
    default='-')
    gpu_m_s = models.CharField(max_length=300, db_index=True, verbose_name='Gpu_m_s',
    default='-')
    gpu_b = models.CharField(max_length=300, db_index=True, verbose_name='Gpu_b',
    default='-')
    gpu_cpu_spd = models.CharField(max_length=300, db_index=True, verbose_name='Gpu_cpu_spd',
    default='-')
    gpu_mem_spd = models.CharField(max_length=300, db_index=True, verbose_name='Gpu_mem_spd',
    default='-')
    gpu_triple_fan_rus = models.CharField(null=True, blank=True,
    verbose_name='3х куллерная карта(ру)',
    db_index=True, max_length=10, choices=CHOISE_RU, default='Нет')
    gpu_triple_fan_ua = models.CharField(null=True, blank=True,
    verbose_name='3х куллерная карта(укр)',
    db_index=True, max_length=10, choices=CHOISE_UA, default='Нi')
    depend_to = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='Depend_to', default='-')
    depend_to_type = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='Depend_to_type', default='-')
    label = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='label')
    gpu_warr_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='гарантия укр')
    gpu_warr_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='гарантия ру')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('part_number', 'is_active')
        ordering = ['name']
        verbose_name = 'Видео_уценка'
        verbose_name_plural = 'Видео_уценка'


class FAN(models.Model):
    name = models.CharField(max_length=300, unique=True, verbose_name='Name_fan')
    part_number = models.CharField(max_length=300, db_index=True,
    verbose_name='Part_number', default='-')
    vendor = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='Vendor', default='-')
    price = models.FloatField(max_length=300, db_index=True, verbose_name='Price', default=0)
    rentability = models.FloatField(default=40, db_index=True, verbose_name='Наценка')
    desc_ukr = models.TextField(db_index=True, verbose_name='Desc_ukr', default='-')
    desc_ru = models.TextField(db_index=True, verbose_name='Desc_ru', default='-')
    case_fan_spd_ua = models.CharField(max_length=300, db_index=True,
    verbose_name='Case_fan_spd_ua',
    default='-')
    case_fan_spd_rus = models.CharField(max_length=300, db_index=True,
    verbose_name='Case_fan_spd_rus',
    default='-')
    case_fan_noise_level = models.CharField(max_length=300, db_index=True,
    verbose_name='Case_fan_noise_level', default='-')
    case_fan_size = models.CharField(max_length=300, db_index=True,
    verbose_name='Case_fan_size', default='-')
    label = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='label')
    case_fan_warr_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='гарантия укр')
    case_fan_warr_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='гарантия ру')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('part_number', 'is_active')
        ordering = ['name']
        verbose_name = 'Вент_уценка'
        verbose_name_plural = 'Вент_уценка'


class CASE(models.Model):

    CHOISE = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('4+', '4+'),
    )

    name = models.CharField(max_length=300, unique=True, verbose_name='Name_case')
    part_number = models.CharField(max_length=300, db_index=True, verbose_name='Part_number',
    default='-')
    vendor = models.CharField(max_length=300, db_index=True, verbose_name='Vendor', default='-')
    price = models.FloatField(max_length=300, db_index=True, verbose_name='Price', default=0)
    rentability = models.FloatField(default=40, db_index=True, verbose_name='Наценка')
    desc_ukr = models.TextField(db_index=True, verbose_name='Desc_ukr', default='-')
    desc_ru = models.TextField(db_index=True, verbose_name='Desc_ru', default='-')
    case_s = models.CharField(max_length=300, db_index=True, verbose_name='Case_s', default='-')
    color_parent = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='Color_parent', default='')
    color = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='Color', default='')
    color_ukr = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='Color_ukr', default='')
    color_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='Color_ru', default='')
    case_wcs_plus_size_ru = models.CharField(null=True, blank=True, verbose_name='360мм СВО(ру)',
    db_index=True, choices=CHOISE_RU,max_length=50, default='Нет')
    case_wcs_plus_size_ua = models.CharField(null=True, blank=True,
    verbose_name='360мм СВО(укр)',
    db_index=True, choices=CHOISE_UA,max_length=50, default='Нi')
    case_gpu_triple_fan_ru = models.CharField(null=True, blank=True,
    verbose_name='3х куллерная карта(ру)',
    db_index=True, choices=CHOISE_RU,max_length=50, default='Нет')
    case_gpu_triple_fan_ua = models.CharField(null=True, blank=True,
    verbose_name='3х куллерная карта(укр)',
    db_index=True, choices=CHOISE_UA,max_length=50, default='Нi')
    case_count_fan = models.CharField(null=True, blank=True,max_length=50, db_index=True,
    verbose_name='Кол вентиляторов', choices=CHOISE, default='2')
    depend_to = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='Depend_to', default='-')
    depend_to_type = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='Depend_to_type', default='-')
    case_height = models.CharField(null=True, blank=True, max_length=30, db_index=True,
    verbose_name='case_height', default='-')
    label = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='label')
    case_warr_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='гарантия укр')
    case_warr_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='гарантия ру')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('part_number', 'is_active')
        ordering = ['name']
        verbose_name = 'Корпус_уценка'
        verbose_name_plural = 'Корпуса_уценка'


class SSD(models.Model):
    name = models.CharField(max_length=300, unique=True, verbose_name='Name_ssd')
    part_number = models.CharField(default='-', max_length=300, db_index=True,
    verbose_name='Part_number')
    vendor = models.CharField(default='-', max_length=300, db_index=True, verbose_name='Vendor')
    f_name = models.CharField(default='-', max_length=300, db_index=True, verbose_name='f_name')
    price = models.FloatField(default=0, max_length=300, db_index=True, verbose_name='Price')
    rentability = models.FloatField(default=40, db_index=True, verbose_name='Наценка')
    desc_ukr = models.TextField(default='-', db_index=True, verbose_name='Desc_ukr')
    desc_ru = models.TextField(default='-', db_index=True, verbose_name='Desc_ru')
    ssd_s = models.CharField(default='-', max_length=300, db_index=True, verbose_name='Ssd_s')
    ssd_spd = models.CharField(default='-', max_length=300, db_index=True,
    verbose_name='Ssd_spd')
    ssd_r_spd = models.CharField(default='-', max_length=300, db_index=True,
    verbose_name='Ssd_r_spd')
    ssd_type_cells = models.CharField(default='-', max_length=300, db_index=True,
    verbose_name='ssd_type_cells')
    label = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='label')
    ssd_warr_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='гарантия укр')
    ssd_warr_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='гарантия ру')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('part_number', 'is_active')
        ordering = ['name']
        verbose_name = 'ССД_уценка'
        verbose_name_plural = 'ССД_уценка'

class WiFi(models.Model):
    name = models.CharField(max_length=300, unique=True, verbose_name='Name_wifi')
    part_number = models.CharField(default='-', max_length=300, db_index=True,
    verbose_name='Part_number')
    vendor = models.CharField(default='-', max_length=300, db_index=True, verbose_name='Vendor')
    r_price = models.FloatField(default=0, max_length=300, db_index=True, verbose_name='r_price')
    price = models.FloatField(default=0, max_length=300, db_index=True, verbose_name='Price')
    rentability = models.FloatField(default=40, db_index=True, verbose_name='Наценка')
    desc_ukr = models.TextField(default='-', db_index=True, verbose_name='Desc_ukr')
    desc_ru = models.TextField(default='-', db_index=True, verbose_name='Desc_ru')
    net_type_ukr = models.CharField(default='-', max_length=300, db_index=True,
    verbose_name='net_type_ukr')
    net_type_rus = models.CharField(default='-', max_length=300, db_index=True,
    verbose_name='net_type_rus')
    net_max_spd = models.CharField(default='-', max_length=300, db_index=True,
    verbose_name='net_max_spd')
    net_stand = models.CharField(default='-', max_length=300, db_index=True,
    verbose_name='net_stand')
    net_int = models.CharField(default='-', max_length=300, db_index=True,
    verbose_name='net_int')
    label = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='label')
    net_warr_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='гарантия укр')
    net_warr_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='гарантия ру')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('part_number', 'is_active')
        ordering = ['name']
        verbose_name = 'ВайФай_уценка'
        verbose_name_plural = 'ВайФай_уценка'

class Cables(models.Model):
    name = models.CharField(max_length=300, unique=True, verbose_name='Name_cables')
    part_number = models.CharField(default='-', max_length=300, db_index=True,
    verbose_name='Part_number')
    vendor = models.CharField(default='-', max_length=300, db_index=True, verbose_name='Vendor')
    r_price = models.FloatField(default=0, max_length=300, db_index=True, verbose_name='r_price')
    rentability = models.FloatField(default=40, db_index=True, verbose_name='Наценка')
    desc_ukr = models.TextField(default='-', db_index=True, verbose_name='Desc_ukr')
    desc_ru = models.TextField(default='-', db_index=True, verbose_name='Desc_ru')
    cab_mat_ukr = models.CharField(default='-', max_length=300, db_index=True,
    verbose_name='cab_mat_ukr')
    cab_mat_ru = models.CharField(default='-', max_length=300, db_index=True,
    verbose_name='cab_mat_ru')
    cab_col_ukr = models.CharField(default='-', max_length=300, db_index=True,
    verbose_name='cab_col_ukr')
    cab_col_ru = models.CharField(default='-', max_length=300, db_index=True,
    verbose_name='cab_col_ru')
    cab_set = models.CharField(default='-', max_length=300, db_index=True,
    verbose_name='cab_set')
    label = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='label')
    cab_warr_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='гарантия укр')
    cab_warr_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='гарантия ру')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('part_number', 'is_active')
        ordering = ['name']
        verbose_name = 'Кабеля_уценка'
        verbose_name_plural = 'Кабеля_уценка'

class Soft(models.Model):
    name = models.CharField(default='-', max_length=300, unique=True, verbose_name='Name_soft')
    part_number = models.CharField(default='-', max_length=300, db_index=True,
    verbose_name='Part_number')
    vendor = models.CharField(default='-', max_length=300, db_index=True, verbose_name='Vendor')
    r_price = models.FloatField(default=0, max_length=300, db_index=True, verbose_name='r_price')
    price = models.FloatField(default=0, max_length=300, db_index=True, verbose_name='Price')
    rentability = models.FloatField(default=40, db_index=True, verbose_name='Наценка')
    desc_ukr = models.TextField(default='-', db_index=True, verbose_name='Desc_ukr')
    desc_ru = models.TextField(default='-', db_index=True, verbose_name='Desc_ru')
    soft_type_ukr = models.CharField(default='-', max_length=300, db_index=True,
    verbose_name='soft_type_ukr')
    soft_type_ru = models.CharField(default='-', max_length=300, db_index=True,
    verbose_name='soft_type_ru')
    soft_lang_ukr = models.CharField(default='-', max_length=300, db_index=True,
    verbose_name='soft_lang_ukr')
    soft_lang_ru = models.CharField(default='-', max_length=300, db_index=True,
    verbose_name='soft_lang_ru')
    soft_set = models.CharField(default='-', max_length=300, db_index=True,
    verbose_name='soft_set')
    label = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='label')
    soft_warr_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='гарантия укр')
    soft_warr_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='гарантия ру')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('part_number', 'is_active')
        ordering = ['name']
        verbose_name = 'ПО_уценка'
        verbose_name_plural = 'ПО_уценка'

#Mark_short.objects.create(name_parts='пусто', kind='aproc')

class Mark_computers(models.Model):
    is_active = models.BooleanField(default=True)
    date_computers = models.DateTimeField(auto_now=True)
    name_computers = models.CharField(max_length=300, db_index=True,
    verbose_name='Имя компьютера', unique=True)
    price_computers = models.FloatField(default=0, db_index=True, verbose_name='Сумма')
    rentability = models.FloatField(default=40, db_index=True, verbose_name='Наценка')
    desc_ru = models.CharField(default='пусто',max_length=600, db_index=True,
    verbose_name='Описание рус')
    desc_ukr = models.CharField(default='пусто',max_length=600, db_index=True,
    verbose_name='Описание укр')

    cpu = models.ForeignKey(
    Mark_short,
    on_delete=models.CASCADE,
    limit_choices_to=Q(kind__in=('aproc', 'iproc')),
    related_name='cpu',
    #related_query_name='comp',
    verbose_name='Проц',
    null=True,
    blank=True,
    )

    mb = models.ForeignKey(
    Mark_short,
    on_delete=models.CASCADE,
    limit_choices_to=Q(kind__in=('amb', 'imb')),
    related_name='mb',
    #related_query_name='comp',
    verbose_name='Мат плата',
    null=True,
    blank=True,
    )

    ram = models.ForeignKey(
    Mark_short,
    on_delete=models.CASCADE,
    limit_choices_to={'kind': 'mem'},
    related_name='ram',
    #related_query_name='comp',
    verbose_name='ОЗУ',
    null=True,
    blank=True,
    )

    gpu = models.ForeignKey(
    Mark_short,
    on_delete=models.CASCADE,
    limit_choices_to={'kind': 'video'},
    related_name='gpu',
    #related_query_name='comp',
    verbose_name='Видео',
    null=True,
    blank=True,
    )

    hdd = models.ForeignKey(
    Mark_short,
    on_delete=models.CASCADE,
    limit_choices_to={'kind': 'hdd'},
    related_name='hdd',
    #related_query_name='comp',
    verbose_name='НДД',
    null=True,
    blank=True,
    )

    ssd = models.ForeignKey(
    Mark_short,
    on_delete=models.CASCADE,
    limit_choices_to={'kind': 'ssd'},
    related_name='ssd',
    #related_query_name='comp',
    verbose_name='ССД',
    null=True,
    blank=True,
    )

    psu = models.ForeignKey(
    Mark_short,
    on_delete=models.CASCADE,
    limit_choices_to={'kind': 'ps'},
    related_name='psu',
    #related_query_name='comp',
    verbose_name='БП',
    null=True,
    blank=True,
    )

    case = models.ForeignKey(
    Mark_short,
    on_delete=models.CASCADE,
    limit_choices_to={'kind': 'case'},
    related_name='case',
    #related_query_name='comp',
    verbose_name='Корпус',
    null=True,
    blank=True,
    )

    cooler = models.ForeignKey(
    Mark_short,
    on_delete=models.CASCADE,
    limit_choices_to={'kind': 'cool'},
    related_name='cooler',
    #related_query_name='comp',
    verbose_name='Кулер',
    null=True,
    blank=True,
    )

    fan = models.ForeignKey(
    Mark_short,
    on_delete=models.CASCADE,
    limit_choices_to={'kind': 'vent'},
    related_name='fan',
    #related_query_name='comp',
    verbose_name='Вентилятор',
    null=True,
    blank=True,
    )

    mon = models.ForeignKey(
    Mark_short,
    on_delete=models.CASCADE,
    limit_choices_to={'kind': 'mon'},
    related_name='mon',
    #related_query_name='comp',
    verbose_name='Монитор',
    null=True,
    blank=True,
    )

    wifi = models.ForeignKey(
    Mark_short,
    on_delete=models.CASCADE,
    limit_choices_to={'kind': 'wifi'},
    related_name='wifi',
    #related_query_name='comp',
    verbose_name='ВайФай',
    null=True,
    blank=True,
    )

    km = models.ForeignKey(
    Mark_short,
    on_delete=models.CASCADE,
    limit_choices_to={'kind': 'km'},
    related_name='km',
    #related_query_name='comp',
    verbose_name='КлМышь',
    null=True,
    blank=True,
    )

    cables = models.ForeignKey(
    Mark_short,
    on_delete=models.CASCADE,
    limit_choices_to={'kind': 'cables'},
    related_name='cables',
    #related_query_name='comp',
    verbose_name='Кабеля',
    null=True,
    blank=True,
    )

    soft = models.ForeignKey(
    Mark_short,
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
    video_num_computers = models.PositiveIntegerField(default=1, db_index=True,
    verbose_name='Видеокарты кол')
    vent_num_computers = models.PositiveIntegerField(default=1, db_index=True,
    verbose_name='Вентиляторы кол')
    you_vid = models.CharField(default='пусто',max_length=300, db_index=True, verbose_name='you_vid')

    category = models.ForeignKey(
                               'Category', on_delete=models.PROTECT,
                               null=True, blank=True, verbose_name='Серия'
                               )

    warr_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='гарантия укр')
    warr_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='гарантия ру')

    def __str__(self):
        return self.name_computers

    class Meta:
        verbose_name_plural = 'АКЦИОННЫЕ_КОМПЬЮТЕРЫ'
        verbose_name = 'Акционный_компьютер'
        ordering = ['-name_computers']

"""
def post_saves_and_calc(sender, instance, created, **kwargs):
    # рабочий код, меняет цену компа при изменении деталей (временно отключаю)

    calc_count = 0

    tuple_mark_comps = (
    'cpu_id', 'mb_id', 'ram_id', 'gpu_id',
    'hdd_id', 'ssd_id', 'psu_id',
    'case_id', 'cooler_id', 'fan_id', 'mon_id',
    'wifi_id', 'km_id', 'cables_id', 'soft_id',
    )

    for key_part in tuple_mark_comps:
        try:
            calc_count += round(Mark_short.objects.get(pk=instance.__dict__[key_part]).x_code)
        except:
            calc_count += 0

    if instance.mem_num_computers > 1:
        calc_count += (Mark_short.objects.get(pk=instance.ram.id).x_code) *\
        (instance.mem_num_computers - 1)
    if instance.video_num_computers > 1:
        calc_count += (Mark_short.objects.get(pk=instance.gpu.id).x_code) *\
        (instance.video_num_computers - 1)
    if instance.vent_num_computers > 1:
        calc_count += (Mark_short.objects.get(pk=instance.fan.id).x_code) *\
        (instance.vent_num_computers - 1)

    if calc_count != instance.price_computers:
        instance.price_computers = calc_count
        instance.save()

signals.post_save.connect(receiver=post_saves_and_calc, sender=Mark_computers)
"""
