from rest_framework import serializers
from .models import *

class MediaSerializer(serializers.Serializer):
    file = serializers.FileField()

class CoolerSer(serializers.ModelSerializer):

    class Meta:
        model = Cooler_OTHER
        fields = ('name', 'category_ru', 'category_ua', 'part_number',
        'price_rent', 'provider', 'vendor', 'hotline', 'delivery',
        'cool_type_ua', 'cool_type_ru', 'cool_ai_ua', 'cool_ai_ru',
        'cool_fan_max_spd_ua', 'cool_fan_max_spd_ru',
        'cool_fan_size', 'cool_tub_am', 'cool_sock', 'cool_max_tdp',
        'cool_col_ua', 'cool_col_ru', 'cool_rgb', 'cool_h', 'cool_warr_ua',
        'cool_warr_ru', 'you_vid', 'label', 'creditoff',
        'cover1', 'cover2', 'cover3', 'part_number_web')


class CPUSer(serializers.ModelSerializer):

    class Meta:
        model = CPU_OTHER
        fields = ('name', 'category_ru', 'category_ua', 'part_number',
        'price_rent', 'provider', 'hotline', 'delivery',
        'vendor', 'cpu_ai_ua', 'cpu_ai_ru', 'cpu_fam', 'cpu_bfq',
        'cpu_cache', 'cpu_soc', 'cpu_core', 'cpu_threeds', 'cpu_tbfq',
        'cpu_gpu', 'cpu_warr_ua', 'cpu_warr_ru', 'you_vid', 'label',
        'creditoff', 'cover1', 'cover2', 'cover3', 'part_number_web')


class MBSer(serializers.ModelSerializer):

    class Meta:
        model = MB_OTHER
        fields = ('name', 'category_ru', 'category_ua', 'part_number',
        'price_rent', 'provider', 'hotline', 'delivery',
        'vendor', 'part_mb_fam', 'part_mb_ai_ua', 'part_mb_ai_ru',
        'part_mb_chip', 'part_mb_ram_max_size', 'part_mb_ram_sl',
        'part_mb_ram_type', 'part_mb_sock', 'part_mb_ff',
        'part_mb_rgb_header', 'part_mb_ram_max_spd', 'part_mb_vga',
        'part_mb_dvi', 'part_mb_hdmi', 'part_mb_dp', 'part_mb_lan',
        'part_mb_wifi', 'part_mb_bt', 'part_mb_usb_type_c',
        'part_mb_sata', 'part_mb_m2', 'part_mb_raid', 'part_mb_warr_ua',
        'part_mb_warr_ru', 'you_vid', 'label', 'creditoff',
        'cover1', 'cover2', 'cover3', 'part_number_web')


class RAMSer(serializers.ModelSerializer):

    class Meta:
        model = RAM_OTHER
        fields = ('name', 'category_ru', 'category_ua', 'part_number',
        'price_rent', 'provider', 'hotline', 'delivery',
        'ram_cl', 'ram_led',
        'vendor', 'ram_size', 'ram_ai_ua', 'ram_ai_ru', 'ram_fq',
        'ram_type', 'ram_mod_am', 'ram_col_ua', 'ram_col_ru',
        'ram_warr_ua', 'ram_warr_ru', 'you_vid', 'label', 'creditoff',
        'cover1', 'cover2', 'cover3', 'part_number_web')


class HDDSer(serializers.ModelSerializer):

    class Meta:
        model = HDD_OTHER
        fields = ('name', 'category_ru', 'category_ua', 'part_number',
        'price_rent', 'provider', 'hotline', 'delivery',
        'vendor', 'hdd_ai_ua', 'hdd_ai_ru', 'hdd_size', 'hdd_spd_ph_ua',
        'hdd_spd_ph_ru', 'hdd_buf', 'hdd_ff', 'hdd_warr_ua', 'hdd_warr_ru',
        'you_vid', 'label', 'creditoff',
        'cover1', 'cover2', 'cover3', 'part_number_web')


class PSUSer(serializers.ModelSerializer):

    class Meta:
        model = PSU_OTHER
        fields = ('name', 'category_ru', 'category_ua', 'part_number',
        'price_rent', 'provider', 'hotline', 'delivery', 'psu_mod',
        'vendor', 'psu_pow', 'psu_80', 'psu_fan', 'psu_ai_ua', 'psu_ai_ru',
        'psu_ff', 'psu_warr_ua', 'psu_warr_ru', 'you_vid', 'label', 'creditoff',
        'cover1', 'cover2', 'cover3', 'part_number_web')


class GPUSer(serializers.ModelSerializer):

    class Meta:
        model = GPU_OTHER
        fields = ('name', 'category_ru', 'category_ua', 'part_number',
        'price_rent', 'provider', 'hotline', 'delivery', 'gpu_pci_type',
        'gpu_mem_type', 'gpu_core_fq', 'gpu_mem_fq', 'gpu_watt',
        'vendor', 'gpu_main_category', 'gpu_model', 'gpu_ai_ua',
        'gpu_ai_ru', 'gpu_mem_size', 'gpu_bit', 'gpu_fan',
        'gpu_vga', 'gpu_dvi', 'gpu_hdmi', 'gpu_dp', 'gpu_max_l',
        'gpu_warr_ua', 'gpu_warr_ru', 'you_vid', 'label', 'creditoff',
        'cover1', 'cover2', 'cover3', 'part_number_web')


class FANSer(serializers.ModelSerializer):

    class Meta:
        model = FAN_OTHER
        fields = ('name', 'category_ru', 'category_ua', 'part_number',
        'price_rent', 'provider', 'hotline', 'delivery',
        'vendor', 'fan_ai_ua', 'fan_ai_ru', 'fan_max_spd_ua',
        'fan_max_spd_ru', 'part_fan_size', 'fan_b_type_ua',
        'fan_b_type_ru', 'fan_quantity', 'fan_pow', 'fan_led_type_ua',
        'fan_led_type_ru', 'fan_col_ua', 'fan_col_ru', 'fan_warr_ua',
        'fan_warr_ru', 'you_vid', 'label', 'creditoff',
        'cover1', 'cover2', 'cover3', 'part_number_web')


class CASESer(serializers.ModelSerializer):

    class Meta:
        model = CASE_OTHER
        fields = ('name', 'category_ru', 'category_ua',
        'part_number', 'price_rent', 'provider', 'hotline', 'delivery',
        'vendor', 'case_ai_ua', 'case_ai_ru', 'case_color_ua',
        'case_color_ru', 'case_s', 'case_mb', 'case_psu_p', 'case_psu_w_ua',
        'case_psu_w_ru', 'case_rgb', 'case_fan', 'case_sp_m_ua',
        'case_sp_m_ru', 'case_warr_ua', 'case_warr_ru', 'you_vid',
        'label', 'creditoff', 'cover1', 'cover2', 'cover3', 'part_number_web')


class SSDSer(serializers.ModelSerializer):

    class Meta:
        model = SSD_OTHER
        fields = ('name', 'category_ru', 'category_ua', 'part_number',
        'price_rent', 'provider', 'hotline', 'delivery',
        'vendor', 'ssd_ai_ua', 'ssd_ai_ru', 'ssd_size', 'ssd_nand',
        'ssd_ff', 'ssd_int', 'part_ssd_r_spd', 'part_ssd_w_spd',
        'ssd_warr_ua', 'ssd_warr_ru', 'you_vid', 'label', 'creditoff',
        'cover1', 'cover2', 'cover3', 'part_number_web')


class WiFiSer(serializers.ModelSerializer):

    class Meta:
        model = WiFi_OTHER
        fields = ('name', 'category_ru', 'category_ua',
        'part_number', 'price_rent', 'provider', 'hotline', 'delivery',
        'vendor', 'net_ai_ua', 'net_ai_ru', 'net_type_ukr',
        'net_type_rus', 'net_max_spd', 'net_stand', 'net_int',
        'net_warr_ua', 'net_warr_ru', 'you_vid', 'label', 'creditoff',
        'cover1', 'cover2', 'cover3', 'part_number_web')


class CablesSer(serializers.ModelSerializer):

    class Meta:
        model = Cables_OTHER
        fields = ('name', 'category_ru', 'category_ua',
        'part_number', 'price_rent', 'provider', 'hotline', 'delivery',
        'vendor', 'cab_ai_ua', 'cab_ai_ru', 'cab_mat_ukr',
        'cab_mat_ru', 'cab_col_ukr', 'cab_col_ru', 'cab_set',
        'cab_warr_ua', 'cab_warr_ru', 'you_vid', 'label', 'creditoff',
        'cover1', 'cover2', 'cover3', 'part_number_web')


class SoftSer(serializers.ModelSerializer):

    class Meta:
        model = Soft_OTHER
        fields = ('name', 'category_ru', 'category_ua',
        'part_number', 'price_rent', 'provider', 'hotline', 'delivery',
        'vendor', 'soft_ai_ua', 'soft_ai_ru', 'soft_type_ukr',
        'soft_type_ru', 'soft_lang_ukr', 'soft_lang_ru', 'soft_set',
        'soft_warr_ua', 'soft_warr_ru', 'you_vid', 'label', 'creditoff',
        'cover1', 'cover2', 'cover3', 'part_number_web')
