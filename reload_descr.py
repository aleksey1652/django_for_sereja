from load_form_providers.load_element import *
from descriptions.models import *

proc = pd.read_excel('proc.xlsx',header=None)
proc_=proc.rename(columns={0: 'part_number', 1: 'vendor',2:'name', 3:'f_name',4:'price',5:'desc_ukr',7:'cpu_c_t',
            8:'f_cpu_c_t',6:'desc_ru', 9:'cpu_b_f',10:'cpu_cache',11:'cpu_i_g_ua',12:'cpu_i_g_rus',13:'depend_from',
            14:'depend_from_type'})

cool = pd.read_excel('cool.xlsx', header=None)
cool_=cool.rename(columns={0: 'part_number', 1: 'vendor',2:'name',3:'price',4:'desc_ukr',6:'fan_type_ua', 7: 'fan_type_rus',
            8:'fan_spd_ua',5:'desc_ru', 9:'fan_spd_rus',10:'fan_noise_level',11:'fan_size',12:'depend_to',13:'depend_to_type',
            14:'cooler_height'})

mb = pd.read_excel('mb.xlsx', header=None)
mb_=mb.rename(columns={0: 'part_number', 1: 'vendor',2:'main_category',3:'name',4:'price',6:'desc_ru', 7: 'mb_chipset',
            8:'mb_max_ram',5:'desc_ukr', 9:'depend_to',10:'depend_to_type',11:'depend_from',12:'depend_from_type'})

ram = pd.read_excel('ram.xlsx', header=None)
ram_=ram.rename(columns={0: 'part_number', 1: 'vendor',2:'name',3:'f_name',4:'price',6:'desc_ru', 7: 'mem_s',
            8:'mem_spd',5:'desc_ukr', 9:'mem_l'})

gpu = pd.read_excel('gpu.xlsx', header=None)
gpu_=gpu.rename(columns={0: 'part_number', 1: 'vendor',2:'main_category',3:'name',4:'f_name',6:'price', 7: 'desc_ukr',
            8:'desc_ru',5:'gpu_fps', 9:'gpu_m_s',10:'gpu_b',11:'gpu_cpu_spd',12:'gpu_mem_spd',13:'depend_to',
            14:'depend_to_type'})

case = pd.read_excel('case.xlsx', header=None)
case_=case.rename(columns={0: 'part_number', 1: 'vendor',2:'name',3:'price',4:'desc_ukr',6:'case_s', 7: 'color_parent',
            8:'color',5:'desc_ru', 9:'color_ukr',10:'color_ru',11:'depend_to',12:'depend_to_type',13:'case_height'})

wifi = pd.read_excel('wifi.xlsx', header=None)
wifi_=wifi.rename(columns={0: 'part_number', 1: 'vendor',2:'name',3:'r_price',4:'price',6:'desc_ru', 7: 'net_type_ukr',
            8:'net_type_rus',5:'desc_ukr', 9:'net_max_spd',10:'net_stand',11:'net_int'})

soft = pd.read_excel('soft.xlsx', header=None)
soft_=soft.rename(columns={0: 'part_number', 1: 'vendor',2:'name',3:'r_price',4:'price',6:'desc_ru', 7: 'soft_type_ukr',
            8:'soft_type_ru',5:'desc_ukr', 9:'soft_lang_ukr',10:'soft_lang_ru',11:'soft_set'})

cables = pd.read_excel('cables.xlsx', header=None)
cables_=cables.rename(columns={0: 'part_number', 1: 'vendor',2:'name',3:'r_price',4:'desc_ukr',6:'cab_mat_ukr', 7: 'cab_mat_ru',
            8:'cab_col_ukr',5:'desc_ru', 9:'cab_col_ru',10:'cab_set'})

def delete_nan(pd_):
    values_list = ['' if isinstance(p, float) and not float(p) > 0  else p for p in pd_.values]
    return pd.Series(values_list, index=list(pd_.index))

def proc_reload(proc_):
    for p in proc_.iloc:
        if isinstance(p.part_number, str) and p.part_number != 'part_number':
            p = delete_nan(p)
            if CPU.objects.filter(name=p['name']).exists():
                CPU.objects.filter(name=p['name']).update(
                                vendor=p.vendor,
                                desc_ukr=p.desc_ukr,desc_ru=p.desc_ru,
                                f_name=p.f_name,cpu_c_t=p.cpu_c_t,
                                f_cpu_c_t=p.f_cpu_c_t,cpu_b_f=p.cpu_b_f,
                                cpu_cache=p.cpu_cache,cpu_i_g_ua=p.cpu_i_g_ua,
                                cpu_i_g_rus=p.cpu_i_g_rus,
                                depend_from=p.depend_from,depend_from_type=p.depend_from_type)
                try:
                    c = CPU.objects.get(name=p['name'])
                except:
                    print(p['name'])
            else:
                cpu = CPU.objects.create(name=p['name'], part_number=p.part_number,
                            vendor=p.vendor,price=p.price,
                            desc_ukr=p.desc_ukr,desc_ru=p.desc_ru,
                            f_name=p.f_name,cpu_c_t=p.cpu_c_t,
                            f_cpu_c_t=p.f_cpu_c_t,cpu_b_f=p.cpu_b_f,
                            cpu_cache=p.cpu_cache,cpu_i_g_ua=p.cpu_i_g_ua,
                            cpu_i_g_rus=p.cpu_i_g_rus,
                            depend_from=p.depend_from,depend_from_type=p.depend_from_type)

def cool_reload(cool_):
    for p in cool_.iloc:
        if isinstance(p.part_number, str) and p.part_number != 'part_number':
            p = delete_nan(p)
            if Cooler.objects.filter(name=p['name']).exists():
                Cooler.objects.filter(name=p['name']).update(
                                vendor=p.vendor,
                                desc_ukr=p.desc_ukr,desc_ru=p.desc_ru,
                                fan_type_ua=p.fan_type_ua,fan_type_rus=p.fan_type_rus,
                                fan_spd_ua=p.fan_spd_ua,fan_spd_rus=p.fan_spd_rus,
                                fan_noise_level=p.fan_noise_level,fan_size=p.fan_size,
                                depend_to=p.depend_to,
                                depend_to_type=p.depend_to_type,cooler_height=p.cooler_height)
                try:
                    c = Cooler.objects.get(name=p['name'])
                except:
                    print(p['name'])
            else:
                cpu = Cooler.objects.create(name=p['name'], part_number=p.part_number,
                            vendor=p.vendor,price=p.price,
                            desc_ukr=p.desc_ukr,desc_ru=p.desc_ru,
                            fan_type_ua=p.fan_type_ua,fan_type_rus=p.fan_type_rus,
                            fan_spd_ua=p.fan_spd_ua,fan_spd_rus=p.fan_spd_rus,
                            fan_noise_level=p.fan_noise_level,fan_size=p.fan_size,
                            depend_to=p.depend_to,
                            depend_to_type=p.depend_to_type,cooler_height=p.cooler_height)

def mb_reload(mb_):
    for p in mb_.iloc:
        if isinstance(p.part_number, str) and p.part_number != 'part_number':
            p = delete_nan(p)
            if MB.objects.filter(name=p['name']).exists():
                MB.objects.filter(name=p['name']).update(
                                vendor=p.vendor,
                                desc_ukr=p.desc_ukr,desc_ru=p.desc_ru,
                                main_category=p.main_category,mb_chipset=p.mb_chipset,
                                mb_max_ram=p.mb_max_ram,depend_to=p.depend_to,
                                depend_to_type=p.depend_to_type,depend_from=p.depend_from,
                                depend_from_type=p.depend_from_type)
                try:
                    c = MB.objects.get(name=p['name'])
                except:
                    print(p['name'])
            else:
                cpu = MB.objects.create(name=p['name'], part_number=p.part_number,
                            vendor=p.vendor,price=p.price,
                            desc_ukr=p.desc_ukr,desc_ru=p.desc_ru,
                            main_category=p.main_category,mb_chipset=p.mb_chipset,
                            mb_max_ram=p.mb_max_ram,depend_to=p.depend_to,
                            depend_to_type=p.depend_to_type,depend_from=p.depend_from,
                            depend_from_type=p.depend_from_type)

def ram_reload(ram_):
    for p in ram_.iloc:
        if isinstance(p.part_number, str) and p.part_number != 'part_number':
            p = delete_nan(p)
            if RAM.objects.filter(name=p['name']).exists():
                RAM.objects.filter(name=p['name']).update(
                                vendor=p.vendor,
                                desc_ukr=p.desc_ukr,desc_ru=p.desc_ru,
                                f_name=p.f_name,mem_s=p.mem_s,
                                mem_spd=p.mem_spd,mem_l=p.mem_l)
                try:
                    c = RAM.objects.get(name=p['name'])
                except:
                    print(p['name'])
            else:
                cpu = RAM.objects.create(name=p['name'], part_number=p.part_number,
                            vendor=p.vendor,price=p.price,
                            desc_ukr=p.desc_ukr,desc_ru=p.desc_ru,
                            f_name=p.f_name,mem_s=p.mem_s,
                            mem_spd=p.mem_spd,mem_l=p.mem_l)

def gpu_reload(gpu_):
    for p in gpu_.iloc:
        if isinstance(p.part_number, str) and p.part_number != 'part_number':
            p = delete_nan(p)
            if GPU.objects.filter(name=p['name']).exists():
                GPU.objects.filter(name=p['name']).update(
                                vendor=p.vendor,
                                desc_ukr=p.desc_ukr,desc_ru=p.desc_ru,
                                main_category=p.main_category,f_name=p.f_name,
                                gpu_fps=p.gpu_fps, gpu_m_s=p.gpu_m_s, gpu_b=p.gpu_b,
                                gpu_cpu_spd=p.gpu_cpu_spd,gpu_mem_spd=p.gpu_mem_spd,
                                depend_to=p.depend_to,
                                depend_to_type=p.depend_to_type)
                try:
                    c = GPU.objects.get(name=p['name'])
                except:
                    print(p['name'])
            else:
                cpu = GPU.objects.create(name=p['name'], part_number=p.part_number,
                            vendor=p.vendor,price=p.price,
                            desc_ukr=p.desc_ukr,desc_ru=p.desc_ru,
                            main_category=p.main_category,f_name=p.f_name,
                            gpu_m_s=p.gpu_m_s,gpu_b=p.gpu_b,
                            gpu_cpu_spd=p.gpu_cpu_spd,gpu_mem_spd=p.gpu_mem_spd,
                            depend_to=p.depend_to,
                            depend_to_type=p.depend_to_type)

def case_reload(case_):
    for p in case_.iloc:
        if isinstance(p.part_number, str) and p.part_number != 'part_number':
            p = delete_nan(p)
            if CASE.objects.filter(name=p['name']).exists():
                CASE.objects.filter(name=p['name']).update(
                                vendor=p.vendor,
                                desc_ukr=p.desc_ukr,desc_ru=p.desc_ru,
                                case_s=p.case_s,color_parent=p.color_parent,
                                color=p.color, color_ukr=p.color_ukr, color_ru=p.color_ru,
                                depend_to=p.depend_to,depend_to_type=p.depend_to_type,
                                case_height=p.case_height)
                try:
                    c = CASE.objects.get(name=p['name'])
                except:
                    print(p['name'])
            else:
                cpu = CASE.objects.create(name=p['name'], part_number=p.part_number,
                            vendor=p.vendor,price=p.price,
                            desc_ukr=p.desc_ukr,desc_ru=p.desc_ru,
                            case_s=p.case_s,color_parent=p.color_parent,
                            color=p.color, color_ukr=p.color_ukr, color_ru=p.color_ru,
                            depend_to=p.depend_to,depend_to_type=p.depend_to_type,
                            case_height=p.case_height)

def wifi_reload(wifi_):
    for p in wifi_.iloc:
        if isinstance(p.part_number, str) and p.part_number != 'part_number':
            p = delete_nan(p)
            if WiFi.objects.filter(name=p['name']).exists():
                WiFi.objects.filter(name=p['name']).update(
                                vendor=p.vendor,
                                desc_ukr=p.desc_ukr,desc_ru=p.desc_ru,
                                net_type_ukr=p.net_type_ukr,
                                net_type_rus=p.net_type_rus, net_max_spd=p.net_max_spd, net_stand=p.net_stand,
                                net_int=p.net_int)
                try:
                    c = WiFi.objects.get(name=p['name'])
                except:
                    print(p['name'])
            else:
                cpu = WiFi.objects.create(name=p['name'], part_number=p.part_number,
                            vendor=p.vendor,price=p.price,
                            desc_ukr=p.desc_ukr,desc_ru=p.desc_ru,
                            r_price=0,net_type_ukr=p.net_type_ukr,
                            net_type_rus=p.net_type_rus, net_max_spd=p.net_max_spd, net_stand=p.net_stand,
                            net_int=p.net_int)

def soft_reload(soft_):
    for p in soft_.iloc:
        if isinstance(p.part_number, str) and p.part_number != 'part_number':
            p = delete_nan(p)
            if Soft.objects.filter(name=p['name']).exists():
                Soft.objects.filter(name=p['name']).update(
                                vendor=p.vendor,
                                desc_ukr=p.desc_ukr,desc_ru=p.desc_ru,
                                soft_type_ukr=p.soft_type_ukr,
                                soft_type_ru=p.soft_type_ru, soft_lang_ukr=p.soft_lang_ukr, soft_lang_ru=p.soft_lang_ru,
                                soft_set=p.soft_set)
                try:
                    c = Soft.objects.get(name=p['name'])
                except:
                    print(p['name'])
            else:
                cpu = Soft.objects.create(name=p['name'], part_number=p.part_number,
                            vendor=p.vendor,
                            desc_ukr=p.desc_ukr,desc_ru=p.desc_ru, price=p.price,
                            soft_type_ukr=p.soft_type_ukr, r_price=p.r_price,
                            soft_type_ru=p.soft_type_ru, soft_lang_ukr=p.soft_lang_ukr, soft_lang_ru=p.soft_lang_ru,
                            soft_set=p.soft_set)

def cables_reload(cables_):
    for p in cables_.iloc:
        if isinstance(p.part_number, str) and p.part_number != 'part_number':
            p = delete_nan(p)
            if Cables.objects.filter(name=p['name']).exists():
                Cables.objects.filter(name=p['name']).update(
                                vendor=p.vendor,
                                desc_ukr=p.desc_ukr,desc_ru=p.desc_ru,
                                cab_mat_ukr=p.cab_mat_ukr,
                                cab_mat_ru=p.cab_mat_ru, cab_col_ukr=p.cab_col_ukr, cab_col_ru=p.cab_col_ru,
                                cab_set=p.cab_set)
                try:
                    c = Cables.objects.get(name=p['name'])
                except:
                    print(p['name'])
            else:
                cpu = Cables.objects.create(name=p['name'], part_number=p.part_number,
                            vendor=p.vendor,
                            desc_ukr=p.desc_ukr,desc_ru=p.desc_ru,
                            cab_mat_ukr=p.cab_mat_ukr, r_price=p.r_price,
                            cab_mat_ru=p.cab_mat_ru, cab_col_ukr=p.cab_col_ukr, cab_col_ru=p.cab_col_ru,
                            cab_set=p.cab_set)
