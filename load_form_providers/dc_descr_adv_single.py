import json
import pandas as pd
import requests
from lxml import etree
from xml.etree.ElementTree import ParseError
import re

from singleparts.models import *
#from tech.models import *
from cat.models import Parts_full, USD, Results
from .dc_descr_adv import to_False_or_True,get_discr_categ_dc,get_foto_price_name

def newCPU(dict_category_periphery, dc_products, dict_category_foto):
    # создаем одиночный CPU
    # dc_products - получен из dc_dict[d['CategoryID']]['Article']
    name_t = 'Процессор |Процесор '

    try:
        if CPU_OTHER.objects.filter(part_number=dc_products['Article']).exists():
            return False

        res, foto_, temp_price, name_ = get_foto_price_name(
        dict_category_periphery, dc_products, dict_category_foto, name_t)

        CPU_OTHER.objects.create(
        name=name_,
        is_active=False,
        full=False,
        category_ru='Процессор',
        category_ua='Процесор',
        part_number=dc_products['Article'],
        price_rent=round(temp_price * 1.05 * 37),
        r_price=round(temp_price * 1.05 * 37),
        price_ua=round(temp_price * 37),
        price_usd=temp_price,
        vendor=dc_products['Vendor'],
        cpu_fam=res[dc_products['Code']]['Сімейство процесора'],
        cpu_bfq=re.split('-', res[dc_products['Code']]['Внутрішня тактова частота (ГГц)'])[0],
        cpu_cache=res[dc_products['Code']]['Кеш L3'],
        cpu_soc='-',
        cpu_core=res[dc_products['Code']]['Кількість ядер процесора'],
        cpu_threeds=res[dc_products['Code']]['Кількість потоків'],
        cpu_tbfq=re.split('-', res[dc_products['Code']]['Внутрішня тактова частота (ГГц)'])[-1],
        cpu_gpu=res[dc_products['Code']]['Інтегрована графіка'],
        cpu_warr_ua=dc_products['Warranty'],
        cpu_warr_ru=dc_products['Warranty'],
        cover1=foto_[0],
        cover2=foto_[1],
        cover3=foto_[-1],
        )
    except Exception as e:
        try:
            print(dc_products['Article'], e)
            return False
        except Exception as es:
            print(es)
            return False

    return True


def newCASE(dict_category_periphery, dc_products, dict_category_foto):
    # создаем одиночный CASE_OTHER
    # dc_products - получен из dc_dict[d['CategoryID']]['Article']
    name_t = 'Корпус '

    try:
        if CASE_OTHER.objects.filter(part_number=dc_products['Article']).exists():
            return False

        res, foto_, temp_price, name_ = get_foto_price_name(
        dict_category_periphery, dc_products, dict_category_foto, name_t)

        try:
            ps = False if res[dc_products['Code']]['Потужність блоку живлення'].find(
            'немає') != -1 else True
        except:
            ps = '-'
        led = res[dc_products['Code']][
        'Підсвічування'] if 'Підсвічування' in res[dc_products['Code']] else '-'
        window = res[dc_products['Code']][
        'Наявність бокового вікна'] if 'Наявність бокового вікна' in res[
        dc_products['Code']] else '-'
        psu_position = res[dc_products['Code']][
        'Розташування блоку живлення'] if 'Розташування блоку живлення' in res[
        dc_products['Code']] else '-'

        CASE_OTHER.objects.create(
        name=name_,
        is_active=False,
        full=False,
        category_ru='Корпус',
        category_ua='Корпус',
        part_number=dc_products['Article'],
        price_rent=round(temp_price * 1.05 * 37),
        r_price=round(temp_price * 1.05 * 37),
        price_ua=round(temp_price * 37),
        price_usd=temp_price,
        vendor=dc_products['Vendor'],
        case_mb=res[dc_products['Code']]['Форм-фактор материнської плати'],
        case_color_ua=res[dc_products['Code']]['Колір'],
        case_color_ru=res[dc_products['Code']]['Колір'],
        case_fan=res[dc_products['Code']]['Кількість встановлених вентиляторів'],
        case_psu_p = ps,
        case_rgb = led,
        case_sp_m_ua = window,
        case_sp_m_ru = window,
        case_psu_w_ua = psu_position,
        case_psu_w_ru = psu_position,
        case_s = dc_products['Subcategory'],
        case_warr_ua=dc_products['Warranty'],
        case_warr_ru=dc_products['Warranty'],
        cover1=foto_[0],
        cover2=foto_[1],
        cover3=foto_[-1],
        )
    except Exception as e:
        try:
            print(dc_products['Article'], e)
            return False
        except Exception as es:
            print(es)
            return False

    return True


def newHDD(dict_category_periphery, dc_products, dict_category_foto):
    # создаем одиночный HDD_OTHER
    # dc_products - получен из dc_dict[d['CategoryID']]['Article']
    name_t = 'Накопитель |Накопичувач '

    try:
        if HDD_OTHER.objects.filter(part_number=dc_products['Article']).exists():
            return False

        res, foto_, temp_price, name_ = get_foto_price_name(
        dict_category_periphery, dc_products, dict_category_foto, name_t)

        HDD_OTHER.objects.create(
        name=name_,
        is_active=False,
        full=False,
        category_ru='Накопитель',
        category_ua='Накопичувач',
        part_number=dc_products['Article'],
        price_rent=round(temp_price * 1.05 * 37),
        r_price=round(temp_price * 1.05 * 37),
        price_ua=round(temp_price * 37),
        price_usd=temp_price,
        vendor=dc_products['Vendor'],
        hdd_size=res[dc_products['Code']]["Об'єм жорсткого диска"],
        hdd_spd_ph_ua=res[dc_products['Code']]['Швидкість обертання (об/хв)'],
        hdd_spd_ph_ru=res[dc_products['Code']]['Швидкість обертання (об/хв)'],
        hdd_buf=res[dc_products['Code']]["Об'єм буфера (MB)"],
        hdd_ff=res[dc_products['Code']]['Форм-фактор'],
        hdd_warr_ua=dc_products['Warranty'],
        hdd_warr_ru=dc_products['Warranty'],
        cover1=foto_[0],
        cover2=foto_[1],
        cover3=foto_[-1],
        )
    except Exception as e:
        try:
            print(dc_products['Article'], e)
            return False
        except Exception as es:
            print(es)
            return False

    return True


def newPSU(dict_category_periphery, dc_products, dict_category_foto):
    # создаем одиночный PSU_OTHER
    # dc_products - получен из dc_dict[d['CategoryID']]['Article']
    name_t = 'Блок питания |Блок живлення '

    try:
        if PSU_OTHER.objects.filter(part_number=dc_products['Article']).exists():
            return False

        res, foto_, temp_price, name_ = get_foto_price_name(
        dict_category_periphery, dc_products, dict_category_foto, name_t)

        psu_mod_ = res[dc_products['Code']]['Модульне підключення']
        psu_mod_ = False if psu_mod_ == 'нет' else True

        PSU_OTHER.objects.create(
        name=name_,
        is_active=False,
        full=False,
        category_ru='Блок питания',
        category_ua='Блок живлення',
        part_number=dc_products['Article'],
        price_rent=round(temp_price * 1.05 * 37),
        r_price=round(temp_price * 1.05 * 37),
        price_ua=round(temp_price * 37),
        price_usd=temp_price,
        vendor=dc_products['Vendor'],
        psu_pow=res[dc_products['Code']]['Потужність'],
        psu_fan=res[dc_products['Code']]['Охолодження'],
        psu_ff=res[dc_products['Code']]['Форм-фактор'],
        psu_mod = psu_mod_,
        psu_warr_ua=dc_products['Warranty'],
        psu_warr_ru=dc_products['Warranty'],
        cover1=foto_[0],
        cover2=foto_[1],
        cover3=foto_[-1],
        )
    except Exception as e:
        try:
            print(dc_products['Article'], e)
            return False
        except Exception as es:
            print(es)
            return False

    return True


def newGPU(dict_category_periphery, dc_products, dict_category_foto):
    # создаем одиночный GPU_OTHER
    # dc_products - получен из dc_dict[d['CategoryID']]['Article']
    name_t = 'Видеокарта |Відеокарта '

    try:
        if GPU_OTHER.objects.filter(part_number=dc_products['Article']).exists():
            return False

        res, foto_, temp_price, name_ = get_foto_price_name(
        dict_category_periphery, dc_products, dict_category_foto, name_t)

        vga = False if res[dc_products['Code']]['D-Sub'].find(
        'відсутній') != -1 else True
        hdmi = False if res[dc_products['Code']]['HDMI'].find(
        'відсутній') != -1 else True
        dp = False if res[dc_products['Code']]['DisplayPort'].find(
        'відсутній') != -1 else True
        dvi = False if res[dc_products['Code']]['DVI'].find(
        'відсутній') != -1 else True
        try:
            gpu_mem_type_ = res[dc_products['Code']]["Тип пам'яті"]
        except:
            gpu_mem_type_ = '-'
        try:
            gpu_core_fq_ = res[dc_products['Code']]['Частота ядра, МГц']
        except:
            gpu_core_fq_ = '-'
        try:
            gpu_mem_fq_ = res[dc_products['Code']]["Частота пам'яті, МГц"]
        except:
            gpu_mem_fq_ = '-'
        try:
            gpu_pci_type_ = res[dc_products['Code']]['Інтерфейс підключення']
        except:
            gpu_pci_type_ = '-'
        try:
            gpu_watt_ = res[dc_products['Code']]['Рекомендована потужність блоку живлення']
        except:
            gpu_watt_ = '-'

        GPU_OTHER.objects.create(
        name=name_,
        is_active=False,
        full=False,
        category_ru='Видеокарта',
        category_ua='Відеокарта',
        part_number=dc_products['Article'],
        price_rent=round(temp_price * 1.05 * 37),
        r_price=round(temp_price * 1.05 * 37),
        price_ua=round(temp_price * 37),
        price_usd=temp_price,
        vendor=dc_products['Vendor'],
        gpu_main_category=res[dc_products['Code']]['Виробник відеокарти'],
        gpu_model=res[dc_products['Code']]['Графічний чіп'],
        gpu_mem_size=res[dc_products['Code']]["Об'єм пам'яті"],
        gpu_bit=res[dc_products['Code']]["Шина пам'яті"],
        gpu_fan=res[dc_products['Code']]['Кількість вентиляторів'],
        gpu_max_l=res[dc_products['Code']]['Довжина відеокарти'],
        gpu_mem_type = gpu_mem_type_,
        gpu_core_fq = gpu_core_fq_,
        gpu_mem_fq = gpu_mem_fq_,
        gpu_pci_type = gpu_pci_type_,
        gpu_watt = gpu_watt_,
        gpu_vga=vga,
        gpu_dvi=dvi,
        gpu_hdmi=hdmi,
        gpu_dp=dp,
        gpu_warr_ua=dc_products['Warranty'],
        gpu_warr_ru=dc_products['Warranty'],
        cover1=foto_[0],
        cover2=foto_[1],
        cover3=foto_[-1],
        )
    except Exception as e:
        try:
            print(dc_products['Article'], e)
            return False
        except Exception as es:
            print(es)
            return False

    return True


def newSSD(dict_category_periphery, dc_products, dict_category_foto):
    # создаем одиночный SSD_OTHER
    # dc_products - получен из dc_dict[d['CategoryID']]['Article']
    name_t = 'Накопитель |Накопичувач '

    try:
        if SSD_OTHER.objects.filter(part_number=dc_products['Article']).exists():
            return False

        res, foto_, temp_price, name_ = get_foto_price_name(
        dict_category_periphery, dc_products, dict_category_foto, name_t)

        SSD_OTHER.objects.create(
        name=name_,
        is_active=False,
        full=False,
        category_ru='Накопитель',
        category_ua='Накопичувач',
        part_number=dc_products['Article'],
        price_rent=round(temp_price * 1.05 * 37),
        r_price=round(temp_price * 1.05 * 37),
        price_ua=round(temp_price * 37),
        price_usd=temp_price,
        vendor=dc_products['Vendor'],
        ssd_size=res[dc_products['Code']]["Об'єм накопичувача"],
        ssd_nand=res[dc_products['Code']]["Тип пам'яті"],
        ssd_ff=res[dc_products['Code']]['Форм-фактор'],
        ssd_int=res[dc_products['Code']]["Інтерфейс"],
        part_ssd_r_spd=res[dc_products['Code']]['Швидкість зчитування'],
        part_ssd_w_spd=res[dc_products['Code']]['Швидкість запису'],
        ssd_warr_ua=dc_products['Warranty'],
        ssd_warr_ru=dc_products['Warranty'],
        cover1=foto_[0],
        cover2=foto_[1],
        cover3=foto_[-1],
        )
    except Exception as e:
        try:
            print(dc_products['Article'], e)
            return False
        except Exception as es:
            print(es)
            return False

    return True


def newRAM(dict_category_periphery, dc_products, dict_category_foto):
    # создаем одиночный RAM_OTHER
    # dc_products - получен из dc_dict[d['CategoryID']]['Article']
    name_t = "Модуль памяти |Модуль пам'яті "

    try:
        if RAM_OTHER.objects.filter(part_number=dc_products['Article']).exists():
            return False

        res, foto_, temp_price, name_ = get_foto_price_name(
        dict_category_periphery, dc_products, dict_category_foto, name_t)

        size = res[dc_products['Code']]["Об'єм одного модуля"]
        num = res[dc_products['Code']]["Кількість модулів у комплекті"]
        size_num = f'{size} * {num}'
        ram_led_ = res[dc_products['Code']]['Наявність підсвічування']
        ram_led_ = False if ram_led_ == 'без підсвічування' else True
        ram_ti = res[dc_products['Code']]["Таймінги"] if "Таймінги" in res[
        dc_products['Code']] else '-'

        RAM_OTHER.objects.create(
        name=name_,
        is_active=False,
        full=False,
        category_ru='Модуль памяти',
        category_ua="Модуль пам'яті",
        part_number=dc_products['Article'],
        price_rent=round(temp_price * 1.05 * 37),
        r_price=round(temp_price * 1.05 * 37),
        price_ua=round(temp_price * 37),
        price_usd=temp_price,
        vendor=dc_products['Vendor'],
        ram_size=size_num,
        ram_cl = ram_ti,
        ram_led = ram_led_,
        ram_fq=res[dc_products['Code']]["Частота пам'яті"],
        ram_type=res[dc_products['Code']]["Тип оперативної пам'яті"],
        ram_mod_am=num,
        ram_col_ua=res[dc_products['Code']]['Колір'],
        ram_col_ru=res[dc_products['Code']]['Колір'],
        ram_warr_ua=dc_products['Warranty'],
        ram_warr_ru=dc_products['Warranty'],
        cover1=foto_[0],
        cover2=foto_[1],
        cover3=foto_[-1],
        )
    except Exception as e:
        try:
            print(dc_products['Article'], e)
            return False
        except Exception as es:
            print(es)
            return False

    return True


def newCooler(dict_category_periphery, dc_products, dict_category_foto):
    # создаем одиночный Cooler_OTHER
    # dc_products - получен из dc_dict[d['CategoryID']]['Article']
    name_t = "Вентилятор |процесорний |Кулер| процессорний "

    try:
        if Cooler_OTHER.objects.filter(part_number=dc_products['Article']).exists():
            return False

        res, foto_, temp_price, name_ = get_foto_price_name(
        dict_category_periphery, dc_products, dict_category_foto, name_t)

        rgb = res[dc_products['Code']]['Підсвічування']
        rgb = rgb if rgb.find('немає') == -1 else '-'
        s1=';1200' if res[dc_products['Code']]['Socket 1200'].find('немає')==-1 else ''
        s2=';am3' if res[dc_products['Code']]['Socket AM3+'].find('немає')==-1 else ''
        s3=';am4' if res[dc_products['Code']]['Socket AM4'].find('немає')==-1 else ''
        s4=';2066' if res[dc_products['Code']]['Socket 2066'].find('немає')==-1 else ''
        s5=';trx4' if res[dc_products['Code']]['Socket TRX4'].find('немає')==-1 else ''
        s6=';1700' if res[dc_products['Code']]['Socket 1700'].find('немає')==-1 else ''
        s7=';tr4' if res[dc_products['Code']]['Socket TR4'].find('немає')==-1 else ''
        s8=';2011' if res[dc_products['Code']]['Socket 2011'].find('немає')==-1 else ''
        s9=';1151' if res[dc_products['Code']]['Socket 1151'].find('немає')==-1 else ''
        s10=';am5' if res[dc_products['Code']]['Socket AM5'].find('немає')==-1 else ''
        sock = f'{s1}{s2}{s3}{s4}{s5}{s6}{s7}{s8}{s9}{s10}'

        Cooler_OTHER.objects.create(
        name=name_,
        is_active=False,
        full=False,
        category_ru='Кулер процессорный',
        category_ua='Кулер процесорний',
        part_number=dc_products['Article'],
        price_rent=round(temp_price * 1.05 * 37),
        r_price=round(temp_price * 1.05 * 37),
        price_ua=round(temp_price * 37),
        price_usd=temp_price,
        vendor=dc_products['Vendor'],
        cool_fan_max_spd_ua=res[dc_products['Code']][
        'Максимальна швидкість обертання, об/хв'],
        cool_fan_max_spd_ru=res[dc_products['Code']][
        'Максимальна швидкість обертання, об/хв'],
        cool_fan_size=res[dc_products['Code']]['Діаметр вентилятора'],
        cool_sock=sock, #
        cool_max_tdp=res[dc_products['Code']]['Максимальний TDP (для ЦП і відеокарт)'],
        cool_col_ua=res[dc_products['Code']]['Колір'],
        cool_col_ru=res[dc_products['Code']]['Колір'],
        cool_rgb=rgb,
        cool_h=res[dc_products['Code']]['Висота системи охолодження'],
        cool_warr_ua=dc_products['Warranty'],
        cool_warr_ru=dc_products['Warranty'],
        cover1=foto_[0],
        cover2=foto_[1],
        cover3=foto_[-1],
        )
    except Exception as e:
        try:
            print(dc_products['Article'], e)
            return False
        except Exception as es:
            print(es)
            return False

    return True


def newMB(dict_category_periphery, dc_products, dict_category_foto):
    # создаем одиночный MB_OTHER
    # dc_products - получен из dc_dict[d['CategoryID']]['Article']
    name_t = "Материнская |плата |Материнська  "

    try:
        if MB_OTHER.objects.filter(part_number=dc_products['Article']).exists():
            return False

        res, foto_, temp_price, name_ = get_foto_price_name(
        dict_category_periphery, dc_products, dict_category_foto, name_t)

        header = True if res[dc_products['Code']][
        'Контроль підсвічування'].find('немає')==-1 else False
        raid = True if res[dc_products['Code']][
        'RAID 10'].find('немає')==-1 else False
        vga = True if res[dc_products['Code']][
        'D-Sub'].find('немає')==-1 else False
        dvi = True if res[dc_products['Code']][
        'DVI'].find('немає')==-1 else False
        hdmi = True if res[dc_products['Code']][
        'HDMI'].find('немає')==-1 else False
        dp = True if res[dc_products['Code']][
        'Display Port'].find('немає')==-1 else False
        lan = True if res[dc_products['Code']][
        'Мережевий адаптер (LAN)'].find('немає')==-1 else False
        wifi = True if res[dc_products['Code']][
        'Wi-Fi'].find('немає')==-1 else False
        bt = True if res[dc_products['Code']][
        'Bluetooth'].find('немає')==-1 else False
        usbtc = True if res[dc_products['Code']][
        'USB Type-C'].find('немає')==-1 else False

        MB_OTHER.objects.create(
        name=name_,
        is_active=False,
        full=False,
        category_ru='Материнская плата',
        category_ua='Материнська плата',
        part_number=dc_products['Article'],
        price_rent=round(temp_price * 1.05 * 37),
        r_price=round(temp_price * 1.05 * 37),
        price_ua=round(temp_price * 37),
        price_usd=temp_price,
        vendor=dc_products['Vendor'],
        part_mb_fam=res[dc_products['Code']]['Для процесорів'],
        part_mb_chip=res[dc_products['Code']]['Чіпсет'],
        part_mb_ram_max_size=res[dc_products['Code']][
        "Максимальний об'єм оперативної пам'яті"],
        part_mb_ram_sl=res[dc_products['Code']]["Кількість слотів пам'яті"].strip(),
        part_mb_ram_type=res[dc_products['Code']]["Тип оперативної пам'яті"].strip(),
        part_mb_sock=res[dc_products['Code']]['Сокет'],
        part_mb_ff=res[dc_products['Code']]['Форм-фактор'],
        part_mb_rgb_header=header,
        part_mb_sata=res[dc_products['Code']]["Роз'єм SATA "],
        part_mb_m2=res[dc_products['Code']]['M.2'],
        part_mb_raid=raid,
        part_mb_vga=vga,
        part_mb_dvi=dvi,
        part_mb_hdmi=hdmi,
        part_mb_dp=dp,
        part_mb_lan=lan,
        part_mb_wifi=wifi,
        part_mb_bt=bt,
        part_mb_usb_type_c=usbtc,
        part_mb_warr_ua=dc_products['Warranty'],
        part_mb_warr_ru=dc_products['Warranty'],
        cover1=foto_[0],
        cover2=foto_[1],
        cover3=foto_[-1],
        )
    except Exception as e:
        try:
            print(dc_products['Article'], e)
            return False
        except Exception as es:
            print(es)
            return False

    return True


def newFAN(dict_category_periphery, dc_products, dict_category_foto):
    # создаем одиночный FAN_OTHER
    # dc_products - получен из dc_dict[d['CategoryID']]['Article']
    name_t = "Вентилятор  "

    try:
        if FAN_OTHER.objects.filter(part_number=dc_products['Article']).exists():
            return False

        res, foto_, temp_price, name_ = get_foto_price_name(
        dict_category_periphery, dc_products, dict_category_foto, name_t)

        rgb = res[dc_products['Code']]['Підсвічування']
        rgb = rgb if rgb.find('немає') == -1 else '-'

        FAN_OTHER.objects.create(
        name=name_,
        is_active=False,
        full=False,
        category_ru='Вентилятор',
        category_ua='Вентилятор',
        part_number=dc_products['Article'],
        price_rent=round(temp_price * 1.05 * 37),
        r_price=round(temp_price * 1.05 * 37),
        price_ua=round(temp_price * 37),
        price_usd=temp_price,
        vendor=dc_products['Vendor'],
        fan_max_spd_ua=res[dc_products['Code']][
        'Максимальна швидкість обертання, об/хв'],
        fan_max_spd_ru=res[dc_products['Code']][
        'Максимальна швидкість обертання, об/хв'],
        part_fan_size=res[dc_products['Code']]['Діаметр вентилятора'],
        fan_b_type_ru=res[dc_products['Code']]["Тип підшипника"],
        fan_b_type_ua=res[dc_products['Code']]['Тип підшипника'],
        fan_quantity=res[dc_products['Code']]['Кількість вентиляторів'],
        fan_pow=res[dc_products['Code']]["Тип роз'єму"],
        fan_led_type_ua=rgb,
        fan_led_type_ru=rgb,
        fan_col_ua=res[dc_products['Code']]["Колір"],
        fan_col_ru=res[dc_products['Code']]["Колір"],
        fan_warr_ua=dc_products['Warranty'],
        fan_warr_ru=dc_products['Warranty'],
        cover1=foto_[0],
        cover2=foto_[1],
        cover3=foto_[-1],
        )
    except Exception as e:
        try:
            print(dc_products['Article'], e)
            return False
        except Exception as es:
            print(es)
            return False

    return True


def newFAN(dict_category_periphery, dc_products, dict_category_foto):
    # создаем одиночный FAN_OTHER
    # dc_products - получен из dc_dict[d['CategoryID']]['Article']
    name_t = "Вентилятор  "

    try:
        if FAN_OTHER.objects.filter(part_number=dc_products['Article']).exists():
            return False

        res, foto_, temp_price, name_ = get_foto_price_name(
        dict_category_periphery, dc_products, dict_category_foto, name_t)

        rgb = res[dc_products['Code']]['Підсвічування']
        rgb = rgb if rgb.find('немає') == -1 else '-'

        FAN_OTHER.objects.create(
        name=name_,
        is_active=False,
        full=False,
        category_ru='Вентилятор',
        category_ua='Вентилятор',
        part_number=dc_products['Article'],
        price_rent=round(temp_price * 1.05 * 37),
        r_price=round(temp_price * 1.05 * 37),
        price_ua=round(temp_price * 37),
        price_usd=temp_price,
        vendor=dc_products['Vendor'],
        fan_max_spd_ua=res[dc_products['Code']][
        'Максимальна швидкість обертання, об/хв'],
        fan_max_spd_ru=res[dc_products['Code']][
        'Максимальна швидкість обертання, об/хв'],
        part_fan_size=res[dc_products['Code']]['Діаметр вентилятора'],
        fan_b_type_ru=res[dc_products['Code']]["Тип підшипника"],
        fan_b_type_ua=res[dc_products['Code']]['Тип підшипника'],
        fan_quantity=res[dc_products['Code']]['Кількість вентиляторів'],
        fan_pow=res[dc_products['Code']]["Тип роз'єму"],
        fan_led_type_ua=rgb,
        fan_led_type_ru=rgb,
        fan_col_ua=res[dc_products['Code']]["Колір"],
        fan_col_ru=res[dc_products['Code']]["Колір"],
        fan_warr_ua=dc_products['Warranty'],
        fan_warr_ru=dc_products['Warranty'],
        cover1=foto_[0],
        cover2=foto_[1],
        cover3=foto_[-1],
        )
    except Exception as e:
        try:
            print(dc_products['Article'], e)
            return False
        except Exception as es:
            print(es)
            return False

    return True
