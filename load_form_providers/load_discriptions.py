from scrapy import get_video,get_cpu,get_mb,get_case,get_ps,get_cool,get_hdd_ssd,get_mem
from cat.models import *

def get_proc_discr(obj):
    formula = get_cpu(obj)
    kind = to_article2_1(obj)
    #kind2 =
    if kind == 'aproc' and len(formula) > 1 and isinstance(formula[1],int):
        if len(formula) == 2:
            return (f'Ryzen {formula[0]} {formula[1]} BOX', f'Ryzen {formula[0]} {formula[1]}')
        if len(formula) > 2:
            return (f'Ryzen {formula[0]} {formula[1]}{formula[2]} BOX', f'Ryzen {formula[0]} {formula[1]}{formula[2]}')
    if kind == 'aproc':
        kind2 = re.findall('athlon|threadripper',obj.lower())
        kind2 = kind2[0] if kind2 else ''
        if kind2 == 'athlon' and len(formula) > 1:
            return (f'Athlon {formula[0]}{formula[1]} BOX', f'Athlon {formula[0]}{formula[1]}')
        if kind2 == 'athlon' and len(formula) > 0:
            return (f'Athlon {formula[0]} BOX', f'Athlon {formula[0]}')
        if kind2 == 'threadripper' and len(formula) > 1:
            return (f'Ryzen Threadripper {formula[0]}{formula[1]} BOX', f'Threadripper {formula[0]}{formula[1]}')
        if kind2 == 'threadripper' and len(formula) > 0:
            return (f'Ryzen Threadripper {formula[0]} BOX', f'Threadripper {formula[0]}')
    if kind == 'iproc' and len(formula) > 1 and isinstance(formula[1],int) and obj.lower().find('core') != -1:
        if len(formula) == 2:
            return (f'Core i{formula[0]} {formula[1]} BOX', f'Core i{formula[0]} {formula[1]}')
        if len(formula) > 2:
            return (f'Core i{formula[0]} {formula[1]}{formula[2]} BOX', f'Core i{formula[0]} {formula[1]}{formula[2]}')
    if kind == 'iproc':
        kind2 = re.findall('celeron|pentium',obj.lower())
        kind2 = kind2[0] if kind2 else ''
        if kind2 == 'celeron' and len(formula) > 1:
            return (f'Celeron {formula[0]}{formula[1]} BOX', f'Celeron {formula[0]}{formula[1]}')
        if kind2 == 'celeron' and len(formula) > 0:
            return (f'Celeron {formula[0]} BOX', f'Celeron {formula[0]}')
        if kind2 == 'pentium' and len(formula) > 1:
            return (f'Pentium {formula[0]} {formula[1]} BOX', f'Pentium {formula[0]}{formula[1]}')
        if kind2 == 'pentium' and len(formula) > 0:
            return (f'Pentium {formula[0]} BOX', f'Pentium {formula[0]}')
    else:
        return ('Unknow','Unknow')

def get_hd_in_proc(obj,kind):
    if kind == 'aproc':
        if obj.lower().find('radeon') != -1:
            return ('AMD Radeon Vega','AMD Radeon Vega')
    if kind == 'iproc':
        if obj.lower().find('hd') != -1:
            return ('Intel UHD Graphics','Intel UHD Graphics')
    else:
        return ('Відсутнє','Отсутствует')

def get_relatins_proc(obj):
    formula = get_cpu(obj)
    if len(formula) == 1 or (len(formula) > 1 and isinstance(formula[1],str)):
        discr = CPU.objects.filter(name__icontains=str(formula[0]))
        for d in discr:
            if d.depend_from:
                return d.depend_from
    if len(formula) > 1 and isinstance(formula[1],int):
        discr = CPU.objects.filter(name__icontains=str(formula[1]))
        for d in discr:
            if d.depend_from:
                return d.depend_from
    else:
        return ''

def to_article2_1(d,pr=1):
    if pr==1:
        if d.lower().find('core') !=-1:
            return 'iproc'
        elif d.lower().find('pentium') !=-1:
            return 'iproc'
        elif d.lower().find('celeron') !=-1:
            return 'iproc'
        elif d.lower().find('xeon') !=-1:
            return 'iproc'
        elif d.lower().find('intel') !=-1:
            return 'iproc'
        else:
            return 'aproc'
    else:
        if re.findall(r'fm3|fm2|am3|am4|9830|320|450|x470|x570|a68|x399|trx40|550|520|amd',d.lower()):
            return 'amb'
        if re.findall(r'4005|1800|1900|61|81|110|310|365|360|z390|x299|410|z490|b460|z590|370|470|510|b560|1200|h570|intel',
                    d.lower()):
            return 'imb'
        else:
            return ''

def brain_discr(brain,partn,kind):
    pass

def brain_cpu(partn,brain,kind):
    prod_dict = {}
    proc_dict = {
                'iproc': ({'desc_ukr':'Відчуй ефект повного занурення в ігровий процес на максимальних налаштуваннях графіки разом з процесорами Intel.'},
                        {'desc_ru':'Почувствуй эффект полного погружения в игровой процесс на максимальных настройках графики вместе с процессорами Intel.'},
                        {'vendor':'Intel'},
                        {'depend_from_type':'chipset'}
                        ),
                'aproc': ({'desc_ukr':'Процесори Ryzen – це гарантія стабільності роботи та ваша перевага над суперниками в сучасних іграх!'},
                        {'desc_ru':'Процессоры Ryzen - это гарантия стабильности работы и ваше преимущество над соперниками в современных играх!'},
                        {'vendor':'Amd'},
                        {'depend_from_type':'chipset'}
                        )
                }
    brain_proc=[]
    for x in brain.values():
        if x['Group']=='Процессоры' and x['Article'] == partn:
            brain_proc = (x['Article'],x['Description'],x['Name'])
    if brain_proc and len(brain_proc) == 3:
        flow = re.findall('(\d+) потоков',brain_proc[1].lower())
        core = re.findall('(\d+) ядер',brain_proc[1].lower())
        flow = flow[0] if flow else ''
        core = core[0] if core else ''
        prod_dict['cpu_c_t'] = f'{core}/{flow}'
        prod_dict['f_cpu_c_t'] = prod_dict['cpu_c_t']
        cpu_b_f = re.findall('потоков,.?(\d\.\d)',brain_proc[1].lower())
        cpu_b_f = cpu_b_f[0] if cpu_b_f else ''
        prod_dict['cpu_b_f'] = cpu_b_f
        temp = re.findall('l[1234]:.?(\d*)|intel smart cache - (\d*)',brain_proc[1].lower())
        temp = [x for x in temp[0] if x] if temp else []
        prod_dict['cpu_cache'] = temp[0] if temp else ''
        prod_dict['name'], prod_dict['f_name'] = get_proc_discr(brain_proc[2])
        if kind in ('aproc','iproc'):
            for t in proc_dict[kind]:
                tt=list(t.keys())[0]
                prod_dict[tt]=t[tt]
        prod_dict['depend_from'] = get_relatins_proc(brain_proc[2])
        cpu_i_g_ua,cpu_i_g_rus = get_hd_in_proc(brain_proc[2],kind)
        prod_dict['cpu_i_g_ua'] = cpu_i_g_ua
        prod_dict['cpu_i_g_rus'] = cpu_i_g_rus
        prod_dict['part_number'] = brain_proc[0]
    else:
        return {}

    return prod_dict

def brain_cool(partn,brain,kind):

    prod_dict = {
                'desc_ukr':'Сучасна система повітряного охолодження розроблена з урахуванням передових технологій та демонструє кращі в своєму класі показники!',
                        'desc_ru':'Современная система воздушного охлаждения разработана с учетом передовых технологий и демонстрирует лучшие в своем классе показатели!',
                        'fan_type_ua':'повітряне',
                        'fan_type_rus':'воздушное'
                }

    ss = '(Xilence\s.+)$|(QUBE\s.+)$|(АARDWOLF\s.+)$|(AeroCool\s.+)$|(Argus\s.+)$|(ID-Cooling\s.+)$|(ENERMAX\s.+)$|(CoolerMaster\s.+)$|(PcСooler\s.+)$|(GIGABYTE\s.+)$|(Arctic\s.+)$|(Thermalright\s.+)$|(Silver Stone\s.+)$|(SCYTHE\s.+)$|(TITAN\s.+)$|(Noctua\s.+)$|(GAMEMAX\s.+)$|(Zalman\s.+)$|(Cooling Baby\s.+)$|(GELID\s.+)$|(ThermalTake\s.+)$|(Antec\s.+)$|(Deepcool\s.+)$'
    vendor = 'Xilence|QUBE|АARDWOLF|AeroCool|Argus|ID-Cooling|ENERMAX|CoolerMaster|PcСooler|GIGABYTE|Arctic|Thermalright|Silver Stone|SCYTHE|TITAN|Noctua|GAMEMAX|Zalman|Cooling Baby|GELID|ThermalTake|Antec|Deepcool'

    brain_cool=[]
    for x in brain.values():
        if x['Group']=='Системы охлаждения' and x['Article'] == partn:
            brain_cool = (x['Article'],x['Description'],x['Name'])
    if brain_cool and len(brain_cool) == 3:
        brain_cool_temp = re.sub('\(.+\)$','',brain_cool[2]).strip()
        name = re.findall(f"{ss}",brain_cool_temp)
        name = name[0] if name else ''
        if name:
            temp=[x for x in name if x]
            name = temp[0] if temp else ''
        prod_dict['name'] = name
        prod_dict['part_number'] = brain_cool[0]
        vendor_temp = re.findall(f"{vendor}",brain_cool[2])
        vendor_temp = vendor_temp[0] if vendor_temp else ''
        prod_dict['vendor'] = vendor_temp
        fan_spd_ua = re.findall('максимальная скорость вращения вентиляторов - (\d+)',brain_cool[1])
        fan_spd_ua = fan_spd_ua[0] if fan_spd_ua else ''
        prod_dict['fan_spd_ua'] = fan_spd_ua  + ' об/хв'
        prod_dict['fan_spd_rus'] = fan_spd_ua  + ' об/мин'
        fan_noise_level = re.findall('уровень шума - (\d+)',brain_cool[1])
        fan_noise_level = fan_noise_level[0] if fan_noise_level else ''
        prod_dict['fan_noise_level'] = fan_noise_level
        fan_size = re.findall('диаметр вентиляторов - (\d+)',brain_cool[1])
        fan_size = fan_size[0] if fan_size else ''
        prod_dict['fan_size'] = fan_size
    else:
        return {}

    return prod_dict

def brain_mb(partn,brain,kind):
    vendor_dict =  {
                    'Intel':'Intel',
                    'Amd':'Amd',
                    'Mini ITX':'Intel'
                    }
    prod_dict = {
                'desc_ukr':'Завдяки унікальному зовнішньому вигляду та ексклюзивним геймерським функціям, дані материнські плати пропонують найкращі ігрові можливості, даючи геймерам те – що їм дійсно потрібно!',
                'desc_ru':'Благодаря уникальному внешнему виду и эксклюзивным геймерским функциям, данные материнские платы предлагают лучшие игровые возможности, давая геймерам то - что им действительно нужно!',
                'depend_to_type':'chipset'
                }

    brain_mb=[]
    for x in brain.values():
        if x['Group']=='Материнские платы' and x['Article'] == partn:
            brain_mb = (x['Article'],x['Description'],x['Name'])
    if brain_mb and len(brain_mb) == 3:
        prod_dict['part_number'] = brain_mb[0]
        vendor_name = re.findall('Материнская плата\s(.+)$',brain_mb[2])
        vendor_name = vendor_name[0] if vendor_name else ''
        vendor = re.findall('^(\w+)\s',vendor_name)
        vendor = vendor[0] if vendor else ''
        #name= re.findall('^\w+\s(.+)$',vendor_name)
        #name = name[0] if name else ''
        prod_dict['name'] = vendor_name
        prod_dict['vendor'] = vendor
        temp = re.findall('intel\s(\w+),|amd\s(\w+),',brain_mb[1].lower())
        if brain_mb[1].lower().find('mini itx') != -1 and not temp:
            prod_dict['main_category'] = 'Intel'
            prod_dict['main_category'] = 'Intel'
            temp = get_mb(brain_mb[2])
            temp = [x for x in temp if x]
            temp = temp[0] if temp else ''
            prod_dict['mb_chipset'] = f'Intel J{temp}'
            depend_to = f'J{temp}'
        else:
            if temp and temp[0] and len(temp[0]) == 2 and temp[0][0]:
                prod_dict['main_category'] = 'Intel'
                depend_to = temp[0][0]
                prod_dict['mb_chipset'] = f'Intel {depend_to}'
            elif temp and temp[0] and len(temp[0]) == 2 and temp[0][1]:
                prod_dict['main_category'] = 'Amd'
                depend_to = temp[0][1]
                prod_dict['mb_chipset'] = f'Amd {depend_to}'
        if depend_to:
            prod_dict['depend_to'] = depend_to
        mb_max_ram = re.findall('Макс. память - (\d+)',brain_mb[1])
        mb_max_ram = mb_max_ram[0] if mb_max_ram else ''
        prod_dict['mb_max_ram'] = f'{mb_max_ram} Gb'
        prod_dict['depend_to'] = depend_to
    else:
        return {}

    return prod_dict

def brain_mem(partn,brain,kind):

    prod_dict = {
                'desc_ukr':"Дані модулі пам'яті предназначені для геймерів, ентузіастів та професіоналів. В модулях використані чіпи найвищої якості! Модулі пам'яті оснащені єфективними радіаторами які відводять надлишок тепла забезпечуючи безперебійну роботу на протязі тривалого часу.",
                        'desc_ru':"Данная память предназначена для геймеров, энтузиастов и профессионалов. В модулях использованы чипы высочайшего качества и оснащены эффективными радиаторами которые отводят избыток тепла обеспечивая бесперебойную работу в течение длительного времени."
                }

    brain_mem=[]
    for x in brain.values():
        if x['Group']=='Модули памяти' and x['Article'] == partn:
            brain_mem = (x['Article'],x['Description'],x['Name'])
    if brain_mem and len(brain_mem) == 3:
        prod_dict['part_number'] = brain_mem[0]
        name = re.sub('\([24]x\d+gb\)','',brain_mem[2].lower())
        name = re.sub('\(.+\)$|модуль памяти для компьютера ','',name.lower()).strip()
        vendor = re.findall('\s(\w+)$',name)
        vendor = vendor[0] if vendor else ''
        prod_dict['name'] = name
        prod_dict['vendor'] = vendor
        f_name = re.findall('ddr[2345]\s(\d+)gb',name.lower())
        f_name = f_name[0] if f_name else ''
        prod_dict['f_name'] = f'{f_name}Gb'
        mem_spd = re.findall('(\d+)\smhz',name.lower())
        mem_spd = mem_spd[0] if mem_spd else ''
        mem_l = re.findall('cl(\d+)',brain_mem[1].lower())
        mem_l = mem_l[0] if mem_l else ''
        prod_dict['mem_spd'] = f'{mem_spd}Mhz'
        prod_dict['mem_l'] = f'CL{mem_l}'
        if_2_4 = re.findall('в наборе - ([24])',brain_mem[1].lower())
        if_2_4 = if_2_4[0] if if_2_4 else 0
        mem_s = f'{f_name}Gb'
        if if_2_4:
            try:
                res = int(f_name)/int(if_2_4)
                res = round(res)
            except:
                res = 0
            if res:
                mem_s = f'{f_name}Gb ({if_2_4}x{str(res)})'
        prod_dict['mem_s'] = mem_s
    else:
        return {}
    return prod_dict

def brain_hdd(partn,brain,kind):

    prod_dict = {
                'desc_ukr':"Творцям, геймерам та тим, хто потребує найкращого – ми пропонуємо жорсткі диски нового покоління, роблячи зберігання та доступ до даних на ПК ще більш комфортним!",
                        'desc_ru':"Создателям, геймерам и тем, кто нуждается в лучшем - мы предлагаем жесткие диски нового поколения, делая хранения и доступ к данным на компьютере еще более комфортным!"
                }

    brain_hdd=[]
    for x in brain.values():
        if x['Group']=='Накопители HDD - 3.5", 2.5", внутренние' and x['Article'] == partn:
            brain_hdd = (x['Article'],x['Description'],x['Name'])
    if brain_hdd and len(brain_hdd) == 3:
        prod_dict['part_number'] = brain_hdd[0]
        name = re.sub('^Жесткий диск |\(.+\)$','',brain_hdd[2]).strip()
        vendor = re.findall('\s(\w+)$',name)
        vendor = vendor[0] if vendor else ''
        f_name = re.findall('3.5"\s+(\w+)\s',name)
        f_name = f_name[0] if f_name else ''
        gb = re.sub('\D','',f_name)
        hdd_s = f'{gb}000Gb' if gb and len(gb) == 1 else f_name
        hdd_spd_ua = re.findall('(\d+) об/мин',brain_hdd[1].lower())
        hdd_spd_ua = hdd_spd_ua[0] if hdd_spd_ua else 'mutable'
        hdd_ca = re.findall('(\d+) mb',brain_hdd[1].lower())
        hdd_ca = hdd_ca[0] if hdd_ca else ''
        prod_dict['name'] = name
        prod_dict['vendor'] = vendor
        prod_dict['f_name'] = f_name
        prod_dict['hdd_s'] = hdd_s
        prod_dict['hdd_s'] = hdd_s
        prod_dict['hdd_spd_ua'] = f'{hdd_spd_ua} об./хв.'
        prod_dict['hdd_spd_rus'] = f'{hdd_spd_ua} об./м.'
        prod_dict['hdd_ca'] = f'{hdd_ca} МБ'
    else:
        return {}
    return prod_dict

def brain_ps(partn,brain,kind):

    prod_dict = {
                'desc_ukr':"Всі блоки живлення проходять безліч стадій тестування! В результаті вдалося добитись відмінного ККД, практично безшумної роботи при максимальній надійності.",
                        'desc_ru':"Все блоки питания проходят множество стадий тестирования! В результате удалось добиться отличного КПД, практически бесшумной работы при максимальной надежности."
                }

    brain_ps=[]
    for x in brain.values():
        if x['Group']=='Корпуса' and x['Article'] == partn:
            brain_ps = (x['Article'],x['Description'],x['Name'])
    if brain_ps and len(brain_ps) == 3:
        prod_dict['part_number'] = brain_ps[0]
        name = re.sub('\(.+\)$|блок питания','',brain_ps[2].lower()).strip().capitalize()
        vendor = re.findall('^(\w+)\s',name)
        vendor = vendor[0] if vendor else ''
        psu_p = re.findall('(\d+)w',name.lower())
        psu_p = psu_p[0] if psu_p else ''
        prod_dict['psu_c'] = '-'
        psu_f = re.findall('[1234]x(\d+) мм',brain_ps[1].lower())
        psu_f = psu_f[0] if psu_f else ''
        prod_dict['name'] = name
        prod_dict['vendor'] = vendor
        prod_dict['psu_p'] = f'{psu_p} Вт'
        prod_dict['psu_f'] = f'{psu_f} мм'
    else:
        return {}
    return prod_dict

def brain_gpu(partn,brain,kind):

    prod_dict = {
                'desc_ukr':"Відеоадаптери лінійки GeForce GTX демонструють високу продуктивність та підтримують передові технології GeForce Experience™ в найсучасніших комп’ютерних іграх.",
                        'desc_ru':"Видеоадаптеры линейки GeForce GTX демонстрируют высокую производительность и поддерживают современные технологии GeForce Experience™ в самых современных компьютерных играх."
                }

    brain_gpu=[]
    for x in brain.values():
        if x['Group']=='Видеокарты' and x['Article'] == partn:
            brain_gpu = (x['Article'],x['Description'],x['Name'])
    if brain_gpu and len(brain_gpu) == 3:
        prod_dict['part_number'] = brain_gpu[0]
        name = re.sub('\(.+\)$|видеокарта','',brain_gpu[2].lower()).strip()
        if not re.findall('^geforce|^radeon|^intel|^quadro',name):
            vendor = re.findall('^(\w+)\s',name.lower())
            vendor = vendor[0].capitalize() if vendor else ''
            f_name = re.sub('^(\w+)\s|(\s\d+gb.+)|(\s\d+mb.*)','',name.lower())
        else:
            vendor = re.findall('\s(\w+)$',name.lower())
            vendor = vendor[0].capitalize() if vendor else ''
            f_name = re.sub('\s(\w+)$|(\s\d+gb.+)|(\s\d+mb.*)','',name.lower())
        main_category = 'Radeon' if name.find('radeon') != -1 else 'Nvidia'
        gpu_fps = f'AMD {f_name}' if name.find('radeon') != -1 else f'Nvidia {f_name}'
        gpu_m_s = re.findall('(\d+) гб',brain_gpu[1].lower())
        gpu_m_s = f'{gpu_m_s[0]} Gb' if gpu_m_s else ''
        gpu_b = re.findall('(\d+)\s+bit',brain_gpu[1].lower())
        gpu_b = f'{gpu_b[0]} bit' if gpu_b else ''
        gpu_cpu_spd = re.findall('base\s+-\s+(\d+)',brain_gpu[1].lower())
        gpu_cpu_spd = f'{gpu_cpu_spd[0]} МГц' if gpu_cpu_spd else ''
        prod_dict['name'] = name.capitalize()
        prod_dict['vendor'] = vendor
        prod_dict['main_category'] = main_category
        prod_dict['f_name'] = f_name
        prod_dict['gpu_fps'] = gpu_fps
        prod_dict['gpu_m_s'] = gpu_m_s
        prod_dict['gpu_b'] = gpu_b
        prod_dict['gpu_cpu_spd'] = gpu_cpu_spd

    else:
        return {}
    return prod_dict

def brain_case(partn,brain,kind):

    prod_dict = {
                'desc_ukr':'Це ідеальний корпус для тих, хто очікує самі високі стандарти, коли мова йде про якість, оригінальність та дизайн.',
                        'desc_ru':'Это идеальный корпус для тех, кто ожидает самые высокие стандарты, когда речь идет о качестве, оригинальности и дизайне.'
                }

    brain_case=[]
    for x in brain.values():
        if x['Group']=='Корпуса' and x['Article'] == partn:
            brain_case = (x['Article'],x['Description'],x['Name'])
    if brain_case and len(brain_case) == 3:
        name = re.sub('\(.+\)$|корпус','',brain_case[2].lower()).strip().capitalize()
        prod_dict['part_number'] = brain_case[0]
        prod_dict['name'] = name
        vendor = re.findall('^(\w+)\s',name)
        vendor = vendor[0] if vendor else ''
        case_s = re.findall('^\w+,\s(\w+)',brain_case[1])
        case_s = case_s[0] if case_s else ''
        prod_dict['vendor'] = vendor
        prod_dict['case_s'] = case_s
    else:
        return {}

    return prod_dict

def brain_ssd(partn,brain,kind):

    prod_dict = {
                'desc_ukr':"Твердотілий накопичувач значно підвищує швидкість роботи системи в цілому. А також забезпечуючи більш високу швидкість запуску ПК, завантаження та передачу даних на блискавичній швидкості!",
                        'desc_ru':"Твердотельный накопитель значительно повышает скорость работы системы в целом. А также обеспечивая более высокую скорость запуска ПК, загрузку и передачу данных на молниеносной скорости!"
                }

    brain_ssd=[]
    for x in brain.values():
        if x['Group']=='Накопители SSD' and x['Article'] == partn:
            brain_ssd = (x['Article'],x['Description'],x['Name'])
    if brain_ssd and len(brain_ssd) == 3:
        prod_dict['part_number'] = brain_ssd[0]
        name = re.sub('накопитель|\(.+\)$','',brain_ssd[2].lower()).strip().capitalize()
        vendor = re.findall('gb\s(.+)$',name.lower())
        vendor = vendor[0].strip().capitalize() if vendor else ''
        f_name = re.findall('(\d+)\s*gb',name.lower())
        f_name = f'{f_name[0]} Gb' if f_name else ''
        temp1 = re.findall('скорость записи, макс.\s+-\s+(\d+)',brain_ssd[1].lower())
        temp1 = temp1[0] if temp1 else ''
        temp2 = re.findall('скорость чтения, макс.\s+-\s+(\d+)',brain_ssd[1].lower())
        temp2 = temp2[0] if temp2 else ''
        ssd_spd = f'{temp1}/{temp2} МБ/с'
        ssd_type_cells = re.findall('gb(.+)2.5|gb(.+)m\.2',brain_ssd[1].lower())
        ssd_type_cells = list(ssd_type_cells[0]) if ssd_type_cells else []
        ssd_type_cells = [x for x in ssd_type_cells if x] if ssd_type_cells else []
        ssd_type_cells = ssd_type_cells[0] if ssd_type_cells else ''
        prod_dict['name'] = name
        prod_dict['vendor'] = vendor.capitalize()
        prod_dict['f_name'] = f_name
        prod_dict['ssd_s'] = f_name
        prod_dict['ssd_spd'] = ssd_spd
        prod_dict['ssd_type_cells'] = re.sub(',','',ssd_type_cells.strip())
    else:
        return {}
    return prod_dict
