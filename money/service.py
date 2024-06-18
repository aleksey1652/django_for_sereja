import re
import bs4
from bs4 import BeautifulSoup
import requests
from random import choice
#providerprice_parts

trans_remainder_category_dict = {
                                'Видеокарты': 'video',
                                'Корпуса': 'case',
                                'Модули памяти': 'mem',
                                'Блоки Питания': 'ps',
                                'Вентиляторы': 'vent',
                                'Накопители SSD': 'ssd',
                                'Накопители HDD': 'hdd',
                                'Охлаждение': 'cool',
                                'прочие': 'cables'
                                }

def video_html(video_blok):
    video_string = ''
    video_string = re.findall(r'\w+', video_blok)
    if video_string and video_string[0].find('1030') != -1:
        return 'nvidia-geforce-gt-10xx'
    elif not video_string or video_blok == 'board':
        return ''
    else:
        try:
            cifar = int(video_string[0][0])
            video_line = video_string[0]
            video_line_more = '-' + video_string[1] if len(video_string) > 1 else ''
            art_video_html = {
                            0: '',
                            3: f'nvidia-geforce-rtx-{video_line}{video_line_more}',
                            2: f'nvidia-geforce-rtx-{video_line}{video_line_more}',
                            1: f'nvidia-geforce-gtx-{video_line}{video_line_more}',
                            1030: 'nvidia-geforce-gt-10xx',
                            7: 'nvidia-geforce-gt-7xx',
                            5: 'amd-radeon-rx-5xx',
                            6: f'amd-radeon-rx-{video_line}{video_line_more}'
                            }
        except:
            cifar = 0
        if cifar in art_video_html:
            return art_video_html[cifar]
        else:
            return ''

desktop_agents = ['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14',
                 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0']

def random_headers():
    return {'User-Agent': choice(desktop_agents),'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}


def get_html(url):
    response = requests.get(url,proxies=None,timeout=10,headers=random_headers())
    return response.text if response.ok else False

def istocnikZakaza_up(prod):
    to_dict =  {
                'Чат': 'Чат',
                'Rozetka': 'Rozetka',
                'Versum.ua': 'Корзина',
                'Корзина': 'Корзина',
                'КОРЗИНА': 'Корзина',
                'Телефон': 'Телефон',
                'Алло': 'Інше джерело',
                'Офис': 'Офіс',
                'Офіс': 'Офіс',
                'ПК витрина 2%': 'ПК вітрина 2%',
                'ПК вітрина 2%': 'ПК вітрина 2%',
                'JivoSite': 'Телефон',
                'Инстаграм': 'Instagram',
                'Instagram': 'Instagram',
                'Telegram': 'Telegram',
                'Інше джерело': 'Інше джерело',
                'Тендер': 'Тендер',
                'OLX': 'OLX',
                'Сервіс': 'Сервіс'
    }
    res = to_dict[prod] if prod in to_dict else 'Інше джерело'
    return res

def get_goods_kind(prod):
    if re.findall(r'^конфигуратор|Конфигуратор|VERSUM|Оптимальный|Прогрессивный|Мультимедийный|Максимальный|Моноблок|Бизнес|IT-Blok|IT-BLOK|Сборка под заказ', prod.strip()):
        return 'Системный блок'
    elif re.findall(r'^софт',prod.strip()):
        return 'ПО'
    else:
        return 'Комплектующие'

def sborsic_up(sum, amount):
    try:
        sum_per_amount = sum
        sum_per_amount = round(sum_per_amount)
    except:
        return ('простой', 1)
    if sum_per_amount <= 10000:
        return ('простой', amount)
    elif sum_per_amount > 10000 and sum_per_amount <= 40000:
        return ('обычный', amount)
    elif sum_per_amount > 40000 and sum_per_amount <= 100000:
        return ('сложный', amount)
    if sum_per_amount > 100000:
        return ('ультра', amount)


def bid(dict_):
    dict_result = {}
    try:
        dict_result['account'] = dict_['info']['account'] if dict_['info']['account'] in ('versum', 'komputeritblok') else False
    except:
        dict_result['account'] = False
    try:
        dict_result['ch_status'] = True if dict_['info']['webhookEvent'] == 'status_change' else False
    except:
        dict_result['ch_status'] = False
    try:
        dict_result['ID'] = dict_['data']['id']
    except:
        dict_result['ID'] = 0
    try:
        dict_result['manager'] = dict_['meta']['fields']['userId']['options'][0]['text']
        dict_result['manager'] = 'Павел Соколов' if dict_result['manager'] == 'Павел' else dict_result['manager']
    except:
        dict_result['manager'] = ''
    try:
        product_list = []
        for prod in dict_['data']['products']:
            get_goods_kind_ = get_goods_kind(prod['name'])
            if get_goods_kind_ == 'Системный блок':
                prod['description'] = prod['description'] if prod['description'] else prod['name']
                product_list.append([prod['description'], get_goods_kind_, sborsic_up(prod['price'], prod['amount']), prod['price']*prod['amount']])
            else:
                prod['description'] = prod['description'] if prod['description'] else prod['name']
                product_list.append([prod['description'], get_goods_kind_, (None, prod['amount']), prod['price']])
        dict_result['products'] = product_list
    except:
        dict_result['products'] = []
    try:
        dict_result['status'] = dict_['meta']['fields']['statusId']['options'][0]['text']
    except:
        dict_result['status'] = ''
    try:
        sborsik_list = []
        for sborsik in dict_['meta']['fields']['sborsik']['options']:
            sborsik_list.append(sborsik['text'])
        dict_result['sborsik'] = sborsik_list
    except:
        dict_result['sborsik'] = []
    try:
        dict_result['sposobOplaty'] = dict_['meta']['fields']['sposobOplaty']['options'][0]['text']
    except:
        try:
            dict_result['sposobOplaty'] = dict_['meta']['fields']['ord_oplata']['options'][0]['text']
        except:
            dict_result['sposobOplaty'] = ''
    try:
        prod = dict_['meta']['fields']['istocnikZakaza']['options'][0]['text']
        istocnikZakaza_up_ = istocnikZakaza_up(prod)
        dict_result['istocnikZakaza'] = istocnikZakaza_up_
    except:
        try:
            prod = dict_['meta']['fields']['ord_istocnikZakaza_2']['options'][0]['text']
            istocnikZakaza_up_ = istocnikZakaza_up(prod)
            dict_result['istocnikZakaza'] = istocnikZakaza_up_
        except:
            dict_result['istocnikZakaza'] = ''
    return dict_result

def cpu_to_code(data_cpu):
    data_cpu = data_cpu.lower().strip()
    full_code = ''
    amd_cpu_parts = 'ryzen|athlon|threadripper|amd'
    amd_cpu_parts_mini = 'athlon|threadripper'
    intel_cpu_parts = 'core|celeron|pentium|intel'
    intel_cpu_parts_mini = 'celeron|pentium'
    delete_from_string = r"amd|intel|\n|.+-core|;"
    if re.findall(r'' + amd_cpu_parts, data_cpu):
        full_code = 'amd '
        temp = re.sub(delete_from_string, '', data_cpu).strip()
        temp_more = re.sub(r' \S+ghz$', '', temp).strip()
        temp_more_mini = re.findall(r'' + amd_cpu_parts_mini, temp_more)
        if temp_more_mini:
            temp_more_mini = temp_more_mini[0].strip() if temp_more_mini else ''
            temp_more_end = re.findall(r'\d+', temp_more)
            temp_more_end = temp_more_end[0].strip() if temp_more_end else ''
            temp_more_endleter = re.findall(r'\d+(q\S*|w\S*|e\S*|r\S*|t\S*|y\S*|u\S*|i\S*|o\S*|p\S*|a\S*|s\S*|d\S*|f\S*|g\S*|h\S*|j\S*|k\S*|l\S*|z\S*|x\S*|c\S*|v\S*|b\S*|n\S*|m\S*)', temp_more)
            temp_more_endleter = temp_more_endleter[0].strip() if temp_more_endleter else ''
            full_code += temp_more_mini + ' ' + temp_more_end + ' ' + temp_more_endleter
        else:
            temp_more_endleter = re.findall(r'\d+(q\S*|w\S*|e\S*|r\S*|t\S*|y\S*|u\S*|i\S*|o\S*|p\S*|a\S*|s\S*|d\S*|f\S*|g\S*|h\S*|j\S*|k\S*|l\S*|z\S*|x\S*|c\S*|v\S*|b\S*|n\S*|m\S*)', temp_more)
            temp_more_endleter = temp_more_endleter[0].strip() if temp_more_endleter else ''
            temp_more_end = re.findall(r'\d+', temp_more)
            try:
                full_code += (' '.join(temp_more_end[:2]) + ' ' + temp_more_endleter).strip()
            except:
                full_code = full_code
    else:
        full_code = 'intel '
        temp = re.sub(delete_from_string, '', data_cpu).strip()
        temp_more = re.sub(r' \S+ghz$', '', temp).strip()
        temp_more_mini = re.findall(r'' + intel_cpu_parts_mini, temp_more)
        if temp_more_mini:
            temp_more_mini = temp_more_mini[0].strip() if temp_more_mini else ''
            temp_more_end = re.findall(r'\d+', temp_more)
            temp_more_end = temp_more_end[0].strip() if temp_more_end else ''
            temp_more_endleter = re.findall(r'\d+(q\S*|w\S*|e\S*|r\S*|t\S*|y\S*|u\S*|i\S*|o\S*|p\S*|a\S*|s\S*|d\S*|f\S*|g\S*|h\S*|j\S*|k\S*|l\S*|z\S*|x\S*|c\S*|v\S*|b\S*|n\S*|m\S*)', temp_more)
            temp_more_endleter = temp_more_endleter[0].strip() if temp_more_endleter else ''
            full_code += temp_more_mini + ' ' + temp_more_end + ' ' + temp_more_endleter
        else:
            temp_more_endleter = re.findall(r'\d+(q\S*|w\S*|e\S*|r\S*|t\S*|y\S*|u\S*|i\S*|o\S*|p\S*|a\S*|s\S*|d\S*|f\S*|g\S*|h\S*|j\S*|k\S*|l\S*|z\S*|x\S*|c\S*|v\S*|b\S*|n\S*|m\S*)', temp_more)
            temp_more_endleter = temp_more_endleter[0].strip() if temp_more_endleter else ''
            temp_more_end = re.findall(r'\d+', temp_more)
            try:
                full_code += (' '.join(temp_more_end[:2]) + ' ' + temp_more_endleter).strip()
            except:
                full_code = full_code
    return full_code.strip()

def video_to_code(data_video):
    data_video = data_video.lower()
    data_video = re.sub(r'\n|;', '', data_video).strip()
    full_code = ''
    video_parts = 'super|ti|xt'
    board_parts = r'intel hd|vega|radeon r\d'
    test_board_exist = re.findall(board_parts, data_video)
    if test_board_exist:
        return 'board'
    temp_more_endleter = re.findall(video_parts, data_video)
    temp_more_endleter = temp_more_endleter[0] if temp_more_endleter else ''
    temp_more_end = re.findall(r'\d+', data_video)
    temp_more_end = temp_more_end[0] if temp_more_end else ''
    full_code = temp_more_end + ' ' + temp_more_endleter

    return full_code.strip()

def mem_to_code(data_mem):
    data_mem = data_mem.lower()
    data_mem = re.sub(r'\n|;', '', data_mem).strip()
    full_code = ''
    temp_more_end = re.findall(r'\d+', data_mem)
    full_code = temp_more_end[0] if temp_more_end else ''

    return full_code.strip()

def test_art_comp(data_):
    try:
        data_true_or_false = isinstance(data_,
        dict) and len(data_) == 9 and data_['name_computers'] and isinstance(data_['price_computers'], float)
    except:
        data_true_or_false = False
    return data_true_or_false

def get_art_single_comp(url):
    delete_from_string = '|объем накопителя|объем второго накопителя|модель материнской платы|корпус|блок питания|охлаждение процессора|:'
    dict_for_enumerate = {
                        0: 'proc_computers',
                        1: 'video_computers',
                        2: 'mem_computers',
                        3: 'hdd_computers',
                        4: 'mb_computers',
                        5: 'case_computers',
                        6: 'ps_computers',
                        }

    dict_single_comp = dict()

    g_in=get_html(url)
    soup = BeautifulSoup(g_in, "html.parser")
    label = 'product__sort-desc expanded'
    label_price = 'product__price'
    label_title = 'product__title title'
    from_label = soup.find('div',class_=label)
    from_label_price = soup.find('div',class_=label_price)
    from_label_title = soup.find('h1', class_=label_title)
    num_ = 6
    if isinstance(from_label_price, bs4.element.Tag):
        price_row_ = from_label_price.get_text()
        price_row = re.findall(r'\d+', price_row_)
        try:
            dict_single_comp['price_computers'] = float(price_row[0]) if price_row else 0
        except:
            dict_single_comp['price_computers'] = 0
    if isinstance(from_label_title, bs4.element.Tag):
        title_row = from_label_title.get_text().strip()
        dict_single_comp['name_computers'] = title_row if title_row else ''
    if isinstance(from_label, bs4.element.Tag):
        from_label_li = from_label.find_all('li')
        if isinstance(from_label_li, bs4.element.ResultSet):
            for num, li in enumerate(from_label_li):
                try:
                    if num == 0:
                        proc_code = cpu_to_code(li.find('a').get_text())
                        dict_single_comp['proc_computers'] = proc_code
                    elif num == 1:
                        video_code = video_to_code(li.get_text())
                        dict_single_comp['video_computers'] = video_code
                    elif num == 2:
                        mem_code = mem_to_code(li.get_text())
                        dict_single_comp['mem_computers'] = mem_code
                    elif num == 4 and li.get_text().lower().find('втор') != -1:
                        data_row = li.get_text().lower()
                        data_row = re.sub(r'\n|;' + delete_from_string, '', data_row).strip()
                        dict_single_comp['hdd_computers'] += ';' + data_row
                        dict_for_enumerate[5] = 'mb_computers'
                        num_ = 7
                    elif num > num_:
                        break
                    else:
                        data_row = li.get_text().lower()
                        if data_row.find('корпус') != -1:
                            data_row = re.sub(r'\n|;' + delete_from_string, '', data_row).strip()
                            dict_single_comp['case_computers'] = data_row
                            continue
                        if data_row.find('охлаждение') != -1:
                            data_row = re.sub(r'\n|;' + delete_from_string, '', data_row).strip()
                            dict_single_comp['cool_computers'] = data_row
                            continue
                        if data_row.find('блок') != -1:
                            data_row = re.sub(r'\n|;' + delete_from_string, '', data_row).strip()
                            dict_single_comp['ps_computers'] = data_row
                            continue
                        data_row = re.sub(r'\n|;' + delete_from_string, '', data_row).strip()
                        dict_single_comp[dict_for_enumerate[num]] = data_row
                except:
                    return {}
        else:
            return {}
    else:
        return {}

    return dict_single_comp
