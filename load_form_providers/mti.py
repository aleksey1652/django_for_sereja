from load_form_providers.get_service import download_file,get_from_xml_mti,price_test
#from bs4 import BeautifulSoup
import requests,re
import pandas as pd
import json
from lxml import etree
from xml.etree.ElementTree import ParseError
import base64
import datetime
import hashlib



class MTI:
    MTI_COMPANY_ID = '215063'
    MTI_COMPANY_KEY = 'E3CC9F47-523F-2131-02B1-B675F27216FE'

    def __init__(self, usd_ua):
        self.usd_ua = usd_ua

    def __code(self, command, time):
        s = ''.join([time, command, self.MTI_COMPANY_ID, self.MTI_COMPANY_KEY])
        b = base64.b64encode(
            hashlib.sha1(s.encode('utf-8')).digest()
        )
        return str(b, 'utf-8')

    def __data(self, store, ff):

        command = 'PRICE'
        params = f'<store_id>{store}</store_id>'
        time = ''
        signature = self.__code(time, command)

        xmlreq = f'''<?xml version="1.0" encoding="UTF-8"?>
            <request>
                <type>{command}</type>
                <time>{time}</time>
                <company>{self.MTI_COMPANY_ID}</company>
                <signature>{signature}</signature>
                <params>{params}</params>
            </request>'''

        r = requests.post('https://api.mti.ua/', data=xmlreq, headers={
            'Content-Type': 'text/xml'
        })

        price_columns = [
            'prodname', 'partnum', 'price_uah_order',
             'store', 'productgroup_id', 'mticode', 'url'
                        ]

        price_filename = f'load_form_providers/mti-price-{store}.xml'

        try:
            with open(price_filename, 'w') as f:
                f.write(r.text)
        except Exception as e:
            print(e)
            with open(price_filename, 'w') as f:
                f.write('')

        return pd.DataFrame(get_from_xml_mti(price_filename, ff), columns=price_columns)

    def get_price(self):
        with open("load_form_providers/list_articles.json", "r") as write_file:
            list_get_list2=json.load(write_file)
        return list_get_list2

    def get_basa(self, fun2=0):
        ff = self.get_price() if fun2 else 0
        store_dfs = []

        for store in ['W600']:
            store_dfs.append(self.__data(store, ff))

        basa = pd.concat(store_dfs)

        return basa

    def get_sort_basa(self):
        res=self.get_basa(fun2=1)
        ff = self.get_price()

        def com_l(d,element):
            if element:
                for x in d:
                        if x.partnum==element:
                            return True, x
                return False, pd.DataFrame()
            else:
                return False, pd.DataFrame()

        list_mti=[]
        for x in ff:
            s1,s2 = com_l(res.iloc,x)
            if s1:
                s2.price_uah_order = round(float(price_test(s2.price_uah_order))/self.usd_ua, 1)
                list_mti.append(s2)
            else:
                list_mti.append(pd.DataFrame())
        return list_mti

    def send_res(self, w=0):
        try:
            with open("dict_file.json", "r") as read_file:
                data = json.load(read_file)
        except Exception as e:
            print(e)
            data = {}

        dict_serj = {'mti': ("J2:J2000", "K5:K1500", 9, 10)}
        dict_it = {}

        res = self.get_basa()
        print('ok... MTI loaded')

        for x in res.iloc:
            if self.usd_ua:
                if x.store in ('-', '0', '1') or not x.store:
                    dict_it[artile_test(x.partnum)] = (round(float(price_test(x.price_uah_order))/self.usd_ua, 1), 1)
                else:
                    dict_it[artile_test(x.partnum)] = (round(float(price_test(x.price_uah_order))/self.usd_ua, 1), 0)
                #dict_it[artile_test(x.partnum)] = round(float(price_test(x.price_uah_order))/self.usd_ua, 1)
            else:
                dict_it[artile_test(x.partnum)] = price_test(x.price_uah_order)


        try:
            list_get_list = get_list_sheet("Price", "B5:B1000")
        except:
            print('not received get_list_sheet')
            list_get_list = []

        dict_for_paint = send_all(data, dict_it, list_get_list,dict_serj['mti'], wait=w)
        print('ok... MTI sended')
        return dict_for_paint

if __name__ == '__main__':

    a=MTI()
    res=a.get_products_df()
    print('ok... Mti loaded')

    with open("dict_file.json", "r") as read_file:
        data = json.load(read_file)


    dict_serj = {'mti': ("J2:J2000", "K5:K1500")}

    dict_it = {}

    for x in res.iloc:
        dict_it[x.partnum]=x.price_uah

    list_get_list = get_list_sheet("Price", "B5:B1000")

    send_all(dict_serj['mti'], data, dict_it, list_get_list)
    print('ok... MTI sended')
