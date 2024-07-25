from django.db import models
from datetime import datetime, date, time
#from django.db.models import signals
from django.core.exceptions import ValidationError
from django.http import HttpResponse
#from sereja.tasks_for_models import send_mail_task
#from django.db.models.functions import Length
#from django.db.models import CharField
#CharField.register_lookup(Length)
import re


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


class Monitors(models.Model):

    name = models.CharField(max_length=300, unique=True, verbose_name="Iм'я")
    category_ru = models.CharField(null=True, blank=True, max_length=300,
    verbose_name='категорiя_ру')
    category_ua = models.CharField(null=True, blank=True, max_length=300,
    verbose_name='категорiя_у')
    part_number = models.CharField(max_length=300, db_index=True,
    verbose_name='партнамбер')
    part_number_web = models.CharField(max_length=300, db_index=True,
    verbose_name='партнамбер_веб', default='-')
    is_active = models.BooleanField(default=True, verbose_name='вкл/викл')
    full = models.BooleanField(default=True, verbose_name='заповн/нi')
    hotline = models.BooleanField(default=False, verbose_name='hotline')
    delivery = models.BooleanField(default=False, verbose_name='доствка')
    creditoff = models.BooleanField(default=False, verbose_name='credit')
    label = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='label')

    price_rent = models.FloatField(max_length=300, db_index=True,
    verbose_name='цiна з нац')
    r_price = models.FloatField(max_length=300, db_index=True,
    verbose_name='r_price')
    rrp_price = models.FloatField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='rrp')
    auto = models.BooleanField(default=False, verbose_name='руч/п')
    price_ua = models.FloatField(max_length=300, db_index=True, verbose_name='цена грн')
    price_usd = models.FloatField(max_length=300, db_index=True,
    verbose_name='цiна $')
    rentability = models.FloatField(default=5, db_index=True, verbose_name='нацiнка')
    provider = models.CharField(default='dc', max_length=300,
    db_index=True, verbose_name='пост')

    vendor = models.CharField(null=True, blank=True,max_length=300,
    db_index=True, verbose_name='vendor')
    sc_d = models.CharField(null=True, blank=True, max_length=300,
    db_index=True, verbose_name='Діагональ екрану')
    sc_r = models.CharField(null=True, blank=True, max_length=300,
    db_index=True, verbose_name='Роздільна здатність екрану')
    sc_t = models.CharField(null=True, blank=True,
    max_length=300, db_index=True,
    verbose_name='Тип матриці')
    sc_ss = models.CharField(null=True, blank=True,
    max_length=300, db_index=True,
    verbose_name='Співвідношення сторін')
    sc_l = models.CharField(null=True, blank=True,
    max_length=300, db_index=True,
    verbose_name='Час реакції')
    sc_v = models.CharField(null=True, blank=True,
    max_length=300, db_index=True,
    verbose_name='Кут огляду')
    sc_b = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='Яскравість')
    sc_s = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='Контрастність')
    sc_h = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='Частота оновлення')
    sc_surf_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='Поверхня екрану_укр')
    sc_surf_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='Поверхня екрану_ру')
    sc_d_sub = models.PositiveIntegerField(default=0, db_index=True,
    verbose_name='D-Sub')
    sc_dvi = models.PositiveIntegerField(default=0, db_index=True,
    verbose_name='DVI')
    sc_hdmi = models.PositiveIntegerField(default=0, db_index=True,
    verbose_name='HDMI')
    sc_dp = models.PositiveIntegerField(default=0, db_index=True,
    verbose_name='DisplayPort')
    sc_arch = models.BooleanField(default=False, db_index=True,
    verbose_name='Вигнутий екран')
    sc_spk = models.BooleanField(default=False, db_index=True,
    verbose_name='Вбудована аудіосистема')
    sc_spk_p = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='Потужність аудіосистеми')
    sc_spin = models.BooleanField(default=False, db_index=True,
    verbose_name='Поворотний екран (Pivot)')
    sc_hight = models.BooleanField(default=False, db_index=True,
    verbose_name='Регулювання по висоті')
    sc_usb = models.BooleanField(default=False, db_index=True,
    verbose_name='Концентратор USB')
    sc_o = models.BooleanField(default=False, db_index=True,
    verbose_name='Ігрові технології')
    sc_os = models.CharField(null=True, blank=True,max_length=300,
    db_index=True, verbose_name='Ігрові_технології')
    sc_fi = models.BooleanField(default=False, db_index=True,
    verbose_name='Безрамковий монітор')
    sc_vesa = models.CharField(null=True, blank=True, max_length=300, db_index=True,
    verbose_name='Кріплення на стіну')
    sc_vol = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='Габарити (ШхВхГ)')
    sc_weight = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='Вага')
    sc_col_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='колор_укр')
    sc_col_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='колор_ру')
    sc_ai_ua = models.TextField(null=True, blank=True,
    db_index=True, verbose_name='опис_укр')
    sc_ai_ru = models.TextField(null=True, blank=True,
    db_index=True, verbose_name='опис_ру')
    sc_warr_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='гарантiя укр')
    sc_warr_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='гарантiя ру')
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
    get_price_rent_price_ua.short_description = '%'

    def warranty(self):
        return re.sub('\D+', '', self.sc_warr_ru)
    warranty.short_description = 'waranty'

    class Meta:
        unique_together = ('part_number', 'is_active')
        ordering = ['name']
        verbose_name = 'Монiтор'
        verbose_name_plural = '0 Монiтори'


class KM(models.Model):

    name = models.CharField(max_length=300, unique=True, verbose_name="Iм'я")
    category_ru = models.CharField(null=True, blank=True, max_length=300,
    verbose_name='категорiя_ру')
    category_ua = models.CharField(null=True, blank=True, max_length=300,
    verbose_name='категорiя_укр')
    part_number = models.CharField(max_length=300, db_index=True,
    verbose_name='партнамбер')
    part_number_web = models.CharField(max_length=300, db_index=True,
    verbose_name='партнамбер_веб', default='-')
    is_active = models.BooleanField(default=True, verbose_name='вкл/викл')
    full = models.BooleanField(default=True, verbose_name='заповн/нi')
    hotline = models.BooleanField(default=False, verbose_name='hotline')
    delivery = models.BooleanField(default=False, verbose_name='доствка')
    creditoff = models.BooleanField(default=False, verbose_name='credit')
    label = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='label')

    price_rent = models.FloatField(max_length=300, db_index=True,
    verbose_name='цiна з нац')
    r_price = models.FloatField(max_length=300, db_index=True,
    verbose_name='r_price')
    rrp_price = models.FloatField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='rrp')
    auto = models.BooleanField(default=False, verbose_name='руч/п')
    price_ua = models.FloatField(max_length=300, db_index=True, verbose_name='цена грн')
    price_usd = models.FloatField(max_length=300, db_index=True,
    verbose_name='цiна $')
    rentability = models.FloatField(default=5, db_index=True, verbose_name='нацiнка')
    provider = models.CharField(default='dc', max_length=300,
    db_index=True, verbose_name='пост')

    vendor = models.CharField(null=True, blank=True,max_length=300,
    db_index=True, verbose_name='vendor')
    km_connect_ua = models.CharField(null=True, blank=True, max_length=300,
    db_index=True, verbose_name='Підключення_укр')
    km_connect_ru = models.CharField(null=True, blank=True, max_length=300,
    db_index=True, verbose_name='Підключення_ру')
    km_int = models.CharField(null=True, blank=True, max_length=300,
    db_index=True, verbose_name='Інтерфейс')
    km_key_type_ua = models.CharField(null=True, blank=True,
    max_length=300, db_index=True,
    verbose_name='Тип клавіш (клавіатура) укр')
    km_key_type_ru = models.CharField(null=True, blank=True,
    max_length=300, db_index=True,
    verbose_name='Тип клавіш (клавіатура) ру')
    km_k_light = models.BooleanField(default=False, db_index=True,
    verbose_name='Підсвічування (клавіатура)')
    km_ua = models.BooleanField(default=False, db_index=True,
    verbose_name='Українська розкладка')
    km_pow_k_ua = models.CharField(null=True, blank=True, max_length=300,
    db_index=True, verbose_name='Живлення (клавіатура) укр')
    km_pow_k_ru = models.CharField(null=True, blank=True, max_length=300,
    db_index=True, verbose_name='Живлення (клавіатура) ру')
    km_sensor_ua = models.CharField(null=True, blank=True, max_length=300,
    db_index=True, verbose_name='Тип сенсора (миша) укр')
    km_sensor_ru = models.CharField(null=True, blank=True, max_length=300,
    db_index=True, verbose_name='Тип сенсора (миша) ру')
    km_numb_buttoms = models.PositiveIntegerField(default=0, db_index=True,
    verbose_name='Кількість кнопок (миша)')
    km_dpi = models.CharField(null=True, blank=True, max_length=300,
    db_index=True, verbose_name='Роздільна здатність (миша)')
    km_mouse_light = models.BooleanField(default=False, db_index=True,
    verbose_name='Підсвічування (миша)')
    km_pow_mouse_ua = models.CharField(null=True, blank=True, max_length=300,
    db_index=True, verbose_name='Живлення (миша) укр')
    km_pow_mouse_ru = models.CharField(null=True, blank=True, max_length=300,
    db_index=True, verbose_name='Живлення (миша) ру')
    km_k_vol = models.CharField(null=True, blank=True, max_length=300,
    db_index=True, verbose_name='Габарити (клавіатура)')
    km_mouse_vol = models.CharField(null=True, blank=True, max_length=300, db_index=True,
    verbose_name='Габарити (миша)')
    km_k_weight = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='Вага (клавіатура)')
    km_mouse_weight = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='Вага (миша)')
    km_col_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='колор_укр')
    km_col_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='колор_ру')
    km_warr_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='гарантия укр')
    km_warr_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True,
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
    get_price_rent_price_ua.short_description = '%'

    def warranty(self):
        return re.sub('\D+', '', self.km_warr_ru)
    warranty.short_description = 'waranty'

    class Meta:
        unique_together = ('part_number', 'is_active')
        ordering = ['name']
        verbose_name = 'Комплект_клавіатура_мишка'
        verbose_name_plural = '4 Комплекти_к_м'


class Keyboards(models.Model):

    name = models.CharField(max_length=300, unique=True, verbose_name="Iм'я")
    category_ru = models.CharField(null=True, blank=True, max_length=300,
    verbose_name='категорiя_ру')
    category_ua = models.CharField(null=True, blank=True, max_length=300,
    verbose_name='категорiя_укр')
    part_number = models.CharField(max_length=300, db_index=True,
    verbose_name='партнамбер')
    part_number_web = models.CharField(max_length=300, db_index=True,
    verbose_name='партнамбер_веб', default='-')
    is_active = models.BooleanField(default=True, verbose_name='вкл/викл')
    full = models.BooleanField(default=True, verbose_name='заповн/нi')
    hotline = models.BooleanField(default=False, verbose_name='hotline')
    delivery = models.BooleanField(default=False, verbose_name='доствка')
    creditoff = models.BooleanField(default=False, verbose_name='credit')
    label = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='label')

    price_rent = models.FloatField(max_length=300, db_index=True,
    verbose_name='цiна з нац')
    r_price = models.FloatField(max_length=300, db_index=True,
    verbose_name='r_price')
    rrp_price = models.FloatField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='rrp')
    auto = models.BooleanField(default=False, verbose_name='руч/пост')
    price_ua = models.FloatField(max_length=300, db_index=True, verbose_name='цiна грн')
    price_usd = models.FloatField(max_length=300, db_index=True,
    verbose_name='цiна $')
    rentability = models.FloatField(default=5, db_index=True, verbose_name='нацiнка')
    provider = models.CharField(default='dc', max_length=300,
    db_index=True, verbose_name='пост')

    kb_type_con_ua = models.CharField(null=True, blank=True,max_length=300,
    db_index=True, verbose_name='Тип підключення укр')
    kb_type_con_ru = models.CharField(null=True, blank=True,max_length=300,
    db_index=True, verbose_name='Тип підключення ру')
    kb_type_but_ua = models.CharField(null=True, blank=True,max_length=300,
    db_index=True, verbose_name='Тип клавіш укр')
    kb_type_but_ru = models.CharField(null=True, blank=True,max_length=300,
    db_index=True, verbose_name='Тип клавіш ру')
    kb_type_pow_ua = models.CharField(null=True, blank=True,max_length=300,
    db_index=True, verbose_name='Джерело живлення укр')
    kb_type_pow_ru = models.CharField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='Джерело живлення ру')
    kb_form_ua = models.CharField(null=True, blank=True,
    max_length=300, verbose_name='Форм-фактор укр')
    kb_form_ru = models.CharField(null=True, blank=True,
    max_length=300, verbose_name='Форм-фактор ру')
    kb_type_conn = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='Тип перемикачів')

    vendor = models.CharField(null=True, blank=True,max_length=300,
    db_index=True, verbose_name='vendor')
    kb_plus_but = models.PositiveIntegerField(default=0, db_index=True,
    verbose_name='Додаткові клавіші')
    kb_light = models.BooleanField(default=False,
    db_index=True, verbose_name='Підсвічування клавіш')
    kb_rgb = models.BooleanField(default=False,
    db_index=True, verbose_name='Наявність RGB')
    kb_res = models.BooleanField(default=False,
    db_index=True, verbose_name='Вологостійкість')
    kb_cab_long = models.CharField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='Довжина кабеля')
    kb_leng = models.CharField(null=True, blank=True,
    max_length=300, verbose_name='Розкладка')
    kb_vol = models.CharField(null=True, blank=True,
    max_length=300, verbose_name='Габарити')
    kb_weight = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='Вага')

    kb_usb = models.BooleanField(default=False, db_index=True,
    verbose_name='USB')
    kb_ps = models.BooleanField(default=False, db_index=True,
    verbose_name='PS/2')
    kb_bt = models.BooleanField(default=False, db_index=True,
    verbose_name='Bluetooth')
    kb_usb_resiver = models.BooleanField(default=False, db_index=True,
    verbose_name='USB-ресивер')
    kb_usb_type_c = models.BooleanField(default=False, db_index=True,
    verbose_name='USB Type-C')

    kb_col_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='колор_укр')
    kb_col_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='колор_ру')
    kb_warr_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='гарантия укр')
    kb_warr_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True,
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
    get_price_rent_price_ua.short_description = '%'

    def warranty(self):
        return re.sub('\D+', '', self.kb_warr_ru)
    warranty.short_description = 'waranty'

    class Meta:
        unique_together = ('part_number', 'is_active')
        ordering = ['name']
        verbose_name = 'Клавіатура'
        verbose_name_plural = '3 Клавіатури'


class Mouses(models.Model):

    name = models.CharField(max_length=300, unique=True, verbose_name="Iм'я")
    category_ru = models.CharField(null=True, blank=True, max_length=300,
    verbose_name='категорiя_ру')
    category_ua = models.CharField(null=True, blank=True, max_length=300,
    verbose_name='категорiя_укр')
    part_number = models.CharField(max_length=300, db_index=True,
    verbose_name='партнамбер')
    part_number_web = models.CharField(max_length=300, db_index=True,
    verbose_name='партнамбер_веб', default='-')
    is_active = models.BooleanField(default=True, verbose_name='вкл/викл')
    full = models.BooleanField(default=True, verbose_name='заповн/нi')
    hotline = models.BooleanField(default=False, verbose_name='hotline')
    delivery = models.BooleanField(default=False, verbose_name='доствка')
    creditoff = models.BooleanField(default=False, verbose_name='credit')
    label = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='label')

    price_rent = models.FloatField(max_length=300, db_index=True,
    verbose_name='цiна з нац')
    r_price = models.FloatField(max_length=300, db_index=True,
    verbose_name='r_price')
    rrp_price = models.FloatField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='rrp')
    auto = models.BooleanField(default=False, verbose_name='руч/п')
    price_ua = models.FloatField(max_length=300, db_index=True, verbose_name='цена грн')
    price_usd = models.FloatField(max_length=300, db_index=True,
    verbose_name='цiна $')
    rentability = models.FloatField(default=5, db_index=True, verbose_name='нацiнка')
    provider = models.CharField(default='dc', max_length=300,
    db_index=True, verbose_name='пост')

    vendor = models.CharField(null=True, blank=True,max_length=300,
    db_index=True, verbose_name='vendor')
    mouse_type_connect_ua = models.CharField(null=True, blank=True, max_length=300,
    db_index=True, verbose_name="Тип з'єднання укр")
    mouse_type_connect_ru = models.CharField(null=True, blank=True, max_length=300,
    db_index=True, verbose_name="Тип з'єднання ру")
    mouse_int = models.CharField(null=True, blank=True, max_length=300,
    db_index=True, verbose_name="Інтерфейс з'єднання")
    mouse_sensor_ua = models.CharField(null=True, blank=True, max_length=300,
    db_index=True, verbose_name="Тип сенсора укр")
    mouse_sensor_ru = models.CharField(null=True, blank=True, max_length=300,
    db_index=True, verbose_name="Тип сенсора ру")
    mouse_dpi = models.CharField(null=True, blank=True, max_length=300,
    db_index=True, verbose_name='Роздільна здатність')
    mouse_numb_buttoms = models.PositiveIntegerField(default=0, db_index=True,
    verbose_name='Кількість кнопок')
    mouse_pow_ua = models.CharField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='Живлення укр')
    mouse_pow_ru = models.CharField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='Живлення ру')
    mouse_length_cable = models.CharField(null=True, blank=True,
    max_length=300, verbose_name='Довжина кабелю')
    mouse_vol = models.CharField(null=True, blank=True,
    max_length=300, verbose_name='Розмір')
    mouse_weight = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='Вага')
    mouse_col_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='колор_укр')
    mouse_col_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='колор_ру')
    mouse_warr_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='гарантия укр')
    mouse_warr_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True,
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
    get_price_rent_price_ua.short_description = '%'

    def warranty(self):
        return re.sub('\D+', '', self.mouse_warr_ru)
    warranty.short_description = 'waranty'

    class Meta:
        unique_together = ('part_number', 'is_active')
        ordering = ['name']
        verbose_name = 'Миша'
        verbose_name_plural = '1 Миші'


class Pads(models.Model):

    name = models.CharField(max_length=300, unique=True, verbose_name="Iм'я")
    category_ru = models.CharField(null=True, blank=True, max_length=300,
    verbose_name='категорiя_ру')
    category_ua = models.CharField(null=True, blank=True, max_length=300,
    verbose_name='категорiя_укр')
    part_number = models.CharField(max_length=300, db_index=True,
    verbose_name='партнамбер')
    part_number_web = models.CharField(max_length=300, db_index=True,
    verbose_name='партнамбер_веб', default='-')
    is_active = models.BooleanField(default=True, verbose_name='вкл/викл')
    full = models.BooleanField(default=True, verbose_name='заповн/нi')
    hotline = models.BooleanField(default=False, verbose_name='hotline')
    delivery = models.BooleanField(default=False, verbose_name='доствка')
    creditoff = models.BooleanField(default=False, verbose_name='credit')
    label = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='label')

    price_rent = models.FloatField(max_length=300, db_index=True,
    verbose_name='цiна з нац')
    r_price = models.FloatField(max_length=300, db_index=True,
    verbose_name='r_price')
    rrp_price = models.FloatField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='rrp')
    auto = models.BooleanField(default=False, verbose_name='руч/п')
    price_ua = models.FloatField(max_length=300, db_index=True, verbose_name='цена грн')
    price_usd = models.FloatField(max_length=300, db_index=True,
    verbose_name='цiна $')
    rentability = models.FloatField(default=5, db_index=True, verbose_name='нацiнка')
    provider = models.CharField(default='dc', max_length=300,
    db_index=True, verbose_name='пост')

    vendor = models.CharField(null=True, blank=True,max_length=300,
    db_index=True, verbose_name='vendor')
    pad_bot_ua = models.CharField(null=True, blank=True, max_length=300,
    db_index=True, verbose_name="Матеріал укр")
    pad_bot_ru = models.CharField(null=True, blank=True, max_length=300,
    db_index=True, verbose_name="Матеріал ру")
    pad_vol = models.CharField(null=True, blank=True, max_length=300,
    db_index=True, verbose_name="Габарити")
    pad_light = models.BooleanField(default=False, db_index=True,
    verbose_name="Наявність підсвічування")
    pad_col_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='колор_укр')
    pad_col_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='колор_ру')
    pad_warr_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='гарантия укр')
    pad_warr_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True,
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
    get_price_rent_price_ua.short_description = '%'

    def warranty(self):
        return re.sub('\D+', '', self.pad_warr_ru)
    warranty.short_description = 'waranty'

    class Meta:
        unique_together = ('part_number', 'is_active')
        ordering = ['name']
        verbose_name = 'Килимок'
        verbose_name_plural = '2 Килимки'


class Headsets(models.Model):

    name = models.CharField(max_length=300, unique=True, verbose_name="Iм'я")
    category_ru = models.CharField(null=True, blank=True, max_length=300,
    verbose_name='категорiя_ру')
    category_ua = models.CharField(null=True, blank=True, max_length=300,
    verbose_name='категорiя_укр')
    part_number = models.CharField(max_length=300, db_index=True,
    verbose_name='партнамбер')
    part_number_web = models.CharField(max_length=300, db_index=True,
    verbose_name='партнамбер_веб', default='-')
    is_active = models.BooleanField(default=True, verbose_name='вкл/викл')
    full = models.BooleanField(default=True, verbose_name='заповн/нi')
    hotline = models.BooleanField(default=False, verbose_name='hotline')
    delivery = models.BooleanField(default=False, verbose_name='доствка')
    creditoff = models.BooleanField(default=False, verbose_name='credit')
    label = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='label')

    price_rent = models.FloatField(max_length=300, db_index=True,
    verbose_name='цiна з нац')
    r_price = models.FloatField(max_length=300, db_index=True,
    verbose_name='r_price')
    rrp_price = models.FloatField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='rrp')
    auto = models.BooleanField(default=False, verbose_name='руч/п')
    price_ua = models.FloatField(max_length=300, db_index=True, verbose_name='цена грн')
    price_usd = models.FloatField(max_length=300, db_index=True,
    verbose_name='цiна $')
    rentability = models.FloatField(default=5, db_index=True, verbose_name='нацiнка')
    provider = models.CharField(default='dc', max_length=300,
    db_index=True, verbose_name='пост')

    vendor = models.CharField(null=True, blank=True,max_length=300,
    db_index=True, verbose_name='vendor')
    hs_type_connect_ua = models.CharField(null=True, blank=True,
    max_length=300, verbose_name='Тип підключення укр')
    hs_type_connect_ru = models.CharField(null=True, blank=True,
    max_length=300, verbose_name='Тип підключення ру')
    hs_sound_range = models.CharField(null=True, blank=True,
    max_length=300, verbose_name='Частотний діапазон')
    hs_resistance = models.CharField(null=True, blank=True,
    max_length=300, verbose_name='Опір навушників')
    hs_purpose_ua = models.CharField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='Призначення укр')
    hs_purpose_ru = models.CharField(null=True, blank=True,
    max_length=300, verbose_name='Призначення ру')
    hs_type_ua = models.CharField(null=True, blank=True,
    max_length=300, verbose_name='Тип навушників укр')
    hs_type_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='Тип навушників ру')
    hs_s_type_ua = models.CharField(null=True, blank=True,
    max_length=300, verbose_name='Тип гарнітури укр')
    hs_s_type_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='Тип гарнітури ру')
    hs_mike_ua = models.CharField(null=True, blank=True,
    max_length=300, verbose_name='Констр мікрофону укр')
    hs_mike_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='Констр мікрофону ру')
    hs_mike_avail = models.BooleanField(default=False, db_index=True,
    verbose_name='Наявність мікрофону')
    hs_cable_length = models.CharField(null=True, blank=True,
    max_length=300, verbose_name='Довжина кабелю')
    hs_interface = models.BooleanField(default=False, db_index=True,
    verbose_name='3.5 мм (mini-jack)')
    hs_usb = models.BooleanField(default=False, db_index=True,
    verbose_name='USB')
    hs_usb_type_c = models.BooleanField(default=False, db_index=True,
    verbose_name='USB Type-C')
    hs_col_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='колор_укр')
    hs_col_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='колор_ру')

    hs_weight = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='Вага')
    hs_ear_pads_material_ua = models.CharField(null=True, blank=True,
    max_length=300, verbose_name='Матеріал амбушюр укр')
    hs_ear_pads_material_ru = models.CharField(null=True, blank=True,
    max_length=300, db_index=True,
    verbose_name='Матеріал амбушюр ру')
    hs_metal_pads_material_ua = models.CharField(null=True, blank=True,
    max_length=300, verbose_name='Матеріал корпусу укр')
    hs_metal_pads_material_ru = models.CharField(null=True, blank=True,
    max_length=300, db_index=True,
    verbose_name='Матеріал корпусу ру')
    hs_time = models.CharField(null=True, blank=True,
    max_length=300, verbose_name='Час роботи розмова/очікування')
    hs_con_type = models.CharField(null=True, blank=True,
    max_length=300, verbose_name='Тип бездротового підключення')
    hs_ver = models.CharField(null=True, blank=True,
    max_length=300, verbose_name='Версія Bluetooth')
    hs_water_res = models.BooleanField(default=False, db_index=True,
    verbose_name='Вологостійкість')
    hs_light = models.BooleanField(default=False, db_index=True,
    verbose_name='Наявність підсвічування')
    hs_pow_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='Живлення_укр')
    hs_pow_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='Живлення_ру')

    hs_warr_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='гарантия укр')
    hs_warr_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True,
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
    get_price_rent_price_ua.short_description = '%'

    def warranty(self):
        return re.sub('\D+', '', self.hs_warr_ru)
    warranty.short_description = 'waranty'

    class Meta:
        unique_together = ('part_number', 'is_active')
        ordering = ['name']
        verbose_name = 'Гарнітура'
        verbose_name_plural = '5 Гарнітури'


class Webcams(models.Model):

    name = models.CharField(max_length=300, unique=True, verbose_name="Iм'я")
    category_ru = models.CharField(null=True, blank=True, max_length=300,
    verbose_name='категорiя_ру')
    category_ua = models.CharField(null=True, blank=True, max_length=300,
    verbose_name='категорiя_укр')
    part_number = models.CharField(max_length=300, db_index=True,
    verbose_name='партнамбер')
    part_number_web = models.CharField(max_length=300, db_index=True,
    verbose_name='партнамбер_веб', default='-')
    is_active = models.BooleanField(default=True, verbose_name='вкл/викл')
    full = models.BooleanField(default=True, verbose_name='заповн/нi')
    hotline = models.BooleanField(default=False, verbose_name='hotline')
    delivery = models.BooleanField(default=False, verbose_name='доствка')
    creditoff = models.BooleanField(default=False, verbose_name='credit')
    label = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='label')

    price_rent = models.FloatField(max_length=300, db_index=True,
    verbose_name='цiна з нац')
    r_price = models.FloatField(max_length=300, db_index=True,
    verbose_name='r_price')
    rrp_price = models.FloatField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='rrp')
    auto = models.BooleanField(default=False, verbose_name='руч/п')
    price_ua = models.FloatField(max_length=300, db_index=True, verbose_name='цена грн')
    price_usd = models.FloatField(max_length=300, db_index=True,
    verbose_name='цiна $')
    rentability = models.FloatField(default=5, db_index=True, verbose_name='нацiнка')
    provider = models.CharField(default='dc', max_length=300,
    db_index=True, verbose_name='пост')

    vendor = models.CharField(null=True, blank=True,max_length=300,
    db_index=True, verbose_name='vendor')
    web_r = models.CharField(null=True, blank=True, max_length=300,
    db_index=True, verbose_name="Роздільна здатність")
    web_pixel = models.CharField(null=True, blank=True, max_length=300,
    db_index=True, verbose_name="Кількість мегапікселів веб-камери")
    web_type_sensor = models.CharField(null=True, blank=True, max_length=300,
    db_index=True, verbose_name="Тип сенсора")
    web_mike = models.BooleanField(default=False, db_index=True,
    verbose_name="Мікрофон")
    web_focus = models.CharField(null=True, blank=True, max_length=300,
    db_index=True, verbose_name="Фокусування")
    web_int = models.CharField(null=True, blank=True, max_length=300,
    db_index=True, verbose_name='Інтерфейси')
    web_max_f = models.PositiveIntegerField(default=0, db_index=True,
    verbose_name='Максимальна частота кадрів відео')
    web_angle = models.CharField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='Кут огляду')
    web_weight = models.CharField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='Вага (г)')
    web_col_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='колор_укр')
    web_col_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='колор_ру')
    web_warr_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='гарантия укр')
    web_warr_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True,
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
    get_price_rent_price_ua.short_description = '%'

    def warranty(self):
        return re.sub('\D+', '', self.web_warr_ru)
    warranty.short_description = 'waranty'

    class Meta:
        unique_together = ('part_number', 'is_active')
        ordering = ['name']
        verbose_name = 'Вебкамера'
        verbose_name_plural = '6 Вебкамери'


class WiFis(models.Model):

    name = models.CharField(max_length=300, unique=True, verbose_name="Iм'я")
    category_ru = models.CharField(null=True, blank=True, max_length=300,
    verbose_name='категорiя_ру')
    category_ua = models.CharField(null=True, blank=True, max_length=300,
    verbose_name='категорiя_укр')
    part_number = models.CharField(max_length=300, db_index=True,
    verbose_name='партнамбер')
    part_number_web = models.CharField(max_length=300, db_index=True,
    verbose_name='партнамбер_веб', default='-')
    is_active = models.BooleanField(default=True, verbose_name='вкл/викл')
    full = models.BooleanField(default=True, verbose_name='заповн/нi')
    hotline = models.BooleanField(default=False, verbose_name='hotline')
    delivery = models.BooleanField(default=False, verbose_name='доствка')
    creditoff = models.BooleanField(default=False, verbose_name='credit')
    label = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='label')

    price_rent = models.FloatField(max_length=300, db_index=True,
    verbose_name='цiна з нац')
    r_price = models.FloatField(max_length=300, db_index=True,
    verbose_name='r_price')
    rrp_price = models.FloatField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='rrp')
    auto = models.BooleanField(default=False, verbose_name='руч/п')
    price_ua = models.FloatField(max_length=300, db_index=True, verbose_name='цена грн')
    price_usd = models.FloatField(max_length=300, db_index=True,
    verbose_name='цiна $')
    rentability = models.FloatField(default=5, db_index=True, verbose_name='нацiнка')
    provider = models.CharField(default='dc', max_length=300,
    db_index=True, verbose_name='пост')

    vendor = models.CharField(null=True, blank=True,max_length=300,
    db_index=True, verbose_name='vendor')
    net_wifi_int = models.CharField(null=True, blank=True, max_length=300,
    db_index=True, verbose_name="Інтерфейс підключення")
    net_wifi_ant_am = models.PositiveIntegerField(default=0, db_index=True,
    verbose_name="Зовнішні антени")
    net_wifi_st = models.CharField(null=True, blank=True, max_length=300,
    db_index=True, verbose_name="Стандарти Wi-Fi")
    net_wifi_ghz = models.CharField(null=True, blank=True, max_length=300,
    db_index=True, verbose_name="Частота роботи Wi-Fi")
    net_wifi_max_spd_ua = models.CharField(null=True, blank=True, max_length=300,
    db_index=True, verbose_name="Швидкість укр")
    net_wifi_max_spd_ru = models.CharField(null=True, blank=True, max_length=300,
    db_index=True, verbose_name="Швидкість ру")
    net_wifi_bt = models.BooleanField(default=False, db_index=True,
    verbose_name='Підтримка Bluetooth')
    net_wifi_warr_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='гарантия укр')
    net_wifi_warr_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True,
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
    get_price_rent_price_ua.short_description = '%'

    def warranty(self):
        return re.sub('\D+', '', self.net_wifi_warr_ru)
    warranty.short_description = 'waranty'

    class Meta:
        unique_together = ('part_number', 'is_active')
        ordering = ['name']
        verbose_name = 'WiFi'
        verbose_name_plural = '7 WiFi'


class Acoustics(models.Model):

    name = models.CharField(max_length=300, unique=True, verbose_name="Iм'я")
    category_ru = models.CharField(null=True, blank=True, max_length=300,
    verbose_name='категорiя_ру')
    category_ua = models.CharField(null=True, blank=True, max_length=300,
    verbose_name='категорiя_укр')
    part_number = models.CharField(max_length=300, db_index=True,
    verbose_name='партнамбер')
    part_number_web = models.CharField(max_length=300, db_index=True,
    verbose_name='партнамбер_веб', default='-')
    is_active = models.BooleanField(default=True, verbose_name='вкл/викл')
    full = models.BooleanField(default=True, verbose_name='заповн/нi')
    hotline = models.BooleanField(default=False, verbose_name='hotline')
    delivery = models.BooleanField(default=False, verbose_name='доствка')
    creditoff = models.BooleanField(default=False, verbose_name='credit')
    label = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='label')

    price_rent = models.FloatField(max_length=300, db_index=True,
    verbose_name='цiна з нац')
    r_price = models.FloatField(max_length=300, db_index=True,
    verbose_name='r_price')
    rrp_price = models.FloatField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='rrp')
    auto = models.BooleanField(default=False, verbose_name='руч/п')
    price_ua = models.FloatField(max_length=300, db_index=True, verbose_name='цена грн')
    price_usd = models.FloatField(max_length=300, db_index=True,
    verbose_name='цiна $')
    rentability = models.FloatField(default=5, db_index=True, verbose_name='нацiнка')
    provider = models.CharField(default='dc', max_length=300,
    db_index=True, verbose_name='пост')

    vendor = models.CharField(null=True, blank=True,max_length=300,
    db_index=True, verbose_name='vendor')
    a_format = models.CharField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='Формат акустики')
    a_p = models.CharField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='Потужність')
    a_f = models.CharField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='Частотний діапазон')
    a_s_n = models.CharField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='Співвідношення сигнал/шум')
    a_audio = models.CharField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='Аудіо')


    a_usb = models.BooleanField(default=False, db_index=True,
    verbose_name='USB')
    a_eth = models.BooleanField(default=False, db_index=True,
    verbose_name='Ethernet')
    a_card = models.BooleanField(default=False, db_index=True,
    verbose_name='Кардрідер')
    a_wifi = models.BooleanField(default=False, db_index=True,
    verbose_name='Wi-Fi')
    a_bt = models.BooleanField(default=False, db_index=True,
    verbose_name='Bluetooth')
    a_fm = models.BooleanField(default=False, db_index=True,
    verbose_name='FM-приймач')
    a_control = models.BooleanField(default=False, db_index=True,
    verbose_name='Пульт ДК')

    a_pow_ua = models.CharField(null=True, blank=True, max_length=300,
    db_index=True, verbose_name="Живлення укр")
    a_pow_ru = models.CharField(null=True, blank=True, max_length=300,
    db_index=True, verbose_name="Живлення ру")
    a_bot_ua = models.CharField(null=True, blank=True, max_length=300,
    db_index=True, verbose_name="Матеріал укр")
    a_bot_ru = models.CharField(null=True, blank=True, max_length=300,
    db_index=True, verbose_name="Матеріал ру")
    a_vol = models.CharField(null=True, blank=True, max_length=300,
    db_index=True, verbose_name="Габарити")
    a_weight = models.CharField(null=True, blank=True, max_length=300,
    db_index=True, verbose_name="Вага")
    a_col_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='колор_укр')
    a_col_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='колор_ру')
    a_warr_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='гарантия укр')
    a_warr_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True,
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
    get_price_rent_price_ua.short_description = '%'

    def warranty(self):
        return re.sub('\D+', '', self.a_warr_ru)
    warranty.short_description = 'waranty'

    class Meta:
        unique_together = ('part_number', 'is_active')
        ordering = ['name']
        verbose_name = 'Акустика'
        verbose_name_plural = '8 Акустика'


class Tables(models.Model):

    name = models.CharField(max_length=300, unique=True, verbose_name="Iм'я")
    category_ru = models.CharField(null=True, blank=True, max_length=300,
    verbose_name='категорiя_ру')
    category_ua = models.CharField(null=True, blank=True, max_length=300,
    verbose_name='категорiя_укр')
    part_number = models.CharField(max_length=300, db_index=True,
    verbose_name='партнамбер')
    part_number_web = models.CharField(max_length=300, db_index=True,
    verbose_name='партнамбер_веб', default='-')
    is_active = models.BooleanField(default=True, verbose_name='вкл/викл')
    full = models.BooleanField(default=True, verbose_name='заповн/нi')
    hotline = models.BooleanField(default=False, verbose_name='hotline')
    delivery = models.BooleanField(default=False, verbose_name='доствка')
    creditoff = models.BooleanField(default=False, verbose_name='credit')
    label = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='label')

    price_rent = models.FloatField(max_length=300, db_index=True,
    verbose_name='цiна з нац')
    r_price = models.FloatField(max_length=300, db_index=True,
    verbose_name='r_price')
    rrp_price = models.FloatField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='rrp')
    auto = models.BooleanField(default=False, verbose_name='руч/п')
    price_ua = models.FloatField(max_length=300, db_index=True, verbose_name='цена грн')
    price_usd = models.FloatField(max_length=300, db_index=True,
    verbose_name='цiна $')
    rentability = models.FloatField(default=5, db_index=True, verbose_name='нацiнка')
    provider = models.CharField(default='dc', max_length=300,
    db_index=True, verbose_name='пост')

    vendor = models.CharField(null=True, blank=True,max_length=300,
    db_index=True, verbose_name='vendor')
    tb_format_ua = models.CharField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='Форма укр')
    tb_format_ru = models.CharField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='Форма ру')

    tb_led = models.BooleanField(default=False, db_index=True,
    verbose_name='Світлодіодне підсвічування')
    tb_h = models.BooleanField(default=False, db_index=True,
    verbose_name='Регулятор висоти')
    tb_angle = models.BooleanField(default=False, db_index=True,
    verbose_name='Регулятор нахилу')
    tb_up = models.BooleanField(default=False, db_index=True,
    verbose_name='Надставка')
    tb_in = models.BooleanField(default=False, db_index=True,
    verbose_name='Висувна полиця для клавіатури')
    tb_box = models.BooleanField(default=False, db_index=True,
    verbose_name='Висувні ящики')
    tb_wheels = models.BooleanField(default=False, db_index=True,
    verbose_name='Наявність коліс')
    tb_cab = models.BooleanField(default=False, db_index=True,
    verbose_name='Кабельне введення')
    tb_down = models.BooleanField(default=False, db_index=True,
    verbose_name='Підставка під системний блок')

    tb_bot_t_ua = models.CharField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='Матеріал стільниці укр')
    tb_bot_t_ru = models.CharField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='Матеріал стільниці ру')
    tb_bot_r_ua = models.CharField(null=True, blank=True, max_length=300,
    db_index=True, verbose_name="Матеріал рами укр")
    tb_bot_r_ru = models.CharField(null=True, blank=True, max_length=300,
    db_index=True, verbose_name="Матеріал рами ру")
    tb_hight = models.CharField(null=True, blank=True, max_length=300,
    db_index=True, verbose_name="Висота")
    tb_width = models.CharField(null=True, blank=True, max_length=300,
    db_index=True, verbose_name="Ширина")
    tb_depth = models.CharField(null=True, blank=True, max_length=300,
    db_index=True, verbose_name="Глибина")
    tb_weight = models.CharField(null=True, blank=True, max_length=300,
    db_index=True, verbose_name="Вага")
    tb_col_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='колор_укр')
    tb_col_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='колор_ру')
    tb_warr_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='гарантия укр')
    tb_warr_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True,
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
    get_price_rent_price_ua.short_description = '%'

    def warranty(self):
        return re.sub('\D+', '', self.tb_warr_ru)
    warranty.short_description = 'waranty'

    class Meta:
        unique_together = ('part_number', 'is_active')
        ordering = ['name']
        verbose_name = 'Стiл'
        verbose_name_plural = 'х10 Столи'


class Chairs(models.Model):

    name = models.CharField(max_length=300, unique=True, verbose_name="Iм'я")
    category_ru = models.CharField(null=True, blank=True, max_length=300,
    verbose_name='категорiя_ру')
    category_ua = models.CharField(null=True, blank=True, max_length=300,
    verbose_name='категорiя_укр')
    part_number = models.CharField(max_length=300, db_index=True,
    verbose_name='партнамбер')
    part_number_web = models.CharField(max_length=300, db_index=True,
    verbose_name='партнамбер_веб', default='-')
    is_active = models.BooleanField(default=True, verbose_name='вкл/викл')
    full = models.BooleanField(default=True, verbose_name='заповн/нi')
    hotline = models.BooleanField(default=False, verbose_name='hotline')
    delivery = models.BooleanField(default=False, verbose_name='доствка')
    creditoff = models.BooleanField(default=False, verbose_name='credit')
    label = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='label')

    price_rent = models.FloatField(max_length=300, db_index=True,
    verbose_name='цiна з нац')
    r_price = models.FloatField(max_length=300, db_index=True,
    verbose_name='r_price')
    rrp_price = models.FloatField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='rrp')
    auto = models.BooleanField(default=False, verbose_name='руч/п')
    price_ua = models.FloatField(max_length=300, db_index=True, verbose_name='цена грн')
    price_usd = models.FloatField(max_length=300, db_index=True,
    verbose_name='цiна $')
    rentability = models.FloatField(default=5, db_index=True, verbose_name='нацiнка')
    provider = models.CharField(default='dc', max_length=300,
    db_index=True, verbose_name='пост')

    vendor = models.CharField(null=True, blank=True,max_length=300,
    db_index=True, verbose_name='vendor')

    ch_type_ua = models.CharField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='Тип укр')
    ch_type_ru = models.CharField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='Тип ру')
    ch_main_ua = models.CharField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='Основа укр')
    ch_main_ru = models.CharField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='Основа ру')
    ch_chr_ua = models.CharField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='Хрестовина укр')
    ch_chr_ru = models.CharField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='Хрестовина ру')
    ch_mat_ua = models.CharField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='Оббивка укр')
    ch_mat_ru = models.CharField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='Оббивка ру')
    ch_frame_ua = models.CharField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='Каркас укр')
    ch_frame_ru = models.CharField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='Каркас ру')

    ch_vol = models.CharField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='Розміри сидіння')
    ch_back = models.CharField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='Розміри спинки')
    ch_back_angle = models.CharField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='Кут нахилу спинки')
    ch_hand = models.BooleanField(default=False, db_index=True,
    verbose_name='Регулювання підлокітників')
    ch_hight = models.BooleanField(default=False, db_index=True,
    verbose_name='Регулювання висоти сидіння')
    ch_mech_ua = models.CharField(null=True, blank=True, max_length=300,
    db_index=True, verbose_name="Вбудовані механізми укр")
    ch_mech_ru = models.CharField(null=True, blank=True, max_length=300,
    db_index=True, verbose_name="Вбудовані механізми ру")
    ch_max_weight = models.CharField(null=True, blank=True, max_length=300,
    db_index=True, verbose_name="Максимально допустиме навантаження")
    ch_weight = models.CharField(null=True, blank=True, max_length=300,
    db_index=True, verbose_name="Вага")
    ch_col_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='колор_укр')
    ch_col_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='колор_ру')
    ch_warr_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='гарантия укр')
    ch_warr_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True,
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
    get_price_rent_price_ua.short_description = '%'

    def warranty(self):
        return re.sub('\D+', '', self.ch_warr_ru)
    warranty.short_description = 'waranty'

    class Meta:
        unique_together = ('part_number', 'is_active')
        ordering = ['name']
        verbose_name = 'Крiсло'
        verbose_name_plural = '9 Крiсла'


class Accessories(models.Model):

    name = models.CharField(max_length=300, unique=True, verbose_name="Iм'я")
    category_ru = models.CharField(null=True, blank=True, max_length=300,
    verbose_name='категорiя_ру')
    category_ua = models.CharField(null=True, blank=True, max_length=300,
    verbose_name='категорiя_укр')
    part_number = models.CharField(max_length=300, db_index=True,
    verbose_name='партнамбер')
    part_number_web = models.CharField(max_length=300, db_index=True,
    verbose_name='партнамбер_веб', default='-')
    is_active = models.BooleanField(default=True, verbose_name='вкл/викл')
    full = models.BooleanField(default=True, verbose_name='заповн/нi')
    hotline = models.BooleanField(default=False, verbose_name='hotline')
    delivery = models.BooleanField(default=False, verbose_name='доствка')
    creditoff = models.BooleanField(default=False, verbose_name='credit')
    label = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='label')

    price_rent = models.FloatField(max_length=300, db_index=True,
    verbose_name='цiна з нац')
    r_price = models.FloatField(max_length=300, db_index=True,
    verbose_name='r_price')
    rrp_price = models.FloatField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='rrp')
    auto = models.BooleanField(default=False, verbose_name='руч/п')
    price_ua = models.FloatField(max_length=300, db_index=True, verbose_name='цена грн')
    price_usd = models.FloatField(max_length=300, db_index=True,
    verbose_name='цiна $')
    rentability = models.FloatField(default=5, db_index=True, verbose_name='нацiнка')
    provider = models.CharField(default='dc', max_length=300,
    db_index=True, verbose_name='пост')

    vendor = models.CharField(null=True, blank=True,max_length=300,
    db_index=True, verbose_name='vendor')
    acc_type_ua = models.CharField(null=True, blank=True, max_length=300,
    db_index=True, verbose_name="Тип укр")
    acc_type_ru = models.CharField(null=True, blank=True, max_length=300,
    db_index=True, verbose_name="Тип ру")
    acc_desc_ua = models.TextField(null=True, blank=True,
    db_index=True, verbose_name="Опис-характеристика укр")
    acc_desc_ru = models.TextField(null=True, blank=True,
    db_index=True, verbose_name="Опис-характеристика ру")
    acc_col_ua = models.CharField(null=True, blank=True, max_length=300,
    db_index=True, verbose_name="колор_укр")
    acc_col_ru = models.CharField(null=True, blank=True, max_length=300,
    db_index=True, verbose_name="колор_ру")

    acc_warr_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='гарантия укр')
    acc_warr_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True,
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
    get_price_rent_price_ua.short_description = '%'

    def warranty(self):
        return re.sub('\D+', '', self.acc_warr_ru)
    warranty.short_description = 'waranty'

    class Meta:
        unique_together = ('part_number', 'is_active')
        ordering = ['name']
        verbose_name = 'Аксесуари для ПК'
        verbose_name_plural = 'х13 Аксесуари для ПК'


class Cabelsplus(models.Model):

    name = models.CharField(max_length=300, unique=True, verbose_name="Iм'я")
    category_ru = models.CharField(null=True, blank=True, max_length=300,
    verbose_name='категорiя_ру')
    category_ua = models.CharField(null=True, blank=True, max_length=300,
    verbose_name='категорiя_укр')
    part_number = models.CharField(max_length=300, db_index=True,
    verbose_name='партнамбер')
    part_number_web = models.CharField(max_length=300, db_index=True,
    verbose_name='партнамбер_веб', default='-')
    is_active = models.BooleanField(default=True, verbose_name='вкл/викл')
    full = models.BooleanField(default=True, verbose_name='заповн/нi')
    hotline = models.BooleanField(default=False, verbose_name='hotline')
    delivery = models.BooleanField(default=False, verbose_name='доствка')
    creditoff = models.BooleanField(default=False, verbose_name='credit')
    label = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='label')

    price_rent = models.FloatField(max_length=300, db_index=True,
    verbose_name='цiна з нац')
    r_price = models.FloatField(max_length=300, db_index=True,
    verbose_name='r_price')
    rrp_price = models.FloatField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='rrp')
    auto = models.BooleanField(default=False, verbose_name='руч/п')
    price_ua = models.FloatField(max_length=300, db_index=True, verbose_name='цена грн')
    price_usd = models.FloatField(max_length=300, db_index=True,
    verbose_name='цiна $')
    rentability = models.FloatField(default=5, db_index=True, verbose_name='нацiнка')
    provider = models.CharField(default='dc', max_length=300,
    db_index=True, verbose_name='пост')

    vendor = models.CharField(null=True, blank=True,max_length=300,
    db_index=True, verbose_name='vendor')
    cab_con_f = models.CharField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name="Роз'єм 1")
    cab_con_s = models.CharField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name="Роз'єм 2")
    cab_conn_ua = models.CharField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name="Конектори укр")
    cab_conn_ru = models.CharField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name="Конектори ру")

    cab_flat = models.BooleanField(default=False, db_index=True,
    verbose_name='Плаский кабель')
    cab_tissue = models.BooleanField(default=False, db_index=True,
    verbose_name='Тканинне обплетення')
    cab_metal = models.BooleanField(default=False, db_index=True,
    verbose_name='Металеве обплетення')
    cab_g_type = models.BooleanField(default=False, db_index=True,
    verbose_name='Г-подібний')

    cab_ver = models.CharField(null=True, blank=True, max_length=300,
    db_index=True, verbose_name="Версія")
    cab_long = models.CharField(null=True, blank=True, max_length=300,
    db_index=True, verbose_name="Довжина кабеля")
    cab_color_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='колор_укр')
    cab_color_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='колор_ру')
    cab_col_u = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='колор_укр')
    cab_col_r = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='колор_ру')
    cab_col_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='колор_укр')
    cab_col_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='колор_ру')
    cab_warr_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='гарантия укр')
    cab_warr_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True,
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
    get_price_rent_price_ua.short_description = '%'

    def warranty(self):
        return re.sub('\D+', '', self.cab_warr_ru)
    warranty.short_description = 'waranty'

    class Meta:
        unique_together = ('part_number', 'is_active')
        ordering = ['name']
        verbose_name = 'Кабель'
        verbose_name_plural = 'х11 Кабелi'


class Filters(models.Model):

    name = models.CharField(max_length=300, unique=True, verbose_name="Iм'я")
    category_ru = models.CharField(null=True, blank=True, max_length=300,
    verbose_name='категорiя_ру')
    category_ua = models.CharField(null=True, blank=True, max_length=300,
    verbose_name='категорiя_укр')
    part_number = models.CharField(max_length=300, db_index=True,
    verbose_name='партнамбер')
    part_number_web = models.CharField(max_length=300, db_index=True,
    verbose_name='партнамбер_веб', default='-')
    is_active = models.BooleanField(default=True, verbose_name='вкл/викл')
    full = models.BooleanField(default=True, verbose_name='заповн/нi')
    hotline = models.BooleanField(default=False, verbose_name='hotline')
    delivery = models.BooleanField(default=False, verbose_name='доствка')
    creditoff = models.BooleanField(default=False, verbose_name='credit')
    label = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='label')

    price_rent = models.FloatField(max_length=300, db_index=True,
    verbose_name='цiна з нац')
    r_price = models.FloatField(max_length=300, db_index=True,
    verbose_name='r_price')
    rrp_price = models.FloatField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='rrp')
    auto = models.BooleanField(default=False, verbose_name='руч/п')
    price_ua = models.FloatField(max_length=300, db_index=True, verbose_name='цена грн')
    price_usd = models.FloatField(max_length=300, db_index=True,
    verbose_name='цiна $')
    rentability = models.FloatField(default=5, db_index=True, verbose_name='нацiнка')
    provider = models.CharField(default='dc', max_length=300,
    db_index=True, verbose_name='пост')

    vendor = models.CharField(null=True, blank=True,max_length=300,
    db_index=True, verbose_name='vendor')
    fi_num = models.CharField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name="Кількість розеток")
    fi_cab_lenght = models.CharField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name="Довжина кабеля")
    fi_u = models.CharField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name="Робоча напруга")
    fi_max_i = models.CharField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name="Максимальна сила струму")
    fi_max_pow = models.CharField(null=True, blank=True,
    max_length=300, db_index=True,
    verbose_name="Максимальна сумарна потужність навантаження")

    fi_con = models.BooleanField(default=False, db_index=True,
    verbose_name='Вимикач')

    fi_bot_ua = models.CharField(null=True, blank=True, max_length=300,
    db_index=True, verbose_name="Матеріал укр")
    fi_bot_ru = models.CharField(null=True, blank=True, max_length=300,
    db_index=True, verbose_name="Матеріал ру")
    fi_col_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='колор_укр')
    fi_col_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='колор_ру')
    fi_warr_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='гарантия укр')
    fi_warr_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True,
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
    get_price_rent_price_ua.short_description = '%'

    def warranty(self):
        return re.sub('\D+', '', self.fi_warr_ru)
    warranty.short_description = 'waranty'

    class Meta:
        unique_together = ('part_number', 'is_active')
        ordering = ['name']
        verbose_name = 'Фiльтр сетьовий'
        verbose_name_plural = 'х12 Фiльтри сетьовi'

class Others(models.Model):

    name = models.CharField(max_length=300, unique=True, verbose_name="Iм'я")
    category_ru = models.CharField(null=True, blank=True, max_length=300,
    verbose_name='категорiя_ру')
    category_ua = models.CharField(null=True, blank=True, max_length=300,
    verbose_name='категорiя_укр')
    part_number = models.CharField(max_length=300, db_index=True,
    verbose_name='партнамбер')
    part_number_web = models.CharField(max_length=300, db_index=True,
    verbose_name='партнамбер_веб', default='-')
    is_active = models.BooleanField(default=True, verbose_name='вкл/викл')
    full = models.BooleanField(default=True, verbose_name='заповн/нi')
    hotline = models.BooleanField(default=False, verbose_name='hotline')
    delivery = models.BooleanField(default=False, verbose_name='доствка')
    creditoff = models.BooleanField(default=False, verbose_name='credit')
    label = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='label')

    price_rent = models.FloatField(max_length=300, db_index=True,
    verbose_name='цiна з нац')
    r_price = models.FloatField(max_length=300, db_index=True,
    verbose_name='r_price')
    rrp_price = models.FloatField(null=True, blank=True,
    max_length=300, db_index=True, verbose_name='rrp')
    auto = models.BooleanField(default=False, verbose_name='руч/п')
    price_ua = models.FloatField(max_length=300, db_index=True, verbose_name='цена грн')
    price_usd = models.FloatField(max_length=300, db_index=True,
    verbose_name='цiна $')
    rentability = models.FloatField(default=5, db_index=True, verbose_name='нацiнка')
    provider = models.CharField(default='dc', max_length=300,
    db_index=True, verbose_name='пост')

    vendor = models.CharField(null=True, blank=True,max_length=300,
    db_index=True, verbose_name='vendor')
    oth_type_ua = models.CharField(null=True, blank=True, max_length=300,
    db_index=True, verbose_name="Категорія укр")
    oth_type_ru = models.CharField(null=True, blank=True, max_length=300,
    db_index=True, verbose_name="Категорія ру")
    oth_desc_ua = models.TextField(null=True, blank=True,
    db_index=True, verbose_name="Опис-характеристика укр")
    oth_desc_ru = models.TextField(null=True, blank=True,
    db_index=True, verbose_name="Опис-характеристика ру")

    oth_warr_ua = models.CharField(null=True, blank=True,max_length=300, db_index=True,
    verbose_name='гарантия укр')
    oth_warr_ru = models.CharField(null=True, blank=True,max_length=300, db_index=True,
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
    get_price_rent_price_ua.short_description = '%'

    def warranty(self):
        return re.sub('\D+', '', self.oth_warr_ru)
    warranty.short_description = 'waranty'

    class Meta:
        unique_together = ('part_number', 'is_active')
        ordering = ['name']
        verbose_name = 'Унiверсальне,рiзне'
        verbose_name_plural = 'х14 Унiверсальне_рiзне'
#
