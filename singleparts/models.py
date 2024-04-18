from django.db import models
from datetime import datetime, date, time
#from django.db.models import signals
from django.core.exceptions import ValidationError
from django.http import HttpResponse
#from sereja.tasks_for_models import send_mail_task
#from django.db.models.functions import Length
#from django.db.models import CharField
#CharField.register_lookup(Length)


CHOISE_RU = (
    ('Да', 'Да'),
    ('Нет', 'Нет'),
)

CHOISE_UA = (
    ('Так', 'Так'),
    ('Нi', 'Нi'),
)

CHOISE_plmin = (
    ('+', '+'),
    ('-', '-'),
)

CHOISE_TYPE_RU = (
    ('Водяное охлаждение', 'Водяное охлаждение'),
    ('Воздушное охлаждение', 'Воздушное охлаждение'),
)

CHOISE_TYPE_UA = (
    ('Повітряне охолодження', 'Повітряне охолодження'),
    ('Водяне охолодження', 'Водяне охолодження'),
)

class Cooler_OTHER(models.Model):

    name = models.CharField(max_length=300, unique=True, verbose_name='имя')
    category_ru = models.CharField(null=True, blank=True, max_length=300,
    verbose_name='категория_ру')
    category_ua = models.CharField(null=True, blank=True, max_length=300,
    verbose_name='категория_у')
    part_number = models.CharField(max_length=300, db_index=True,
    verbose_name='партнамбер')
    part_number_web = models.CharField(max_length=300, db_index=True,
    verbose_name='партнамбер_веб')
    is_active = models.BooleanField(default=True, verbose_name='вкл/выкл')
    full = models.BooleanField(default=True, verbose_name='заполнен/нет')
    hotline = models.BooleanField(default=False, verbose_name='hotline')
    delivery = models.BooleanField(default=False, verbose_name='доствка')
    creditoff = models.BooleanField(default=False, verbose_name='credit')
    label = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='label')

    price_rent = models.FloatField(max_length=300, db_index=True,
    verbose_name='цена с нац')
    r_price = models.FloatField(max_length=300, db_index=True,
    verbose_name='r_price')
    rrp_price = models.FloatField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='rrp')
    auto = models.BooleanField(default=False, verbose_name='руч/п')
    price_ua = models.FloatField(max_length=300, db_index=True, verbose_name='цена грн')
    price_usd = models.FloatField(max_length=300, db_index=True,
    verbose_name='цена $')
    rentability = models.FloatField(default=5, db_index=True, verbose_name='наценка')
    provider = models.CharField(default='dc', max_length=300,
    db_index=True, verbose_name='пост')

    vendor = models.CharField(null=True, blank=True,max_length=300,
    db_index=True, verbose_name='производитель')
    cool_type_ua = models.TextField(null=True, blank=True,
    db_index=True, verbose_name='тип_укр', choices=CHOISE_TYPE_UA)
    cool_type_ru = models.TextField(null=True, blank=True,
    db_index=True, verbose_name='тип_ру', choices=CHOISE_TYPE_RU)
    cool_ai_ua = models.TextField(null=True, blank=True,
    db_index=True, verbose_name='описание_укр')
    cool_ai_ru = models.TextField(null=True, blank=True,
    db_index=True, verbose_name='описание_ру')
    cool_fan_max_spd_ua = models.CharField(null=True, blank=True,
    max_length=300, db_index=True,
    verbose_name='скорость вращения (max)укр')
    cool_fan_max_spd_ru = models.CharField(null=True, blank=True,
    max_length=300, db_index=True,
    verbose_name='скорость вращения (max)ру')
    cool_fan_size = models.CharField(null=True, blank=True,
    max_length=300, db_index=True,
    verbose_name='диаметр')
    cool_tub_am = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='кол тепловых труб')
    cool_sock = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='сокет')
    cool_max_tdp = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='максимальное TDP')
    cool_col_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='цвет укр')
    cool_col_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='цвет ру')
    cool_rgb = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='подсветка')
    cool_h = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='высота кулера')
    cool_warr_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='гарантия укр')
    cool_warr_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='гарантия ру')
    you_vid = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='you_vid')
    cover1 = models.ImageField(null=True, blank=True,
    verbose_name='фото1')
    cover2 = models.ImageField(null=True, blank=True,
    verbose_name='фото2')
    cover3 = models.ImageField(null=True, blank=True,
    verbose_name='фото3')
    groups = models.ForeignKey(
                               'self', on_delete=models.PROTECT,
                               related_name="tags",
                               related_query_name="tag",
                               null=True, blank=True, verbose_name='Связь'
                               )

    def __str__(self):
        return self.name

    def get_sum_part_number(self):
        if self.tags.exists():
            return f"{';'.join(self.tags.all().values_list('part_number', flat=True))}"

        return self.part_number

    get_sum_part_number.short_description = 'связь-партнамберов'

    def get_price_rent_price_ua(self):
        try:
            return round((self.price_rent / self.price_ua - 1) * 100)
        except:
            return 0
    get_price_rent_price_ua.short_description = '$'

    class Meta:
        unique_together = ('part_number', 'is_active')
        ordering = ['name']
        verbose_name = 'Кулер'
        verbose_name_plural = 'Кулеры'


class CPU_OTHER(models.Model):

    name = models.CharField(max_length=300, unique=True, verbose_name='имя')
    category_ru = models.CharField(null=True, blank=True, max_length=300,
    verbose_name='категория_ру')
    category_ua = models.CharField(null=True, blank=True, max_length=300,
    verbose_name='категория_у')
    part_number = models.CharField(max_length=300, db_index=True, verbose_name='партнамбер')
    part_number_web = models.CharField(max_length=300, db_index=True,
    verbose_name='партнамбер_веб')
    is_active = models.BooleanField(default=True, verbose_name='вкл/выкл')
    full = models.BooleanField(default=True, verbose_name='заполнен/нет')
    hotline = models.BooleanField(default=False, verbose_name='hotline')
    delivery = models.BooleanField(default=False, verbose_name='доствка')
    creditoff = models.BooleanField(default=False, verbose_name='credit')
    label = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='label')

    price_rent = models.FloatField(max_length=300, db_index=True,
    verbose_name='цена с нац')
    r_price = models.FloatField(max_length=300, db_index=True,
    verbose_name='r_price')
    rrp_price = models.FloatField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='rrp')
    auto = models.BooleanField(default=False, verbose_name='руч/п')
    price_ua = models.FloatField(max_length=300, db_index=True, verbose_name='цена грн')
    price_usd = models.FloatField(max_length=300, db_index=True,
    verbose_name='цена $')
    rentability = models.FloatField(default=5, db_index=True, verbose_name='наценка')
    provider = models.CharField(default='dc', max_length=300,
    db_index=True, verbose_name='пост')

    vendor = models.CharField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='производитель')
    cpu_ai_ua = models.TextField(null=True, blank=True,
    db_index=True, verbose_name='описание_укр')
    cpu_ai_ru = models.TextField(null=True, blank=True,
    db_index=True, verbose_name='описание_ру')
    cpu_fam = models.CharField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='линейка')
    cpu_bfq = models.CharField(null=True, blank=True,
    max_length=300, db_index=True,
    verbose_name='тактовая частота')
    cpu_cache = models.CharField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='кеш')

    cpu_soc = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='тип разъема (Socket)')
    cpu_core = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='кол ядер')
    cpu_threeds = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='кол потоков')
    cpu_tbfq = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='тактовая частота (max)')
    cpu_gpu = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='графика')
    cpu_warr_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='гарантия укр')
    cpu_warr_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='гарантия ру')
    you_vid = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='you_vid')
    cover1 = models.ImageField(null=True, blank=True,
    verbose_name='фото1')
    cover2 = models.ImageField(null=True, blank=True,
    verbose_name='фото2')
    cover3 = models.ImageField(null=True, blank=True,
    verbose_name='фото3')
    groups = models.ForeignKey(
                               'self', on_delete=models.PROTECT,
                               related_name="tags",
                               related_query_name="tag",
                               null=True, blank=True, verbose_name='Связь'
                               )

    def __str__(self):
        return self.name

    def get_sum_part_number(self):
        if self.tags.exists():
            return f"{';'.join(self.tags.all().values_list('part_number', flat=True))}"

        return self.part_number

    get_sum_part_number.short_description = 'связь-партнамберов'

    def get_r_price_rrp_price(self):
        rrp = self.rrp_price if self.rrp_price else 0
        return f"{self.r_price}/ {rrp}"
    get_r_price_rrp_price.short_description = 'r_price/ rrp'

    def get_price_rent_price_ua(self):
        try:
            return round((self.price_rent / self.price_ua - 1) * 100)
        except:
            return 0
    get_price_rent_price_ua.short_description = '$'

    class Meta:
        unique_together = ('part_number', 'is_active')
        ordering = ['name']
        verbose_name = 'Процессор'
        verbose_name_plural = 'Процессоры'


class MB_OTHER(models.Model):

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

    name = models.CharField(max_length=300, unique=True, verbose_name='имя')
    category_ru = models.CharField(null=True, blank=True, max_length=300,
    verbose_name='категория_ру')
    category_ua = models.CharField(null=True, blank=True, max_length=300,
    verbose_name='категория_у')
    part_number = models.CharField(max_length=300, db_index=True, verbose_name='партнамбер')
    part_number_web = models.CharField(max_length=300, db_index=True,
    verbose_name='партнамбер_веб')
    is_active = models.BooleanField(default=True, verbose_name='вкл/выкл')
    full = models.BooleanField(default=True, verbose_name='заполнен/нет')
    hotline = models.BooleanField(default=False, verbose_name='hotline')
    delivery = models.BooleanField(default=False, verbose_name='доствка')
    creditoff = models.BooleanField(default=False, verbose_name='credit')
    label = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='label')

    price_rent = models.FloatField(max_length=300, db_index=True,
    verbose_name='цена с нац')
    r_price = models.FloatField(max_length=300, db_index=True,
    verbose_name='r_price')
    rrp_price = models.FloatField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='rrp')
    auto = models.BooleanField(default=False, verbose_name='руч/п')
    price_ua = models.FloatField(max_length=300, db_index=True, verbose_name='цена грн')
    price_usd = models.FloatField(max_length=300, db_index=True,
    verbose_name='цена $')
    rentability = models.FloatField(default=5, db_index=True, verbose_name='наценка')
    provider = models.CharField(default='dc', max_length=300,
    db_index=True, verbose_name='пост')

    vendor = models.CharField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='производитель')
    part_mb_fam = models.CharField(null=True, blank=True,
    max_length=300, db_index=True,
    verbose_name='для процессоров')
    part_mb_ai_ua = models.TextField(null=True, blank=True,
    db_index=True, verbose_name='описание_укр')
    part_mb_ai_ru = models.TextField(null=True, blank=True,
    db_index=True, verbose_name='описание_ру')
    part_mb_chip = models.CharField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='чипсет')
    part_mb_ram_max_size = models.CharField(null=True, blank=True,
    max_length=300, db_index=True,
    verbose_name='макс. объем памяти')
    part_mb_ram_sl = models.CharField(null=True, blank=True, verbose_name='кол слотов памяти',
    max_length=50, db_index=True, choices=CHOISE)
    part_mb_ram_type = models.CharField(null=True, blank=True, verbose_name='тип памяти',
    max_length=50, db_index=True, choices=CHOISE1)

    part_mb_sock = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='тип разъема (Socket)')
    part_mb_ff = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='форм-фактор')
    part_mb_rgb_header = models.BooleanField(default=False,
    verbose_name='RGB Header')
    part_mb_ram_max_spd = models.CharField(null=True, blank=True,max_length=300,
    db_index=True, verbose_name='максимальная частота ОЗУ')
    part_mb_vga = models.BooleanField(default=False,
    verbose_name='видеовыход_vga')
    part_mb_dvi = models.BooleanField(default=False,
    verbose_name='видеовыход_dvi')
    part_mb_hdmi = models.BooleanField(default=False,
    verbose_name='видеовыход_hdmi')
    part_mb_dp = models.BooleanField(default=False,
    verbose_name='видеовыход_dp')
    part_mb_lan = models.BooleanField(default=False,
    verbose_name='разьем_lan')
    part_mb_wifi = models.BooleanField(default=False,
    verbose_name='разьем_wifi')
    part_mb_bt = models.BooleanField(default=False,
    verbose_name='разьем_bluetooth')
    part_mb_usb_type_c = models.BooleanField(default=False, verbose_name='USB Type-C')
    part_mb_sata = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='кол SATA')
    part_mb_m2 = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='кол M.2')
    part_mb_raid = models.BooleanField(default=False, verbose_name='наличие_raid')
    part_mb_warr_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='гарантия_ua')
    part_mb_warr_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='гарантия_ru')
    you_vid = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='you_vid')
    cover1 = models.ImageField(null=True, blank=True,
    verbose_name='фото1')
    cover2 = models.ImageField(null=True, blank=True,
    verbose_name='фото2')
    cover3 = models.ImageField(null=True, blank=True,
    verbose_name='фото3')
    groups = models.ForeignKey(
                               'self', on_delete=models.PROTECT,
                               related_name="tags",
                               related_query_name="tag",
                               null=True, blank=True, verbose_name='Связь'
                               )

    def __str__(self):
        return self.name

    def get_sum_part_number(self):
        if self.tags.exists():
            return f"{';'.join(self.tags.all().values_list('part_number', flat=True))}"

        return self.part_number

    get_sum_part_number.short_description = 'связь-партнамберов'

    def get_r_price_rrp_price(self):
        rrp = self.rrp_price if self.rrp_price else 0
        return f"{self.r_price}/ {rrp}"
    get_r_price_rrp_price.short_description = 'r_price/ rrp'

    def get_price_rent_price_ua(self):
        try:
            return round((self.price_rent / self.price_ua - 1) * 100)
        except:
            return 0
    get_price_rent_price_ua.short_description = '$'

    class Meta:
        unique_together = ('part_number', 'is_active')
        ordering = ['name']
        verbose_name = 'Материнская плата'
        verbose_name_plural = 'Материнские платы'


class RAM_OTHER(models.Model):

    CHOISE1 = (
        ('DDR3', 'DDR3'),
        ('DDR4', 'DDR4'),
        ('DDR5', 'DDR5'),
    )

    name = models.CharField(max_length=300, unique=True, verbose_name='имя')
    category_ru = models.CharField(null=True, blank=True, max_length=300,
    verbose_name='категория_ру')
    category_ua = models.CharField(null=True, blank=True, max_length=300,
    verbose_name='категория_у')
    part_number = models.CharField(max_length=300, db_index=True, verbose_name='партнамбер')
    part_number_web = models.CharField(max_length=300, db_index=True,
    verbose_name='партнамбер_веб')
    is_active = models.BooleanField(default=True, verbose_name='вкл/выкл')
    full = models.BooleanField(default=True, verbose_name='заполнен/нет')
    hotline = models.BooleanField(default=False, verbose_name='hotline')
    delivery = models.BooleanField(default=False, verbose_name='доствка')
    creditoff = models.BooleanField(default=False, verbose_name='credit')
    label = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='label')

    price_rent = models.FloatField(max_length=300, db_index=True,
    verbose_name='цена с нац')
    r_price = models.FloatField(max_length=300, db_index=True,
    verbose_name='r_price')
    rrp_price = models.FloatField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='rrp')
    auto = models.BooleanField(default=False, verbose_name='руч/п')
    price_ua = models.FloatField(max_length=300, db_index=True, verbose_name='цена грн')
    price_usd = models.FloatField(max_length=300, db_index=True,
    verbose_name='цена $')
    rentability = models.FloatField(default=5, db_index=True, verbose_name='наценка')
    provider = models.CharField(default='dc', max_length=300,
    db_index=True, verbose_name='пост')

    vendor = models.CharField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='производитель')
    ram_size = models.CharField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='объём памяти')
    ram_ai_ua = models.TextField(null=True, blank=True,
    db_index=True, verbose_name='описание_укр')
    ram_ai_ru = models.TextField(null=True, blank=True,
    db_index=True, verbose_name='описание_ру')
    ram_fq = models.CharField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='частота памяти')
    ram_type = models.CharField(default='DDR4', verbose_name='тип памяти',
    max_length=50, db_index=True, choices=CHOISE1)
    ram_cl = models.CharField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='тайминги')
    ram_led = models.BooleanField(default=False, verbose_name='подсветка')

    ram_mod_am = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='кол модулей')
    ram_col_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='цвет_укр')
    ram_col_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='цвет_ру')
    ram_warr_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='гарантия_укр')
    ram_warr_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='гарантия_ру')
    you_vid = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='you_vid')
    cover1 = models.ImageField(null=True, blank=True,
    verbose_name='фото1')
    cover2 = models.ImageField(null=True, blank=True,
    verbose_name='фото2')
    cover3 = models.ImageField(null=True, blank=True,
    verbose_name='фото3')
    groups = models.ForeignKey(
                               'self', on_delete=models.PROTECT,
                               related_name="tags",
                               related_query_name="tag",
                               null=True, blank=True, verbose_name='Связь'
                               )

    def __str__(self):
        return self.name

    def get_sum_part_number(self):
        if self.tags.exists():
            return f"{';'.join(self.tags.all().values_list('part_number', flat=True))}"

        return self.part_number

    get_sum_part_number.short_description = 'связь-партнамберов'

    def get_r_price_rrp_price(self):
        rrp = self.rrp_price if self.rrp_price else 0
        return f"{self.r_price}/ {rrp}"
    get_r_price_rrp_price.short_description = 'r_price/ rrp'

    def get_price_rent_price_ua(self):
        try:
            return round((self.price_rent / self.price_ua - 1) * 100)
        except:
            return 0
    get_price_rent_price_ua.short_description = '$'

    class Meta:
        unique_together = ('part_number', 'is_active')
        ordering = ['name']
        verbose_name = 'Память'
        verbose_name_plural = 'Память'


class HDD_OTHER(models.Model):

    name = models.CharField(max_length=300, unique=True, verbose_name='имя')
    category_ru = models.CharField(null=True, blank=True, max_length=300,
    verbose_name='категория_ру')
    category_ua = models.CharField(null=True, blank=True, max_length=300,
    verbose_name='категория_у')
    part_number = models.CharField(max_length=300, db_index=True, verbose_name='партнамбер')
    part_number_web = models.CharField(max_length=300, db_index=True,
    verbose_name='партнамбер_веб')
    is_active = models.BooleanField(default=True, verbose_name='вкл/выкл')
    full = models.BooleanField(default=True, verbose_name='заполнен/нет')
    hotline = models.BooleanField(default=False, verbose_name='hotline')
    delivery = models.BooleanField(default=False, verbose_name='доствка')
    creditoff = models.BooleanField(default=False, verbose_name='credit')
    label = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='label')

    price_rent = models.FloatField(max_length=300, db_index=True,
    verbose_name='цена с нац')
    r_price = models.FloatField(max_length=300, db_index=True,
    verbose_name='r_price')
    rrp_price = models.FloatField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='rrp')
    auto = models.BooleanField(default=False, verbose_name='руч/п')
    price_ua = models.FloatField(max_length=300, db_index=True, verbose_name='цена грн')
    price_usd = models.FloatField(max_length=300, db_index=True,
    verbose_name='цена $')
    rentability = models.FloatField(default=5, db_index=True, verbose_name='наценка')
    provider = models.CharField(default='dc', max_length=300,
    db_index=True, verbose_name='пост')

    vendor = models.CharField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='производитель')
    hdd_ai_ua = models.TextField(null=True, blank=True,
    db_index=True, verbose_name='описание_укр')
    hdd_ai_ru = models.TextField(null=True, blank=True,
    db_index=True, verbose_name='описание_ру')
    hdd_size = models.CharField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='объем')
    hdd_spd_ph_ua = models.CharField(null=True, blank=True,
    max_length=300, db_index=True,
    verbose_name='скорость вращения укр')
    hdd_spd_ph_ru = models.CharField(null=True, blank=True,
    max_length=300, db_index=True,
    verbose_name='скорость вращения ру')
    hdd_buf = models.CharField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='буфер обмена')

    hdd_ff = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='форм-фактор')
    hdd_warr_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='гарантия_укр')
    hdd_warr_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='гарантия_ру')
    you_vid = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='you_vid')
    cover1 = models.ImageField(null=True, blank=True,
    verbose_name='фото1')
    cover2 = models.ImageField(null=True, blank=True,
    verbose_name='фото2')
    cover3 = models.ImageField(null=True, blank=True,
    verbose_name='фото3')
    groups = models.ForeignKey(
                               'self', on_delete=models.PROTECT,
                               related_name="tags",
                               related_query_name="tag",
                               null=True, blank=True, verbose_name='Связь'
                               )

    def __str__(self):
        return self.name

    def get_sum_part_number(self):
        if self.tags.exists():
            return f"{';'.join(self.tags.all().values_list('part_number', flat=True))}"

        return self.part_number

    get_sum_part_number.short_description = 'связь-партнамберов'

    def get_r_price_rrp_price(self):
        rrp = self.rrp_price if self.rrp_price else 0
        return f"{self.r_price}/ {rrp}"
    get_r_price_rrp_price.short_description = 'r_price/ rrp'

    def get_price_rent_price_ua(self):
        try:
            return round((self.price_rent / self.price_ua - 1) * 100)
        except:
            return 0
    get_price_rent_price_ua.short_description = '$'

    class Meta:
        unique_together = ('part_number', 'is_active')
        ordering = ['name']
        verbose_name = 'Жесткий диск'
        verbose_name_plural = 'Жесткие диски'

class PSU_OTHER(models.Model):

    name = models.CharField(max_length=300, unique=True, verbose_name='имя')
    category_ru = models.CharField(null=True, blank=True, max_length=300,
    verbose_name='категория_ру')
    category_ua = models.CharField(null=True, blank=True, max_length=300,
    verbose_name='категория_у')
    part_number = models.CharField(max_length=300, db_index=True, verbose_name='партнамбер')
    part_number_web = models.CharField(max_length=300, db_index=True,
    verbose_name='партнамбер_веб')
    is_active = models.BooleanField(default=True, verbose_name='вкл/выкл')
    full = models.BooleanField(default=True, verbose_name='заполнен/нет')
    hotline = models.BooleanField(default=False, verbose_name='hotline')
    delivery = models.BooleanField(default=False, verbose_name='доствка')
    creditoff = models.BooleanField(default=False, verbose_name='credit')
    label = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='label')

    price_rent = models.FloatField(max_length=300, db_index=True,
    verbose_name='цена с нац')
    r_price = models.FloatField(max_length=300, db_index=True,
    verbose_name='r_price')
    rrp_price = models.FloatField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='rrp')
    auto = models.BooleanField(default=False, verbose_name='руч/п')
    price_ua = models.FloatField(max_length=300, db_index=True, verbose_name='цена грн')
    price_usd = models.FloatField(max_length=300, db_index=True,
    verbose_name='цена $')
    rentability = models.FloatField(default=5, db_index=True, verbose_name='наценка')
    provider = models.CharField(default='dc', max_length=300,
    db_index=True, verbose_name='пост')

    vendor = models.CharField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='производитель')
    psu_pow = models.CharField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='мощность')
    psu_80 = models.CharField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='сертификация БП')
    psu_fan = models.CharField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='вентиляторы')
    psu_mod = models.BooleanField(default=False, verbose_name='модульность')
    psu_ai_ua = models.TextField(null=True, blank=True,
    db_index=True, verbose_name='описание_укр')
    psu_ai_ru = models.TextField(null=True, blank=True,
    db_index=True, verbose_name='описание_ру')

    psu_ff = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='форм-фактор')
    psu_warr_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='гарантия_укр')
    psu_warr_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='гарантия_ру')
    you_vid = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='you_vid')
    cover1 = models.ImageField(null=True, blank=True,
    verbose_name='фото1')
    cover2 = models.ImageField(null=True, blank=True,
    verbose_name='фото2')
    cover3 = models.ImageField(null=True, blank=True,
    verbose_name='фото3')
    groups = models.ForeignKey(
                               'self', on_delete=models.PROTECT,
                               related_name="tags",
                               related_query_name="tag",
                               null=True, blank=True, verbose_name='Связь'
                               )

    def __str__(self):
        return self.name

    def get_sum_part_number(self):
        if self.tags.exists():
            return f"{';'.join(self.tags.all().values_list('part_number', flat=True))}"

        return self.part_number

    get_sum_part_number.short_description = 'связь-партнамберов'

    def get_r_price_rrp_price(self):
        rrp = self.rrp_price if self.rrp_price else 0
        return f"{self.r_price}/ {rrp}"
    get_r_price_rrp_price.short_description = 'r_price/ rrp'

    def get_price_rent_price_ua(self):
        try:
            return round((self.price_rent / self.price_ua - 1) * 100)
        except:
            return 0
    get_price_rent_price_ua.short_description = '$'

    class Meta:
        unique_together = ('part_number', 'is_active')
        ordering = ['name']
        verbose_name = 'БП'
        verbose_name_plural = 'БП'


class GPU_OTHER(models.Model):

    name = models.CharField(max_length=300, unique=True, verbose_name='имя')
    category_ru = models.CharField(null=True, blank=True, max_length=300,
    verbose_name='категория_ру')
    category_ua = models.CharField(null=True, blank=True, max_length=300,
    verbose_name='категория_у')
    part_number = models.CharField(max_length=300, db_index=True, verbose_name='партнамбер')
    part_number_web = models.CharField(max_length=300, db_index=True,
    verbose_name='партнамбер_веб')
    is_active = models.BooleanField(default=True, verbose_name='вкл/выкл')
    full = models.BooleanField(default=True, verbose_name='заполнен/нет')
    hotline = models.BooleanField(default=False, verbose_name='hotline')
    delivery = models.BooleanField(default=False, verbose_name='доствка')
    creditoff = models.BooleanField(default=False, verbose_name='credit')
    label = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='label')

    price_rent = models.FloatField(max_length=300, db_index=True,
    verbose_name='цена с нац')
    r_price = models.FloatField(max_length=300, db_index=True,
    verbose_name='r_price')
    rrp_price = models.FloatField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='rrp')
    auto = models.BooleanField(default=False, verbose_name='руч/п')
    price_ua = models.FloatField(max_length=300, db_index=True, verbose_name='цена грн')
    price_usd = models.FloatField(max_length=300, db_index=True,
    verbose_name='цена $')
    rentability = models.FloatField(default=5, db_index=True, verbose_name='наценка')
    provider = models.CharField(default='dc', max_length=300,
    db_index=True, verbose_name='пост')

    vendor = models.CharField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='производитель')
    gpu_main_category = models.CharField(null=True, blank=True,
    max_length=300, db_index=True,
    verbose_name='семейство процессора')
    gpu_model = models.CharField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='чип')
    gpu_ai_ua = models.TextField(null=True, blank=True,
    db_index=True, verbose_name='описание_укр')
    gpu_ai_ru = models.TextField(null=True, blank=True,
    db_index=True, verbose_name='описание_ру')
    gpu_mem_size = models.CharField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='объём памяти')
    gpu_bit = models.CharField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='разрядность')
    gpu_mem_type = models.CharField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='тип памяти')
    gpu_core_fq = models.CharField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='частота ядра')
    gpu_mem_fq = models.CharField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='частота памяти')
    gpu_pci_type = models.CharField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='интерфейс подключения')
    gpu_watt = models.CharField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='мощность бп')

    gpu_fan = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='кол вентиляторов')
    gpu_vga = models.BooleanField(default=False,
    verbose_name='разъемы_vga')
    gpu_dvi = models.BooleanField(default=False,
    verbose_name='разъемы_dvi')
    gpu_hdmi = models.BooleanField(default=False,
    verbose_name='разъемы_hdmi')
    gpu_dp = models.BooleanField(default=False,
    verbose_name='разъемы_dp')
    gpu_max_l = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='длина видеокарты')
    gpu_warr_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='гарантия_укр')
    gpu_warr_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='гарантия_ру')
    you_vid = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='you_vid')
    cover1 = models.ImageField(null=True, blank=True,
    verbose_name='фото1')
    cover2 = models.ImageField(null=True, blank=True,
    verbose_name='фото2')
    cover3 = models.ImageField(null=True, blank=True,
    verbose_name='фото3')
    groups = models.ForeignKey(
                               'self', on_delete=models.PROTECT,
                               related_name="tags",
                               related_query_name="tag",
                               null=True, blank=True, verbose_name='Связь'
                               )

    def __str__(self):
        return self.name

    def get_sum_part_number(self):
        if self.tags.exists():
            return f"{';'.join(self.tags.all().values_list('part_number', flat=True))}"

        return self.part_number

    get_sum_part_number.short_description = 'связь-партнамберов'

    def get_r_price_rrp_price(self):
        rrp = self.rrp_price if self.rrp_price else 0
        return f"{self.r_price}/ {rrp}"
    get_r_price_rrp_price.short_description = 'r_price/ rrp'

    def get_price_rent_price_ua(self):
        try:
            return round((self.price_rent / self.price_ua - 1) * 100)
        except:
            return 0
    get_price_rent_price_ua.short_description = '$'

    class Meta:
        unique_together = ('part_number', 'is_active')
        ordering = ['name']
        verbose_name = 'Видеокарта'
        verbose_name_plural = 'Видеокарты'


class FAN_OTHER(models.Model):

    name = models.CharField(max_length=300, unique=True, verbose_name='имя')
    category_ru = models.CharField(null=True, blank=True, max_length=300,
    verbose_name='категория_ру')
    category_ua = models.CharField(null=True, blank=True, max_length=300,
    verbose_name='категория_у')
    part_number = models.CharField(max_length=300, db_index=True, verbose_name='партнамбер')
    part_number_web = models.CharField(max_length=300, db_index=True,
    verbose_name='партнамбер_веб')
    is_active = models.BooleanField(default=True, verbose_name='вкл/выкл')
    full = models.BooleanField(default=True, verbose_name='заполнен/нет')
    hotline = models.BooleanField(default=False, verbose_name='hotline')
    delivery = models.BooleanField(default=False, verbose_name='доствка')
    creditoff = models.BooleanField(default=False, verbose_name='credit')
    label = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='label')

    price_rent = models.FloatField(max_length=300, db_index=True,
    verbose_name='цена с нац')
    r_price = models.FloatField(max_length=300, db_index=True,
    verbose_name='r_price')
    rrp_price = models.FloatField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='rrp')
    auto = models.BooleanField(default=False, verbose_name='руч/п')
    price_ua = models.FloatField(max_length=300, db_index=True, verbose_name='цена грн')
    price_usd = models.FloatField(max_length=300, db_index=True,
    verbose_name='цена $')
    rentability = models.FloatField(default=5, db_index=True, verbose_name='наценка')
    provider = models.CharField(default='dc', max_length=300,
    db_index=True, verbose_name='пост')

    vendor = models.CharField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='производитель')
    fan_ai_ua = models.TextField(null=True, blank=True,
    db_index=True, verbose_name='описание_укр')
    fan_ai_ru = models.TextField(null=True, blank=True,
    db_index=True, verbose_name='описание_ру')
    fan_max_spd_ua = models.CharField(null=True, blank=True,
    max_length=300, db_index=True,
    verbose_name='скорость вращения укр(max)')
    fan_max_spd_ru = models.CharField(null=True, blank=True,
    max_length=300, db_index=True,
    verbose_name='скорость вращения ру(max)')
    part_fan_size = models.CharField(null=True, blank=True,
    max_length=300, db_index=True,
    verbose_name='диаметр')

    fan_b_type_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='тип подшипника укр')
    fan_b_type_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='Тип подшипника ру')
    fan_quantity = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='кол в наборе')
    fan_pow = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='подключение')
    fan_led_type_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='подсветка укр')
    fan_led_type_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='подсветка ру')
    fan_col_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='цвет укр')
    fan_col_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='цвет ру')
    fan_warr_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='гарантия_укр')
    fan_warr_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='гарантия_ру')
    you_vid = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='you_vid')
    cover1 = models.ImageField(null=True, blank=True,
    verbose_name='фото1')
    cover2 = models.ImageField(null=True, blank=True,
    verbose_name='фото2')
    cover3 = models.ImageField(null=True, blank=True,
    verbose_name='фото3')
    groups = models.ForeignKey(
                               'self', on_delete=models.PROTECT,
                               related_name="tags",
                               related_query_name="tag",
                               null=True, blank=True, verbose_name='Связь'
                               )

    def __str__(self):
        return self.name

    def get_sum_part_number(self):
        if self.tags.exists():
            return f"{';'.join(self.tags.all().values_list('part_number', flat=True))}"

        return self.part_number

    get_sum_part_number.short_description = 'связь-партнамберов'

    def get_r_price_rrp_price(self):
        rrp = self.rrp_price if self.rrp_price else 0
        return f"{self.r_price}/ {rrp}"
    get_r_price_rrp_price.short_description = 'r_price/ rrp'

    def get_price_rent_price_ua(self):
        try:
            return round((self.price_rent / self.price_ua - 1) * 100)
        except:
            return 0
    get_price_rent_price_ua.short_description = '$'

    class Meta:
        unique_together = ('part_number', 'is_active')
        ordering = ['name']
        verbose_name = 'Вентилятор'
        verbose_name_plural = 'Вентиляторы'


class CASE_OTHER(models.Model):

    name = models.CharField(max_length=300, unique=True, verbose_name='имя')
    category_ru = models.CharField(null=True, blank=True, max_length=300,
    verbose_name='категория_ру')
    category_ua = models.CharField(null=True, blank=True, max_length=300,
    verbose_name='категория_у')
    part_number = models.CharField(max_length=300, db_index=True, verbose_name='партнамбер')
    part_number_web = models.CharField(max_length=300, db_index=True,
    verbose_name='партнамбер_веб')
    is_active = models.BooleanField(default=True, verbose_name='вкл/выкл')
    full = models.BooleanField(default=True, verbose_name='заполнен/нет')
    hotline = models.BooleanField(default=False, verbose_name='hotline')
    delivery = models.BooleanField(default=False, verbose_name='доствка')
    creditoff = models.BooleanField(default=False, verbose_name='credit')
    label = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='label')

    price_rent = models.FloatField(max_length=300, db_index=True,
    verbose_name='цена с нац')
    r_price = models.FloatField(max_length=300, db_index=True,
    verbose_name='r_price')
    rrp_price = models.FloatField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='rrp')
    auto = models.BooleanField(default=False, verbose_name='руч/п')
    price_ua = models.FloatField(max_length=300, db_index=True, verbose_name='цена грн')
    price_usd = models.FloatField(max_length=300, db_index=True,
    verbose_name='цена $')
    rentability = models.FloatField(default=5, db_index=True, verbose_name='наценка')
    provider = models.CharField(default='dc', max_length=300,
    db_index=True, verbose_name='пост')

    vendor = models.CharField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='производитель')
    case_ai_ua = models.TextField(null=True, blank=True,
    db_index=True, verbose_name='описание_укр')
    case_ai_ru = models.TextField(null=True, blank=True,db_index=True,
    verbose_name='описание_ру')
    case_color_ua = models.CharField(max_length=300, db_index=True,
    verbose_name='цвет укр', default='')
    case_color_ru = models.CharField(max_length=300, db_index=True,
    verbose_name='цвет ру', default='')

    case_s = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='тип')
    case_mb = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='форм-фактор мат. платы')
    case_psu_p = models.BooleanField(default=False,
    verbose_name='блок питания (есть/нету)')
    case_psu_w_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='отсек для БП укр')
    case_psu_w_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='отсек для БП ру')
    case_rgb = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='подсветка')
    case_fan = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='кол предустановленных вентиляторов')
    case_sp_m_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='боковое окно укр')
    case_sp_m_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='боковое окно ру')
    case_warr_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='гарантия_укр')
    case_warr_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='гарантия_ру')
    you_vid = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='you_vid')
    cover1 = models.ImageField(null=True, blank=True,
    verbose_name='фото1')
    cover2 = models.ImageField(null=True, blank=True,
    verbose_name='фото2')
    cover3 = models.ImageField(null=True, blank=True,
    verbose_name='фото3')
    groups = models.ForeignKey(
                               'self', on_delete=models.PROTECT,
                               related_name="tags",
                               related_query_name="tag",
                               null=True, blank=True, verbose_name='Связь'
                               )

    def __str__(self):
        return self.name

    def get_sum_part_number(self):
        if self.tags.exists():
            return f"{';'.join(self.tags.all().values_list('part_number', flat=True))}"

        return self.part_number

    get_sum_part_number.short_description = 'связь-партнамберов'

    def get_r_price_rrp_price(self):
        rrp = self.rrp_price if self.rrp_price else 0
        return f"{self.r_price}/ {rrp}"
    get_r_price_rrp_price.short_description = 'r_price/ rrp'

    def get_price_rent_price_ua(self):
        try:
            return round((self.price_rent / self.price_ua - 1) * 100)
        except:
            return 0
    get_price_rent_price_ua.short_description = '$'

    class Meta:
        unique_together = ('part_number', 'is_active')
        ordering = ['name']
        verbose_name = 'Корпус'
        verbose_name_plural = 'Корпуса'


class SSD_OTHER(models.Model):

    name = models.CharField(max_length=300, unique=True, verbose_name='имя')
    category_ru = models.CharField(null=True, blank=True, max_length=300,
    verbose_name='категория_ру')
    category_ua = models.CharField(null=True, blank=True, max_length=300,
    verbose_name='категория_у')
    part_number = models.CharField(max_length=300, db_index=True, verbose_name='партнамбер')
    part_number_web = models.CharField(max_length=300, db_index=True,
    verbose_name='партнамбер_веб')
    is_active = models.BooleanField(default=True, verbose_name='вкл/выкл')
    full = models.BooleanField(default=True, verbose_name='заполнен/нет')
    hotline = models.BooleanField(default=False, verbose_name='hotline')
    delivery = models.BooleanField(default=False, verbose_name='доствка')
    creditoff = models.BooleanField(default=False, verbose_name='credit')
    label = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='label')

    price_rent = models.FloatField(max_length=300, db_index=True,
    verbose_name='цена с нац')
    r_price = models.FloatField(max_length=300, db_index=True,
    verbose_name='r_price')
    rrp_price = models.FloatField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='rrp')
    auto = models.BooleanField(default=False, verbose_name='руч/п')
    price_ua = models.FloatField(max_length=300, db_index=True, verbose_name='цена грн')
    price_usd = models.FloatField(max_length=300, db_index=True,
    verbose_name='цена $')
    rentability = models.FloatField(default=5, db_index=True, verbose_name='наценка')
    provider = models.CharField(default='dc', max_length=300,
    db_index=True, verbose_name='пост')

    vendor = models.CharField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='производитель')
    ssd_ai_ua = models.TextField(null=True, blank=True,
    db_index=True, verbose_name='описание_укр')
    ssd_ai_ru = models.TextField(null=True, blank=True,
    db_index=True, verbose_name='описание_ру')
    ssd_size = models.CharField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='обьем')
    ssd_nand = models.CharField(null=True, blank=True,
    max_length=300, db_index=True,
    verbose_name='тип ячеек памяти')

    ssd_ff = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='форм-фактор')
    ssd_int = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='интерфейс')
    part_ssd_r_spd = models.CharField(null=True, blank=True,max_length=300,db_index=True,
    verbose_name='скорость чтения')
    part_ssd_w_spd = models.CharField(null=True, blank=True,max_length=300,db_index=True,
    verbose_name='скорость записи')
    ssd_warr_ua = models.CharField(null=True, blank=True,max_length=300,
    db_index=True, verbose_name='гарантия_укр')
    ssd_warr_ru = models.CharField(null=True, blank=True,max_length=300,
    db_index=True, verbose_name='гарантия_ру')
    you_vid = models.CharField(null=True, blank=True,max_length=300,
    db_index=True, verbose_name='you_vid')
    cover1 = models.ImageField(null=True, blank=True,
    verbose_name='фото1')
    cover2 = models.ImageField(null=True, blank=True,
    verbose_name='фото2')
    cover3 = models.ImageField(null=True, blank=True,
    verbose_name='фото3')
    groups = models.ForeignKey(
                               'self', on_delete=models.PROTECT,
                               related_name="tags",
                               related_query_name="tag",
                               null=True, blank=True, verbose_name='Связь'
                               )

    def __str__(self):
        return self.name

    def get_sum_part_number(self):
        if self.tags.exists():
            return f"{';'.join(self.tags.all().values_list('part_number', flat=True))}"

        return self.part_number

    get_sum_part_number.short_description = 'связь-партнамберов'

    def get_r_price_rrp_price(self):
        rrp = self.rrp_price if self.rrp_price else 0
        return f"{self.r_price}/ {rrp}"
    get_r_price_rrp_price.short_description = 'r_price/ rrp'

    def get_price_rent_price_ua(self):
        try:
            return round((self.price_rent / self.price_ua - 1) * 100)
        except:
            return 0
    get_price_rent_price_ua.short_description = '$'

    class Meta:
        unique_together = ('part_number', 'is_active')
        ordering = ['name']
        verbose_name = 'SSD'
        verbose_name_plural = 'SSD'


class WiFi_OTHER(models.Model):

    name = models.CharField(max_length=300, unique=True, verbose_name='имя')
    category_ru = models.CharField(null=True, blank=True, max_length=300,
    verbose_name='категория_ру')
    category_ua = models.CharField(null=True, blank=True, max_length=300,
    verbose_name='категория_у')
    part_number = models.CharField(max_length=300, db_index=True, verbose_name='партнамбер')
    part_number_web = models.CharField(max_length=300, db_index=True,
    verbose_name='партнамбер_веб')
    is_active = models.BooleanField(default=True, verbose_name='вкл/выкл')
    full = models.BooleanField(default=True, verbose_name='заполнен/нет')
    hotline = models.BooleanField(default=False, verbose_name='hotline')
    delivery = models.BooleanField(default=False, verbose_name='доствка')
    creditoff = models.BooleanField(default=False, verbose_name='credit')
    label = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='label')

    price_rent = models.FloatField(max_length=300, db_index=True,
    verbose_name='цена с нац')
    r_price = models.FloatField(max_length=300, db_index=True,
    verbose_name='r_price')
    rrp_price = models.FloatField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='rrp')
    auto = models.BooleanField(default=False, verbose_name='руч/п')
    price_ua = models.FloatField(max_length=300, db_index=True, verbose_name='цена грн')
    price_usd = models.FloatField(max_length=300, db_index=True,
    verbose_name='цена $')
    rentability = models.FloatField(default=5, db_index=True, verbose_name='наценка')
    provider = models.CharField(default='dc', max_length=300,
    db_index=True, verbose_name='пост')

    vendor = models.CharField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='производитель')
    net_ai_ua = models.TextField(null=True, blank=True,
    db_index=True, verbose_name='описание_укр')
    net_ai_ru = models.TextField(null=True, blank=True,
    db_index=True, verbose_name='описание_ру')
    net_type_ukr = models.CharField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='net_type_ukr')
    net_type_rus = models.CharField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='net_type_rus')
    net_max_spd = models.CharField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='net_max_spd')
    net_stand = models.CharField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='net_stand')
    net_int = models.CharField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='net_int')
    net_warr_ua = models.CharField(null=True, blank=True,max_length=300,
    db_index=True, verbose_name='гарантия_укр')
    net_warr_ru = models.CharField(null=True, blank=True,max_length=300,
    db_index=True, verbose_name='гарантия_ру')
    you_vid = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='you_vid')
    cover1 = models.ImageField(null=True, blank=True,
    verbose_name='фото1')
    cover2 = models.ImageField(null=True, blank=True,
    verbose_name='фото2')
    cover3 = models.ImageField(null=True, blank=True,
    verbose_name='фото3')
    groups = models.ForeignKey(
                               'self', on_delete=models.PROTECT,
                               related_name="tags",
                               related_query_name="tag",
                               null=True, blank=True, verbose_name='Связь'
                               )

    def __str__(self):
        return self.name

    def get_sum_part_number(self):
        if self.tags.exists():
            return f"{';'.join(self.tags.all().values_list('part_number', flat=True))}"

        return self.part_number

    get_sum_part_number.short_description = 'связь-партнамберов'

    def get_r_price_rrp_price(self):
        rrp = self.rrp_price if self.rrp_price else 0
        return f"{self.r_price}/ {rrp}"
    get_r_price_rrp_price.short_description = 'r_price/ rrp'

    def get_price_rent_price_ua(self):
        try:
            return round((self.price_rent / self.price_ua - 1) * 100)
        except:
            return 0
    get_price_rent_price_ua.short_description = '$'

    class Meta:
        unique_together = ('part_number', 'is_active')
        ordering = ['name']
        verbose_name = 'WIFI'
        verbose_name_plural = 'WIFI'

class Cables_OTHER(models.Model):

    name = models.CharField(max_length=300, unique=True, verbose_name='имя')
    category_ru = models.CharField(null=True, blank=True, max_length=300,
    verbose_name='категория_ру')
    category_ua = models.CharField(null=True, blank=True, max_length=300,
    verbose_name='категория_у')
    part_number = models.CharField(max_length=300, db_index=True, verbose_name='партнамбер')
    part_number_web = models.CharField(max_length=300, db_index=True,
    verbose_name='партнамбер_веб')
    is_active = models.BooleanField(default=True, verbose_name='вкл/выкл')
    full = models.BooleanField(default=True, verbose_name='заполнен/нет')
    hotline = models.BooleanField(default=False, verbose_name='hotline')
    delivery = models.BooleanField(default=False, verbose_name='доствка')
    creditoff = models.BooleanField(default=False, verbose_name='credit')
    label = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='label')

    price_rent = models.FloatField(max_length=300, db_index=True,
    verbose_name='цена с нац')
    r_price = models.FloatField(max_length=300, db_index=True,
    verbose_name='r_price')
    rrp_price = models.FloatField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='rrp')
    auto = models.BooleanField(default=False, verbose_name='руч/п')
    price_ua = models.FloatField(max_length=300, db_index=True, verbose_name='цена грн')
    price_usd = models.FloatField(max_length=300, db_index=True,
    verbose_name='цена $')
    rentability = models.FloatField(default=5, db_index=True, verbose_name='наценка')
    provider = models.CharField(default='dc', max_length=300,
    db_index=True, verbose_name='пост')

    vendor = models.CharField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='производитель')
    cab_ai_ua = models.TextField(null=True, blank=True,
    db_index=True, verbose_name='описание_укр')
    cab_ai_ru = models.TextField(null=True, blank=True,
    db_index=True, verbose_name='описание_ру')
    cab_mat_ukr = models.CharField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='cab_mat_ukr')
    cab_mat_ru = models.CharField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='cab_mat_ru')
    cab_col_ukr = models.CharField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='cab_col_ukr')
    cab_col_ru = models.CharField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='cab_col_ru')
    cab_set = models.CharField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='cab_set')
    cab_warr_ua = models.CharField(null=True, blank=True,max_length=300,
    db_index=True, verbose_name='гарантия_укр')
    cab_warr_ru = models.CharField(null=True, blank=True,max_length=300,
    db_index=True, verbose_name='гарантия_ру')
    you_vid = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='you_vid')
    cover1 = models.ImageField(null=True, blank=True,
    verbose_name='фото1')
    cover2 = models.ImageField(null=True, blank=True,
    verbose_name='фото2')
    cover3 = models.ImageField(null=True, blank=True,
    verbose_name='фото3')
    groups = models.ForeignKey(
                               'self', on_delete=models.PROTECT,
                               related_name="tags",
                               related_query_name="tag",
                               null=True, blank=True, verbose_name='Связь'
                               )

    def __str__(self):
        return self.name

    def get_sum_part_number(self):
        if self.tags.exists():
            return f"{';'.join(self.tags.all().values_list('part_number', flat=True))}"

        return self.part_number

    get_sum_part_number.short_description = 'связь-партнамберов'

    def get_r_price_rrp_price(self):
        rrp = self.rrp_price if self.rrp_price else 0
        return f"{self.r_price}/ {rrp}"
    get_r_price_rrp_price.short_description = 'r_price/ rrp'

    def get_price_rent_price_ua(self):
        try:
            return round((self.price_rent / self.price_ua - 1) * 100)
        except:
            return 0
    get_price_rent_price_ua.short_description = '$'

    class Meta:
        unique_together = ('part_number', 'is_active')
        ordering = ['name']
        verbose_name = 'Кабеля'
        verbose_name_plural = 'Кабеля'

class Soft_OTHER(models.Model):

    name = models.CharField(max_length=300, unique=True, verbose_name='имя')
    category_ru = models.CharField(null=True, blank=True, max_length=300,
    verbose_name='категория_ру')
    category_ua = models.CharField(null=True, blank=True, max_length=300,
    verbose_name='категория_у')
    part_number = models.CharField(max_length=300, db_index=True, verbose_name='партнамбер')
    part_number_web = models.CharField(max_length=300, db_index=True,
    verbose_name='партнамбер_веб')
    is_active = models.BooleanField(default=True, verbose_name='вкл/выкл')
    full = models.BooleanField(default=True, verbose_name='заполнен/нет')
    hotline = models.BooleanField(default=False, verbose_name='hotline')
    delivery = models.BooleanField(default=False, verbose_name='доствка')
    creditoff = models.BooleanField(default=False, verbose_name='credit')
    label = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='label')

    price_rent = models.FloatField(max_length=300, db_index=True,
    verbose_name='цена с нац')
    r_price = models.FloatField(max_length=300, db_index=True,
    verbose_name='r_price')
    rrp_price = models.FloatField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='rrp')
    auto = models.BooleanField(default=False, verbose_name='руч/п')
    price_ua = models.FloatField(max_length=300, db_index=True, verbose_name='цена грн')
    price_usd = models.FloatField(max_length=300, db_index=True,
    verbose_name='цена $')
    rentability = models.FloatField(default=5, db_index=True, verbose_name='наценка')
    provider = models.CharField(default='dc', max_length=300,
    db_index=True, verbose_name='пост')

    vendor = models.CharField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='производитель')
    soft_ai_ua = models.TextField(null=True, blank=True,
    db_index=True, verbose_name='описание_укр')
    soft_ai_ru = models.TextField(null=True, blank=True,
    db_index=True, verbose_name='описание_ру')
    soft_type_ukr = models.CharField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='soft_type_ukr')
    soft_type_ru = models.CharField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='soft_type_ru')
    soft_lang_ukr = models.CharField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='soft_lang_ukr')
    soft_lang_ru = models.CharField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='soft_lang_ru')
    soft_set = models.CharField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='soft_set')
    soft_warr_ua = models.CharField(null=True, blank=True,max_length=300,
    db_index=True, verbose_name='гарантия_укр')
    soft_warr_ru = models.CharField(null=True, blank=True,max_length=300,
    db_index=True, verbose_name='гарантия_ру')
    you_vid = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='you_vid')
    cover1 = models.ImageField(null=True, blank=True,
    verbose_name='фото1')
    cover2 = models.ImageField(null=True, blank=True,
    verbose_name='фото2')
    cover3 = models.ImageField(null=True, blank=True,
    verbose_name='фото3')
    groups = models.ForeignKey(
                               'self', on_delete=models.PROTECT,
                               related_name="tags",
                               related_query_name="tag",
                               null=True, blank=True, verbose_name='Связь'
                               )

    def __str__(self):
        return self.name

    def get_sum_part_number(self):
        if self.tags.exists():
            return f"{';'.join(self.tags.all().values_list('part_number', flat=True))}"

        return self.part_number

    get_sum_part_number.short_description = 'связь-партнамберов'

    def get_r_price_rrp_price(self):
        rrp = self.rrp_price if self.rrp_price else 0
        return f"{self.r_price}/ {rrp}"
    get_r_price_rrp_price.short_description = 'r_price/ rrp'

    def get_price_rent_price_ua(self):
        try:
            return round((self.price_rent / self.price_ua - 1) * 100)
        except:
            return 0
    get_price_rent_price_ua.short_description = '$'

    class Meta:
        unique_together = ('part_number', 'is_active')
        ordering = ['name']
        verbose_name = 'ПО'
        verbose_name_plural = 'ПО'
