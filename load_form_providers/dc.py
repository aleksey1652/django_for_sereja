from load_form_providers.get_service import download_file,get_from_xml
#from bs4 import BeautifulSoup
import requests,re
import pandas as pd
import json
from lxml import etree
from xml.etree.ElementTree import ParseError

class DC:
    DC_LOGIN = 'itblok'
    DC_PASSWORD = 'VIA5qPUv'

    def get_price(self):
        with open("load_form_providers/list_articles.json", "r") as write_file:
            list_get_list2=json.load(write_file)
        return list_get_list2

    def get_basa(self, fun2=0):
        ff = self.get_price() if fun2 else 0
        try:
            r = requests.post('https://api.dclink.com.ua/api/GetPriceAll', data={
                'login': self.DC_LOGIN,
                'password': self.DC_PASSWORD
            })
        except Exception as e:
            print(e)
            r = ''

        price_columns = [
            'Article', 'CategoryID', 'Name',
            'Availability', 'PriceUSD', 'RRP_UAH',
            'Code','Url'
                        ]

        price_filename = 'load_form_providers/dclink-price.xml'

        try:
            with open(price_filename, 'wb') as f:
                f.write(r.content)
        except Exception as e:
            print('Dc wrong data loaded old price')

        basa = pd.DataFrame(get_from_xml(price_filename, ff), columns=price_columns)

        return basa

    def get_exch(self):

        r = requests.post('https://api.dclink.com.ua/api/GetExchangeRates', data={
            'login': self.DC_LOGIN,
            'password': self.DC_PASSWORD
        })

        try:
            ww=etree.fromstring(r.content)
        except:
            print('Wrong  data')
            return ''

        for appt in ww.getchildren():
            for x in appt.getchildren():
                if  x.tag=="CashRate":
                    return float(x.text)

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

        list_dc=[]
        for x in ff:
            s1,s2 = com_l(res.iloc,x)
            if s1:
                list_dc.append(s2)
            else:
                list_dc.append(pd.DataFrame())
        return list_dc
"""
        with open(price_filename, 'rb') as f:
            basa = pd.DataFrame(get_elements_values(
                price_columns, f, 'Product'
            ), columns=price_columns)"""
