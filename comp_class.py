#from run_data_sort import *
from scrapy import *
from get_service import Service, get_list_sheet
from sheet_class import *

def pack_data():
    service, CREDENTIALS_FILE, spreadsheetId = Service()
    g = get_list_sheet("Price", "A5:D1000")
    dict_code={}
    for x in g[:116]:
        if x and len(x)>1 and x[0] and x[1]:
            dict_code[x[1]]=[x[0],get_cpu(x[0])]
    for x in g[119:232]:
        if x and len(x)>1 and x[0] and x[1]:
            dict_code[x[1]]=[x[0],get_mb(x[0])]
    for x in g[234:262]:
        if x and len(x)>1 and x[0] and x[1]:
            temp=get_cool(x[0])
            dict_code[x[1]]=(x[0],get_ps(temp,plan=1))
    for x in g[264:440]:
        if x and len(x)>1 and x[0] and x[1]:
            dict_code[x[1]]=[x[0],get_video(x[0])]
    for x in g[445:520]:
        if x and len(x)>1 and x[0] and x[1]:
            dict_code[x[1]]=[x[0],get_mem(x[0])]
    for x in g[525:610]:
        if x and len(x)>1 and x[0] and x[1]:
            dict_code[x[1]]=[x[0],get_hdd_ssd(x[0])]
    for x in g[615:665]:
        if x and len(x)>1 and x[0] and x[1]:
            dict_code[x[1]]=[x[0],get_ps(x[0])]
    for x in g[666:787]:
        if x and len(x)>1 and x[0] and x[1]:
            dict_code[x[1]]=[x[0],get_case(x[0])]
    t = pd.DataFrame([],columns=['item_name','item_price'])
    for x in g:
        if x and len(x)==4:
            t.loc[x[1]]=[x[0],x[3]]
    return t,dict_code

def get_cpu_art(c):
        a=[]
        ge = c.lower().find('ge')
        if re.findall(r'^\d(.+)',c):
            c=re.findall(r'^\d(.+)',c)[0]
        aa=re.sub(r'\D',' ',c).strip().split(' ')
        aa=[i for i in aa if i] if aa else None
        aa=aa[1:3]
        for x in aa:
            try:
                a.append(int(x))
            except:
                a.append(x)
                print(c)
        a2=re.findall(r'{}(\D+)'.format(a[-1]),c)
        if a2:
                if len(a2[0])>1  and a2[0][0]!=' ':
                    a.append(a2[0][:2].strip().lower())
                elif len(a2[0])==1 and a2[0][0]!=' ':
                    a.append(a2[0].lower())
        if a and a[-1]!='ge' and ge!=-1:
            a.append('ge')
        return a
def pd_proc_art(pr,n=0):
    #n=0 for versum n=2 for itblok
    list_index = ['Name', 'Partnumbers', 'X_code', 'Advanced']
    temp_dict = {}
    if n==0:
        temp_dict['Name'] = pr
        temp_dict['Partnumbers'] = []
        temp_dict['Advanced'] = []
        temp_dict['X_code'] = get_cpu_art(pr)
    else:
        temp_dict['Name'] = pr[n]
        temp_dict['Partnumbers'] = []
        temp_dict['Advanced'] = []
        temp_dict['X_code'] = get_cpu_art(pr[n])
    temp_par=[]
    for x in list_index:
        temp_par.append(temp_dict[x])
    return pd.Series(temp_par,index=list_index)


class IT_LOTS:
    __sheet = pd.DataFrame()
    __loaded_element_price = pd.DataFrame()
    __panda_set = {}
    __dict_code = {}
    __param_dict = {}
    __cil=[
           'name','comp_url','price','proc','mb','mem','video',
           'hdd','ps','case','cool','class','warranty'
           ]
    __basa = pd.DataFrame(columns=__cil)

    def __init__(self, dict_code):
        self.__dict_code = dict_code

    def set_element_price(self, pd_element):
        self.__loaded_element_price = pd_element

    def set_panda_set(self, obj_pd):
        self.__panda_set = {}
        for k,v in obj_pd.items():
            self.__panda_set[k] = v

    def set_sheet(self, obj):
        self.__sheet = obj

    def __hdd_enumerate(self, h):
        temp=[]
        for y,x in enumerate(h):
            if x.lower().find('hdd')!=-1:
                temp.append('3,5 '+h[y+1])
            elif x.lower().find('ssd')!=-1:
                temp.append('ssd '+h[y+1])
        return temp

    def __get_param(self, it_dict):
        if len(it_dict.keys()) == 13:
            it_dict['proc'] = it_dict['proc'][2]
            it_dict['mb'] = it_dict['mb'][2]
            it_dict['mem'] = it_dict['mem'][2]+it_dict['mem'][-1]
            it_dict['video']=it_dict['video'][4]
            it_dict['ps']=it_dict['ps'][2]
            it_dict['case']=it_dict['case'][2]
            it_dict['cool']=it_dict['cool'][2]
            it_dict['class']=it_dict['class'][-1]
            it_dict['warranty']=it_dict['warranty'][-1]
            it_dict['hdd']=self.__hdd_enumerate(it_dict['hdd'])
            self.__param_dict['cool']=pd_cool(it_dict['cool'])
            self.__param_dict['mem']=pd_mem(it_dict['mem'])
            self.__param_dict['proc']=pd_proc(it_dict['proc'])
            self.__param_dict['mb']=pd_mb(it_dict['mb'])
            self.__param_dict['video']=pd_video(it_dict['video'])
            self.__param_dict['ps']=pd_ps(it_dict['ps'])
            self.__param_dict['case']=pd_case(it_dict['case'])
            temp = []
            for x in it_dict['hdd']:
                temp.append(pd_hdd_ssd(x))
            self.__param_dict['hdd']=temp
            for k in it_dict.keys():
                if k in ('proc', 'cool'):
                    for x,y in self.__dict_code.items():
                        if len(y)>1 and self.__param_dict[k].X_code and self.__param_dict[k].X_code==y[1]:
                            self.__param_dict[k].Partnumbers.append(x)
                elif k in ('mem', 'mb', 'video', 'ps'):
                    for x,y in self.__dict_code.items():
                        if len(y)>1 and self.__param_dict[k].X_code and self.__param_dict[k].X_code[:-1]==y[1][:-1]:
                            self.__param_dict[k].Partnumbers.append(x)
                elif k == 'case':
                    for x,y in self.__dict_code.items():
                        if len(y)>1 and [self.__param_dict[k].X_code]==y[1]:
                            self.__param_dict[k].Partnumbers.append(x)
                elif k == 'hdd':
                    for i in self.__param_dict[k]:
                        for x,y in self.__dict_code.items():
                            if len(y)>1 and i.X_code and i.X_code[:-1]==y[1][:-1]:
                                i.Partnumbers.append(x)
                elif k in ('comp_url', 'name', 'class', 'warranty', 'price'):
                    self.__param_dict[k] = it_dict[k]
        else:
            self.__param_dict = {
                                 'comp_url': '', 'name': '', 'price': '', 'proc': '',
                                  'mb': '', 'mem': '', 'video': '', 'hdd':'', 'ps': '',
                                  'case': '', 'class': '', 'cool': '', 'warranty': ''
                                  }

    def __get_basa(self,ind):
        self.__basa.loc[ind]=self.__param_dict

    def it_basa(self):
        for x in self.__panda_set.keys():
            self.__get_param(self.__panda_set[x])
            self.__get_basa(x)
        return self.__basa

    def get_list_sheet_element(self, num):
        dict_obj = {}
        if self.__sheet.empty == False:
            for x in ('dc', 'asbis', 'elko', 'mti', 'itlink', 'brain', 'edg', 'erc'):
                try:
                    temp = Sheed_element(self.__sheet.loc[num])
                except:
                    #print(f'Element {num} not finding in pd')
                    #dict_obj['error'] = 'not finding in pd'
                    dict_obj['error'] = 'not finding in pd'
                    temp = None
                if temp:
                    dict_obj[x] = temp.__dict__[x] if temp.__dict__[x].empty == False else None
                else:
                    return dict_obj
        if self.__loaded_element_price.empty == False:
            try:
                dict_obj['item_part'] = self.__loaded_element_price.loc[num].item_price
            except:
                #print(f'Element {num} not finding in price')
                #dict_obj['error'] = 'not finding in price'
                dict_obj['item_part'] = ''
        return dict_obj

class VERSUM_LOTS(IT_LOTS):
    _IT_LOTS__cil=[
           'name','comp_url','price','proc','mb','mem','video',
           'hdd','ps','case','cool','class','warranty'
           ]
    _IT_LOTS__sheet = pd.DataFrame()
    _IT_LOTS__basa = pd.DataFrame(columns=_IT_LOTS__cil)
    replacements = {
                    'Процесор:': 'proc', 'Кулер:': 'cool',
                    'Материнська плата:': 'mb', 'Оперативна пам’ять:':'mem',
                    'Відеокарта:':'video','Блок живлення:':'ps','Корпус:':'case'
                    }
    """def __transform(self,versum_dict):
        for x in versum_dict:
            versum_dict[x]['hdd']=[]
            for i in ('Накопичувач SSD:','Накопичувач HDD:'):
                try:
                    versum_dict[x]['hdd'].append(versum_dict[x].pop(i))
                except:
                    continue
            for i in versum_dict[x]:
                if i in self.replacements:
                    versum_dict[x][self.replacements[i]] = versum_dict[x].pop(i)
        return versum_dict"""

    def __transform(self,versum_dict):
        temp_dict = {}
        for x in versum_dict:
            temp_dict[x] = {}
            temp_dict[x]['hdd']=[]
            for i in ('Накопичувач SSD:','Накопичувач HDD:'):
                try:
                    temp_dict[x]['hdd'].append(versum_dict[x][i])
                except:
                    continue
            for ii in versum_dict[x]:
                if ii in self.replacements:
                    temp_dict[x][self.replacements[ii]] = versum_dict[x][ii]
            if 'comp_url' in versum_dict[x]:
                temp_dict[x]['comp_url'] = versum_dict[x]['comp_url']
            if 'name' in versum_dict[x]:
                temp_dict[x]['name'] = versum_dict[x]['name']
            if 'price' in versum_dict[x]:
                temp_dict[x]['price'] = versum_dict[x]['price']
        return temp_dict

    def set_panda_set(self, obj_pd):
        obj_pd = self.__transform(obj_pd)
        self._IT_LOTS__panda_set = {}
        for k,v in obj_pd.items():
            self._IT_LOTS__panda_set[k] = v

    def _IT_LOTS__get_param(self, it_dict):
        if len(it_dict.keys()) > 10:
            self._IT_LOTS__param_dict['cool']=pd_cool(it_dict['cool'])
            self._IT_LOTS__param_dict['mem']=pd_mem(it_dict['mem'])
            self._IT_LOTS__param_dict['proc']=pd_proc(it_dict['proc'])
            self._IT_LOTS__param_dict['mb']=pd_mb(it_dict['mb'])
            self._IT_LOTS__param_dict['video']=pd_video(it_dict['video'])
            self._IT_LOTS__param_dict['ps']=pd_ps(it_dict['ps'])
            self._IT_LOTS__param_dict['case']=pd_case(it_dict['case'])
            temp = []
            for x in it_dict['hdd']:
                temp.append(pd_hdd_ssd(x))
            self._IT_LOTS__param_dict['hdd']=temp
            for k in it_dict.keys():
                if k in ('proc', 'cool'):
                    for x,y in self._IT_LOTS__dict_code.items():
                        if len(y)>1 and self._IT_LOTS__param_dict[k].X_code==y[1]:
                            self._IT_LOTS__param_dict[k].Partnumbers.append(x)
                elif k in ('mem', 'mb', 'video', 'ps'):
                    for x,y in self._IT_LOTS__dict_code.items():
                        if self._IT_LOTS__param_dict[k].X_code and self._IT_LOTS__param_dict[k].X_code[-1] != '':
                            if len(y)>1 and self._IT_LOTS__param_dict[k].X_code==y[1]:
                                self._IT_LOTS__param_dict[k].Partnumbers.append(x)
                        elif self._IT_LOTS__param_dict[k].X_code and self._IT_LOTS__param_dict[k].X_code[-1] == '':
                            if len(y)>1 and self._IT_LOTS__param_dict[k].X_code[:-1]==y[1][:-1]:
                                self._IT_LOTS__param_dict[k].Partnumbers.append(x)
                elif k == 'case':
                    for x,y in self._IT_LOTS__dict_code.items():
                        if len(y)>1 and y[1]:
                            if self._IT_LOTS__param_dict[k].X_code and self._IT_LOTS__param_dict[k].X_code==y[1][0]:
                                self._IT_LOTS__param_dict[k].Partnumbers.append(x)
                elif k == 'hdd':
                    for i in self._IT_LOTS__param_dict[k]:
                        for x,y in self._IT_LOTS__dict_code.items():
                            if i.X_code and i.X_code[-1] != '':
                                if i.X_code==y[1]:
                                    i.Partnumbers.append(x)
                            elif i.X_code and i.X_code[-1] == '':
                                if len(y)>1 and i.X_code[:-1]==y[1][:-1]:
                                    i.Partnumbers.append(x)
                elif k in ('comp_url', 'name', 'price'):
                    self._IT_LOTS__param_dict[k] = it_dict[k]
                self._IT_LOTS__param_dict['class'] = ''
                self._IT_LOTS__param_dict['warranty'] = ''
        else:
            self._IT_LOTS__param_dict = {
                                 'comp_url': '', 'name': '', 'price': '', 'proc': '',
                                  'mb': '', 'mem': '', 'video': '', 'hdd':'', 'ps': '',
                                  'case': '', 'class': '', 'cool': '', 'warranty': ''
                                  }

class Fury(IT_LOTS):
    _IT_LOTS__cil=[
           'name','comp_url','price','proc','mb','mem','video',
           'hdd','ps','case','cool','class','warranty'
           ]
    _IT_LOTS__sheet = pd.DataFrame()
    _IT_LOTS__basa = pd.DataFrame(columns=_IT_LOTS__cil)
    def _IT_LOTS__get_param(self, it_dict):
        if len(it_dict.keys()) == 13:
            self._IT_LOTS__param_dict['mem']=pd_mem(it_dict['mem'])
            self._IT_LOTS__param_dict['proc']=pd_proc(it_dict['proc'])
            self._IT_LOTS__param_dict['mb']=pd_mb(it_dict['mb'])
            self._IT_LOTS__param_dict['video']=pd_video(it_dict['video'])
            self._IT_LOTS__param_dict['ps']=pd_ps(it_dict['ps'])
            self._IT_LOTS__param_dict['case']=pd_case(it_dict['case'])

            temp = []
            for x in it_dict['hdd']:
                temp.append(pd_hdd_ssd(x))
            self._IT_LOTS__param_dict['hdd']=temp
            for k in it_dict.keys():
                if k in ('comp_url', 'name', 'class', 'price', 'cool', 'warranty'):
                    self._IT_LOTS__param_dict[k] = it_dict[k]
                elif k == 'hdd':
                    for i in self._IT_LOTS__param_dict[k]:
                        for x,y in self._IT_LOTS__dict_code.items():
                            """if i.X_code and i.X_code[-1] != '':
                                if i.X_code==y[1]:
                                    i.Partnumbers.append(x)
                            elif i.X_code and i.X_code[-1] == '':
                                if i.X_code[:-1]==y[1][:-1]:
                                    i.Partnumbers.append(x)"""
                            if i.X_code[:-1] and len(y)>1 and i.X_code[:-1]==y[1][:-1]:
                                i.Partnumbers.append(x)
                elif k == 'case':
                    for x,y in self._IT_LOTS__dict_code.items():
                        if len(y)>1 and y[1]:
                            if self._IT_LOTS__param_dict[k].X_code==y[1][0]:
                                self._IT_LOTS__param_dict[k].Partnumbers.append(x)
                elif k == 'proc':
                    for x,y in self._IT_LOTS__dict_code.items():
                        if len(y)>1 and self._IT_LOTS__param_dict[k].X_code and self._IT_LOTS__param_dict[k].X_code==y[1]:
                            self._IT_LOTS__param_dict[k].Partnumbers.append(x)
                else:
                    for x,y in self._IT_LOTS__dict_code.items():
                        """if self._IT_LOTS__param_dict[k].X_code and self._IT_LOTS__param_dict[k].X_code[-1] != '':
                            if self._IT_LOTS__param_dict[k].X_code==y[1]:
                                self._IT_LOTS__param_dict[k].Partnumbers.append(x)
                        elif self._IT_LOTS__param_dict[k].X_code and self._IT_LOTS__param_dict[k].X_code[-1] == '':
                            if self._IT_LOTS__param_dict[k].X_code[:-1]==y[1][:-1]:
                                self._IT_LOTS__param_dict[k].Partnumbers.append(x)"""
                        if self._IT_LOTS__param_dict[k].X_code[:-1]==y[1][:-1]:
                            self._IT_LOTS__param_dict[k].Partnumbers.append(x)
        else:
            self._IT_LOTS__param_dict = {
                                 'comp_url': '', 'name': '', 'price': '', 'proc': '',
                                  'mb': '', 'mem': '', 'video': '', 'hdd':'', 'ps': '',
                                  'case': '', 'class': '', 'cool': '', 'warranty': ''
                                  }
    def it_basa(self):
        for x in self._IT_LOTS__panda_set.keys():
            self._IT_LOTS__get_param(self._IT_LOTS__panda_set[x])
            self._IT_LOTS__get_basa(x)
        return self._IT_LOTS__basa

class UA(IT_LOTS):
    _IT_LOTS__cil=[
           'name','comp_url','price','proc','mb','mem','video',
           'hdd','ps','case','cool','class','warranty'
           ]
    _IT_LOTS__sheet = pd.DataFrame()
    _IT_LOTS__basa = pd.DataFrame(columns=_IT_LOTS__cil)
    replacements = {
                    'Категория ПК':'class','Процессор':'proc','Видеокарта':'video',
                    'Объем оперативной памяти':'mem','Чипсет материнской платы':'mb',
                    'Охлаждение процессора':'cool','Блок питания':'ps','Гарантия':'warranty'
                    }
    def __hdd_transform(self, d):
        d['hdd']=[]
        if d['Накопитель'].lower().find('ssd')!=-1:
            d['hdd'].append(d.pop('Накопитель'))
            if 'Объем SSD' in d:
                d.pop('Объем SSD')
                return d
        else:
            d['hdd'].append('3,5 '+d.pop('Накопитель'))
            if 'Объем SSD' in d:
                d['hdd'].append('ssd '+d.pop('Объем SSD'))
            return d

    def __transform2(self, ua_dict):
        temp = {}
        for x in ua_dict:
            name=x
            x=self.__hdd_transform(ua_dict[x])
            x['case']=[]
            for c in x:
                if c.find('itm')!=-1:
                    x['case'].append(x[c])
            for i in x:
                if i in self.replacements:
                    x[self.replacements[i]] = x.pop(i)
            x['name']=name
            if 'cool' in x and x['cool'].lower()=='box':
                if x['Семейство процессора'].lower().find('intel')!=-1:
                    x['cool']='intel box'
                elif x['Семейство процессора'].lower().find('amd')!=-1:
                    x['cool']='amd box'
            temp[name]=x
        return temp

    def set_panda_set(self, obj_pd):
        obj_pd = self.__transform2(obj_pd)
        self._IT_LOTS__panda_set = {}
        for k,v in obj_pd.items():
            self._IT_LOTS__panda_set[k] = v

    def _IT_LOTS__get_param(self, it_dict):
        if len(it_dict.keys()) > 13:
            self._IT_LOTS__param_dict['mem']=pd_mem(it_dict['mem'])
            self._IT_LOTS__param_dict['proc']=pd_proc(it_dict['proc'])
            #self._IT_LOTS__param_dict['video']=pd_video(it_dict['video'])
            self._IT_LOTS__param_dict['ps']=pd_ps(it_dict['ps'])
            if 'video' in it_dict:
                self._IT_LOTS__param_dict['video']=pd_video(it_dict['video'])
            else:
                self._IT_LOTS__param_dict['video']=''
            if 'mb' in it_dict:
                self._IT_LOTS__param_dict['mb']=pd_mb(it_dict['mb'])
            else:
                self._IT_LOTS__param_dict['mb']=''
            if 'cool' in it_dict:
                self._IT_LOTS__param_dict['cool']=pd_cool(it_dict['cool'])
            else:
                self._IT_LOTS__param_dict['cool']=''
            temp = []
            for x in it_dict['hdd']:
                temp.append(pd_hdd_ssd(x))
            self._IT_LOTS__param_dict['hdd']=temp

            for k in it_dict.keys():
                if k in ('comp_url', 'name', 'class', 'price', 'warranty', 'case'):
                    self._IT_LOTS__param_dict[k] = it_dict[k]
                elif k == 'hdd':
                    for i in self._IT_LOTS__param_dict[k]:
                        for x,y in self._IT_LOTS__dict_code.items():
                            if i.X_code and len(y) > 1 and i.X_code[:-1]==y[1][:-1]:
                                i.Partnumbers.append(x)
                elif k in ('proc', 'cool'):
                    for x,y in self._IT_LOTS__dict_code.items():
                        if self._IT_LOTS__param_dict[k].X_code and len(y) > 1 and self._IT_LOTS__param_dict[k].X_code==y[1]:
                            self._IT_LOTS__param_dict[k].Partnumbers.append(x)
                elif k in ('video', 'ps'):
                    for x,y in self._IT_LOTS__dict_code.items():
                        if self._IT_LOTS__param_dict[k].X_code and len(y) > 1 and self._IT_LOTS__param_dict[k].X_code[:-1]==y[1][:-1]:
                            self._IT_LOTS__param_dict[k].Partnumbers.append(x)
                elif k in ('mb', 'mem'):
                    for x,y in self._IT_LOTS__dict_code.items():
                        try:
                            if self._IT_LOTS__param_dict[k].X_code and len(y) > 1 and self._IT_LOTS__param_dict[k].X_code[0]==y[1][0]:
                                self._IT_LOTS__param_dict[k].Partnumbers.append(x)
                        except:
                            #print(x,y,self._IT_LOTS__param_dict[k].X_code)
                            pass
        else:
            self._IT_LOTS__param_dict = {
                                 'comp_url': '', 'name': '', 'price': '', 'proc': '',
                                  'mb': '', 'mem': '', 'video': '', 'hdd':'', 'ps': '',
                                  'case': '', 'class': '', 'cool': '', 'warranty': ''
                                  }

class ART(IT_LOTS):
    replacements = {
                    'Модель процессора': 'proc', 'Охлаждение процессора': 'cool',
                    'Модель материнской платы': 'mb', 'Оперативная память':'mem',
                    'Видеокарта':'video','Блок питания':'ps','Корпус':'case',
                    'Гарантия':'warranty'
                    }
    def __transform(self,versum_dict):
        temp_dict = {}
        for x in versum_dict:
            temp_dict[x] = {}
            temp_dict[x]['hdd']=[]
            for i in ('Объем накопителя','Объем второго накопителя'):
                try:
                    temp_dict[x]['hdd'].append(versum_dict[x][i])
                except:
                    continue
            for ii in versum_dict[x]:
                if ii in self.replacements:
                    temp_dict[x][self.replacements[ii]] = versum_dict[x][ii]
            if 'comp_url' in versum_dict[x]:
                temp_dict[x]['comp_url'] = versum_dict[x]['comp_url']
            if 'name' in versum_dict[x]:
                temp_dict[x]['name'] = versum_dict[x]['name']
            if 'price' in versum_dict[x]:
                temp_dict[x]['price'] = versum_dict[x]['price']
        return temp_dict

    def set_panda_set(self, obj_pd):
        obj_pd = self.__transform(obj_pd)
        self._IT_LOTS__panda_set = {}
        for k,v in obj_pd.items():
            self._IT_LOTS__panda_set[k] = v

    def _IT_LOTS__get_param(self, it_dict):
        if len(it_dict.keys()) > 10:
            self._IT_LOTS__param_dict['cool']=pd_cool(it_dict['cool']) if 'cool' in it_dict else ''
            self._IT_LOTS__param_dict['mem']=pd_mem(it_dict['mem']) if 'mem' in it_dict else ''
            self._IT_LOTS__param_dict['proc']=pd_proc_art(it_dict['proc']) if 'proc' in it_dict else ''
            self._IT_LOTS__param_dict['mb']=pd_mb(it_dict['mb']) if 'mb' in it_dict else ''
            self._IT_LOTS__param_dict['video']=pd_video(it_dict['video']) if 'video' in it_dict else ''
            self._IT_LOTS__param_dict['ps']=pd_ps(it_dict['ps']) if 'ps' in it_dict else ''
            self._IT_LOTS__param_dict['case']=pd_case(it_dict['case']) if 'case' in it_dict else ''
            temp = []
            if 'hdd' not in it_dict:
                it_dict['hdd'] = []
            for x in it_dict['hdd']:
                temp.append(pd_hdd_ssd(x))
            self._IT_LOTS__param_dict['hdd']=temp
            for k in it_dict.keys():
                if k in ('proc', 'cool'):
                    for x,y in self._IT_LOTS__dict_code.items():
                        if len(y) > 1 and self._IT_LOTS__param_dict[k].X_code==y[1]:
                            self._IT_LOTS__param_dict[k].Partnumbers.append(x)
                elif k in ('mem', 'mb', 'video', 'ps'):
                    for x,y in self._IT_LOTS__dict_code.items():
                        if self._IT_LOTS__param_dict[k].X_code and len(y) > 1 and self._IT_LOTS__param_dict[k].X_code[:-1]==y[1][:-1]:
                            self._IT_LOTS__param_dict[k].Partnumbers.append(x)
                elif k == 'case':
                    for x,y in self._IT_LOTS__dict_code.items():
                        if len(y)>1 and y[1]:
                            if self._IT_LOTS__param_dict[k].X_code==y[1][0]:
                                self._IT_LOTS__param_dict[k].Partnumbers.append(x)
                elif k == 'hdd':
                    for i in self._IT_LOTS__param_dict[k]:
                        for x,y in self._IT_LOTS__dict_code.items():
                            if i.X_code and len(y) > 1 and i.X_code[:-1]==y[1][:-1]:
                                i.Partnumbers.append(x)
                elif k in ('comp_url', 'name', 'price'):
                    self._IT_LOTS__param_dict[k] = it_dict[k]
                self._IT_LOTS__param_dict['class'] = ''
                self._IT_LOTS__param_dict['warranty'] = it_dict['warranty'] if 'warranty' in it_dict else ''
        else:
            self._IT_LOTS__param_dict = {
                                 'comp_url': '', 'name': '', 'price': '', 'proc': '',
                                  'mb': '', 'mem': '', 'video': '', 'hdd':'', 'ps': '',
                                  'case': '', 'class': '', 'cool': '', 'warranty': ''
                                  }
