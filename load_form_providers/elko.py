from load_form_providers.get_service import download_file,get_from_json_elko,price_test,send_list,Service
#from bs4 import BeautifulSoup
import requests,re
import pandas as pd
import json
from lxml import etree
from xml.etree.ElementTree import ParseError
import time

class ELKO:
    ELKO_USERNAME = 'innaviktor'
    ELKO_PASSWORD = 'l&LqO*6l/['
    token = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2NsYWltcy9uYW1lIjoiNjAyMTA1NkAxIiwiaHR0cDovL3NjaGVtYXMubWljcm9zb2Z0LmNvbS93cy8yMDA4LzA2L2lkZW50aXR5L2NsYWltcy9yb2xlIjoiQXBpIiwiZXhwIjoxNjIxMzMwMzcxLCJpc3MiOiJodHRwczovL2tpZXYuZWxrb2dyb3VwLmNvbSIsImF1ZCI6Imh0dHBzOi8va2lldi5lbGtvZ3JvdXAuY29tIn0._RJPKiLH1cnrZHTiaTWQgTorTEBuXyxXTDds59YHsR0'

    token2 = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2NsYWltcy9uYW1lIjoiNjAxMzU1M0AxIiwiaHR0cDovL3NjaGVtYXMubWljcm9zb2Z0LmNvbS93cy8yMDA4LzA2L2lkZW50aXR5L2NsYWltcy9yb2xlIjoiQXBpIiwiZXhwIjoxNjM5MTUwNDA2LCJpc3MiOiJodHRwczovL2tpZXYuZWxrb2dyb3VwLmNvbSIsImF1ZCI6Imh0dHBzOi8va2lldi5lbGtvZ3JvdXAuY29tIn0.2Vv50AMZXYMUX9mcJOzWV7cj1I50LkTtlsJqrF1HN8I'

    def __init__(self, usd_ua):
        self.usd_ua = usd_ua

    def get_price(self):
        with open("load_form_providers/list_articles.json", "r") as write_file:
            list_get_list2=json.load(write_file)
        return list_get_list2

    def get_basa(self, fun2=0):
        ff = self.get_price() if fun2 else 0
        price_columns = [
            'manufacturerCode',
            'name_itm',
            'price',
            'quantity',
            'httpDescription',
            'id'
        ]

        r = requests.get('https://uaapi.elkogroup.com/v3.0/Catalogs/Products', params={
            'CategoryCode': '',
            'VendorCode': '',
            'ELKOcode': ''},
        headers={'Authorization': self.token,"Content-Type": "application/json"}
        )

        r2 = requests.get('https://uaapi.elkogroup.com/v3.0/Catalogs/Products', params={
            'CategoryCode': '',
            'VendorCode': '',
            'ELKOcode': ''},
        headers={'Authorization': self.token2,"Content-Type": "application/json"}
        )

        if r.status_code == 200:
            elko = r.json()
            with open('load_form_providers/elko-price.json', 'w') as write_file:
                json.dump(elko,write_file)
        else:
            print('error file')

        if r2.status_code == 200:
            elko2 = r2.json()
            with open('load_form_providers/elko-price2.json', 'w') as write_file:
                json.dump(elko2,write_file)
        else:
            print('error file2')

        basa = pd.DataFrame(get_from_json_elko('load_form_providers/elko-price.json', ff), columns=price_columns)

        return basa

    def get_sort_basa(self):
        res=self.get_basa(fun2=1)
        ff = self.get_price()

        def com_l(d,element):
            if element:
                for x in d:
                        if x.manufacturerCode==element:
                            return True, x
                return False, pd.DataFrame()
            else:
                return False, pd.DataFrame()

        list_elko=[]
        for x in ff:
            s1,s2 = com_l(res.iloc,x)
            if s1:
                s2.price = round(float(price_test(s2.price))/self.usd_ua, 1)
                list_elko.append(s2)
            else:
                list_elko.append(pd.DataFrame())
        return list_elko

    def sen_res2(self):
        service, CREDENTIALS_FILE, spreadsheetId = Service()

        def send_list(l,list_dict,l2):
            results = service.spreadsheets().values().batchUpdate(spreadsheetId = spreadsheetId, body = {
    "valueInputOption": "USER_ENTERED",
    "data": [
        {"range": f"{l}!{l2}",
         "majorDimension": "ROWS",     # Сначала заполнять строки, затем столбцы
         "values":list_dict}
             ]}).execute()

        list_cpu,list_imb,list_amb,list_hdd,list_ssd,list_video,list_wifi=[],[['imb','','','']],[['amb','','','']],[['hdd','','','']],[['ssd','','','']],[['video','','','']],[['wifi','','','']]
        dict_ = {'CPU':list_cpu,'MBI':list_imb,'MBA':list_amb,
                'HDS':list_hdd,'SSU':list_ssd,'SSP':list_ssd,
                'SSM':list_ssd,'VGP':list_video,'WRA':list_wifi}
        list_empty=[['','','','']]
        l_full_empty=list_empty*220
        #send_list('Elko2', l_full_empty, 'A2:D221')
        with open("load_form_providers/elko-price2.json", "r") as write_file:
            elko2=json.load(write_file)
        for k,v in dict_.items():
            for x in elko2:
                if x['catalog']==k:
                    v.append([x['name'],x['manufacturerCode'],x['quantity'],x['price']])
        try:
            send_list('Elko2',l_full_empty,'A2:D230')
            time.sleep(10)
            send_list('Elko2',list_cpu,'A2:D30')
            time.sleep(5)
            send_list('Elko2',list_imb,'A31:D62')
            time.sleep(5)
            send_list('Elko2',list_amb,'A63:D94')
            time.sleep(5)
            send_list('Elko2',list_hdd,'A95:D126')
            time.sleep(5)
            send_list('Elko2',list_ssd,'A127:D158')
            time.sleep(5)
            send_list('Elko2',list_video,'A159:D190')
            time.sleep(5)
            send_list('Elko2',list_wifi,'A191:D222')
            time.sleep(5)
        except:
            print('elko2 sended error')
        print('elko2 sended ok')

    def send_res(self, w=0):
        try:
            with open("dict_file.json", "r") as read_file:
                data = json.load(read_file)
        except Exception as e:
            print(e)
            data = {}

        dict_serj = {'elko': ("K2:K2000", "L5:L1500", 10, 11)}
        dict_it = {}

        res = self.get_basa()
        print('ok... Elko loaded')

        for x in res.iloc:
            if self.usd_ua:
                if x.quantity == '0' or not x.quantity:
                    dict_it[artile_test(x.manufacturerCode)] = (round(float(price_test(x.price))/self.usd_ua, 1), 1)
                else:
                    dict_it[artile_test(x.manufacturerCode)] = (round(float(price_test(x.price))/self.usd_ua, 1), 0)
            else:
                dict_it[artile_test(x.manufacturerCode)] = price_test(x.price)

        try:
            list_get_list = get_list_sheet("Price", "B5:B1000")
        except:
            print('not received get_list_sheet')
            list_get_list = []

        dict_for_paint = send_all(data, dict_it, list_get_list, dict_serj['elko'], wait=w)
        print('ok... Elko sended')
        return dict_for_paint

if __name__ == '__main__':

    a=ELKO()
    res=a.get_products_df()
    print('ok... Elko loaded')

    with open("dict_file.json", "r") as read_file:
        data = json.load(read_file)


    dict_serj = {'elko': ("K2:K2000", "L5:L1500")}

    dict_it = {}

    for x in res.iloc:
        dict_it[x.manufacturerCode] = x.price

    list_get_list = get_list_sheet("Price", "B5:B1000")

    send_all(dict_serj['elko'], data, dict_it, list_get_list)
    print('ok... Elko sended')
