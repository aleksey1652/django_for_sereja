from load_form_providers.get_service import download_file,get_from_html
from bs4 import BeautifulSoup
import requests,re
import pandas as pd
import json
from lxml import etree
from xml.etree.ElementTree import ParseError

class ITLINK:
    ITLINK_LOGIN = 'hotbox'
    ITLINK_PASSWORD = 'рщеищч321!'

    price_url = 'http://it-link.ua/Home/pricelist?id=%20%20%20%20%20A135'

    def get_price(self):
        with open("load_form_providers/list_articles.json", "r") as write_file:
            list_get_list2=json.load(write_file)
        return list_get_list2

    def get_basa(self, fun2=0):
        ff = self.get_price() if fun2 else 0
        with requests.Session() as rs:
            r = rs.post(
                'http://it-link.ua/account/LogOn',
                data={
                    'username': self.ITLINK_LOGIN,
                    'password': self.ITLINK_PASSWORD,
                    'rememberMe': False
                }
            )

            """price_columns = [
                'price', 'model', 'article', 'availability'
            ]
            filename = download_file(self.price_url, 'itlink-price.xml', rs)

            m = get_from_xml(filename)"""

            """if m:
                basa = pd.DataFrame(m, columns=price_columns)
            else:
                price_columns = ['Article', 'Availability', 'Price']
                basa = pd.DataFrame(get_from_html(filename), columns=price_columns) if filename else pd.DataFrame()"""
            filename = download_file(self.price_url, 'load_form_providers/itlink-price.xml', rs)
            price_columns = ['Article', 'Availability', 'Price', 'Meas', 'Url']
            basa = pd.DataFrame(get_from_html(filename, ff), columns=price_columns) if filename else pd.DataFrame()

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

        list_itlink=[]
        for x in ff:
            s1,s2 = com_l(res.iloc,x)
            if s1:
                list_itlink.append(s2)
            else:
                list_itlink.append(pd.DataFrame())
        return list_itlink

    def send_res(self, w=0):
        try:
            with open("dict_file.json", "r") as read_file:
                data = json.load(read_file)
        except Exception as e:
            print(e)
            data = {}

        dict_serj = {'itlink': ("H2:H2000", "I5:I1500", 7, 8)}

        dict_it = {}

        res = self.get_basa()
        print('ok... It-link loaded')

        for x in range(0 ,len(res)):
            if res.loc[x].Availability == 'Уточняйте':
                dict_it[artile_test(res.loc[x].Article)]=(price_test(res.loc[x].Price), 1)
            else:
                dict_it[artile_test(res.loc[x].Article)]=(price_test(res.loc[x].Price), 0)
            #dict_it[artile_test(res.loc[x].Article)] = price_test(res.loc[x].Price)

        try:
            list_get_list = get_list_sheet("Price", "B5:B1000")
        except:
            print('not received get_list_sheet')
            list_get_list = []

        dict_for_paint = send_all(data, dict_it, list_get_list, dict_serj['itlink'], wait=w)
        print('ok... It-link sended')
        return dict_for_paint
