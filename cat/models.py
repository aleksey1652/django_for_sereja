from django.db import models
from datetime import datetime, date, time

class USD(models.Model):
    usd = models.FloatField(db_index=True, verbose_name='usd')
    date_ch = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (self.date_ch).strftime("%d %B %Y") + ':' + str(self.usd)

class Parts_full(models.Model):
    name_parts = models.CharField(max_length=300, db_index=True, verbose_name='Name_parts')
    partnumber_parts = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='Partnumber_parts')
    #provider = models.CharField(null=True, blank=True,max_length=50, db_index=True, verbose_name='Provider', unique=True)
    availability_parts = models.CharField(null=True, blank=True,max_length=50, db_index=True, verbose_name='Availability_parts')
    providerprice_parts = models.CharField(null=True, blank=True,max_length=50, db_index=True, verbose_name='price_parts')
    url_parts = models.CharField(null=True, blank=True,max_length=200, db_index=True, verbose_name='Url_parts')
    item_price = models.CharField(null=True, blank=True,max_length=50, db_index=True, verbose_name='Item_price')
    remainder = models.CharField(null=True, blank=True,max_length=50, db_index=True, verbose_name='remainder')
    providers = models.ForeignKey('Providers', on_delete=models.CASCADE,null=True)
    date_chg = models.DateTimeField(null=True, blank=True, verbose_name='date_chg')

    def __str__(self):
        return self.name_parts

    class Meta:
        verbose_name_plural = 'Parts_full+'
        verbose_name = 'Parts_full'
        ordering = ['-name_parts']

class Parts_short(models.Model):
    name_parts = models.CharField(max_length=300, db_index=True, verbose_name='Name_parts')
    partnumber_list = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='Partnumber_list')
    x_code = models.CharField(null=True, blank=True,max_length=50, db_index=True, verbose_name='X_code')
    Advanced_parts = models.CharField(null=True, blank=True,max_length=50, db_index=True, verbose_name='Advanced_parts')
    min_price = models.CharField(null=True, blank=True,max_length=50, db_index=True, verbose_name='min_price')
    date_chg = models.DateTimeField(null=True, blank=True, verbose_name='date_chg')
    kind = models.CharField(null=True, blank=True,max_length=50, db_index=True, verbose_name='Kind')
    parts_full = models.ManyToManyField('Parts_full')
    kind2 = models.BooleanField(default=False)

    def __str__(self):
        return self.name_parts

    class Meta:
        verbose_name_plural = 'Parts_short+'
        verbose_name = 'Parts_short'
        ordering = ['-name_parts']

class Computers(models.Model):
    name_computers = models.CharField(max_length=300, db_index=True, verbose_name='Name_computers')
    url_computers = models.CharField(max_length=300, db_index=True, verbose_name='Url_computers')
    price_computers = models.CharField(max_length=300, db_index=True, verbose_name='Price_computers')
    proc_computers = models.CharField(max_length=300, db_index=True, verbose_name='Proc_computers')
    mb_computers = models.CharField(max_length=300, db_index=True, verbose_name='Mb_computers')
    mem_computers = models.CharField(max_length=300, db_index=True, verbose_name='Mem_computers')
    video_computers = models.CharField(max_length=300, db_index=True, verbose_name='Video_computers')
    hdd_computers = models.CharField(max_length=300, db_index=True, verbose_name='Hdd_computers')
    ps_computers = models.CharField(max_length=300, db_index=True, verbose_name='Ps_computers')
    case_computers = models.CharField(max_length=300, db_index=True, verbose_name='Case_computers')
    cool_computers = models.CharField(max_length=300, db_index=True, verbose_name='Cool_computers')
    class_computers = models.CharField(max_length=300, db_index=True, verbose_name='Class_computers')
    warranty_computers = models.CharField(max_length=300, db_index=True, verbose_name='Warranty_computers')
    vent_computers = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='Cool_computers')
    mem_num_computers = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='Mem_computers')
    video_num_computers = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='Video_computers')
    vent_num_computers = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='Cool_computers')
    is_active = models.BooleanField(default=True)
    date_computers = models.DateTimeField(auto_now=True)
    mon_computers = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='mon_computers')
    wifi_computers = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='wifi_computers')
    km_computers = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='km_computers')

    pc_assembly = models.ForeignKey(
                               'Pc_assembly',on_delete=models.PROTECT,
                               null=True,verbose_name='Pc_assembly'
                               )

    def __str__(self):
        return self.name_computers

    class Meta:
        verbose_name_plural = 'Computers'
        verbose_name = 'Computer'
        ordering = ['-name_computers']

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

"""class Pack(models.Model):
    item_name = models.CharField(max_length=100, db_index=True, verbose_name='Item_name')
    item_price = models.CharField(null=True, blank=True,max_length=50, db_index=True, verbose_name='Item_price')
    item_article = models.CharField(max_length=100, db_index=True, verbose_name='Item_article')

    def __str__(self):
        return self.item_name"""

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
        ('-', '-'),
    )
    # choices=CHOISE2,default='dc'
    name_provider =  models.CharField(max_length=50,db_index=True,choices=CHOISE,default='-',verbose_name='Name_provider')
    more = models.TextField(null=True, blank=True, verbose_name='More_about_provider')

    def __str__(self):
        return self.name_provider

    class Meta:
        verbose_name_plural = 'Provider'
        verbose_name = 'Providers+'

class Articles(models.Model):
    article = models.CharField(max_length=50, db_index=True, verbose_name='Article_field', unique=True)
    providers = models.ManyToManyField(Providers)
    item_name = models.CharField(null=True, blank=True,max_length=100, db_index=True, verbose_name='Item_name')
    item_price = models.CharField(null=True, blank=True,max_length=50, db_index=True, verbose_name='Item_price')
    computers = models.ForeignKey(Computers, null=True,on_delete=models.CASCADE)

    def __str__(self):
        return self.article

class Pc_assembly(models.Model):
    name_assembly = models.CharField(max_length=300, db_index=True, verbose_name='Name_assembly')
    kind_assembly = models.CharField(null=True, blank=True,max_length=50, db_index=True, verbose_name='Kind_assembly')

    sites = models.ForeignKey(
                               'Sites',on_delete=models.PROTECT,
                               null=True,verbose_name='Site',
                               related_query_name='entry'
                               )

    def __str__(self):
        return self.name_assembly

    class Meta:
        verbose_name_plural = 'Assemblies'
        verbose_name = 'Assembly'

class Cooler(models.Model):
    name = models.CharField(max_length=300, db_index=True, verbose_name='Name_cooler')
    part_number = models.CharField(max_length=300, db_index=True, verbose_name='Part_number')
    vendor = models.CharField(max_length=300, db_index=True, verbose_name='Vendor')
    price = models.CharField(max_length=300, db_index=True, verbose_name='Price')
    desc_ukr = models.TextField(db_index=True, verbose_name='Desc_ukr')
    desc_ru = models.TextField(db_index=True, verbose_name='Desc_ru')
    fan_type_ua = models.CharField(max_length=300, db_index=True, verbose_name='Fan_type_ua')
    fan_type_rus = models.CharField(max_length=300, db_index=True, verbose_name='fan_type_rus')
    fan_spd_ua = models.CharField(max_length=300, db_index=True, verbose_name='Fan_spd_ua')
    fan_spd_rus = models.CharField(max_length=300, db_index=True, verbose_name='Fan_spd_rus')
    fan_noise_level = models.CharField(max_length=300, db_index=True, verbose_name='Fan_noise_level')
    fan_size = models.CharField(max_length=300, db_index=True, verbose_name='Fan_size')
    more = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='More')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class CPU(models.Model):
    name = models.CharField(max_length=300, db_index=True, verbose_name='Name_cpu')
    part_number = models.CharField(max_length=300, db_index=True, verbose_name='Part_number')
    vendor = models.CharField(max_length=300, db_index=True, verbose_name='Vendor')
    price = models.CharField(max_length=300, db_index=True, verbose_name='Price')
    desc_ukr = models.TextField(db_index=True, verbose_name='Desc_ukr')
    desc_ru = models.TextField(db_index=True, verbose_name='Desc_ru')
    f_name = models.CharField(max_length=300, db_index=True, verbose_name='f_name')
    cpu_c_t = models.CharField(max_length=300, db_index=True, verbose_name='Cpu_c_t')
    f_cpu_c_t = models.CharField(max_length=300, db_index=True, verbose_name='F_cpu_c_t')
    cpu_b_f = models.CharField(max_length=300, db_index=True, verbose_name='Cpu_b_f')
    cpu_cache = models.CharField(max_length=300, db_index=True, verbose_name='Cpu_cache')
    cpu_i_g_ua = models.CharField(max_length=300, db_index=True, verbose_name='Cpu_i_g_ua')
    cpu_i_g_rus = models.CharField(max_length=300, db_index=True, verbose_name='Cpu_i_g_rus')
    more = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='More')
    depend_from = models.CharField(max_length=300, db_index=True, verbose_name='Depend_from')
    depend_from_type = models.CharField(max_length=300, db_index=True, verbose_name='Depend_from_type')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class MB(models.Model):
    name = models.CharField(max_length=300, db_index=True, verbose_name='Name_mb')
    part_number = models.CharField(max_length=300, db_index=True, verbose_name='Part_number')
    vendor = models.CharField(max_length=300, db_index=True, verbose_name='Vendor')
    main_category = models.CharField(max_length=300, db_index=True, verbose_name='Main_category')
    price = models.CharField(max_length=300, db_index=True, verbose_name='Price')
    desc_ukr = models.TextField(db_index=True, verbose_name='Desc_ukr')
    desc_ru = models.TextField(db_index=True, verbose_name='Desc_ru')
    mb_chipset = models.CharField(max_length=300, db_index=True, verbose_name='Mb_chipset')
    mb_max_ram = models.CharField(max_length=300, db_index=True, verbose_name='Mb_max_ram')
    more = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='More')
    depend_to = models.CharField(max_length=300, db_index=True, verbose_name='Depend_to')
    depend_to_type = models.CharField(max_length=300, db_index=True, verbose_name='Depend_to_type')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class RAM(models.Model):
    name = models.CharField(max_length=300, db_index=True, verbose_name='Name_ram')
    part_number = models.CharField(max_length=300, db_index=True, verbose_name='Part_number')
    vendor = models.CharField(max_length=300, db_index=True, verbose_name='Vendor')
    f_name = models.CharField(max_length=300, db_index=True, verbose_name='f_name')
    price = models.CharField(max_length=300, db_index=True, verbose_name='Price')
    desc_ukr = models.TextField(db_index=True, verbose_name='Desc_ukr')
    desc_ru = models.TextField(db_index=True, verbose_name='Desc_ru')
    mem_s = models.CharField(max_length=300, db_index=True, verbose_name='Mem_s')
    mem_spd = models.CharField(max_length=300, db_index=True, verbose_name='Mem_spd')
    mem_l = models.CharField(max_length=300, db_index=True, verbose_name='Mem_l')
    more = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='More')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class HDD(models.Model):
    name = models.CharField(max_length=300, db_index=True, verbose_name='Name_hdd')
    part_number = models.CharField(max_length=300, db_index=True, verbose_name='Part_number')
    vendor = models.CharField(max_length=300, db_index=True, verbose_name='Vendor')
    f_name = models.CharField(max_length=300, db_index=True, verbose_name='f_name')
    price = models.CharField(max_length=300, db_index=True, verbose_name='Price')
    desc_ukr = models.TextField(db_index=True, verbose_name='Desc_ukr')
    desc_ru = models.TextField(db_index=True, verbose_name='Desc_ru')
    hdd_s = models.CharField(max_length=300, db_index=True, verbose_name='Hdd_s')
    hdd_spd_ua = models.CharField(max_length=300, db_index=True, verbose_name='Hdd_spd_ua')
    hdd_spd_rus = models.CharField(max_length=300, db_index=True, verbose_name='Hdd_spd_rus')
    hdd_ca = models.CharField(max_length=300, db_index=True, verbose_name='Hdd_ca')
    more = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='More')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class PSU(models.Model):
    name = models.CharField(max_length=300, db_index=True, verbose_name='Name_psu')
    part_number = models.CharField(max_length=300, db_index=True, verbose_name='Part_number')
    vendor = models.CharField(max_length=300, db_index=True, verbose_name='Vendor')
    price = models.CharField(max_length=300, db_index=True, verbose_name='Price')
    desc_ukr = models.TextField(db_index=True, verbose_name='Desc_ukr')
    desc_ru = models.TextField(db_index=True, verbose_name='Desc_ru')
    psu_p = models.CharField(max_length=300, db_index=True, verbose_name='Psu_p')
    psu_c = models.CharField(max_length=300, db_index=True, verbose_name='Psu_c')
    psu_f = models.CharField(max_length=300, db_index=True, verbose_name='Psu_f')
    more = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='More')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class GPU(models.Model):
    name = models.CharField(max_length=300, db_index=True, verbose_name='Name_gpu')
    part_number = models.CharField(max_length=300, db_index=True, verbose_name='Part_number')
    vendor = models.CharField(max_length=300, db_index=True, verbose_name='Vendor')
    main_category = models.CharField(max_length=300, db_index=True, verbose_name='Main_category')
    f_name = models.CharField(max_length=300, db_index=True, verbose_name='f_name')
    price = models.CharField(max_length=300, db_index=True, verbose_name='Price')
    desc_ukr = models.TextField(db_index=True, verbose_name='Desc_ukr')
    desc_ru = models.TextField(db_index=True, verbose_name='Desc_ru')
    gpu_fps = models.CharField(max_length=300, db_index=True, verbose_name='Gpu_fps')
    gpu_m_s = models.CharField(max_length=300, db_index=True, verbose_name='Gpu_m_s')
    gpu_b = models.CharField(max_length=300, db_index=True, verbose_name='Gpu_b')
    gpu_cpu_spd = models.CharField(max_length=300, db_index=True, verbose_name='Gpu_cpu_spd')
    gpu_mem_spd = models.CharField(max_length=300, db_index=True, verbose_name='Gpu_mem_spd')
    more = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='More')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class FAN(models.Model):
    name = models.CharField(max_length=300, db_index=True, verbose_name='Name_fan')
    part_number = models.CharField(max_length=300, db_index=True, verbose_name='Part_number')
    vendor = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='Vendor')
    price = models.CharField(max_length=300, db_index=True, verbose_name='Price')
    desc_ukr = models.TextField(db_index=True, verbose_name='Desc_ukr')
    desc_ru = models.TextField(db_index=True, verbose_name='Desc_ru')
    case_fan_spd_ua = models.CharField(max_length=300, db_index=True, verbose_name='Case_fan_spd_ua')
    case_fan_spd_rus = models.CharField(max_length=300, db_index=True, verbose_name='Case_fan_spd_rus')
    case_fan_noise_level = models.CharField(max_length=300, db_index=True, verbose_name='Case_fan_noise_level')
    case_fan_size = models.CharField(max_length=300, db_index=True, verbose_name='Case_fan_size')
    more = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='More')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class CASE(models.Model):
    name = models.CharField(max_length=300, db_index=True, verbose_name='Name_case')
    part_number = models.CharField(max_length=300, db_index=True, verbose_name='Part_number')
    vendor = models.CharField(max_length=300, db_index=True, verbose_name='Vendor')
    price = models.CharField(max_length=300, db_index=True, verbose_name='Price')
    desc_ukr = models.TextField(db_index=True, verbose_name='Desc_ukr')
    desc_ru = models.TextField(db_index=True, verbose_name='Desc_ru')
    case_s = models.CharField(max_length=300, db_index=True, verbose_name='Case_s')
    more = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='More')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class SSD(models.Model):
    name = models.CharField(max_length=300, db_index=True, verbose_name='Name_ssd')
    part_number = models.CharField(max_length=300, db_index=True, verbose_name='Part_number')
    vendor = models.CharField(max_length=300, db_index=True, verbose_name='Vendor')
    f_name = models.CharField(max_length=300, db_index=True, verbose_name='f_name')
    price = models.CharField(max_length=300, db_index=True, verbose_name='Price')
    desc_ukr = models.TextField(db_index=True, verbose_name='Desc_ukr')
    desc_ru = models.TextField(db_index=True, verbose_name='Desc_ru')
    ssd_s = models.CharField(max_length=300, db_index=True, verbose_name='Ssd_s')
    ssd_spd = models.CharField(max_length=300, db_index=True, verbose_name='Ssd_spd')
    ssd_r_spd = models.CharField(max_length=300, db_index=True, verbose_name='Ssd_r_spd')
    ssd_type_cells = models.CharField(max_length=300, db_index=True, verbose_name='ssd_type_cells')
    more = models.CharField(null=True, blank=True,max_length=300, db_index=True, verbose_name='More')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
