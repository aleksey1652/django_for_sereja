from bs4 import BeautifulSoup
import requests
import pickle
#import pickle5 as pickle
from random import choice
import re
import pandas as pd
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
"""
def get_cpu(c):
    a=[]
    if re.findall(r'^\d(.+)',c):
        c=re.findall(r'^\d(.+)',c)[0]
    '''if 'Я' in c:
        c=re.findall(r'(.+)\d-Я',c)[0]'''
    if 'celeron' in c.lower():
        c=re.sub(r'\D',' ',c).strip().split(' ')[0]
    if 'pentium' in c.lower():
        c=re.sub(r'\D',' ',c).strip().split(' ')[0]
    if 'threadripper' in c.lower():
        c=re.sub(r'\D',' ',c).strip().split(' ')[0]
    aa=re.sub(r'\D',' ',c).strip().split(' ')[:2]
    for x in aa:
        try:
            a.append(int(x))
        except:
            a.append(x)
            print(c)
    a2=re.findall(r'{}(\D)'.format(a[-1]),c)
    if a2:
        if a2[0] !=' ':
            a.append(a2[0].lower())
    return a

def get_video(a):
    if len(a)<5:
        return []
    if re.findall(r'hd graphics',a.lower()):
        return re.findall(r'hd graphics',a.lower())[:1]
    if re.findall(r'vega',a.lower()):
        return re.findall(r'vega',a.lower())
    if re.findall(r'amd hd',a.lower()):
        return re.findall(r'amd hd',a.lower())
    try:
        a1=[]
        aa=re.sub(r'\D',' ',a).strip().split(' ')[:1]
        if aa:
            a1.append(int(aa[0]))
            a2=re.findall(r'ti',a.lower())
            a3=re.findall(r'super',a.lower())
            if a2:
                a1.append(a2[0])
            if a3:
                a1.append(a3[0])
            return a1

    except:
        return a1

def get_mem(a):
    try:
        if re.sub(r'\D',' ',a).strip().split(' ')[:1]:
            return int(re.sub(r'\D',' ',a).strip().split(' ')[0])
    except:
        return 0
"""
def random_headers():
    return {'User-Agent': choice(desktop_agents),'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}



def get_html(url):
    response = requests.get(url,proxies=None,timeout=10,headers=random_headers())
    return response.text if response.ok else False

def get_list(y,h):
    list1=[]
    for x in y.get_text().split('\n'):
        if x !='':
            list1.append(x.strip())
    list1[0]=(list1[0],get_cpu(list1[0]))
    list1[1]=(list1[1],get_video(list1[1]))
    list1[2]=(list1[2],get_mem(list1[2]))
    list1.append(h)
    return list1

def get_soup_it_f(url,par1='item-info',par2='td',par3='special-price'):
    dict1={}
    yy=0
    for m in range(1,24):
        g=get_html(url+'/computeri.html'+'?page={}'.format(m))
        if g:
            soup = BeautifulSoup(g, "html.parser")
        else:
            continue
        list1=[]
        list2=[]
        for x in soup.find_all(class_='product-image'):
            list2.append(x.get('href')) if x else ' '
        for x in soup.find_all(class_=par1):
            list1.append(x) if x else ' '
        for y,x in enumerate(list1):
                list0=x.find_all(par2)
                if len(list0)>10:
                    list1=[list0[1].get_text(),list0[7].get_text(),list0[5].get_text(),list0[9].get_text(),list0[11].get_text()]
                else:
                    list1=[list0[1].get_text(),list0[7].get_text(),list0[5].get_text(),list0[9].get_text()]
                list1[0]=(list1[0],get_cpu(list1[0]))
                list1[1]=(list1[1],get_video(list1[1]))
                list1[2]=(list1[2],get_mem(list1[2]))
                list1.append(url+'/{}'.format(list2[y]))
                if x.find(class_=par3):
                    dict1[y+yy]=(list1,int(''.join(re.findall(r'\d',x.find(class_=par3).get_text()))))
                else:
                    dict1[y+yy]=(list1,0)
        yy=yy+y+1
    print(len(dict1))
    return dict1

def get_soup_ua(url):
    dict1={}
    yy=0
    pp=0
    for m in range(2,4):
        g=get_html(url+'/catalog/sistemnye-bloki-pk?page={}'.format(m))
        if g:
            soup = BeautifulSoup(g, "html.parser")
        else:
            continue
        for z,y in enumerate(soup.find_all(class_='details')):
            list_pr=[]
            try:
                list_pr.append(y.find(class_="annotation").get_text())
            except:
                list_pr.append(' ')
            list_pr=list_pr[0].split('/')
            if len(list_pr)>3:
                list_pr[0]=(list_pr[0],get_cpu(list_pr[0]))
                list_pr[1]=(list_pr[1],get_mem(list_pr[1]))
                list_pr[3]=(list_pr[3],get_video(list_pr[3]))
                a=list_pr[1]
                list_pr[1]=list_pr[3]
                list_pr[3]=a
                a=list_pr[2]
                list_pr[2]=list_pr[3]
                list_pr[3]=a
                #href=y.find(class_='')
                href=y.find('a')
                if href:
                    href=href.get('href')
                    if href!=None: list_pr.append(url+'/'+href)
                if y.find(class_='price'):
                    try:
                        c=int(re.sub(r'\D','',y.find(class_='price').get_text()))
                    except:
                        c=0
                else:
                    c=0
                dict1[z+yy-pp]=(list_pr,c)
            else:
                pp=pp+1
        yy=yy+z+1
    print(len(dict1))
    return dict1

def get_soup_versum(url):
    dict1={}
    yy=0
    pp=0
    for m in range(1,10):
        g=get_html(url+'/pc/?page={}'.format(m))
        if g:
            soup = BeautifulSoup(g, "html.parser")
        else:
            continue
        for z,y in enumerate(soup.find_all(class_='catalog-item')):
            list_pr=[]
            for i in y.find_all(class_='stat-text'):
                try:
                    list_pr.append(i.get_text())
                except:
                    list_pr.append(' ')
            if len(list_pr)>3:
                list_pr[2]=(list_pr[2],get_video(list_pr[2]))
                list_pr[0]=(list_pr[0],get_cpu(list_pr[0][:-7]))
                list_pr[3]=(list_pr[3],get_mem(list_pr[3]))
                list_pr.pop(1)
                href=y.find(class_='catalog-title')
                if href:
                    try:
                        href=href.find('a').get('href')
                        list_pr.append(href)
                    except:
                        href=0
                if y.find(class_='catalog-price'):
                    try:
                        c=int(re.sub(r'\D','',y.find(class_='catalog-price').get_text()))
                    except:
                        c=0
                else:
                    c=0
                dict1[z+yy-pp]=(list_pr,c)
        else:
                pp=pp+1
        yy=yy+z+1
    print(len(dict1))
    return dict1

def get_soup_fury(url,dict1):
    list2=['g-power','zeus-evo','EX_MACHINA','GTA_5_Edition','special-b','ChiChi_3000','VALKYRIE_STORM',
    'CEREBRO_ROG','crystal_dragon','RED_QUEEN','VECTOR_SIGMA','INTECEPTOR_7000','HURRICANE_X','worker_vx7',
    'steel-phoenix','ICARUS_XK-120','TITANIUM_ARMOR','VI_NITRO','DARK_AVENGER','G8_RAPTOR','JARVIS_POWER',
    'the_rock','amd-ryzen-2','SUB-ZERO','MATRIX_EXTREME','Z-DAY_3000','red_jack_rx','PERFORMANCE_X',
    'THORS_HAMMER','DESTROYER_ZX','Gold_Gamer_Evolution','QUATTROPORTE_LX','JACK_THE_RIPPER','NASA_MARS_2025',
    'sleepwalker','CONQUEROR_1805','revolt_x58','king_threadripper','red_sparrow','GX12_DESTROYER','WINNER_PRO',
    'PREDATOR','THE_POWER','WARRIOR_F1','GENESIS_GAME','X-PRO','amd_extreme','amd-ryzen-3']
    long_dict=len(dict1)
    for v,z in enumerate(list2):
        g=get_html(url+'/computer/'+z)
        if g:
            soup = BeautifulSoup(g, "html.parser")
        else:
            continue

        list1=[]
        for x in (7,10,11,14,15):
            s=soup.find(id='comto{}'.format(x))
            try:
                if x==11:
                    if s.find_all('span')[0].get_text()=='Не устанавливать видеокарту':
                        list1.append(s.find_all('span')[1].get_text())
                    else:
                        list1.append(s.find_all('span')[0].get_text())
                else:
                    list1.append(s.find('span').get_text())
            except:
                list1.append('')
                print(z)

        a=list1[2]
        list1[2]=list1[1]
        list1[1]=a
        list1[0]=(list1[0],get_cpu(list1[0]))
        list1[1]=(list1[1],get_video(list1[1]))
        list1[2]=(list1[2],get_mem(list1[2]))
        list1.append(url+'/computer/'+z)
        c=soup.find(class_='bottom_price_nav')
        c=c.find(class_='bottom_price') if c else ''
        try:
            c=int(re.sub(r'\D','',c.get_text()))
            dict1[long_dict+v]=(list1,c)
        except:
            dict1[long_dict+v]=(list1,0)

def get_cp(l):
    aa=l.split('.')[0]
    aa=aa[:-2]
    aa=aa[-12:]
    return get_cpu(aa)



def get_soup_art(url):
    dict1={}
    yy=0
    pp=0
    for m in range(0,781,20):
        g=get_html(url+'/kompyutery-artline?start={}'.format(m))
        if g:
            soup = BeautifulSoup(g, "html.parser")
        else:
            continue
        list_href=[]
        list_c=[]
        for c in soup.find_all('div',class_='PricesalesPrice'):
            try:
                list_c.append(int(re.sub(r'\D','',c.get_text())))
            except:
                list_c.append(0)
        for x in soup.find_all(class_='b1c-name'):
            list_href.append(url+x.get('href'))
        for z,y in enumerate(soup.find_all(class_='product_s_desc')):
            list_pr=[]
            for x in y.get_text().split('\n'):
                if x !='':
                    list_pr.append(x.strip())
            list_pr=list_pr[0].split('/')
            if len(list_pr)>3:
                list_pr[0]=(list_pr[0],get_cp(list_pr[0]))
                list_pr[2]=(list_pr[2],get_mem(list_pr[2]))
                list_pr[-3]=(list_pr[-3],get_video(list_pr[-3]))
                a=list_pr[1]
                list_pr[1]=list_pr[-3]
                list_pr[-3]=a
                list_pr[-1]=list_href[z]
                dict1[z+yy-pp]=(list_pr,list_c[z])
            else:
                pp=pp+1
        yy=yy+z+1
    print(len(dict1))
    return dict1

def get_soup(html,par1,par2,par3,url):
    soup = BeautifulSoup(html, "html.parser")
    dict1={}
    for y,x in enumerate(soup.find_all(class_=par1)):
        href=x.find(class_='product_block_stars_and_reviews crr-cnt no-vr')
        href=href.get('data-crr-url') if href else ' '
        try:
            c=int(''.join(re.findall(r'\d',x.find(class_=par3).get_text())))
        except:
            c=0
        dict1[y]=(get_list(x.find(class_=par2),href),c)
    get_soup_fury(url,dict1)
    print(len(dict1))
    return dict1

def pickl(list_s,pi):
    with open(pi,'wb') as f:
	    pickle.dump(list_s, f)

if __name__ == '__main__':
    par1='mobile_product_block'
    par2='mobile_product_block_info'
    par3='product_block_prices_new'
    url='https://digitalfury.pro'
    url2='https://it-blok.com.ua'
    url3='http://artline.ua'
    pickl(get_soup(get_html(url),par1,par2,par3,url),'pickl1.txt')
    #pickl(get_soup_it_f(url2,par1='item-info',par2='td',par3='special-price'),'pickl3.txt')
    #pickl(get_soup_art(url3),'pickl_art.txt')
    #pickl(get_soup_ua('https://uastore.com.ua'),'pickl_ua.txt')

def get_video(a):
    list_brand=['sapphire','msi','gigabyte','asus','inno3d','palit','colorful']
    if len(a)<5:
        return []
    if re.findall(r'hd graphics',a.lower()):
        return re.findall(r'hd graphics',a.lower())
    if re.findall(r'vega',a.lower()):
        return re.findall(r'hd graphics',a.lower())
    if re.findall(r'amd hd',a.lower()):
        return re.findall(r'hd graphics',a.lower())
    if re.findall(r'hd',a.lower()):
        return re.findall(r'hd graphics',a.lower())
    try:
        atr_list=['super','ti','xt']
        aa=re.sub(r'\D',' ',a).strip().split(' ')
        if aa:
            aa=aa[:1]
            for x in atr_list:
                if re.findall(r'{}'.format(x),a.lower()):
                    aa.insert(1,x)
            for x in list_brand:
                if re.findall(r'{}'.format(x),a.lower()):
                    aa.append(x)
                    return aa
            aa.append('')
            return aa
        else:
            return []
    except:
        return []

def get_cpu(c):
    a=[]
    ge = c.lower().find('ge')
    if re.findall(r'^\d(.+)',c):
        c=re.findall(r'^\d(.+)',c)[0]
    aa=re.sub(r'\D',' ',c).strip().split(' ')[:2]
    aa=[i for i in aa if i] if aa else None
    for x in aa:
        try:
            a.append(int(x))
        except:
            a.append(x)
            print(c)
    a2=re.findall(r'{}(\D+)'.format(a[-1]),c) if a else ''
    if a2:
            if len(a2[0])>1  and a2[0][0]!=' ':
                a.append(a2[0][:2].strip().lower())
            elif len(a2[0])==1 and a2[0][0]!=' ':
                a.append(a2[0].lower())
    if a and a[-1]!='ge' and ge!=-1:
        a.append('ge')
    return a

def get_hdd_ssd(c, plan=0):
    list_hdd = []
    list_brand=['toshiba','seagate','wd','kingston','crucial','goodram','gigabyte']
    if plan==0:
        for x in ['ssd','3,5']:
            temp = re.findall(r'{}'.format(x),c.lower())
            if temp:
                temp_list = re.sub(r'\D',' ',c).strip().split(' ')
                temp_list = [i for i in temp_list if i] if temp_list else None
                list_hdd.append(x)
                if temp_list and len(temp_list[-1])<4:
                    list_hdd.append(temp_list[-1])
                elif temp_list and len(temp_list[-1])>=4:
                    list_hdd.append(temp_list[-1][0])
                else:
                    list_hdd.append('')
        for x in list_brand:
            if re.findall(r'{}'.format(x),c.lower()):
                list_hdd.append(x)
                return list_hdd
        list_hdd.append('')
        return list_hdd
    elif plan=='s':
        temp_list = re.sub(r'\D',' ',c).strip().split(' ')
        temp_list = [i for i in temp_list if i] if temp_list else None
        if temp_list:
            list_hdd.append('ssd')
            list_hdd.append(temp_list[0])
    elif plan=='h':
        temp_list = re.sub(r'\D',' ',c).strip().split(' ')
        temp_list = [i for i in temp_list if i] if temp_list else None
        if temp_list:
            list_hdd.append('3,5')
            if len(temp_list[0])<4:
                list_hdd.append(temp_list[0])
            else:
                list_hdd.append(temp_list[0][0])
    return list_hdd

def get_mb(c):
    list_brand=['asrock','msi','gigabyte','asus','biostar']
    list_mb = []
    list_atr =[' atx', 'itx']
    temp_list = re.sub(r'\D',' ',c).strip().split(' ')
    temp_list = [i for i in temp_list if i] if temp_list else []
    list_mb.append(temp_list[0]) if temp_list else None
    if list_mb:
        for x in list_atr:
            if re.findall(r'{}'.format(x),c.lower()):
                list_mb.insert(1,x)
                break
    for x in list_brand:
        if re.findall(r'{}'.format(x),c.lower()):
            list_mb.append(x)
            return list_mb
    list_mb.append('')
    return list_mb

case_dict={
           'FC-F55A':'Frontier Warlock','MT521-NP':'Gamemax MT521','HAN SOLO-F75A BK/OG':'Frontier Han Solo',
           'CS-105':'AeroCool CS-105','SCOUT BK/BU':'Frontier SCOUT','Graphyte':'Vinga Graphyte',
           'Aerocool Tomahawk':'Aerocool Tomahawk','Pardo White':'Gamemax Pardo White',
           'G561-F Blue':'GameMax G561','Thor':'Frontier Thor','T-11':'Inter-Tech T-11',
           'CS213B':'Vinga CS213B','Diamond Black':'Gamemax Diamond','ET-210-400':'Gamemax ET210',
           'ET-211-400':'Gamemax ET211','LB-081':'FrimeCom LB-081',
           'R1-450SI':'1stPlayer R1-450SI Black','Smart-400W':'Vinga Smart',
           'ST-610G':'ST610G','ST-610W':'ST610W',
           'FC-F75A-500 BK/OG':'Frontier Han Solo','Smart-450W':'Vinga Smart',
           'F52A-400':'Frontier Qui-Gon','FD-CA-ERA-ITX-GY':'Fractal Design Era ITX Titanium',
           'CS404B':'Vinga CS404B','ST-102':'GameMax ST-102',
           'CA-1B8-00S1WN-00':'ThermalTake Core V1','QBX':'Cougar QBX Black Mini ITX',
           'FD-CA-DEF-NANO-S-BK-W':'Fractal Design Define Nano S','G516 Asgard Red':'GameMax ASGARD Red',
           'RIANBOW-R7 COLOR LED':'1st Player Rainbow-R7-G2 RGB','ACCM-PB17013.11':'Aerocool Aero One',
           'Panda ECO':'Gamemax Panda ECO','Earlkase RGB':'Deepcool Earlkase RGB',
           'Earlkase RGB White':'Deepcool Earlkase RGB White','GAMEMAX Paladin':'GAMEMAX Paladin',
           'MACUBE 310P WH':'Deepcool MACUBE 310P','MX330-G':'Cougar MX330-G',
           'Gemini M (Iron Gray)':'Cougar Gemini M Iron Gray','GS-ATX-MACUBE310P-BKG0P':'Deepcool MACUBE 310P BK',
           'FD-CA-FOCUS-RD-W':'Fractal Design FD-CA-FOCUS-RD-W','MATREXX 55':'Deepcool MATREXX 55',
           'Vampiric 011C':'MSI MAG Vampiric 011C','Vampiric 010X':'MSI Mag Vampiric 010X',
           'Forge 100R':'MSI MAG Forge 100R','Gungnir 100D':'MSI MPG Gungnir 100D',
           'PGS Python':'AEROCOOL PGS Python Black','Aerocool Klaw':'AEROCOOL PGS Klaw RGB',
           '385BMB0.0001':'Cougar Gemini S','Firebase X8 RGB LED':'1st Player X8 RGB',
           'Aerocool Tor Pro':'Aerocool Tor Pro RGB','GP-02B-OP':'Chieftec Stallion II',
           'CA-H500B-BR':'NZXT H500','CSAZ-6000W':'AZZA Storm 6000W',
           'DP-MATX-BNKSBK-LQD':'Deepcool Baronkase Liquid','CA-H700W-BR':'NZXT H700',
           'Panzer Max':'Cougar Panzer Max Black','FD-CA-DEF-R6-WT-TG':'Fractal Design Define R6 White Tempered G',
           'Gemini T':'Cougar Gemini T','Macube 550':'Deepcool Macube 550',
           'Raidmax X08':'Raidmax XO8','Cougar Blazer':'Cougar Blazer','CA-1H7-00M1WN-00':'Thermaltake Versa C23 TG',
           'Panzer EVO':'Cougar Panzer EVO','Panzer EVO RGB':'Cougar Panzer EVO RGB',
           'MCM-H500P-MGNN-S10':'CoolerMaster MasterCase H500P','GB-AC300W':'Aorus AC',
           'GB-C200G':'C200 Glass','Conquer 2':'Cougar Conquer 2','EN44375':'Xigmatek Athena',
           'RAIDER RA08A':'Frontier Raider','DTS-E3015':'DTS-E3015','Vampiric 010M':'MSI Mag Vampiric 010M',
           'Elysium Black':'GameMax Elysium Black','Chaos':'Vinga Chaos'
           }
def get_ps(c,plan=0):
    list_brand=['deepcool','chieftec','gamemax','corsair','be quiet','aorus']
    if plan==0:
        temp_list = []
        temp_list = re.sub(r'\D',' ',c).strip().split(' ')
        temp_list = [i for i in temp_list if i] if temp_list else None
        temp_list = temp_list[-1:] if temp_list else []
        for x in list_brand:
            if re.findall(r'{}'.format(x),c.lower()):
                temp_list.append(x) if temp_list else []
                return temp_list
        temp_list.append('')
        return temp_list
    elif plan=='case':
        temp = re.findall(r'.+\D(\d\d\d)[W,w]$',c.strip())
        return temp if temp else []
    elif plan==1:
        temp = c.strip().lower().split(' ')
        temp = [i for i in temp if i]
        return temp if temp else []
def get_case(c):
    temp=[]

    for k,v in case_dict.items():
        if c.strip().lower().find(v.lower())!=-1:
            temp = [v]
            break
    temp2 = []
    if temp:
        temp2=get_ps(c,plan='case')
        temp2.insert(0,temp) if temp2 else temp2.append(temp)
    return temp2

def pd_proc(pr,n=0):
    #n=0 for versum n=2 for itblok
    list_index = ['Name', 'Partnumbers', 'X_code', 'Advanced']
    temp_dict = {}
    if n==0:
        temp_dict['Name'] = pr
        temp_dict['Partnumbers'] = []
        temp_dict['Advanced'] = []
        temp_dict['X_code'] = get_cpu(pr)
    else:
        temp_dict['Name'] = pr[n]
        temp_dict['Partnumbers'] = []
        temp_dict['Advanced'] = []
        temp_dict['X_code'] = get_cpu(pr[n])
    temp_par=[]
    for x in list_index:
        temp_par.append(temp_dict[x])
    return pd.Series(temp_par,index=list_index)

def pd_mb(mb,n=0):
    #n=0 for versum n=2 for itblok
    list_index = ['Name', 'Partnumbers', 'X_code', 'Advanced']
    temp_dict = {}
    if n==0:
        temp_dict['Name'] = mb
        temp_dict['Partnumbers'] = []
        temp_dict['Advanced'] = []
        temp_dict['X_code'] = get_mb(mb)
    else:
        temp_dict['Name'] = mb[n]
        temp_dict['Partnumbers'] = []
        temp_dict['Advanced'] = []
        temp_dict['X_code'] = get_mb(mb[n])[:-1]
    temp_par=[]
    for x in list_index:
        temp_par.append(temp_dict[x])
    return pd.Series(temp_par,index=list_index)

def get_mem(c,n=0):
    list_brand=['team','crucial ballistix','crucial','kingston','goodram']
    if n==0:
        temp = re.sub(r'\D',' ',c).strip().split(' ')
        temp = [i for i in temp if i] if temp else None
        for x in list_brand:
            if re.findall(r'{}'.format(x),c.lower()):
                temp.append(x)
                return temp
        temp.append('') if temp else None
        return temp if temp else []
    else:
        temp = re.sub(r'\D',' ',c).strip().split(' ')
        temp = [i for i in temp if i] if temp else None
        return temp[:1] if temp else []

def pd_mem(mem,n=0):
    #n=0 for versum n=2 for itblok
    list_index = ['Name', 'Partnumbers', 'X_code', 'Advanced']
    temp_dict = {}
    if n==0:
        temp_dict['Name'] = mem
        temp_dict['Partnumbers'] = []
        temp_dict['Advanced'] = [get_mem(mem)[2]] if len(get_mem(mem))>2 else []
        temp_dict['X_code'] = get_mem(mem)
    else:
        temp_dict['Name'] = mem[n]
        temp_dict['Partnumbers'] = []
        temp_dict['Advanced'] = get_mem(mem[n+2],n=n)
        temp_dict['X_code'] = get_mem(mem[n],n=n)
    temp_par=[]
    for x in list_index:
        temp_par.append(temp_dict[x])
    return pd.Series(temp_par,index=list_index)

def pd_video(v,n=0):
    #n=0 for versum n=4 for itblok
    list_index = ['Name', 'Partnumbers', 'X_code', 'Advanced']
    temp_dict = {}
    if n==0:
        temp_dict['Name'] = v
        temp_dict['Partnumbers'] = []
        temp_dict['Advanced'] = [get_video(v)[-1]] if len(get_video(v))>1 else []
        temp_dict['X_code'] = get_video(v)
    else:
        temp_dict['Name'] = v[n]
        temp_dict['Partnumbers'] = []
        temp_dict['Advanced'] = get_video(v[n+2])[0]  if len(get_video(v[n+2]))>1 and len(v)>n+2 else []
        temp_dict['X_code'] = get_video(v[n])[:-1] if len(get_video(v[n]))>1 else []
    temp_par=[]
    for x in list_index:
        temp_par.append(temp_dict[x])
    return pd.Series(temp_par,index=list_index)

def pd_hdd_ssd(h,n=0):
    list_index = ['Name', 'Partnumbers', 'X_code', 'Advanced']
    temp_dict = {}
    if n==0:
        temp_dict['Name'] = h
        temp_dict['Partnumbers'] = []
        temp_dict['Advanced'] = [get_hdd_ssd(h, plan=0)[-1]] if len(get_hdd_ssd(h, plan=0))>1 else []
        temp_dict['X_code'] = get_hdd_ssd(h, plan=0)
        temp_par=[]
        for x in list_index:
            temp_par.append(temp_dict[x])
        return pd.Series(temp_par,index=list_index)
    else:
        pd_temp = []
        for y,x in enumerate(h):
            temp_dict = {}
            if x.lower().find('hdd')!=-1:
                temp_dict['Name'] = h[y+1]
                temp_dict['Partnumbers'] = []
                temp_dict['Advanced'] = []
                temp_dict['X_code'] = get_hdd_ssd(h[y+1],plan='h')
                temp_par=[]
                for x in list_index:
                    temp_par.append(temp_dict[x])
                pd_temp.append(pd.Series(temp_par,index=list_index))
            elif x.lower().find('ssd')!=-1:
                temp_dict['Name'] = h[y+1]
                temp_dict['Partnumbers'] = []
                temp_dict['Advanced'] = []
                temp_dict['X_code'] = get_hdd_ssd(h[y+1],plan='s')
                temp_par=[]
                for x in list_index:
                    temp_par.append(temp_dict[x])
                pd_temp.append(pd.Series(temp_par,index=list_index))
        return(pd_temp)

def pd_case(c, n=0):
    #n=0 for versum n=2 for itblok
    list_index = ['Name', 'Partnumbers', 'X_code', 'Advanced']
    temp_dict = {}
    if n==0:
        temp_dict['Name'] = c
        temp_dict['Partnumbers'] = []
        temp_dict['Advanced'] = get_case(c)[-1:] if len(get_case(c))>1 else []
        temp_dict['X_code'] = get_case(c)[0] if len(get_case(c))>0 else []
    else:
        temp_dict['Name'] = c[n]
        temp_dict['Partnumbers'] = []
        temp_dict['Advanced'] = get_case(c[n])[-1:] if len(get_case(c[n]))>1 else []
        temp_dict['X_code'] = get_case(c[n])[0] if len(get_case(c[n]))>0 else []
    temp_par=[]
    for x in list_index:
        temp_par.append(temp_dict[x])
    return pd.Series(temp_par,index=list_index)

cooler_dict={'E126M': ['pccooler', 'e126m'], 'GAMMAXX 200T': ['deepcool', 'gammaxx', '200t'], 'GI-UX4': ['pccooler', 'gi-ux4'], 'GAMMAXX 300': ['deepcool', 'gammaxx', '300'], 'SE-224-RGB': ['id-cooling', 'se-224-rgb'], 'dp-mch4-gmx400': ['deepcool', 'gammaxx', '400', 'white'], 'Gammaxx GTE V2': ['deepcool', 'gammaxx', 'gte'], 'Gammaxx GT': ['deepcool', 'gammaxx', 'gt'], 'GI-D66A ': ['pccooler', 'gi-d66a'], 'E32-0802210-A87': ['msi', 'core', 'frozr', 's'], 'E32-0801920-A87': ['msi', 'core', 'frozr', 'l'], 'E32-0802070-A87': ['msi', 'core', 'frozr', 'xl'], 'NH-U14S': ['noctua', 'nh-u14s'], 'NH-U14S TR4 - SP3': ['noctua', 'nh-u14s', 'tr4', '-', 'sp3'], 'NH-D15': ['noctua', 'nh-d15'], 'INTEL-BOX1': ['intel'], 'AMD-BOX1': ['amd'], 'AMD-BOX2': ['amd'], 'AMD-BOX3': ['amd'], 'CWS-SLI': ['контурна', 'сво', 'sli'], 'GAMMAXX L120 T RED': ['gammaxx', 'l120'], 'GAMMAXX L240 V2': ['gammaxx', 'l240'], 'GAMMAXX L240 T RED': ['pccooler', 'gi-ah240u', 'halo', 'rgb'], 'GAMMAXX L360 V2': ['pccooler', 'gi-ah360u', 'halo', 'rgb'], 'RL-KRX52-02': ['nzxt', 'kraken', 'x52'], 'FD-WCU-CELSIUS-S24-BK': ['fractal', 'design', 'celsius', 's24'], 'RL-KRX72-01': ['nzxt', 'kraken', 'x72'], 'SE-802': ['id-cooling', 'se-802'], 'BK021': ['dark', 'rock', '4'], 'GAMMAXX 400 WHITE': ['deepcool', 'gammaxx', '400', 'white'], 'BK022': ['be', 'quiet!', 'dark', 'rock', 'pro', '4'], 'GI-D66A HALO FRGB': ['pccooler', 'gi-d66a', 'halo', 'frgb'], 'MAG CoreLiquid 240R': ['msi', 'mag', 'coreliquid', '240r'], 'MAG CoreLiquid 360R': ['msi', 'mag', 'coreliquid', '360r'], 'AQUA 240': ['cougar', 'aqua', '240'], 'AQUA 360': ['cougar', 'aqua', '360']}

def pd_ps(ps,n=0):
    #n=0 for versum n=2 for itblok
    list_index = ['Name', 'Partnumbers', 'X_code', 'Advanced']
    temp_dict = {}
    if n==0:
        temp_dict['Name'] = ps
        temp_dict['Partnumbers'] = []
        temp_dict['Advanced'] = get_ps(ps)[-1:] if len(get_ps(ps))>1 else []
        temp_dict['X_code'] = get_ps(ps)
    else:
        temp_dict['Name'] = ps[n]
        temp_dict['Partnumbers'] = []
        temp_dict['Advanced'] = get_ps(ps[n])[-1:] if len(get_ps(ps[n]))>1 else []
        temp_dict['X_code'] = get_ps(ps[n])[:-1] if len(get_ps(ps[n]))>1 else []
    temp_par=[]
    for x in list_index:
        temp_par.append(temp_dict[x])
    return pd.Series(temp_par,index=list_index)

def get_cool(cool):
    temp = re.sub('wt$','',cool.lower().strip())
    temp = re.sub('halo frgb$','',temp)
    temp = re.sub('corona b$','',temp)
    temp = re.sub('r$','',temp)
    if cool.lower().find('amd')!=-1:
        temp = 'amd'
    if cool.lower().find('intel')!=-1:
        temp = 'intel'
    return temp


def pd_cool(cool,n=0):
    #n=0 for versum n=2 for itblok
    cool = get_cool(cool)
    list_index = ['Name', 'Partnumbers', 'X_code', 'Advanced']
    temp_dict = {}
    if n==0:
        temp=[]
        for k,v in cooler_dict.items():
            if v == get_ps(cool,plan=1):
                temp = v
                break
        temp_dict['Name'] = cool
        temp_dict['Partnumbers'] = []
        temp_dict['Advanced'] =  []
        temp_dict['X_code'] = temp
    else:
        temp=[]
        for k,v in cooler_dict.items():
            if v == get_ps(cool[n],plan=1):
                temp = v
                break
        temp_dict['Name'] = cool[n]
        temp_dict['Partnumbers'] = []
        temp_dict['Advanced'] =  []
        temp_dict['X_code'] = temp
    temp_par=[]
    for x in list_index:
        temp_par.append(temp_dict[x])
    return pd.Series(temp_par,index=list_index)
