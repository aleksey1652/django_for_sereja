from django.db import models
from datetime import datetime, date, time
from django.db.models import signals
#from sereja.tasks_for_models import send_mail_task
#from httplib2 import Http
#from json import dumps
from django.db.models.functions import Length
from django.db.models import CharField
#CharField.register_lookup(Length) providerprice_parts x_code

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

class Cooler_OTHER(models.Model):
    root = models.OneToOneField(
        'Cooler',
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='root_other',
    )
    r_price = models.FloatField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='r_price')
    #cool_fan_am = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    #verbose_name='cool_fan_am')
    cool_tub_am = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='кол тепловых труб')
    #cool_tub_con_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    #verbose_name='cool_tub_con_ru')
    #cool_tub_con_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    #verbose_name='cool_tub_con_ua')
    #cool_rad_mat_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    #verbose_name='cool_rad_mat_ru')
    #cool_rad_mat_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    #verbose_name='cool_rad_mat_ua')
    #cool_fix_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    #verbose_name='cool_fix_ru')
    #cool_fix_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    #verbose_name='cool_fix_ua')
    cool_sock = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='сокет')
    #cool_fan_b_t_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    #verbose_name='cool_fan_b_t_ru')
    #cool_fan_b_t_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    #verbose_name='cool_fan_b_t_ua')
    #cool_fan_min_spd_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    #verbose_name='cool_fan_min_spd_ua')
    #cool_fan_min_spd_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    #verbose_name='cool_fan_min_spd_ru')
    #cool_fan_max_spd_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    #verbose_name='скорость вращения (max)укр')
    #cool_fan_max_spd_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    #verbose_name='скорость вращения (max)ру')
    #cool_fan_max_af = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    #verbose_name='cool_fan_max_af')
    #cool_pwm = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    #verbose_name='cool_pwm')
    cool_max_tdp = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='максимальное TDP')
    #cool_conn = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    #verbose_name='cool_conn')
    cool_col_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='цвет укр')
    cool_col_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='цвет ру')
    cool_rgb = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='подсветка')
    #cool_min_no = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    #verbose_name='cool_min_no')
    cool_h = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='высота кулера')
    #cool_w = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='cool_w')
    #cool_ai_ua = models.TextField(null=True, blank=True,max_length=300, db_index=True, verbose_name='cool_ai_ua')
    #cool_ai_ru = models.TextField(null=True, blank=True,max_length=300, db_index=True, verbose_name='cool_ai_ru')
    cool_warr_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='гарантия укр')
    cool_warr_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='гарантия ру')
    you_vid = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='you_vid')
    label = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='label')
    creditoff = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='creditoff')

    is_active = models.BooleanField(default=True, verbose_name='Одиночная деталь вкл/выкл')

    def __str__(self):
        return self.root.name + '_other'

class Cooler(models.Model):
    name = models.CharField(max_length=300, unique=True, verbose_name='имя')
    part_number = models.CharField(max_length=300, db_index=True, verbose_name='партнамбер')
    vendor = models.CharField(max_length=300, db_index=True, verbose_name='производитель')
    desc_ukr = models.TextField(db_index=True, verbose_name='описание_укр')
    desc_ru = models.TextField(db_index=True, verbose_name='описание_ру')
    fan_type_ua = models.CharField(max_length=300, db_index=True, verbose_name='тип кулера укр')
    fan_type_rus = models.CharField(max_length=300, db_index=True, verbose_name='тип кулера ру')
    fan_spd_ua = models.CharField(max_length=300, db_index=True,
    verbose_name='скорость вращения (max)укр')
    fan_spd_rus = models.CharField(max_length=300, db_index=True,
    verbose_name='скорость вращения (max)ру')
    fan_noise_level = models.CharField(max_length=300, db_index=True,
    verbose_name='уровень шума')
    fan_size = models.CharField(max_length=300, db_index=True, verbose_name='диаметр')
    depend_to = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='Depend_to')
    depend_to_type = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='Depend_to_type')
    cooler_height = models.CharField(null=True,blank=True,
    max_length=30,db_index=True,verbose_name='высота кулера')
    fan_triple_wcs_rus = models.CharField(null=True, blank=True,
    verbose_name='СВО 3х куллерная(ру)',
    max_length=50, db_index=True, choices=CHOISE_RU)
    fan_triple_wcs_ua = models.CharField(null=True, blank=True,
    verbose_name='СВО 3х куллерная(укр)',
    max_length=50, db_index=True, choices=CHOISE_UA)
    more = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='More')
    parent_option = models.CharField(max_length=300, db_index=True,
    verbose_name='parent_option', default='-')
    is_active = models.BooleanField(default=True)
    config = models.BooleanField(default=True, verbose_name='конфигуратор/нет')
    price = models.FloatField(max_length=300, db_index=True, verbose_name='цена')
    special_price = models.FloatField(default=0, db_index=True, verbose_name='скидка')
    cover = models.ImageField(null=True, blank=True,
    verbose_name='фото')

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('part_number', 'is_active')
        ordering = ['name']
        verbose_name = 'Кулер'
        verbose_name_plural = 'Кулеры'

"""def post_saves_or_update_to_change_descr(sender, instance, created, **kwargs):
    from cat.models import Parts_short
    from pars.ecatalog import create_relation_from_cat_models, create_short_from_descr

    if not Parts_short.objects.filter(kind='cool', kind2=False, name_parts=instance.name).exists():
        create_short_from_descr(instance.name, 'cool', instance.price, instance.part_number)

signals.post_save.connect(receiver=post_saves_or_update_to_change_descr, sender=Cooler)"""

class CPU_OTHER(models.Model):
    root = models.OneToOneField(
        'CPU',
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='root_other',
    )
    r_price = models.FloatField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='r_price')
    #cpu_core_name = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='cpu_core_name')
    #cpu_fam = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    #verbose_name='линейка')
    cpu_soc = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='тип разъема (Socket)')
    cpu_core = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='кол ядер')
    cpu_threeds = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='кол потоков')
    cpu_tbfq = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='тактовая частота (max)')
    #cpu_nm = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='cpu_nm')
    #cpu_tdp = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='cpu_tdp')
    #cpu_gpu_model = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='cpu_gpu_model')
    #cpu_max_temp = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='cpu_max_temp')
    cpu_gpu = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='графика')
    #cpu_max_ram = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='cpu_max_ram')
    #cpu_cha = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='cpu_cha')
    #cpu_bot = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='cpu_bot')
    cpu_warr_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='гарантия укр')
    cpu_warr_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='гарантия ру')
    #cpu_ai_ua = models.TextField(null=True, blank=True,max_length=300, db_index=True, verbose_name='cpu_ai_ua')
    #cpu_ai_ru = models.TextField(null=True, blank=True,max_length=300, db_index=True, verbose_name='cpu_ai_ru')
    you_vid = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='you_vid')
    label = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='label')
    creditoff = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='creditoff')

    is_active = models.BooleanField(default=True, verbose_name='Одиночная деталь вкл/выкл')

    def __str__(self):
        return self.root.name + '_other'

class CPU(models.Model):

    CHOISERU = (
        ('Отсутствует', 'Отсутствует'),
        ('Radeon RX Vega Graphics', 'Radeon RX Vega Graphics'),
        ('Intel HD Graphics', 'Intel HD Graphics'),
    )

    CHOISEUA = (
        ('Відсутнє', 'Відсутнє'),
        ('Radeon RX Vega Graphics', 'Radeon RX Vega Graphics'),
        ('Intel HD Graphics', 'Intel HD Graphics'),
    )

    name = models.CharField(max_length=300, unique=True, verbose_name='имя')
    part_number = models.CharField(max_length=300, db_index=True, verbose_name='партнамбер')
    vendor = models.CharField(max_length=300, db_index=True, verbose_name='производитель')
    desc_ukr = models.TextField(db_index=True, verbose_name='описание_укр')
    desc_ru = models.TextField(db_index=True, verbose_name='описание_ру')
    f_name = models.CharField(max_length=300, db_index=True, verbose_name='линейка')
    cpu_c_t = models.CharField(max_length=300, db_index=True, verbose_name='ядра/потоки')
    f_cpu_c_t = models.CharField(max_length=300, db_index=True, verbose_name='F_cpu_c_t')
    cpu_b_f = models.CharField(max_length=300, db_index=True,
    verbose_name='тактовая частота')
    cpu_cache = models.CharField(max_length=300, db_index=True, verbose_name='кеш')
    cpu_i_g_ua = models.CharField(max_length=50, db_index=True,
    verbose_name='графика_укр', choices=CHOISEUA)
    cpu_i_g_rus = models.CharField(max_length=50, db_index=True,
    verbose_name='графика_ру', choices=CHOISERU)
    more = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='More')
    depend_from = models.CharField(max_length=300, db_index=True, verbose_name='Depend_from')
    depend_from_type = models.CharField(max_length=300, db_index=True,
    verbose_name='Depend_from_type')
    cpu_streem_ru = models.CharField(default='-',
    verbose_name='пригодность для стриминга',
    max_length=50, db_index=True, choices=CHOISE_plmin)
    cpu_streem_ukr = models.CharField(default='Нi',
    verbose_name='пригодность для стриминга(укр)',
    max_length=50, db_index=True, choices=CHOISE_UA)
    cpu_render_ru = models.CharField(default='-',
    verbose_name='пригодность для рендера',
    max_length=50, db_index=True, choices=CHOISE_plmin)
    cpu_render_ukr = models.CharField(default='Нi',
    verbose_name='пригодность для рендера(укр)',
    max_length=50, db_index=True, choices=CHOISE_UA)
    parent_option = models.CharField(max_length=300, db_index=True,
    verbose_name='parent_option', default='-')
    is_active = models.BooleanField(default=True)
    config = models.BooleanField(default=True, verbose_name='конфигуратор/нет')
    price = models.FloatField(max_length=300, db_index=True, verbose_name='цена')
    special_price = models.FloatField(default=0, db_index=True, verbose_name='скидка')

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('part_number', 'is_active')
        ordering = ['name']
        verbose_name = 'Процессор'
        verbose_name_plural = 'Процессоры'

class MB_OTHER(models.Model):
    root = models.OneToOneField(
        'MB',
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='root_other',
    )
    r_price = models.FloatField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='r_price')
    part_mb_sock = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='тип разъема (Socket)')
    part_mb_ff = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='форм-фактор')
    #part_mb_pow_ph = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='part_mb_pow_ph')
    #part_mb_ram_type = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='part_mb_ram_type')
    part_mb_rgb_header = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='RGB Header')
    #part_mb_ram_ch = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='part_mb_ram_ch')
    part_mb_ram_max_spd = models.CharField(null=True, blank=True,max_length=300,
    db_index=True, verbose_name='максимальная частота ОЗУ')
    part_mb_vga = models.CharField(default='+', db_index=True,
    verbose_name='видеовыход_vga', choices=CHOISE_plmin, max_length=30)
    part_mb_dvi = models.CharField(default='+', db_index=True,
    verbose_name='видеовыход_dvi', choices=CHOISE_plmin, max_length=30)
    part_mb_hdmi = models.CharField(default='+', db_index=True,
    verbose_name='видеовыход_hdmi', choices=CHOISE_plmin, max_length=30)
    part_mb_dp = models.CharField(default='+', db_index=True,
    verbose_name='видеовыход_dp', choices=CHOISE_plmin, max_length=30)
    #part_mb_sound_ch = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='part_mb_sound_ch')
    #part_mb_sound_chip = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='part_mb_sound_chip')
    part_mb_lan = models.CharField(default='+', db_index=True,
    verbose_name='разьем_lan', choices=CHOISE_plmin, max_length=30)
    part_mb_wifi = models.CharField(default='+', db_index=True,
    verbose_name='разьем_wifi', choices=CHOISE_plmin, max_length=30)
    part_mb_bt = models.CharField(default='+', db_index=True,
    verbose_name='разьем_bluetooth', choices=CHOISE_plmin, max_length=30)
    part_mb_usb_type_c = models.CharField(default='+', db_index=True,
    verbose_name='USB Type-C', choices=CHOISE_plmin, max_length=30)
    part_mb_sata = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='кол SATA')
    part_mb_m2 = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='кол M.2')
    part_mb_raid = models.CharField(default=True, db_index=True,
    verbose_name='наличие_raid', choices=CHOISE_plmin, max_length=30)
    #part_mb_sl_x1 = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='part_mb_sl_x1')
    #part_mb_sl_x16 = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='part_mb_sl_x16')
    #part_mb_main_conn = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='cool_h')
    #part_mb_cpu_conn = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='part_mb_cpu_conn')
    #part_mb_fan_conn = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='part_mb_fan_conn')
    #part_mb_ai_ua = models.TextField(null=True, blank=True,max_length=300, db_index=True, verbose_name='part_mb_ai_ua')
    #part_mb_ai_ru = models.TextField(null=True, blank=True,max_length=300, db_index=True, verbose_name='part_mb_ai_ru')
    part_mb_warr_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='гарантия_ua')
    part_mb_warr_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='гарантия_ru')
    you_vid = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='you_vid')
    label = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='label')
    creditoff = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='creditoff')

    is_active = models.BooleanField(default=True, verbose_name='Одиночная деталь вкл/выкл')

    def __str__(self):
        return self.root.name + '_other'

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

    name = models.CharField(max_length=300, unique=True, verbose_name='имя')
    part_number = models.CharField(max_length=300, db_index=True, verbose_name='партнамбер')
    vendor = models.CharField(max_length=300, db_index=True, verbose_name='производитель')
    main_category = models.CharField(max_length=300, db_index=True,
    verbose_name='для процессоров')
    desc_ukr = models.TextField(db_index=True, verbose_name='описание_укр')
    desc_ru = models.TextField(db_index=True, verbose_name='описание_ру')
    mb_chipset = models.CharField(max_length=300, db_index=True, verbose_name='чипсет')
    mb_max_ram = models.CharField(max_length=300, db_index=True,
    verbose_name='макс. объем памяти')
    mb_count_slot = models.CharField(null=True, blank=True, verbose_name='кол слотов памяти',
    max_length=50, db_index=True, choices=CHOISE)
    mb_type_memory = models.CharField(null=True, blank=True, verbose_name='тип памяти',
    max_length=50, db_index=True, choices=CHOISE1)
    more = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='More')
    depend_to = models.CharField(max_length=300, db_index=True, verbose_name='Depend_to')
    depend_to_type = models.CharField(max_length=300, db_index=True,
    verbose_name='Depend_to_type')
    depend_from = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='Depend_from')
    depend_from_type = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='Depend_from_type')
    parent_option = models.CharField(max_length=300, db_index=True,
    verbose_name='parent_option', default='-')
    is_active = models.BooleanField(default=True)
    config = models.BooleanField(default=True, verbose_name='конфигуратор/нет')
    price = models.FloatField(max_length=300, db_index=True, verbose_name='цена')
    special_price = models.FloatField(default=0, db_index=True, verbose_name='скидка')

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('part_number', 'is_active')
        ordering = ['name']
        verbose_name = 'Материнская плата'
        verbose_name_plural = 'Материнские платы'

class RAM(models.Model):

    CHOISE1 = (
        ('DDR3', 'DDR3'),
        ('DDR4', 'DDR4'),
        ('DDR5', 'DDR5'),
    )

    name = models.CharField(max_length=300, unique=True, verbose_name='имя')
    part_number = models.CharField(max_length=300, db_index=True, verbose_name='партнамбер')
    vendor = models.CharField(max_length=300, db_index=True, verbose_name='производитель')
    f_name = models.CharField(max_length=300, db_index=True, verbose_name='объём памяти')
    desc_ukr = models.TextField(db_index=True, verbose_name='описание_укр')
    desc_ru = models.TextField(db_index=True, verbose_name='описание_ру')
    mem_s = models.CharField(max_length=300, db_index=True, verbose_name='Mem_s')
    mem_spd = models.CharField(max_length=300, db_index=True, verbose_name='частота памяти')
    mem_type = models.CharField(null=True, blank=True, verbose_name='тип памяти',
    max_length=50, db_index=True, choices=CHOISE1)
    mem_l = models.CharField(max_length=300, db_index=True, verbose_name='Mem_l')
    depend_from = models.CharField(null=True, blank=True, max_length=300,
    db_index=True,verbose_name='depend_from')
    depend_from_type = models.CharField(null=True, blank=True, max_length=300,
    db_index=True, verbose_name='depend_from_type')
    depend_to = models.CharField(null=True, blank=True, max_length=300,
    db_index=True,verbose_name='depend_to')
    depend_to_type = models.CharField(null=True, blank=True, max_length=300,
    db_index=True, verbose_name='depend_to_type')
    more = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='More')
    parent_option = models.CharField(max_length=300, db_index=True,
    verbose_name='parent_option', default='-')
    is_active = models.BooleanField(default=True)
    config = models.BooleanField(default=True, verbose_name='конфигуратор/нет')
    price = models.FloatField(max_length=300, db_index=True, verbose_name='цена')
    special_price = models.FloatField(default=0, db_index=True, verbose_name='скидка')

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('part_number', 'is_active')
        ordering = ['name']
        verbose_name = 'Память'
        verbose_name_plural = 'Память'

class RAM_OTHER(models.Model):
    root = models.OneToOneField(
        'RAM',
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='root_other',
    )
    r_price = models.FloatField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='r_price')
    ram_mod_am = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='кол модулей')
    #ram_type = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='ram_type')
    #ram_cl = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='ram_cl')
    #ram_xmp = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='ram_xmp')
    #ram_pow = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='ram_pow')
    #ram_cool_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='ram_cool_ua')
    #ram_cool_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='ram_cool_ru')
    ram_col_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='цвет_укр')
    ram_col_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='цвет_ру')
    #ram_led = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='память_led')
    ram_warr_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='гарантия_укр')
    ram_warr_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='гарантия_ру')
    #ram_ai_ua = models.TextField(null=True, blank=True,db_index=True, verbose_name='ram_ai_ua')
    #ram_ai_ru = models.TextField(null=True, blank=True,db_index=True, verbose_name='ram_ai_ru')
    you_vid = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='you_vid')
    label = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='label')
    creditoff = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='creditoff')

    is_active = models.BooleanField(default=True, verbose_name='Одиночная деталь вкл/выкл')

    def __str__(self):
        return self.root.name + '_other'

class HDD(models.Model):
    name = models.CharField(max_length=300, unique=True, verbose_name='имя')
    part_number = models.CharField(max_length=300, db_index=True, verbose_name='партнамбер')
    vendor = models.CharField(max_length=300, db_index=True, verbose_name='производитель')
    f_name = models.CharField(max_length=300, db_index=True, verbose_name='объем памяти')
    desc_ukr = models.TextField(db_index=True, verbose_name='описание_укр')
    desc_ru = models.TextField(db_index=True, verbose_name='описание_ру')
    hdd_s = models.CharField(max_length=300, db_index=True, verbose_name='Hdd_s')
    hdd_spd_ua = models.CharField(max_length=300, db_index=True,
    verbose_name='скорость вращения укр')
    hdd_spd_rus = models.CharField(max_length=300, db_index=True,
    verbose_name='скорость вращения ру')
    hdd_ca = models.CharField(max_length=300, db_index=True, verbose_name='буфер обмена')
    more = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='More')
    parent_option = models.CharField(max_length=300, db_index=True,
    verbose_name='parent_option', default='-')
    is_active = models.BooleanField(default=True)
    config = models.BooleanField(default=True, verbose_name='конфигуратор/нет')
    price = models.FloatField(max_length=300, db_index=True, verbose_name='цена')
    special_price = models.FloatField(default=0, db_index=True, verbose_name='скидка')

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('part_number', 'is_active')
        ordering = ['name']
        verbose_name = 'Жесткий диск'
        verbose_name_plural = 'Жесткие диски'

class HDD_OTHER(models.Model):
    root = models.OneToOneField(
        'HDD',
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='root_other',
    )
    r_price = models.FloatField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='r_price')
    #hdd_type1_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='hdd_type1_ua')
    #hdd_type1_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='hdd_type1_ru')
    #hdd_type2_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='hdd_type2_ua')
    #hdd_type2_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='hdd_type2_ru')
    hdd_ff = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='форм-фактор')
    #hdd_int = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='hdd_int')
    hdd_warr_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='гарантия_укр')
    hdd_warr_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='гарантия_ру')
    #hdd_ai_ua = models.TextField(null=True, blank=True,db_index=True, verbose_name='hdd_ai_ua')
    #hdd_ai_ru = models.TextField(null=True, blank=True,db_index=True, verbose_name='hdd_ai_ru')
    you_vid = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='you_vid')
    label = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='label')
    creditoff = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='creditoff')

    is_active = models.BooleanField(default=True, verbose_name='Одиночная деталь вкл/выкл')

    def __str__(self):
        return self.root.name + '_other'

class PSU_OTHER(models.Model):
    root = models.OneToOneField(
        'PSU',
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='root_other',
    )
    r_price = models.FloatField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='r_price')
    psu_ff = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='форм-фактор')
    #psu_pfc = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='psu_pfc')
    #psu_no = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='psu_no')
    #psu_main_conn = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='psu_main_conn')
    #psu_gpu_conn = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='psu_gpu_conn')
    #psu_sata_conn = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='psu_sata_conn')
    #psu_molex_conn = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='psu_molex_conn')
    #psu_mod_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='psu_mod_ua')
    #psu_mod_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='psu_mod_ru')
    #psu_sl = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='psu_sl')
    psu_warr_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='гарантия_укр')
    psu_warr_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='гарантия_ру')
    #psu_ai_ua = models.TextField(null=True, blank=True,db_index=True, verbose_name='psu_ai_ua')
    #psu_ai_ru = models.TextField(null=True, blank=True,db_index=True, verbose_name='psu_ai_ru')
    you_vid = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='you_vid')
    label = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='label')
    creditoff = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='creditoff')

    is_active = models.BooleanField(default=True, verbose_name='Одиночная деталь вкл/выкл')

    def __str__(self):
        return self.root.name + '_other'

class PSU(models.Model):
    name = models.CharField(max_length=300, unique=True, verbose_name='имя')
    part_number = models.CharField(max_length=300, db_index=True, verbose_name='партнамбер')
    vendor = models.CharField(max_length=300, db_index=True, verbose_name='производитель')
    desc_ukr = models.TextField(db_index=True, verbose_name='описание_укр')
    desc_ru = models.TextField(db_index=True, verbose_name='описание_ру')
    psu_p = models.CharField(max_length=300, db_index=True, verbose_name='мощность')
    psu_c = models.CharField(max_length=300, db_index=True, verbose_name='сертификация БП')
    psu_f = models.CharField(max_length=300, db_index=True, verbose_name='вентиляторы')
    more = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='More')
    parent_option = models.CharField(max_length=300, db_index=True,
    verbose_name='parent_option', default='-')
    is_active = models.BooleanField(default=True)
    config = models.BooleanField(default=True, verbose_name='конфигуратор/нет')
    price = models.FloatField(max_length=300, db_index=True, verbose_name='цена')
    special_price = models.FloatField(default=0, db_index=True, verbose_name='скидка')

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('part_number', 'is_active')
        ordering = ['name']
        verbose_name = 'БП'
        verbose_name_plural = 'БП'

class GPU_OTHER(models.Model):
    root = models.OneToOneField(
        'GPU',
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='root_other',
    )
    r_price = models.FloatField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='r_price')
    gpu_fan = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='кол вентиляторов')
    #gpu_mem_type = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='gpu_mem_type')
    #gpu_watt = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='gpu_watt')
    #gpu_max_sc = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='gpu_max_sc')
    gpu_vga = models.CharField(default='+',max_length=300, db_index=True,
    verbose_name='разъемы_vga', choices=CHOISE_plmin)
    gpu_dvi = models.CharField(default='+',max_length=300, db_index=True,
    verbose_name='разъемы_dvi', choices=CHOISE_plmin)
    gpu_hdmi = models.CharField(default='+',max_length=300, db_index=True,
    verbose_name='разъемы_hdmi', choices=CHOISE_plmin)
    gpu_dp = models.CharField(default='+',max_length=300, db_index=True,
    verbose_name='разъемы_dp', choices=CHOISE_plmin)
    #gpu_cool_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='gpu_cool_ua')
    #gpu_cool_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='gpu_cool_ru')
    #gpu_sl = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='gpu_sl')
    gpu_max_l = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='длина видеокарты')
    #gpu_lp = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='gpu_lp')
    gpu_warr_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='гарантия_укр')
    gpu_warr_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='гарантия_ру')
    #gpu_ai_ua = models.TextField(null=True, blank=True,db_index=True, verbose_name='gpu_ai_ua')
    #gpu_ai_ru = models.TextField(null=True, blank=True,db_index=True, verbose_name='gpu_ai_ru')
    you_vid = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='you_vid')
    label = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='label')
    creditoff = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='creditoff')

    is_active = models.BooleanField(default=True, verbose_name='Одиночная деталь вкл/выкл')

    def __str__(self):
        return self.root.name + '_other'

class GPU(models.Model):

    CHOISE_type_ru = (
        ('Базовый Игровой', 'Базовый Игровой'),
        ('Продвинутый Игровой', 'Продвинутый Игровой'),
        ('Максимальный Игровой', 'Максимальный Игровой'),)

    CHOISE_type_ukr = (
        ('Базовий Ігровий', 'Базовий Ігровий'),
        ('Прогресивний Ігровий', 'Прогресивний Ігровий'),
        ('Максимальний Ігровий', 'Максимальний Ігровий'),)

    CHOISE_hd = (
        ('FullHD (1080p)', 'FullHD (1080p)'),
        ('QuadHD 2K (1440p)', 'QuadHD 2K (1440p)'),
        ('UltraHD 4K (2160p)', 'UltraHD 4K (2160p)'),)

    name = models.CharField(max_length=300, unique=True, verbose_name='имя')
    part_number = models.CharField(max_length=300, db_index=True, verbose_name='партнамбер')
    vendor = models.CharField(max_length=300, db_index=True, verbose_name='производитель')
    main_category = models.CharField(max_length=300, db_index=True,
    verbose_name='семейство процессора')
    f_name = models.CharField(max_length=300, db_index=True, verbose_name='чип')
    desc_ukr = models.TextField(db_index=True, verbose_name='описание_укр')
    desc_ru = models.TextField(db_index=True, verbose_name='описание_ру')
    gpu_fps = models.CharField(max_length=300, db_index=True, verbose_name='Gpu_fps')
    gpu_m_s = models.CharField(max_length=300, db_index=True, verbose_name='объём памяти')
    gpu_b = models.CharField(max_length=300, db_index=True, verbose_name='разрядность')
    gpu_cpu_spd = models.CharField(max_length=300, db_index=True, verbose_name='Gpu_cpu_spd')
    gpu_mem_spd = models.CharField(max_length=300, db_index=True, verbose_name='Gpu_mem_spd')
    gpu_triple_fan_rus = models.CharField(null=True, blank=True,
    verbose_name='3х куллерная карта(ру)',
    db_index=True, max_length=10, choices=CHOISE_RU)
    gpu_triple_fan_ua = models.CharField(null=True, blank=True,
    verbose_name='3х куллерная карта(укр)',
    db_index=True, max_length=10, choices=CHOISE_UA)
    more = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='More')
    depend_to = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='Depend_to')
    depend_to_type = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='Depend_to_type')

    gpu_3d_ru = models.CharField(default='-',
    verbose_name='пригодность для 3D мод',
    max_length=50, db_index=True, choices=CHOISE_plmin)
    gpu_3d_ukr = models.CharField(default='Нi',
    verbose_name='пригодность для 3D мод(укр)',
    max_length=50, db_index=True, choices=CHOISE_UA)
    gpu_VR_ru = models.CharField(default='-',
    verbose_name='пригодность для VR',
    max_length=50, db_index=True, choices=CHOISE_plmin)
    gpu_VR_ukr = models.CharField(default='Нi',
    verbose_name='пригодность для VR(укр)',
    max_length=50, db_index=True, choices=CHOISE_UA)

    gpu_type_ru = models.CharField(default='Продвинутый Игровой',
    verbose_name='игровое назначение(ру)',
    max_length=50, db_index=True, choices=CHOISE_type_ru)
    gpu_type_ukr = models.CharField(default='Прогресивний Ігровий',
    verbose_name='игровое назначение(укр)',
    max_length=50, db_index=True, choices=CHOISE_type_ukr)
    gpu_ref_hd = models.CharField(default='FullHD (1080p)', max_length=300, db_index=True,
    verbose_name='рекомендуемое разрешение', choices=CHOISE_hd)

    parent_option = models.CharField(max_length=300, db_index=True,
    verbose_name='parent_option', default='-')
    is_active = models.BooleanField(default=True)
    config = models.BooleanField(default=True, verbose_name='конфигуратор/нет')
    price = models.FloatField(max_length=300, db_index=True, verbose_name='цена')
    special_price = models.FloatField(default=0, db_index=True, verbose_name='скидка')

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('part_number', 'is_active')
        ordering = ['name']
        verbose_name = 'Видеокарта'
        verbose_name_plural = 'Видеокарты'

class FAN_OTHER(models.Model):
    root = models.OneToOneField(
        'FAN',
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='root_other',
    )
    r_price = models.FloatField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='r_price')
    fan_b_type_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='тип подшипника укр')
    fan_b_type_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='Тип подшипника ру')
    fan_quantity = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='кол в наборе')
    #fan_pwm = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='fan_pwm')
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
    #fan_min_spd_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='fan_min_spd_ua')
    #fan_min_spd_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='fan_min_spd_ru')
    #fan_max_spd_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='fan_max_spd_ua')
    #fan_max_spd_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='fan_max_spd_ru')
    fan_warr_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='гарантия_укр')
    fan_warr_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='гарантия_ру')
    #fan_ai_ua = models.TextField(null=True, blank=True,db_index=True, verbose_name='fan_ai_ua')
    #fan_ai_ru = models.TextField(null=True, blank=True,db_index=True, verbose_name='fan_ai_ru')
    you_vid = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='you_vid')
    label = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='label')
    creditoff = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='creditoff')

    is_active = models.BooleanField(default=True, verbose_name='Одиночная деталь вкл/выкл')

    def __str__(self):
        return self.root.name + '_other'

class FAN(models.Model):
    name = models.CharField(max_length=300, unique=True, verbose_name='имя')
    part_number = models.CharField(max_length=300, db_index=True, verbose_name='партнамбер')
    vendor = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='производитель')
    desc_ukr = models.TextField(db_index=True, verbose_name='описание_укр')
    desc_ru = models.TextField(db_index=True, verbose_name='описание_ру')
    case_fan_spd_ua = models.CharField(max_length=300, db_index=True,
    verbose_name='скорость вращения укр(max)')
    case_fan_spd_rus = models.CharField(max_length=300, db_index=True,
    verbose_name='скорость вращения ру(max)')
    case_fan_noise_level = models.CharField(max_length=300, db_index=True,
    verbose_name='уровень шума')
    case_fan_size = models.CharField(max_length=300, db_index=True,
    verbose_name='диаметр')
    more = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='More')
    parent_option = models.CharField(max_length=300, db_index=True,
    verbose_name='parent_option', default='-')
    is_active = models.BooleanField(default=True)
    config = models.BooleanField(default=True, verbose_name='конфигуратор/нет')
    price = models.FloatField(max_length=300, db_index=True, verbose_name='цена')
    special_price = models.FloatField(default=0, db_index=True, verbose_name='скидка')

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('part_number', 'is_active')
        ordering = ['name']
        verbose_name = 'Вентилятор'
        verbose_name_plural = 'Вентиляторы'

class CASE_OTHER(models.Model):
    root = models.OneToOneField(
        'CASE',
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='root_other',
    )
    r_price = models.FloatField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='r_price')
    case_mb = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='форм-фактор мат. платы')
    case_psu_p = models.CharField(default='+', db_index=True, max_length=30,
    verbose_name='блок питания (есть/нету)', choices=CHOISE_plmin)
    case_psu_w_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='отсек для БП укр')
    case_psu_w_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='отсек для БП ру')
    case_rgb = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='подсветка')
    #case_5_с = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='case_5_с')
    #case_3_с = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='case_3_с')
    #case_2_с = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='case_2_с')
    #case_e_с = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='case_e_с')
    case_fan = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='кол предустановленных вентиляторов')
    #case_fan_t = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='case_fan_t')
    #case_fan_b = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='case_fan_b')
    #case_pan_f = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='case_pan_f')
    #case_pan_t = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='case_pan_t')
    #case_pan_b = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='case_pan_b')
    #case_front_usb = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='case_front_usb')
    #case_front_h = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='case_front_h')
    #case_front_m = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='case_front_m')
    #case_front_l = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='case_front_l')
    #case_size = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='case_size')
    #case_weight = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='case_weight')
    #case_fp_m_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='case_fp_m_ua')
    #case_fp_m_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='case_fp_m_ru')
    case_sp_m_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='боковое окно укр')
    case_sp_m_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='боковое окно ру')
    #case_sh_m_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='case_sh_m_ua')
    #case_sh_m_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='case_sh_m_ru')
    #case_os_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='case_os_ua')
    #case_os_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='case_os_ru')
    #case_color_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    #verbose_name='цвет укр')
    #case_color_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    #verbose_name='цвет ру')
    #case_max_cpu = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='case_max_cpu')
    #case_max_gpu = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='case_max_gpu')
    #case_cm = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='case_cm')
    #case_df = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='case_df')
    #case_ai_ua = models.TextField(null=True, blank=True,max_length=300, db_index=True, verbose_name='case_ai_ua')
    #case_ai_ru = models.TextField(null=True, blank=True,max_length=300, db_index=True, verbose_name='case_ai_ru')
    case_warr_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='гарантия_укр')
    case_warr_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='гарантия_ру')
    you_vid = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='you_vid')
    label = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='label')
    creditoff = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='creditoff')

    is_active = models.BooleanField(default=True, verbose_name='Одиночная деталь вкл/выкл')

    def __str__(self):
        return self.root.name + '_other'

class CASE(models.Model):

    CHOISE = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('4+', '4+'),
    )

    name = models.CharField(max_length=300, unique=True, verbose_name='имя')
    part_number = models.CharField(max_length=300, db_index=True, verbose_name='партнамбер')
    vendor = models.CharField(max_length=300, db_index=True, verbose_name='производитель')
    desc_ukr = models.TextField(db_index=True, verbose_name='описание_укр_ukr')
    desc_ru = models.TextField(db_index=True, verbose_name='описание_ру')
    case_s = models.CharField(max_length=300, db_index=True, verbose_name='тип')
    more = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='More')
    color_parent = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='Color_parent', default='')
    color = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='Color', default='')
    color_ukr = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='цвет укр', default='')
    color_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='цвет ру', default='')
    case_wcs_plus_size_ru = models.CharField(null=True, blank=True,
    verbose_name='360мм СВО(ру)',
    db_index=True, choices=CHOISE_RU,max_length=50)
    case_wcs_plus_size_ua = models.CharField(null=True, blank=True,
    verbose_name='360мм СВО(укр)',
    db_index=True, choices=CHOISE_UA,max_length=50)
    case_gpu_triple_fan_ru = models.CharField(null=True, blank=True,
    verbose_name='3х куллерная карта(ру)',
    db_index=True, choices=CHOISE_RU,max_length=50)
    case_gpu_triple_fan_ua = models.CharField(null=True, blank=True,
    verbose_name='3х куллерная карта(укр)',
    db_index=True, choices=CHOISE_UA,max_length=50)
    case_count_fan = models.CharField(null=True, blank=True,max_length=50, db_index=True,
    verbose_name='Кол вентиляторов', choices=CHOISE)
    depend_to = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='Depend_to', default='')
    depend_to_type = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='Depend_to_type', default='')
    case_height = models.CharField(null=True, blank=True, max_length=30, db_index=True,
    verbose_name='case_height')
    parent_option = models.CharField(max_length=300, db_index=True,
    verbose_name='parent_option', default='-')
    is_active = models.BooleanField(default=True)
    config = models.BooleanField(default=True, verbose_name='конфигуратор/нет')
    price = models.FloatField(max_length=300, db_index=True, verbose_name='цена')
    special_price = models.FloatField(default=0, db_index=True, verbose_name='скидка')

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('part_number', 'is_active')
        ordering = ['name']
        verbose_name = 'Корпус'
        verbose_name_plural = 'Корпуса'

class SSD_OTHER(models.Model):
    root = models.OneToOneField(
        'SSD',
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='root_other',
    )
    r_price = models.FloatField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='r_price')
    #ssd_type1_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='ssd_type1_ua')
    #ssd_type1_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='ssd_type1_ru')
    #ssd_type2_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='ssd_type2_ua')
    #ssd_type2_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='ssd_type2_ru')
    ssd_ff = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='форм-фактор')
    ssd_int = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='интерфейс')
    ssd_warr_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='гарантия_укр')
    ssd_warr_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='гарантия_ру')
    #ssd_ai_ua = models.TextField(null=True, blank=True,db_index=True, verbose_name='ssd_ai_ua')
    #ssd_ai_ru = models.TextField(null=True, blank=True,db_index=True, verbose_name='ssd_ai_ru')
    part_ssd_r_spd = models.CharField(null=True, blank=True,max_length=300,db_index=True,
    verbose_name='скорость чтения')
    part_ssd_w_spd = models.CharField(null=True, blank=True,max_length=300,db_index=True,
    verbose_name='скорость записи')
    #ssd_con_type = models.CharField(null=True, blank=True,max_length=300,db_index=True, verbose_name='ssd_con_type')
    you_vid = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='you_vid')
    label = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='label')
    creditoff = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='creditoff')

    is_active = models.BooleanField(default=True, verbose_name='Одиночная деталь вкл/выкл')

    def __str__(self):
        return self.root.name + '_other'

class SSD(models.Model):
    name = models.CharField(max_length=300, unique=True, verbose_name='имя')
    part_number = models.CharField(max_length=300, db_index=True, verbose_name='партнамбер')
    vendor = models.CharField(max_length=300, db_index=True, verbose_name='производитель')
    f_name = models.CharField(max_length=300, db_index=True, verbose_name='объем памяти')
    desc_ukr = models.TextField(db_index=True, verbose_name='описание_укр')
    desc_ru = models.TextField(db_index=True, verbose_name='описание_ру')
    ssd_s = models.CharField(max_length=300, db_index=True, verbose_name='Ssd_s')
    ssd_spd = models.CharField(max_length=300, db_index=True, verbose_name='Ssd_spd')
    ssd_r_spd = models.CharField(max_length=300, db_index=True, verbose_name='Ssd_r_spd')
    ssd_type_cells = models.CharField(max_length=300, db_index=True,
    verbose_name='тип ячеек памяти')
    more = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='More')
    parent_option = models.CharField(max_length=300, db_index=True,
    verbose_name='parent_option', default='-')
    is_active = models.BooleanField(default=True)
    config = models.BooleanField(default=True, verbose_name='конфигуратор/нет')
    price = models.FloatField(max_length=300, db_index=True, verbose_name='Price')
    special_price = models.FloatField(default=0, db_index=True, verbose_name='скидка')

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('part_number', 'is_active')
        ordering = ['name']
        verbose_name = 'SSD'
        verbose_name_plural = 'SSD'

class WiFi(models.Model):
    name = models.CharField(max_length=300, unique=True, verbose_name='Name_wifi')
    part_number = models.CharField(max_length=300, db_index=True, verbose_name='Part_number')
    vendor = models.CharField(max_length=300, db_index=True, verbose_name='Vendor')
    r_price = models.FloatField(max_length=300, db_index=True, verbose_name='r_price')
    price = models.CharField(max_length=300, db_index=True, verbose_name='Price')
    special_price = models.FloatField(default=0, db_index=True, verbose_name='скидка')
    desc_ukr = models.TextField(db_index=True, verbose_name='Desc_ukr')
    desc_ru = models.TextField(db_index=True, verbose_name='Desc_ru')
    net_type_ukr = models.CharField(max_length=300, db_index=True, verbose_name='net_type_ukr')
    net_type_rus = models.CharField(max_length=300, db_index=True, verbose_name='net_type_rus')
    net_max_spd = models.CharField(max_length=300, db_index=True, verbose_name='net_max_spd')
    net_stand = models.CharField(max_length=300, db_index=True, verbose_name='net_stand')
    net_int = models.CharField(max_length=300, db_index=True, verbose_name='net_int')
    more = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='More')
    parent_option = models.CharField(max_length=300, db_index=True,
    verbose_name='parent_option', default='-')
    is_active = models.BooleanField(default=True)
    config = models.BooleanField(default=True, verbose_name='конфигуратор/нет')

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('part_number', 'is_active')
        ordering = ['name']
        verbose_name = 'WIFI'
        verbose_name_plural = 'WIFI'

class Cables(models.Model):
    name = models.CharField(max_length=300, unique=True, verbose_name='Name_cables')
    part_number = models.CharField(max_length=300, db_index=True, verbose_name='Part_number')
    vendor = models.CharField(max_length=300, db_index=True, verbose_name='Vendor')
    r_price = models.FloatField(max_length=300, db_index=True, verbose_name='r_price')
    special_price = models.FloatField(default=0, db_index=True, verbose_name='скидка')
    desc_ukr = models.TextField(db_index=True, verbose_name='Desc_ukr')
    desc_ru = models.TextField(db_index=True, verbose_name='Desc_ru')
    cab_mat_ukr = models.CharField(max_length=300, db_index=True, verbose_name='cab_mat_ukr')
    cab_mat_ru = models.CharField(max_length=300, db_index=True, verbose_name='cab_mat_ru')
    cab_col_ukr = models.CharField(max_length=300, db_index=True, verbose_name='cab_col_ukr')
    cab_col_ru = models.CharField(max_length=300, db_index=True, verbose_name='cab_col_ru')
    cab_set = models.CharField(max_length=300, db_index=True, verbose_name='cab_set')
    more = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='More')
    parent_option = models.CharField(max_length=300, db_index=True,
    verbose_name='parent_option', default='-')
    is_active = models.BooleanField(default=True)
    config = models.BooleanField(default=True, verbose_name='конфигуратор/нет')

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('part_number', 'is_active')
        ordering = ['name']
        verbose_name = 'Кабеля'
        verbose_name_plural = 'Кабеля'

class Soft(models.Model):
    name = models.CharField(max_length=300, unique=True, verbose_name='Name_soft')
    part_number = models.CharField(max_length=300, db_index=True, verbose_name='Part_number')
    vendor = models.CharField(max_length=300, db_index=True, verbose_name='Vendor')
    r_price = models.FloatField(max_length=300, db_index=True, verbose_name='r_price')
    special_price = models.FloatField(default=0, db_index=True, verbose_name='скидка')
    price = models.CharField(max_length=300, db_index=True, verbose_name='Price')
    desc_ukr = models.TextField(db_index=True, verbose_name='Desc_ukr')
    desc_ru = models.TextField(db_index=True, verbose_name='Desc_ru')
    soft_type_ukr = models.CharField(max_length=300, db_index=True, verbose_name='soft_type_ukr')
    soft_type_ru = models.CharField(max_length=300, db_index=True, verbose_name='soft_type_ru')
    soft_lang_ukr = models.CharField(max_length=300, db_index=True, verbose_name='soft_lang_ukr')
    soft_lang_ru = models.CharField(max_length=300, db_index=True, verbose_name='soft_lang_ru')
    soft_set = models.CharField(max_length=300, db_index=True, verbose_name='soft_set')
    more = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='More')
    parent_option = models.CharField(max_length=300, db_index=True,
    verbose_name='parent_option', default='-')
    is_active = models.BooleanField(default=True)
    config = models.BooleanField(default=True, verbose_name='конфигуратор/нет')

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('part_number', 'is_active')
        ordering = ['name']
        verbose_name = 'ПО'
        verbose_name_plural = 'ПО'
