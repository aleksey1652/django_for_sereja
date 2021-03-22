import hashlib
from load_form_providers.get_service import get_from_xml_brain
#from bs4 import BeautifulSoup
import requests,re
import pandas as pd
import json
from lxml import etree
from xml.etree.ElementTree import ParseError

def download_file(url, s=requests):
    try:
        r = s.get(url)
        with open('load_form_providers/brain-price.json', 'wb') as f:
            f.write(r.content)

        return 'load_form_providers/brain-price.json'
    except Exception as e:
        print(e)
        return ''

class BRAIN:
    BRAIN_LOGIN = 'peregons@ukr.net'
    BRAIN_PASSWORD = 'gbpltw11'

    def __met(self):
        r = requests.post('http://api.brain.com.ua/auth', data={
            'login': self.BRAIN_LOGIN,
            'password': hashlib.md5(self.BRAIN_PASSWORD.encode('utf-8')).hexdigest()
        })

        if r.status_code == 200:
            return r.json()['result']

    def __tt(self, s):
        r = requests.get(f'http://api.brain.com.ua/targets/{s}')
        return r.json()['result']

    def __get_from_brain(self, filename, ff):
        try:
            with open(filename, "r") as write_file:
                j=json.load(write_file)
        except:
            print(f'not json file')
            j={}
        list_soup_dict=[]
        for x in j.keys():
            d={}
            for k,v in j[x].items():
                if k in ['Article', 'Name', 'PriceUSD', 'Available', 'URL']:
                    d[k]=v
            if ff:
                if d['Article'] in ff: list_soup_dict.append(d)
            else:
                list_soup_dict.append(d)
        return list_soup_dict

    def __board(self, s, t, ff):
        if t['targetID'] in (4,29):
            r = requests.get(f"http://api.brain.com.ua/pricelists/{t['targetID']}/json/{s}")
            if r.json()['status']:
                filename = download_file(r.json()['url'])
                return self.__get_from_brain(filename, ff)

    def get_price(self):
        with open("load_form_providers/list_articles.json", "r") as write_file:
            list_get_list2=json.load(write_file)
        return list_get_list2

    def get_basa(self, fun2=0):
        ff = self.get_price() if fun2 else 0
        price_columns = [
            'Article',
            'Name',
            'PriceUSD',
            'Available',
            'URL'
                        ]

        s = self.__met()

        l_full = []
        for t in self.__tt(s):
            l = self.__board(s, t, ff)
            if l:
                l_full+=l
        basa = pd.DataFrame(l_full, columns=price_columns) if l_full else pd.DataFrame()

        return basa

    def get_sort_basa(self):
        res=self.get_basa(fun2=1)
        ff = self.get_price()

        def com_l(d,element):
            if element:
                for x in d:
                        if x.Article==element:
                            return True, x
                return False, pd.DataFrame()
            else:
                return False, pd.DataFrame()

        list_brain=[]
        for x in ff:
            s1,s2 = com_l(res.iloc,x)
            if s1:
                list_brain.append(s2)
            else:
                list_brain.append(pd.DataFrame())
        return list_brain

    def send_res(self, w=0):
        try:
            with open("dict_file.json", "r") as read_file:
                data = json.load(read_file)
        except Exception as e:
            print(e)
            data = {}

        dict_serj = {'brain': ("E2:E2000", "F5:F1500", 4, 5)}
        dict_it = {}

        res = self.get_basa()
        print('ok... Brain loaded')

        for x in res.iloc:
            if x.Available and x.Available != '1' and x.Available != '0':
                dict_it[artile_test(x.Article)]=(price_test(x.PriceUSD), 0)
            else:
                dict_it[artile_test(x.Article)]=(price_test(x.PriceUSD), 1)
            #dict_it[artile_test(x.Article)]=price_test(x.PriceUSD)

        try:
            list_get_list = get_list_sheet("Price", "B5:B1000")
        except:
            print('not received get_list_sheet')
            list_get_list = []

        dict_for_paint = send_all(data, dict_it, list_get_list, dict_serj['brain'], wait=w)
        print('ok... Brain sended')
        return dict_for_paint
