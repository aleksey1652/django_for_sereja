#from get_service import get_list_sheet
import json
import pandas as pd

class Panda_db:
    __panda_set = {}
    __set_on = set()
    __set_no = set()
    def __test(self,obj):
        try:
            if not obj.empty:
                if len(obj) > 5 and isinstance(obj.partnumber_parts,str) and isinstance(obj.name_parts,str) and  obj.providerprice_parts:
                    try:
                        float(obj.providerprice_parts)
                    except:
                        return pd.DataFrame()
                    return obj
                else:
                    return pd.DataFrame()
            else:
                return pd.DataFrame()
        except:
            return pd.DataFrame()

    def __init__(self, obj_pd):
        for k,v in obj_pd.items():
            self.__panda_set[k] = v
        for k,v in self.__panda_set.items():
            if isinstance(v, pd.core.frame.DataFrame) and not v.empty:
                self.__set_on = set.union(self.__set_on,set(v.index))
            else:
                self.__panda_set.pop(k)
    def search(self,article):
        temp_dict = {}
        if isinstance(article,str) and article in self.__set_on:
            temp_dict = {}
            self.__set_no.add(article)
            for k,v in self.__panda_set.items():
                if article in v.index:
                    if  not self.__test(v.loc[article]).empty:
                        temp_dict[k] = v.loc[article]
        return temp_dict
    def for_db(self):
        temp_dict = {}
        for k,v in self.__panda_set.items():
            for i in v.iloc:
                if i.partnumber_parts not in self.__set_no:
                    if k not in temp_dict:
                        temp_dict[k] = [i]
                    else:
                        temp_dict[k].append(i)
        return temp_dict
    def get_panda_set(self):
        return self.__panda_set
    def get_set_on(self):
        return self.__set_on
    def get_set_no(self):
        return self.__set_no

class Panda:
    __panda_set = {}
    __price = []
    def __get_price():
        """list_get_list = get_list_sheet("Price", "B5:B1000")
        list_get_list2=[]
        for x in list_get_list:
            if x:
                list_get_list2.append(x[0])
            else:
                list_get_list2.append('')"""
        with open("load_form_providers/list_articles.json", "r") as write_file:
            list_get_list2=json.load(write_file)

        return list_get_list2
    def __init__(self):
        self.__price = Panda.__get_price()
    def set_panda_set(self, obj_pd):
        for k,v in obj_pd.items():
            self.__panda_set[k] = v
    def get_panda_set(self):
        return self.__panda_set
    def __panda_sort(self, arg):
        list_f=[]
        for x in range(len(arg[0])):
            list_temp=[]
            for y in arg:
                try:
                    list_temp.append(y[x])
                except:
                    list_temp.append('')
            list_f.append(list_temp)
        return(list_f)
    def full_panda_set(self):
        list_values = []
        list_keys = []
        for k in self.__panda_set.keys():
            list_keys.append(k)
            list_values.append(self.__panda_set[k])
        list_zip = self.__panda_sort(list_values)
        basa=pd.DataFrame(list_zip,columns=list_keys, index=self.__price)
        return basa

    def get_element_panda_num(self, num):
        panda_full = self.full_panda_set()
        sh = Sheed_element(panda_full.iloc[int(num)])
        return sh

    def get_element_panda_partnum(self, partnum):
        panda_full = self.full_panda_set()
        sh = Sheed_element(panda_full.loc[partnum])
        return sh

class Sheed_element:
    dc, asbis, elko, mti, itlink, brain, edg, erc = (
            pd.Series(dtype = 'float64'), pd.Series(dtype = 'float64'), pd.Series(dtype = 'float64'),
            pd.Series(dtype = 'float64'),
            pd.Series(dtype = 'float64'), pd.Series(dtype = 'float64'),
            pd.Series(dtype = 'float64'), pd.Series(dtype = 'float64')
                                                    )
    list_index = ['Name', 'Partnumber', 'Availability', 'Price', 'Url']
    Dict_partner = {'itlink': ('Meas', 'Article', 'Availability', 'Price', 'Url'),
                    'erc': ('gname', 'code', 'swh', 'sprice', 'url'),
                    'dc': ('Name', 'Article', 'Availability', 'PriceUSD', 'Url'),
                    'asbis': ('DESCRIPTION', 'WIC', 'AVAIL', 'MY_PRICE', 'Url'),
                    'mti': ('prodname', 'partnum', 'store', 'price_uah_order', 'url'),
                    'brain': ('Name', 'Article', 'Available', 'PriceUSD', 'URL'),
                    'elko': ('name_itm','manufacturerCode','quantity','price','httpDescription'),
                    'edg': ('Name', 'Code', 'StockName', 'Price', 'Url'),
                    #'itm': ('item_name', 'item_id', '', '', '')
                    }
    def __ff(self, p):
        return list(p.index)

    def __init__(self, p):
        if isinstance(p, pd.core.series.Series):
            temp_list = self.__ff(p)
            for x in temp_list:
                if p[x].empty==False:
                    temp_par = []
                    for y in self.Dict_partner[x]:
                        temp_par.append(p[x][y]) if y!='' else temp_par.append('')
                    self.__dict__[x] = pd.Series(temp_par,index=self.list_index)
                else:
                    self.__dict__[x] = pd.Series(dtype = 'float64')
        else:
            print('Bad data')
            self.dc, self.asbis, self.elko, self.mti, self.itlink, self.brain, self.edg, self.erc = (
                    pd.Series(dtype = 'float64'), pd.Series(dtype = 'float64'),
                    pd.Series(dtype = 'float64'), pd.Series(dtype = 'float64'),
                    pd.Series(dtype = 'float64'), pd.Series(dtype = 'float64'),
                    pd.Series(dtype = 'float64'), pd.Series(dtype = 'float64')
                    )

    def __getitem__(self, key):
        return self.__dict__[key]
"""
    def __init__(self, p):
        if isinstance(p, pd.core.series.Series):
            self.itlink = pd.Series([p.itlink.Meas,p.itlink.Article,p.itlink.Availability,p.itlink.Price,p.itlink.Url],
                          index=self.list_index) if p.itlink.empty==False else pd.Series()
            self.erc = pd.Series([p.erc.gname,p.erc.code,p.erc.swh,p.erc.sprice,''],
                          index=self.list_index) if p.erc.empty==False else pd.Series()
            self.dc = pd.Series([p.dc.Name,p.dc.Article,p.dc.Availability,p.dc.PriceUSD,''],
                          index=self.list_index) if p.dc.empty==False else pd.Series()
            self.asbis = pd.Series([p.asbis.DESCRIPTION,p.asbis.WIC,p.asbis.AVAIL,
                          p.asbis.MY_PRICE,p.asbis.SMALL_IMAGE],
                          index=self.list_index) if p.asbis.empty==False else pd.Series()
            self.mti = pd.Series([p.mti.prodname,p.mti.partnum,p.mti.store,
                          p.mti.price_uah_order,''],
                          index=self.list_index) if p.mti.empty==False else pd.Series()
            self.brain = pd.Series([p.brain.Name,p.brain.Article,p.brain.Available,
                          p.brain.PriceUSD,p.brain.URL],
                          index=self.list_index) if p.brain.empty==False else pd.Series()
            self.elko = pd.Series([p.elko.productName,p.elko.manufacturerCode,p.elko.stockQuantity,
                          p.elko.price,p.elko.httpDescription],
                          index=self.list_index) if p.elko.empty==False else pd.Series()
            self.edg = pd.Series([p.edg.Name,p.edg.Code,p.edg.StockName,
                          p.edg.Price,''],
                          index=self.list_index) if p.edg.empty==False else pd.Series()
        else:
            print('Bad data')
            self.dc, self.asbis, self.elko, self.mti, self.itlink, self.brain, self.edg, self.erc = (
                    pd.Series(), pd.Series(), pd.Series(), pd.Series(),
                    pd.Series(), pd.Series(), pd.Series(), pd.Series()
                    )"""
