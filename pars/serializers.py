from rest_framework import serializers
from cat.models import *
from descriptions.models import *


dict_change_params = {
                    'Cooler': {
                            'fan_type_ua': 'cool_type_ua',
                            'fan_type_rus': 'cool_type_ru',
                            'fan_noise_level': 'cool_max_no',
                            'fan_size': 'cool_fan_size',
                            'fan_spd_ua': 'cool_fan_min_spd_ua',
                            'fan_spd_rus': 'cool_fan_min_spd_ru',
                            'desc_ukr': 'cool_ai_ua',
                            'desc_ru': 'cool_ai_ru'
                              },
                    'CPU': {
                            'cpu_b_f': 'cpu_bfq',
                            'desc_ukr': 'cpu_ai_ua',
                            'desc_ru': 'cpu_ai_ru',
                            'cpu_cache': 'cpu_cache',
                            'f_name': 'cpu_fam',
                              },
                    'HDD': {
                            'hdd_s': 'hdd_size',
                            'hdd_spd_ua': 'hdd_spd_ph_ua',
                            'hdd_spd_rus': 'hdd_spd_ph_ru',
                            'hdd_ca': 'hdd_buf',
                            'desc_ukr': 'hdd_ai_ua',
                            'desc_ru': 'hdd_ai_ru'
                            },
                    'FAN': {
                            'case_fan_size': 'part_fan_size',
                            'case_fan_spd_ua': 'fan_max_spd_ua',
                            'case_fan_spd_rus': 'fan_max_spd_ru',
                            'desc_ukr': 'fan_ai_ua',
                            'desc_ru': 'fan_ai_ru'
                           },
                    'MB': {
                            'main_category': 'part_mb_fam',
                            'mb_max_ram': 'part_mb_ram_max_size',
                            'mb_chipset': 'part_mb_chip',
                            'desc_ukr': 'part_mb_ai_ua',
                            'desc_ru': 'part_mb_ai_ru',
                            'mb_count_slot': 'part_mb_ram_sl',
                            'mb_type_memory': 'part_mb_ram_type'
                          },
                    'SSD': {
                            'ssd_s': 'ssd_size',
                            'ssd_type_cells': 'ssd_nand',
                            'desc_ukr': 'ssd_ai_ua',
                            'desc_ru': 'ssd_ai_ru'
                           },
                    'PSU': {
                            'psu_p': 'psu_pow',
                            'psu_c': 'psu_80',
                            'psu_f': 'psu_fan',
                            'desc_ukr': 'psu_ai_ua',
                            'desc_ru': 'psu_ai_ru'
                           },
                    'RAM': {
                            'f_name': 'ram_size',
                            'mem_spd': 'ram_fq',
                            'mem_type': 'ram_type',
                            'desc_ukr': 'ram_ai_ua',
                            'desc_ru': 'ram_ai_ru'
                           },
                    'CASE': {
                            'case_s': 'case_type',
                            'desc_ukr': 'case_ai_ua',
                            'desc_ru': 'case_ai_ru',
                            'color_ukr': 'case_color_ua',
                            'color_ru': 'case_color_ru'
                            },
                    'GPU': {
                            'gpu_m_s': 'gpu_mem_size',
                            'gpu_b': 'gpu_bit',
                            'f_name': 'gpu_model',
                            'main_category': 'gpu_main_category',
                            'desc_ukr': 'gpu_ai_ua',
                            'desc_ru': 'gpu_ai_ru',

                           },
                    }

class CompsSerializer(serializers.Serializer):
    name_computers = serializers.CharField(max_length=300)
    url_computers = serializers.CharField(max_length=300)
    price_computers = serializers.CharField(max_length=300)
    proc_computers = serializers.CharField(max_length=300)
    mb_computers = serializers.CharField(max_length=300)
    mem_computers = serializers.CharField(max_length=300)
    video_computers = serializers.CharField(max_length=300)
    hdd_computers = serializers.CharField(max_length=300)
    ps_computers = serializers.CharField(max_length=300)
    case_computers = serializers.CharField(max_length=300)
    cool_computers = serializers.CharField(max_length=300,)
    class_computers = serializers.CharField(max_length=300)
    warranty_computers = serializers.CharField(max_length=300)
    vent_computers = serializers.CharField(max_length=300)
    mem_num_computers = serializers.CharField(max_length=300)
    video_num_computers = serializers.CharField(max_length=300)
    vent_num_computers = serializers.CharField(max_length=300)
    is_active = serializers.BooleanField()
    date_computers = serializers.DateTimeField()
    mon_computers = serializers.CharField(max_length=300)
    wifi_computers = serializers.CharField(max_length=300)
    km_computers = serializers.CharField(max_length=300)
    time_assembly_ru = serializers.CharField(max_length=300)
    time_assembly_ukr = serializers.CharField(max_length=300)

class CoolerSerializer(serializers.Serializer):
    name = serializers.CharField()
    part_number = serializers.CharField()
    vendor = serializers.CharField()
    price = serializers.CharField()
    desc_ukr = serializers.CharField()
    desc_ru = serializers.CharField()
    fan_type_ua = serializers.CharField()
    fan_type_rus = serializers.CharField()
    fan_spd_ua = serializers.CharField()
    fan_spd_rus = serializers.CharField()
    fan_noise_level = serializers.CharField()
    fan_size = serializers.CharField()
    fan_triple_wcs_rus = serializers.CharField()
    fan_triple_wcs_ua = serializers.CharField()
    depend_to = serializers.CharField()
    depend_to_type = serializers.CharField()
    cooler_height = serializers.CharField()
    config = serializers.CharField()
    parent_option = serializers.CharField()
    special_price = serializers.CharField()
    #cover = serializers.ImageField(max_length=None, use_url=True)
    #more = serializers.CharField()
    #is_active = models.BooleanField(default=True)

class CoolerSertest(serializers.ModelSerializer):
    cover = serializers.ImageField(max_length=None, use_url=True)
    class Meta:
        model = Cooler
        fields = ('id', 'name', 'cover',)

class CoolerSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Cooler
        fields = ('name', 'part_number', 'vendor','price', 'desc_ukr', 'desc_ru',
                'fan_type_ua', 'fan_type_rus', 'fan_noise_level', 'fan_size',
                'fan_spd_ua', 'fan_spd_rus')

class Cooler_OTHERSerializer(serializers.ModelSerializer):
    root = CoolerSerializer2(required=True)
    class Meta:
        model = Cooler_OTHER
        fields = (
        'r_price', 'cool_tub_am', 'cool_sock',
        'cool_max_tdp', 'cool_col_ua', 'cool_col_ru', 'cool_rgb', 'cool_h',
        'cool_warr_ua', 'cool_warr_ru', 'you_vid', 'label', 'creditoff', 'root')

class CpuSerializer(serializers.Serializer):
    name = serializers.CharField()
    part_number = serializers.CharField()
    vendor = serializers.CharField()
    price = serializers.CharField()
    desc_ukr = serializers.CharField()
    desc_ru = serializers.CharField()
    f_name = serializers.CharField()
    cpu_c_t = serializers.CharField()
    f_cpu_c_t = serializers.CharField()
    cpu_b_f = serializers.CharField()
    cpu_cache = serializers.CharField()
    cpu_i_g_ua = serializers.CharField()
    cpu_i_g_rus = serializers.CharField()
    #more = serializers.CharField()
    depend_from = serializers.CharField()
    depend_from_type = serializers.CharField()
    cpu_streem = serializers.CharField(source='cpu_streem_ru')
    #cpu_streem_ukr = serializers.CharField()
    cpu_render = serializers.CharField(source='cpu_render_ru')
    config = serializers.CharField()
    parent_option = serializers.CharField()
    special_price = serializers.CharField()
    #cpu_render_ukr = serializers.CharField()

class CpuSerializer2(serializers.ModelSerializer):
    class Meta:
        model = CPU
        fields = ('name', 'part_number', 'vendor','price', 'desc_ukr', 'desc_ru', 'cpu_cache',
        'cpu_b_f', 'f_name')


class CPU_OTHERSerializer(serializers.ModelSerializer):
    root = CpuSerializer2(required=True)
    class Meta:
        model = CPU_OTHER
        fields = (
        'r_price', 'cpu_tbfq',
        'cpu_soc', 'cpu_core', 'cpu_threeds', 'cpu_gpu',
        'cpu_warr_ua', 'cpu_warr_ru',
        'you_vid', 'label', 'creditoff', 'root'
        )

class MbSerializer(serializers.Serializer):
    name = serializers.CharField()
    part_number = serializers.CharField()
    vendor = serializers.CharField()
    main_category = serializers.CharField()
    price = serializers.CharField()
    desc_ukr = serializers.CharField()
    desc_ru = serializers.CharField()
    mb_chipset = serializers.CharField()
    mb_max_ram = serializers.CharField()
    #more = serializers.CharField()
    mb_count_slot = serializers.CharField()
    mb_type_memory = serializers.CharField()
    depend_to = serializers.CharField()
    depend_to_type = serializers.CharField()
    depend_from = serializers.CharField()
    depend_from_type = serializers.CharField()
    config = serializers.CharField()
    parent_option = serializers.CharField()
    special_price = serializers.CharField()

class MbSerializer2(serializers.ModelSerializer):
    class Meta:
        model = MB
        fields = ('name', 'part_number', 'vendor','price', 'desc_ukr', 'desc_ru',
                'main_category', 'mb_max_ram', 'mb_chipset',
                'mb_count_slot', 'mb_type_memory')

class MB_OTHERSerializer(serializers.ModelSerializer):
    root = MbSerializer2(required=True)
    class Meta:
        model = MB_OTHER
        fields = ('r_price','part_mb_sock', 'part_mb_ff',
        'part_mb_ram_max_spd', 'part_mb_rgb_header', 'part_mb_vga', 'part_mb_dvi',
        'part_mb_hdmi', 'part_mb_dp', 'part_mb_usb_type_c', 'part_mb_lan',
        'part_mb_wifi', 'part_mb_bt', 'part_mb_sata',
        'part_mb_m2', 'part_mb_raid',
        'part_mb_warr_ua', 'part_mb_warr_ru', 'you_vid', 'label',
        'creditoff', 'root')

class RamSerializer(serializers.Serializer):
    name = serializers.CharField()
    part_number = serializers.CharField()
    vendor = serializers.CharField()
    f_name = serializers.CharField()
    price = serializers.CharField()
    desc_ukr = serializers.CharField()
    desc_ru = serializers.CharField()
    mem_s = serializers.CharField()
    mem_spd = serializers.CharField()
    mem_l = serializers.CharField()
    depend_from = serializers.CharField()
    depend_from_type = serializers.CharField()
    depend_to = serializers.CharField()
    depend_to_type = serializers.CharField()
    mem_type = serializers.CharField()
    #more = serializers.CharField()
    config = serializers.CharField()
    parent_option = serializers.CharField()
    special_price = serializers.CharField()

class RamSerializer2(serializers.ModelSerializer):
    class Meta:
        model = RAM
        fields = ('name', 'part_number', 'vendor','price', 'desc_ukr', 'desc_ru',
                'f_name', 'mem_spd', 'mem_type')

class RAM_OTHERSerializer(serializers.ModelSerializer):
    root = RamSerializer2(required=True)
    class Meta:
        model = RAM_OTHER
        fields = ('r_price','ram_mod_am',
                'ram_col_ua', 'ram_col_ru', 'ram_warr_ua', 'ram_warr_ru',
                'you_vid', 'label', 'creditoff', 'root')

class HddSerializer(serializers.Serializer):
    name = serializers.CharField()
    part_number = serializers.CharField()
    vendor = serializers.CharField()
    f_name = serializers.CharField()
    price = serializers.CharField()
    desc_ukr = serializers.CharField()
    desc_ru = serializers.CharField()
    hdd_s = serializers.CharField()
    hdd_spd_ua = serializers.CharField()
    hdd_spd_rus = serializers.CharField()
    hdd_ca = serializers.CharField()
    config = serializers.CharField()
    parent_option = serializers.CharField()
    special_price = serializers.CharField()

class HddSerializer2(serializers.ModelSerializer):
    class Meta:
        model = HDD
        fields = ('name', 'part_number', 'vendor','price', 'desc_ukr', 'desc_ru', 'hdd_s',
                'hdd_spd_ua', 'hdd_spd_rus', 'hdd_ca')

class HDD_OTHERSerializer(serializers.ModelSerializer):
  root = HddSerializer2(required=True)
  class Meta:
    model = HDD_OTHER
    fields = ('r_price', 'hdd_ff',
            'hdd_warr_ua', 'hdd_warr_ru',
            'you_vid', 'label', 'creditoff', 'root')

class PsuSerializer(serializers.Serializer):
    name = serializers.CharField()
    part_number = serializers.CharField()
    vendor = serializers.CharField()
    price = serializers.CharField()
    desc_ukr = serializers.CharField()
    desc_ru = serializers.CharField()
    psu_p = serializers.CharField()
    psu_c = serializers.CharField()
    psu_f = serializers.CharField()
    config = serializers.CharField()
    parent_option = serializers.CharField()
    special_price = serializers.CharField()

class PsuSerializer2(serializers.ModelSerializer):
    class Meta:
        model = PSU
        fields = ('name', 'part_number', 'vendor','price', 'desc_ukr', 'desc_ru',
                'psu_p', 'psu_c', 'psu_f')

class PSU_OTHERSerializer(serializers.ModelSerializer):
  root = PsuSerializer2(required=True)
  class Meta:
    model = PSU_OTHER
    fields = ('r_price', 'psu_ff',
    'psu_warr_ua', 'psu_warr_ru',
    'you_vid', 'label', 'creditoff', 'root')

class GpuSerializer(serializers.Serializer):
    name = serializers.CharField()
    part_number = serializers.CharField()
    vendor = serializers.CharField()
    main_category = serializers.CharField()
    f_name = serializers.CharField()
    price = serializers.CharField()
    desc_ukr = serializers.CharField()
    desc_ru = serializers.CharField()
    gpu_fps = serializers.CharField()
    gpu_m_s = serializers.CharField()
    gpu_b = serializers.CharField()
    gpu_cpu_spd = serializers.CharField()
    gpu_mem_spd = serializers.CharField()
    gpu_triple_fan_rus = serializers.CharField()
    gpu_triple_fan_ua = serializers.CharField()
    depend_to = serializers.CharField()
    depend_to_type = serializers.CharField()
    gpu_3d = serializers.CharField(source='gpu_3d_ru')
    #gpu_3d_ukr = serializers.CharField()
    gpu_VR = serializers.CharField(source='gpu_VR_ru')
    #gpu_VR_ukr = serializers.CharField()
    gpu_ref_hd = serializers.CharField()
    #more = serializers.CharField()
    gpu_type_ru = serializers.CharField()
    gpu_type_ukr = serializers.CharField()
    config = serializers.CharField()
    parent_option = serializers.CharField()
    special_price = serializers.CharField()

class GpuSerializer2(serializers.ModelSerializer):
    class Meta:
        model = GPU
        fields = ('name', 'part_number', 'vendor','price', 'desc_ukr', 'desc_ru',
                'gpu_m_s', 'gpu_b', 'f_name', 'main_category')

class GPU_OTHERSerializer(serializers.ModelSerializer):
    root = GpuSerializer2(required=True)
    class Meta:
        model = GPU_OTHER
        fields = ('r_price',
                'gpu_fan', 'gpu_vga', 'gpu_dvi', 'gpu_hdmi', 'gpu_dp',
                'gpu_max_l', 'gpu_warr_ua', 'gpu_warr_ru',
                'you_vid', 'label', 'creditoff', 'root')

class FanSerializer(serializers.Serializer):
    name = serializers.CharField()
    part_number = serializers.CharField()
    vendor = serializers.CharField()
    price = serializers.CharField()
    desc_ukr = serializers.CharField()
    desc_ru = serializers.CharField()
    case_fan_spd_ua = serializers.CharField()
    case_fan_spd_rus = serializers.CharField()
    case_fan_noise_level = serializers.CharField()
    case_fan_size = serializers.CharField()
    config = serializers.CharField()
    parent_option = serializers.CharField()
    special_price = serializers.CharField()

class FanSerializer2(serializers.ModelSerializer):
    class Meta:
        model = FAN
        fields = ('name', 'part_number', 'vendor','price', 'desc_ukr', 'desc_ru',
                'case_fan_size', 'case_fan_spd_ua', 'case_fan_spd_rus')

class FAN_OTHERSerializer(serializers.ModelSerializer):
    root = FanSerializer2(required=True)
    class Meta:
        model = FAN_OTHER
        fields = ('r_price','fan_b_type_ua', 'fan_b_type_ru',
        'fan_pow', 'fan_led_type_ua', 'fan_led_type_ru',
        'fan_col_ua', 'fan_warr_ua', 'fan_warr_ru', 'fan_quantity', 'fan_col_ru',
        'you_vid', 'label', 'creditoff', 'root')

class CaseSerializer(serializers.Serializer):
    name = serializers.CharField()
    part_number = serializers.CharField()
    vendor = serializers.CharField()
    price = serializers.CharField()
    desc_ukr = serializers.CharField()
    desc_ru = serializers.CharField()
    case_s = serializers.CharField()
    color_parent = serializers.CharField()
    color = serializers.CharField()
    color_ukr = serializers.CharField()
    color_ru = serializers.CharField()
    case_wcs_plus_size_ru = serializers.CharField()
    case_wcs_plus_size_ua = serializers.CharField()
    case_gpu_triple_fan_ua = serializers.CharField()
    case_gpu_triple_fan_ru = serializers.CharField()
    case_count_fan = serializers.CharField()
    depend_to = serializers.CharField()
    depend_to_type = serializers.CharField()
    case_height = serializers.CharField()
    config = serializers.CharField()
    parent_option = serializers.CharField()
    special_price = serializers.CharField()

class CaseSerializer2(serializers.ModelSerializer):
    class Meta:
        model = CASE
        fields = ('name', 'part_number', 'vendor','price', 'desc_ukr', 'desc_ru',
        'color_ukr', 'color_ru', 'case_s')


class CASE_OTHERSerializer(serializers.ModelSerializer):
    root = CaseSerializer2(required=True)
    class Meta:
        model = CASE_OTHER
        fields = ('r_price', 'case_psu_p', 'case_psu_w_ua', 'case_psu_w_ru',
        'case_mb', 'case_rgb', 'case_fan',
        'case_sp_m_ua', 'case_sp_m_ru', 'case_warr_ua', 'case_warr_ru',
        'you_vid', 'label', 'creditoff', 'root')

class SsdSerializer(serializers.Serializer):
    name = serializers.CharField()
    part_number = serializers.CharField()
    vendor = serializers.CharField()
    f_name = serializers.CharField()
    price = serializers.CharField()
    desc_ukr = serializers.CharField()
    desc_ru = serializers.CharField()
    ssd_s = serializers.CharField()
    ssd_spd = serializers.CharField()
    ssd_r_spd = serializers.CharField()
    ssd_type_cells = serializers.CharField()
    config = serializers.CharField()
    parent_option = serializers.CharField()
    special_price = serializers.CharField()

class SsdSerializer2(serializers.ModelSerializer):
    class Meta:
        model = SSD
        fields = ('name', 'part_number', 'vendor','price', 'desc_ukr', 'desc_ru',
                'ssd_s', 'ssd_type_cells')

class SSD_OTHERSerializer(serializers.ModelSerializer):
    root = SsdSerializer2(required=True)
    class Meta:
        model = SSD_OTHER
        fields = ('r_price', 'part_ssd_w_spd',
                'ssd_ff', 'ssd_int',
                'ssd_warr_ua', 'ssd_warr_ru', 'part_ssd_r_spd',
                'you_vid', 'label', 'creditoff', 'root')

class CablesSerializer(serializers.Serializer):
    name = serializers.CharField()
    part_number = serializers.CharField()
    vendor = serializers.CharField()
    r_price = serializers.CharField()
    desc_ukr = serializers.CharField()
    desc_ru = serializers.CharField()
    cab_mat_ukr = serializers.CharField()
    cab_mat_ru = serializers.CharField()
    cab_col_ukr = serializers.CharField()
    cab_col_ru = serializers.CharField()
    cab_set = serializers.CharField()
    config = serializers.CharField()
    parent_option = serializers.CharField()
    special_price = serializers.CharField()

class WiFiSerializer(serializers.Serializer):
    name = serializers.CharField()
    part_number = serializers.CharField()
    vendor = serializers.CharField()
    r_price = serializers.CharField()
    price = serializers.CharField()
    desc_ukr = serializers.CharField()
    desc_ru = serializers.CharField()
    net_type_ukr = serializers.CharField()
    net_type_rus = serializers.CharField()
    net_max_spd = serializers.CharField()
    net_stand = serializers.CharField()
    net_int = serializers.CharField()
    config = serializers.CharField()
    parent_option = serializers.CharField()
    special_price = serializers.CharField()

class SoftSerializer(serializers.Serializer):
    name = serializers.CharField()
    part_number = serializers.CharField()
    vendor = serializers.CharField()
    r_price = serializers.CharField()
    price = serializers.CharField()
    desc_ukr = serializers.CharField()
    desc_ru = serializers.CharField()
    soft_type_ukr = serializers.CharField()
    soft_type_ru = serializers.CharField()
    soft_lang_ukr = serializers.CharField()
    soft_lang_ru = serializers.CharField()
    soft_set = serializers.CharField()
    config = serializers.CharField()
    parent_option = serializers.CharField()
    special_price = serializers.CharField()

class PromotionSerializer(serializers.ModelSerializer):
    computers = serializers.PrimaryKeyRelatedField(queryset=Computers.objects.all(), many=True)

    class Meta:
        model = Promotion
        fields = ('id', 'english_prom', 'computers')


class ComputersSerializer2(serializers.ModelSerializer):
    promotion = PromotionSerializer(many=True, read_only=True)
    #prom = serializers.PrimaryKeyRelatedField(queryset=Promotion.objects.all(), many=True)
    promotion_set = serializers.StringRelatedField(many=True)

    class Meta:
        model = Computers
        fields = ('id', 'name_computers', 'promotion', 'promotion_set')

class PromotionNewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = ('english_prom',)

class Pc_assemblyNewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pc_assembly
        fields = ('kind_assembly', 'desc_ru', 'desc_ukr')


class CompNewSerializer(serializers.ModelSerializer):
    promotion_set = PromotionNewSerializer(many=True, read_only=True)
    pc_assembly = Pc_assemblyNewSerializer()

    #margin = serializers.CharField(source='class_computers')
    #special_price = serializers.CharField(source='warranty_computers')

    class Meta:
        model = Computers
        fields = (
        'name_computers', 'proc_computers', 'mb_computers', 'mem_computers',
        'video_computers', 'hdd_computers',
        'ps_computers', 'case_computers', 'cool_computers', 'vent_computers',
        'mem_num_computers', 'video_num_computers', 'vent_num_computers',
        'wifi_computers', 'cables_computers', 'soft_computers', 'you_vid',
        'perm_conf', 'elite_conf', 'time_assembly_ru', 'time_assembly_ukr',
        'pc_assembly', 'promotion_set', 'margin_pk', 'special_price_pk')
        # 'margin', 'special_price' не забудь вставить!!!!
        extra_kwargs = {'promotion_set': {'required': False},
                        'margin_pk': {'source': 'class_computers'},
                        'special_price_pk': {'source': 'warranty_computers'},
                        }
