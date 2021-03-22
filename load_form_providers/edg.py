from load_form_providers.get_service import download_file,get_from_xml_edg
#from bs4 import BeautifulSoup
import requests,re
import pandas as pd
import json
from lxml import etree
from xml.etree.ElementTree import ParseError

class EDG:
    EDG_TOKEN = '0e8a27f168b41bbfedff6d77e7db65f0'
    price_url = f'http://b2b.dako.ua/price_server.php?token={EDG_TOKEN}'

    def get_price(self):
        with open("load_form_providers/list_articles.json", "r") as write_file:
            list_get_list2=json.load(write_file)
        return list_get_list2

    def get_basa(self, fun2=0):
        ff = self.get_price() if fun2 else 0
        price_columns = [
            'Code', 'Name', 'Price', 'StockName', 'Images', 'Url'
        ]

        filename = download_file(self.price_url, 'load_form_providers/edg-price.xml')

        basa = pd.DataFrame(get_from_xml_edg(filename, ff), columns=price_columns) if filename else pd.DataFrame()

        return basa

    def get_sort_basa(self):
        res=self.get_basa(fun2=1)
        ff = self.get_price()

        def com_l(d,element):
            if element:
                for x in d:
                        if x.Code==element:
                            return True, x
                return False, pd.DataFrame()
            else:
                return False, pd.DataFrame()

        list_edg=[]
        for x in ff:
            s1,s2 = com_l(res.iloc,x)
            if s1:
                list_edg.append(s2)
            else:
                list_edg.append(pd.DataFrame())
        return list_edg

    def send_res(self, w=0):
        try:
            with open("dict_file.json", "r") as read_file:
                data = json.load(read_file)
        except Exception as e:
            print(e)
            data = {}

        dict_serj = {'edg': ("L2:L2000", "M5:M1500", 11, 12)}
        dict_it = {}

        res = self.get_basa()
        print('ok... EDG loaded')

        for x in res.iloc:
            if x.StockName and x.StockName != 'Нет в наличии' and x.StockName != 'Зарезервировано':
                dict_it[artile_test(x.Code)]=(price_test(x.Price), 0)
            else:
                dict_it[artile_test(x.Code)]=(price_test(x.Price), 1)
            #dict_it[artile_test(x.Code)] = price_test(x.Price)

        try:
            list_get_list = get_list_sheet("Price", "B5:B1000")
        except:
            print('not received get_list_sheet')
            list_get_list = []

        dict_for_paint = send_all(data, dict_it, list_get_list, dict_serj['edg'], wait=w)
        print('ok... EDG sended')
        return dict_for_paint

if __name__ == '__main__':

    a=EDG()
    res=a.get_basa()
    print('ok... EDG loaded')

    with open("dict_file.json", "r") as read_file:
        data = json.load(read_file)


    dict_serj={'edg': ("L2:L2000", "M5:M1500")}

    dict_it={}

    for x in res.iloc:
        dict_it[x.Code]=x.Price

    list_get_list = get_list_sheet("Price", "B5:B1000")

    send_all(dict_serj['edg'], data, dict_it, list_get_list)
    print('ok... EDG sended')
