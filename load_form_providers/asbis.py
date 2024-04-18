from load_form_providers.get_service import download_file,get_from_xml_asbis,get_from_xml_asbis2
#from bs4 import BeautifulSoup
import requests,re
import pandas as pd
import json
from lxml import etree
from xml.etree.ElementTree import ParseError

class ASBIS:
    ASBIS_USERNAME = 'peregon21'
    ASBIS_PASSWORD = 'discovery21'

    price_url = f'https://services.it4profit.com/product/ru/508/PriceAvail.xml?USERNAME={ASBIS_USERNAME}&PASSWORD={ASBIS_PASSWORD}'

    def __init__(self, usd_ua):
        self.usd_ua = usd_ua

    def get_price(self):
        with open("load_form_providers/list_articles.json", "r") as write_file:
            list_get_list2=json.load(write_file)
        return list_get_list2

    def get_basa(self, fun2=0):
        ff = self.get_price() if fun2 else 0
        price_columns = [
            'WIC', 'DESCRIPTION', 'MY_PRICE', 'AVAIL', 'SMALL_IMAGE', 'Url', 'GROUP_NAME',
            'RETAIL_PRICE'
        ]
        if not fun2:
            try:
                r = requests.get(self.price_url, timeout=30)
            except:
                return pd.DataFrame()
            data, index = get_from_xml_asbis2(r, self.usd_ua)
            basa = pd.DataFrame(
            data, columns=price_columns, index=index) if r.status_code == 200 else pd.DataFrame()
            return basa

        filename = download_file(self.price_url, 'load_form_providers/asbis-price.xml')

        basa = pd.DataFrame(get_from_xml_asbis(filename, ff), columns=price_columns) if filename else pd.DataFrame()

        return basa

    def get_sort_basa2(self):
        res=self.get_basa()
        if not res.empty:
            res2=res.rename(columns={'WIC':'partnumber_parts', 'DESCRIPTION':'name_parts',
            'MY_PRICE':'providerprice_parts','AVAIL':'availability_parts',
            'SMALL_IMAGE':'images', 'Url':'url_parts', 'GROUP_NAME':'subcategory',
            'RETAIL_PRICE': 'RRP_UAH'
            })
            return res2
        return pd.DataFrame()

    def get_sort_basa(self):
        res=self.get_basa(fun2=1)
        ff = self.get_price()

        def com_l(d,element):
            if element:
                for x in d:
                        if x.WIC==element:
                            return True, x
                return False, pd.DataFrame()
            else:
                return False, pd.DataFrame()

        list_asbis=[]
        for x in ff:
            s1,s2 = com_l(res.iloc,x)
            if s1:
                list_asbis.append(s2)
            else:
                list_asbis.append(pd.DataFrame())
        return list_asbis

    """def get_sort_basa2(self):
        res=self.get_basa()

        list_asbis=[]
        for x in res.iloc:
            if not x.empty:
                list_asbis.append(x)
            else:
                list_asbis.append(pd.DataFrame())
        return list_asbis"""

    def send_res(self, w=0):
        try:
            with open("dict_file.json", "r") as read_file:
                data = json.load(read_file)
        except Exception as e:
            print(e)
            data = {}

        dict_serj = {'asbis': ["G2:G2000", "H5:H1500", 6, 7]}
        dict_it={}

        res = self.get_basa()
        print('ok... Asbis loaded')
        #dict_it[artile_test(x.WIC)]=(price_test(x.MY_PRICE), artile_test(x.AVAIL))

        for x in res.iloc:
            if artile_test(x.AVAIL) == '' or artile_test(x.AVAIL) == 'звоните':
                dict_it[artile_test(x.WIC)]=(price_test(x.MY_PRICE), 1)
            else:
                dict_it[artile_test(x.WIC)]=(price_test(x.MY_PRICE), 0)

        try:
            list_get_list = get_list_sheet("Price", "B5:B1000")
        except:
            print('not received get_list_sheet')
            list_get_list = []

        dict_for_paint = send_all(data, dict_it, list_get_list, dict_serj['asbis'], wait=w)
        print('ok... Asbis sended')

        return dict_for_paint
