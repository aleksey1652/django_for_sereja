from django.db import models
from datetime import datetime, date, time
#from django.db.models import signals
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.db.models import signals


def validate_name(value):
    from cat.models import Computers

    valid_names = Computers.objects.filter(
    pc_assembly__sites__name_sites='versum'
    ).values_list('name_computers', flat=True)

    if value not in valid_names:
        raise ValidationError(f'Нет такого компа: {value}')

class Assemblage(models.Model):
    CHOISE_RAM = (
        ('DDR4', 'DDR4'),
        ('DDR5', 'DDR5'),
    )

    date_ch = models.DateTimeField(auto_now=True, verbose_name='Дата')
    name = models.CharField(max_length=50, db_index=True,
    verbose_name='Имя', unique=True, validators=[validate_name])
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True,
    db_index=True, verbose_name="URL")
    is_active = models.BooleanField(default=False, verbose_name='Вкл/выкл')
    proc = models.CharField(max_length=50, db_index=True,
    verbose_name='Процессор',default='')
    gpu = models.CharField(max_length=50, db_index=True,
    verbose_name='Видеокарта',default='')
    ram = models.CharField(max_length=50, db_index=True,
    verbose_name='ОЗУ',default='')
    ram_type = models.CharField(max_length=50, db_index=True,
    verbose_name='Тип ОЗУ', choices=CHOISE_RAM, default='DDR4')
    versum = models.URLField(max_length=255, unique=True, null=True, blank=True,
    db_index=True, verbose_name="versum")
    itblok = models.URLField(max_length=255, unique=True, null=True, blank=True,
    db_index=True, verbose_name="itblok")
    hotline = models.URLField(max_length=255, unique=True, null=True, blank=True,
    db_index=True, verbose_name="hotline")
    artline = models.URLField(max_length=255, unique=True, null=True, blank=True,
    db_index=True, verbose_name="artline")
    telemart = models.URLField(max_length=255, unique=True, null=True, blank=True,
    db_index=True, verbose_name="telemart")
    compx = models.URLField(max_length=255, unique=True, null=True, blank=True,
    db_index=True, verbose_name="compx")
    ver_price = models.FloatField(db_index=True, default=0, verbose_name='ver')
    it_price = models.FloatField(db_index=True, default=0, verbose_name='it')
    hot_price = models.FloatField(db_index=True, default=0, verbose_name='hot')
    art_price = models.FloatField(db_index=True, default=0, verbose_name='art')
    tel_price = models.FloatField(db_index=True, default=0, verbose_name='tel')
    com_price = models.FloatField(db_index=True, default=0, verbose_name='com')
    ver_it = models.FloatField(db_index=True, default=0, verbose_name='ver-it')
    ver_hot = models.FloatField(db_index=True, default=0, verbose_name='ver-hot')
    ver_art = models.FloatField(db_index=True, default=0, verbose_name='ver-art')
    ver_tel = models.FloatField(db_index=True, default=0, verbose_name='ver-tel')
    ver_com = models.FloatField(db_index=True, default=0, verbose_name='ver-com')

    groups = models.ForeignKey('Groups', on_delete=models.PROTECT, null=True)

    def __str__(self):
        return f'{str(self.proc)}-{str(self.gpu)}-{self.ram}-{self.ram_type}'

    def get_absolute_url(self):
        return reverse('test_assemblage', kwargs={'assm_slug': self.slug})

    #def save_model(self, request, obj, form, change):
        # Automatically populate versum field as "https://versum.ua/" + slug
        #obj.versum = "https://versum.ua/" + obj.slug
        #super().save_model(request, obj, form, change)

    class Meta:
        verbose_name_plural = 'Сборки-сравни'
        verbose_name = 'Сборка-сравни'
        ordering = ['proc']

def post_saves_or_update_rivals(sender, instance, created, **kwargs):
    if not instance.versum:
        instance.versum = "https://versum.ua/" + instance.slug
        instance.save()

signals.post_save.connect(receiver=post_saves_or_update_rivals, sender=Assemblage)


class Groups(models.Model):
    name = models.CharField(max_length=50, db_index=True, unique=True,
    verbose_name="Группа сборок")
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True,
    db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('test_groups', kwargs={'gr_slug': self.slug})

    class Meta:
        verbose_name_plural = 'Группы-сборки-сравни'
        verbose_name = 'Группа-сборка-сравни'
        ordering = ['name']

class Rentabilitys(models.Model):
    rentability = models.FloatField(default=23, db_index=True, verbose_name='наценка')

    def __str__(self):
        return f"Rentability-{self.rentability}"

    class Meta:
        verbose_name_plural = 'Наценка'
        verbose_name = 'Наценка'
