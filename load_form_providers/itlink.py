from load_form_providers.get_service import download_file,get_from_html
from bs4 import BeautifulSoup
import requests,re
import pandas as pd
import json
from lxml import etree
from xml.etree.ElementTree import ParseError

class ITLINK:
    #ITLINK_LOGIN = 'hotbox'
    #ITLINK_PASSWORD = 'рщеищч321!'

    price_url = 'https://it-link.ua/api/v1.0/Price?id=YTVjNzY4ZjQtZDRiMS0xMWVhLTgwYzQtMDAwYzI5ZTU4ZDUx&cid=N2NkYWU3NzAtZDRiOC0xMWVhLTgwYzQtMDAwYzI5ZTU4ZDUx'

    def get_basa(self, fun2=0):
        """ """
        content_ = None
        try:
            itlink = requests.get(self.price_url)
            if itlink.status_code == 200:
                content_ = itlink.content
                root = etree.fromstring(content_)
        except Exception as e:
            print(e)
            return content_

        price_filename = 'load_form_providers/itlink-price.xml'
        with open(price_filename, "wb") as f:
            f.write(etree.tostring(
            root,
            pretty_print=True,
            encoding="utf-8",
            xml_declaration=True
             ))

        return content_

    def get_sort_basa2(self):
        res=self.get_basa()
        return res

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
