from load_form_providers.get_service import download_file,get_from_xml_erc,price_test
#from bs4 import BeautifulSoup
import requests,re
import pandas as pd
import json
from lxml import etree
from xml.etree.ElementTree import ParseError

ERC_LOGIN = "innessa777@gmail.com"
ERC_PASSWORD = "25039"
def download_file(url,file_name, s=requests):
    r = s.get(url)
    with open(file_name, 'wb') as f:
        f.write(r.text)

    return file_name

class ERC:

    def __init__(self, usd_ua):
        self.usd_ua = usd_ua

    ERC_LOGIN = 'innessa777@gmail.com'
    ERC_PASSWORD = '25039'
    df = pd.DataFrame()
    price_filename = 'load_form_providers/erc-price.xml'

    def get_price(self):
        with open("load_form_providers/list_articles.json", "r") as write_file:
            list_get_list2=json.load(write_file)
        return list_get_list2

    def get_basa(self, fun2=0):
        ff = self.get_price() if fun2 else 0
        price_columns = ['gname', 'code', 'rprice', 'sprice', 'swh', 'url']

        r  = requests.post('https://connect.erc.ua/connectservice/api/specprice/DoExport', data=json.dumps({
            'Email': self.ERC_LOGIN,
            'Pass': self.ERC_PASSWORD,
            "IsNew": 1,
            'Infotype': 6
            }),
            headers={'Content-Type': 'application/json'}
            )

        #with open(self.price_filename, 'w') as f:
        #    f.write(r.text)

        basa = pd.DataFrame(get_from_xml_erc('load_form_providers/erc-price.xml', ff), columns=price_columns)

        return basa

    def get_sort_basa(self):
        res=self.get_basa(fun2=1)
        ff = self.get_price()

        def com_l(d,element):
            if element:
                for x in d:
                        if x.code==element:
                            return True, x
                return False, pd.DataFrame()
            else:
                return False, pd.DataFrame()

        list_erc=[]
        for x in ff:
            s1,s2 = com_l(res.iloc,x)
            if s1:
                if  (float(price_test(s2.sprice)))>0 and (float(price_test(s2.rprice)))/(float(price_test(s2.sprice)))<3:
                    s2.sprice = round(float(price_test(s2.sprice))/self.usd_ua, 1)
                list_erc.append(s2)
            else:
                list_erc.append(pd.DataFrame())
        return list_erc

    def get_sort_basa2(self):
        return [pd.DataFrame()]

    def send_res(self, w=0):
        try:
            with open("dict_file.json", "r") as read_file:
                data = json.load(read_file)
        except Exception as e:
            print(e)
            data = {}

        dict_serj = {'erc': ("I2:I2000", "J5:J1500", 8, 9)}
        dict_it={}

        res = self.get_basa()
        print('ok... ERC loaded')

        for x in res.iloc:
            if self.usd_ua:
                if  (float(price_test(x.sprice)))>0 and (float(price_test(x.rprice)))/(float(price_test(x.sprice)))<3:
                    if x.swh and x.swh != 'Нет':
                        dict_it[artile_test(x.code)] = (round(float(price_test(x.sprice))/self.usd_ua, 1), 0)
                    else:
                        dict_it[artile_test(x.code)] = (round(float(price_test(x.sprice))/self.usd_ua, 1), 1)
                    #dict_it[artile_test(x.code)] = round(float(price_test(x.sprice))/self.usd_ua, 1)
                else:
                    if x.swh and x.swh != 'Нет':
                        dict_it[artile_test(x.code)] = (round(float(price_test(x.sprice)), 1), 0)
                    else:
                        dict_it[artile_test(x.code)] = (round(float(price_test(x.sprice)), 1), 1)
                    #dict_it[artile_test(x.code)] = round(float(price_test(x.sprice)), 1)
            else:
                dict_it[artile_test(x.code)] = price_test(x.sprice)

        try:
            list_get_list = get_list_sheet("Price", "B5:B1000")
        except:
            print('not received get_list_sheet')
            list_get_list = []

        dict_for_paint = send_all(data, dict_it, list_get_list, dict_serj['erc'], wait=w)
        print('ok... ERC sended')
        return dict_for_paint

if __name__ == '__main__':

    a=ERC()
    res=a.get_basa()
    print('ok... Erc loaded')

    with open("dict_file.json", "r") as read_file:
        data = json.load(read_file)


    dict_serj={'erc': ("I2:I2000", "J5:J1500")}

    dict_it={}

    for x in res.iloc:
        dict_it[x.code]=x.sprice

    list_get_list = get_list_sheet("Price", "B5:B1000")

    send_all(dict_serj['erc'], data, dict_it, list_get_list)
    print('ok... Erc sended')
