from cat.models import *
from descriptions.models import *
import re
#providerprice_parts
dict_kind = {186: 'proc', 187: '-mb',189: 'video',190: 'hdd',188: 'ram',61: 'ssd',193:'-case',351: 'ps',303: '-cooler,-vent'}

dict_kind_id = {'cpu': (186, "cpu_edition(dict_, art)"),
                'mb': (187, "mb_edition(dict_, art)"),
                'gpu': (189, "gpu_edition(dict_, art)"),
                'hdd': (190, "hdd_edition(dict_, art)"),
                'ram': (188, "mem_edition(dict_, art)"),
                'ssd': (61, "ssd_edition(dict_, art)"),
                'case': (193, "case_edition(dict_, art)"),
                'psu': (351, "psu_edition(dict_, art)"),
                'cooler': (303, "cooler_edition(dict_, art)"),
                'fan': (303, "fan_edition(dict_, art)")}

dict_kind_key = {'ram': "mem_create(dict_for_db, key_)",
                'cpu': "cpu_create(dict_for_db, key_)",
                'cooler': "cooler_create(dict_for_db, key_)",
                'mb': "mb_create(dict_for_db, key_)",
                'hdd': "hdd_create(dict_for_db, key_)",
                'ssd': "ssd_create(dict_for_db, key_)",
                'gpu': "gpu_create(dict_for_db, key_)",
                'fan': "fan_create(dict_for_db, key_)",
                'psu': "psu_create(dict_for_db, key_)",
                'case': "case_create(dict_for_db, key_)",
                }

dict_form = {
            'ram':"Ram_otherForm(initial={'name':n.name, 'part_number':n.part_number, 'vendor':n.vendor, 'price':n.price, 'desc_ukr': n.desc_ukr, 'desc_ru':n.desc_ru, 'ram_size':n.f_name, 'ram_type': n.root_other.ram_type, 'r_price': n.root_other.r_price,'ram_fq': n.mem_spd, 'ram_mod_am': n.root_other.ram_mod_am, 'ram_cl': n.root_other.ram_cl, 'ram_xmp': n.root_other.ram_xmp, 'ram_pow': n.root_other.ram_pow, 'ram_cool_ua': n.root_other.ram_cool_ua, 'ram_cool_ru': n.root_other.ram_cool_ru, 'ram_col_ua': n.root_other.ram_col_ua, 'ram_col_ru': n.root_other.ram_col_ru, 'ram_led': n.root_other.ram_led, 'ram_warr_ua': n.root_other.ram_warr_ua, 'ram_warr_ru': n.root_other.ram_warr_ru, 'ram_ai_ua': n.root_other.ram_ai_ua, 'ram_ai_ru': n.root_other.ram_ai_ru, 'you_vid': n.root_other.you_vid, 'label': n.root_other.label,'creditoff': n.root_other.creditoff})",
            'cpu':"CPU_otherForm(initial={'name':n.name, 'part_number':n.part_number, 'vendor':n.vendor, 'price':n.price, 'desc_ukr': n.desc_ukr, 'desc_ru':n.desc_ru, 'cpu_fam':n.root_other.cpu_fam, 'r_price': n.root_other.r_price, 'cpu_bfq': n.cpu_b_f, 'cpu_cache': n.cpu_cache,'cpu_core_name': n.root_other.cpu_core_name, 'cpu_soc': n.root_other.cpu_soc, 'cpu_core': n.root_other.cpu_core, 'cpu_threeds': n.root_other.cpu_threeds, 'cpu_warr_ua': n.root_other.cpu_warr_ua, 'cpu_warr_ru': n.root_other.cpu_warr_ru, 'you_vid': n.root_other.you_vid, 'label': n.root_other.label, 'cpu_tbfq': n.root_other.cpu_tbfq, 'cpu_nm': n.root_other.cpu_nm, 'cpu_tdp': n.root_other.cpu_tdp, 'cpu_max_temp': n.root_other.cpu_max_temp, 'cpu_gpu': n.root_other.cpu_gpu, 'cpu_max_ram': n.root_other.cpu_max_ram, 'cpu_cha': n.root_other.cpu_cha, 'cpu_bot': n.root_other.cpu_bot, 'creditoff': n.root_other.creditoff,'cpu_ai_ua': n.root_other.cpu_ai_ua, 'cpu_ai_ru': n.root_other.cpu_ai_ru, 'cpu_gpu_model': n.root_other.cpu_gpu_model})",
            'cooler':"Cooler_otherForm(initial={'name':n.name, 'part_number':n.part_number, 'vendor':n.vendor, 'price':n.price, 'desc_ukr': n.desc_ukr, 'desc_ru':n.desc_ru, 'cool_type_ua':n.fan_type_ua, 'cool_type_ru': n.fan_type_rus, 'cool_fan_min_spd_ua': n.root_other.cool_fan_min_spd_ua,'cool_fan_min_spd_ru': n.root_other.cool_fan_min_spd_ru, 'cool_fan_max_spd_ua': n.root_other.cool_fan_max_spd_ua, 'cool_fan_max_spd_ru': n.root_other.cool_fan_max_spd_ru, 'cool_min_no': n.root_other.cool_min_no, 'cool_max_no': n.fan_noise_level, 'cool_fan_size': n.fan_size, 'cool_fan_am': n.root_other.cool_fan_am, 'cool_tub_am': n.root_other.cool_tub_am, 'cool_tub_con_ru': n.root_other.cool_tub_con_ru, 'cool_tub_con_ua': n.root_other.cool_tub_con_ua, 'cool_rad_mat_ru': n.root_other.cool_rad_mat_ru, 'cool_rad_mat_ua': n.root_other.cool_rad_mat_ua, 'you_vid': n.root_other.you_vid, 'label': n.root_other.label, 'cool_fix_ru': n.root_other.cool_fix_ru, 'cool_fix_ua': n.root_other.cool_fix_ua, 'cool_sock': n.root_other.cool_sock, 'cool_fan_b_t_ru': n.root_other.cool_fan_b_t_ru, 'cool_fan_b_t_ua': n.root_other.cool_fan_b_t_ua, 'cool_fan_max_af': n.root_other.cool_fan_max_af, 'cool_pwm': n.root_other.cool_pwm, 'cool_max_tdp': n.root_other.cool_max_tdp, 'creditoff': n.root_other.creditoff, 'cool_conn': n.root_other.cool_conn, 'cool_col': n.root_other.cool_col, 'cool_h': n.root_other.cool_h, 'cool_w': n.root_other.cool_w, 'cool_ai_ua': n.root_other.cool_ai_ua, 'cool_ai_ru': n.root_other.cool_ai_ru, 'cool_warr_ua': n.root_other.cool_warr_ua, 'cool_warr_ru': n.root_other.cool_warr_ru, 'r_price': n.root_other.r_price})",
            'mb':"MB_otherForm(initial={'name':n.name, 'part_number':n.part_number, 'vendor':n.vendor, 'price':n.price, 'desc_ukr': n.desc_ukr, 'desc_ru':n.desc_ru, 'part_mb_fam':n.main_category, 'part_mb_ff': n.depend_from, 'part_mb_sock': n.root_other.part_mb_sock,'part_mb_ram_type': n.root_other.part_mb_ram_type, 'part_mb_ram_sl': n.root_other.part_mb_ram_sl, 'part_mb_ram_ch': n.root_other.part_mb_ram_ch, 'part_mb_ram_max_spd': n.root_other.part_mb_ram_max_spd, 'part_mb_pow_ph': n.root_other.part_mb_pow_ph, 'part_mb_vga': n.root_other.part_mb_vga, 'part_mb_dvi': n.root_other.part_mb_dvi, 'part_mb_hdmi': n.root_other.part_mb_hdmi, 'part_mb_dp': n.root_other.part_mb_dp, 'part_mb_sound_ch': n.root_other.part_mb_sound_ch, 'part_mb_sound_chip': n.root_other.part_mb_sound_chip, 'part_mb_lan': n.root_other.part_mb_lan, 'you_vid': n.root_other.you_vid, 'label': n.root_other.label, 'part_mb_wifi': n.root_other.part_mb_wifi, 'part_mb_bt': n.root_other.part_mb_bt, 'part_mb_lan_chip': n.root_other.part_mb_lan_chip, 'part_mb_sata': n.root_other.part_mb_sata, 'part_mb_m2': n.root_other.part_mb_m2, 'part_mb_raid': n.root_other.part_mb_raid, 'part_mb_sl_x1': n.root_other.part_mb_sl_x1, 'part_mb_sl_x16': n.root_other.part_mb_sl_x16,'part_mb_chip': n.depend_to,'part_mb_ram_max_size': n.mb_max_ram, 'creditoff': n.root_other.creditoff, 'part_mb_main_conn': n.root_other.part_mb_main_conn, 'part_mb_cpu_conn': n.root_other.part_mb_cpu_conn, 'part_mb_fan_conn': n.root_other.part_mb_fan_conn, 'part_mb_ai_ua': n.root_other.part_mb_ai_ua, 'part_mb_ai_ru': n.root_other.part_mb_ai_ru, 'part_mb_warr_ua': n.root_other.part_mb_warr_ua, 'part_mb_warr_ru': n.root_other.part_mb_warr_ru, 'r_price': n.root_other.r_price})",
            'hdd':"HDD_otherForm(initial={'name':n.name, 'part_number':n.part_number, 'vendor':n.vendor, 'price':n.price, 'desc_ukr': n.desc_ukr, 'desc_ru':n.desc_ru, 'hdd_size':n.hdd_s, 'hdd_spd_ph_ru': n.hdd_spd_rus, 'r_price': n.root_other.r_price,'hdd_spd_ph_ua': n.hdd_spd_ua, 'hdd_buf': n.hdd_ca, 'hdd_type1_ua': n.root_other.hdd_type1_ua, 'hdd_type1_ru': n.root_other.hdd_type1_ru, 'hdd_type2_ru': n.root_other.hdd_type2_ru, 'hdd_type2_ua': n.root_other.hdd_type2_ua, 'hdd_ff': n.root_other.hdd_ff, 'hdd_int': n.root_other.hdd_int, 'hdd_warr_ua': n.root_other.hdd_warr_ua, 'hdd_warr_ru': n.root_other.hdd_warr_ru, 'hdd_ai_ua': n.root_other.hdd_ai_ua, 'hdd_ai_ru': n.root_other.hdd_ai_ru, 'you_vid': n.root_other.you_vid, 'label': n.root_other.label, 'creditoff': n.root_other.creditoff})",
            'ssd':"SSD_otherForm(initial={'name':n.name, 'part_number':n.part_number, 'vendor':n.vendor, 'price':n.price, 'desc_ukr': n.desc_ukr, 'desc_ru':n.desc_ru, 'ssd_size': n.ssd_s, 'r_price': n.root_other.r_price,'ssd_nand': n.ssd_type_cells, 'ssd_type1_ua': n.root_other.ssd_type1_ua, 'ssd_type1_ru': n.root_other.ssd_type1_ru, 'ssd_type2_ru': n.root_other.ssd_type2_ru, 'ssd_type2_ua': n.root_other.ssd_type2_ua, 'ssd_ff': n.root_other.ssd_ff, 'ssd_int': n.root_other.ssd_int, 'ssd_warr_ua': n.root_other.ssd_warr_ua, 'ssd_warr_ru': n.root_other.ssd_warr_ru, 'ssd_ai_ua': n.root_other.ssd_ai_ua, 'ssd_ai_ru': n.root_other.ssd_ai_ru, 'you_vid': n.root_other.you_vid, 'label': n.root_other.label, 'creditoff': n.root_other.creditoff, 'ssd_con_type': n.root_other.ssd_con_type, 'part_ssd_w_spd': n.root_other.part_ssd_w_spd, 'part_ssd_r_spd': n.root_other.part_ssd_r_spd})",
            'gpu':"GPU_otherForm(initial={'name':n.name, 'part_number':n.part_number, 'vendor':n.vendor, 'price':n.price, 'desc_ukr': n.desc_ukr, 'desc_ru':n.desc_ru, 'gpu_mem_size':n.gpu_m_s, 'part_gpu_gpu_spd': n.gpu_cpu_spd, 'r_price': n.root_other.r_price,'gpu_bit': n.gpu_b, 'gpu_mem_type': n.root_other.gpu_mem_type, 'part_gpu_mem_spd': n.gpu_mem_spd, 'gpu_model': n.root_other.gpu_model, 'gpu_watt': n.root_other.gpu_watt, 'gpu_max_sc': n.root_other.gpu_max_sc, 'gpu_vga': n.root_other.gpu_vga, 'gpu_dvi': n.root_other.gpu_dvi, 'gpu_hdmi': n.root_other.gpu_hdmi, 'gpu_dp': n.root_other.gpu_dp, 'gpu_warr_ua': n.root_other.gpu_warr_ua, 'gpu_warr_ru': n.root_other.gpu_warr_ru, 'gpu_ai_ua': n.root_other.gpu_ai_ua, 'gpu_ai_ru': n.root_other.gpu_ai_ru, 'you_vid': n.root_other.you_vid, 'label': n.root_other.label, 'gpu_cool_ua': n.root_other.gpu_cool_ua, 'gpu_cool_ru': n.root_other.gpu_cool_ru, 'gpu_sl': n.root_other.gpu_sl, 'gpu_max_l': n.root_other.gpu_max_l, 'gpu_lp': n.root_other.gpu_lp, 'creditoff': n.root_other.creditoff})",
            'fan':"FAN_otherForm(initial={'name':n.name, 'part_number':n.part_number, 'vendor':n.vendor, 'price':n.price, 'desc_ukr': n.desc_ukr, 'desc_ru':n.desc_ru, 'part_fan_size':n.case_fan_size, 'fan_max_no': n.case_fan_noise_level, 'r_price': n.root_other.r_price,'fan_b_type_ua': n.root_other.fan_b_type_ua, 'fan_b_type_ru': n.root_other.fan_b_type_ru, 'fan_min_spd_ua': n.root_other.fan_min_spd_ua, 'fan_min_spd_ru': n.root_other.fan_min_spd_ru, 'fan_max_spd_ua': n.root_other.fan_max_spd_ua, 'fan_max_spd_ru': n.root_other.fan_max_spd_ru, 'fan_pwm': n.root_other.fan_pwm, 'fan_pow': n.root_other.fan_pow, 'fan_led_type_ua': n.root_other.fan_led_type_ua, 'fan_led_type_ru': n.root_other.fan_led_type_ru, 'fan_warr_ua': n.root_other.fan_warr_ua, 'fan_warr_ru': n.root_other.fan_warr_ru, 'fan_ai_ua': n.root_other.fan_ai_ua, 'fan_ai_ru': n.root_other.fan_ai_ru, 'you_vid': n.root_other.you_vid, 'label': n.root_other.label, 'fan_max_af': n.root_other.fan_max_af, 'creditoff': n.root_other.creditoff})",
            'psu':"PSU_otherForm(initial={'name':n.name, 'part_number':n.part_number, 'vendor':n.vendor, 'price':n.price, 'desc_ukr': n.desc_ukr, 'desc_ru':n.desc_ru, 'psu_pow':n.psu_p, 'psu_80': n.psu_c, 'r_price': n.root_other.r_price,'psu_fan': n.psu_f, 'psu_ff': n.root_other.psu_ff, 'psu_pfc': n.root_other.psu_pfc, 'psu_no': n.root_other.psu_no, 'psu_main_conn': n.root_other.psu_main_conn, 'psu_gpu_conn': n.root_other.psu_gpu_conn, 'psu_sata_conn': n.root_other.psu_sata_conn, 'psu_molex_conn': n.root_other.psu_molex_conn, 'psu_mod_ua': n.root_other.psu_mod_ua, 'psu_mod_ru': n.root_other.psu_mod_ru, 'psu_warr_ua': n.root_other.psu_warr_ua, 'psu_warr_ru': n.root_other.psu_warr_ru, 'psu_ai_ua': n.root_other.psu_ai_ua, 'psu_ai_ru': n.root_other.psu_ai_ru, 'you_vid': n.root_other.you_vid, 'label': n.root_other.label, 'psu_sl': n.root_other.psu_sl, 'creditoff': n.root_other.creditoff})",
            'case':"CASE_otherForm(initial={'name':n.name, 'part_number':n.part_number, 'vendor':n.vendor, 'case_mb':n.depend_to, 'price':n.price, 'desc_ukr':n.desc_ukr, 'desc_ru':n.desc_ru, 'case_type':n.case_s, 'case_psu_p':n.root_other.case_psu_p, 'case_psu_w_ua':n.root_other.case_psu_w_ua, 'case_psu_w_ru':n.root_other.case_psu_w_ru, 'case_5_с':n.root_other.case_5_с, 'case_3_с':n.root_other.case_3_с, 'case_2_с':n.root_other.case_2_с, 'case_e_с':n.root_other.case_e_с, 'case_fan_f':n.root_other.case_fan_f, 'case_fan_t':n.root_other.case_fan_t, 'case_fan_b':n.root_other.case_fan_b, 'case_pan_f':n.root_other.case_pan_f, 'case_pan_t':n.root_other.case_pan_t, 'case_pan_b':n.root_other.case_pan_b, 'case_front_usb':n.root_other.case_front_usb, 'case_front_h':n.root_other.case_front_h, 'case_front_m':n.root_other.case_front_m, 'case_front_l':n.root_other.case_front_l, 'case_size':n.root_other.case_size, 'case_weight':n.root_other.case_weight, 'case_fp_m_ua':n.root_other.case_fp_m_ua, 'case_fp_m_ru':n.root_other.case_fp_m_ru, 'case_sp_m_ua':n.root_other.case_sp_m_ua, 'case_sp_m_ru':n.root_other.case_sp_m_ru, 'case_sh_m_ua':n.root_other.case_sh_m_ua, 'case_sh_m_ru':n.root_other.case_sh_m_ru, 'case_os_ua':n.root_other.case_os_ua, 'case_os_ru':n.root_other.case_os_ru, 'case_color_ua':n.root_other.case_color_ua, 'case_color_ru':n.root_other.case_color_ru, 'case_max_cpu':n.root_other.case_max_cpu, 'case_max_gpu':n.root_other.case_max_gpu, 'case_cm':n.root_other.case_cm, 'case_df':n.root_other.case_df, 'case_warr_ua':n.root_other.case_warr_ua, 'case_warr_ru':n.root_other.case_warr_ru, 'case_ai_ua':n.root_other.case_ai_ua, 'case_ai_ru':n.root_other.case_ai_ru, 'you_vid':n.root_other.you_vid, 'label':n.root_other.label, 'creditoff':n.root_other.creditoff, 'r_price': n.root_other.r_price})",
            }

dict_base = {
            'cpu':'CPU.objects.filter(root_other__isnull=False)',
            'cooler':'Cooler.objects.filter(root_other__isnull=False)',
            'mb':'MB.objects.filter(root_other__isnull=False)',
            'ram':'RAM.objects.filter(root_other__isnull=False)',
            'hdd':'HDD.objects.filter(root_other__isnull=False)',
            'ssd':'SSD.objects.filter(root_other__isnull=False)',
            'gpu':'GPU.objects.filter(root_other__isnull=False)',
            'psu':'PSU.objects.filter(root_other__isnull=False)',
            'fan':'FAN.objects.filter(root_other__isnull=False)',
            'case':'CASE.objects.filter(root_other__isnull=False)',
            '-':'CPU.objects.filter(root_other__isnull=False)',
            #'wifi':WiFi.objects.all(),
            #'cables':Cables.objects.all(),
            #'soft':Soft.objects.all()
            }

dict_v3 =    {
            'cpu':'CPU.objects.get(pk=id_other)',
            'cooler':'Cooler.objects.get(pk=id_other)',
            'mb':'MB.objects.get(pk=id_other)',
            'ram':'RAM.objects.get(pk=id_other)',
            'hdd':'HDD.objects.get(pk=id_other)',
            'ssd':'SSD.objects.get(pk=id_other)',
            'gpu':'GPU.objects.get(pk=id_other)',
            'psu':'PSU.objects.get(pk=id_other)',
            'fan':'FAN.objects.get(pk=id_other)',
            'case':'CASE.objects.get(pk=id_other)',
            #'wifi':'WiFi.objects.get(pk=id)',
            #'cables':'Cables.objects.get(pk=id)',
            #'soft':'Soft.objects.get(pk=id)'
            }

def case_edition(dict_, art):
    case_dict = {
                'Mini Tower': 'ITX,mATX',
                'Midi Tower': 'ITX,mATX,ATX',
                'Desktop': 'ITX'
                }
    vendor_set = {'DarkFlash', 'Vinga', 'Logicpower', 'Be quiet', 'Chieftec', '2E', 'Frontier', 'Gigabyte', 'MSI',
                'Frime', '1stPlayer', 'Corsair', 'Aerocool', 'Gamemax', 'Deepcool', 'Fractal Design',
                'NZXT', 'ThermalTake', 'Xigmatek', 'Raidmax', 'Cooler Master', 'Tecware', 'Cougar'}
    dict_for_db = {}
    dict_for_db['part_number'] = art
    title = dict_['титл'] if 'титл' in dict_ else ''
    for v in vendor_set:
        if title.lower().find(v.lower()) != -1:
            dict_for_db['vendor'] = v
    if 'vendor' not in dict_for_db:
        dict_for_db['vendor'] = ''
    dict_for_db['name'] = re.sub(r'\W',' ',title)
    dict_for_db['desc_ukr'] = CASE.objects.first().desc_ukr if CASE.objects.first() else ''
    dict_for_db['desc_ru'] = CASE.objects.first().desc_ru if CASE.objects.first() else ''
    dict_for_db['case_type'] = dict_['Форм фактор корпуса'] if 'Форм фактор корпуса' in dict_ else ''
    if dict_for_db['case_type'] and dict_for_db['case_type'] in case_dict:
        dict_for_db['case_mb'] = case_dict[dict_for_db['case_type']]
    else:
        dict_for_db['case_mb'] = '-'
    dict_for_db['case_psu_p'] = dict_['Мощность БП'] if 'Мощность БП' in dict_ else '-'
    dict_for_db['case_front_usb'] = dict_['Лицевая панель'] if 'Лицевая панель' in dict_ else '-'
    dict_for_db['case_front_h'] = '+'
    dict_for_db['case_front_m'] = '+'
    dict_for_db['case_front_l'] = 'Power,HDD'
    dict_for_db['depend_to_type'] = 'case'
    if re.findall(r'(\S+)$', title):
        dict_for_db['case_color_ua'] = dict_for_db['case_color_ru'] = re.findall(r'(\S+)$', title)[0]
    else:
        dict_for_db['case_color_ua'] = dict_for_db['case_color_ru'] = '-'
    dict_for_db['case_5_с'] = dict_['Отсеков 5 25 '] if 'Отсеков 5 25 ' in dict_ else '-'
    dict_for_db['case_3_с'] = dict_['Внутренних отсеков 3 5 '] if 'Внутренних отсеков 3 5 ' in dict_ else '-'
    dict_for_db['case_2_с'] = dict_['Внутренних отсеков 2 5 '] if 'Внутренних отсеков 2 5 ' in dict_ else '-'

    return dict_for_db

def case_create(dict_mem, key_, update=False):
    count_obj = 0
    if dict_mem['part_number'] and not PSU.objects.filter(part_number=dict_mem['part_number']) and update == False:
        case = CASE.objects.create(name=dict_mem['name'], part_number=dict_mem['part_number'],
        vendor=dict_mem['vendor'], price=0,desc_ukr=dict_mem['desc_ukr'], desc_ru=dict_mem['desc_ru'],
        case_s=dict_mem['case_type'], depend_to=dict_mem['case_mb'],
        depend_to_type=dict_mem['depend_to_type'], is_active = True)

        if key_ in ('other_parts', 'both'):
            root_other = CASE_OTHER.objects.create(root=case,
            r_price=0, case_psu_p=dict_mem['case_psu_p'],
            case_5_с=dict_mem['case_5_с'],
            case_3_с=dict_mem['case_3_с'],case_2_с=dict_mem['case_2_с'],
            case_front_usb=dict_mem['case_front_usb'],
            case_front_h=dict_mem['case_front_h'],case_front_m=dict_mem['case_front_m'],
            case_front_l=dict_mem['case_front_l'],
            case_color_ua=dict_mem['case_color_ua'],
            case_color_ru=dict_mem['case_color_ru'])
            if key_ == 'other_parts':
                case.is_active = False
                case.save()
        return (count_obj, case.pk)

    if dict_mem['part_number'] and CASE.objects.filter(part_number=dict_mem['part_number']).exists() and update == False:
        try:
            case = CASE.objects.get(part_number=dict_mem['part_number'])
        except:
            case = CASE.objects.filter(part_number=dict_mem['part_number']).first()
            count_obj = CASE.objects.filter(part_number=dict_mem['part_number']).count()

        if key_ in ('other_parts', 'both'):
            try:
                test = case.root_other
            except:
                root_other = CASE_OTHER.objects.create(root=case,
                r_price=0, case_psu_p=dict_mem['case_psu_p'],
                case_5_с=dict_mem['case_5_с'],
                case_3_с=dict_mem['case_3_с'],case_2_с=dict_mem['case_2_с'],
                case_front_usb=dict_mem['case_front_usb'],
                case_front_h=dict_mem['case_front_h'],case_front_m=dict_mem['case_front_m'],
                case_front_l=dict_mem['case_front_l'],
                case_sh_m_ru=dict_mem['case_sh_m_ru'],
                case_color_ua=dict_mem['case_color_ua'],
                case_color_ru=dict_mem['case_color_ru'])
        return (count_obj, case.pk)
    if update == True:
        c = CASE.objects.get(name=dict_mem['name'])
        c.part_number=dict_mem['part_number']
        c.vendor=dict_mem['vendor']
        c.price=dict_mem['price']
        c.desc_ukr=dict_mem['desc_ukr']
        c.desc_ru=dict_mem['desc_ru']
        c.depend_to=dict_mem['case_mb']
        c.case_s=dict_mem['case_type']
        c.save()

        other = c.root_other

        other.r_price = dict_mem['r_price']
        other.case_psu_p = dict_mem['case_psu_p']
        other.case_psu_w_ua = dict_mem['case_psu_w_ua']
        other.case_psu_w_ru = dict_mem['case_psu_w_ru']
        other.case_5_с = dict_mem['case_5_с']
        other.case_3_с = dict_mem['case_3_с']
        other.case_2_с = dict_mem['case_2_с']
        other.case_e_с = dict_mem['case_e_с']
        other.case_fan_f = dict_mem['case_fan_f']
        other.case_fan_t = dict_mem['case_fan_t']
        other.case_fan_b = dict_mem['case_fan_b']
        other.case_pan_f = dict_mem['case_pan_f']
        other.case_pan_t = dict_mem['case_pan_t']
        other.case_pan_b = dict_mem['case_pan_b']
        other.case_front_usb = dict_mem['case_front_usb']
        other.case_front_h = dict_mem['case_front_h']
        other.case_front_m = dict_mem['case_front_m']
        other.case_front_l = dict_mem['case_front_l']
        other.case_size = dict_mem['case_size']
        other.case_weight = dict_mem['case_weight']
        other.case_fp_m_ua = dict_mem['case_fp_m_ua']
        other.case_fp_m_ru = dict_mem['case_fp_m_ru']
        other.case_sp_m_ua = dict_mem['case_sp_m_ua']
        other.case_sp_m_ru = dict_mem['case_sp_m_ru']
        other.case_sh_m_ua = dict_mem['case_sh_m_ua']
        other.case_sh_m_ru = dict_mem['case_sh_m_ru']
        other.case_os_ua = dict_mem['case_os_ua']
        other.case_os_ru = dict_mem['case_os_ru']
        other.case_color_ua = dict_mem['case_color_ua']
        other.case_color_ru = dict_mem['case_color_ru']
        other.case_max_cpu = dict_mem['case_max_cpu']
        other.case_max_gpu = dict_mem['case_max_gpu']
        other.case_cm = dict_mem['case_cm']
        other.case_df = dict_mem['case_df']
        other.case_warr_ua = dict_mem['case_warr_ua']
        other.case_warr_ru = dict_mem['case_warr_ru']
        other.case_ai_ua = dict_mem['case_ai_ua']
        other.case_ai_ru = dict_mem['case_ai_ru']
        other.you_vid = dict_mem['you_vid']
        other.label = dict_mem['label']
        other.creditoff = dict_mem['creditoff']
        other.save()

        return (count_obj, c.pk)

    return (count_obj, None)

def psu_edition(dict_, art):
    vendor_set = {'DarkFlash', 'Vinga', 'Logicpower', 'Be quiet', 'Chieftec',
                'Frime', '1stPlayer', 'Corsair', 'Aerocool', 'Gamemax', 'Deepcool'}
    dict_for_db = {}
    dict_for_db['part_number'] = art
    title = dict_['титл'] if 'титл' in dict_ else ''
    for v in vendor_set:
        if title.lower().find(v.lower()) != -1:
            dict_for_db['vendor'] = v
    if 'vendor' not in dict_for_db:
        dict_for_db['vendor'] = ''
    dict_for_db['name'] = re.sub(r'\W',' ',title)
    dict_for_db['desc_ukr'] = PSU.objects.first().desc_ukr if PSU.objects.first() else ''
    dict_for_db['desc_ru'] = PSU.objects.first().desc_ru if PSU.objects.first() else ''
    dict_for_db['psu_pow'] = dict_['Мощность'] if 'Мощность' in dict_ else ''
    dict_for_db['psu_80'] = dict_['Сертификат'] if 'Сертификат' in dict_ else '-'
    dict_for_db['psu_fan'] = '1x' + dict_['Диаметр вентилятора'] if 'Диаметр вентилятора' in dict_ else ''
    dict_for_db['psu_ff'] = dict_['Форм фактор'] if 'Форм фактор' in dict_ else '-'
    dict_for_db['psu_pfc'] = dict_['КПД'] if 'КПД' in dict_ else '-'
    dict_for_db['psu_no'] = '-'
    dict_for_db['psu_main_conn'] = dict_['Питание MB CPU'] if 'Питание MB CPU' in dict_ else '-'
    dict_for_db['psu_gpu_conn'] = dict_['PCI E 8pin 6 2 '] if 'PCI E 8pin 6 2 ' in dict_ else '-'
    dict_for_db['psu_sata_conn'] = dict_['SATA'] if 'SATA' in dict_ else '-'
    dict_for_db['psu_molex_conn'] = dict_['MOLEX'] if 'MOLEX' in dict_ else '-'
    dict_for_db['psu_mod_ru'] = dict_['Система кабелей'] if 'Система кабелей' in dict_ else '-'
    dict_for_db['psu_mod_ua'] = 'модульне' if dict_for_db['psu_mod_ru'] == 'модульная' else 'не модульне'
    dict_for_db['psu_sl'] = '-'

    return dict_for_db

def psu_create(dict_mem, key_, update=False):
    count_obj = 0
    if dict_mem['part_number'] and not PSU.objects.filter(part_number=dict_mem['part_number']) and update == False:
        psu = PSU.objects.create(name=dict_mem['name'], part_number=dict_mem['part_number'],
        vendor=dict_mem['vendor'], price=0,desc_ukr=dict_mem['desc_ukr'], desc_ru=dict_mem['desc_ru'],
        psu_p=dict_mem['psu_pow'], psu_c=dict_mem['psu_80'],
        psu_f=dict_mem['psu_fan'], is_active = True)

        if key_ in ('other_parts', 'both'):
            root_other = PSU_OTHER.objects.create(root=psu, r_price=0, psu_ff=dict_mem['psu_ff'],
                                                psu_pfc=dict_mem['psu_pfc'],
                                                psu_no=dict_mem['psu_no'],
                                                psu_main_conn=dict_mem['psu_main_conn'],psu_gpu_conn=dict_mem['psu_gpu_conn'],
                                                psu_sata_conn=dict_mem['psu_sata_conn'],psu_molex_conn=dict_mem['psu_molex_conn'],
                                                psu_mod_ua=dict_mem['psu_mod_ua'],psu_mod_ru=dict_mem['psu_mod_ru'],
                                                psu_sl=dict_mem['psu_sl'])
            if key_ == 'other_parts':
                psu.is_active = False
                psu.save()
        return (count_obj, psu.pk)

    if dict_mem['part_number'] and PSU.objects.filter(part_number=dict_mem['part_number']).exists() and update == False:
        try:
            psu = PSU.objects.get(part_number=dict_mem['part_number'])
        except:
            psu = PSU.objects.filter(part_number=dict_mem['part_number']).first()
            count_obj = PSU.objects.filter(part_number=dict_mem['part_number']).count()

        if key_ in ('other_parts', 'both'):
            try:
                test = psu.root_other
            except:
                root_other = PSU_OTHER.objects.create(root=psu, r_price=0, psu_ff=dict_mem['psu_ff'],
                                                    psu_pfc=dict_mem['psu_pfc'],
                                                    psu_no=dict_mem['psu_no'],
                                                    psu_main_conn=dict_mem['psu_main_conn'],psu_gpu_conn=dict_mem['psu_gpu_conn'],
                                                    psu_sata_conn=dict_mem['psu_sata_conn'],
                                                    psu_molex_conn=dict_mem['psu_molex_conn'],
                                                    psu_mod_ua=dict_mem['psu_mod_ua'],psu_mod_ru=dict_mem['psu_mod_ru'],
                                                    psu_sl=dict_mem['psu_sl'])
        return (count_obj, psu.pk)
    if update == True:
        c = PSU.objects.get(name=dict_mem['name'])
        c.part_number=dict_mem['part_number']
        c.vendor=dict_mem['vendor']
        c.price=dict_mem['price']
        c.desc_ukr=dict_mem['desc_ukr']
        c.desc_ru=dict_mem['desc_ru']
        c.psu_p=dict_mem['psu_pow']
        c.psu_c=dict_mem['psu_80']
        c.psu_f=dict_mem['psu_fan']
        c.save()

        other = c.root_other

        other.r_price = dict_mem['r_price']
        other.psu_ff = dict_mem['psu_ff']
        other.psu_pfc = dict_mem['psu_pfc']
        other.psu_no = dict_mem['psu_no']
        other.psu_main_conn = dict_mem['psu_main_conn']
        other.psu_gpu_conn = dict_mem['psu_gpu_conn']
        other.psu_sata_conn = dict_mem['psu_sata_conn']
        other.psu_molex_conn = dict_mem['psu_molex_conn']
        other.psu_mod_ua = dict_mem['psu_mod_ua']
        other.psu_mod_ru = dict_mem['psu_mod_ru']
        other.psu_sl = dict_mem['psu_sl']
        other.psu_ai_ua = dict_mem['psu_ai_ua']
        other.psu_ai_ru = dict_mem['psu_ai_ru']
        other.psu_warr_ua = dict_mem['psu_warr_ua']
        other.psu_warr_ru = dict_mem['psu_warr_ru']
        other.you_vid = dict_mem['you_vid']
        other.label = dict_mem['label']
        other.creditoff = dict_mem['creditoff']
        other.save()

        return (count_obj, c.pk)

    return (count_obj, None)

def fan_edition(dict_, art):
    vendor_set = {'DarkFlash', 'PCCooler', 'ID-COOLING', 'Be quiet', 'Vinga',
                'Frime', '1stPlayer', 'ARCTIC', 'Aerocool', 'Gamemax', 'Noctua'}
    dict_for_db = {}
    dict_for_db['part_number'] = art
    title = dict_['титл'] if 'титл' in dict_ else ''
    for v in vendor_set:
        if title.lower().find(v.lower()) != -1:
            dict_for_db['vendor'] = v
    if 'vendor' not in dict_for_db:
        dict_for_db['vendor'] = ''
    dict_for_db['name'] = re.sub(r'\W',' ',title)
    dict_for_db['desc_ukr'] = FAN.objects.first().desc_ukr if FAN.objects.first() else ''
    dict_for_db['desc_ru'] = FAN.objects.first().desc_ru if FAN.objects.first() else ''
    min = dict_['Минимальные обороты'] if 'Минимальные обороты' in dict_ else ''
    dict_for_db['fan_min_spd_ua'] = re.findall(r'\d+',min)[0] + ' об/хв' if re.findall(r'\d+',min) else ''
    dict_for_db['fan_min_spd_ru'] = re.findall(r'\d+',min)[0] + ' об/мин' if re.findall(r'\d+',min) else ''
    max = dict_['Максимальные обороты'] if 'Максимальные обороты' in dict_ else ''
    dict_for_db['fan_max_spd_ua'] = re.findall(r'\d+',max)[0] + ' об/хв' if re.findall(r'\d+',max) else ''
    dict_for_db['fan_max_spd_ru'] = re.findall(r'\d+',max)[0] + ' об/мин' if re.findall(r'\d+',max) else ''
    dict_for_db['fan_max_no'] = dict_['Уровень шума'] if 'Уровень шума' in dict_ else ''
    dict_for_db['part_fan_size'] = dict_['Диаметр вентилятора'] if 'Диаметр вентилятора' in dict_ else ''
    dict_for_db['fan_b_type_ru'] = dict_['Тип подшипника'] if 'Тип подшипника' in dict_ else ''
    dict_for_db['fan_b_type_ua'] = 'гідродинамічний' if dict_for_db['fan_b_type_ru'] == 'гидродинамический' else '-'
    dict_for_db['fan_max_af'] = dict_['Макс воздушный поток'] if 'Макс воздушный поток' in dict_ else '-'
    dict_for_db['fan_pwm'] = '+' if 'Регулятор оборотов' in dict_  and dict_['Регулятор оборотов'].find('PWM') != -1 else '-'
    dict_for_db['fan_pow'] = dict_['Питание'] if 'Питание' in dict_ else '-'
    dict_for_db['fan_led_type_ua'] = dict_for_db['fan_led_type_ru'] = dict_['Цвет подсветки'] if 'Цвет подсветки' in dict_ else '-'

    return dict_for_db

def fan_create(dict_mem, key_, update=False):
    count_obj = 0
    if dict_mem['part_number'] and not FAN.objects.filter(part_number=dict_mem['part_number']) and update == False:
        fan = FAN.objects.create(name=dict_mem['name'], part_number=dict_mem['part_number'],
        vendor=dict_mem['vendor'], price=0,desc_ukr=dict_mem['desc_ukr'], desc_ru=dict_mem['desc_ru'],
        case_fan_spd_ua=dict_mem['fan_max_spd_ua'], case_fan_spd_rus=dict_mem['fan_max_spd_ru'],
        case_fan_noise_level=dict_mem['fan_max_no'], case_fan_size=dict_mem['part_fan_size'],is_active = True)

        if key_ in ('other_parts', 'both'):
            root_other = FAN_OTHER.objects.create(root=fan, r_price=0, fan_b_type_ua=dict_mem['fan_b_type_ua'],
                                                fan_b_type_ru=dict_mem['fan_b_type_ru'],
                                                fan_min_spd_ua=dict_mem['fan_min_spd_ua'],
                                                fan_min_spd_ru=dict_mem['fan_min_spd_ru'],fan_max_spd_ua=dict_mem['fan_max_spd_ua'],
                                                fan_max_spd_ru=dict_mem['fan_max_spd_ru'],fan_max_af=dict_mem['fan_max_af'],
                                                fan_pwm=dict_mem['fan_pwm'],fan_pow=dict_mem['fan_pow'],
                                                fan_led_type_ua=dict_mem['fan_led_type_ua'],
                                                fan_led_type_ru=dict_mem['fan_led_type_ru'])
            if key_ == 'other_parts':
                fan.is_active = False
                fan.save()
        return (count_obj, fan.pk)

    if dict_mem['part_number'] and FAN.objects.filter(part_number=dict_mem['part_number']).exists() and update == False:
        try:
            fan = FAN.objects.get(part_number=dict_mem['part_number'])
        except:
            fan = FAN.objects.filter(part_number=dict_mem['part_number']).first()
            count_obj = FAN.objects.filter(part_number=dict_mem['part_number']).count()

        if key_ in ('other_parts', 'both'):
            try:
                test = fan.root_other
            except:
                root_other = FAN_OTHER.objects.create(root=fan, r_price=0, fan_b_type_ua=dict_mem['fan_b_type_ua'],
                                                    fan_b_type_ru=dict_mem['fan_b_type_ru'],
                                                    fan_min_spd_ua=dict_mem['fan_min_spd_ua'],
                                                    fan_min_spd_ru=dict_mem['fan_min_spd_ru'],
                                                    fan_max_spd_ua=dict_mem['fan_max_spd_ua'],
                                                    fan_max_spd_ru=dict_mem['fan_max_spd_ru'],fan_max_af=dict_mem['fan_max_af'],
                                                    fan_pwm=dict_mem['fan_pwm'],fan_pow=dict_mem['fan_pow'],
                                                    fan_led_type_ua=dict_mem['fan_led_type_ua'],
                                                    fan_led_type_ru=dict_mem['fan_led_type_ru'])
        return (count_obj, fan.pk)
    if update == True:
        c = FAN.objects.get(name=dict_mem['name'])
        c.part_number=dict_mem['part_number']
        c.vendor=dict_mem['vendor']
        c.price=dict_mem['price']
        c.desc_ukr=dict_mem['desc_ukr']
        c.desc_ru=dict_mem['desc_ru']
        c.case_fan_size=dict_mem['part_fan_size']
        c.case_fan_noise_level=dict_mem['fan_max_no']
        c.save()

        other = c.root_other

        other.r_price = dict_mem['r_price']
        other.fan_b_type_ua = dict_mem['fan_b_type_ua']
        other.fan_b_type_ru = dict_mem['fan_b_type_ru']
        other.fan_min_spd_ua = dict_mem['fan_min_spd_ua']
        other.fan_min_spd_ru = dict_mem['fan_min_spd_ru']
        other.fan_max_spd_ua = dict_mem['fan_max_spd_ua']
        other.fan_max_spd_ru = dict_mem['fan_max_spd_ru']
        other.fan_max_af = dict_mem['fan_max_af']
        other.fan_pwm = dict_mem['fan_pwm']
        other.fan_pow = dict_mem['fan_pow']
        other.fan_led_type_ua = dict_mem['fan_led_type_ua']
        other.fan_led_type_ru = dict_mem['fan_led_type_ru']
        other.fan_ai_ua = dict_mem['fan_ai_ua']
        other.fan_ai_ru = dict_mem['fan_ai_ru']
        other.fan_warr_ua = dict_mem['fan_warr_ua']
        other.fan_warr_ru = dict_mem['fan_warr_ru']
        other.you_vid = dict_mem['you_vid']
        other.label = dict_mem['label']
        other.creditoff = dict_mem['creditoff']
        other.save()

        return (count_obj, c.pk)

    return (count_obj, None)

def gpu_edition(dict_, art):
    vendor_set = {'MSI', 'Asus', 'Inno3D', 'XFX', 'Sapphire',
                'Palit', 'Gigabyte', 'PowerColor'}
    dict_for_db = {}
    dict_for_db['part_number'] = art
    title = dict_['титл'] if 'титл' in dict_ else ''
    for v in vendor_set:
        if title.lower().find(v.lower()) != -1:
            dict_for_db['vendor'] = v
    if 'vendor' not in dict_for_db:
        dict_for_db['vendor'] = ''
    dict_for_db['name'] = re.sub(r'\W',' ',title)
    dict_for_db['desc_ukr'] = GPU.objects.first().desc_ukr if GPU.objects.first() else ''
    dict_for_db['desc_ru'] = GPU.objects.first().desc_ru if GPU.objects.first() else ''
    dict_for_db['gpu_model'] = dict_['Модель GPU'] if 'Модель GPU' in dict_ else ''
    dict_for_db['f_name'] = re.sub('AMD|NVIDIA','',dict_for_db['gpu_model']).strip()
    dict_for_db['main_category'] = 'NVIDIA' if dict_for_db['gpu_model'].find('NVIDIA') != -1 else 'RADEON'
    dict_for_db['gpu_mem_size'] = dict_['Объем памяти'] if 'Объем памяти' in dict_ else ''
    dict_for_db['gpu_bit'] = dict_['Разрядность шины'] if 'Разрядность шины' in dict_ else ''
    dict_for_db['part_gpu_gpu_spd'] = dict_['Частота работы GPU'] if 'Частота работы GPU' in dict_ else ''
    dict_for_db['part_gpu_mem_spd'] = dict_['Частота работы памяти'] if 'Частота работы памяти' in dict_ else ''
    dict_for_db['gpu_mem_type'] = dict_['Тип памяти'] if 'Тип памяти' in dict_ else ''
    dict_for_db['gpu_watt'] = dict_['Рекомендуемая мощность БП от'] if 'Рекомендуемая мощность БП от' in dict_ else ''
    dict_for_db['gpu_max_sc'] = dict_['Макс подключаемых мониторов'] if 'Макс подключаемых мониторов' in dict_ else ''
    dict_for_db['gpu_vga'] = dict_['VGA'] if 'VGA' in dict_ else '-'
    dict_for_db['gpu_dvi'] = dict_['DVI D'] if 'DVI D' in dict_ else '-'
    dict_for_db['gpu_hdmi'] = dict_['HDMI'] if 'HDMI' in dict_ else '-'
    dict_for_db['gpu_dp'] = dict_['DisplayPort'] if 'DisplayPort' in dict_ else '-'
    gpu_max_l = re.match(r'(\d+) мм', dict_['Длина видеокарты']) if 'Длина видеокарты' in dict_ else ''
    dict_for_db['gpu_max_l'] = gpu_max_l.group() if gpu_max_l else '-'
    dict_for_db['gpu_lp'] = '+' if 'Низкопрофильная low profile ' in dict_ else '-'
    dict_for_db['gpu_sl'] = dict_['Занимаемых слотов'] if 'Занимаемых слотов' in dict_ else ''
    dict_for_db['gpu_cool_ru'] = dict_['Охлаждение'] if 'Охлаждение' in dict_ else '-'
    dict_for_db['gpu_cool_ua'] = 'активне кулер' if dict_for_db['gpu_cool_ru'] == 'активное кулер ' else 'пасивне радіатор '

    return dict_for_db

def gpu_create(dict_mem, key_, update=False):
    count_obj = 0
    if dict_mem['part_number'] and not GPU.objects.filter(part_number=dict_mem['part_number']) and update == False:
        gpu = GPU.objects.create(name=dict_mem['name'], part_number=dict_mem['part_number'],
        vendor=dict_mem['vendor'], price=0,desc_ukr=dict_mem['desc_ukr'], desc_ru=dict_mem['desc_ru'],
        main_category=dict_mem['main_category'], f_name=dict_mem['f_name'], gpu_m_s=dict_mem['gpu_mem_size'],
        gpu_b=dict_mem['gpu_bit'], gpu_cpu_spd=dict_mem['part_gpu_gpu_spd'], gpu_mem_spd=dict_mem['part_gpu_mem_spd'],
        gpu_fps=dict_mem['gpu_model'], is_active = True)

        if key_ in ('other_parts', 'both'):
            root_other = GPU_OTHER.objects.create(root=gpu, r_price=0, gpu_model=dict_mem['gpu_model'],
                                                gpu_mem_type=dict_mem['gpu_mem_type'],
                                                gpu_watt=dict_mem['gpu_watt'],
                                                gpu_max_sc=dict_mem['gpu_max_sc'],gpu_vga=dict_mem['gpu_vga'],
                                                gpu_dvi=dict_mem['gpu_dvi'],gpu_hdmi=dict_mem['gpu_hdmi'],
                                                gpu_dp=dict_mem['gpu_dp'],gpu_cool_ua=dict_mem['gpu_cool_ua'],
                                                gpu_cool_ru=dict_mem['gpu_cool_ru'],gpu_sl=dict_mem['gpu_sl'],
                                                gpu_max_l=dict_mem['gpu_max_l'],gpu_lp=dict_mem['gpu_lp'])
            if key_ == 'other_parts':
                gpu.is_active = False
                gpu.save()
        return (count_obj, gpu.pk)

    if dict_mem['part_number'] and GPU.objects.filter(part_number=dict_mem['part_number']).exists() and update == False:
        try:
            gpu = GPU.objects.get(part_number=dict_mem['part_number'])
        except:
            gpu = GPU.objects.filter(part_number=dict_mem['part_number']).first()
            count_obj = GPU.objects.filter(part_number=dict_mem['part_number']).count()

        if key_ in ('other_parts', 'both'):
            try:
                test = gpu.root_other
            except:
                root_other = GPU_OTHER.objects.create(root=gpu, r_price=0, gpu_model=dict_mem['gpu_model'],
                                                    gpu_mem_type=dict_mem['gpu_mem_type'],
                                                    gpu_watt=dict_mem['gpu_watt'],
                                                    gpu_max_sc=dict_mem['gpu_max_sc'],gpu_vga=dict_mem['gpu_vga'],
                                                    gpu_dvi=dict_mem['gpu_dvi'],gpu_hdmi=dict_mem['gpu_hdmi'],
                                                    gpu_dp=dict_mem['gpu_dp'],gpu_cool_ua=dict_mem['gpu_cool_ua'],
                                                    gpu_cool_ru=dict_mem['gpu_cool_ru'],gpu_sl=dict_mem['gpu_sl'],
                                                    gpu_max_l=dict_mem['gpu_max_l'],gpu_lp=dict_mem['gpu_lp'])
        return (count_obj, gpu.pk)
    if update == True:
        c = GPU.objects.get(name=dict_mem['name'])
        c.part_number=dict_mem['part_number']
        c.vendor=dict_mem['vendor']
        c.price=dict_mem['price']
        c.desc_ukr=dict_mem['desc_ukr']
        c.desc_ru=dict_mem['desc_ru']
        c.gpu_m_s=dict_mem['gpu_mem_size']
        c.gpu_b=dict_mem['gpu_bit']
        c.gpu_cpu_spd=dict_mem['part_gpu_gpu_spd']
        c.gpu_mem_spd=dict_mem['part_gpu_mem_spd']
        c.save()

        other = c.root_other

        other.r_price = dict_mem['r_price']
        other.gpu_mem_type = dict_mem['gpu_mem_type']
        other.gpu_watt = dict_mem['gpu_watt']
        other.gpu_max_sc = dict_mem['gpu_max_sc']
        other.gpu_vga = dict_mem['gpu_vga']
        other.gpu_dvi = dict_mem['gpu_dvi']
        other.gpu_hdmi = dict_mem['gpu_hdmi']
        other.gpu_dp = dict_mem['gpu_dp']
        other.gpu_cool_ua = dict_mem['gpu_cool_ua']
        other.gpu_cool_ru = dict_mem['gpu_cool_ru']
        other.gpu_sl = dict_mem['gpu_sl']
        other.gpu_max_l = dict_mem['gpu_max_l']
        other.gpu_lp = dict_mem['gpu_lp']
        other.gpu_ai_ua = dict_mem['gpu_ai_ua']
        other.gpu_ai_ru = dict_mem['gpu_ai_ru']
        other.gpu_warr_ua = dict_mem['gpu_warr_ua']
        other.gpu_warr_ru = dict_mem['gpu_warr_ru']
        other.you_vid = dict_mem['you_vid']
        other.label = dict_mem['label']
        other.creditoff = dict_mem['creditoff']
        other.save()

        return (count_obj, c.pk)

    return (count_obj, None)

def ssd_edition(dict_, art):
    vendor_set = {'Intel', 'Kingston', 'Samsung', 'WD', 'Crucial', 'Team',
                'Patriot', 'Gigabyte', 'GoodRAM', 'Western Digital'}
    dict_for_db = {}
    dict_for_db['part_number'] = art
    title = dict_['титл'] if 'титл' in dict_ else ''
    for v in vendor_set:
        if title.lower().find(v.lower()) != -1:
            dict_for_db['vendor'] = v
    if 'vendor' not in dict_for_db:
        dict_for_db['vendor'] = ''
    dict_for_db['name'] = re.sub(r'\W',' ',title)
    dict_for_db['desc_ukr'] = SSD.objects.first().desc_ukr if SSD.objects.first() else ''
    dict_for_db['desc_ru'] = SSD.objects.first().desc_ru if SSD.objects.first() else ''
    dict_for_db['ssd_size'] = dict_['Объем'] if 'Объем' in dict_ else ''
    f_name = re.findall(r'(\d+).ГБ',dict_for_db['ssd_size'])[0] if re.findall(r'(\d+).ГБ',dict_for_db['ssd_size']) else ''
    dict_for_db['f_name'] = f"{round(int(f_name)/1000)}" + 'Tb' if f_name else dict_for_db['ssd_size']
    if dict_for_db['f_name'] == '0Tb':
        dict_for_db['f_name'] = dict_for_db['ssd_size']
    part_ssd_r_spd = dict_['Внешняя скорость считывания'] if 'Внешняя скорость считывания' in dict_ else ''
    part_ssd_w_spd = dict_['Внешняя скорость записи'] if 'Внешняя скорость записи' in dict_ else ''
    dict_for_db['part_ssd_r_spd'] = re.findall(r'(\d+)',part_ssd_r_spd)[0] + ' МБ/с' if re.findall(r'(\d+)',part_ssd_r_spd) else ''
    dict_for_db['part_ssd_w_spd'] = re.findall(r'(\d+)',part_ssd_w_spd)[0] + ' МБ/с' if re.findall(r'(\d+)',part_ssd_w_spd) else ''
    dict_for_db['ssd_spd'] = f"{part_ssd_w_spd} / {part_ssd_r_spd} МБ/с"
    dict_for_db['ssd_r_spd'] = '-'
    dict_for_db['ssd_nand'] = dict_['Тип памяти'] if 'Тип памяти' in dict_ else ''

    dict_for_db['ssd_type1_ua'] = 'SSD накопичувач'
    dict_for_db['ssd_type1_ru'] = 'SSD накопитель'
    dict_for_db['ssd_type2_ru'] = dict_['Тип'].capitalize() if 'Тип' in dict_ else ''
    dict_for_db['ssd_type2_ua'] = 'Внутрішній' if dict_for_db['ssd_type2_ru'] == 'Внутренний' else '-'
    dict_for_db['ssd_ff'] = dict_['Форм фактор'] if 'Форм фактор' in dict_ else ''
    dict_for_db['ssd_int'] = dict_['Разъем'] if 'Разъем' in dict_ else ''
    dict_for_db['ssd_int'] = dict_['Интерфейс M 2'] if 'Интерфейс M 2' in dict_  else dict_for_db['ssd_int']
    dict_for_db['ssd_con_type'] = dict_['Контроллер'] if 'Контроллер' in dict_ else ''

    return dict_for_db

def ssd_create(dict_mem, key_, update=False):
    count_obj = 0
    if dict_mem['part_number'] and not SSD.objects.filter(part_number=dict_mem['part_number']) and update == False:
        ssd = SSD.objects.create(name=dict_mem['name'], part_number=dict_mem['part_number'],
        vendor=dict_mem['vendor'], price=0,desc_ukr=dict_mem['desc_ukr'], desc_ru=dict_mem['desc_ru'],
        ssd_s=dict_mem['ssd_size'], f_name=dict_mem['f_name'], ssd_spd=dict_mem['ssd_spd'],
        ssd_r_spd=dict_mem['ssd_r_spd'], ssd_type_cells=dict_mem['ssd_nand'],is_active = True)

        if key_ in ('other_parts', 'both'):
            root_other = SSD_OTHER.objects.create(root=ssd, r_price=0, part_ssd_r_spd=dict_mem['part_ssd_r_spd'],
                                                part_ssd_w_spd=dict_mem['part_ssd_w_spd'],
                                                ssd_con_type=dict_mem['ssd_con_type'],
                                                ssd_int=dict_mem['ssd_int'],ssd_type1_ua=dict_mem['ssd_type1_ua'],
                                                ssd_type1_ru=dict_mem['ssd_type1_ru'],ssd_type2_ua=dict_mem['ssd_type2_ua'],
                                                ssd_ff=dict_mem['ssd_ff'],ssd_type2_ru=dict_mem['ssd_type2_ru']
                                                )
            if key_ == 'other_parts':
                ssd.is_active = False
                ssd.save()
        return (count_obj, ssd.pk)

    if dict_mem['part_number'] and SSD.objects.filter(part_number=dict_mem['part_number']).exists() and update == False:
        try:
            ssd = SSD.objects.get(part_number=dict_mem['part_number'])
        except:
            ssd = SSD.objects.filter(part_number=dict_mem['part_number']).first()
            count_obj = SSD.objects.filter(part_number=dict_mem['part_number']).count()

        if key_ in ('other_parts', 'both'):
            try:
                test = ssd.root_other
            except:
                root_other = SSD_OTHER.objects.create(root=ssd, r_price=0, part_ssd_r_spd=dict_mem['part_ssd_r_spd'],
                                                    part_ssd_w_spd=dict_mem['part_ssd_w_spd'],
                                                    ssd_con_type=dict_mem['ssd_con_type'],
                                                    ssd_int=dict_mem['ssd_int'],ssd_type1_ua=dict_mem['ssd_type1_ua'],
                                                    ssd_type1_ru=dict_mem['ssd_type1_ru'],ssd_type2_ua=dict_mem['ssd_type2_ua'],
                                                    ssd_ff=dict_mem['ssd_ff'],ssd_type2_ru=dict_mem['ssd_type2_ru']
                                                    )
        return (count_obj, ssd.pk)
    if update == True:
        c = SSD.objects.get(name=dict_mem['name'])
        c.part_number=dict_mem['part_number']
        c.vendor=dict_mem['vendor']
        c.price=dict_mem['price']
        c.desc_ukr=dict_mem['desc_ukr']
        c.desc_ru=dict_mem['desc_ru']
        c.ssd_s=dict_mem['ssd_size']
        #c.f_name=dict_mem['f_name']
        #c.ssd_spd=dict_mem['ssd_spd']
        #c.ssd_r_spd=dict_mem['ssd_r_spd']
        c.ssd_type_cells=dict_mem['ssd_nand']
        c.save()

        other = c.root_other

        other.r_price = dict_mem['r_price']
        other.ssd_type1_ua = dict_mem['ssd_type1_ua']
        other.ssd_type1_ru = dict_mem['ssd_type1_ru']
        other.ssd_type2_ua = dict_mem['ssd_type2_ua']
        other.ssd_type2_ru = dict_mem['ssd_type2_ru']
        other.ssd_ff = dict_mem['ssd_ff']
        other.ssd_int = dict_mem['ssd_int']
        other.ssd_con_type = dict_mem['ssd_con_type']
        other.part_ssd_r_spd = dict_mem['part_ssd_r_spd']
        other.part_ssd_w_spd = dict_mem['part_ssd_w_spd']
        other.ssd_ai_ua = dict_mem['ssd_ai_ua']
        other.ssd_ai_ru = dict_mem['ssd_ai_ru']
        other.ssd_warr_ua = dict_mem['ssd_warr_ua']
        other.ssd_warr_ru = dict_mem['ssd_warr_ru']
        other.you_vid = dict_mem['you_vid']
        other.label = dict_mem['label']
        other.creditoff = dict_mem['creditoff']
        other.save()

        return (count_obj, c.pk)

    return (count_obj, None)

def hdd_edition(dict_, art):
    vendor_set = {'Western Digital', 'Toshiba', 'Seagate', 'WD'}
    dict_for_db = {}
    dict_for_db['part_number'] = art
    title = dict_['титл'] if 'титл' in dict_ else ''
    for v in vendor_set:
        if title.lower().find(v.lower()) != -1:
            dict_for_db['vendor'] = v
    if 'vendor' not in dict_for_db:
        dict_for_db['vendor'] = ''
    dict_for_db['name'] = re.sub(r'\W',' ',title)
    dict_for_db['desc_ukr'] = HDD.objects.first().desc_ukr if HDD.objects.first() else ''
    dict_for_db['desc_ru'] = HDD.objects.first().desc_ru if HDD.objects.first() else ''
    dict_for_db['hdd_size'] = dict_['Объем'] if 'Объем' in dict_ else ''
    f_name = re.findall(r'(\d+).ГБ',dict_for_db['hdd_size'])[0] if re.findall(r'(\d+).ГБ',dict_for_db['hdd_size']) else '0'
    dict_for_db['f_name'] = f"{round(int(f_name)/1000)}" + 'Tb' if f_name else dict_for_db['hdd_size']
    if dict_for_db['f_name'] == '0Tb':
        dict_for_db['f_name'] = dict_for_db['hdd_size']
    spd = dict_['Частота вращения шпинделя'] if 'Частота вращения шпинделя' in dict_ else ''
    dict_for_db['hdd_spd_ph_ua'] = re.findall(r'(\d+)',spd)[0] + ' об/хв' if re.findall(r'(\d+)',spd) else ''
    dict_for_db['hdd_spd_ph_ru'] = re.findall(r'(\d+)',spd)[0] + ' об/мин' if re.findall(r'(\d+)',spd) else ''
    dict_for_db['hdd_buf'] = dict_['Объем буфера обмена'] if 'Объем буфера обмена' in dict_ else ''

    dict_for_db['hdd_type1_ua'] = 'Жорсткий диск'
    dict_for_db['hdd_type1_ru'] = 'Жесткий диск'
    dict_for_db['hdd_type2_ru'] = dict_['Исполнение'].capitalize() if 'Исполнение' in dict_ else ''
    dict_for_db['hdd_type2_ua'] = 'Внутрішній' if dict_for_db['hdd_type2_ru'] == 'Внутренний' else '-'
    dict_for_db['hdd_ff'] = '3,5"'
    dict_for_db['hdd_int'] = dict_['Интерфейсы подключения'] if 'Интерфейсы подключения' in dict_ else ''

    return dict_for_db

def hdd_create(dict_mem, key_, update=False):
    count_obj = 0
    if dict_mem['part_number'] and not HDD.objects.filter(part_number=dict_mem['part_number']) and update == False:
        hdd = HDD.objects.create(name=dict_mem['name'], part_number=dict_mem['part_number'],
        vendor=dict_mem['vendor'], price=0,desc_ukr=dict_mem['desc_ukr'], desc_ru=dict_mem['desc_ru'],
        hdd_s=dict_mem['hdd_size'], f_name=dict_mem['f_name'], hdd_spd_ua=dict_mem['hdd_spd_ph_ua'],
        hdd_spd_rus=dict_mem['hdd_spd_ph_ru'], hdd_ca=dict_mem['hdd_buf'],is_active = True)

        if key_ in ('other_parts', 'both'):
            root_other = HDD_OTHER.objects.create(root=hdd, r_price=0, hdd_type1_ua=dict_mem['hdd_type1_ua'],
                                                hdd_type1_ru=dict_mem['hdd_type1_ru'],
                                                hdd_type2_ua=dict_mem['hdd_type2_ua'],
                                                hdd_type2_ru=dict_mem['hdd_type2_ru'],
                                                hdd_ff=dict_mem['hdd_ff'],
                                                hdd_int=dict_mem['hdd_int'],
                                                )
            if key_ == 'other_parts':
                hdd.is_active = False
                hdd.save()
        return (count_obj, hdd.pk)

    if dict_mem['part_number'] and HDD.objects.filter(part_number=dict_mem['part_number']).exists() and update == False:
        try:
            hdd = HDD.objects.get(part_number=dict_mem['part_number'])
        except:
            hdd = HDD.objects.filter(part_number=dict_mem['part_number']).first()
            count_obj = HDD.objects.filter(part_number=dict_mem['part_number']).count()

        if key_ in ('other_parts', 'both'):
            try:
                test = hdd.root_other
            except:
                root_other = HDD_OTHER.objects.create(root=hdd, r_price=0, hdd_type1_ua=dict_mem['hdd_type1_ua'],
                                                    hdd_type1_ru=dict_mem['hdd_type1_ru'],
                                                    hdd_type2_ua=dict_mem['hdd_type2_ua'],
                                                    hdd_type2_ru=dict_mem['hdd_type2_ru'],
                                                    hdd_ff=dict_mem['hdd_ff'],
                                                    hdd_int=dict_mem['hdd_int'],
                                                    )
        return (count_obj, hdd.pk)
    if update == True:
        c = HDD.objects.get(name=dict_mem['name'])
        c.part_number=dict_mem['part_number']
        c.vendor=dict_mem['vendor']
        c.price=dict_mem['price']
        c.desc_ukr=dict_mem['desc_ukr']
        c.desc_ru=dict_mem['desc_ru']
        c.hdd_s=dict_mem['hdd_size']
        c.hdd_spd_ua=dict_mem['hdd_spd_ph_ua']
        c.hdd_spd_rus=dict_mem['hdd_spd_ph_ru']
        c.hdd_ca=dict_mem['hdd_buf']
        c.save()

        other = c.root_other

        other.r_price = dict_mem['r_price']
        other.hdd_type1_ua = dict_mem['hdd_type1_ua']
        other.hdd_type1_ru = dict_mem['hdd_type1_ru']
        other.hdd_type2_ua = dict_mem['hdd_type2_ua']
        other.hdd_type2_ru = dict_mem['hdd_type2_ru']
        other.hdd_ff = dict_mem['hdd_ff']
        other.hdd_int = dict_mem['hdd_int']
        other.hdd_ai_ua = dict_mem['hdd_ai_ua']
        other.hdd_ai_ru = dict_mem['hdd_ai_ru']
        other.hdd_warr_ua = dict_mem['hdd_warr_ua']
        other.hdd_warr_ru = dict_mem['hdd_warr_ru']
        other.you_vid = dict_mem['you_vid']
        other.label = dict_mem['label']
        other.creditoff = dict_mem['creditoff']
        other.save()

        return (count_obj, c.pk)

    return (count_obj, None)

def mb_edition(dict_, art):
    vendor_set = {'Biostar', 'Intel', 'Gigabyte', 'MSI', 'ASUS', 'ASRock'}
    dict_for_db = {}
    dict_for_db['part_number'] = art
    title = dict_['титл'] if 'титл' in dict_ else ''
    for v in vendor_set:
        if title.lower().find(v.lower()) != -1:
            dict_for_db['vendor'] = v
    if 'vendor' not in dict_for_db:
        dict_for_db['vendor'] = ''
    dict_for_db['name'] = re.sub(dict_for_db['vendor'].lower(), '',title.lower()).strip().capitalize()
    part_mb_fam = dict_['Чипсет'] if 'Чипсет' in dict_ else ''
    dict_for_db['part_mb_fam'] = 'Intel' if part_mb_fam.lower().find('intel') != -1 else 'AMD'
    dict_for_db['desc_ukr'] = MB.objects.first().desc_ukr if MB.objects.first() else ''
    dict_for_db['desc_ru'] = MB.objects.first().desc_ru if MB.objects.first() else ''
    dict_for_db['mb_chipset'] = dict_['Чипсет'] if 'Чипсет' in dict_ else ''

    dict_for_db['part_mb_chip'] = re.sub('intel|amd','',dict_for_db['mb_chipset'].lower()).strip()

    dict_for_db['part_mb_ram_max_size'] = '-'
    dict_for_db['depend_to_type'] = 'chipset'
    dict_for_db['part_mb_ff'] = re.sub('micro ', 'm', dict_['Форм фактор']) if 'Форм фактор' in dict_ else ''
    dict_for_db['depend_from_type'] = 'case'

    dict_for_db['part_mb_sock'] = re.sub('Intel|AMD','',dict_['Socket']).strip() if 'Socket' in dict_ else ''
    ddr = re.findall(r'(DDR\d)', dict_['Слоты ОЗУ']) if 'Слоты ОЗУ' in dict_ else ''
    part_mb_ram_sl = re.findall(r'DDR\d (\d)', dict_['Слоты ОЗУ']) if 'Слоты ОЗУ' in dict_ else ''
    dict_for_db['part_mb_ram_type'] = ddr[0] if ddr else ''
    dict_for_db['part_mb_ram_sl'] = part_mb_ram_sl[0] if part_mb_ram_sl else ''
    dict_for_db['part_mb_ram_ch'] = '2'
    dict_for_db['part_mb_ram_max_spd'] = dict_['Тактовая частота ОЗУ'] if 'Тактовая частота ОЗУ' in dict_ else ''
    dict_for_db['part_mb_main_conn'] = dict_['Разъем питания'] if 'Разъем питания' in dict_ else ''
    dict_for_db['part_mb_cpu_conn'] = dict_['Питание процессора'] if 'Питание процессора' in dict_ else ''
    dict_for_db['part_mb_sound_ch'] = dict_['Звук каналов '] if 'Звук каналов ' in dict_ else ''
    dict_for_db['part_mb_lan'] = '+'
    dict_for_db['part_mb_hdmi'] = '+' if 'Разъемы' in dict_ and dict_['Разъемы'].find('HDMI') != -1 else '-'
    dict_for_db['part_mb_dp'] = '+' if 'Доп разъемы' in dict_ and dict_['Доп разъемы'].find('DisplayPort') != -1 else '-'
    dict_for_db['part_mb_wifi'] = '+' if title.find('WI-FI') != -1 else '-'

    return dict_for_db

def mb_create(dict_mem, key_, update=False):
    count_obj = 0
    if dict_mem['part_number'] and not MB.objects.filter(part_number=dict_mem['part_number']) and update == False:
        mb = MB.objects.create(name=dict_mem['name'], part_number=dict_mem['part_number'],
        vendor=dict_mem['vendor'], price=0,desc_ukr=dict_mem['desc_ukr'], desc_ru=dict_mem['desc_ru'],
        main_category=dict_mem['part_mb_fam'], mb_chipset=dict_mem['mb_chipset'], mb_max_ram=dict_mem['part_mb_ram_max_size'],
        depend_to=dict_mem['part_mb_chip'], depend_to_type=dict_mem['depend_to_type'],depend_from=dict_mem['part_mb_ff'],
        depend_from_type=dict_mem['depend_from_type'],is_active = True)

        if key_ in ('other_parts', 'both'):
            root_other = MB_OTHER.objects.create(root=mb, r_price=0, part_mb_sock=dict_mem['part_mb_sock'],
                                                part_mb_ram_type=dict_mem['part_mb_ram_type'],
                                                part_mb_ram_sl=dict_mem['part_mb_ram_sl'],
                                                part_mb_ram_ch=dict_mem['part_mb_ram_ch'],
                                                part_mb_ram_max_spd=dict_mem['part_mb_ram_max_spd'],
                                                part_mb_hdmi=dict_mem['part_mb_hdmi'],
                                                part_mb_dp=dict_mem['part_mb_dp'],
                                                part_mb_sound_ch=dict_mem['part_mb_sound_ch'],
                                                part_mb_lan=dict_mem['part_mb_lan'],
                                                part_mb_wifi=dict_mem['part_mb_wifi'],
                                                part_mb_cpu_conn=dict_mem['part_mb_cpu_conn'],
                                                part_mb_main_conn=dict_mem['part_mb_main_conn']
                                                )
            if key_ == 'other_parts':
                mb.is_active = False
                mb.save()
        return (count_obj, mb.pk)

    if dict_mem['part_number'] and MB.objects.filter(part_number=dict_mem['part_number']).exists() and update == False:
        try:
            mb = MB.objects.get(part_number=dict_mem['part_number'])
        except:
            mb = MB.objects.filter(part_number=dict_mem['part_number']).first()
            count_obj = MB.objects.filter(part_number=dict_mem['part_number']).count()

        if key_ in ('other_parts', 'both'):
            try:
                test = mb.root_other
            except:
                root_other = MB_OTHER.objects.create(root=mb, r_price=0, part_mb_sock=dict_mem['part_mb_sock'],
                                                    part_mb_ram_type=dict_mem['part_mb_ram_type'],
                                                    part_mb_ram_sl=dict_mem['part_mb_ram_sl'],
                                                    part_mb_ram_ch=dict_mem['part_mb_ram_ch'],
                                                    part_mb_ram_max_spd=dict_mem['part_mb_ram_max_spd'],
                                                    part_mb_hdmi=dict_mem['part_mb_hdmi'],
                                                    part_mb_dp=dict_mem['part_mb_dp'],
                                                    part_mb_sound_ch=dict_mem['part_mb_sound_ch'],
                                                    part_mb_lan=dict_mem['part_mb_lan'],
                                                    part_mb_wifi=dict_mem['part_mb_wifi'],
                                                    part_mb_cpu_conn=dict_mem['part_mb_cpu_conn'],
                                                    part_mb_main_conn=dict_mem['part_mb_main_conn']
                                                    )
        return (count_obj, mb.pk)
    if update == True:
        c = MB.objects.get(name=dict_mem['name'])
        c.part_number=dict_mem['part_number']
        c.vendor=dict_mem['vendor']
        c.price=dict_mem['price']
        c.desc_ukr=dict_mem['desc_ukr']
        c.desc_ru=dict_mem['desc_ru']
        c.main_category=dict_mem['part_mb_fam']
        #c.mb_chipset=dict_mem['mb_chipset']
        c.mb_max_ram=dict_mem['part_mb_ram_max_size']
        c.depend_from=dict_mem['part_mb_ff']
        #c.depend_from_type=dict_mem['depend_from_type']
        c.depend_to=dict_mem['part_mb_chip']
        #c.depend_to_type=dict_mem['depend_to_type']
        c.save()

        other = c.root_other

        other.r_price = dict_mem['r_price']
        other.part_mb_sock = dict_mem['part_mb_sock']
        other.part_mb_pow_ph = dict_mem['part_mb_pow_ph']
        other.part_mb_ram_type = dict_mem['part_mb_ram_type']
        other.part_mb_ram_sl = dict_mem['part_mb_ram_sl']
        other.part_mb_ram_ch = dict_mem['part_mb_ram_ch']
        other.part_mb_ram_max_spd = dict_mem['part_mb_ram_max_spd']
        other.part_mb_vga = dict_mem['part_mb_vga']
        other.part_mb_dvi = dict_mem['part_mb_dvi']
        other.part_mb_hdmi = dict_mem['part_mb_hdmi']
        other.part_mb_dp = dict_mem['part_mb_dp']
        other.part_mb_sound_ch = dict_mem['part_mb_sound_ch']
        other.part_mb_sound_chip = dict_mem['part_mb_sound_chip']
        other.part_mb_lan = dict_mem['part_mb_lan']
        other.part_mb_wifi = dict_mem['part_mb_wifi']
        other.part_mb_bt = dict_mem['part_mb_bt']
        other.part_mb_lan_chip = dict_mem['part_mb_lan_chip']
        other.part_mb_sata = dict_mem['part_mb_sata']
        other.part_mb_m2 = dict_mem['part_mb_m2']
        other.part_mb_raid = dict_mem['part_mb_raid']
        other.part_mb_sl_x1 = dict_mem['part_mb_sl_x1']
        other.part_mb_sl_x16 = dict_mem['part_mb_sl_x16']
        other.part_mb_main_conn = dict_mem['part_mb_main_conn']
        other.part_mb_cpu_conn = dict_mem['part_mb_cpu_conn']
        other.part_mb_fan_conn = dict_mem['part_mb_fan_conn']
        other.part_mb_ai_ua = dict_mem['part_mb_ai_ua']
        other.part_mb_ai_ru = dict_mem['part_mb_ai_ru']
        other.part_mb_warr_ua = dict_mem['part_mb_warr_ua']
        other.part_mb_warr_ru = dict_mem['part_mb_warr_ru']
        other.you_vid = dict_mem['you_vid']
        other.label = dict_mem['label']
        other.creditoff = dict_mem['creditoff']
        other.save()

        return (count_obj, c.pk)

    return (count_obj, None)

def cooler_edition(dict_, art):
    vendor_set = {'Aerocool', 'Cooler Master', 'ID-COOLING', 'Gamemax', 'PcCooler', 'Deepcool', 'Be quiet', 'Cougar', 'NZXT',
                'Custom'}
    dict_for_db = {}
    dict_for_db['part_number'] = art
    title = dict_['титл'] if 'титл' in dict_ else ''
    for v in vendor_set:
        if title.lower().find(v.lower()) != -1:
            dict_for_db['vendor'] = v
    if 'vendor' not in dict_for_db:
        dict_for_db['vendor'] = ''
    dict_for_db['name'] = re.sub(dict_for_db['vendor'].lower(), '',title.lower()).strip().capitalize()
    dict_for_db['cool_type_ru'] = 'воздушное'
    dict_for_db['cool_type_ua'] = 'повітряне'
    min = dict_['Минимальные обороты'] if 'Минимальные обороты' in dict_ else ''
    dict_for_db['cool_fan_min_spd_ua'] = re.findall(r'\d+',min)[0] + ' об/хв' if re.findall(r'\d+',min) else ''
    dict_for_db['cool_fan_min_spd_ru'] = re.findall(r'\d+',min)[0] + ' об/мин' if re.findall(r'\d+',min) else ''
    max = dict_['Максимальные обороты'] if 'Максимальные обороты' in dict_ else ''
    dict_for_db['cool_fan_max_spd_ua'] = re.findall(r'\d+',max)[0] + ' об/хв' if re.findall(r'\d+',max) else ''
    dict_for_db['cool_fan_max_spd_ru'] = re.findall(r'\d+',max)[0] + ' об/мин' if re.findall(r'\d+',max) else ''
    dict_for_db['fan_spd_ua'] = dict_for_db['fan_spd_rus'] = ''
    if re.findall(r'\d+',min) and re.findall(r'\d+',max):
        dict_for_db['fan_spd_ua'] = re.findall(r'\d+',min)[0] + '-' + re.findall(r'\d+',max)[0] + ' об/хв'
        dict_for_db['fan_spd_rus'] = re.findall(r'\d+',min)[0] + '-' + re.findall(r'\d+',max)[0] + ' об/мин'
    if re.findall(r'\d+',max):
        dict_for_db['fan_spd_ua'] = dict_for_db['cool_fan_max_spd_ua']
        dict_for_db['fan_spd_rus'] = dict_for_db['cool_fan_max_spd_ru']
    dict_for_db['cool_min_no'] = '-'
    dict_for_db['cool_max_no'] = dict_['Уровень шума'] if 'Уровень шума' in dict_ else ''
    dict_for_db['cool_fan_size'] = dict_['Диаметр вентилятора'] if 'Диаметр вентилятора' in dict_ else ''
    depend_to = dict_['Socket'] if 'Socket' in dict_ else ''
    dict_for_db['cool_sock'] = depend_to
    intel_amd = 'Intel' if depend_to.lower().find('intel') != -1 else ''
    intel_amd = intel_amd + ' AMD' if depend_to.lower().find('amd') != -1 else intel_amd
    dict_for_db['depend_to'] = intel_amd
    dict_for_db['cool_fan_am'] = dict_['Вентиляторов'] if 'Вентиляторов' in dict_ else ''
    dict_for_db['cool_tub_am'] = dict_['Тепловых трубок'] if 'Тепловых трубок' in dict_ else ''
    dict_for_db['depend_to_type'] = 'cooler'
    dict_for_db['desc_ukr'] = Cooler.objects.first().desc_ukr if Cooler.objects.first() else ''
    dict_for_db['desc_ru'] = Cooler.objects.first().desc_ru if Cooler.objects.first() else ''
    dict_for_db['cool_tub_con_ru'] = dict_['Контакт теплотрубок'].capitalize() if 'Контакт теплотрубок' in dict_ else ''
    dict_for_db['cool_tub_con_ua'] = 'Прямий' if dict_for_db['cool_tub_con_ru'] == 'Прямой' else 'Непрямий'
    dict_for_db['cool_rad_mat_ru'] = dict_['Материал радиатора'] if 'Материал радиатора' in dict_ else ''
    dict_for_db['cool_rad_mat_ua'] = 'aлюміній мідь' if dict_for_db['cool_rad_mat_ru'] == 'алюминий медь' else ''
    dict_for_db['cool_fix_ru'] = dict_['Тип крепления'] if 'Тип крепления' in dict_ else ''
    dict_for_db['cool_fix_ua'] = 'двустороннiй backplate' if dict_for_db['cool_fix_ru'] == 'двусторонний backplate ' else ''
    dict_for_db['cool_fan_b_t_ru'] = dict_['Тип подшипника'] if 'Тип подшипника' in dict_ else ''
    dict_for_db['cool_fan_b_t_ua'] = 'Гідродинамічний' if dict_for_db['cool_fan_b_t_ru'] == 'гидродинамический' else ''
    dict_for_db['cool_fan_max_af'] = dict_['Макс воздушный поток'] if 'Макс воздушный поток' in dict_ else ''
    dict_for_db['cool_max_tdp'] = '-'
    dict_for_db['cool_pwm'] = dict_['Регулятор оборотов'] if 'Регулятор оборотов' in dict_ else ''
    dict_for_db['cool_conn'] = dict_['Питание'] if 'Питание' in dict_ else ''
    dict_for_db['cool_col'] = dict_['Цвет подсветки'] if 'Цвет подсветки' in dict_ else ''
    dict_for_db['cool_h'] = dict_['Высота'] if 'Высота' in dict_ else '-'
    dict_for_db['cool_w'] = dict_['Вес'] if 'Вес' in dict_ else '-'

    return dict_for_db

def cooler_create(dict_mem, key_, update=False):
    count_obj = 0
    if dict_mem['part_number'] and not Cooler.objects.filter(part_number=dict_mem['part_number']) and update == False:
        cooler = Cooler.objects.create(name=dict_mem['name'], part_number=dict_mem['part_number'],
        vendor=dict_mem['vendor'], price=0,desc_ukr=dict_mem['desc_ukr'], desc_ru=dict_mem['desc_ru'],
        fan_type_ua=dict_mem['cool_type_ua'], fan_type_rus=dict_mem['cool_type_ru'], fan_size=dict_mem['cool_fan_size'],
        depend_to=dict_mem['depend_to'], depend_to_type=dict_mem['depend_to_type'],fan_noise_level=dict_mem['cool_max_no'],
        fan_spd_ua=dict_mem['fan_spd_ua'],fan_spd_rus=dict_mem['fan_spd_rus'],is_active = True)

        if key_ in ('other_parts', 'both'):
            root_other = Cooler_OTHER.objects.create(root=cooler, r_price=0, cool_fan_am=dict_mem['cool_fan_am'],
                                                cool_tub_am=dict_mem['cool_tub_am'], cool_tub_con_ru=dict_mem['cool_tub_con_ru'],
                                                cool_tub_con_ua=dict_mem['cool_tub_con_ua'],
                                                cool_rad_mat_ru=dict_mem['cool_rad_mat_ru'],
                                                cool_rad_mat_ua=dict_mem['cool_rad_mat_ua'], cool_fix_ru=dict_mem['cool_fix_ru'],
                                                cool_fix_ua=dict_mem['cool_fix_ua'], cool_sock=dict_mem['cool_sock'],
                                                cool_fan_b_t_ru=dict_mem['cool_fan_b_t_ru'],
                                                cool_fan_b_t_ua=dict_mem['cool_fan_b_t_ua'],
                                                cool_fan_min_spd_ua=dict_mem['cool_fan_min_spd_ua'],
                                                cool_fan_min_spd_ru=dict_mem['cool_fan_min_spd_ru'],
                                                cool_fan_max_spd_ua=dict_mem['cool_fan_max_spd_ua'],
                                                cool_fan_max_spd_ru=dict_mem['cool_fan_max_spd_ru'],
                                                cool_fan_max_af=dict_mem['cool_fan_max_af'],
                                                cool_pwm=dict_mem['cool_pwm'], cool_max_tdp=dict_mem['cool_max_tdp'],
                                                cool_conn=dict_mem['cool_conn'], cool_col=dict_mem['cool_col'],
                                                cool_min_no=dict_mem['cool_min_no'], cool_h=dict_mem['cool_h'],
                                                cool_w=dict_mem['cool_w'])
            if key_ == 'other_parts':
                cooler.is_active = False
                cooler.save()
        return (count_obj, cooler.pk)

    if dict_mem['part_number'] and Cooler.objects.filter(part_number=dict_mem['part_number']).exists() and update == False:
        try:
            cooler = Cooler.objects.get(part_number=dict_mem['part_number'])
        except:
            cooler = Cooler.objects.filter(part_number=dict_mem['part_number']).first()
            count_obj = Cooler.objects.filter(part_number=dict_mem['part_number']).count()

        if key_ in ('other_parts', 'both'):
            try:
                test = cooler.root_other
            except:
                root_other = Cooler_OTHER.objects.create(root=cooler, r_price=0, cool_fan_am=dict_mem['cool_fan_am'],
                                                    cool_tub_am=dict_mem['cool_tub_am'], cool_tub_con_ru=dict_mem['cool_tub_con_ru'],
                                                    cool_tub_con_ua=dict_mem['cool_tub_con_ua'],
                                                    cool_rad_mat_ru=dict_mem['cool_rad_mat_ru'],
                                                    cool_rad_mat_ua=dict_mem['cool_rad_mat_ua'], cool_fix_ru=dict_mem['cool_fix_ru'],
                                                    cool_fix_ua=dict_mem['cool_fix_ua'], cool_sock=dict_mem['cool_sock'],
                                                    cool_fan_b_t_ru=dict_mem['cool_fan_b_t_ru'],
                                                    cool_fan_b_t_ua=dict_mem['cool_fan_b_t_ua'],
                                                    cool_fan_min_spd_ua=dict_mem['cool_fan_min_spd_ua'],
                                                    cool_fan_min_spd_ru=dict_mem['cool_fan_min_spd_ru'],
                                                    cool_fan_max_spd_ua=dict_mem['cool_fan_max_spd_ua'],
                                                    cool_fan_max_spd_ru=dict_mem['cool_fan_max_spd_ru'],
                                                    cool_fan_max_af=dict_mem['cool_fan_max_af'],
                                                    cool_pwm=dict_mem['cool_pwm'], cool_max_tdp=dict_mem['cool_max_tdp'],
                                                    cool_conn=dict_mem['cool_conn'], cool_col=dict_mem['cool_col'],
                                                    cool_min_no=dict_mem['cool_min_no'], cool_h=dict_mem['cool_h'],
                                                    cool_w=dict_mem['cool_w'])
        return (count_obj, cooler.pk)
    if update == True:
        c = Cooler.objects.get(name=dict_mem['name'])
        c.part_number=dict_mem['part_number']
        c.vendor=dict_mem['vendor']
        c.price=dict_mem['price']
        c.desc_ukr=dict_mem['desc_ukr']
        c.desc_ru=dict_mem['desc_ru']
        c.fan_type_ua=dict_mem['cool_type_ua']
        c.fan_type_rus=dict_mem['cool_type_ru']
        c.fan_noise_level=dict_mem['cool_max_no']
        c.fan_size=dict_mem['cool_fan_size']
        #c.depend_to=dict_mem['depend_to']
        #c.depend_to_type=dict_mem['depend_to_type']
        c.save()

        other = c.root_other

        other.r_price = dict_mem['r_price']
        other.cool_fan_am = dict_mem['cool_fan_am']
        other.cool_tub_am = dict_mem['cool_tub_am']
        other.cool_tub_con_ru = dict_mem['cool_tub_con_ru']
        other.cool_tub_con_ua = dict_mem['cool_tub_con_ua']
        other.cool_rad_mat_ru = dict_mem['cool_rad_mat_ru']
        other.cool_rad_mat_ua = dict_mem['cool_rad_mat_ua']
        other.cool_fix_ru = dict_mem['cool_fix_ru']
        other.cool_fix_ua = dict_mem['cool_fix_ua']
        other.cool_sock = dict_mem['cool_sock']
        other.cool_fan_b_t_ru = dict_mem['cool_fan_b_t_ru']
        other.cool_fan_b_t_ua = dict_mem['cool_fan_b_t_ua']
        other.cool_fan_min_spd_ua = dict_mem['cool_fan_min_spd_ua']
        other.cool_fan_min_spd_ru = dict_mem['cool_fan_min_spd_ru']
        other.cool_fan_max_spd_ua = dict_mem['cool_fan_max_spd_ua']
        other.cool_fan_max_spd_ru = dict_mem['cool_fan_max_spd_ru']
        other.cool_fan_max_af = dict_mem['cool_fan_max_af']
        other.cool_pwm = dict_mem['cool_pwm']
        other.cool_max_tdp = dict_mem['cool_max_tdp']
        other.cool_conn = dict_mem['cool_conn']
        other.cool_col = dict_mem['cool_col']
        other.cool_min_no = dict_mem['cool_min_no']
        other.cool_h = dict_mem['cool_h']
        other.cool_w = dict_mem['cool_w']
        other.cool_ai_ua = dict_mem['cool_ai_ua']
        other.cool_ai_ru = dict_mem['cool_ai_ru']
        other.cool_warr_ua = dict_mem['cool_warr_ua']
        other.cool_warr_ru = dict_mem['cool_warr_ru']
        other.you_vid = dict_mem['you_vid']
        other.label = dict_mem['label']
        other.creditoff = dict_mem['creditoff']
        other.save()

        return (count_obj, c.pk)

    return (count_obj, None)

def cpu_edition(dict_, art):
    dict_for_db = {}
    title = dict_['титл'] if 'титл' in dict_ else ''
    if title.lower().find('amd') != -1:
        dict_for_db['vendor'] = 'AMD'
    else:
        dict_for_db['vendor'] = 'Intel'
    dict_for_db['name'] = re.sub('amd|intel|box', '', title.lower()).strip().capitalize()
    dict_for_db['f_name'] = dict_for_db['name']
    dict_for_db['cpu_core_name'] = dict_['Кодовое название'] if 'Кодовое название' in dict_ else ''
    dict_for_db['cpu_fam'] = dict_['Серия'] if 'Серия' in dict_ else ''
    dict_for_db['cpu_soc'] = dict_['Разъем Socket '] if 'Разъем Socket ' in dict_ else ''
    core = dict_['Кол во ядер'] if 'Кол во ядер' in dict_ else ''
    threeds = dict_['Кол во потоков'] if 'Кол во потоков' in dict_ else ''
    if re.findall(r'(\d+)',core) and re.findall(r'(\d+)',threeds):
        dict_for_db['cpu_core'] = int(re.findall(r'(\d+)',core)[0])
        dict_for_db['cpu_threeds'] = int(re.findall(r'(\d+)',threeds)[0])
        dict_for_db['cpu_c_t'] = dict_for_db['f_cpu_c_t'] = f"{dict_for_db['cpu_core']}/{dict_for_db['cpu_threeds']}"
    else:
        dict_for_db['cpu_core'] = dict_for_db['cpu_threeds'] = dict_for_db['cpu_c_t'] = dict_for_db['f_cpu_c_t'] = ''
    dict_for_db['cpu_bfq'] = '.'.join(re.findall(r'\d+',dict_['Тактовая частота'])) + ' ГГц' if 'Тактовая частота' in dict_ else ''
    dict_for_db['cpu_tbfq'] = '.'.join(re.findall(r'\d+',dict_['Частота TurboBoost TurboCore'])) + ' ГГц' if 'Частота TurboBoost TurboCore' in dict_ else ''
    dict_for_db['cpu_cache'] = dict_['3 го уровня L3'] if '3 го уровня L3' in dict_ else ''
    dict_for_db['cpu_nm'] = dict_['Техпроцесс'] if 'Техпроцесс' in dict_ else ''
    dict_for_db['cpu_tdp'] = dict_['Тепловыделение TDP '] if 'Тепловыделение TDP ' in dict_ else ''
    dict_for_db['cpu_max_temp'] = dict_['Макс рабочая температура'] if 'Макс рабочая температура' in dict_ else '95 С'
    gpu = dict_['Модель IGP'] if 'Модель IGP' in dict_ else ''
    if gpu and gpu.lower().find('отсутствует') == -1:
        dict_for_db['cpu_gpu_model'] = gpu
        dict_for_db['cpu_gpu'] = '+'
    else:
        dict_for_db['cpu_gpu_model'] = dict_for_db['cpu_gpu'] = '-'
    dict_for_db['cpu_max_ram'] = dict_['Макс объем'] if 'Макс объем' in dict_ else ''
    dict_for_db['cpu_cha'] = dict_['Число каналов'] if 'Число каналов' in dict_ else '2'
    dict_for_db['cpu_bot'] = 'BOX' if title and title.lower().find('box') != -1 else 'tray'
    dict_for_db['cpu_warr_ua'] = ''
    dict_for_db['cpu_warr_ru'] = ''
    dict_for_db['cpu_i_g_ua'] = dict_for_db['cpu_gpu_model']
    dict_for_db['cpu_i_g_rus'] = dict_for_db['cpu_gpu_model']
    dict_for_db['you_vid'] = ''
    dict_for_db['label'] = ''
    dict_for_db['creditoff'] = ''
    dict_for_db['part_number'] = art
    dict_for_db['desc_ukr'] = CPU.objects.filter(vendor__icontains=dict_for_db['vendor']).first().desc_ukr if CPU.objects.first() else ''
    dict_for_db['desc_ru'] = CPU.objects.filter(vendor__icontains=dict_for_db['vendor']).first().desc_ru if CPU.objects.first() else ''

    return dict_for_db

def cpu_create(dict_mem, key_, update=False):
    count_obj = 0
    if dict_mem['part_number'] and not CPU.objects.filter(part_number=dict_mem['part_number']) and update == False:
        cpu = CPU.objects.create(name=dict_mem['name'], part_number=dict_mem['part_number'],
        vendor=dict_mem['vendor'], price=0,desc_ukr=dict_mem['desc_ukr'], desc_ru=dict_mem['desc_ru'],
        cpu_cache=dict_mem['cpu_cache'], cpu_i_g_ua=dict_mem['cpu_i_g_ua'], cpu_i_g_rus=dict_mem['cpu_i_g_rus'],
        f_name=dict_mem['f_name'], cpu_c_t=dict_mem['cpu_c_t'], f_cpu_c_t=dict_mem['f_cpu_c_t'], cpu_b_f=dict_mem['cpu_bfq'],
        is_active = True)

        if key_ in ('other_parts', 'both'):
            root_other = CPU_OTHER.objects.create(root=cpu, r_price=0, cpu_core_name=dict_mem['cpu_core_name'],
                                                cpu_fam=dict_mem['cpu_fam'], cpu_soc=dict_mem['cpu_soc'],
                                                cpu_core=dict_mem['cpu_core'], cpu_threeds=dict_mem['cpu_threeds'],
                                                cpu_tbfq=dict_mem['cpu_tbfq'], cpu_nm=dict_mem['cpu_nm'],
                                                cpu_tdp=dict_mem['cpu_tdp'], cpu_max_temp=dict_mem['cpu_max_temp'],
                                                cpu_gpu=dict_mem['cpu_gpu'], cpu_max_ram=dict_mem['cpu_max_ram'],
                                                cpu_cha=dict_mem['cpu_cha'], cpu_warr_ua=dict_mem['cpu_warr_ua'],
                                                cpu_warr_ru=dict_mem['cpu_warr_ru'], you_vid=dict_mem['you_vid'],
                                                label=dict_mem['label'], cpu_bot=dict_mem['cpu_bot'],
                                                cpu_gpu_model=dict_mem['cpu_gpu_model'],)
            if key_ == 'other_parts':
                cpu.is_active = False
                cpu.save()
        return (count_obj, cpu.pk)

    if dict_mem['part_number'] and CPU.objects.filter(part_number=dict_mem['part_number']).exists() and update == False:
        try:
            cpu = CPU.objects.get(part_number=dict_mem['part_number'])
        except:
            cpu = CPU.objects.filter(part_number=dict_mem['part_number']).first()
            count_obj = CPU.objects.filter(part_number=dict_mem['part_number']).count()

        if key_ in ('other_parts', 'both'):
            try:
                test = cpu.root_other
            except:
                root_other = CPU_OTHER.objects.create(root=cpu, r_price=0, cpu_core_name=dict_mem['cpu_core_name'],
                                                    cpu_fam=dict_mem['cpu_fam'], cpu_soc=dict_mem['cpu_soc'],
                                                    cpu_core=dict_mem['cpu_core'], cpu_threeds=dict_mem['cpu_threeds'],
                                                    cpu_tbfq=dict_mem['cpu_tbfq'], cpu_nm=dict_mem['cpu_nm'],
                                                    cpu_tdp=dict_mem['cpu_tdp'], cpu_max_temp=dict_mem['cpu_max_temp'],
                                                    cpu_gpu=dict_mem['cpu_gpu'], cpu_max_ram=dict_mem['cpu_max_ram'],
                                                    cpu_cha=dict_mem['cpu_cha'], cpu_warr_ua=dict_mem['cpu_warr_ua'],
                                                    cpu_warr_ru=dict_mem['cpu_warr_ru'], you_vid=dict_mem['you_vid'],
                                                    label=dict_mem['label'], cpu_bot=dict_mem['cpu_bot'],
                                                    cpu_gpu_model=dict_mem['cpu_gpu_model'])
        return (count_obj, cpu.pk)
    if update == True:
        c = CPU.objects.get(name=dict_mem['name'])
        c.part_number=dict_mem['part_number']
        c.vendor=dict_mem['vendor']
        c.price=dict_mem['price']
        c.desc_ukr=dict_mem['desc_ukr']
        c.desc_ru=dict_mem['desc_ru']
        #c.f_name=dict_mem['f_name']
        #c.cpu_c_t=dict_mem['cpu_c_t']
        #c.f_cpu_c_t=dict_mem['f_cpu_c_t']
        c.cpu_b_f=dict_mem['cpu_bfq']
        c.cpu_cache=dict_mem['cpu_cache']
        c.save()

        other = c.root_other

        other.r_price = dict_mem['r_price']
        other.cpu_core_name = dict_mem['cpu_core_name']
        other.cpu_fam = dict_mem['cpu_fam']
        other.cpu_soc = dict_mem['cpu_soc']
        other.cpu_core = dict_mem['cpu_core']
        other.cpu_threeds = dict_mem['cpu_threeds']
        other.cpu_tbfq = dict_mem['cpu_tbfq']
        other.cpu_nm = dict_mem['cpu_nm']
        other.cpu_tdp = dict_mem['cpu_tdp']
        other.cpu_max_temp = dict_mem['cpu_max_temp']
        other.cpu_gpu = dict_mem['cpu_gpu']
        other.cpu_max_ram = dict_mem['cpu_max_ram']
        other.cpu_cha = dict_mem['cpu_cha']
        other.cpu_gpu_model = dict_mem['cpu_gpu_model']
        other.cpu_bot = dict_mem['cpu_bot']
        other.cpu_warr_ua = dict_mem['cpu_warr_ua']
        other.cpu_warr_ru = dict_mem['cpu_warr_ru']
        other.cpu_ai_ua = dict_mem['cpu_ai_ua']
        other.cpu_ai_ru = dict_mem['cpu_ai_ru']
        other.you_vid = dict_mem['you_vid']
        other.label = dict_mem['label']
        other.creditoff = dict_mem['creditoff']
        other.save()

        return (count_obj, c.pk)

    return (count_obj, None)

def mem_edition(dict_, art):
    dict_for_db = {}
    vol = dict_['Объем памяти комплекта'] if 'Объем памяти комплекта' in dict_ else ''
    mul = dict_['Кол во планок в комплекте'] if 'Кол во планок в комплекте' in dict_ else ''
    if mul and re.findall(r'(\d) шт',mul) and int(re.findall(r'(\d) шт',mul)[0]) > 1:
        temp_mul = int(re.findall(r'(\d) шт',mul)[0])
        temp_vol = int(re.findall(r'(\d+) ГБ',vol)[0]) if vol and re.findall(r'(\d+) ГБ',vol) else 0
        if temp_vol:
            dict_for_db['mem_s'] = f'{temp_vol}Gb ({temp_mul}x{round(temp_vol/temp_mul)})'
    else:
        dict_for_db['mem_s'] = vol
    cool_type = dict_['Тип охлаждения'] if 'Тип охлаждения' in dict_ else ''
    if cool_type and isinstance(cool_type, str) and cool_type.lower().find('радиатор') != -1:
        dict_for_db['ram_cool_ua'] = 'Радіатор'
        dict_for_db['ram_cool_ru'] = 'Радиатор'
    else:
        dict_for_db['ram_cool_ua'] = '-'
        dict_for_db['ram_cool_ru'] = '-'
    ram_xmp = dict_['Дополнительно'] if 'Дополнительно' in dict_ else ''
    if isinstance(ram_xmp, str) and ram_xmp.lower().find('xmp') != -1:
        dict_for_db['ram_xmp'] = '+'
    else:
        dict_for_db['ram_xmp'] = '-'
    dict_for_db['ram_led'] = '-'
    dict_for_db['ram_col_ru'] = dict_['Цвет']
    dict_for_db['ram_col_ua'] = dict_['Цвет']
    title = dict_['титл'] if 'титл' in dict_ else ''
    if re.findall(r'(\S+)\s',title):
        dict_for_db['vendor'] = re.findall(r'(\S+)\s',title)[0]
    else:
        dict_for_db['vendor'] = ''

    dict_for_db['desc_ukr'] = RAM.objects.first().desc_ukr if RAM.objects.first() else ''
    dict_for_db['desc_ru'] = RAM.objects.first().desc_ru if RAM.objects.first() else ''
    dict_for_db['name'] = dict_['титл']
    dict_for_db['ram_size'] = dict_['Объем памяти комплекта']
    dict_for_db['ram_mod_am'] = dict_['Кол во планок в комплекте']
    dict_for_db['ram_type'] = dict_['Тип памяти'] if 'Тип памяти' in dict_ else ''
    dict_for_db['ram_fq'] = dict_['Тактовая частота'] if 'Тактовая частота' in dict_ else ''
    dict_for_db['mem_l'] = dict_['CAS латентность'] if 'CAS латентность' in dict_ else ''
    dict_for_db['ram_cl'] = dict_['Схема таймингов памяти'] if 'Схема таймингов памяти' in dict_ else ''
    dict_for_db['ram_pow'] = '.'.join(re.findall('\d+',dict_['Рабочее напряжение'])) + ' V' if 'Рабочее напряжение' in dict_ else ''
    dict_for_db['ram_warr_ua'] = ''
    dict_for_db['ram_warr_ru'] = ''
    dict_for_db['ram_ai_ua'] = ''
    dict_for_db['ram_ai_ru'] = ''
    dict_for_db['you_vid'] = ''
    dict_for_db['label'] = ''
    dict_for_db['part_number'] = art

    return dict_for_db

def mem_create(dict_mem, key_, update=False):
    count_obj = 0
    if dict_mem['part_number'] and not RAM.objects.filter(part_number=dict_mem['part_number']) and update == False:
        ram = RAM.objects.create(name=dict_mem['name'], part_number=dict_mem['part_number'],
        vendor=dict_mem['vendor'], price=0,mem_s=dict_mem['mem_s'],mem_l=dict_mem['mem_l'],
        desc_ukr=dict_mem['desc_ukr'], desc_ru=dict_mem['desc_ru'],
        f_name=dict_mem['ram_size'], mem_spd=dict_mem['ram_fq'],is_active = True)

        if key_ in ('other_parts', 'both'):
            root_other = RAM_OTHER.objects.create(root=ram, r_price=0, ram_mod_am=dict_mem['ram_mod_am'],
                                                ram_type=dict_mem['ram_type'], ram_cl=dict_mem['ram_cl'],
                                                ram_xmp=dict_mem['ram_xmp'], ram_pow=dict_mem['ram_pow'],
                                                ram_cool_ua=dict_mem['ram_cool_ua'], ram_cool_ru=dict_mem['ram_cool_ru'],
                                                ram_col_ua=dict_mem['ram_col_ua'], ram_col_ru=dict_mem['ram_col_ru'],
                                                ram_led=dict_mem['ram_led'], ram_warr_ua=dict_mem['ram_warr_ua'],
                                                ram_warr_ru=dict_mem['ram_warr_ru'], ram_ai_ua=dict_mem['ram_ai_ua'],
                                                ram_ai_ru=dict_mem['ram_ai_ru'], you_vid=dict_mem['you_vid'],
                                                label=dict_mem['label'])
            if key_ == 'other_parts':
                ram.is_active = False
                ram.save()
        return (count_obj, ram.pk)

    if dict_mem['part_number'] and RAM.objects.filter(part_number=dict_mem['part_number']).exists() and update == False:
        try:
            ram = RAM.objects.get(part_number=dict_mem['part_number'])
        except:
            ram = RAM.objects.filter(part_number=dict_mem['part_number']).first()
            count_obj = RAM.objects.filter(part_number=dict_mem['part_number']).count()

        if key_ in ('other_parts', 'both'):
            try:
                test = ram.root_other
            except:
                root_other = RAM_OTHER.objects.create(root=ram, r_price=0, ram_mod_am=dict_mem['ram_mod_am'],
                                                    ram_type=dict_mem['ram_type'], ram_cl=dict_mem['ram_cl'],
                                                    ram_xmp=dict_mem['ram_xmp'], ram_pow=dict_mem['ram_pow'],
                                                    ram_cool_ua=dict_mem['ram_cool_ua'], ram_cool_ru=dict_mem['ram_cool_ru'],
                                                    ram_col_ua=dict_mem['ram_col_ua'], ram_col_ru=dict_mem['ram_col_ru'],
                                                    ram_led=dict_mem['ram_led'], ram_warr_ua=dict_mem['ram_warr_ua'],
                                                    ram_warr_ru=dict_mem['ram_warr_ru'], ram_ai_ua=dict_mem['ram_ai_ua'],
                                                    ram_ai_ru=dict_mem['ram_ai_ru'], you_vid=dict_mem['you_vid'],
                                                    label=dict_mem['label'])
        return (count_obj, ram.pk)
    if update == True:
        c = RAM.objects.get(name=dict_mem['name'])
        c.part_number=dict_mem['part_number']
        c.vendor=dict_mem['vendor']
        c.price=dict_mem['price']
        c.desc_ukr=dict_mem['desc_ukr']
        c.desc_ru=dict_mem['desc_ru']
        c.f_name=dict_mem['ram_size']
        #c.mem_s=dict_mem['mem_s']
        c.mem_spd=dict_mem['ram_fq']
        #c.mem_l=dict_mem['mem_l']
        c.save()

        other = c.root_other

        other.r_price = dict_mem['r_price']
        other.ram_mod_am = dict_mem['ram_mod_am']
        other.ram_type = dict_mem['ram_type']
        other.ram_cl = dict_mem['ram_cl']
        other.ram_xmp = dict_mem['ram_xmp']
        other.ram_pow = dict_mem['ram_pow']
        other.ram_cool_ua = dict_mem['ram_cool_ua']
        other.ram_cool_ru = dict_mem['ram_cool_ru']
        other.ram_col_ua = dict_mem['ram_col_ua']
        other.ram_col_ru = dict_mem['ram_col_ru']
        other.ram_led = dict_mem['ram_led']
        other.ram_warr_ua = dict_mem['ram_warr_ua']
        other.ram_warr_ru = dict_mem['ram_warr_ru']
        other.ram_ai_ua = dict_mem['ram_ai_ua']
        other.ram_ai_ru = dict_mem['ram_ai_ru']
        other.you_vid = dict_mem['you_vid']
        other.label = dict_mem['label']
        other.creditoff = dict_mem['creditoff']
        other.save()

        return (count_obj, c.pk)

    return (count_obj, None)
