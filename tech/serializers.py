from rest_framework import serializers
from .models import *

class MediaSerializer(serializers.Serializer):
    file = serializers.FileField()
#
class MonitorsSer(serializers.ModelSerializer):

    class Meta:
        model = Monitors
        fields = ('name', 'category_ru', 'category_ua', 'part_number',
        'price_rent', 'provider', 'vendor', 'hotline', 'delivery',
        'sc_d', 'sc_r', 'sc_t', 'sc_ss', 'sc_l', 'sc_v',
        'sc_b', 'sc_s', 'sc_h', 'sc_surf_ua',
        'sc_surf_ru', 'sc_d_sub', 'sc_dvi', 'sc_hdmi', 'sc_dp',
        'sc_arch', 'sc_spk', 'sc_spk_p', 'sc_spin', 'sc_hight',
        'sc_usb', 'sc_os', 'sc_fi', 'sc_vesa', 'sc_vol',
        'sc_weight', 'sc_col_ua', 'sc_col_ru', 'sc_ai_ua', 'sc_ai_ru',
        'sc_warr_ua', 'sc_warr_ru', 'warranty',
        'you_vid', 'label', 'creditoff',
        'cover1', 'cover2', 'cover3', 'part_number_web')


class KMSer(serializers.ModelSerializer):

    class Meta:
        model = KM
        fields = ('name', 'category_ru', 'category_ua', 'part_number',
        'price_rent', 'provider', 'hotline', 'delivery',
        'vendor', 'km_connect_ua', 'km_connect_ru', 'km_int', 'km_key_type_ua',
        'km_key_type_ru', 'km_k_light', 'km_ua', 'km_pow_k_ua', 'km_pow_k_ru',
        'km_sensor_ua', 'km_sensor_ru', 'km_numb_buttoms', 'km_dpi', 'km_mouse_light',
        'km_pow_mouse_ua', 'km_pow_mouse_ru', 'km_k_vol', 'km_mouse_vol',
        'km_k_weight', 'km_mouse_weight', 'km_col_ua', 'km_col_ru',
        'km_warr_ua', 'km_warr_ru', 'warranty', 'you_vid', 'label',
        'creditoff', 'cover1', 'cover2', 'cover3', 'part_number_web')


class KeyboardsSer(serializers.ModelSerializer):

    class Meta:
        model = Keyboards
        fields = ('name', 'category_ru', 'category_ua', 'part_number',
        'price_rent', 'provider', 'hotline', 'delivery',
        'vendor', 'kb_type_con_ua', 'kb_type_con_ru', 'kb_type_but_ua',
        'kb_type_but_ru', 'kb_type_pow_ua', 'kb_type_pow_ru', 'kb_form_ua',
        'kb_form_ru', 'kb_type_conn', 'kb_plus_but', 'kb_light', 'kb_rgb',
        'kb_res', 'kb_cab_long', 'kb_leng', 'kb_vol',
        'kb_weight', 'kb_usb', 'kb_ps', 'kb_bt', 'kb_usb_resiver',
        'kb_usb_type_c', 'kb_col_ua', 'kb_col_ru', 'kb_warr_ua',
        'kb_warr_ru', 'warranty', 'you_vid', 'label', 'creditoff',
        'cover1', 'cover2', 'cover3', 'part_number_web')


class MousesSer(serializers.ModelSerializer):

    class Meta:
        model = Mouses
        fields = ('name', 'category_ru', 'category_ua', 'part_number',
        'price_rent', 'provider', 'hotline', 'delivery', 'vendor',
        'mouse_type_connect_ua', 'mouse_type_connect_ru',
        'mouse_int', 'mouse_sensor_ua', 'mouse_sensor_ru',
        'mouse_dpi', 'mouse_numb_buttoms', 'mouse_pow_ua',
        'mouse_pow_ru', 'mouse_length_cable', 'mouse_vol',
        'mouse_weight', 'mouse_col_ua', 'mouse_col_ru',
        'mouse_warr_ua', 'mouse_warr_ru', 'warranty', 'you_vid', 'label', 'creditoff',
        'cover1', 'cover2', 'cover3', 'part_number_web')


class PadsSer(serializers.ModelSerializer):

    class Meta:
        model = Pads
        fields = ('name', 'category_ru', 'category_ua', 'part_number',
        'price_rent', 'provider', 'hotline', 'delivery',
        'vendor', 'pad_bot_ua', 'pad_bot_ru', 'pad_vol', 'pad_light',
        'pad_col_ua', 'pad_col_ru', 'pad_warr_ua', 'pad_warr_ru', 'warranty',
        'you_vid', 'label', 'creditoff',
        'cover1', 'cover2', 'cover3', 'part_number_web')


class HeadsetsSer(serializers.ModelSerializer):

    class Meta:
        model = Headsets
        fields = ('name', 'category_ru', 'category_ua', 'part_number',
        'price_rent', 'provider', 'hotline', 'delivery', 'vendor',
        'hs_type_connect_ua', 'hs_type_connect_ru', 'hs_sound_range',
        'hs_resistance', 'hs_purpose_ua', 'hs_purpose_ru',
        'hs_type_ua', 'hs_type_ru', 'hs_s_type_ua', 'hs_s_type_ru',
        'hs_mike_ua', 'hs_mike_ru', 'hs_mike_avail',
        'hs_cable_length', 'hs_interface', 'hs_usb',
        'hs_usb_type_c', 'hs_col_ua', 'hs_col_ru', 'hs_weight',
        'hs_ear_pads_material_ua', 'hs_ear_pads_material_ru',
        'hs_metal_pads_material_ua', 'hs_metal_pads_material_ru',
        'hs_time', 'hs_con_type', 'hs_ver', 'hs_water_res',
        'hs_light', 'hs_pow_ua', 'hs_pow_ru',
        'hs_warr_ua', 'hs_warr_ru', 'warranty', 'you_vid', 'label', 'creditoff',
        'cover1', 'cover2', 'cover3', 'part_number_web')


class WebcamsSer(serializers.ModelSerializer):

    class Meta:
        model = Webcams
        fields = ('name', 'category_ru', 'category_ua', 'part_number',
        'price_rent', 'provider', 'hotline', 'delivery', 'vendor',
        'web_r', 'web_pixel', 'web_type_sensor', 'web_mike',
        'web_focus', 'web_int', 'web_max_f', 'web_angle',
        'web_weight', 'web_col_ua', 'web_col_ru',
        'web_warr_ua', 'web_warr_ru', 'warranty', 'you_vid', 'label', 'creditoff',
        'cover1', 'cover2', 'cover3', 'part_number_web')


class WiFisSer(serializers.ModelSerializer):

    class Meta:
        model = WiFis
        fields = ('name', 'category_ru', 'category_ua', 'part_number',
        'price_rent', 'provider', 'hotline', 'delivery',
        'vendor', 'net_wifi_int', 'net_wifi_ant_am', 'net_wifi_st',
        'net_wifi_ghz', 'net_wifi_max_spd_ua', 'net_wifi_max_spd_ru',
        'net_wifi_bt','net_wifi_warr_ua',
        'net_wifi_warr_ru', 'warranty', 'you_vid', 'label', 'creditoff',
        'cover1', 'cover2', 'cover3', 'part_number_web')


class AcousticsSer(serializers.ModelSerializer):

    class Meta:
        model = Acoustics
        fields = ('name', 'category_ru', 'category_ua',
        'part_number', 'price_rent', 'provider', 'hotline', 'delivery',
        'vendor', 'a_format', 'a_p', 'a_f', 'a_s_n', 'a_audio',
        'a_usb', 'a_eth', 'a_card', 'a_wifi', 'a_bt',
        'a_fm', 'a_control', 'a_pow_ua', 'a_pow_ru',
        'a_bot_ua', 'a_bot_ru', 'a_vol', 'a_weight', 'a_col_ua',
        'a_col_ru', 'a_warr_ua', 'a_warr_ru', 'warranty', 'you_vid',
        'label', 'creditoff', 'cover1', 'cover2', 'cover3', 'part_number_web')


class TablesSer(serializers.ModelSerializer):

    class Meta:
        model = Tables
        fields = ('name', 'category_ru', 'category_ua', 'part_number',
        'price_rent', 'provider', 'hotline', 'delivery',
        'vendor', 'tb_format_ua', 'tb_format_ru', 'tb_led', 'tb_h',
        'tb_angle', 'tb_up', 'tb_in', 'tb_box', 'tb_wheels',
        'tb_cab', 'tb_down', 'tb_bot_t_ua', 'tb_bot_t_ru', 'tb_bot_r_ua',
        'tb_bot_r_ru', 'tb_hight', 'tb_width', 'tb_depth', 'tb_weight',
        'tb_col_ua', 'tb_col_ru',
        'tb_warr_ua', 'tb_warr_ru', 'warranty', 'you_vid', 'label', 'creditoff',
        'cover1', 'cover2', 'cover3', 'part_number_web')


class ChairsSer(serializers.ModelSerializer):

    class Meta:
        model = Chairs
        fields = ('name', 'category_ru', 'category_ua',
        'part_number', 'price_rent', 'provider', 'hotline', 'delivery',
        'vendor', 'ch_type_ua', 'ch_type_ru', 'ch_main_ua',
        'ch_main_ru', 'ch_chr_ua', 'ch_chr_ru', 'ch_mat_ua',
        'ch_mat_ru', 'ch_frame_ua', 'ch_frame_ru', 'ch_vol', 'ch_back',
        'ch_back_angle', 'ch_hand', 'ch_hight', 'ch_mech_ua',
        'ch_mech_ru', 'ch_max_weight', 'ch_weight', 'ch_col_ua', 'ch_col_ru',
        'ch_warr_ua', 'ch_warr_ru', 'warranty', 'you_vid', 'label', 'creditoff',
        'cover1', 'cover2', 'cover3', 'part_number_web')


class AccessoriesSer(serializers.ModelSerializer):

    class Meta:
        model = Accessories
        fields = ('name', 'category_ru', 'category_ua',
        'part_number', 'price_rent', 'provider', 'hotline', 'delivery',
        'vendor', 'acc_type_ua', 'acc_type_ru', 'acc_desc_ua',
        'acc_desc_ru', 'acc_col_ua', 'acc_col_ru',
        'acc_warr_ua', 'acc_warr_ru', 'warranty', 'you_vid', 'label', 'creditoff',
        'cover1', 'cover2', 'cover3', 'part_number_web')


class CabelsplusSer(serializers.ModelSerializer):

    class Meta:
        model = Cabelsplus
        fields = ('name', 'category_ru', 'category_ua',
        'part_number', 'price_rent', 'provider', 'hotline', 'delivery',
        'vendor', 'cab_con_f', 'cab_con_s', 'cab_conn_ua',
        'cab_conn_ru', 'cab_flat', 'cab_tissue', 'cab_metal',
        'cab_g_type', 'cab_ver', 'cab_long', 'cab_color_ua', 'cab_color_ru',
        'cab_warr_ua', 'cab_warr_ru', 'warranty', 'you_vid', 'label', 'creditoff',
        'cover1', 'cover2', 'cover3', 'part_number_web')

class FiltersSer(serializers.ModelSerializer):

    class Meta:
        model = Filters
        fields = ('name', 'category_ru', 'category_ua',
        'part_number', 'price_rent', 'provider', 'hotline', 'delivery',
        'vendor', 'fi_num', 'fi_cab_lenght', 'fi_u',
        'fi_max_i', 'fi_max_pow', 'fi_con',
        'fi_bot_ua', 'fi_bot_ru', 'fi_col_ua', 'fi_col_ru',
        'fi_warr_ua', 'fi_warr_ru', 'warranty', 'you_vid', 'label', 'creditoff',
        'cover1', 'cover2', 'cover3', 'part_number_web')


class OthersSer(serializers.ModelSerializer):

    class Meta:
        model = Others
        fields = ('name', 'category_ru', 'category_ua',
        'part_number', 'price_rent', 'provider', 'hotline', 'delivery',
        'vendor', 'oth_type_ua', 'oth_type_ru', 'oth_desc_ua',
        'oth_desc_ru',
        'oth_warr_ua', 'oth_warr_ru', 'warranty', 'you_vid', 'label', 'creditoff',
        'cover1', 'cover2', 'cover3', 'part_number_web')
