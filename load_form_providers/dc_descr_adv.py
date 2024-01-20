import json
import pandas as pd
import requests
from lxml import etree
from xml.etree.ElementTree import ParseError
import re

#from singleparts.models import *
from tech.models import *
from cat.models import Parts_full, USD, Results

def to_False_or_True(str_, cifar= False, str_or_minus=False):
    # str_ строку с разными знач в булево при cifar== False, str_or_minus==False
    # из-за возм-го наличия различных и
    # нужных данных ('1', '2', ..., "что-то") в этом вар-те
    # возвращ True
    # при cifar == True int or 0
    # при str_or_minus == True str_ or '-'

    to_get = False

    if cifar:
        to_get = 0
    if str_or_minus:
        to_get = '-'

    if not isinstance(str_, str):
        return to_get

    str_ = str_.lower().strip()

    dict_values = {
    'ні': False,
    'відсутній': False,
    'відсутня': False,
    'немає': False,
    'немає даних': False,
    'без підсвічування': False,
    'так': True,
    'є': True,
    'з мікрофоном': True,
    }

    if cifar:
        try:
            return int(str_)
        except ValueError:
            return to_get

    if str_or_minus:
        if str_ not in dict_values:
            return str_
        to_get = '+' if dict_values[str_] else '-'
        return to_get

    try:
        return dict_values[str_]
    except KeyError:
        return to_get

def get_discr_categ_dc(data, data_key):
    # создает описание характеристик товара по его data_key(внутр id DC)
    data_to_temp_dict = dict()
    try:
        data_to_temp_dict['values'] = {val[0]: val[1] for val in data['values']}
        data_to_temp_dict['properties'] = {val[0]: val[1] for val in data['properties']}
        data_to_temp_dict['items'] = {val[0]: val[1] for val in data['items'][data_key]}

        dict_res = {
        v: data_to_temp_dict['values'][data_to_temp_dict['items'][k]] for k, v\
        in  data_to_temp_dict['properties'].items() if k in data_to_temp_dict['items']
        }
    except:
        dict_res = {}

    return {data_key: dict_res}

def get_foto_price_name(dict_category_periphery, dc_products, dict_category_foto, name_t):
    # из словаря(полученного от get_from_xml) и list_periphery
    # получаем описания, список ссылок на фото, обработ цену, обработ имя

    res = get_discr_categ_dc(dict_category_periphery[dc_products['CategoryID']],
                            dc_products['Code'])

    foto_ = dict_category_foto[dc_products['CategoryID']]
    try:
        foto_ = foto_[dc_products['Code']]
    except:
        foto_ = ['пусто']
    foto_ = foto_ if len(foto_) > 1 else foto_ + foto_
    temp_price = float(dc_products['PriceUSD'])
    name_ = re.sub(
    name_t, '', dc_products['Name'][:99]
    )

    return (res, foto_, temp_price, name_)

def newMonitor(dict_category_periphery, dc_products, dict_category_foto):
    # создаем одиночный монитор
    # dc_products - получен из dc_dict[d['CategoryID']]['Article']
    name_t = 'Монитор '

    try:
        if Monitors.objects.filter(part_number=dc_products['Article']).exists():
            return False

        res, foto_, temp_price, name_ = get_foto_price_name(
        dict_category_periphery, dc_products, dict_category_foto, name_t)

        dvi = to_False_or_True(res[dc_products['Code']]['DVI'],
        cifar= True) if 'DVI' in res[dc_products['Code']] else 0
        D_Sub = to_False_or_True(res[dc_products['Code']]['D-Sub'],
        cifar= True) if 'D-Sub' in res[dc_products['Code']] else 0
        HDMI = to_False_or_True(res[dc_products['Code']]['HDMI'],
        cifar= True) if 'HDMI' in res[dc_products['Code']] else 0
        DisplayPort = to_False_or_True(res[dc_products['Code']]['DisplayPort'],
        cifar= True) if 'DisplayPort' in res[dc_products['Code']] else 0
        arch = to_False_or_True(
        res[dc_products['Code']]['Вигнутий екран'],
        ) if 'Вигнутий екран' in res[dc_products['Code']] else False
        audio = to_False_or_True(
        res[dc_products['Code']]['Вбудована аудіосистема'],
        ) if 'Вбудована аудіосистема' in res[dc_products['Code']] else False
        audio_p = to_False_or_True(
        res[dc_products['Code']]['Потужність аудіосистеми'],
        str_or_minus=True) if 'Потужність аудіосистеми' in res[
        dc_products['Code']] else '-'
        spin = to_False_or_True(
        res[dc_products['Code']]['Поворотний екран (Pivot)'],
        ) if 'Поворотний екран (Pivot)' in res[dc_products['Code']] else False
        h_reg = to_False_or_True(
        res[dc_products['Code']]['Регулювання по висоті'],
        ) if 'Регулювання по висоті' in res[dc_products['Code']] else False
        usb = to_False_or_True(
        res[dc_products['Code']]['Концентратор USB'],
        ) if 'Концентратор USB' in res[dc_products['Code']] else False
        game = to_False_or_True(
        res[dc_products['Code']]['Ігрові технології'],
        ) if 'Ігрові технології' in res[dc_products['Code']] else '-'
        fi = to_False_or_True(
        res[dc_products['Code']]['Безрамковий монітор'],
        ) if 'Безрамковий монітор' in res[dc_products['Code']] else False


        Monitors.objects.create(
        name=name_,
        is_active=False,
        full=False,
        category_ru='Монитор',
        category_ua='Монiтор',
        part_number=dc_products['Article'],
        price_rent=round(temp_price * 1.05 * 37),
        r_price=round(temp_price * 1.05 * 37),
        price_ua=round(temp_price * 37),
        price_usd=temp_price,
        vendor=dc_products['Vendor'],
        sc_d=res[dc_products['Code']]['Діагональ екрану'],
        sc_r=res[dc_products['Code']]['Роздільна здатність екрану'],
        sc_t=res[dc_products['Code']]['Тип матриці'],
        sc_ss=res[dc_products['Code']]["Співвідношення сторін"],
        sc_l=res[dc_products['Code']]['Час реакції'],
        sc_v=res[dc_products['Code']]['Кут огляду'],
        sc_b=res[dc_products['Code']]['Яскравість'],
        sc_s=res[dc_products['Code']]['Контрастність'],
        sc_h=res[dc_products['Code']]['Частота оновлення'],
        sc_surf_ua=res[dc_products['Code']]['Поверхня екрану'],
        sc_d_sub=D_Sub,
        sc_dvi=dvi,
        sc_hdmi=HDMI,
        sc_dp=DisplayPort,
        sc_arch=arch,
        sc_spk=audio,
        sc_spk_p=audio_p,
        sc_spin=spin,
        sc_hight=h_reg,
        sc_usb=usb,
        sc_fi=fi,
        sc_os=game,
        sc_vesa=res[dc_products['Code']]['Кріплення на стіну'],
        sc_vol=res[dc_products['Code']]['Габарити (ШхВхГ)'],
        sc_weight=res[dc_products['Code']]['Вага'],
        sc_col_ua=res[dc_products['Code']]['Колір'],

        sc_warr_ua=dc_products['Warranty'],
        sc_warr_ru=dc_products['Warranty'],
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

def newKM(dict_category_periphery, dc_products, dict_category_foto):
    # создаем одиночный KM
    # dc_products - получен из dc_dict[d['CategoryID']]['Article']
    name_t = 'Комплект (клавиатура+мышь) '

    try:
        if KM.objects.filter(part_number=dc_products['Article']).exists():
            return False

        res, foto_, temp_price, name_ = get_foto_price_name(
        dict_category_periphery, dc_products, dict_category_foto, name_t)

        light = to_False_or_True(
        res[dc_products['Code']]['Підсвічування (клавіатура)']
        ) if 'Підсвічування (клавіатура)' in res[dc_products['Code']] else False
        km_ua_ = to_False_or_True(
        res[dc_products['Code']]['Українська розкладка']
        ) if 'Українська розкладка' in res[dc_products['Code']] else False
        buttoms = to_False_or_True(
        res[dc_products['Code']]['Кількість клавіш (клавіатура)'],
        cifar= True) if 'Кількість клавіш (клавіатура)' in res[
        dc_products['Code']] else 0
        mouse_light = to_False_or_True(
        res[dc_products['Code']]['Підсвічування (миша)']
        ) if 'Підсвічування (миша)' in res[dc_products['Code']] else False
        mouse_w = to_False_or_True(
        res[dc_products['Code']]['Вага (клавіатура)'],
        str_or_minus= True) if 'Вага (клавіатура)' in res[dc_products['Code']] else '-'
        k_w = to_False_or_True(
        res[dc_products['Code']]['Вага (миша)'],
        str_or_minus= True) if 'Вага (миша)' in res[dc_products['Code']] else '-'

        KM.objects.create(
        name=name_,
        is_active=False,
        full=False,
        category_ru='Комплект (клавиатура+мышь)',
        category_ua='Комплект (клавіатура, мишка)',
        part_number=dc_products['Article'],
        price_rent=round(temp_price * 1.05 * 37),
        r_price=round(temp_price * 1.05 * 37),
        price_ua=round(temp_price * 37),
        price_usd=temp_price,
        vendor=dc_products['Vendor'],
        km_connect_ua=res[dc_products['Code']]['Підключення'],
        km_int=res[dc_products['Code']]['Інтерфейс'],
        km_key_type_ua=res[dc_products['Code']]['Тип клавіш (клавіатура)'],
        km_k_light=light,
        km_ua=km_ua_,
        km_pow_k_ua=res[dc_products['Code']]['Живлення (клавіатура)'],
        km_sensor_ua=res[dc_products['Code']]['Тип сенсора (миша)'],
        km_numb_buttoms=buttoms,
        km_dpi=res[dc_products['Code']]['Роздільна здатність (миша)'],
        km_mouse_light=mouse_light,
        km_pow_mouse_ua=res[dc_products['Code']]['Живлення (миша)'],
        km_k_vol=res[dc_products['Code']]['Габарити (клавіатура)'],
        km_mouse_vol=res[dc_products['Code']]['Габариты (мышь)'],
        km_k_weight=mouse_w,
        km_mouse_weight=k_w,
        km_col_ua=res[dc_products['Code']]['Колір'],

        km_warr_ua=dc_products['Warranty'],
        km_warr_ru=dc_products['Warranty'],
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


def newKeyboards(dict_category_periphery, dc_products, dict_category_foto):
    # создаем одиночный Keyboards
    # dc_products - получен из dc_dict[d['CategoryID']]['Article']
    name_t = 'Клавиатура '

    try:
        if Keyboards.objects.filter(part_number=dc_products['Article']).exists():
            return False

        res, foto_, temp_price, name_ = get_foto_price_name(
        dict_category_periphery, dc_products, dict_category_foto, name_t)

        kb_light_ = to_False_or_True(
        res[dc_products['Code']]['Підсвічування клавіш']
        ) if 'Підсвічування клавіш' in res[dc_products['Code']] else False
        kb_rgb_ = to_False_or_True(
        res[dc_products['Code']]['Наявність RGB']
        ) if 'Наявність RGB' in res[dc_products['Code']] else False
        kb_res_ = to_False_or_True(
        res[dc_products['Code']]['Вологостійкість']
        ) if 'Вологостійкість' in res[dc_products['Code']] else False
        plus_but = to_False_or_True(
        res[dc_products['Code']]['Додаткові клавіші'],
        cifar= True) if 'Додаткові клавіші' in res[dc_products['Code']] else 0

        kb_usb_ = to_False_or_True(
        res[dc_products['Code']]['USB']
        ) if 'USB' in res[dc_products['Code']] else False
        kb_ps_ = to_False_or_True(
        res[dc_products['Code']]['PS/2']
        ) if 'PS/2' in res[dc_products['Code']] else False
        kb_bt_ = to_False_or_True(
        res[dc_products['Code']]['Bluetooth']
        ) if 'Bluetooth' in res[dc_products['Code']] else False
        kb_usb_resiver_ = to_False_or_True(
        res[dc_products['Code']]['USB-ресивер']
        ) if 'USB-ресивер' in res[dc_products['Code']] else False
        kb_usb_type_c_ = to_False_or_True(
        res[dc_products['Code']]['USB Type-C']
        ) if 'USB Type-C' in res[dc_products['Code']] else False
        kb_vol_ = to_False_or_True(
        res[dc_products['Code']]['Габарити'],
        str_or_minus= True) if 'Габарити' in res[dc_products['Code']] else '-'
        kb_weight_ = to_False_or_True(
        res[dc_products['Code']]['Вага'],
        str_or_minus= True) if 'Вага' in res[dc_products['Code']] else '-'
        try:
            kb_type_con_ua_ = to_False_or_True(
            res[dc_products['Code']]['Тип підключення'],
            str_or_minus=True)
        except:
            kb_type_con_ua_ = '-'
        try:
            kb_type_but_ua_ = to_False_or_True(
            res[dc_products['Code']]['Тип клавіш'],
            str_or_minus=True)
        except:
            kb_type_but_ua_ = '-'
        try:
            kb_type_pow_ua_ = to_False_or_True(
            res[dc_products['Code']]['Джерело живлення'],
            str_or_minus=True)
        except:
            kb_type_pow_ua_ = '-'
        try:
            kb_form_ua_ = to_False_or_True(
            res[dc_products['Code']]['Форм-фактор'],
            str_or_minus=True)
        except:
            kb_form_ua_ = '-'
        try:
            kb_type_conn_ = to_False_or_True(
            res[dc_products['Code']]['Тип перемикачів'],
            str_or_minus=True)
        except:
            kb_type_conn_ = '-'

        Keyboards.objects.create(
        name=name_,
        is_active=False,
        full=False,
        category_ru='Клавиатура',
        category_ua='Клавіатура',
        part_number=dc_products['Article'],
        price_rent=round(temp_price * 1.05 * 37),
        r_price=round(temp_price * 1.05 * 37),
        price_ua=round(temp_price * 37),
        price_usd=temp_price,
        vendor=dc_products['Vendor'],
        kb_plus_but=plus_but,
        kb_light=kb_light_,
        kb_rgb=kb_rgb_,
        kb_res=kb_res_,
        kb_cab_long=res[dc_products['Code']]['Довжина кабеля'],
        kb_leng=res[dc_products['Code']]['Розкладка'],
        kb_vol=kb_vol_,
        kb_weight=kb_weight_,
        kb_usb=kb_usb_,
        kb_ps=kb_ps_,
        kb_bt=kb_bt_,
        kb_usb_resiver=kb_usb_resiver_,
        kb_usb_type_c=kb_usb_type_c_,
        kb_col_ua=res[dc_products['Code']]['Колір'],
        kb_type_con_ua = kb_type_con_ua_,
        kb_type_but_ua = kb_type_but_ua_,
        kb_type_pow_ua = kb_type_pow_ua_,
        kb_form_ua = kb_form_ua_,
        kb_type_conn = kb_type_conn_,

        kb_warr_ua=dc_products['Warranty'],
        kb_warr_ru=dc_products['Warranty'],
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


def newMouses(dict_category_periphery, dc_products, dict_category_foto):
    # создаем одиночный Mouses
    # dc_products - получен из dc_dict[d['CategoryID']]['Article']
    name_t = 'Мышь '

    try:
        if Mouses.objects.filter(part_number=dc_products['Article']).exists():
            return False

        res, foto_, temp_price, name_ = get_foto_price_name(
        dict_category_periphery, dc_products, dict_category_foto, name_t)

        buttoms = to_False_or_True(
        res[dc_products['Code']]['Кількість кнопок'],
        cifar= True) if 'Кількість кнопок' in res[dc_products['Code']] else 0

        Mouses.objects.create(
        name=name_,
        is_active=False,
        full=False,
        category_ru='Мышь',
        category_ua='Мишка',
        part_number=dc_products['Article'],
        price_rent=round(temp_price * 1.05 * 37),
        r_price=round(temp_price * 1.05 * 37),
        price_ua=round(temp_price * 37),
        price_usd=temp_price,
        vendor=dc_products['Vendor'],
        mouse_type_connect_ua=res[dc_products['Code']]["Тип з'єднання"],
        mouse_int='-',
        mouse_sensor_ua=res[dc_products['Code']]["Тип сенсора"],
        mouse_dpi=res[dc_products['Code']]["Роздільна здатність сенсора"],
        mouse_numb_buttoms=buttoms,
        mouse_pow_ua=res[dc_products['Code']]['Тип живлення'],
        mouse_length_cable=res[dc_products['Code']]['Довжина кабелю'],
        mouse_vol=res[dc_products['Code']]['Розмір'],
        mouse_weight=res[dc_products['Code']]['Вага'],
        mouse_col_ua=res[dc_products['Code']]['Колір'],

        mouse_warr_ua=dc_products['Warranty'],
        mouse_warr_ru=dc_products['Warranty'],
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


def newPads(dict_category_periphery, dc_products, dict_category_foto):
    # создаем одиночный Pads
    # dc_products - получен из dc_dict[d['CategoryID']]['Article']
    name_t = 'Коврик для мыши |Игровая поверхность '

    try:
        if Pads.objects.filter(part_number=dc_products['Article']).exists():
            return False

        res, foto_, temp_price, name_ = get_foto_price_name(
        dict_category_periphery, dc_products, dict_category_foto, name_t)

        pad_light_ = to_False_or_True(
        res[dc_products['Code']]['Наявність підсвічування']
        ) if 'Наявність підсвічування' in res[dc_products['Code']] else False

        Pads.objects.create(
        name=name_,
        is_active=False,
        full=False,
        category_ru='Коврик для мыши',
        category_ua='Килимок для миші',
        part_number=dc_products['Article'],
        price_rent=round(temp_price * 1.05 * 37),
        r_price=round(temp_price * 1.05 * 37),
        price_ua=round(temp_price * 37),
        price_usd=temp_price,
        vendor=dc_products['Vendor'],
        pad_bot_ua=res[dc_products['Code']]["Матеріал"],
        pad_vol=res[dc_products['Code']]["Габарити"],
        pad_light=pad_light_,
        pad_col_ua=res[dc_products['Code']]['Колір'],

        pad_warr_ua=dc_products['Warranty'],
        pad_warr_ru=dc_products['Warranty'],
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


def newHeadsets(dict_category_periphery, dc_products, dict_category_foto):
    # создаем одиночный Headsets
    # dc_products - получен из dc_dict[d['CategoryID']]['Article']
    name_t = 'гарнитура '

    try:
        if Headsets.objects.filter(part_number=dc_products['Article']).exists():
            return False

        res, foto_, temp_price, name_ = get_foto_price_name(
        dict_category_periphery, dc_products, dict_category_foto, name_t)

        try:
            mike = res[dc_products['Code']]['Наявність мікрофону']
        except:
            mike = 'y'
        hs_mike_avail_ = False if mike.find('з мікрофоном') == -1 else True
        hs_interface_ = to_False_or_True(
        res[dc_products['Code']]['3.5 мм (mini-jack)']
        ) if '3.5 мм (mini-jack)' in res[dc_products['Code']] else False
        hs_usb_ = to_False_or_True(
        res[dc_products['Code']]['USB']
        ) if 'USB' in res[dc_products['Code']] else False
        hs_usb_type_c_ = to_False_or_True(
        res[dc_products['Code']]['USB Type-C']
        ) if 'USB Type-C' in res[dc_products['Code']] else False
        hs_water_res_ = to_False_or_True(
        res[dc_products['Code']]['Вологостійкість']
        ) if 'Вологостійкість' in res[dc_products['Code']] else False
        hs_light_ = to_False_or_True(
        res[dc_products['Code']]['Наявність підсвічування']
        ) if 'Наявність підсвічування' in res[dc_products['Code']] else False
        hs_resistance_ = to_False_or_True(
        res[dc_products['Code']]['Опір навушників'],
        str_or_minus=True) if 'Опір навушників' in res[dc_products['Code']] else '-'
        hs_weight_ = to_False_or_True(
        res[dc_products['Code']]['Вага'],
        str_or_minus=True) if 'Вага' in res[dc_products['Code']] else '-'
        hs_time_ = to_False_or_True(
        res[dc_products['Code']]['Час роботи розмова/очікування'],
        str_or_minus=True) if 'Час роботи розмова/очікування' in res[
        dc_products['Code']] else '-'
        hs_con_type_ = to_False_or_True(
        res[dc_products['Code']]['Тип бездротового підключення'],
        str_or_minus=True) if 'Тип бездротового підключення' in res[
        dc_products['Code']] else '-'
        hs_ver_ = to_False_or_True(
        res[dc_products['Code']]['Версія Bluetooth'],
        str_or_minus=True) if 'Версія Bluetooth' in res[dc_products['Code']] else '-'

        Headsets.objects.create(
        name=name_,
        is_active=False,
        full=False,
        category_ru='Гарнитура',
        category_ua='Гарнітура',
        part_number=dc_products['Article'],
        price_rent=round(temp_price * 1.05 * 37),
        r_price=round(temp_price * 1.05 * 37),
        price_ua=round(temp_price * 37),
        price_usd=temp_price,
        vendor=dc_products['Vendor'],
        hs_type_connect_ua=res[dc_products['Code']]['Тип підключення'],
        hs_sound_range=res[dc_products['Code']]['Частотний діапазон'],
        hs_resistance=hs_resistance_,
        hs_purpose_ua=res[dc_products['Code']]['Призначення'],
        hs_type_ua=res[dc_products['Code']]['Тип навушників'],
        hs_s_type_ua=res[dc_products['Code']]['Тип гарнітури'],
        hs_mike_ua=res[dc_products['Code']]['Конструкція мікрофону'],
        hs_mike_avail=hs_mike_avail_,
        hs_cable_length=res[dc_products['Code']]['Довжина кабелю'],
        hs_interface=hs_interface_,
        hs_usb=hs_usb_,
        hs_usb_type_c=hs_usb_type_c_,
        hs_col_ua=res[dc_products['Code']]['Колір'],

        hs_weight=hs_weight_,
        hs_ear_pads_material_ua=res[dc_products['Code']]['Матеріал амбушюр'],
        hs_metal_pads_material_ua=res[dc_products['Code']]['Матеріал корпусу'],
        hs_time=hs_time_,
        hs_con_type=hs_con_type_,
        hs_water_res=hs_water_res_,
        hs_light=hs_light_,
        hs_pow_ua=res[dc_products['Code']]['Живлення'],
        hs_ver = hs_ver_,

        hs_warr_ua=dc_products['Warranty'],
        hs_warr_ru=dc_products['Warranty'],
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


def newWebcams(dict_category_periphery, dc_products, dict_category_foto):
    # создаем одиночный Webcams
    # dc_products - получен из dc_dict[d['CategoryID']]['Article']
    name_t = 'Веб-камера '

    try:
        if Webcams.objects.filter(part_number=dc_products['Article']).exists():
            return False

        res, foto_, temp_price, name_ = get_foto_price_name(
        dict_category_periphery, dc_products, dict_category_foto, name_t)

        web_mike_ = to_False_or_True(
        res[dc_products['Code']]['Мікрофон']
        ) if 'Мікрофон' in res[dc_products['Code']] else False
        web_max_f_ = to_False_or_True(
        res[dc_products['Code']]['Максимальна частота кадрів відео'],
        cifar=True) if 'Максимальна частота кадрів відео' in res[
        dc_products['Code']] else 0
        web_focus_ = to_False_or_True(
        res[dc_products['Code']]['Фокусування'],
        str_or_minus=True) if 'Фокусування' in res[dc_products['Code']] else '-'
        web_weight_ = to_False_or_True(
        res[dc_products['Code']]['Вага (г)'],
        str_or_minus=True) if 'Вага (г)' in res[dc_products['Code']] else '-'

        Webcams.objects.create(
        name=name_,
        is_active=False,
        full=False,
        category_ru='Веб-камера',
        category_ua='Веб-камера',
        part_number=dc_products['Article'],
        price_rent=round(temp_price * 1.05 * 37),
        r_price=round(temp_price * 1.05 * 37),
        price_ua=round(temp_price * 37),
        price_usd=temp_price,
        vendor=dc_products['Vendor'],
        web_r=res[dc_products['Code']]["Роздільна здатність"],
        web_pixel=res[dc_products['Code']]["Кількість мегапікселів веб-камери"],
        web_type_sensor=res[dc_products['Code']]["Тип сенсора"],
        web_mike=web_mike_,

        web_focus=web_focus_,
        web_int=res[dc_products['Code']]["Інтерфейси"],
        web_angle=res[dc_products['Code']]["Кут огляду"],
        web_max_f=web_max_f_,
        web_weight=web_weight_,
        web_col_ua=res[dc_products['Code']]["Колір"],

        web_warr_ua=dc_products['Warranty'],
        web_warr_ru=dc_products['Warranty'],
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


def newWiFis(dict_category_periphery, dc_products, dict_category_foto):
    # создаем одиночный WiFis
    # dc_products - получен из dc_dict[d['CategoryID']]['Article']
    name_t = 'Беспроводной адаптер '

    try:
        if WiFis.objects.filter(part_number=dc_products['Article']).exists():
            return False

        res, foto_, temp_price, name_ = get_foto_price_name(
        dict_category_periphery, dc_products, dict_category_foto, name_t)

        net_wifi_bt_ = to_False_or_True(
        res[dc_products['Code']]['Підтримка Bluetooth']
        ) if 'Підтримка Bluetooth' in res[dc_products['Code']] else False
        net_wifi_ant_am_ = to_False_or_True(
        res[dc_products['Code']]['Зовнішні антени'],
        cifar=True) if 'Зовнішні антени' in res[dc_products['Code']] else 0

        WiFis.objects.create(
        name=name_,
        is_active=False,
        full=False,
        category_ru='Беспроводной адаптер',
        category_ua='Бездротовий адаптер',
        part_number=dc_products['Article'],
        price_rent=round(temp_price * 1.05 * 37),
        r_price=round(temp_price * 1.05 * 37),
        price_ua=round(temp_price * 37),
        price_usd=temp_price,
        vendor=dc_products['Vendor'],
        net_wifi_int=res[dc_products['Code']]["Інтерфейс підключення"],
        net_wifi_ant_am=net_wifi_ant_am_,
        net_wifi_st=res[dc_products['Code']]["Стандарти Wi-Fi"],
        net_wifi_ghz=res[dc_products['Code']]['Частота роботи Wi-Fi'],
        net_wifi_bt=net_wifi_bt_,

        net_wifi_warr_ua=dc_products['Warranty'],
        net_wifi_warr_ru=dc_products['Warranty'],
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


def newAcoustics(dict_category_periphery, dc_products, dict_category_foto):
    # создаем одиночный Acoustics
    # dc_products - получен из dc_dict[d['CategoryID']]['Article']
    name_t = 'Акустическая система '

    try:
        if Acoustics.objects.filter(part_number=dc_products['Article']).exists():
            return False

        res, foto_, temp_price, name_ = get_foto_price_name(
        dict_category_periphery, dc_products, dict_category_foto, name_t)

        a_usb_ = to_False_or_True(
        res[dc_products['Code']]['USB']
        ) if 'USB' in res[dc_products['Code']] else False
        a_card_ = to_False_or_True(
        res[dc_products['Code']]['Кардрідер']
        ) if 'Кардрідер' in res[dc_products['Code']] else False
        a_wifi_ = to_False_or_True(
        res[dc_products['Code']]['Wi-Fi']
        ) if 'Wi-Fi' in res[dc_products['Code']] else False
        a_bt_ = to_False_or_True(
        res[dc_products['Code']]['Bluetooth']
        ) if 'Bluetooth' in res[dc_products['Code']] else False
        a_fm_ = to_False_or_True(
        res[dc_products['Code']]['FM-приймач']
        ) if 'FM-приймач' in res[dc_products['Code']] else False
        a_control_ = to_False_or_True(
        res[dc_products['Code']]['Пульт ДК']
        ) if 'Пульт ДК' in res[dc_products['Code']] else False
        a_audio_ = to_False_or_True(
        res[dc_products['Code']]["Аудіо"],
        str_or_minus=True
        ) if 'Аудіо' in res[dc_products['Code']] else '-'

        Acoustics.objects.create(
        name=name_,
        is_active=False,
        full=False,
        category_ru='Акустическая система',
        category_ua='Акустична система',
        part_number=dc_products['Article'],
        price_rent=round(temp_price * 1.05 * 37),
        r_price=round(temp_price * 1.05 * 37),
        price_ua=round(temp_price * 37),
        price_usd=temp_price,
        vendor=dc_products['Vendor'],
        a_format=res[dc_products['Code']]['Формат акустики'],
        a_p=res[dc_products['Code']]['Потужність'],
        a_f=res[dc_products['Code']]['Частотний діапазон'],
        a_s_n=res[dc_products['Code']]['Співвідношення сигнал/шум'],
        a_audio=a_audio_,
        a_usb=a_usb_,
        a_card=a_card_,
        a_wifi=a_wifi_,
        a_bt=a_bt_,
        a_fm=a_fm_,
        a_control=a_control_,
        a_pow_ua=res[dc_products['Code']]['Живлення'],
        a_bot_ua=res[dc_products['Code']]['Матеріал корпусу'],
        a_vol=res[dc_products['Code']]['Габарити'],
        a_weight=res[dc_products['Code']]['Вага'],
        a_col_ua=res[dc_products['Code']]['Колір'],

        a_warr_ua=dc_products['Warranty'],
        a_warr_ru=dc_products['Warranty'],
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


def newTables(dict_category_periphery, dc_products, dict_category_foto):
    # создаем одиночный Tables
    # dc_products - получен из dc_dict[d['CategoryID']]['Article']
    name_t = 'Геймерский стол '

    try:
        if Tables.objects.filter(part_number=dc_products['Article']).exists():
            return False

        res, foto_, temp_price, name_ = get_foto_price_name(
        dict_category_periphery, dc_products, dict_category_foto, name_t)

        tb_led_ = to_False_or_True(
        res[dc_products['Code']]['Світлодіодне підсвічування']
        ) if 'Світлодіодне підсвічування' in res[dc_products['Code']] else False
        tb_h_ = to_False_or_True(
        res[dc_products['Code']]['Регулятор висоти']
        ) if 'Регулятор висоти' in res[dc_products['Code']] else False
        tb_angle_ = to_False_or_True(
        res[dc_products['Code']]['Регулятор нахилу']
        ) if 'Регулятор нахилу' in res[dc_products['Code']] else False
        tb_up_ = to_False_or_True(
        res[dc_products['Code']]['Надставка']
        ) if 'Надставка' in res[dc_products['Code']] else False
        tb_in_ = to_False_or_True(
        res[dc_products['Code']]['Висувна поліця для клавіатури']
        ) if 'Висувна поліця для клавіатури' in res[dc_products['Code']] else False
        tb_box_ = to_False_or_True(
        res[dc_products['Code']]['Висувні ящики']
        ) if 'Висувні ящики' in res[dc_products['Code']] else False
        tb_wheels_ = to_False_or_True(
        res[dc_products['Code']]["Наявність коліс"]
        ) if 'Наявність коліс' in res[dc_products['Code']] else False
        tb_cab_ = to_False_or_True(
        res[dc_products['Code']]['Кабельне введення']
        ) if 'Кабельне введення' in res[dc_products['Code']] else False
        tb_down_ = to_False_or_True(
        res[dc_products['Code']]["Підставка під системний блок"]
        ) if 'Підставка під системний блок' in res[dc_products['Code']] else False
        tb_bot_r_ua_ = to_False_or_True(
        res[dc_products['Code']]["Матеріал рами"],
        str_or_minus=True
        ) if 'Матеріал рами' in res[dc_products['Code']] else '-'

        Tables.objects.create(
        name=name_,
        is_active=False,
        full=False,
        category_ru='Геймерский стол',
        category_ua='Геймерський стіл',
        part_number=dc_products['Article'],
        price_rent=round(temp_price * 1.05 * 37),
        r_price=round(temp_price * 1.05 * 37),
        price_ua=round(temp_price * 37),
        price_usd=temp_price,
        vendor=dc_products['Vendor'],
        tb_format_ua=res[dc_products['Code']]['Форма'],
        tb_led=tb_led_,
        tb_h=tb_h_,
        tb_angle=tb_angle_,
        tb_up=tb_up_,
        tb_in=tb_in_,
        tb_box=tb_box_,
        tb_wheels=tb_wheels_,
        tb_cab=tb_cab_,
        tb_down=tb_down_,
        tb_bot_t_ua=res[dc_products['Code']]['Матеріал стільниці'],
        tb_bot_r_ua=tb_bot_r_ua_,
        tb_hight=res[dc_products['Code']]['Висота'],
        tb_width=res[dc_products['Code']]['Ширина'],
        tb_depth=res[dc_products['Code']]['Глибина'],
        tb_weight=res[dc_products['Code']]['Вага'],
        tb_col_ua=res[dc_products['Code']]['Колір'],

        tb_warr_ua=dc_products['Warranty'],
        tb_warr_ru=dc_products['Warranty'],
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


def newChairs(dict_category_periphery, dc_products, dict_category_foto):
    # создаем одиночный Chairs
    # dc_products - получен из dc_dict[d['CategoryID']]['Article']
    name_t = 'Кресло для геймеров '

    try:
        if Chairs.objects.filter(part_number=dc_products['Article']).exists():
            return False

        res, foto_, temp_price, name_ = get_foto_price_name(
        dict_category_periphery, dc_products, dict_category_foto, name_t)

        ch_hand_ = to_False_or_True(
        res[dc_products['Code']]['Регулювання підлокітників']
        ) if 'Регулювання підлокітників' in res[dc_products['Code']] else False
        ch_hight_ = to_False_or_True(
        res[dc_products['Code']]['Регулювання висоти сидіння']
        ) if 'Регулювання висоти сидіння' in res[dc_products['Code']] else False
        try:
            frame_ = res[dc_products['Code']]['Каркас ']
        except:
            frame_ = '-'

        Chairs.objects.create(
        name=name_,
        is_active=False,
        full=False,
        category_ru='Кресло для геймеров',
        category_ua='Крісло для геймерів',
        part_number=dc_products['Article'],
        price_rent=round(temp_price * 1.05 * 37),
        r_price=round(temp_price * 1.05 * 37),
        price_ua=round(temp_price * 37),
        price_usd=temp_price,
        vendor=dc_products['Vendor'],
        ch_type_ua=res[dc_products['Code']]['Тип'],
        ch_main_ua=res[dc_products['Code']]['Основа'],
        ch_chr_ua=res[dc_products['Code']]['Хрестовина'],
        ch_mat_ua=res[dc_products['Code']]['Оббивка'],
        ch_frame_ua=frame_,
        ch_vol=res[dc_products['Code']]['Розміри сидіння'],
        ch_back=res[dc_products['Code']]['Розміри спинки'],
        ch_back_angle=res[dc_products['Code']]['Кут нахилу спинки'],
        ch_hand=ch_hand_,
        ch_hight=ch_hight_,
        ch_mech_ua=res[dc_products['Code']]['Вбудовані механізми'],
        ch_max_weight=res[dc_products['Code']]['Максимально допустиме навантаження'],
        ch_weight=res[dc_products['Code']]['Вага'],
        ch_col_ua=res[dc_products['Code']]['Колір'],

        ch_warr_ua=dc_products['Warranty'],
        ch_warr_ru=dc_products['Warranty'],
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


def newCabelsplus(dict_category_periphery, dc_products, dict_category_foto):
    # создаем одиночный Cabelsplus
    # dc_products - получен из dc_dict[d['CategoryID']]['Article']
    name_t = 'Адаптер |Кабель '

    try:
        if Cabelsplus.objects.filter(part_number=dc_products['Article']).exists():
            return False

        res, foto_, temp_price, name_ = get_foto_price_name(
        dict_category_periphery, dc_products, dict_category_foto, name_t)

        cab_flat_ = to_False_or_True(
        res[dc_products['Code']]['Плаский кабель']
        ) if 'Плаский кабель' in res[dc_products['Code']] else False
        cab_tissue_ = to_False_or_True(
        res[dc_products['Code']]['Тканинне обплетення']
        ) if 'Тканинне обплетення' in res[dc_products['Code']] else False
        cab_metal_ = to_False_or_True(
        res[dc_products['Code']]['Металеве обплетення']
        ) if 'Металеве обплетення' in res[dc_products['Code']] else False
        cab_g_type_ = to_False_or_True(
        res[dc_products['Code']]['Г-подібний']
        ) if 'Г-подібний' in res[dc_products['Code']] else False

        Cabelsplus.objects.create(
        name=name_,
        is_active=False,
        full=False,
        category_ru='Адаптер_Кабель',
        category_ua='Адаптер_Кабель',
        part_number=dc_products['Article'],
        price_rent=round(temp_price * 1.05 * 37),
        r_price=round(temp_price * 1.05 * 37),
        price_ua=round(temp_price * 37),
        price_usd=temp_price,
        vendor=dc_products['Vendor'],
        cab_con_f=res[dc_products['Code']]["Роз'єм 1"],
        cab_con_s=res[dc_products['Code']]["Роз'єм 2"],
        cab_conn_ua=res[dc_products['Code']]['Конектори'],
        cab_flat=cab_flat_,
        cab_tissue=cab_tissue_,
        cab_metal=cab_metal_,
        cab_g_type=cab_g_type_,
        cab_ver='-',
        cab_long=res[dc_products['Code']]['Довжина кабеля'],
        cab_col_ua=res[dc_products['Code']]['Колір'],

        cab_warr_ua=dc_products['Warranty'],
        cab_warr_ru=dc_products['Warranty'],
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


def newFilters(dict_category_periphery, dc_products, dict_category_foto):
    # создаем одиночный Filters
    # dc_products - получен из dc_dict[d['CategoryID']]['Article']
    name_t = 'Фильтр питания |Сетевой фильтр |Сетевой удлинитель '

    try:
        if Filters.objects.filter(part_number=dc_products['Article']).exists():
            return False

        res, foto_, temp_price, name_ = get_foto_price_name(
        dict_category_periphery, dc_products, dict_category_foto, name_t)

        fi_con_ = to_False_or_True(
        res[dc_products['Code']]['Вимикач']
        ) if 'Вимикач' in res[dc_products['Code']] else False

        Filters.objects.create(
        name=name_,
        is_active=False,
        full=False,
        category_ru='Фильтр питания',
        category_ua='Фільтр живлення',
        part_number=dc_products['Article'],
        price_rent=round(temp_price * 1.05 * 37),
        r_price=round(temp_price * 1.05 * 37),
        price_ua=round(temp_price * 37),
        price_usd=temp_price,
        vendor=dc_products['Vendor'],
        fi_num=res[dc_products['Code']]["Кількість розеток"],
        fi_cab_lenght=res[dc_products['Code']]["Довжина кабеля"],
        fi_u=res[dc_products['Code']]['Робоча напруга'],
        fi_max_i=res[dc_products['Code']]['Максимальна сила струму'],
        fi_max_pow=res[dc_products['Code']]['Максимальна сумарна потужність навантаження'],
        fi_con=fi_con_,
        fi_bot_ua=res[dc_products['Code']]['Матеріал'],
        fi_col_ua=res[dc_products['Code']]['Колір'],

        fi_warr_ua=dc_products['Warranty'],
        fi_warr_ru=dc_products['Warranty'],
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
