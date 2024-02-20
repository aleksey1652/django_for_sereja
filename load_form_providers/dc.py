from load_form_providers.get_service import download_file,get_from_xml,get_from_dc
#from bs4 import BeautifulSoup
import requests,re
import pandas as pd
import json
from lxml import etree
from xml.etree.ElementTree import ParseError

Category_main_dict = {
'11': 'mouse',
'24': 'pads',
'5': 'mon',
'255': 'wifi',
'33': 'keyboards',
'56': 'headsts',
'125': 'chairs',
'1410': 'wifi',
'125': 'tables',
}

class DC:
    DC_LOGIN = 'itblok'
    DC_PASSWORD = 'VIA5qPUv'

    def get_price(self):
        with open("load_form_providers/list_articles.json", "r") as write_file:
            list_get_list2=json.load(write_file)
        return list_get_list2

    def get_basa(self, fun2=0):
        ff = self.get_price() if fun2 else 0
        CategoryID = ['8', '3', '724', '255', '1', '9', '27', '2', '23', '6', '5']
        try:
            r = requests.post('https://api.dclink.com.ua/api/GetPriceAll', data={
                'login': self.DC_LOGIN,
                'password': self.DC_PASSWORD
            }, timeout=30)
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

        if not ff:
            data,index = get_from_dc(r, CategoryID)
            basa = pd.DataFrame(data, columns=price_columns, index=index) if data else pd.DataFrame()


            return basa


            """list_periphery, dict_category_periphery, dict_category_foto = get_from_xml(
            r.content, self.DC_LOGIN, self.DC_PASSWORD, periphery=True)"""

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

    def get_sort_basa2(self):
        res=self.get_basa()
        if not res.empty:
            res2=res.rename(columns={'Article':'partnumber_parts', 'Name':'name_parts',
            'PriceUSD':'providerprice_parts',
            'Availability':'availability_parts', 'Code':'images', 'Url':'url_parts',
            'CategoryID':'subcategory',
            'RRP_UAH':'RRP_UAH'})
            return res2
        return pd.DataFrame()
