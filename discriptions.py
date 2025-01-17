Python 3.6.9 (default, Jan 26 2021, 15:33:00) 
[GCC 8.4.0] on linux
Type "help", "copyright", "credits" or "license()" for more information.
>>> import os,json,pickle,django
>>> os.environ.setdefault('DJANGO_SETTINGS_MODULE','sereja.settings')
'sereja.settings'
>>> from cat.models import *
Traceback (most recent call last):
  File "<pyshell#2>", line 1, in <module>
    from cat.models import *
  File "/home/aleksey1652/sereja/cat/models.py", line 4, in <module>
    class USD(models.Model):
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/models/base.py", line 108, in __new__
    app_config = apps.get_containing_app_config(module)
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/apps/registry.py", line 253, in get_containing_app_config
    self.check_apps_ready()
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/apps/registry.py", line 136, in check_apps_ready
    raise AppRegistryNotReady("Apps aren't loaded yet.")
django.core.exceptions.AppRegistryNotReady: Apps aren't loaded yet.
>>> django.setup()
>>> from cat.models import *
>>> import pandas as pd
>>> itlink = pd.read_excel('load_form_providers/erc.xlsx', usecols=[0,2,3,6,7],header=None)
>>> erc=pd.read_excel('load_form_providers/erc.xlsx', usecols=[2,3,4,8,12],header=None)
>>> erc.iloc[0]
2     Підкатегорія
3     Найменування
4              Код
8            Дилер
12          Кіл-ть
Name: 0, dtype: object
>>> erc_=erc.rename(columns={2:'subcategory', 3:'name_parts',
            4:'partnumber_parts',8:'providerprice_parts',
            12:'availability_parts'})
>>> erc_.iloc[0]
subcategory            Підкатегорія
name_parts             Найменування
partnumber_parts                Код
providerprice_parts           Дилер
availability_parts           Кіл-ть
Name: 0, dtype: object
>>> dict1={'Накопичувачі SSD':'ssd', 'Корпуси для ПК':'case', 'Материнські плати':0,'Накопичувачі HDD для комп`ютерів':'hdd', 'Відеокарти':'video', "Пам'ять DDR для ПК":'mem','Блоки живлення':'ps','Монітори':'mon'}
>>> from load_form_providers.load_element import to_article2_1
>>> to_article2_1('Материнcька плата ASUS TUF_GAMING_B550M-E_WIFI sAM4 B550 4xDDR4 M.2 HDMI-DP Wi-Fi!!!BT mATX',pr=0)
'amb'
>>> dict_erc={}
>>> for x in erc_.iloc:
	if isinstance(x['subcategory'],str) and x['subcategory'] in dict1:
		kind = dict1[x['subcategory']] if dict1[x['subcategory']] != 0 else to_article2_1(x["name_parts"],pr=0)
		dict_erc[x["partnumber_parts"]]=(x["name_parts"],x["providerprice_parts"],x["availability_parts"])

		
>>> dict_erc.keys()

>>> erc_k=list(dict_erc.keys())
>>> erc_k[:10]
['L194WT-BF*', 'L194WT-SF*', 'L1952TR-SF*', 'L1750SQ-SN*', 'L1953S-SF*', 'W1934S-SN*', 'W1942S-PF*', 'W1942T-SF*', 'TS120GMTS420S*', 'SUV500M8/240G*']
>>> dict_erc['L194WT-BF*']
('Монiтор LCD 19" LG L194WT-BF D-Sub, DVI 16:10', 840, '0')
>>> erc_.iloc[10]
subcategory                        Зарядні пристрої та адаптери живлення
name_parts             Тримач автомобільний Remax Wireless charger RM...
partnumber_parts                                           6954851298250
providerprice_parts                                               175.98
availability_parts                                                     1
Name: 10, dtype: object
>>> erc_.iloc[100]
subcategory               Кабелі, розгалужувачі, перехідники комп`ютерні
name_parts             Тримач автомобільний Remax Car Holder RM-C10 b...
partnumber_parts                                           6954851257554
providerprice_parts                                                58.68
availability_parts                                                   <20
Name: 100, dtype: object
>>> erc_.iloc[1000]
subcategory                                       Чохли для планшетів
name_parts             Чохол 2E для Lenovo Tab4 10" Plus, Case, Black
partnumber_parts                                     2E-L-T410P-MCCBB
providerprice_parts                                               390
availability_parts                                               <500
Name: 1000, dtype: object
>>> erc_.iloc[1000]["partnumber_parts"]
'2E-L-T410P-MCCBB'
>>> erc.loc['TS120GMTS420S*']
Traceback (most recent call last):
  File "<pyshell#28>", line 1, in <module>
    erc.loc['TS120GMTS420S*']
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/pandas/core/indexing.py", line 879, in __getitem__
    return self._getitem_axis(maybe_callable, axis=axis)
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/pandas/core/indexing.py", line 1110, in _getitem_axis
    return self._get_label(key, axis=axis)
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/pandas/core/indexing.py", line 1059, in _get_label
    return self.obj.xs(label, axis=axis)
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/pandas/core/generic.py", line 3491, in xs
    loc = self.index.get_loc(key)
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/pandas/core/indexes/range.py", line 358, in get_loc
    raise KeyError(key)
KeyError: 'TS120GMTS420S*'
>>> erc.loc['TS120GMTS420S']
Traceback (most recent call last):
  File "<pyshell#29>", line 1, in <module>
    erc.loc['TS120GMTS420S']
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/pandas/core/indexing.py", line 879, in __getitem__
    return self._getitem_axis(maybe_callable, axis=axis)
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/pandas/core/indexing.py", line 1110, in _getitem_axis
    return self._get_label(key, axis=axis)
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/pandas/core/indexing.py", line 1059, in _get_label
    return self.obj.xs(label, axis=axis)
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/pandas/core/generic.py", line 3491, in xs
    loc = self.index.get_loc(key)
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/pandas/core/indexes/range.py", line 358, in get_loc
    raise KeyError(key)
KeyError: 'TS120GMTS420S'
>>> erc_.loc['TS120GMTS420S*']
Traceback (most recent call last):
  File "<pyshell#30>", line 1, in <module>
    erc_.loc['TS120GMTS420S*']
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/pandas/core/indexing.py", line 879, in __getitem__
    return self._getitem_axis(maybe_callable, axis=axis)
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/pandas/core/indexing.py", line 1110, in _getitem_axis
    return self._get_label(key, axis=axis)
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/pandas/core/indexing.py", line 1059, in _get_label
    return self.obj.xs(label, axis=axis)
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/pandas/core/generic.py", line 3491, in xs
    loc = self.index.get_loc(key)
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/pandas/core/indexes/range.py", line 358, in get_loc
    raise KeyError(key)
KeyError: 'TS120GMTS420S*'
>>> erc_.loc['TS120GMTS420S']
Traceback (most recent call last):
  File "<pyshell#31>", line 1, in <module>
    erc_.loc['TS120GMTS420S']
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/pandas/core/indexing.py", line 879, in __getitem__
    return self._getitem_axis(maybe_callable, axis=axis)
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/pandas/core/indexing.py", line 1110, in _getitem_axis
    return self._get_label(key, axis=axis)
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/pandas/core/indexing.py", line 1059, in _get_label
    return self.obj.xs(label, axis=axis)
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/pandas/core/generic.py", line 3491, in xs
    loc = self.index.get_loc(key)
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/pandas/core/indexes/range.py", line 358, in get_loc
    raise KeyError(key)
KeyError: 'TS120GMTS420S'
>>> for x in erc_.iloc[:10]:
	if isinstance(x['subcategory'],str) and x['subcategory'] in dict1:
		kind = dict1[x['subcategory']] if dict1[x['subcategory']] != 0 else to_article2_1(x["name_parts"],pr=0)
		print(x["partnumber_parts"],end=' ')

		
Traceback (most recent call last):
  File "<pyshell#34>", line 2, in <module>
    if isinstance(x['subcategory'],str) and x['subcategory'] in dict1:
TypeError: string indices must be integers
>>> erc_.iloc[:2]
      subcategory  ... availability_parts
0    Підкатегорія  ...             Кіл-ть
1  Колонки для ПК  ...                  0

[2 rows x 5 columns]
>>> for x in erc_.iloc[:10]:
	print(x["partnumber_parts"],end=' ')

	
Traceback (most recent call last):
  File "<pyshell#38>", line 2, in <module>
    print(x["partnumber_parts"],end=' ')
TypeError: string indices must be integers
>>> erc_.iloc[2]
subcategory                                               Колонки для ПК
name_parts             Колонки MICROLAB 2.1 FC530 Wooden, з зовнішнім...
partnumber_parts                                                 FC-530*
providerprice_parts                                              2120.04
availability_parts                                                     0
Name: 2, dtype: object
>>> dict_erc={}
>>> import re
>>> re.sub('*','','FC-530*')
Traceback (most recent call last):
  File "<pyshell#42>", line 1, in <module>
    re.sub('*','','FC-530*')
  File "/usr/lib/python3.6/re.py", line 191, in sub
    return _compile(pattern, flags).sub(repl, string, count)
  File "/usr/lib/python3.6/re.py", line 301, in _compile
    p = sre_compile.compile(pattern, flags)
  File "/usr/lib/python3.6/sre_compile.py", line 562, in compile
    p = sre_parse.parse(p, flags)
  File "/usr/lib/python3.6/sre_parse.py", line 855, in parse
    p = _parse_sub(source, pattern, flags & SRE_FLAG_VERBOSE, 0)
  File "/usr/lib/python3.6/sre_parse.py", line 416, in _parse_sub
    not nested and not items))
  File "/usr/lib/python3.6/sre_parse.py", line 616, in _parse
    source.tell() - here + len(this))
sre_constants.error: nothing to repeat at position 0
>>> re.sub(r'*','','FC-530*')
Traceback (most recent call last):
  File "<pyshell#43>", line 1, in <module>
    re.sub(r'*','','FC-530*')
  File "/usr/lib/python3.6/re.py", line 191, in sub
    return _compile(pattern, flags).sub(repl, string, count)
  File "/usr/lib/python3.6/re.py", line 301, in _compile
    p = sre_compile.compile(pattern, flags)
  File "/usr/lib/python3.6/sre_compile.py", line 562, in compile
    p = sre_parse.parse(p, flags)
  File "/usr/lib/python3.6/sre_parse.py", line 855, in parse
    p = _parse_sub(source, pattern, flags & SRE_FLAG_VERBOSE, 0)
  File "/usr/lib/python3.6/sre_parse.py", line 416, in _parse_sub
    not nested and not items))
  File "/usr/lib/python3.6/sre_parse.py", line 616, in _parse
    source.tell() - here + len(this))
sre_constants.error: nothing to repeat at position 0
>>> re.sub('\*','','FC-530*')
'FC-530'
>>> re.sub('\*$','','FC-530*')
'FC-530'
>>> re.sub('\*$','','FC-530*o')
'FC-530*o'
>>> re.sub('\*$','','FC-530* ')
'FC-530* '
>>> re.sub('\*$'|' ','','FC-530* ')
Traceback (most recent call last):
  File "<pyshell#48>", line 1, in <module>
    re.sub('\*$'|' ','','FC-530* ')
TypeError: unsupported operand type(s) for |: 'str' and 'str'
>>> re.sub('\*$' or ' ','','FC-530* ')
'FC-530* '
>>> re.sub('\*$' or 'j','','FC-530j*')
'FC-530j'
>>> re.sub('\*$| ','','FC-530* ')
'FC-530*'
>>> re.sub('\*$'|'j','','FC-530j*')
Traceback (most recent call last):
  File "<pyshell#52>", line 1, in <module>
    re.sub('\*$'|'j','','FC-530j*')
TypeError: unsupported operand type(s) for |: 'str' and 'str'
>>> re.sub('\*$|j','','FC-530*')
'FC-530'
>>> re.sub('\*$|j','','FC-530j')
'FC-530'
>>> re.sub('\*$|\ ','','FC-530 ')
'FC-530'
>>> for x in erc_.iloc:
	if isinstance(x['subcategory'],str) and x['subcategory'] in dict1:
		kind = dict1[x['subcategory']] if dict1[x['subcategory']] != 0 else to_article2_1(x["name_parts"],pr=0)
		dict_erc[re.sub('\*$','',x["partnumber_parts"])]=(x["name_parts"],x["providerprice_parts"],x["availability_parts"])

		
>>> erc_k=list(dict_erc.keys())
>>> erc_k[:10]
['L194WT-BF', 'L194WT-SF', 'L1952TR-SF', 'L1750SQ-SN', 'L1953S-SF', 'W1934S-SN', 'W1942S-PF', 'W1942T-SF', 'TS120GMTS420S', 'SUV500M8/240G']
>>> dict_erc['SUV500M8/240G']
('SSD M.2 SATA 2280 240GB Kingston UV500 3D TLC R520Mbps/W500Mbps', 1120.02, '0')
>>> re.findall('\d*','<500')
['', '500', '']
>>> re.findall('[\d*]','<500')
['5', '0', '0']
>>> re.findall('(\d*)','<500')
['', '500', '']
>>> re.search('\d*','<500')
<_sre.SRE_Match object; span=(0, 0), match=''>
>>> rr=re.search('\d*','<500')
>>> rr.group
<built-in method group of _sre.SRE_Match object at 0x7feebbd68c60>
>>> rr.group()
''
>>> re.findall('(\d*)','<')
['', '']
>>> re.findall('\d*','<')
['', '']
>>> (x for x in re.findall('\d*','<500') if x)
<generator object <genexpr> at 0x7feedc357938>
>>> xx=(x for x in re.findall('\d*','<500') if x)
>>> xx
<generator object <genexpr> at 0x7feebc4f5518>
>>> [x for x in re.findall('\d*','<500') if x]
['500']
>>> [x for x in re.findall('\d*','<') if x]
[]
>>> [x for x in re.findall('\d*','0') if x]
['0']
>>> def status_erc(av):
	temp = [x for x in re.findall('\d*',av) if x]
	temp = int(temp[0]) if temp else 0
	if temp <= 20 and temp != 0:
		return 'q'
	elif temp >= 20:
		return 'yes'
	else:
		return 'no'

	
>>> status_erc('>')
'no'
>>> status_erc('0')
'no'
>>> status_erc('<20')
'q'
>>> status_erc('<500')
'yes'
>>> status_erc('<50')
'yes'
>>> dict_erc={}
>>> for x in erc_.iloc:
	if isinstance(x['subcategory'],str) and x['subcategory'] in dict1:
		kind = dict1[x['subcategory']] if dict1[x['subcategory']] != 0 else to_article2_1(x["name_parts"],pr=0)
		dict_erc[x["partnumber_parts"]]=(x["name_parts"],x["providerprice_parts"],status_erc(x["availability_parts"]))

		
>>> dict_erc['SUV500M8/240G']
Traceback (most recent call last):
  File "<pyshell#94>", line 1, in <module>
    dict_erc['SUV500M8/240G']
KeyError: 'SUV500M8/240G'
>>> dict_erc={}
>>> for x in erc_.iloc:
	if isinstance(x['subcategory'],str) and x['subcategory'] in dict1:
		kind = dict1[x['subcategory']] if dict1[x['subcategory']] != 0 else to_article2_1(x["name_parts"],pr=0)
		dict_erc[re.sub('\*$','',x["partnumber_parts"])]=(x["name_parts"],x["providerprice_parts"],status_erc(x["availability_parts"]))

		
>>> dict_erc['SUV500M8/240G']
('SSD M.2 SATA 2280 240GB Kingston UV500 3D TLC R520Mbps/W500Mbps', 1120.02, 'no')
>>> re.sub('\*$|j','',None)
Traceback (most recent call last):
  File "<pyshell#99>", line 1, in <module>
    re.sub('\*$|j','',None)
  File "/usr/lib/python3.6/re.py", line 191, in sub
    return _compile(pattern, flags).sub(repl, string, count)
TypeError: expected string or bytes-like object
>>> re.sub('\*$|j','','')
''
>>> for x in erc_.iloc:
        if isinstance(x['subcategory'],str) and x['subcategory'] in dict1:
            kind = dict1[x['subcategory']] if dict1[x['subcategory']] != 0 else to_article2_1(x["name_parts"],pr=0)
            pa = re.sub('\*$','',x["partnumber_parts"])
            av = status_erc(x["availability_parts"])
            #dict_erc[key]=(x["name_parts"],x["providerprice_parts"],status_erc(x["availability_parts"]))
            if pa:
                set_erc.add(key)
                n,pr = x['name_parts'],x['providerprice_parts']
                prov,_ = Providers.objects.get_or_create(name_provider='erc')
                prov1 = Providers.objects.get(name_provider='-')
                p1 = Parts_full.objects.filter(partnumber_parts=pa,providers=prov)
                try:
                    a1,_ = Articles.objects.get_or_create(article=pa,item_name=n,item_price=kind)
                except:
                    a1 = Articles.objects.get(article=pa)
                if not p1:
                    p_itl = Parts_full.objects.create(name_parts=n,
                    partnumber_parts=pa,providers=prov,
                    providerprice_parts=pr,date_chg=timezone.now(),
                    availability_parts=av,kind=kind)
                    a1.parts_full.add(p_itl)
                    count_no += 1
                elif p1.count() > 0:
                    temp2 = p1.first()
                    temp2.availability_parts = av
                    temp2.providerprice_parts = pr
                    temp2.date_chg = timezone.now()
                    temp2.kind = kind
                    temp2.save()
                    count_on += 1
                    if p1.count() > 1:
                        print(f'count:{p1.count()} ')
                        for x in p1[1:]:
                            x.delete()
                if Parts_full.objects.filter(partnumber_parts=pa,providers=prov1).exists() and av == 'yes':
                    pl = Parts_full.objects.filter(partnumber_parts=pa,providers=prov1)[0]
                    try:
                        if float(pl.providerprice_parts) > float(pr):
                            pl.providerprice_parts = pr
                            pl.save()
                    except:
                        print(f'error in erc element:{pa}')
                else:
                    pr = pr if av == 'yes' else 0
                    p_main = Parts_full.objects.create(name_parts=n,
                    partnumber_parts=pa,providers=prov1,
                    providerprice_parts=pr,date_chg=timezone.now(),
                    availability_parts=av,kind=kind)
                    a1.parts_full.add(p_main)
            else:
                continue

        
Traceback (most recent call last):
  File "<pyshell#102>", line 8, in <module>
    set_erc.add(key)
NameError: name 'set_erc' is not defined
>>> set_erc = set()
>>> count_no, count_on = 0, 0
>>> for x in erc_.iloc:
        if isinstance(x['subcategory'],str) and x['subcategory'] in dict1:
            kind = dict1[x['subcategory']] if dict1[x['subcategory']] != 0 else to_article2_1(x["name_parts"],pr=0)
            pa = re.sub('\*$','',x["partnumber_parts"])
            av = status_erc(x["availability_parts"])
            #dict_erc[key]=(x["name_parts"],x["providerprice_parts"],status_erc(x["availability_parts"]))
            if pa:
                set_erc.add(key)
                n,pr = x['name_parts'],x['providerprice_parts']
                prov,_ = Providers.objects.get_or_create(name_provider='erc')
                prov1 = Providers.objects.get(name_provider='-')
                p1 = Parts_full.objects.filter(partnumber_parts=pa,providers=prov)
                try:
                    a1,_ = Articles.objects.get_or_create(article=pa,item_name=n,item_price=kind)
                except:
                    a1 = Articles.objects.get(article=pa)
                if not p1:
                    p_itl = Parts_full.objects.create(name_parts=n,
                    partnumber_parts=pa,providers=prov,
                    providerprice_parts=pr,date_chg=timezone.now(),
                    availability_parts=av,kind=kind)
                    a1.parts_full.add(p_itl)
                    count_no += 1
                elif p1.count() > 0:
                    temp2 = p1.first()
                    temp2.availability_parts = av
                    temp2.providerprice_parts = pr
                    temp2.date_chg = timezone.now()
                    temp2.kind = kind
                    temp2.save()
                    count_on += 1
                    if p1.count() > 1:
                        print(f'count:{p1.count()} ')
                        for x in p1[1:]:
                            x.delete()
                if Parts_full.objects.filter(partnumber_parts=pa,providers=prov1).exists() and av == 'yes':
                    pl = Parts_full.objects.filter(partnumber_parts=pa,providers=prov1)[0]
                    try:
                        if float(pl.providerprice_parts) > float(pr):
                            pl.providerprice_parts = pr
                            pl.save()
                    except:
                        print(f'error in erc element:{pa}')
                else:
                    pr = pr if av == 'yes' else 0
                    p_main = Parts_full.objects.create(name_parts=n,
                    partnumber_parts=pa,providers=prov1,
                    providerprice_parts=pr,date_chg=timezone.now(),
                    availability_parts=av,kind=kind)
                    a1.parts_full.add(p_main)
            else:
                continue

        
Traceback (most recent call last):
  File "<pyshell#106>", line 8, in <module>
    set_erc.add(key)
NameError: name 'key' is not defined
>>> for x in erc_.iloc:
        if isinstance(x['subcategory'],str) and x['subcategory'] in dict1:
            kind = dict1[x['subcategory']] if dict1[x['subcategory']] != 0 else to_article2_1(x["name_parts"],pr=0)
            pa = re.sub('\*$','',x["partnumber_parts"])
            av = status_erc(x["availability_parts"])
            #dict_erc[key]=(x["name_parts"],x["providerprice_parts"],status_erc(x["availability_parts"]))
            if pa:
                set_erc.add(pa)
                n,pr = x['name_parts'],x['providerprice_parts']
                prov,_ = Providers.objects.get_or_create(name_provider='erc')
                prov1 = Providers.objects.get(name_provider='-')
                p1 = Parts_full.objects.filter(partnumber_parts=pa,providers=prov)
                try:
                    a1,_ = Articles.objects.get_or_create(article=pa,item_name=n,item_price=kind)
                except:
                    a1 = Articles.objects.get(article=pa)
                if not p1:
                    p_itl = Parts_full.objects.create(name_parts=n,
                    partnumber_parts=pa,providers=prov,
                    providerprice_parts=pr,date_chg=timezone.now(),
                    availability_parts=av,kind=kind)
                    a1.parts_full.add(p_itl)
                    count_no += 1
                elif p1.count() > 0:
                    temp2 = p1.first()
                    temp2.availability_parts = av
                    temp2.providerprice_parts = pr
                    temp2.date_chg = timezone.now()
                    temp2.kind = kind
                    temp2.save()
                    count_on += 1
                    if p1.count() > 1:
                        print(f'count:{p1.count()} ')
                        for x in p1[1:]:
                            x.delete()
                if Parts_full.objects.filter(partnumber_parts=pa,providers=prov1).exists() and av == 'yes':
                    pl = Parts_full.objects.filter(partnumber_parts=pa,providers=prov1)[0]
                    try:
                        if float(pl.providerprice_parts) > float(pr):
                            pl.providerprice_parts = pr
                            pl.save()
                    except:
                        print(f'error in erc element:{pa}')
                else:
                    pr = pr if av == 'yes' else 0
                    p_main = Parts_full.objects.create(name_parts=n,
                    partnumber_parts=pa,providers=prov1,
                    providerprice_parts=pr,date_chg=timezone.now(),
                    availability_parts=av,kind=kind)
                    a1.parts_full.add(p_main)
            else:
                continue

        
Traceback (most recent call last):
  File "<pyshell#108>", line 20, in <module>
    providerprice_parts=pr,date_chg=timezone.now(),
NameError: name 'timezone' is not defined
>>> from django.utils import timezone
>>> for x in erc_.iloc:
        if isinstance(x['subcategory'],str) and x['subcategory'] in dict1:
            kind = dict1[x['subcategory']] if dict1[x['subcategory']] != 0 else to_article2_1(x["name_parts"],pr=0)
            pa = re.sub('\*$','',x["partnumber_parts"])
            av = status_erc(x["availability_parts"])
            #dict_erc[key]=(x["name_parts"],x["providerprice_parts"],status_erc(x["availability_parts"]))
            if pa:
                set_erc.add(pa)
                n,pr = x['name_parts'],x['providerprice_parts']
                prov,_ = Providers.objects.get_or_create(name_provider='erc')
                prov1 = Providers.objects.get(name_provider='-')
                p1 = Parts_full.objects.filter(partnumber_parts=pa,providers=prov)
                try:
                    a1,_ = Articles.objects.get_or_create(article=pa,item_name=n,item_price=kind)
                except:
                    a1 = Articles.objects.get(article=pa)
                if not p1:
                    p_itl = Parts_full.objects.create(name_parts=n,
                    partnumber_parts=pa,providers=prov,
                    providerprice_parts=pr,date_chg=timezone.now(),
                    availability_parts=av,kind=kind)
                    a1.parts_full.add(p_itl)
                    count_no += 1
                elif p1.count() > 0:
                    temp2 = p1.first()
                    temp2.availability_parts = av
                    temp2.providerprice_parts = pr
                    temp2.date_chg = timezone.now()
                    temp2.kind = kind
                    temp2.save()
                    count_on += 1
                    if p1.count() > 1:
                        print(f'count:{p1.count()} ')
                        for x in p1[1:]:
                            x.delete()
                if Parts_full.objects.filter(partnumber_parts=pa,providers=prov1).exists() and av == 'yes':
                    pl = Parts_full.objects.filter(partnumber_parts=pa,providers=prov1)[0]
                    try:
                        if float(pl.providerprice_parts) > float(pr):
                            pl.providerprice_parts = pr
                            pl.save()
                    except:
                        print(f'error in erc element:{pa}')
                else:
                    pr = pr if av == 'yes' else 0
                    p_main = Parts_full.objects.create(name_parts=n,
                    partnumber_parts=pa,providers=prov1,
                    providerprice_parts=pr,date_chg=timezone.now(),
                    availability_parts=av,kind=kind)
                    a1.parts_full.add(p_main)
            else:
                continue

        
Traceback (most recent call last):
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/models/query.py", line 573, in get_or_create
    return self.get(**kwargs), False
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/models/query.py", line 431, in get
    self.model._meta.object_name
cat.models.Articles.DoesNotExist: Articles matching query does not exist.

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/backends/utils.py", line 84, in _execute
    return self.cursor.execute(sql, params)
psycopg2.errors.StringDataRightTruncation: value too long for type character varying(100)


The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "<pyshell#111>", line 14, in <module>
    a1,_ = Articles.objects.get_or_create(article=pa,item_name=n,item_price=kind)
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/models/manager.py", line 85, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/models/query.py", line 576, in get_or_create
    return self._create_object_from_params(kwargs, params)
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/models/query.py", line 610, in _create_object_from_params
    obj = self.create(**params)
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/models/query.py", line 447, in create
    obj.save(force_insert=True, using=self.db)
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/models/base.py", line 754, in save
    force_update=force_update, update_fields=update_fields)
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/models/base.py", line 792, in save_base
    force_update, using, update_fields,
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/models/base.py", line 895, in _save_table
    results = self._do_insert(cls._base_manager, using, fields, returning_fields, raw)
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/models/base.py", line 935, in _do_insert
    using=using, raw=raw,
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/models/manager.py", line 85, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/models/query.py", line 1254, in _insert
    return query.get_compiler(using=using).execute_sql(returning_fields)
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/models/sql/compiler.py", line 1397, in execute_sql
    cursor.execute(sql, params)
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/backends/utils.py", line 98, in execute
    return super().execute(sql, params)
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/backends/utils.py", line 66, in execute
    return self._execute_with_wrappers(sql, params, many=False, executor=self._execute)
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/backends/utils.py", line 75, in _execute_with_wrappers
    return executor(sql, params, many, context)
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/backends/utils.py", line 84, in _execute
    return self.cursor.execute(sql, params)
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/utils.py", line 90, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/backends/utils.py", line 84, in _execute
    return self.cursor.execute(sql, params)
django.db.utils.DataError: value too long for type character varying(100)


During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "<pyshell#111>", line 16, in <module>
    a1 = Articles.objects.get(article=pa)
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/models/manager.py", line 85, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/models/query.py", line 431, in get
    self.model._meta.object_name
cat.models.Articles.DoesNotExist: Articles matching query does not exist.
>>> for x in erc_.iloc:
	pa = re.sub('\*$','',x["partnumber_parts"])
	n,pr = x['name_parts'],x['providerprice_parts']
	a1= Articles.objects.filter(article=pa,item_name=n)
	if a1.count()>1:
		print(pa,end=' ')


>>> for x in erc_.iloc:
	pa = re.sub('\*$','',x["partnumber_parts"])
	n,pr = x['name_parts'],x['providerprice_parts']
	a1= Articles.objects.filter(article=pa,item_name=n)
	if a1.count()>1:
		print(pa,end=' ')

		
>>>  erc_.iloc[0]
SyntaxError: unexpected indent
>>> erc_.iloc[0]
subcategory            Підкатегорія
name_parts             Найменування
partnumber_parts                Код
providerprice_parts           Дилер
availability_parts           Кіл-ть
Name: 0, dtype: object
>>>  erc_.iloc[1]
SyntaxError: unexpected indent
>>> erc_.iloc[1]
subcategory                          Колонки для ПК
name_parts             Колонки Genius SP-U115 Black
partnumber_parts                       31731006100*
providerprice_parts                          200.04
availability_parts                                0
Name: 1, dtype: object
>>> len('ЗП Remax SET RP-U22 PRO 2.4A 2*USB + кабель Lightning 220V (EU) white')
69
>>> erc_.iloc[1]["partnumber_parts"]
'31731006100*'
>>> re.sub('\*$','',erc_.iloc[1]["partnumber_parts"])[:49]
'31731006100'
>>> prov,_ = Providers.objects.get_or_create(name_provider='erc')
>>> Parts_full.objects.filter(providers=prov)
<QuerySet [<Parts_full: A68 ASUS>, <Parts_full: Пам'ять до ПК Kingston DDR4 2666 16GB HyperX Fury Black>, <Parts_full: Пам'ять до ПК Kingston DDR4 3600 16GB HyperX Fury Black>, <Parts_full: Ryzen 5 3600 BOX>, <Parts_full: A320 Gigabyte>, <Parts_full: H310 Asrock>, <Parts_full: B365 ASrock mATX>, <Parts_full: Материнскьа плата GIGABYTE Z490M s1200 Z490 4xDDR4 M.2 DP-HDMI-DVI Type-C mATX>, <Parts_full: MSI CORE FROZR L>, <Parts_full: GT710 2Gb Gigabyte>, <Parts_full: GT1030 Asus>, <Parts_full: GTX1650 Gigabyte>, <Parts_full: Вiдеокарта ASUS GeForce GTX1650 4GB DDR5 OC>, <Parts_full: GTX1650 Super ASUS>, <Parts_full: GTX1650 Super Gigabyte>, <Parts_full: GTX1660 ASUS>, <Parts_full: Відеокарта GIGABYTE GeForce GTX1660 6GB DDR5 192bit DPx3-HDMI OC>, <Parts_full: RTX2070 Gigabyte>, <Parts_full: RTX2060Super Gigabyte>, <Parts_full: RTX2070 ASUS>, '...(remaining elements truncated)...']>
>>> for x in erc_.iloc:
        if isinstance(x['subcategory'],str) and x["partnumber_parts"] and x['subcategory'] in dict1:
            kind = dict1[x['subcategory']] if dict1[x['subcategory']] != 0 else to_article2_1(x["name_parts"],pr=0)
            pa = re.sub('\*$','',x["partnumber_parts"])[:49]
            av = status_erc(x["availability_parts"])
            #dict_erc[key]=(x["name_parts"],x["providerprice_parts"],status_erc(x["availability_parts"]))
            if pa:
                set_erc.add(pa)
                n,pr = x['name_parts'][:99],x['providerprice_parts'][:49]
                prov,_ = Providers.objects.get_or_create(name_provider='erc')
                prov1 = Providers.objects.get(name_provider='-')
                p1 = Parts_full.objects.filter(partnumber_parts=pa,providers=prov)
                try:
                    a1,_ = Articles.objects.get_or_create(article=pa,item_name=n,item_price=kind)
                except:
                    a1 = Articles.objects.get(article=pa)
                if not p1:
                    p_itl = Parts_full.objects.create(name_parts=n,
                    partnumber_parts=pa,providers=prov,
                    providerprice_parts=pr,date_chg=timezone.now(),
                    availability_parts=av,kind=kind)
                    a1.parts_full.add(p_itl)
                    count_no += 1
                elif p1.count() > 0:
                    temp2 = p1.first()
                    temp2.availability_parts = av
                    temp2.providerprice_parts = pr
                    temp2.date_chg = timezone.now()
                    temp2.kind = kind
                    temp2.save()
                    count_on += 1
                    if p1.count() > 1:
                        print(f'count:{p1.count()} ')
                        for x in p1[1:]:
                            x.delete()
                if Parts_full.objects.filter(partnumber_parts=pa,providers=prov1).exists() and av == 'yes':
                    pl = Parts_full.objects.filter(partnumber_parts=pa,providers=prov1)[0]
                    try:
                        if float(pl.providerprice_parts) > float(pr):
                            pl.providerprice_parts = pr
                            pl.save()
                    except:
                        print(f'error in erc element:{pa}')
                else:
                    pr = pr if av == 'yes' else 0
                    p_main = Parts_full.objects.create(name_parts=n,
                    partnumber_parts=pa,providers=prov1,
                    providerprice_parts=pr,date_chg=timezone.now(),
                    availability_parts=av,kind=kind)
                    a1.parts_full.add(p_main)
            else:
                continue

        
Traceback (most recent call last):
  File "<pyshell#129>", line 9, in <module>
    n,pr = x['name_parts'][:99],x['providerprice_parts'][:49]
TypeError: 'int' object is not subscriptable
>>> for x in erc_.iloc:
        if isinstance(x['subcategory'],str) and x["partnumber_parts"] and x['subcategory'] in dict1:
            kind = dict1[x['subcategory']] if dict1[x['subcategory']] != 0 else to_article2_1(x["name_parts"],pr=0)
            pa = re.sub('\*$','',x["partnumber_parts"])[:49]
            av = status_erc(x["availability_parts"])
            #dict_erc[key]=(x["name_parts"],x["providerprice_parts"],status_erc(x["availability_parts"]))
            if pa:
                set_erc.add(pa)
                n,pr = x['name_parts'][:99],x['providerprice_parts']
                prov,_ = Providers.objects.get_or_create(name_provider='erc')
                prov1 = Providers.objects.get(name_provider='-')
                p1 = Parts_full.objects.filter(partnumber_parts=pa,providers=prov)
                try:
                    a1,_ = Articles.objects.get_or_create(article=pa,item_name=n,item_price=kind)
                except:
                    a1 = Articles.objects.get(article=pa)
                if not p1:
                    p_itl = Parts_full.objects.create(name_parts=n,
                    partnumber_parts=pa,providers=prov,
                    providerprice_parts=pr,date_chg=timezone.now(),
                    availability_parts=av,kind=kind)
                    a1.parts_full.add(p_itl)
                    count_no += 1
                elif p1.count() > 0:
                    temp2 = p1.first()
                    temp2.availability_parts = av
                    temp2.providerprice_parts = pr
                    temp2.date_chg = timezone.now()
                    temp2.kind = kind
                    temp2.save()
                    count_on += 1
                    if p1.count() > 1:
                        print(f'count:{p1.count()} ')
                        for x in p1[1:]:
                            x.delete()
                if Parts_full.objects.filter(partnumber_parts=pa,providers=prov1).exists() and av == 'yes':
                    pl = Parts_full.objects.filter(partnumber_parts=pa,providers=prov1)[0]
                    try:
                        if float(pl.providerprice_parts) > float(pr):
                            pl.providerprice_parts = pr
                            pl.save()
                    except:
                        print(f'error in erc element:{pa}')
                else:
                    pr = pr if av == 'yes' else 0
                    p_main = Parts_full.objects.create(name_parts=n,
                    partnumber_parts=pa,providers=prov1,
                    providerprice_parts=pr,date_chg=timezone.now(),
                    availability_parts=av,kind=kind)
                    a1.parts_full.add(p_main)
            else:
                continue

        
count:2 
(2, {'cat.Articles_parts_full': 1, 'cat.Parts_full': 1})
>>> import os
>>> from sereja.settings import BASE_DIR
>>> MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
>>> MEDIA_ROOT
'/home/aleksey1652/sereja/media'
>>> erc = pd.read_excel(MEDIA_ROOT+'/прайс_erc.xls', usecols=[0,2,3,6,7],header=None)
>>> erc.iloc[1]
0                      !Розпродаж
2                  Колонки для ПК
3    Колонки Genius SP-U115 Black
6                             220
7                               0
Name: 1, dtype: object
>>> erc = pd.read_excel(MEDIA_ROOT+'/прайс_erc.xls', usecols=[2,3,4,8,12],header=None)
>>> erc.iloc[1]
2                   Колонки для ПК
3     Колонки Genius SP-U115 Black
4                     31731006100*
8                           200.04
12                               0
Name: 1, dtype: object
>>> erc_=erc.rename(columns={2:'subcategory', 3:'name_parts',
            4:'partnumber_parts',8:'providerprice_parts',
            12:'availability_parts'})
>>> erc_.iloc[1]
subcategory                          Колонки для ПК
name_parts             Колонки Genius SP-U115 Black
partnumber_parts                       31731006100*
providerprice_parts                          200.04
availability_parts                                0
Name: 1, dtype: object
>>> Parts_full.objects.filter(partnumber_parts='100-000000050',remainder=True)
<QuerySet []>
>>> Parts_full.objects.filter(partnumber_parts='100-000000050',remainder=False)
<QuerySet []>
>>> Parts_full.objects.filter(partnumber_parts='100-000000050',providers__name_provider='-')
<QuerySet [<Parts_full: Ryzen 5 3500>]>
>>> p1=Parts_full.objects.get(partnumber_parts='100-000000050',providers__name_provider='-')
>>> p1.remainder
'price:141; 1'
>>> p2=Parts_full.objects.get(partnumber_parts='100-000000050',providers__name_provider='asbis')
>>> p2.remainder
>>> with open('load_form_providers/brain-price.json', "r") as write_file:
                brain=json.load(write_file)

                
>>> br=list(brain.keys())
>>> br[:3]
['2', '3', '17']
>>> br1=brain['29']
>>> br1.keys()
dict_keys(['CategoryID', 'Code', 'Group', 'Article', 'Vendor', 'Model', 'Name', 'Description', 'PriceUSD', 'Price_ind', 'CategoryName', 'Bonus', 'RecommendedPrice', 'DDP', 'Warranty', 'Stock', 'Note', 'DayDelivery', 'ProductID', 'URL', 'UKTVED', 'GroupID', 'ClassID', 'ClassName', 'Available', 'Country', 'RetailPrice', 'CostDelivery', 'Exclusive', 'FOP'])
>>> len(br)
113164
>>> br1['Description']
'Compact Flash, 16 ГБ'
>>> brain_cool=[]
>>> for x in brain.values():
	if x['Group']=='Системы охлаждения':
		brain_cool.append((x[Article],x[Description]))

		
Traceback (most recent call last):
  File "<pyshell#161>", line 3, in <module>
    brain_cool.append((x[Article],x[Description]))
NameError: name 'Article' is not defined
>>> for x in brain.values():
	if x['Group']=='Системы охлаждения':
		brain_cool.append((x['Article'],x['Description']))

		
>>> len(brain_cool)
820
>>> brain_cool[:2]
[('N8R-22K1-GP', 'Количество вентиляторов - 1, диаметр вентиляторов - 80 мм, тип подшипника - втулка (подшипник скольжения), максимальная скорость вращения вентиляторов - 2200RPM, материал - пластик, уровень шума - 21dB, тип разъема подключения - 2pin (Molex), размер - 80 х 80 х 25 мм'), ('RR-212E-16PK-R1', 'Для процессоров - INTEL, AMD, под сокет - 775, 1155, 1156, 1366, 2011, AM2, AM2+, AM3, AM3+, FM1, тип системы охлаждения - активная (кулер), материал радиатора - алюминий + медь, диаметр вентиляторов - 120 мм, максимальная скорость вращения вентиляторов - 1300 об/мин, система подшипников - втулка (подшипник скольжения), уровень шума - 31 dB, разъемы питания - 4-pin, подсветка - нет, 4 тепловые трубки')]
>>> for x in brain_cool:
	if x[0]=='RH-I30-26FK-R1':
		print(x[1])

		
Для процессоров - INTEL, под сокет - 1151, 1150, 1155, 1156, тип системы охлаждения - активная (кулер), материал радиатора - алюминий, диаметр вентиляторов - 92 мм, максимальная скорость вращения вентиляторов - 2600 об/мин, система подшипников - втулка (подшипник скольжения), уровень шума - 28 dB, разъемы питания - 3-pin, подсветка - нет
>>> re.findall('диаметр вентиляторов - (\d+)','Количество вентиляторов - 1, диаметр вентиляторов - 80 мм, тип подшипника - втулка (подшипник скольжения), максимальная скорость вращения вентиляторов - 2200RPM, материал - пластик, уровень шума - 21dB, тип разъема подключения - 2pin (Molex), размер - 80 х 80 х 25 мм')
['80']
>>> s='Количество вентиляторов - 1, диаметр вентиляторов - 80 мм, тип подшипника - втулка (подшипник скольжения), максимальная скорость вращения вентиляторов - 2200RPM, материал - пластик, уровень шума - 21dB, тип разъема подключения - 2pin (Molex), размер - 80 х 80 х 25 мм'
>>> re.findall('максимальная скорость вращения вентиляторов - (\d+)',s)
['2200']
>>> re.findall('уровень шума - (\d+)',s)
['21']
>>> brain_proc=[]
>>> for x in brain.values():
	if x['Group']=='Процессоры':
		brain_proc.append((x['Article'],x['Description']))

		
>>> brain_proc[:2]
[('YD160XBCAEWOF', 'AM4, 6 ядер, 12 потоков, 3.6, Boost, ГГц - 4.0, нет, L3: 16MB, 14nm, TDP - 95W, BOX без кулера'), ('YD1600BBAEBOX', 'AM4, 6 ядер, 12 потоков, 3.2, Boost, ГГц - 3.6, нет, L3: 16MB, 14nm, TDP - 65W, Zen, + Wraith Spire cooler')]
>>> len(brain_proc)
77
>>> brain_proc[2:12]
[('YD192XA8UC9AE', 'TR4, 12 ядер, 3.5, нет, L3: 32MB, 14nm, TDP - 180W, Zen, без кулера, Tray'), ('YD190XA8AEWOF', 'TR4, 8 ядер, 3.8, нет, L3: 16MB, 14nm, TDP - 180W, Zen, без кулера, BOX'), ('YD2600BBAFBOX', 'AM4, 6 ядер, 12 потоков, 3.4, Boost, ГГц - 3.9, нет, L3: 16MB, TDP - 65W, Zen+, BOX'), ('BX80684I79700K', 's1151, 8 ядер, 8 потоков, 3.6, Boost, ГГц - 4.9, Intel UHD 630, L3: 12MB, TDP - 95W, разблокированный множитель, BOX'), ('BX80684I59600KF', 's1151, 6 ядер, 6 потоков, 3.7, Boost, ГГц - 4.6, нет, L3: 9MB, 14nm, TDP - 95W, DDR4-2666, BOX'), ('BX80684I79700KF', 's1151, 8 ядер, 8 потоков, 3.6, Boost, ГГц - 4.9, нет, Intel Smart Cache - 12Mb, 14nm, TDP - 95W, Coffee Lake, BOX'), ('BX80684I99900KF', 's1151, 8 ядер, 16 потоков, 3.6, Boost, ГГц - 5.0, нет, L3: 16MB, 14nm, TDP - 95W, BOX'), ('YD2600BBM6IAF', 'AM4, 6 ядер, 12 потоков, 3.4, Boost, ГГц - 3.9, нет, L3: 16MB, TDP - 65W, Zen+, Tray'), ('100-100000031BOX', 'AM4, 6 ядер, 12 потоков, 3.6, Boost, ГГц - 4.2, нет, L3: 32MB, 7nm, TDP - 65W, Zen 2, разблокированный множитель, BOX'), ('100-100000025BOX', 'AM4, 8 ядер, 16 потоков, 3.9, Boost, ГГц - 4.5, нет, L3: 32MB, 7nm, TDP - 105W, Zen 2, BOX')]
>>> list_hd=[]
>>> re.findall('hd',l.lower())
Traceback (most recent call last):
  File "<pyshell#181>", line 1, in <module>
    re.findall('hd',l.lower())
NameError: name 'l' is not defined
>>> l='s1151, 8 ядер, 8 потоков, 3.6, Boost, ГГц - 4.9, Intel UHD 630, L3: 12MB, TDP - 95W, разблокированный множитель, BOX'
>>> re.findall('hd',l.lower())
['hd']
>>> for b in brain_proc:
	if re.findall('hd',b[1].lower()):
		list_hd.append(b)

		
>>> len(list_hd)
16
>>> list_hd
[('BX80684I79700K', 's1151, 8 ядер, 8 потоков, 3.6, Boost, ГГц - 4.9, Intel UHD 630, L3: 12MB, TDP - 95W, разблокированный множитель, BOX'), ('CM8068403873925', 's1151, 8 ядер, 3.6, Boost, ГГц - 4.5, 5.0, Intel UHD 630, L3: 16MB, TDP - 95W, разблокированный множитель, Tray'), ('BX8070110700K', 's1200, 8 ядер, 16 потоков, 3.8, Boost, ГГц - 5.1, Intel UHD Graphics 630, Intel Smart Cache - 16Mb, 14nm, TDP - 125W, Comet Lake, BOX'), ('BX8070110700', 's1200, 8 ядер, 16 потоков, 2.9, Boost, ГГц - 4.8, Intel UHD Graphics 630, Intel Smart Cache - 16Mb, 14nm, TDP - 65W, Comet Lake, BOX'), ('BX8070110850K', 's1200, 10 ядер, 20 потоков, 3.6, Boost, ГГц - 5.2, Boost v3.0, ГГц - 5.1, Intel UHD Graphics 630, Intel Smart Cache - 20Mb, 14nm, TDP - 125W, Comet Lake, разблокированный множитель, BOX без кулера'), ('BX8070110600KA', 's1200, 6 ядер, 12 потоков, 4.1, Boost, ГГц - 4.8, Intel UHD Graphics 630, Intel Smart Cache - 12Mb, 14nm, TDP - 125W, Comet Lake, разблокированный множитель, BOX без кулера'), ('BX8070110900', 's1200, 10 ядер, 20 потоков, 2.8, Boost, ГГц - 5.2, Intel UHD Graphics 630, Intel Smart Cache - 20Mb, 14nm, TDP - 65W, Comet Lake, BOX'), ('BX806849900K', 's1151, 8 ядер, 16 потоков, 3.6, Boost, ГГц - 5.0, Intel UHD Graphics 630, L3: 16MB, 14nm, TDP - 95W, Coffee Lake, без кулера, разблокированный множитель, BOX без кулера'), ('BX8070811400', 's1200, 6 ядер, 12 потоков, 2.6, Boost, ГГц - 4.4, Intel UHD Graphics 730, Intel Smart Cache - 12Mb, 14nm, TDP - 65W, Rocket Lake, DDR4-3200, BOX'), ('BX8070811600', 's1200, 6 ядер, 12 потоков, 2.8, Boost, ГГц - 4.8, Intel UHD Graphics 750, Intel Smart Cache - 12Mb, 14nm, TDP - 65W, Rocket Lake, DDR4-3200, BOX'), ('BX8070811600K', 's1200, 6 ядер, 12 потоков, 3.9, Boost, ГГц - 4.9, Intel UHD Graphics 750, Intel Smart Cache - 12Mb, 14nm, TDP - 95W, Rocket Lake, DDR4-3200, BOX'), ('BX8070811700', 's1200, 8 ядер, 16 потоков, 2.5, Boost, ГГц - 4.8, Boost v3.0, ГГц - 4.9, Intel UHD Graphics 750, Intel Smart Cache - 16Mb, 14nm, TDP - 65W, Rocket Lake, DDR4-3200, BOX'), ('BX8070811700K', 's1200, 8 ядер, 16 потоков, 3.6, Boost, ГГц - 5.0, Intel UHD Graphics 750, Intel Smart Cache - 16Mb, 14nm, TDP - 95W, Rocket Lake, DDR4-3200, BOX'), ('BX8070811900', 's1200, 8 ядер, 16 потоков, 2.5, Boost, ГГц - 5.2, Intel UHD Graphics 750, Intel Smart Cache - 16Mb, 14nm, TDP - 65W, Rocket Lake, DDR4-3200, BOX'), ('BX8070811900K', 's1200, 8 ядер, 16 потоков, 3.5, Boost, ГГц - 5.3, Intel UHD Graphics 750, Intel Smart Cache - 16Mb, 14nm, TDP - 95W, Rocket Lake, DDR4-3200, BOX'), ('CM8070804491513', 's1200, 6 ядер, 12 потоков, 2.8, Boost, ГГц - 4.8, Intel UHD Graphics 750, Intel Smart Cache - 12Mb, 14nm, TDP - 65W, Rocket Lake, DDR4-3200, Tray')]
>>> re.findall('(\d+) потоков',l)
['8']
>>> re.findall('(\d+) ядер',l)
['8']
>>> re.findall('потоков,(\d+)',l)
[]
>>> re.findall('потоков, (\d+)',l)
['3']
>>> re.findall('потоков, (\d\.\d)',l)
['3.6']
>>> re.findall('потоков,.?(\d\.\d)',l)
['3.6']
>>> re.findall('потоков,.?(\d\.\d)','s1151, 8 ядер, 8 потоков,  3.6')
[]
>>> re.findall('потоков,.*(\d\.\d)','s1151, 8 ядер, 8 потоков,3.6')
['3.6']
>>> re.findall('потоков,.?(\d\.\d)','s1151, 8 ядер, 8 потоков,   3.6')
[]
>>> re.findall('потоков,.*(\d\.\d)','s1151, 8 ядер, 8 потоков,   3.6')
['3.6']
>>> re.findall('потоков,.*(\d\.\d)',l.lower())
['4.9']
>>> re.findall('потоков,.?(\d\.\d)',l.lower())
['3.6']
>>> re.findall('потоков,\t*(\d\.\d)',l.lower())
[]
>>> re.findall('потоков,\t?(\d\.\d)',l.lower())
[]
>>> re.findall('потоков,?(\d\.\d)',l.lower())
[]
>>> re.findall('потоков,.?(\d\.\d)','s1151, 8 ядер, 8 потоков,3.6')
['3.6']
>>> re.findall('l[1,2,3,4]:.?(\d\.\d)',', Intel UHD 630, L3: 12MB, TDP - 95W')
[]
>>> re.findall('l[1,2,3,4]:.?(\d\.\d)',', Intel UHD 630, L3: 12MB, TDP - 95W'.lower())
[]
>>> re.findall('l[1234]:.?(\d*)|intel smart cache - (\d*)',l.lower())
[('12', '')]
>>> 'Процессоры Ryzen - это гарантия стабильности работы и ваше \
                         преимущество над соперниками в современных играх!'
'Процессоры Ryzen - это гарантия стабильности работы и ваше                          преимущество над соперниками в современных играх!'
>>> re.findall('(\d+).+потоков',l)
['1151']
>>> re.findall('(\d+) потоков',l)
['8']
>>> brain_proc=[]
>>> for x in brain.values():
	if x['Group']=='Процессоры':
		brain_proc.append((x['Article'],x['Description'],x['Name']))

		
>>> brain_proc[:2]
[('YD160XBCAEWOF', 'AM4, 6 ядер, 12 потоков, 3.6, Boost, ГГц - 4.0, нет, L3: 16MB, 14nm, TDP - 95W, BOX без кулера', 'Процессор AMD Ryzen 5 1600X (YD160XBCAEWOF)'), ('YD1600BBAEBOX', 'AM4, 6 ядер, 12 потоков, 3.2, Boost, ГГц - 3.6, нет, L3: 16MB, 14nm, TDP - 65W, Zen, + Wraith Spire cooler', 'Процессор AMD Ryzen 5 1600 (YD1600BBAEBOX)')]
>>> from scrapy import get_video,get_cpu,get_mb,get_case,get_ps,get_cool,get_hdd_ssd,get_mem
>>> get_cpu('Процессор AMD Ryzen 5 1600 (YD1600BBAEBOX)')
[5, 1600]
>>> to_article2_1('Процессор AMD Ryzen 5 1600 (YD1600BBAEBOX)')
'aproc'
>>> get_cpu('Ryzen Threadripper 2990WX BOX')
[2990, 'wx']
>>> get_cpu('athlon 200ge')
[200, 'ge']
>>> get_cpu('athlon 3000g tray')
[3000, 'g']
>>> kind2=re.findall('athlon|threadripper','Ryzen Threadripper 2990WX BOX')
>>> kind2
[]
>>> re.findall('athlon|threadripper','Ryzen Threadripper 2990WX BOX'.lower())
['threadripper']
>>> re.findall('athlon|threadripper','Athlon 3000G tray'.lower())
['athlon']
>>> re.findall('athlon|threadripper','Процессор AMD Ryzen 5 1600 (YD1600BBAEBOX)'.lower())
[]
>>> get_cpu('celeron j1600')
[1600]
>>> get_cpu('celeron g1600')
[1600]
>>> get_cpu('pentium g1600')
[1600]
>>> get_cpu('pentium g1600f')
[1600, 'f']
>>> get_cpu('celeron g1600f')
[1600, 'f']
>>> get_cpu('pentium g1600fe')
[1600, 'fe']
>>> get_cpu('pentium g1600feq')
[1600, 'fe']
>>> def get_proc_discr(obj):
    formula = get_cpu(obj)
    kind = to_article2_1(obj)
    #kind2 = 
    if kind == 'aproc' and len(formula) > 1 and isinstance(formula[1],int):
        if len(formula) == 2:
            return (f'Ryzen {formula[0]} {formula[1]} BOX', f'Ryzen {formula[0]} {formula[1]}')
        if len(formula) > 2:
            return (f'Ryzen {formula[0]} {formula[1]}{formula[2]} BOX', f'Ryzen {formula[0]} {formula[1]}{formula[2]}')
    if kind == 'aproc':
        kind2 = re.findall('athlon|threadripper',obj.lower())
        kind2 = kind2[0] if kind2 else ''
        if kind2 == 'athlon' and len(formula) > 1:
            return (f'Athlon {formula[0]}{formula[1]} BOX', f'Athlon {formula[0]}{formula[1]}')
        if kind2 == 'athlon' and len(formula) > 0:
            return (f'Athlon {formula[0]} BOX', f'Athlon {formula[0]}')
        if kind2 == 'threadripper' and len(formula) > 1:
            return (f'Ryzen Threadripper {formula[0]}{formula[1]} BOX', f'Threadripper {formula[0]}{formula[1]}')
        if kind2 == 'threadripper' and len(formula) > 0:
            return (f'Ryzen Threadripper {formula[0]} BOX', f'Threadripper {formula[0]}')
    if kind == 'iproc' and len(formula) > 1 and isinstance(formula[1],int) and obj.lower().find('core') != -1:
        if len(formula) == 2:
            return (f'Core i{formula[0]} {formula[1]} BOX', f'Core i{formula[0]} {formula[1]}')
        if len(formula) > 2:
            return (f'Core i{formula[0]} {formula[1]}{formula[2]} BOX', f'Core i{formula[0]} {formula[1]}{formula[2]}')
    if kind == 'iproc':
        kind2 = re.findall('celeron|pentium',obj.lower())
        kind2 = kind2[0] if kind2 else ''
        if kind2 == 'celeron' and len(formula) > 1:
            return (f'Celeron {formula[0]}{formula[1]} BOX', f'Celeron {formula[0]}{formula[1]}')
        if kind2 == 'celeron' and len(formula) > 0:
            return (f'Celeron {formula[0]} BOX', f'Celeron {formula[0]}')
        if kind2 == 'pentium' and len(formula) > 1:
            return (f'Pentium {formula[0]} {formula[1]} BOX', f'Pentium {formula[0]}{formula[1]}')
        if kind2 == 'pentium' and len(formula) > 0:
            return (f'Pentium {formula[0]} BOX', f'Pentium {formula[0]}')

        
>>> get_proc_discr('Ryzen Threadripper 2990WX BOX')
('Ryzen Threadripper 2990wx BOX', 'Threadripper 2990wx')
>>> get_proc_discr('Процессор AMD Ryzen 5 1600X (YD160XBCAEWOF)')
('Ryzen 5 1600x BOX', 'Ryzen 5 1600x')
>>> get_proc_discr('Athlon 3000G tray')
('Athlon 3000g BOX', 'Athlon 3000g')
>>> get_proc_discr('Процессор intel Core i5 9600kf (YD160XBCAEWOF)')
('Core i5 9600kf BOX', 'Core i5 9600kf')
>>> get_proc_discr('Процессор intel Core i5 9600 (YD160XBCAEWOF)')
('Core i5 9600 BOX', 'Core i5 9600')
>>> get_proc_discr('Процессор intel Celeron g9600 (YD160XBCAEWOF)')
('Celeron 9600 BOX', 'Celeron 9600')
>>> get_proc_discr('Процессор intel Celeron g9600f (YD160XBCAEWOF)')
('Celeron 9600f BOX', 'Celeron 9600f')
>>> get_proc_discr('Процессор intel Pentium g9600f (YD160XBCAEWOF)')
('Pentium 9600 f BOX', 'Pentium 9600f')
>>> proc_dict = {
                'iproc': ('desc_ukr':
                        'Відчуй ефект повного занурення в ігровий процес на максимальних налаштуваннях графіки разом з процесорами Intel.',
                        'desc_ru': 
                        'Почувствуй эффект полного погружения в игровой процесс на максимальных настройках графики вместе с процессорами Intel.',
                        'vendor':'Intel',
                        'depend_from_type':'chipset'
                        ),
                'aproc': ('desc_ukr':
                        'Процесори Ryzen – це гарантія стабільності роботи та ваша перевага над суперниками в сучасних іграх!',
                        'desc_ru': 
                        'Процессоры Ryzen - это гарантия стабильности работы и ваше преимущество над соперниками в современных играх!',
                        'vendor':'Amd',
                        'depend_from_type':'chipset'
                        )
		
SyntaxError: invalid syntax
>>> proc_dict = {
                'iproc': ('desc_ukr':'Відчуй ефект повного занурення в ігровий процес на максимальних налаштуваннях графіки разом з процесорами Intel.',
                        'desc_ru':'Почувствуй эффект полного погружения в игровой процесс на максимальных настройках графики вместе с процессорами Intel.',
                        'vendor':'Intel',
                        'depend_from_type':'chipset'
                        ),
                'aproc': ('desc_ukr':'Процесори Ryzen – це гарантія стабільності роботи та ваша перевага над суперниками в сучасних іграх!',
                        'desc_ru':'Процессоры Ryzen - это гарантия стабильности работы и ваше преимущество над соперниками в современных играх!',
                        'vendor':'Amd',
                        'depend_from_type':'chipset'
                        )
		
SyntaxError: invalid syntax
>>> ('a':'aa','b':'bb')
		
SyntaxError: invalid syntax
>>> ['a':'aa','b':'bb']
		
SyntaxError: invalid syntax
>>> proc_dict = {
                'iproc': ({'desc_ukr':'Відчуй ефект повного занурення в ігровий процес на максимальних налаштуваннях графіки разом з процесорами Intel.'},
                        {'desc_ru':'Почувствуй эффект полного погружения в игровой процесс на максимальных настройках графики вместе с процессорами Intel.'},
                        {'vendor':'Intel'},
                        {'depend_from_type':'chipset'}
                        ),
                'aproc': ({'desc_ukr':'Процесори Ryzen – це гарантія стабільності роботи та ваша перевага над суперниками в сучасних іграх!'},
                        {'desc_ru':'Процессоры Ryzen - это гарантия стабильности работы и ваше преимущество над соперниками в современных играх!'},
                        {'vendor':'Amd'},
                        {'depend_from_type':'chipset'}
                        )
                }
		
>>> prod_dict={}
		
>>> proc_dict['iproc'][0].keys()
		
dict_keys(['desc_ukr'])
>>> for t in proc_dict['iproc']:
	tt=list(t.keys())[0]
	prod_dict[tt]=t[tt]

		
>>> prod_dict
		
{'desc_ukr': 'Відчуй ефект повного занурення в ігровий процес на максимальних налаштуваннях графіки разом з процесорами Intel.', 'desc_ru': 'Почувствуй эффект полного погружения в игровой процесс на максимальных настройках графики вместе с процессорами Intel.', 'vendor': 'Intel', 'depend_from_type': 'chipset'}
>>> def get_hd_in_proc(obj,kind):
    if kind == 'aproc':
        if obj.lower().find('radeon') != -1:
            return 'AMD Radeon Vega'
    if kind == 'iproc':
        if obj.lower().find('hd') != -1:
            return 'Intel UHD Graphics'
    else:
        ''

		
>>> get_hd_in_proc('s1200, 8 ядер, 16 потоков, 3.5, Boost, ГГц - 5.3, Intel UHD Graphics 750, Intel Smart Cache - 16Mb, 14nm, TDP - 95W, Rocket Lake, DDR4-3200, BOX','iproc')
		
'Intel UHD Graphics'
>>> get_hd_in_proc('AM4, 8 ядер, 16 потоков, 3.9, Boost, ГГц - 4.5, нет, L3: 32MB, 7nm, TDP - 105W, Zen 2, BOX','aproc')
		
>>> def get_relatins_proc(obj):
    formula = get_cpu(obj)
    if len(formula) == 1 or (len(formula) > 1 and isinstance(formula[1],str)):
        discr = CPU.objects.filter(item_name__icontains=formula[0])
        for d in discr:
            if d.depend_from:
                return d.depend_from
    if len(formula) > 1 and isinstance(formula[1],int):
        discr = CPU.objects.filter(item_name__icontains=formula[1])
        for d in discr:
            if d.depend_from:
                return d.depend_from
    else:
        return ''

		
>>> get_relatins_proc()
KeyboardInterrupt
>>> 'Процессор intel Core i5 9600 (YD160XBCAEWOF)'
		
'Процессор intel Core i5 9600 (YD160XBCAEWOF)'
>>> get_relatins_proc('Процессор intel Core i5 9600 (YD160XBCAEWOF)')
		
Traceback (most recent call last):
  File "<pyshell#264>", line 1, in <module>
    get_relatins_proc('Процессор intel Core i5 9600 (YD160XBCAEWOF)')
  File "<pyshell#262>", line 9, in get_relatins_proc
    discr = CPU.objects.filter(item_name__icontains=formula[1])
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/models/manager.py", line 85, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/models/query.py", line 942, in filter
    return self._filter_or_exclude(False, *args, **kwargs)
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/models/query.py", line 962, in _filter_or_exclude
    clone._filter_or_exclude_inplace(negate, *args, **kwargs)
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/models/query.py", line 969, in _filter_or_exclude_inplace
    self._query.add_q(Q(*args, **kwargs))
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/models/sql/query.py", line 1358, in add_q
    clause, _ = self._add_q(q_object, self.used_aliases)
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/models/sql/query.py", line 1380, in _add_q
    split_subq=split_subq, check_filterable=check_filterable,
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/models/sql/query.py", line 1258, in build_filter
    lookups, parts, reffed_expression = self.solve_lookup_type(arg)
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/models/sql/query.py", line 1084, in solve_lookup_type
    _, field, _, lookup_parts = self.names_to_path(lookup_splitted, self.get_meta())
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/models/sql/query.py", line 1482, in names_to_path
    "Choices are: %s" % (name, ", ".join(available)))
django.core.exceptions.FieldError: Cannot resolve keyword 'item_name' into field. Choices are: cpu_b_f, cpu_c_t, cpu_cache, cpu_i_g_rus, cpu_i_g_ua, depend_from, depend_from_type, desc_ru, desc_ukr, f_cpu_c_t, f_name, id, is_active, more, name, part_number, price, vendor
>>> def get_relatins_proc(obj):
    formula = get_cpu(obj)
    if len(formula) == 1 or (len(formula) > 1 and isinstance(formula[1],str)):
        discr = CPU.objects.filter(name__icontains=formula[0])
        for d in discr:
            if d.depend_from:
                return d.depend_from
    if len(formula) > 1 and isinstance(formula[1],int):
        discr = CPU.objects.filter(name__icontains=formula[1])
        for d in discr:
            if d.depend_from:
                return d.depend_from
    else:
        return ''

		
>>> get_relatins_proc('Процессор intel Core i5 9600 (YD160XBCAEWOF)')
		
Traceback (most recent call last):
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/backends/utils.py", line 84, in _execute
    return self.cursor.execute(sql, params)
psycopg2.OperationalError: SSL connection has been closed unexpectedly


The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "<pyshell#267>", line 1, in <module>
    get_relatins_proc('Процессор intel Core i5 9600 (YD160XBCAEWOF)')
  File "<pyshell#266>", line 10, in get_relatins_proc
    for d in discr:
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/models/query.py", line 287, in __iter__
    self._fetch_all()
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/models/query.py", line 1308, in _fetch_all
    self._result_cache = list(self._iterable_class(self))
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/models/query.py", line 53, in __iter__
    results = compiler.execute_sql(chunked_fetch=self.chunked_fetch, chunk_size=self.chunk_size)
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/models/sql/compiler.py", line 1156, in execute_sql
    cursor.execute(sql, params)
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/backends/utils.py", line 98, in execute
    return super().execute(sql, params)
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/backends/utils.py", line 66, in execute
    return self._execute_with_wrappers(sql, params, many=False, executor=self._execute)
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/backends/utils.py", line 75, in _execute_with_wrappers
    return executor(sql, params, many, context)
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/backends/utils.py", line 84, in _execute
    return self.cursor.execute(sql, params)
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/utils.py", line 90, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/backends/utils.py", line 84, in _execute
    return self.cursor.execute(sql, params)
django.db.utils.OperationalError: SSL connection has been closed unexpectedly

>>> formula = get_cpu('Процессор intel Core i5 9600 (YD160XBCAEWOF)')
		
>>> formula
		
[5, 9600]
>>> CPU.objects.filter(name__icontains=str(formula[1]))
		
Traceback (most recent call last):
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/backends/base/base.py", line 237, in _cursor
    return self._prepare_cursor(self.create_cursor(name))
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/utils/asyncio.py", line 26, in inner
    return func(*args, **kwargs)
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/backends/postgresql/base.py", line 236, in create_cursor
    cursor = self.connection.cursor()
psycopg2.InterfaceError: connection already closed

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "<pyshell#270>", line 1, in <module>
    CPU.objects.filter(name__icontains=str(formula[1]))
  File "/usr/lib/python3.6/idlelib/rpc.py", line 621, in displayhook
    text = repr(value)
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/models/query.py", line 263, in __repr__
    data = list(self[:REPR_OUTPUT_SIZE + 1])
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/models/query.py", line 287, in __iter__
    self._fetch_all()
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/models/query.py", line 1308, in _fetch_all
    self._result_cache = list(self._iterable_class(self))
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/models/query.py", line 53, in __iter__
    results = compiler.execute_sql(chunked_fetch=self.chunked_fetch, chunk_size=self.chunk_size)
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/models/sql/compiler.py", line 1154, in execute_sql
    cursor = self.connection.cursor()
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/utils/asyncio.py", line 26, in inner
    return func(*args, **kwargs)
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/backends/base/base.py", line 259, in cursor
    return self._cursor()
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/backends/base/base.py", line 237, in _cursor
    return self._prepare_cursor(self.create_cursor(name))
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/utils.py", line 90, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/backends/base/base.py", line 237, in _cursor
    return self._prepare_cursor(self.create_cursor(name))
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/utils/asyncio.py", line 26, in inner
    return func(*args, **kwargs)
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/backends/postgresql/base.py", line 236, in create_cursor
    cursor = self.connection.cursor()
django.db.utils.InterfaceError: connection already closed
>>> CPU.objects.all()
		
Traceback (most recent call last):
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/backends/base/base.py", line 237, in _cursor
    return self._prepare_cursor(self.create_cursor(name))
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/utils/asyncio.py", line 26, in inner
    return func(*args, **kwargs)
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/backends/postgresql/base.py", line 236, in create_cursor
    cursor = self.connection.cursor()
psycopg2.InterfaceError: connection already closed

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "<pyshell#271>", line 1, in <module>
    CPU.objects.all()
  File "/usr/lib/python3.6/idlelib/rpc.py", line 621, in displayhook
    text = repr(value)
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/models/query.py", line 263, in __repr__
    data = list(self[:REPR_OUTPUT_SIZE + 1])
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/models/query.py", line 287, in __iter__
    self._fetch_all()
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/models/query.py", line 1308, in _fetch_all
    self._result_cache = list(self._iterable_class(self))
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/models/query.py", line 53, in __iter__
    results = compiler.execute_sql(chunked_fetch=self.chunked_fetch, chunk_size=self.chunk_size)
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/models/sql/compiler.py", line 1154, in execute_sql
    cursor = self.connection.cursor()
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/utils/asyncio.py", line 26, in inner
    return func(*args, **kwargs)
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/backends/base/base.py", line 259, in cursor
    return self._cursor()
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/backends/base/base.py", line 237, in _cursor
    return self._prepare_cursor(self.create_cursor(name))
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/utils.py", line 90, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/backends/base/base.py", line 237, in _cursor
    return self._prepare_cursor(self.create_cursor(name))
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/utils/asyncio.py", line 26, in inner
    return func(*args, **kwargs)
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/backends/postgresql/base.py", line 236, in create_cursor
    cursor = self.connection.cursor()
django.db.utils.InterfaceError: connection already closed
>>> Parts_short.objects.all()
		
Traceback (most recent call last):
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/backends/base/base.py", line 237, in _cursor
    return self._prepare_cursor(self.create_cursor(name))
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/utils/asyncio.py", line 26, in inner
    return func(*args, **kwargs)
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/backends/postgresql/base.py", line 236, in create_cursor
    cursor = self.connection.cursor()
psycopg2.InterfaceError: connection already closed

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "<pyshell#272>", line 1, in <module>
    Parts_short.objects.all()
  File "/usr/lib/python3.6/idlelib/rpc.py", line 621, in displayhook
    text = repr(value)
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/models/query.py", line 263, in __repr__
    data = list(self[:REPR_OUTPUT_SIZE + 1])
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/models/query.py", line 287, in __iter__
    self._fetch_all()
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/models/query.py", line 1308, in _fetch_all
    self._result_cache = list(self._iterable_class(self))
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/models/query.py", line 53, in __iter__
    results = compiler.execute_sql(chunked_fetch=self.chunked_fetch, chunk_size=self.chunk_size)
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/models/sql/compiler.py", line 1154, in execute_sql
    cursor = self.connection.cursor()
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/utils/asyncio.py", line 26, in inner
    return func(*args, **kwargs)
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/backends/base/base.py", line 259, in cursor
    return self._cursor()
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/backends/base/base.py", line 237, in _cursor
    return self._prepare_cursor(self.create_cursor(name))
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/utils.py", line 90, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/backends/base/base.py", line 237, in _cursor
    return self._prepare_cursor(self.create_cursor(name))
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/utils/asyncio.py", line 26, in inner
    return func(*args, **kwargs)
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/backends/postgresql/base.py", line 236, in create_cursor
    cursor = self.connection.cursor()
django.db.utils.InterfaceError: connection already closed
>>> from cat.models import *
		
>>> Parts_short.objects.all()
		
Traceback (most recent call last):
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/backends/base/base.py", line 237, in _cursor
    return self._prepare_cursor(self.create_cursor(name))
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/utils/asyncio.py", line 26, in inner
    return func(*args, **kwargs)
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/backends/postgresql/base.py", line 236, in create_cursor
    cursor = self.connection.cursor()
psycopg2.InterfaceError: connection already closed

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "<pyshell#274>", line 1, in <module>
    Parts_short.objects.all()
  File "/usr/lib/python3.6/idlelib/rpc.py", line 621, in displayhook
    text = repr(value)
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/models/query.py", line 263, in __repr__
    data = list(self[:REPR_OUTPUT_SIZE + 1])
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/models/query.py", line 287, in __iter__
    self._fetch_all()
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/models/query.py", line 1308, in _fetch_all
    self._result_cache = list(self._iterable_class(self))
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/models/query.py", line 53, in __iter__
    results = compiler.execute_sql(chunked_fetch=self.chunked_fetch, chunk_size=self.chunk_size)
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/models/sql/compiler.py", line 1154, in execute_sql
    cursor = self.connection.cursor()
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/utils/asyncio.py", line 26, in inner
    return func(*args, **kwargs)
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/backends/base/base.py", line 259, in cursor
    return self._cursor()
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/backends/base/base.py", line 237, in _cursor
    return self._prepare_cursor(self.create_cursor(name))
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/utils.py", line 90, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/backends/base/base.py", line 237, in _cursor
    return self._prepare_cursor(self.create_cursor(name))
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/utils/asyncio.py", line 26, in inner
    return func(*args, **kwargs)
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/backends/postgresql/base.py", line 236, in create_cursor
    cursor = self.connection.cursor()
django.db.utils.InterfaceError: connection already closed
>>> prov,_ = Providers.objects.get_or_create(name_provider='erc')
		
Traceback (most recent call last):
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/backends/base/base.py", line 237, in _cursor
    return self._prepare_cursor(self.create_cursor(name))
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/utils/asyncio.py", line 26, in inner
    return func(*args, **kwargs)
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/backends/postgresql/base.py", line 236, in create_cursor
    cursor = self.connection.cursor()
psycopg2.InterfaceError: connection already closed

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "<pyshell#275>", line 1, in <module>
    prov,_ = Providers.objects.get_or_create(name_provider='erc')
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/models/manager.py", line 85, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/models/query.py", line 573, in get_or_create
    return self.get(**kwargs), False
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/models/query.py", line 425, in get
    num = len(clone)
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/models/query.py", line 269, in __len__
    self._fetch_all()
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/models/query.py", line 1308, in _fetch_all
    self._result_cache = list(self._iterable_class(self))
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/models/query.py", line 53, in __iter__
    results = compiler.execute_sql(chunked_fetch=self.chunked_fetch, chunk_size=self.chunk_size)
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/models/sql/compiler.py", line 1154, in execute_sql
    cursor = self.connection.cursor()
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/utils/asyncio.py", line 26, in inner
    return func(*args, **kwargs)
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/backends/base/base.py", line 259, in cursor
    return self._cursor()
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/backends/base/base.py", line 237, in _cursor
    return self._prepare_cursor(self.create_cursor(name))
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/utils.py", line 90, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/backends/base/base.py", line 237, in _cursor
    return self._prepare_cursor(self.create_cursor(name))
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/utils/asyncio.py", line 26, in inner
    return func(*args, **kwargs)
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/backends/postgresql/base.py", line 236, in create_cursor
    cursor = self.connection.cursor()
django.db.utils.InterfaceError: connection already closed
>>> django.setup()
		
>>> from cat.models import *
		
>>> prov,_ = Providers.objects.get_or_create(name_provider='erc')
		
Traceback (most recent call last):
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/backends/base/base.py", line 237, in _cursor
    return self._prepare_cursor(self.create_cursor(name))
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/utils/asyncio.py", line 26, in inner
    return func(*args, **kwargs)
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/backends/postgresql/base.py", line 236, in create_cursor
    cursor = self.connection.cursor()
psycopg2.InterfaceError: connection already closed

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "<pyshell#278>", line 1, in <module>
    prov,_ = Providers.objects.get_or_create(name_provider='erc')
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/models/manager.py", line 85, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/models/query.py", line 573, in get_or_create
    return self.get(**kwargs), False
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/models/query.py", line 425, in get
    num = len(clone)
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/models/query.py", line 269, in __len__
    self._fetch_all()
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/models/query.py", line 1308, in _fetch_all
    self._result_cache = list(self._iterable_class(self))
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/models/query.py", line 53, in __iter__
    results = compiler.execute_sql(chunked_fetch=self.chunked_fetch, chunk_size=self.chunk_size)
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/models/sql/compiler.py", line 1154, in execute_sql
    cursor = self.connection.cursor()
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/utils/asyncio.py", line 26, in inner
    return func(*args, **kwargs)
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/backends/base/base.py", line 259, in cursor
    return self._cursor()
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/backends/base/base.py", line 237, in _cursor
    return self._prepare_cursor(self.create_cursor(name))
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/utils.py", line 90, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/backends/base/base.py", line 237, in _cursor
    return self._prepare_cursor(self.create_cursor(name))
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/utils/asyncio.py", line 26, in inner
    return func(*args, **kwargs)
  File "/home/aleksey1652/.local/lib/python3.6/site-packages/django/db/backends/postgresql/base.py", line 236, in create_cursor
    cursor = self.connection.cursor()
django.db.utils.InterfaceError: connection already closed
>>> 
