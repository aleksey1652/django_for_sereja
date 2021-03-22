from bs4 import BeautifulSoup
import requests ,re, json, pickle, time
from random import choice
from scrapy import desktop_agents, random_headers, get_html, get_cpu

def get_html2(url):
        response = requests.get(url)
        return response.text if response.ok else False

"""
dict1={}
for m in range(1,17):
    g=get_html('https://it-blok.com.ua/computeri.html'+'?page={}'.format(m))
    list1=[]
    if g:
        soup = BeautifulSoup(g, "html.parser")

    else:
        continue
    for x in soup.find_all(class_='item-info'):
        try:
            list1.append((x.find(class_='item-title').find('a').get('href'),
            x.find(class_='item-title').get_text(),
            int(''.join(re.findall(r'\d',x.find(class_='special-price').get_text()))))) if x else ' '
        except:
            continue

    for n in list1:
        if len(n) == 3:
            g2=get_html('https://it-blok.com.ua/{}'.format(n[0]))
            soup2 = BeautifulSoup(g2, "html.parser")
            dict1[soup2.find(class_='sku-block').find_all('span')[1].get_text()]=n
    print(f'{m} page ok')
print('please wait')
list_dict=[]
count=2
for x1,y1 in dict1.items():
    list_dict.append([x1,y1[1],y1[2],'=ROUND(C{}/1,19;1)'.format(count),'https://it-blok.com.ua/'+y1[0]])
    count+=1
list_dict.insert(0,["CODE", "COMPUTER NAME","PRICE","PRICE2", "COMPUTER URL","BARCODE"])

with open("it_blok_price.json", "w") as write_file:
    json.dump(list_dict, write_file)

print(f'finished  {len(list_dict)} objects loaded')
"""
def get_itblok():
    comp_dict = {}
    try:
        for m in range(1,29):
            list1=[]
            try:
                g=get_html(f'https://it-blok.com.ua/ua/computeri.html/?page={m}')
            except:
                print(f'error in {m} page will try with timeout')
                time.sleep(11)
                g=get_html(f'https://it-blok.com.ua/ua/computeri.html/?page={m}')

            if g:
                soup = BeautifulSoup(g, "html.parser")

            else:
                continue
            for c in soup.find_all(class_='product-inner'):
                comp_praram = {}
                try:
                    comp_praram['comp_url'] = 'https://it-blok.com.ua/' + c.find(class_='h4').find('a').get('href')
                    comp_praram['name'] = c.find(class_='h4').find('a').text
                    comp_praram['price'] = re.sub(r'\D','',c.find(class_='price').find(class_='price-new').text)
                    comp_praram['class'] = ''
                    comp_praram['warranty'] = ''
                    list1.append(comp_praram)
                except:
                    continue
            for n in list1:
                if len(n.keys()) == 5:
                    g2=get_html(n['comp_url'])
                    soup2 = BeautifulSoup(g2, "html.parser")
                    s01=soup2.find(class_='table table-bordered')
                    sall=s01.find_all('tbody')
                    Reverse_param={"Процесор":'proc',"На чіпсеті":'mb',
                    "Потужність":'ps',
                    "Корпус":'case',"Кулер для процесора":'cool'}
                    lis_par=["Процесор","На чіпсеті","Потужність","Корпус","Кулер для процесора"]
                    temp_hdd_ssd = []
                    temp_mem = []
                    temp_video = []
                    for x in sall:
                        for y in x.findAll('tr'):
                            to_dict = re.sub(r':','',(y.find('td').text).strip())
                            if to_dict in lis_par:
                                try:
                                    temp = y.find_all('td')[1].text
                                except:
                                    temp = ''
                                n[Reverse_param[to_dict]] = temp
                            elif to_dict in ("Об'єм HDD", "Диск SSD","SSD M.2 NVMe"):
                                try:
                                    temp_hdd_ssd.append(to_dict[-3:].lower() + ' ' +  y.find_all('td')[1].text)
                                except:
                                    temp_mem.append('')
                            elif to_dict in ("Об'єм пам'яті ОЗУ", "Частота шини"):
                                try:
                                    temp_mem.append(y.find_all('td')[1].text)
                                except:
                                    temp_mem.append('')
                            elif to_dict in ("Відеокарта", "Объем видеопамяти"):
                                try:
                                    temp_video.append(y.find_all('td')[1].text)
                                except:
                                    temp_video.append('')
                    #print((temp_hdd_ssd,temp_mem))
                    try:
                        n['hdd'] = temp_hdd_ssd[0] + ';' + temp_hdd_ssd[1] if len(temp_hdd_ssd) == 2 else temp_hdd_ssd[0]
                    except:
                        n['hdd'] = ''
                    try:
                        n['mem'] = temp_mem[0] + ' ' +  temp_mem[1] if len(temp_mem) == 2 else temp_mem[0]
                    except:
                        n['mem'] = ''
                    try:
                        n['video'] = ttemp_video[0] + ' ' +  temp_video[1] if len(temp_video) == 2 else temp_video[0]
                    except:
                        n['video'] = ''
                try:
                    comp_dict[n['name']] = n
                except:
                    print('error computer code')
                    continue
            print(f'{m} page ok')
    except:
        print('loaded not all objects')
    with open("load_form_providers/loads/it_blok_price2.json", "w") as write_file:
        json.dump(comp_dict, write_file)

    print(f'finished  {len(comp_dict.keys())} objects loaded')
    return comp_dict

def get_versum():
    try:
        comp_dict = {}
        url = 'https://versum.ua'
        for m in range(1,13):
            try:
                g=get_html(url+'/pc/?page={}'.format(m))
            except:
                print(f'error in {m} page will try with timeout')
                time.sleep(11)
                g=get_html(url+'/pc/?page={}'.format(m))
            if g:
                soup = BeautifulSoup(g, "html.parser")
            else:
                continue
            list1=soup.find_all(class_='catalog-item')
            for x in list1:
                comp_praram = {}
                comp_praram['comp_url'] = x.find(class_='catalog-title').find('a').get('href')
                comp_praram['name'] = comp_praram['comp_url'].split('/')[-1]
                try:
                    comp_praram['price'] = int(re.sub(r'\D','',x.find(class_='catalog-price').get_text()))
                except:
                    comp_praram['price'] = ''
                g2=get_html(comp_praram['comp_url'])
                soup2 = BeautifulSoup(g2, "html.parser")
                soup3=soup2.find(class_='prod-tab')
                for s in soup3.find_all(class_='stat-item'):
                    comp_praram[s.find(class_='stat-min').get_text()]=s.find(class_='stat-text').get_text()
                comp_dict[comp_praram['name']] = comp_praram
            print(f'{m} page ok')
    except:
        print('loaded not all objects')
    with open("load_form_providers/loads/versum_price.json", "w") as write_file:
        json.dump(comp_dict, write_file)
    print(f'finished  {len(comp_dict.keys())} objects loaded')
    return comp_dict

def hdd_enumerate(h):
    h=h.split('+')
    temp=[]
    for x in h:
        if x.lower().find('hdd')!=-1:
            temp.append('3,5 ' + x.strip())
        elif x.lower().find('ssd')!=-1:
            temp.append(x.strip())
        else:
            temp.append('3,5 ' + x.strip())
    return temp

def get_fury():
    furylist=['HELLCAT PRO', 'G-POWER', 'BACK TO SCHOOL', 'AMD RYZEN', 'CHALLENGER R1', 'BACK TO SCHOOL 2', 'Zeus Evo', 'AVENTADOR', 'PRO GAMER 3000', 'GRIFFIN POWER', 'SPECIAL-B', 'DOMINATOR ULTRA', 'EX MACHINA', 'GTA V - SPECIAL EDITION', 'VALKYRIE STORM', 'ChiChi 3000', 'CEREBRO ROG', 'ICARUS XK-120', 'CYCLONE F23', 'CRYSTAL DRAGON', 'AVENTUM QX', 'HURRICANE X', 'VECTOR SIGMA', 'RAVEN X-TREME', 'MATRIX EXTREME', 'PLATINUM POWER', 'WARRIOR F1', 'RED QUEEN', 'AMD Threadripper Конфигуратор', 'Intel Core i7 Конфигуратор', 'STEEL PHOENIX', 'VI NITRO', 'TITANIUM ARMOR', 'INTECEPTOR 7000', 'WORKER VX7', 'DARK AVENGER', 'AMD RYZEN 2 ', 'SCORPIO X1 ', 'GOLD GAMER-EVOLUTION ', 'THE POWER', 'PREDATOR', 'VENOM PREMIUM ', 'G8 RAPTOR', 'THE ROCK ', 'JARVIS POWER', 'REVOLT X9', "THOR'S HAMMER", 'SUB-ZERO', 'Z-DAY 3000', 'PERFORMANCE X', 'RED JACK', 'DESTROYER ZX', ' AMD EXTREME', 'QUATTROPORTE LX', 'JACK THE RIPPER', 'WINNER PRO', 'AMD RYZEN 3 ', 'NASA MARS 2025', 'RED SPARROW', 'GX12 DESTROYER', 'CONQUEROR 1805', 'SLEEPWALKER', 'ELEMENT 7', 'KING THREADRIPPER', 'MEDUSA AURUM', 'REVOLT X7', 'GENESIS GAME', 'X-PRO', 'REVOLT X1', 'REVOLT X3', 'POWER BLADE', 'GALAXY RYZEN 3 ']

    url = 'https://digitalfury.pro/filters/?search='
    dict_product ={}
    list_id = ['proc', 'video', 'mem', 'mb', 'hdd', 'case', 'ps']
    for m in furylist:
        list_temp = []
        g=get_html(url+m)
        soup = BeautifulSoup(g, "html.parser") if g else None
        ss = soup.find(class_='filters_products_block').find('a')
        list_li = ss.find_all('li') if ss else None
        if list_li and len(list_li) == len(list_id):
            dict_temp = {}
            for y,x in enumerate(list_li):
                dict_temp[list_id[y]] = x.get_text()
            price = ss.find(class_='product_block_prices_new')
            dict_temp['price'] = price.get_text() if price else ''
            name = ss.find(class_='product_block_title')
            dict_temp['name'] = name.get_text().strip() if name else ''
            dict_temp['comp_url'] = url+m
            dict_temp['hdd'] = hdd_enumerate(dict_temp['hdd'])
            dict_temp['cool'] = ''
            dict_temp['class'] = ''
            dict_temp['warranty'] = ''
        else:
            continue
        dict_product[m.strip()] = dict_temp
    with open("load_form_providers/loads/fury_price.json", "w") as write_file:
        json.dump(dict_product, write_file)
    return dict_product

def get_ua():

    with open("dict_code.json", "r") as write_file:
        dict_code=json.load(write_file)

    comp_dict = {}
    url = 'https://www.uastore.com.ua/'
    for m in range(2,10):
        g=get_html(url+f'/catalog/sistemnye-bloki-pk?page={m}')
        if g:
            soup = BeautifulSoup(g, "html.parser")
        else:
            continue
        sf=soup.find_all(class_='details')
        for s in sf:
            ifcpu = 0
            forcpu = s.find(class_="annotation")
            forcpu = forcpu.get_text() if forcpu else ''
            forcpu = forcpu.split('/') if forcpu else []
            if forcpu and len(forcpu) > 3:
                cpu = get_cpu(forcpu[0])
                for k,v in dict_code.items():
                    if cpu == v[1] and cpu != '':
                        ifcpu = 1
                        break
                if ifcpu:
                    temp_dict ={}
                    ts = s.find(class_='price')
                    temp_dict['price'] = ts.get_text() if ts else ''
                    href = s.find('a')
                    temp_dict['comp_url'] = url+href.get('href') if href else ''
                    g2 = get_html(temp_dict['comp_url'])
                    if g2:
                        soup2 = BeautifulSoup(g2, "html.parser")
                    else:
                        continue
                    temp = soup2.find_all(class_="gift_list_item")
                    if temp:
                        for e,t in enumerate(temp):
                            temp_dict[f'itm{e}-'] = t.find(class_="gift_list_price_value").get_text()
                    sspr=soup2.find('div',id="features_product")
                    if sspr:
                        li=sspr.find_all('li')
                    else:
                        continue
                    if li:
                        for l in li:
                            try:
                                temp_dict[l.find('label').get_text()] = l.find('span').get_text()
                            except:
                                print('error in <li>')
                    comp_dict[temp_dict['comp_url'][36:]] = temp_dict
                else:
                    continue
            else:
                continue
    with open("load_form_providers/loads/ua_price.json", "w") as write_file:
        json.dump(comp_dict, write_file)
    return comp_dict

def get_art():
    comp_dict = {}
    url = 'https://artline.ua/catalog/kompyutery-artline/tip=kompyuter/page='
    try:
        for m in range(1,39):
            try:
                g=get_html(url + f'{m}')
            except:
                print(f'error in {m} page will try with timeout')
                time.sleep(11)
                g=get_html(url + f'{m}')
            if g:
                soup = BeautifulSoup(g, "html.parser")
            else:
                continue
            sf=soup.find_all(class_='product-cart')
            for s in sf:
                status = s.find(class_='product-cart__status')
                if status:
                    status = status.get_text()
                    if status.lower().find('нет') != -1:
                        continue
                    else:
                        temp_dict ={}
                        a = s.find('a')
                        temp_dict['comp_url'] = a.get('href') if a else ''
                        g2 = get_html(temp_dict['comp_url'])
                        if g2:
                            soup2 = BeautifulSoup(g2, "html.parser")
                        else:
                            continue
                        try:
                            temp_dict['price'] = soup2.find(class_='product__price').find(class_='product__price-normal').get_text()
                        except:
                            temp_dict['price'] = ''
                        if re.findall(r'\d+',temp_dict['price']):
                            temp_dict['price'] = re.findall(r'\d+',temp_dict['price'])[0]
                        ss=soup2.find(class_='product__sort-desc expanded')
                        if ss:
                            if ss.find_all('li'):
                                for l in ss.find_all('li'):
                                    try:
                                        temp=l.get_text().split(':')
                                        temp_dict[temp[0]] = temp[1]
                                    except:
                                        continue
                        temp_dict['name'] = temp_dict['comp_url'][27:]
                        comp_dict[temp_dict['comp_url'][27:]] = temp_dict
    except:
        print('loaded not all objects')
    with open("load_form_providers/loads/art_price.json", "w") as write_file:
        json.dump(comp_dict, write_file)
    print(f'finished  {len(comp_dict.keys())} objects loaded')
    return comp_dict
