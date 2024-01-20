Python 3.9.5 (default, Nov 18 2021, 16:00:48) 
[GCC 10.3.0] on linux
Type "help", "copyright", "credits" or "license()" for more information.
>>> import re, json
>>> filename = '/home/alexey/alexapp/sereja/load_form_providers/brain-price.json'
>>> with open(filename, "r") as write_file:
                json_data=json.load(write_file)

                
>>> list_ = list(json_data.keys())
>>> list_[50:60]
['299', '305', '306', '310', '311', '312', '313', '314', '320', '321']
>>> json_data['299']
{'CategoryID': 7925, 'Code': 'L0002417', 'Group': 'Расходные материалы оригинальные', 'Article': 'Q7553X', 'Vendor': 'HP', 'Model': 'LJ    53X  2015', 'Name': 'Картридж HP LJ  53X 2015 (Q7553X)', 'Description': 'лазерный, оригинальный, Black, Совместимость - Hewlett Packard, 7000 стр', 'PriceUSD': 229, 'Price_ind': 0, 'CategoryName': 'Картриджи', 'Bonus': 0, 'RecommendedPrice': 0, 'DDP': 0, 'Warranty': 0, 'Stock': '0', 'Note': '', 'DayDelivery': '1', 'ProductID': 299, 'URL': 'https://opt.brain.com.ua/Kartridjh_HP_LJ_2015_Q7553X-p22831.html', 'UKTVED': '8443999090', 'GroupID': 1034, 'ClassID': 102, 'ClassName': 'Картридж', 'Available': 0, 'Country': 'Китай', 'RetailPrice': 8555, 'CostDelivery': 0, 'Exclusive': 0, 'FOP': 0}
>>> for data in json_data:
	if data['DayDelivery'] == 0:
		print(data)
		break

	
Traceback (most recent call last):
  File "/usr/lib/python3.9/idlelib/run.py", line 559, in runcode
    exec(code, self.locals)
  File "<pyshell#11>", line 2, in <module>
TypeError: string indices must be integers
>>> for data in json_data:
	if json_data[data]['DayDelivery'] == 0:
		print(data)
		break

	
>>> for data in json_data:
	if json_data[data]['DayDelivery'] == '0':
		print(data)
		break

	
50
>>> json_data['50']
{'CategoryID': 1361, 'Code': 'B0004280', 'Group': 'Накопители HDD - 3.5", 2.5", внутренние', 'Article': 'ST500DM002', 'Vendor': 'Seagate', 'Model': '3.5"   500Gb', 'Name': 'Жесткий диск 3.5"  500Gb Seagate (ST500DM002)', 'Description': '500 GB, 7200 об/мин, 16 MB, SATA III, Barracuda 7200.12, 10 Вт', 'PriceUSD': 23.29, 'Price_ind': 0, 'CategoryName': 'Жесткие диски (HDD)', 'Bonus': 0, 'RecommendedPrice': 0, 'DDP': 0, 'Warranty': 24, 'Stock': '1', 'Note': '', 'DayDelivery': '0', 'ProductID': 50, 'URL': 'https://opt.brain.com.ua/JHestkiy_disk_35_500Gb_Seagate_ST500DM002-p45692.html', 'UKTVED': '8471705000', 'GroupID': 1040, 'ClassID': 260, 'ClassName': 'Жесткий диск', 'Available': 3, 'Country': 'Сингапур', 'RetailPrice': 899, 'CostDelivery': 0, 'Exclusive': 0, 'FOP': 1}
>>> list_res = []
>>> for data in json_data:
	if json_data[data]['DayDelivery'] == '0':
		list_res.append(data)

		
>>> list_res

>>> list_res[50:60]
['1081', '1264', '1519', '1546', '1548', '1551', '1577', '1751', '1756', '1768']
>>> json_data['1081']
{'CategoryID': 1381, 'Code': 'B0003009', 'Group': 'Телефоны, факсы, АТС', 'Article': 'KX-TG1611UAH', 'Vendor': 'Panasonic', 'Model': 'KX-TG1611UAH', 'Name': 'Телефон DECT Panasonic KX-TG1611UAH', 'Description': 'черный, монохромный, матричный, с голубой подсветкой, полифония, 16-ти тональная, 12 мелодий, Автоопределитель номера, CallerID, нет, 50 номеров, набор на трубке, нет', 'PriceUSD': 32, 'Price_ind': 0, 'CategoryName': 'Телефоны беспроводные', 'Bonus': 0, 'RecommendedPrice': 0, 'DDP': 0, 'Warranty': 36, 'Stock': '1', 'Note': '', 'DayDelivery': '0', 'ProductID': 1081, 'URL': 'https://opt.brain.com.ua/Telefon_DECT_PANASONIC_KX-TG1611UAH-p43722.html', 'UKTVED': '8517110000', 'GroupID': 1053, 'ClassID': 189, 'ClassName': 'Телефон DECT', 'Available': 2, 'Country': 'Китай', 'RetailPrice': 1249, 'CostDelivery': 0, 'Exclusive': 0, 'FOP': 0}
>>> for data in json_data.values():
	print(data)
	break

{'CategoryID': 7273, 'Code': '10750', 'Group': 'Устройства бесперебойного питания', 'Article': 'BK500EI', 'Vendor': 'APC', 'Model': 'Back-UPS CS 500', 'Name': 'Источник бесперебойного питания Back-UPS CS 500 APC (BK500EI)', 'Description': 'для домашних ПК, резервный (off line), 300 Вт, 500 В*А, аппроксимированная (ступенчатая) синусоида, 180 до 260 В, 91х165х284, 6.4 кг', 'PriceUSD': 190, 'Price_ind': 0, 'CategoryName': 'Источники бесперебойного питания', 'Bonus': 0, 'RecommendedPrice': 0, 'DDP': 0, 'Warranty': 24, 'Stock': '0', 'Note': '', 'DayDelivery': '2', 'ProductID': 2, 'URL': 'https://opt.brain.com.ua/Istochnik_bespereboynogo_pitaniya_APC_Back-UPS_CS_500_BK500EI-p2906.html', 'UKTVED': '8504403000', 'GroupID': 1035, 'ClassID': 166, 'ClassName': 'Источник бесперебойного питания', 'Available': 0, 'Country': 'Индия', 'RetailPrice': 7129, 'CostDelivery': 0, 'Exclusive': 0, 'FOP': 0}
>>> 
>>> json_data['1768']
{'CategoryID': 1365, 'Code': 'U0002683', 'Group': 'Наушники, гарнитуры, микрофоны', 'Article': '31710151100', 'Vendor': 'Genius', 'Model': 'HS-200C', 'Name': 'Наушники Genius HS-200C (31710151100)', 'Description': 'VoIP телефония и колл-центры, проводное, Jack 3.5 мм, полузакрытые, 32 Ом, чувствительность - 105 дБ, 20  -  20000 Гц, с микрофоном, количество jack(ов) - 2, количество PIN (контактов) - 3, Black, 57 г', 'PriceUSD': 4.97, 'Price_ind': 0, 'CategoryName': 'Наушники и гарнитуры', 'Bonus': 0, 'RecommendedPrice': 0, 'DDP': 1, 'Warranty': 12, 'Stock': '1', 'Note': '', 'DayDelivery': '0', 'ProductID': 1768, 'URL': 'https://opt.brain.com.ua/Garnitura_Genius_HS-200C_31710151100-p63271.html', 'UKTVED': '8518300090', 'GroupID': 100064, 'ClassID': 157, 'ClassName': 'Наушники', 'Available': 2, 'Country': 'Китай', 'RetailPrice': 192, 'CostDelivery': 0, 'Exclusive': 0, 'FOP': 0}
>>> if 5 == 5 and\
   6 == 6:
	print('ok')

	
ok
>>> d = {}
>>> d[1] =2
>>> d
{1: 2}
>>> 5000/26500
0.18867924528301888
>>> class From_provders_filePrices:
    """ меняем цену в dict_ если дешевле при наличии
        set_parts - партнамберы периферии всех категорий """

    def __init__(self, set_parts, dict_):
        self.stock_price = stock_price
        self.dict_ = dict_

    def from_brain(self, filename):

        dict_sub = {
        'Акустические системы': '25',
        'Фильтры питания': '45',
        'Веб-камеры': '54',
        'Мониторы': '5',
        'Наушники, гарнитуры, микрофоны': '56'
        }

        try:
            with open(filename, "r") as write_file:
                json_data=json.load(write_file)
        except:
            return (False, 'no_file')

        if isinstance(json_data, dict):

            for data_json_data in json_data.values():
                try:
                    if data_json_data['Article'] in self.set_parts and\
                    data_json_data['DayDelivery'] in ('0', '1', '2', '3') and\
                    data_json_data['Group'] in dict_sub:
                        if dict_sub[data_json_data['Group']] in self.dict_:
                            if data_json_data['Article'] in self.dict_[
                            dict_sub[data_json_data['Group']]
                            ]:
                                if float(
                                data_json_data['PriceUSD']) < self.dict_[
                                dict_sub[
                                data_json_data['Group']]][data_json_data['Article']]['PriceUSD']:
                                    self.dict_[
                                    dict_sub[
                                    data_json_data['Group']]][data_json_data['Article']] = \
                                    {'PriceUSD': float(
                                    data_json_data['PriceUSD']),
                                    'provider': 'brain'}
                            else:
                                self.dict_[
                                dict_sub[data_json_data['Group']][data_json_data['Article']] =\
                                {'PriceUSD': float(
                                data_json_data['PriceUSD']),
                                'provider': 'brain'}
                        else:
                            self.dict_[dict_sub[data_json_data['Group']]] = {}
                            self.dict_[
                            dict_sub[data_json_data['Group']][data_json_data['Article']] =\
                            {'PriceUSD': float(
                            data_json_data['PriceUSD']),
                            'provider': 'brain'}
                except Exception as e:
                    return (False, e)

        else:
            return (False, 'json_data_no_dict')
			    
SyntaxError: invalid syntax
>>> class From_provders_filePrices:
    """ меняем цену в dict_ если дешевле при наличии
        set_parts - партнамберы периферии всех категорий """

    def __init__(self, set_parts, dict_):
        self.stock_price = stock_price
        self.dict_ = dict_

    def from_brain(self, filename):

        dict_sub = {
        'Акустические системы': '25',
        'Фильтры питания': '45',
        'Веб-камеры': '54',
        'Мониторы': '5',
        'Наушники, гарнитуры, микрофоны': '56'
        }

        try:
            with open(filename, "r") as write_file:
                json_data=json.load(write_file)
        except:
            return (False, 'no_file')

        if isinstance(json_data, dict):

            for data_json_data in json_data.values():
                try:
                    if data_json_data['Article'] in self.set_parts and\
                    data_json_data['DayDelivery'] in ('0', '1', '2', '3') and\
                    data_json_data['Group'] in dict_sub:
                        if dict_sub[data_json_data['Group']] in self.dict_:
                            if data_json_data['Article'] in self.dict_[
                            dict_sub[data_json_data['Group']]
                            ]:
                                if float(
                                data_json_data['PriceUSD']) < self.dict_[
                                dict_sub[
                                data_json_data['Group']]][data_json_data['Article']]['PriceUSD']:
                                    self.dict_[
                                    dict_sub[
                                    data_json_data['Group']]][data_json_data['Article']] = \
                                    {'PriceUSD': float(
                                    data_json_data['PriceUSD']),
                                    'provider': 'brain'}
                            else:
                                self.dict_[
                                dict_sub[data_json_data['Group']]][data_json_data['Article']] =\
                                {'PriceUSD': float(
                                data_json_data['PriceUSD']),
                                'provider': 'brain'}
                        else:
                            self.dict_[dict_sub[data_json_data['Group']]] = {}
                            self.dict_[
                            dict_sub[data_json_data['Group']]][data_json_data['Article']] =\
                            {'PriceUSD': float(
                            data_json_data['PriceUSD']),
                            'provider': 'brain'}
                except Exception as e:
                    return (False, e)

        else:
            return (False, 'json_data_no_dict')

        
>>> f = From_provders_filePrices(set(), {})
Traceback (most recent call last):
  File "/usr/lib/python3.9/idlelib/run.py", line 559, in runcode
    exec(code, self.locals)
  File "<pyshell#40>", line 1, in <module>
  File "<pyshell#39>", line 6, in __init__
NameError: name 'stock_price' is not defined
>>> class From_provders_filePrices:
    """ меняем цену в dict_ если дешевле при наличии
        set_parts - партнамберы периферии всех категорий """

    def __init__(self, set_parts, dict_):
        self.set_parts = set_parts
        self.dict_ = dict_

    def from_brain(self, filename):

        dict_sub = {
        'Акустические системы': '25',
        'Фильтры питания': '45',
        'Веб-камеры': '54',
        'Мониторы': '5',
        'Наушники, гарнитуры, микрофоны': '56'
        }

        try:
            with open(filename, "r") as write_file:
                json_data=json.load(write_file)
        except:
            return (False, 'no_file')

        if isinstance(json_data, dict):

            for data_json_data in json_data.values():
                try:
                    if data_json_data['Article'] in self.set_parts and\
                    data_json_data['DayDelivery'] in ('0', '1', '2', '3') and\
                    data_json_data['Group'] in dict_sub:
                        if dict_sub[data_json_data['Group']] in self.dict_:
                            if data_json_data['Article'] in self.dict_[
                            dict_sub[data_json_data['Group']]
                            ]:
                                if float(
                                data_json_data['PriceUSD']) < self.dict_[
                                dict_sub[
                                data_json_data['Group']]][data_json_data['Article']]['PriceUSD']:
                                    self.dict_[
                                    dict_sub[
                                    data_json_data['Group']]][data_json_data['Article']] = \
                                    {'PriceUSD': float(
                                    data_json_data['PriceUSD']),
                                    'provider': 'brain'}
                            else:
                                self.dict_[
                                dict_sub[data_json_data['Group']]][data_json_data['Article']] =\
                                {'PriceUSD': float(
                                data_json_data['PriceUSD']),
                                'provider': 'brain'}
                        else:
                            self.dict_[dict_sub[data_json_data['Group']]] = {}
                            self.dict_[
                            dict_sub[data_json_data['Group']]][data_json_data['Article']] =\
                            {'PriceUSD': float(
                            data_json_data['PriceUSD']),
                            'provider': 'brain'}
                except Exception as e:
                    return (False, e)

        else:
            return (False, 'json_data_no_dict')

        
>>> f = From_provders_filePrices(set(), {})
>>> set_mon = set()
>>> for data in json_data:
	if json_data[data]['Group'] == 'Мониторы':
		print(data)
		set_mon.add(json_data[data]['Article'])

		
159727
184490
199847
212415
219647
227300
255738
261584
261586
264981
267847
267848
271091
280807
280808
280813
283500
283503
283505
283511
283865
283866
291960
291966
294367
301442
313192
315031
315032
319306
319441
319448
322782
532778
534152
534158
543453
544304
545806
545807
546757
549999
550002
553400
556315
559997
563119
563126
563127
565255
565275
565277
565284
566176
566186
570092
573067
576864
577126
578651
578652
578653
587256
589960
593221
594530
594534
594535
594536
594538
596652
597846
601260
603935
604997
606668
607218
607220
607221
609788
609797
610122
611786
612184
612186
612189
614164
617868
635497
635498
638143
638144
638293
641864
644185
644186
644195
644197
647448
650016
650019
650022
650781
654293
655119
659141
659142
659143
659148
660482
660483
665700
665967
665969
665970
667469
670182
670183
670185
670187
670188
670191
670193
670194
670197
670200
670423
670554
670556
670560
670561
671543
671544
671545
674579
676651
681415
682753
683182
683185
687709
687710
687711
688694
688697
688699
688700
688701
688703
688983
688984
693610
693611
699872
701279
702895
702896
702897
717988
717989
717991
717995
718020
718021
718025
718026
722787
722789
723085
723091
723092
723095
725846
725847
726880
733784
733785
733786
733788
733789
733792
733795
733796
733797
733822
733824
733825
734667
734677
734684
734687
734688
734690
734691
734695
734696
734698
748393
749222
749223
749224
749230
750971
751855
751857
751858
751863
751868
100001327
100001328
100001329
100068681
100068682
100072675
100072676
100072682
100072684
100072686
100072687
100072693
100072694
100073582
100074008
100074010
100074014
100074015
100074016
100074596
100075600
100075601
100087102
100087110
100087113
100088716
100094218
100094220
100094227
100094228
100094229
100094234
100094239
100094243
100094245
100094246
100094739
100094740
100094896
100095246
100095247
100098767
100099515
100100404
100101214
100101376
100101377
100102556
100102558
100104795
100104796
100104798
100104800
100104803
100104805
100104807
100104811
100106921
100106924
100106930
100106931
100106933
100108671
100108673
100108674
100108944
100110602
100110847
100111553
100111943
100126307
100126308
100126311
100126314
100126783
100126784
100126787
100126789
100129404
100129406
100129409
100129410
100129411
100129415
100129417
100138107
100138114
100138116
100138117
100138118
100138120
100140308
100140311
100140313
100141088
100141089
100141608
100141609
100141612
100149381
100149383
100149390
100150599
100150600
100150601
100150604
100150605
100150606
100150607
100150608
100161663
100173824
100177650
100182874
100182875
100183121
100188642
100189945
100189946
100199331
100199333
100199334
100199340
100202183
100202645
100202646
100202647
100202648
100202649
100202650
100203970
100205039
100205040
100205352
100205353
100205354
100206368
100206369
100207328
100207329
100207330
100207331
100207332
100207333
100207334
100207335
100207338
100207340
100207341
100207342
100207343
100208198
100208199
100208204
100210082
100217524
100217526
100217527
100217528
100217529
100217531
100223116
100225577
100227550
100227698
100231726
100231727
100231729
100232790
100232803
100232805
100232809
100232813
100232815
100232816
100232821
100232822
100232826
100232827
100232829
100232830
100232831
100233021
100233022
100233023
100233024
100233025
100233028
100235707
100235708
100236097
100236098
100236099
100236100
100236101
100236836
100236837
100237492
100242714
100242715
100246428
100246430
100246431
100246432
100246433
100246434
100246435
100246436
100246437
100246438
100246439
100247024
100247031
100247032
100247033
100247037
100257905
100259954
100260408
100260409
100260410
100260411
100260413
100260414
100261180
100261181
100261182
100261184
100261186
100261187
100261189
100261190
100261192
100261193
100261194
100268172
100274648
100274649
100274651
100274653
100278518
100278519
100278520
100281995
100281998
100281999
100282000
100282007
100282009
100282010
100282011
100282015
100282019
100282022
100282024
100282025
100282028
100282029
100282031
100287759
100288232
100288233
100288234
100289788
100289789
100291314
100291315
100291316
100291317
100291319
100291321
100291322
100291323
100291659
100291661
100292811
100294615
100294616
100294618
100294620
100297707
100297708
100297709
100299619
100299620
100300845
100300846
100301555
100303013
100303318
100303319
100303321
100303322
100303324
100303325
100303328
100303329
100303330
100303331
100303332
100303333
100303334
100303336
100303337
100303338
100304071
100304072
100304073
100304074
100304075
100304076
100304812
100304813
100304814
100304815
100304817
100304821
100304822
100309381
100310472
100310473
100310474
100310475
100312134
100312135
100312995
100312996
100312997
100312998
100312999
100313000
100313001
100313003
100313004
100313531
100313532
100313533
100315416
100316326
100316327
100316329
100316330
100316331
100316332
100318529
100318530
100318531
100319539
100319540
100319541
>>> set_mon
{'ProArt PA248CRV', '9H.LLHLA.TBE', 'BL2780T Black', '32H02AA', '242S1AE/00', 'CU34P3CV', 'XUB2796QSU-B5', '2E-F2723B-01.UA', '222B1TC/00', 'G32QC A Gaming Monitor', 'XUB2792HSN-B5', 'DR-22G', '242B1TC/00', '34WN780-B', '61E9GAT6UA', 'M34WQ-EK', 'GB3461WQSU-B1', 'E1980D-B1', '9H.LKNLB.QBE', '210-AKBD', 'LF24T450FQIXCI', 'C24G2AE/BK', 'UM.HX3EE.005', 'LS24C360EAIXCI', '221V8LD/00', '498P9/00', '27E3UM', '242E2FA/00', 'UM.KX0EE.006', '27E1N8900/00', '210-BDRJ', '272E2FA/00', '24BK55YP-I', 'VS18190', '61DAMAT1UA', '273V7QDSB/00', '9H.LKSLB.QBE', 'EW3280U Metallic Brown-Black', 'VX2718-P-MHD', '27QN600-B', 'ROG Strix XG259CM', '62B9MAT4UA', 'Q32V5CE/BK', 'Q2790PQE', '32UN650-W', '24MP60G-B', 'CQ32G2SE/BK', '62A9GAT1UA', 'VA24EHE', '27G2SAE/BK', '210-BDXS', '223V5LHSB2/00', 'X2283HSU-B1', 'CU34P2C', 'G2250HS-B1', 'PA328QV', 'PA328CGV', '345B1C/00', 'T2455MSC-B1', 'EW2780U Brown-Black', 'U34G3XM/EU', '9H.LJXLA.TBE', '243V7QJABF/00', 'MD271P', '34M1C5500VA/00', '346P1CRH/00', '245E1S/00', '2E-E2020B-01.UA', 'OPTIX G321CQP', '210-AVBF', '450M5AA', '32UN880-B', '241E1SCA/00', '2E-G2723B-01.UA', '242V8LA/00', '27B2DM', '66D1GAC1UA', '2E-G3022B-01.UA', '2E-G3422B-01.UA', 'LS27A600UUIXCI', 'Q27B3MA', 'TUF Gaming VG279QM1A', '32GN550-B', '221V8/00', 'FI32U', 'VA3209-MH', 'VG279QL1A', 'GW2283', 'PRO MP243', 'VP229HE', '9H.LLALJ.LBE', '210-AYUK', 'LS32A600NWIXCI', 'T2252MSC-B1', '66E5GAC3UA', 'VY279HE', 'LS27AG300NIXCI', '27GN60R-B', 'UM.WV7EE.H11', 'E243F Black', 'TUF Gaming VG27AQML1A', 'Z4W65A4', '241E2FD/00', '27MP60GP-B', '24P3CW', 'LF22T350FHIXCI', 'GW2480 Black', 'VP32UQ', '345E2AE/00', 'Modern MD241PW', '9H.LKPLB.QBE', 'GW2780 Black', 'Q27V5N/BK', 'Q27V5C/BK', 'XUB2492HSN-B5', 'TUF Gaming VG289Q1A', 'VA27DCP', 'ZenScreen Ink MB14AHD', '2E-G2723BV-01.UA', '9H.LJMLB.QBE', 'UM.WE0EE.301', 'Q27E3UAM', '27G2SU/BK', 'XUB2792QSU-W5', '24B1U5301H/00', '272S1MH/00', '325E1C/00', '27B2DA', 'XUB2893UHSU-B5', '210-BBSK', 'VP228DE', 'SC-24E', '62CEGAT3UA', 'AG493QCX', 'VP247HAE', 'ROG Strix XG49WCR', '2E-L2820B-01.UA', '272S1AE/00', 'LU28R550UQIXCI', '210-BBRR', '242S9JML/00', 'U32P2', 'UM.WV6EE.037', 'T2435MSC-B2', '24MP400P-B', 'VZ239HE-W', 'PA278QV', '32G13AA', 'VA24EQSB', '29WP500-B', '62A3UAT1WL', '24MP450-B', 'ZenScreen MB166B', '9H.LJRLA.TPE', '27UL500-W', 'T2336MSC-B2', 'TUF Gaming VG32UQA1A', '6N6E9AA', '2E-E2723B-01.UA', '22MK430H-B', '459J9AA', 'XUB2492HSC-B1', '279P1/00', 'M32UC-EK', '27V5CE/BK', '66EEGAC3UA', 'E273F white', 'MB16AP', 'ROG Swift PG27AQN', 'LC24RG50FZIXCI', 'C27G2ZE/BK', 'LS27C360EAIXCI', '26WQ500-B', '243B1/00', 'GW2480T Black', 'LC27G55TQBIXCI', 'G281UV', '9H.LK4LA.TBE', 'PA247CV', 'EW3270U Metallic Grey', 'LS32BG650EIXUA', '24V5C/BK', '67A2KAC6UA', 'MPG ARTYMIS 323CQR', '2E-D2621W-01.UA', '61F5GAT1UA', '62AEKAT2UA', '32M1C5500VL/00', '325B1L/00', '210-BFWN', 'XUB3294QSU-B1', '34M2C7600MV/00', '24GQ50F-B', '27G2U5/BK', '24MP400-B', '220V8/01', 'OPTIX MAG342CQR', '24P3CV', 'PD3200U Grey', 'UM.QX2EE.E05', '29WQ600-W', 'XU2792HSU-B1', '90LM06P1-B01170', 'Q34E2A', 'PRO MP241X', 'Modern MD271CP', 'VY279HE-W', '288E2UAE/00', '27MP400-B', '271V8LA/00', '2E-B2423B-01.UA', '210-BDEG', '6N4E2AA', 'MB16AMT', '2E-E2423B-01.UA', '241E1SC/00', '90LM05A0-B02370', 'UM.HX2EE.F01', '275S1AE/00', 'X4373UHSU-B1', 'XU3294QSU-B1', '34WP550-B', 'VA34VCPSN', '24B2XHM2', '210-AZZH', 'MPG ARTYMIS 273CQR QD', '273V7QDAB/00', '64X66AA', 'TX-19', '34WK95U-W', 'VS18554', '210-BGPJ', '210-AXKR', '27E1N5300AE/00', '242V8A/00', '210-AXKQ', '27M1N3500LS/00', 'AG273QXP', 'XUB2792QSU-B5', '27P1/GR', '2E-G2422B-01.UA', '24B2XD', '243V7QDAB/00', '61F1GAT2UA', '27MP60G-B', '9H.LKYLJ.TPE', 'BL2581T Black', 'LS27C310EAIXCI', '210-BBBF', '272S1M/00', '210-AZZB', '275E1S/00', 'PD2705Q', '60004650', '61DDUAT6UA', '276C8/00', '9H.LH4LB.QPE', 'LS27A700NWIXCI', '24E1N5300AE/00', 'BHR4975EU', 'BL2420PT', '34B1U5600CH/00', '210-BDZZ', 'G321CUV', 'GB2770HSU-B5', 'ProArt PA148CTV', 'VX2418C', '322E1C/00', '9H.LHTLB.QPE', 'VG27VQ', '62DDGAT6UA', 'T2454MSC-B1AG', '27M1N5200PA/00', '453D2AA', '329M1RV/00', 'XB3270QS-B5', '242B1TFL/00', '32GN50R-B', '222B1TFL/00', '62B1GAT2UA', '25M2N3200W/00', '34WQ60C-B', '2E-G2721B-01.UA', 'LS24C310EAIXCI', 'ProArt PA348CGV', '221V8A/00', '9TT53AA', 'VG249Q1A', '210-BGQG', 'U32U1', '273V7QJAB/00', '210-AXKW', 'VS18453', 'VP289Q', '24V5CE/BK', 'PRO MP273', '45B1U6900C/00', 'TUF Gaming VG32VQR', '24P2C', '276B9H/00', '2E-G2423B-01.UA', '210-BDDX', '32QN600-B', '32MN500M-B', '24B2XDM', '210-AZKU-08', 'XG309CM', 'U28P2A', 'OCULUX NXG253R', 'AG274QXM', 'U27P2', '22MP410P-B', '328B1/00', '24M1N3200VS/00', 'CU34V5C/BK', '9H.LJNLB.QBE', 'SE2222H-08', 'Q27V5CW/BK', 'LS34BG850SIXUA', '272V8LA/00', 'XUB2595WSU-B1', '24MK430H-B', 'VA3209-2K-MHD', 'RX-22G WHITE', 'XU2792QSU-B1', 'LS49AG950NIXCI', 'VG289Q', '162B9T/00', '243V7QDSB/00', 'Q24P2Q', '27M1F5500P/00', '499P9H/00', 'TM-22', 'Optix MEG381CQR Plus', '241V8LA/00', 'LS27BG650EIXUA', '210-BEQZ', '328E1CA/00', '24B2XDA', 'LS49CG954SIXUA', '9H.LHALB.QBE/LHVLB.QPE', '66BDKAC2UA', '276E8VJSB/00', 'Q24V4EA', '210-AZYX', '22MP410-B', '24M1N3200VA/00', '64W41AA', 'I1659FWUX', 'VG28UQL1A', '42M2N8900/00', '273B9/00', 'GL2480 Black', '27QN880-B', 'ROG Swift PG42UQ', '27GN800-B', '9H.LL6LB.QBE', 'LS24R650FDIXCI', 'Q32P2CA', '62A8KAT1UA', 'M32QC-EK', 'FO48U', 'AG275QX/EU', 'MPG Artymis 273CQRX-QD', '6N4D0AA', '222V8LA/00', '346E2CUAE/00', 'M28U', 'G24F 2Gaming Monitor', '24M1N3200ZA/00', '210-BFIS', 'VA2406-H', '242S9JAL/00', 'CQ27G2U/BK', 'U34E2M', 'VX2718-2KPC-MHD', '210-BDFZ', 'PD3200Q Black', 'AG325QZN/EU', '45B1U6900CH/00', '210-AZGT', '32GQ850-B', '210-BDSL', 'VG32AQA1A', '210-BBRQ', 'E2270SWHN', 'GB2590HSU-B1', 'LS27A800UNIXCI', 'XU2294HSU-B2', 'PD2700U Grey', '245B1/00', 'ZenScreen MQ16AH', '210-BDFS', 'GB2470HSU-B5', 'UM.QV7EE.E03', 'UM.SE1EE.S01', '210-BDGB', '346B1C/00', '27P2C', '243S7EYMB/00', '210-AYUL', '326P1H/00', '62AFKAT2/62AFKAR2', '271E1CA/00', 'TUF Gaming VG249QM1A', 'CU34V5CW/BK', '222B9T/00', '27V5C/BK', '27UP650-W', 'Q32E2N', 'VZ249HE', '271V8L/00', 'TUF Gaming VG34VQEL1A', '24P3QW', '62AAKAT6UA', '24B2XH/EU', 'UM.QR0EE.015', '27E1N3300A/00', 'GB2766HSU-B1', 'U2790PQU', '25M2N5200P/00', 'MS321UP', '66F2GAC1UA', 'ZenScreen MB166C', '62CFGAT1UA', 'VZ279HE', 'GW2475H', 'LC27R500FHIXCI', 'B1980D-B1', '210-AZKS', '210-AZKU-LCPHF21', '66C9UAC1UA', 'MB16AHP', '210-BEJD-2209BRN', 'VP349CGL', 'G2766HSU-B1', 'VZ279HE-W', '272V8A/00', 'GB2770QSU-B5', 'ProArt PA279CV', 'QM-5502', 'M32U', '32GN650-B', 'XU2493HS-B5', '275E2FAE/00', 'XUB2294HSU-W2', '62DCRAT3UA', 'VA2715-H', 'ZenScreen GO MB16AWP', 'PD2500Q Grey', 'U32P2CA', '242E1GAJ/00', '9H.LJPLB.QBE', '63A5GAT6UA', 'GB2790QSU-B1', 'LC32G55TQBIXCI', 'ROG Strix XG27AQMR', 'VA2715-2K-MHD', 'XUB2793QS-B1', 'ZenScreen MQ13AH', '34WP500-B', '242B1H/00', '62C5GAT1UA', 'XG49VQ', 'ZenScreen MB16ACV', 'T2254MSC-B1AG', '24P2Q', 'AG254FG', 'LS24AG300NIXCI', '9H.LKDLA.TBE', 'VT229H', '66BEKAC2UA', '498P9Z/00', '24G2SAE/BK', 'T1721MSC-B1', 'U27V4EA', 'C32G2ZE/BK', '66CFGAC1UA', '210-BEJD', 'U32E2N', '24B1H', '60004303', 'SW240', '3B1W4AA', '27M1C3200VL/00', '27M1C5500VL/00', 'C32G3AE/BK', '62F9GAT4UA', '27E1N5500LA/00', 'RX-24G', '27E1N5600AE/00', '172B9TL/00', 'VP228HE', '27GP850-B', '5ZP65AA', '210-AZGT-EC', '242E1GAEZ/00', 'VG32AQL1A', 'Q27P2Q', 'ROG Strix XG349C', '2E-G3223B-01.UA', 'QM-4302', '64X69AA', '20MK400H-B', '27P2Q', 'ROG Strix XG32VC', '21Y56AA', '288E2A/00', 'X-17E BLACK', '35WN75C-B', '278B1/00', 'T2754MSC-B1AG', '61EDGAT2UA', '27M1N3200ZA/00', '6N4F1AA', '9H.LKGLA.TBE', '27UP850N-W', '9SV94AA', '32MP60G-B', '24E1N3300A/00', '24V5CW/BK', '327E8QJAB/00', '27G2SPU/BK', '210-BEGY', '278E1A/00', '34E1C5600HE/00', 'VG32VQR', '210-AZYZ', 'UM.QV0EE.H01', 'EA245WMi-2 Black', '210-AXLE', 'FI32Q-X-EK', 'Q27P2CA', '32M1N5800A/00', 'XU2492HSU-B1', '210-AXKZ', 'LS32BG700EIXUA', 'XUB2792UHSU-B1', '1TJ76AA', '241V8L/00', '210-BFIM', '6N6E6AA', 'LS28BG700EIXUA', 'VS18312', 'Optix MPG341QR', '272E1CA/00', '33K31AA', '2E-F2422B-01.UA', '27B2AM', '66EFGAC3UA', 'EA245WMi-2 White', 'VZ24EHE', 'AG274QZM', '210-BBSJ', 'LS32CM801UIXUA', '27M1F5800/00', 'Q27T1', '32UL950-W'}
>>> f = From_provders_filePrices(set_mon, {})
>>> dict_ = dict()
>>> f = From_provders_filePrices(set_mon, dict_)
>>> f.from_brain('/home/alexey/alexapp/sereja/load_form_providers/brain-price.json')
>>> dict_

>>> dict_.keys()
dict_keys(['5'])
>>> val = list(dict_['5'].values())
>>> val[:10]
[{'PriceUSD': 370.0, 'provider': 'brain'}, {'PriceUSD': 600.0, 'provider': 'brain'}, {'PriceUSD': 236.0, 'provider': 'brain'}, {'PriceUSD': 368.0, 'provider': 'brain'}, {'PriceUSD': 107.0, 'provider': 'brain'}, {'PriceUSD': 97.9, 'provider': 'brain'}, {'PriceUSD': 382.0, 'provider': 'brain'}, {'PriceUSD': 134.0, 'provider': 'brain'}, {'PriceUSD': 101.0, 'provider': 'brain'}, {'PriceUSD': 412.0, 'provider': 'brain'}]
>>> dict_['5']['VZ24EHE']
{'PriceUSD': 130.0, 'provider': 'brain'}
>>> f = From_provders_filePrices(set_mon, dict_)
>>> f.from_brain('/home/alexey/alexapp/sereja/load_form_providers/brain-price.json')
>>> dict_['5']['VZ24EHE']
{'PriceUSD': 130.0, 'provider': 'brain'}
>>> class From_provders_filePrices:
    """ меняем цену в dict_ если дешевле при наличии
        set_parts - партнамберы периферии всех? категорий """

    def __init__(self, set_parts, dict_):
        self.set_parts = set_parts
        self.dict_ = dict_

    def from_brain(self, filename):
        # из скачанного файла brain меняем dict_

        __count_new, __count_update = 0, 0
        # __count_new, __count_update - счетчики добавлений в dict_ и замены

        dict_sub = {
        'Акустические системы': '25',
        'Фильтры питания': '45',
        'Веб-камеры': '54',
        'Мониторы': '5',
        'Наушники, гарнитуры, микрофоны': '56'
        }
        # категории brain в dict_ категории

        try:
            with open(filename, "r") as write_file:
                json_data=json.load(write_file)
        except:
            return (False, {'__count_new': __count_new,
                    '__count_update': __count_update,
                    'status': 'no_file'})

        if isinstance(json_data, dict):

            for data_json_data in json_data.values():
                try:
                    if data_json_data['Article'] in self.set_parts and\
                    data_json_data['DayDelivery'] in ('0', '1', '2', '3') and\
                    data_json_data['Group'] in dict_sub:
                        # если партнамбер-brain есть в set_parts и наличие тру
                        # и категория-brain есть в dict_sub
                        if dict_sub[data_json_data['Group']] in self.dict_:
                            # если категория-brain в dict_
                            if data_json_data['Article'] in self.dict_[
                            dict_sub[data_json_data['Group']]
                            ]:
                                # если партнамбер уже существует и цена ниже - меняем в dict_
                                if float(
                                data_json_data['PriceUSD']) < self.dict_[
                                dict_sub[
                                data_json_data['Group']]][data_json_data['Article']]['PriceUSD']:
                                    self.dict_[
                                    dict_sub[
                                    data_json_data['Group']]][data_json_data['Article']] = \
                                    {'PriceUSD': float(
                                    data_json_data['PriceUSD']),
                                    'provider': 'brain'}
                                    __count_update += 1
                            else:
                                # если партнамбера нет - записываем в dict_
                                self.dict_[
                                dict_sub[data_json_data['Group']]][data_json_data['Article']] =\
                                {'PriceUSD': float(
                                data_json_data['PriceUSD']),
                                'provider': 'brain'}
                                __count_new += 1
                        else:
                            # если категория-brain нет dict_ - создаем кат и записываем нов об-т
                            self.dict_[dict_sub[data_json_data['Group']]] = {}
                            self.dict_[
                            dict_sub[data_json_data['Group']]][data_json_data['Article']] =\
                            {'PriceUSD': float(
                            data_json_data['PriceUSD']),
                            'provider': 'brain'}
                            __count_new += 1
                    return (True, {'__count_new': __count_new,
                            '__count_update': __count_update,
                            'status': 'ok'})
                except Exception as e:
                    return (False, {'__count_new': __count_new,
                            '__count_update': __count_update,
                            'status': e})

        else:
            return (False, {'__count_new': __count_new,
                    '__count_update': __count_update,
                    'status': 'json_data_no_dict'})

        
>>> f = From_provders_filePrices(set_mon, dict_)
>>> f.from_brain('/home/alexey/alexapp/sereja/load_form_providers/brain-price.json')
(True, {'__count_new': 0, '__count_update': 0, 'status': 'ok'})
>>> dict_ = dict()
>>> f = From_provders_filePrices(set_mon, dict_)
>>> f.from_brain('/home/alexey/alexapp/sereja/load_form_providers/brain-price.json')
(True, {'__count_new': 0, '__count_update': 0, 'status': 'ok'})
>>> dict_
{}
>>> class From_provders_filePrices:
    """ меняем цену в dict_ если дешевле при наличии
        set_parts - партнамберы периферии всех? категорий """

    def __init__(self, set_parts, dict_):
        self.set_parts = set_parts
        self.dict_ = dict_

    def from_brain(self, filename):
        # из скачанного файла brain меняем dict_

        __count_new, __count_update = 0, 0
        # __count_new, __count_update - счетчики добавлений в dict_ и замены

        dict_sub = {
        'Акустические системы': '25',
        'Фильтры питания': '45',
        'Веб-камеры': '54',
        'Мониторы': '5',
        'Наушники, гарнитуры, микрофоны': '56'
        }
        # категории brain в dict_ категории

        try:
            with open(filename, "r") as write_file:
                json_data=json.load(write_file)
        except:
            return (False, {'count_new': __count_new,
                    'count_update': __count_update,
                    'status': 'no_file'})

        if isinstance(json_data, dict):

            for data_json_data in json_data.values():
                try:
                    if data_json_data['Article'] in self.set_parts and\
                    data_json_data['DayDelivery'] in ('0', '1', '2', '3') and\
                    data_json_data['Group'] in dict_sub:
                        # если партнамбер-brain есть в set_parts и наличие тру
                        # и категория-brain есть в dict_sub
                        if dict_sub[data_json_data['Group']] in self.dict_:
                            # если категория-brain в dict_
                            if data_json_data['Article'] in self.dict_[
                            dict_sub[data_json_data['Group']]
                            ]:
                                # если партнамбер уже существует и цена ниже - меняем в dict_
                                if float(
                                data_json_data['PriceUSD']) < self.dict_[
                                dict_sub[
                                data_json_data['Group']]][data_json_data['Article']]['PriceUSD']:
                                    self.dict_[
                                    dict_sub[
                                    data_json_data['Group']]][data_json_data['Article']] = \
                                    {'PriceUSD': float(
                                    data_json_data['PriceUSD']),
                                    'provider': 'brain'}
                                    __count_update += 1
                            else:
                                # если партнамбера нет - записываем в dict_
                                self.dict_[
                                dict_sub[data_json_data['Group']]][data_json_data['Article']] =\
                                {'PriceUSD': float(
                                data_json_data['PriceUSD']),
                                'provider': 'brain'}
                                __count_new += 1
                        else:
                            # если категория-brain нет dict_ - создаем кат и записываем нов об-т
                            self.dict_[dict_sub[data_json_data['Group']]] = {}
                            self.dict_[
                            dict_sub[data_json_data['Group']]][data_json_data['Article']] =\
                            {'PriceUSD': float(
                            data_json_data['PriceUSD']),
                            'provider': 'brain'}
                            __count_new += 1
                except Exception as e:
                    return (False, {'count_new': __count_new,
                            'count_update': __count_update,
                            'status': e})

            return (True, {'count_new': __count_new,
                    'count_update': __count_update,
                    'status': 'ok'})

        else:
            return (False, {'count_new': __count_new,
                    'count_update': __count_update,
                    'status': 'json_data_no_dict'})

        
>>> f = From_provders_filePrices(set_mon, dict_)
>>> f.from_brain('/home/alexey/alexapp/sereja/load_form_providers/brain-price.json')
(True, {'count_new': 519, 'count_update': 0, 'status': 'ok'})
>>> len(set_mon)
558
>>> f = From_provders_filePrices(set_mon, dict_)
>>> f.from_brain('/home/alexey/alexapp/sereja/load_form_providers/brain-price.json')
(True, {'count_new': 0, 'count_update': 0, 'status': 'ok'})
>>> dict_['5']['VZ24EHE']
{'PriceUSD': 130.0, 'provider': 'brain'}
>>> EDG_TOKEN = '0e8a27f168b41bbfedff6d77e7db65f0'
>>> price_url = f'http://b2b.dako.ua/price_server.php?token={EDG_TOKEN}'
>>> r = requests.get(price_url, timeout=30)
Traceback (most recent call last):
  File "/usr/lib/python3.9/idlelib/run.py", line 559, in runcode
    exec(code, self.locals)
  File "<pyshell#79>", line 1, in <module>
NameError: name 'requests' is not defined
>>> import requests
>>> r = requests.get(price_url, timeout=30)
>>> r.status_code
200
>>> res = r.content
>>> from lxml import etree
>>> root = etree.fromstring(xml)
Traceback (most recent call last):
  File "/usr/lib/python3.9/idlelib/run.py", line 559, in runcode
    exec(code, self.locals)
  File "<pyshell#85>", line 1, in <module>
NameError: name 'xml' is not defined
>>> root = etree.fromstring(res)
>>> result_data = root.find('items').findall('item')
>>> set_category = set()
>>> for x in result_data:
	for k in x.getchildren():
		if k.tag == 'Subcategory':
			set_category.add(k.tag)

			
>>> set_category
{'Subcategory'}
>>> set_category = set()
>>> for x in result_data:
	for k in x.getchildren():
		if k.tag == 'Subcategory':
			set_category.add(k.text)

			
>>> set_category
{'LED стрічки', 'Мобільні аксесуари', 'Картридери внутрішні', 'Миші', 'Адаптери та перехідники', 'HDMI/VGA/DVI/USB пристрої', 'Геймпад, кермо, джойстик', 'Електроінструмент акумуляторний', 'HDMI, DVI, VGA', 'Блоки живлення, зарядні пристрої', 'Електросамокати', 'Стабілізатори', 'Блоки живлення ATX', 'Навушники та мікрофони', 'Патч-панелі', 'LED лампи', 'Ручний інструмент', 'Філамент для 3D', 'Подовжувачі та колодки', '3D принтери', 'Електромонтажне обладнання', 'Зарядні пристрої', 'Геймерські крісла', 'Конвертери/грабери', 'Клавіатури', 'Кухонне приладдя', 'Аксесуари', 'Підставки для ноутбуків', 'Зварювальні апарати', 'Акустичні системи', 'Рюкзаки та сумки', 'Сувенірна продукція', 'Внутрішні кишені', 'Аксесуари та запчастини', 'Вимірювальні інструменти', 'Електровелосипеди', 'Комплекти (клавіатура+миша)', 'Ігрові столи', 'Мережеві фільтри', 'Патч-корди', 'Рюкзаки та сумки для туризму', 'Універсальні акумулятори', 'Активне мережеве обладнання', 'Сумки та чохли для фотоапаратів', 'Одяг', 'Мийки високого тиску', 'Чистячі засоби', 'Килимки', 'Електроскутери', 'Термоси та термокухлі', 'Системи охолодження, Cooler', 'Паяльне обладнання', 'Аудіо/відео кабелі', 'Електроінструмент', 'Кабелі живлення', 'Зовнішні кишені для HDD', 'Адаптери USB', 'Сковорідки', 'Різне (eSATA, Firewire)', 'Різне', 'Сумки-холодильники', 'Елементи живлення', 'LED аксесуари', 'Плати розширення PCI, PCI-E, IDE-SATA та ін.', 'Док-станції/хаби/картридери', 'Головні убори', 'Зарядні станції', 'Вебкамери', 'Тримачі та підставки', 'Кронштейни для TV', 'Презентери', 'Інвертори', 'Компресори', 'Серверні шафи та аксесуари', 'Корпуси', 'Каструлі', 'Внутрішні кабелі', 'Мережеві кабелі', 'Інструменти', 'Пилососи', 'ДБЖ (UPS)', 'Акумуляторні батареї', 'Кабелі/перехідники USB'}
>>> set_status = set()
>>> for x in result_data:
	for k in x.getchildren():
		if k.tag == 'StockName':
			set_status.add(k.text)

			
>>> set_status
{'Очікується', 'Нет в наличии', 'Закінчується', 'Немає в наявності', 'Зарезервовано', 'В наявності'}
>>> class From_provders_filePrices:
    """ меняем цену в dict_ если дешевле при наличии
        set_parts - партнамберы периферии всех? категорий """

    def __init__(self, set_parts, dict_):
        self.set_parts = set_parts
        self.dict_ = dict_
    def from_edg(self, filename):
        # из скачанного файла edg меняем dict_

        __count_new, __count_update = 0, 0
        # __count_new, __count_update - счетчики добавлений в dict_ и замены

        dict_sub = {
        'Миші': '11',
        'Геймерські крісла': '125',
        'Клавіатури': '33',
        'Комплекти (клавіатура+миша)': '968',
        'Навушники та мікрофони': '56',
        'Акустичні системи': '25',
        'Ігрові столи': '1376',
        'Мережеві фільтри': '45',
        'Килимки': '24',
        'Вебкамери': '54',
        'Аудіо/відео кабелі': '648',
        }
        # категории edg в dict_ категории

        status_ = ('В наявності', 'Закінчується')

        try:
            with open(filename, 'rb') as fobj:
                xml = fobj.read()
        except:
            return (False, {'count_new': __count_new,
                    'count_update': __count_update,
                    'status': 'no_file'})

        try:
            root = etree.fromstring(xml)
            result_data=root.find('items').findall('item')
        except:
            return (False, {'count_new': __count_new,
                    'count_update': __count_update,
                    'status': 'xml_data_bad'})

        for data in result_data:
            try:
                temp = dict()
                for k in data.getchildren():
                    temp = dict()
                    if k.tag in ['Code', 'Price', 'StockName', 'Subcategory']:
                        temp[k.tag] = k.text
                if temp['Subcategory'] in dict_sub and temp['Code'] in\
                self.set_parts and temp['StockName'] in status_:
                    if dict_sub[temp['Subcategory']] in self.dict_:
                        # если категория-edg в dict_
                        if temp['Code'] in self.dict_[
                        dict_sub[temp['Subcategory']]
                        ]:
                            # если партнамбер уже существует и цена ниже - меняем в dict_
                            if float(
                            temp['Price']) < self.dict_[
                            dict_sub[
                            temp['Subcategory']]][temp['Code']]['Price']:
                                self.dict_[
                                dict_sub[
                                temp['Subcategory']]][temp['Code']] = \
                                {'PriceUSD': float(
                                temp['Price']),
                                'provider': 'edg'}
                                __count_update += 1
                        else:
                            # если партнамбера нет - записываем в dict_
                            self.dict_[
                            dict_sub[temp['Subcategory']]][temp['Code']] =\
                            {'PriceUSD': float(
                            temp['Price']),
                            'provider': 'edg'}
                            __count_new += 1
                    else:
                        # если категория-edg нет dict_ - создаем кат и записываем нов об-т
                        self.dict_[dict_sub[temp['Subcategory']]] = {}
                        self.dict_[
                        dict_sub[temp['Subcategory']]][temp['Code']] =\
                        {'PriceUSD': float(
                        temp['Price']),
                        'provider': 'edg'}
                        __count_new += 1

            except Exception as e:
                return (False, {'count_new': __count_new,
                        'count_update': __count_update,
                        'status': e})
        return (True, {'count_new': __count_new,
                'count_update': __count_update,
                'status': 'ok'})

>>> set_kb = set()
>>> for data in result_data:
	temp = dict()
	for k in data.getchildren():
		if k.tag in ['Code', 'Price', 'StockName', 'Subcategory']:
			temp[k.tag] = k.text
		if temp['Subcategory'] == 'Клавіатури':
			set_kb.add(temp['Code'])

			
Traceback (most recent call last):
  File "/usr/lib/python3.9/idlelib/run.py", line 559, in runcode
    exec(code, self.locals)
  File "<pyshell#114>", line 6, in <module>
KeyError: 'Subcategory'
>>> for data in result_data:
	temp = dict()
	for k in data.getchildren():
		if k.tag in ['Code', 'Price', 'StockName', 'Subcategory']:
			temp[k.tag] = k.text
	if temp['Subcategory'] == 'Клавіатури':
		set_kb.add(temp['Code'])

		
>>> len(set_kb)
144
>>> list(set_kb)[:10]
['FK11 USB (White)', 'KB-112-U', 'KR-85 PS/2 (Black)', 'FBK25 (Black)', 'B810RC Bloody (White)', 'FX50 USB (White)', 'KB-UML3-01-W-RU', 'KB-UML3-01-W-UA', 'G800MU PS/2 (Black)', 'FX61 USB (Grey)']
>>> class From_provders_filePrices:
    """ меняем цену в dict_ если дешевле при наличии
        set_parts - партнамберы периферии всех? категорий """

    def __init__(self, set_parts, dict_):
        self.set_parts = set_parts
        self.dict_ = dict_
    def from_edg(self, filename):
        # из скачанного файла edg меняем dict_

        __count_new, __count_update = 0, 0
        # __count_new, __count_update - счетчики добавлений в dict_ и замены

        dict_sub = {
        'Миші': '11',
        'Геймерські крісла': '125',
        'Клавіатури': '33',
        'Комплекти (клавіатура+миша)': '968',
        'Навушники та мікрофони': '56',
        'Акустичні системи': '25',
        'Ігрові столи': '1376',
        'Мережеві фільтри': '45',
        'Килимки': '24',
        'Вебкамери': '54',
        'Аудіо/відео кабелі': '648',
        }
        # категории edg в dict_ категории

        status_ = ('В наявності', 'Закінчується')

        try:
            with open(filename, 'rb') as fobj:
                xml = fobj.read()
        except:
            return (False, {'count_new': __count_new,
                    'count_update': __count_update,
                    'status': 'no_file'})

        try:
            root = etree.fromstring(xml)
            result_data=root.find('items').findall('item')
        except:
            return (False, {'count_new': __count_new,
                    'count_update': __count_update,
                    'status': 'xml_data_bad'})

        for data in result_data:
            try:
                temp = dict()
                for k in data.getchildren():
                    #temp = dict()
                    if k.tag in ['Code', 'Price', 'StockName', 'Subcategory']:
                        temp[k.tag] = k.text
                if temp['Subcategory'] in dict_sub and temp['Code'] in\
                self.set_parts and temp['StockName'] in status_:
                    if dict_sub[temp['Subcategory']] in self.dict_:
                        # если категория-edg в dict_
                        if temp['Code'] in self.dict_[
                        dict_sub[temp['Subcategory']]
                        ]:
                            # если партнамбер уже существует и цена ниже - меняем в dict_
                            if float(
                            temp['Price']) < self.dict_[
                            dict_sub[
                            temp['Subcategory']]][temp['Code']]['Price']:
                                self.dict_[
                                dict_sub[
                                temp['Subcategory']]][temp['Code']] = \
                                {'PriceUSD': float(
                                temp['Price']),
                                'provider': 'edg'}
                                __count_update += 1
                        else:
                            # если партнамбера нет - записываем в dict_
                            self.dict_[
                            dict_sub[temp['Subcategory']]][temp['Code']] =\
                            {'PriceUSD': float(
                            temp['Price']),
                            'provider': 'edg'}
                            __count_new += 1
                    else:
                        # если категория-edg нет dict_ - создаем кат и записываем нов об-т
                        self.dict_[dict_sub[temp['Subcategory']]] = {}
                        self.dict_[
                        dict_sub[temp['Subcategory']]][temp['Code']] =\
                        {'PriceUSD': float(
                        temp['Price']),
                        'provider': 'edg'}
                        __count_new += 1

            except Exception as e:
                return (False, {'count_new': __count_new,
                        'count_update': __count_update,
                        'status': e})
        return (True, {'count_new': __count_new,
                'count_update': __count_update,
                'status': 'ok'})

>>> f = From_provders_filePrices(set_kb, dict_)
>>> filename = '/home/alexey/alexapp/sereja/load_form_providers/edg-price.xml'
>>> r.status_code
200
>>> with open(filename, 'wb') as f:
                        f.write(r.content)

                        
4217439
>>> f = From_provders_filePrices(set_kb, dict_)
>>> f.from_edg(filename)
(True, {'count_new': 59, 'count_update': 0, 'status': 'ok'})
>>> dict_['33']
{'KR-750 USB (Black)': {'PriceUSD': 8.5, 'provider': 'edg'}, 'KR-85 PS/2 (Black)': {'PriceUSD': 8.3, 'provider': 'edg'}, 'KV-300H USB (Grey+Black)': {'PriceUSD': 28.0, 'provider': 'edg'}, 'Q100 Bloody (Black)': {'PriceUSD': 16.0, 'provider': 'edg'}, 'KB-U-103-UA': {'PriceUSD': 3.8, 'provider': 'edg'}, 'KB-103-UA': {'PriceUSD': 3.95, 'provider': 'edg'}, 'B820R Bloody (Black) Red SW': {'PriceUSD': 54.0, 'provider': 'edg'}, 'B930 RGB Bloody (Black)': {'PriceUSD': 55.0, 'provider': 'edg'}, 'B150N Bloody (Black)': {'PriceUSD': 27.0, 'provider': 'edg'}, 'FK10 (Orange)': {'PriceUSD': 10.0, 'provider': 'edg'}, 'FK10 (White)': {'PriceUSD': 10.0, 'provider': 'edg'}, 'B120N Bloody (Black)': {'PriceUSD': 20.0, 'provider': 'edg'}, 'B500N Bloody (Grey)': {'PriceUSD': 32.0, 'provider': 'edg'}, '700K EVO': {'PriceUSD': 122.0, 'provider': 'edg'}, 'FK13P (Black)': {'PriceUSD': 5.4, 'provider': 'edg'}, 'KB-112-U': {'PriceUSD': 4.4, 'provider': 'edg'}, 'B760 Bloody (Grey) Green Sw': {'PriceUSD': 41.0, 'provider': 'edg'}, 'FK13P (White)': {'PriceUSD': 5.4, 'provider': 'edg'}, 'KB-UM-106-UA': {'PriceUSD': 4.83, 'provider': 'edg'}, 'KB-UML-01-UA': {'PriceUSD': 8.35, 'provider': 'edg'}, 'KB-UML3-01-UA': {'PriceUSD': 9.02, 'provider': 'edg'}, 'KB-MCH-03-UA': {'PriceUSD': 5.9, 'provider': 'edg'}, 'KB-MCH-03-W-UA': {'PriceUSD': 5.7, 'provider': 'edg'}, 'FK11 USB (White)': {'PriceUSD': 8.5, 'provider': 'edg'}, 'B800 Bloody (NetBee)': {'PriceUSD': 45.0, 'provider': 'edg'}, 'FK15 (White)': {'PriceUSD': 10.5, 'provider': 'edg'}, 'FK15 (Black)': {'PriceUSD': 10.5, 'provider': 'edg'}, 'FK13 (Grey)': {'PriceUSD': 6.0, 'provider': 'edg'}, 'KB-MCH-04-UA': {'PriceUSD': 3.8, 'provider': 'edg'}, 'KB-UM-107-UA': {'PriceUSD': 4.49, 'provider': 'edg'}, 'FK13 (White)': {'PriceUSD': 6.0, 'provider': 'edg'}, 'VANTAR AX Black': {'PriceUSD': 38.0, 'provider': 'edg'}, 'FKS11 USB (Grey)': {'PriceUSD': 8.2, 'provider': 'edg'}, 'FK25 (White)': {'PriceUSD': 10.5, 'provider': 'edg'}, 'FKS10 (Orange)': {'PriceUSD': 9.0, 'provider': 'edg'}, 'FKS10 (Blue)': {'PriceUSD': 9.0, 'provider': 'edg'}, 'FKS10 (White)': {'PriceUSD': 9.0, 'provider': 'edg'}, 'FKS11 USB (White)': {'PriceUSD': 8.2, 'provider': 'edg'}, 'B750N Bloody (Black)': {'PriceUSD': 40.0, 'provider': 'edg'}, 'KBG-UML-01-UA': {'PriceUSD': 8.6, 'provider': 'edg'}, 'FX-51 USB (Grey)': {'PriceUSD': 20.0, 'provider': 'edg'}, 'FX-50 USB (Grey)': {'PriceUSD': 24.0, 'provider': 'edg'}, 'B318 Bloody (Black) LK Black': {'PriceUSD': 28.0, 'provider': 'edg'}, 'FX60 USB (Grey) White backlit': {'PriceUSD': 25.8, 'provider': 'edg'}, 'FX60H USB (Grey) White backlit': {'PriceUSD': 29.8, 'provider': 'edg'}, 'FX61 USB (Grey)': {'PriceUSD': 24.0, 'provider': 'edg'}, 'FX61 USB (White)': {'PriceUSD': 24.0, 'provider': 'edg'}, 'KPD-U-03': {'PriceUSD': 3.34, 'provider': 'edg'}, 'B135N Bloody (Black)': {'PriceUSD': 16.0, 'provider': 'edg'}, 'B140N Bloody (Black)': {'PriceUSD': 16.0, 'provider': 'edg'}, 'B310N Bloody (Black)': {'PriceUSD': 22.5, 'provider': 'edg'}, 'FBX50C (White)': {'PriceUSD': 29.0, 'provider': 'edg'}, 'FBX51C (White)': {'PriceUSD': 26.0, 'provider': 'edg'}, 'S510R Bloody (Pudding Black)': {'PriceUSD': 31.5, 'provider': 'edg'}, 'S98 Bloody (Sports Red)': {'PriceUSD': 58.0, 'provider': 'edg'}, 'S98 Bloody (Sports Lime)': {'PriceUSD': 58.0, 'provider': 'edg'}, 'FX50 USB (White)': {'PriceUSD': 24.0, 'provider': 'edg'}, 'FX51 USB (White)': {'PriceUSD': 20.0, 'provider': 'edg'}, 'Puri Mini RGB': {'PriceUSD': 70.0, 'provider': 'edg'}}
>>> list(dict_['5'].values())[:2]
[{'PriceUSD': 370.0, 'provider': 'brain'}, {'PriceUSD': 600.0, 'provider': 'brain'}]
>>> ELKO_USERNAME = 'Inna_K'
>>> ELKO_PASSWORD = '26022011M'
>>> token = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2NsYWltcy9uYW1lIjoiNjAxNDIyMUAxIiwiaHR0cDovL3NjaGVtYXMubWljcm9zb2Z0LmNvbS93cy8yMDA4LzA2L2lkZW50aXR5L2NsYWltcy9yb2xlIjoiQXBpIiwiZXhwIjoxNzE2NjQyMzczLCJpc3MiOiJodHRwczovL2tpZXYuZWxrb2dyb3VwLmNvbSIsImF1ZCI6InVhYXBpLmVsa28uY2xvdWQifQ.xmStyX1wPACsP6Fhy5nUVNrwlEUXP_QItcNX2s4V6lw'
>>> r = requests.get('https://uaapi.elko.cloud/v3.0/Catalogs/Products', params={
                'CategoryCode': '',
                'VendorCode': '',
                'ELKOcode': ''},
            headers={'Authorization': token,"Content-Type": "application/json"},
            timeout=30)

>>> r.status_code
200
>>> elko = r.json()
>>> filename = '/home/alexey/alexapp/sereja/load_form_providers/elko-price.json'
>>> with open(filename, 'w') as write_file:
                json.dump(elko,write_file)

                
>>> set_category = set()
>>> for x in elko:
	set_category.add(x['catalog'])

	
>>> set_category
{'CCC', 'DDC', 'UCC', 'SSU', 'SSP', 'MES', 'HDA', 'MDE', 'SCH', 'HES', 'NDP', 'UPW', 'CHA', 'VCR', 'SPU', 'CLA', 'GAC', 'MGR', 'SOP', 'HST', 'SKP', 'MCR', 'DMA', 'FAC', 'MPC', 'SLJ', 'MDU', 'CMO', 'NIC', 'COA', 'MBA', 'NB', 'COC', 'STC', 'CPS', 'KEY', 'PSU', 'WAP', 'SSM', 'LC3', 'MBS', 'CNS', 'PWA', 'BAC', 'CBM', 'MIX', 'HAV', 'WR3', 'BLE', 'COS', 'KET', 'SIR', 'PLE', 'IRH', 'MEB', 'CAS', 'MFL', 'WRO', 'ICA', 'PCL', 'DEV', 'WOD', 'VGP', 'TOS', 'WRA', 'POB', 'SFA', 'EVC', 'VCL', 'RCA', 'ESD', 'SCO', 'IPC', 'WAD', 'SPR', 'HPH', 'OWI', 'MPH', 'MEM', 'TPC', 'SSX', 'HDR', 'GST', 'CGR', 'PCC', 'PMI', 'HE2', 'UHU', 'NCC', 'JBO', 'VSS', 'RCL', 'MNB', 'MOP', 'UCB', 'PWL', 'LBU', 'ADM', 'CRL', 'FPR', 'NCI', 'IIO', 'JEX', 'SFM', 'WAE', 'MBI', 'SWI', 'CNP', 'HDE', 'NBA', 'SCB', 'PWS', 'FCB', 'HMS', 'DRA', 'CAB', 'FAH', 'IOC', 'STS', 'RMD', 'TME', 'ANT', 'FNC', 'TSL', 'PLO', 'BMR', 'POS', 'IRO', 'CPU', 'SPF', 'SPE', 'HDS', 'CSW', 'ROU', 'HDC', 'CBL', 'VCB', 'AIO', 'CNA', 'POL', 'SBS', 'POE', 'PWG', 'ABP', 'SMO', 'SER', 'GCO', 'HAU', 'WRE', 'MCO', 'MOU', 'GRI', 'WCO'}
>>> dict_name = dict()
>>> for x in elko:
	if x['name'] not in dict_name:
		dict_name[x['name']] = x['catalog']

		
>>> dict_name

>>> list_ = [(k,v) in k,v in dict_name.items()]
Traceback (most recent call last):
  File "/usr/lib/python3.9/idlelib/run.py", line 559, in runcode
    exec(code, self.locals)
  File "<pyshell#150>", line 1, in <module>
NameError: name 'v' is not defined
>>> list_ = list(dict_name.items())
>>> list_[:50]
[('DRONE ACC ZENMUSE L1/CP.EN.00000330.01 DJI', 'DRA'), ('UPS TOWER/RACK 20000VA/UPS2000-G-20KRTL-01 HUAWEI', 'UPW'), ('UPS TOWER/RACK 15000VA/UPS2000-G-15KRTL-01 HUAWEI', 'UPW'), ('VMware vCenter Server 6 Standard for vSphere 6 (Per Instance)', 'CSW'), ('SCOPE VARMINT LRFTS50-640/3142555306RA51 AGM', 'PCL'), ('NAS STORAGE RACKST 16BAY 3U RP/NO HDD USB3 RS2821RP+ SYNOLOGY', 'STS'), ('SCOPE VARMINT LRFTS50-384/3142455306RA51 AGM', 'PCL'), ('NAS STORAGE TOWER 12BAY/NO HDD USB3 DS3622XS+ SYNOLOGY', 'STS'), ('VMware vSphere 6 Enterprise Plus for 1 processor', 'CSW'), ('NET CAMERA Q6135-LE 50HZ/PTZ DOME HDTV 01958-002 AXIS', 'FNC'), ('NB B360 CI5-1240P 13" 8GB/256GB W11P BS3154BHBDGX GETAC', 'RMD'), ('NET SWITCH 48PORT 1000M 4SFP+/6100 JL675A ARUBA BY HPE', 'SWI'), ('NET ROUTER  SFP+ 8PORT/CCR1072-1G-8S+ MIKROTIK', 'ROU'), ('NET SWITCH MODULE ARUBA 5400R/24P J9986A ARUBA BY HPE', 'MCO'), ('UPS TOWER 9E 6000VA 4800W/9E6KI EATON', 'UPW'), ('PA AMPLIFIER 2X500W PAVIRO/PVA-2P500 BOSCH', 'PLE'), ('VMware vSAN 6 Standard for 1 processor', 'CSW'), ('NAS EXPAN RACKST 12BAY 2U RP/NO HDD RX1217RP SYNOLOGY', 'JBO'), ('VGA PCIE16 RTX4090 24GB GDDR6X/RTX4090SUPRIM LIQUID X 24G MSI', 'VGP'), ('VGA PCIE16 RTX4090 24GB GDDR6X/RTX 4090 SUPRIM X 24G MSI', 'VGP'), ('UPS TOWER 9SX 3000I 3000VA/2700W 9SX3000I EATON', 'UPW'), ('NAS STORAGE TOWER 12BAY/NO HDD USB3 DS2422+ SYNOLOGY', 'STS'), ('PRINTER LABEL B-EX6T1-TS12/18221168843 TOSHIBA', 'POS'), ('NET SWITCH 48PORT CL4 4SFP/6000 R8N85A ARUBA BY HPE', 'SWI'), ('UPS TOWER/RACK 5PX RT3U 3000VA/3000W 5PX3000IRT3UG2 EATON', 'UPW'), ('PA VAS CONTROLLER PAVIRO/PVA-4CR12 BOSCH', 'PLE'), ('NAS STORAGE TOWER 8BAY/NO HDD DS1823XS+ SYNOLOGY', 'STS'), ('ALARM SECURITY BARRIERS/MICRO 8 MITECH', 'CNP'), ('SPEAKER TOWER BLACK/B23-465TOWER TRUAUDIO', 'HAV'), ('NET SWITCH 10G 12P 4SFP+/1960 JL805A ARUBA BY HPE', 'SWI'), ('UPS ACC BATTERY 240V RACK/ESS-240V12-9AhBPVBA01 HUAWEI', 'UCC'), ('VGA PCIE16 RTX4090 24GB GDDR6X/RTX 4090 VENTUS 3X 24G OC MSI', 'VGP'), ('NB K3605VV CI7-13700H 16" 32GB/1TB K3605VV-MX047 ASUS', 'NB'), ('PA VAS ROUTER PAVIRO/PVA-4R24 BOSCH', 'PLE'), ('SPEAKER SUBWOOFER 12"/CSUB-12 TRUAUDIO', 'HAV'), ('NB K3605VV CI7-13700H 16" 32GB/1TB K3605VV-PL086 ASUS', 'NB'), ('UPS RACK 9SX 2000VA 1800W/9SX2000IRACK2U EATON', 'UPW'), ('CPUX16C 2900/22M S3647 OEM/GOLD 6226R CD8069504449000 IN', 'CPS'), ('UPS TOWER/RACK 5SC 3000VA/2700W 5SC3000IRT EATON', 'UPW'), ('NB K3605ZV CI7-12700H 16" 32GB/1TB K3605ZV-N1025 ASUS', 'NB'), ('PRINTER LABEL B-EX4T1/18221168769 TOSHIBA', 'POS'), ('NAS STORAGE RACKST 8BAY 2U RP/NO HDD TS-832PXU-RP-4G QNAP', 'STS'), ('UPS ACC BATTERY 240V RACK/ESS-240V12-7AHBPVBA01  HUAWEI', 'UCC'), ('VGA PCIE16 RTX4080 16GB GDDR6X/RTX 4080 16GB SUPRIM X MSI', 'VGP'), ('NAS STORAGE RACKST 4BAY 1U/NO HDD TS-453DU-RP-4G QNAP', 'STS'), ('CASE FULL TOWER EATX W/O PSU/C700M-KHNN-SL1 COOLER MASTER', 'CAS'), ('POWER STATION 2000W/AC200P BLUETTI', 'PWS'), ('SERVER THINKSYSTEM ST50/E-2224G 7Y48S1KR00 LENOVO', 'SER'), ('NB G614JU CI5-13450HX 16" 16GB/512GB G614JU-N4224 ASUS', 'NB'), ('POWER STATION EXPLORER 2000PRO/2160WH HTE0782000 JACKERY', 'PWS')]
>>> len(list_)
2287
>>> dict_name = dict()
>>> for x in elko:
	if x['catalog'] not in dict_name.values():
		dict_name[x['name']] = x['catalog']

		
>>> len(dict_name)
153
>>> dict_name
{'DRONE ACC ZENMUSE L1/CP.EN.00000330.01 DJI': 'DRA', 'UPS TOWER/RACK 20000VA/UPS2000-G-20KRTL-01 HUAWEI': 'UPW', 'VMware vCenter Server 6 Standard for vSphere 6 (Per Instance)': 'CSW', 'SCOPE VARMINT LRFTS50-640/3142555306RA51 AGM': 'PCL', 'NAS STORAGE RACKST 16BAY 3U RP/NO HDD USB3 RS2821RP+ SYNOLOGY': 'STS', 'NET CAMERA Q6135-LE 50HZ/PTZ DOME HDTV 01958-002 AXIS': 'FNC', 'NB B360 CI5-1240P 13" 8GB/256GB W11P BS3154BHBDGX GETAC': 'RMD', 'NET SWITCH 48PORT 1000M 4SFP+/6100 JL675A ARUBA BY HPE': 'SWI', 'NET ROUTER  SFP+ 8PORT/CCR1072-1G-8S+ MIKROTIK': 'ROU', 'NET SWITCH MODULE ARUBA 5400R/24P J9986A ARUBA BY HPE': 'MCO', 'PA AMPLIFIER 2X500W PAVIRO/PVA-2P500 BOSCH': 'PLE', 'NAS EXPAN RACKST 12BAY 2U RP/NO HDD RX1217RP SYNOLOGY': 'JBO', 'VGA PCIE16 RTX4090 24GB GDDR6X/RTX4090SUPRIM LIQUID X 24G MSI': 'VGP', 'PRINTER LABEL B-EX6T1-TS12/18221168843 TOSHIBA': 'POS', 'ALARM SECURITY BARRIERS/MICRO 8 MITECH': 'CNP', 'SPEAKER TOWER BLACK/B23-465TOWER TRUAUDIO': 'HAV', 'UPS ACC BATTERY 240V RACK/ESS-240V12-9AhBPVBA01 HUAWEI': 'UCC', 'NB K3605VV CI7-13700H 16" 32GB/1TB K3605VV-MX047 ASUS': 'NB', 'CPUX16C 2900/22M S3647 OEM/GOLD 6226R CD8069504449000 IN': 'CPS', 'CASE FULL TOWER EATX W/O PSU/C700M-KHNN-SL1 COOLER MASTER': 'CAS', 'POWER STATION 2000W/AC200P BLUETTI': 'PWS', 'SERVER THINKSYSTEM ST50/E-2224G 7Y48S1KR00 LENOVO': 'SER', 'SERVER CHASSIS 2U 920W EATX/CSE-826BE1C-R920LPB SUPERMICRO': 'SCH', 'SW ESD PROJECT PRO 2021/H30-05939 MS': 'ESD', 'PETROL GENERATOR 6.5KW 380V/GDA 7500DPE-3 DAEWOO': 'PWG', "RACK ENCLOSURE 42U 19''/UA-MGSE42810B CMS": 'RCA', 'WRL ACCESS POINT 1750MBPS 5PCS/UNIFI UAP-AC-M-PRO-5 UBIQUITI': 'WOD', 'ENTRY PANEL MAIN UNIT HELIOS/IP VERSO W/CAMERA 9155101CB 2N': 'NDP', 'ENTRY PANEL IP BUTTON MODULE/2BUTTONS &10W SPK 9152102W 2N': 'DEV', 'TABLET TAB P12 PRO 12" 256GB/STORM GREY ZA9E0025UA LENOVO': 'TPC', 'ACCESS UNIT 2.0 BLUETOOTH RFID/9160335 2N': 'CRL', 'PC M3700WYAK R7-5825U 27" 16GB/512GB M3700WYAK-WA028M ASUS': 'MNB', 'WRL ACCESS POINT 1733MBPS/5PACK UAP-NANOHD-5 UBIQUITI': 'WAP', 'SOLAR PANEL 350W/PV350 BLUETTI': 'SOP', 'RAID CARD SAS 8P/AOC-S3108L-H8IR SUPERMICRO': 'DDC', 'CPU CORE I9-13900KS S1700 BOX/6.0G BX8071513900KS S RMBX IN': 'CPU', 'NET SPEAKER CABINET/C1004-E 0833-001 AXIS': 'CNS', 'SPEAKER 9.1 BAR/JBLBAR913DBLKEP JBL': 'SPE', 'VACUUM CLEANER ROBOT S8+/BLACK S8P52-00 ROBOROCK': 'VCR', 'SSD PCIE 6.4TB 7450 MAX U.3/MTFDKCB6T4TFS MICRON': 'SSP', 'HDD SATA 16TB 7200RPM 6GB/S/256MB HAT5300-16T SYNOLOGY': 'HES', 'VACUUM CLEANER/V12 DETECT SLIM ABSOLUTE DYSON': 'VCL', 'PRINTER/COP/SCAN ESTUDIO2323AM/6AG00010113 TOSHIBA': 'AIO', 'HDD SAS 16TB 7200RPM 12GB/S/512MB HAS5300-16T SYNOLOGY': 'HDC', 'MONITOR LCD 34"/OPTIX MPG341QR MSI': 'LC3', 'SSD SATA2.5" 3.84TB TLC/D3-S4620 SSDSC2KG038TZ01 INTEL': 'SFM', 'NET APPLIANCE/UDM-SE UBIQUITI': 'WCO', 'NET VIDEO ENCODER P7304/01680-001 AXIS': 'IPC', 'SCOOTER ELECTRIC/N65 NAVEE': 'SBS', 'HAIR STYLER AIRWRAP COMPLETE/LONG COPPER/NICKEL DYSON': 'BAC', 'SERVER MB C621 S3647 ATX/MBD-X11DPL-I-O SUPERMICRO': 'MBS', 'COFFEE MACHINE ECAM 350.50 B/0132215442 DELONGHI': 'CBM', 'MB AMD X670 SAM5 ATX/MPG X670E CARBON WIFI MSI': 'MBA', 'NET ROUTER 1200M 4PORT/RUTX12000000 TELTONIKA': 'WRO', 'MOBILE PHONE RENO10 PRO 12/256/CPH2525 GLOSSY PURPLE OPPO': 'MPH', 'CHARGER WALL-BOX 3-PHASE 11KW/5M DN-3P16-050 ASSMANN': 'CHA', 'HAIR DRYER SUPERSONIC/HD07 COPPER DYSON': 'HDR', 'PRINTER ACC DOCUMENT FEEDER/6AR00001070 TOSHIBA': 'PCC', 'NET CARD PCIE SFP28/E25G21-F2 SYNOLOGY': 'NIC', 'FOOD PROCESSOR KVC 85.004 SI/0W20011378 KENWOOD': 'FPR', 'PANEL HOUSING FOR PSU/PSB 0004 A BOSCH': 'ICA', 'HDD SATA 16TB 7200RPM 6GB/S/256MB ST16000NT001 SEAGATE': 'HDS', 'SSD M.2 2280 2TB T700/CT2000T700SSD3 CRUCIAL': 'SSU', 'NAS ACC RAM MEMORY DDR4 16GB/D4EC-2666-16G SYNOLOGY': 'TME', 'MB Z790 S1700 ATX/Z790 AERO G 1.0 GIGABYTE': 'MBI', 'GAMING CHAIR CALIBER X2/CMI-GCX2-BK COOLER MASTER': 'GAC', 'CASE PSU ATX 1300W/MEG AI1300P PCIE5 MSI': 'PSU', 'IRON 2700W W/STEAM GENERATOR/IS 7286BK SS 128805002 BRAUN': 'IRO', 'GRILL ELECTRIC CGH 1130 DP/179510011 DELONGHI': 'GRI', 'CABLE EV CHARGING 10M 32A/DK-3P32-S-100 ASSMANN': 'EVC', 'SERVER ACC PSU 1200W/FSP1200-50FS FSP': 'SPU', 'NET POE INJECTOR MDSPN/JW701A ARUBA BY HPE': 'POE', 'SSD SATA2.5" 4TB 6GB/S/870 EVO MZ-77E4T0B/EU SAMSUNG': 'SSM', 'BATTERY 12V 330W/HRL12330W CSB': 'ABP', 'NET CAMERA ACC WALL MOUNT/T91G61 5506-951 AXIS': 'NCC', 'CPU COOLER AORUS/WATERFORCE X 360 GIGABYTE': 'COC', 'MEMORY DIMM 64GB DDR5-6000 K2/6000J3238G32GX2-TZ5K G.SKILL': 'MEM', 'HDD USB3 10TB EXT. 3.5"/WDBWLG0100HBK-EESN WDC': 'HDE', 'PRINTER ACC FUSER UNIT 230V/6LK12912100 TOSHIBA': 'SLJ', 'DETECTOR ACC GROUND FIXING/BASE GAR GR MITECH': 'FAC', 'HEADSET GAMING/QUANTUM ONE BLACK JBL': 'HST', 'SW LIC ROUTEROS CHR P-UNLIM': 'CLA', 'NAS ACC SSD ADAPTER CARD/M2D20 SYNOLOGY': 'STC', 'JUICE EXTRACTOR JE 850/0WJE850002 KENWOOD': 'JEX', 'SW OEM WIN 11 PRO 64B/UA DVD FQC-10557 MS': 'OWI', 'SSD USB3.1 2TB EXT./SHIELD T7 MU-PE2T0R/EU SAMSUNG': 'SSX', 'MEAT GRINDER MG 516/0WMG516002 KENWOOD': 'MGR', 'HDD USB3 4TB EXT./LAC9000633 LACIE': 'HE2', 'AIR FRYER/E6AF1-4ST ELECTROLUX': 'MCR', 'BREAD MAKER BM1400E/312793 GORENJE': 'BMR', 'HEADPHONES K612 PRO/2458X00100 AKG': 'HPH', 'IR HEATER 2900W/S/29 UFO': 'IRH', 'DETECTOR WRL MOTIONCAM/OUTDOOR PHOD 000027961 AJAX': 'MDE', 'INTERFACE MODULE OCTO-INPUT/FLM-420-I8R1-S BOSCH': 'ADM', 'CAR GPS TRACKER/FMB641 TELTONIKA': 'CNA', 'CABLE DAC SFP+/SFP+ 3M/J9283D ARUBA BY HPE': 'CBL', 'MIXER MMC700W/663554 GORENJE': 'MIX', 'WRL 4G ROUTER MOBILE/M7450 TP-LINK': 'WR3', 'LAMP SMART FLOOD LIGHT/550LM UP-FLOODLIGHT UBIQUITI': 'LBU', 'ENTRY PANEL IP VERSO 2 MODULE/FLUSH FRAME 9155012 2N': 'DMA', 'WRL CAMERA BITES 2 LITE/BL10US PETCUBE': 'NCI', 'MOUSE USB OPTICAL WRL MM731/MM-731-WWOH1 COOLER MASTER': 'MOU', 'KEYBOARD USB RUS/AORUS K1 GIGABYTE': 'KEY', 'NET CAMERA SOFTWARE ACS/1LIC ADD-ON 0202-602 AXIS': 'VSS', 'SMART VALVE 1/2"/WATERSTOP WHITE 000029710 AJAX': 'HAU', 'SERVER MEMORY 32GB PC25600/REG KSM32RS4/32MFR KINGSTON': 'MES', 'KETTLE KBIN 2001 BK/0210110140 DELONGHI': 'KET', 'PA LOUDSPEAKER CEILING 24W/METAL GRILLE LBC3099/41 BOSCH': 'PLO', 'GIMBAL ACC RONIN BG30 GRIP/CP.RN.00000103.03 DJI': 'CCC', 'NB MEMORY 32GB DDR5-4800 SO/CT32G48C40S5 CRUCIAL': 'MEB', 'HDD SATA2.5" 2TB 6GB/S 128MB/BLUE WD20SPZX WDC': 'HMS', 'NET POWERLINE ADAPTER 1200MBPS/TL-PA8010P KIT TP-LINK': 'PWL', 'POWER STATION ACC BAG//EXPLORER 2000 PRO JACKERY': 'PWA', 'BLENDER MQ 5264 BK BL/0X22111345 BRAUN': 'BLE', 'TOASTER CTOT 2103 GY/0230120123 DELONGHI': 'TOS', 'FAN HEATER SMART ZNNFJ07ZM/ERH6006EU SMARTMI': 'FAH', 'WRL ADAPTER 3000MBPS PCIE/ARCHER TX3000E TP-LINK': 'WRA', 'CASE ACC VERTICAL VGA HOLDER/MCA-U000R-WFVK03 COOLER MASTER': 'CMO', 'WRL POWERLINE EXTEN 1000MBPS/TL-WPA7617 KIT TP-LINK': 'WRE', 'GARMENT STEAMER HANDHELD/E7HS1-6OW 910003640 ELECTROLUX': 'GST', 'CABLE USB3 20M/DA-73107 ASSMANN': 'UCB', 'MEMORY DRIVE FLASH USB-C 1TB/SILV AELI-UE800-1T-CSG ADATA': 'MDU', 'SIREN OUTDOOR STREETSIREN WRL/WHITE 000001159 AJAX': 'SIR', 'MOUSE PAD MP511 XXL/MP-511-CBXC1 COOLER MASTER': 'MOP', 'SERVER ACC RACK KIT BLACK//SC742 CSE-PT26L-B SUPERMICRO': 'SMO', 'KEYPAD WRL/PLUS WHITE 000023070 AJAX': 'SKP', 'POWER BANK SOLAR 25000MAH/420-56 SANDBERG': 'POB', 'SERVER ACC HEATSINK/SNK-P0078PC SUPERMICRO': 'SFA', 'MEMORY MICRO SDXC 128GB W/AD./AUSDX128GUII3CL10-CA1 ADATA': 'MFL', 'ANTENNA KIT LORA OMNI/868 OMNI ANTENNA MIKROTIK': 'WAE', 'CASE FAN 120MM 3-RGB SET/RIING/CL-F042-PL12SW-B THERMALTAKE': 'COS', 'NB ACC COOLING PAD 17" BLACK/R9-NBS-E32K-GP COOLER MASTER': 'NBA', 'SERVER ACC RISER CARD PCIE4/1U RSC-S-6G4 SUPERMICRO': 'SCO', 'SMARTBAND BAND 2/OBBE215 MIDNIGHT BLACK OPPO': 'SPF', 'PA MICROPHONE HAND HELD DYN./OMNIDIR. LBB9080/00 BOSCH': 'PMI', 'COFFEE GRINDER/GX204D10 KRUPS': 'CGR', 'GAMEPAD WRL/FORCE GC30 V2 BLACK MSI': 'GCO', 'CPU COOLER ACC THERMAL PAD/290X290X1 ACTPD00018A ARCTIC': 'COA', 'CABLE SAS MSASX4 (SFF-8643) TO/SFF-8482 0.8 2280100-R ADAPTEC': 'SCB', 'CABLE HDMI 10M/AK-330118-100-S ASSMANN': 'VCB', 'SSD ACC ENCLOSURE M.2 RGB/PV860UPRGM PATRIOT': 'HDA', 'I/O HUB USB3 7PORT/UH700 TP-LINK': 'UHU', 'Antivirus + Antirasomware + Web-Protection 1 year Commersial 1-9 Users': 'ANT', 'WRL ROUTER/MOD. 300MBPS ADSL2+/TD-W8961N TP-LINK': 'WAD', 'TABLET CASE COVER RPC3026 GREY/RPC2294 GREY OPPO': 'TSL', 'PROTECTOR POWER SURGE 6DIN/PS6D EATON': 'SPR', 'CABLE CONSOLE USB TO MICRO USB/JY728A ARUBA BY HPE': 'CAB', 'REMOTE CONTROLLER SPACECONTROL/WHITE 000001157 AJAX': 'RCL', 'MOBILE COVER A78/AL22106 BLACK OPPO': 'MPC', 'ADAPTER HDMI TO USB-C/MRCS194 MEDIARANGE': 'IOC', 'PATCH CABLE LC-LC OM4/5M 50/125 DK-2533-05-4 ASSMANN': 'FCB', 'CAMPING LATERN LED/GREEN 58392 GOOBAY': 'POL', 'I/O INDUSTRIAL SENSOR /TRANS/SENINNEU868 W TEKTELIC': 'IIO'}
>>> type(elko)
<class 'list'>
>>> elko[0]
{'id': 1341426, 'name': 'DRONE ACC ZENMUSE L1/CP.EN.00000330.01 DJI', 'manufacturerCode': 'CP.EN.00000330.01', 'vendorName': 'DJI', 'vendorCode': 'DJ', 'catalog': 'DRA', 'quantity': '1', 'price': 9800.0, 'discountPrice': 9800.0, 'fullDsc': 'DRONE ACC ZENMUSE L1/CP.EN.00000330.01 DJI', 'altDsc': 'DRONE ACC ZENMUSE L1/CP.EN.00000330.01 DJI', 'detailedDescription': '', 'currency': 'USD', 'httpDescription': 'https://ecom.elko.ua/product/1341426', 'packagingQuantity': 1, 'warranty': '2 years', 'eanCode': '6941565910042', 'reservedQuantity': 0, 'reservedQuantityFromBasket': 0, 'transitQuantity': '0', 'rrp': 545999.0, 'rrPcontrol': 'Y', 'searchText': 'CP.EN.00000330.01', 'prP4': 'MSC', 'code_UKTZED': '9015101000', 'uAproductName': 'Лазерний далекомірний сканер (лідар) L1 для квадрокоптера - CP.EN.00000330.01 DJI', 'pictureUrl': 'https://static.elko.cloud/ProductImages/4be6bc4a-d9ff-46dd-a81d-8c3164838e84.Jpeg', 'discount': {'status': False, 'price': [], 'link': None}, 'origin': 'Китай'}
>>> elko[0]['name_itm']
Traceback (most recent call last):
  File "/usr/lib/python3.9/idlelib/run.py", line 559, in runcode
    exec(code, self.locals)
  File "<pyshell#162>", line 1, in <module>
KeyError: 'name_itm'
>>> elko[0]['manufacturerCode']
'CP.EN.00000330.01'
>>> from alexapp.sereja.load_form_providers.get_service import quantity_to_avail
Traceback (most recent call last):
  File "/usr/lib/python3.9/idlelib/run.py", line 559, in runcode
    exec(code, self.locals)
  File "<pyshell#164>", line 1, in <module>
  File "/home/alexey/alexapp/sereja/load_form_providers/get_service.py", line 12, in <module>
    from load_form_providers.dc_descr_catalog import *
ModuleNotFoundError: No module named 'load_form_providers'
>>> def quantity_to_avail(str_):
    # for get_from_json_elko2
    #пребразование из quantity в общий статус (yes, no)

    if str_.find('>') != -1:
        return 'yes'
    elif str_ == '0':
        return 'no'
    else:
        return 'q'

>>> set_mon = set()
>>> for x in elko:
	if x['catalog'] == 'LC3':
		set_mon.add(x['manufacturerCode'])

		
>>> len(set_mon)
37
>>> class From_provders_filePrices:
    """ меняем цену в dict_ если дешевле при наличии
        set_parts - партнамберы периферии всех? категорий """

    def __init__(self, set_parts, dict_):
        self.set_parts = set_parts
        self.dict_ = dict_
    def from_elko(self, filename):
        # из скачанного файла brain меняем dict_

        __count_new, __count_update = 0, 0
        # __count_new, __count_update - счетчики добавлений в dict_ и замены

        dict_sub = {
        'LC3': '5',
        'MOU': '11',
        'KEY': '33',
        'HST': '56',
        'SPE': '25',
        }
        # категории brain в dict_ категории

        try:
            with open(filename, "r") as write_file:
                json_data=json.load(write_file)
        except:
            return (False, {'count_new': __count_new,
                    'count_update': __count_update,
                    'status': 'no_file'})

        if isinstance(json_data, list):

            for data in json_data:
                try:
                    if data['manufacturerCode'] in self.set_parts and\
                    quantity_to_avail(data['quantity']) == 'yes' and\
                    data['catalog'] in dict_sub:
                        # если партнамбер-brain есть в set_parts и наличие тру
                        # и категория-brain есть в dict_sub
                        if dict_sub[data['catalog']] in self.dict_:
                            # если категория-brain в dict_
                            if data['manufacturerCode'] in self.dict_[
                            dict_sub[data['catalog']]
                            ]:
                                # если партнамбер уже существует и цена ниже - меняем в dict_
                                if float(
                                data['price']) < self.dict_[
                                dict_sub[
                                data['catalog']]][data['manufacturerCode']]['price']:
                                    self.dict_[
                                    dict_sub[
                                    data['catalog']]][data['manufacturerCode']] = \
                                    {'PriceUSD': float(
                                    data['price']),
                                    'provider': 'brain'}
                                    __count_update += 1
                            else:
                                # если партнамбера нет - записываем в dict_
                                self.dict_[
                                dict_sub[data['catalog']]][data['manufacturerCode']] =\
                                {'PriceUSD': float(
                                data['price']),
                                'provider': 'brain'}
                                __count_new += 1
                        else:
                            # если категория-brain нет dict_ - создаем кат и записываем нов об-т
                            self.dict_[dict_sub[data['catalog']]] = {}
                            self.dict_[
                            dict_sub[data['catalog']]][data['manufacturerCode']] =\
                            {'PriceUSD': float(
                            data['price']),
                            'provider': 'brain'}
                            __count_new += 1
                except Exception as e:
                    return (False, {'count_new': __count_new,
                            'count_update': __count_update,
                            'status': e})

            return (True, {'count_new': __count_new,
                    'count_update': __count_update,
                    'status': 'ok'})

        else:
            return (False, {'count_new': __count_new,
                    'count_update': __count_update,
                    'status': 'json_data_no_dict'})

        
>>> dict_ = dict()
>>> f = From_provders_filePrices(set_mon, dict_)
>>> f.from_elko('/home/alexey/alexapp/sereja/load_form_providers/elko-price.json')
(True, {'count_new': 14, 'count_update': 0, 'status': 'ok'})
>>> dict_
{'5': {'M32QC-EK': {'PriceUSD': 411.0, 'provider': 'brain'}, '66C9UAC1UA': {'PriceUSD': 375.0, 'provider': 'brain'}, 'G322CQP': {'PriceUSD': 346.5, 'provider': 'brain'}, 'VA3209-2K-MHD': {'PriceUSD': 255.3, 'provider': 'brain'}, '66E5GAC3UA': {'PriceUSD': 238.0, 'provider': 'brain'}, 'VX2718-P-MHD': {'PriceUSD': 194.5, 'provider': 'brain'}, 'VA2715-2K-MHD': {'PriceUSD': 187.3, 'provider': 'brain'}, 'PRO MP273QV': {'PriceUSD': 180.2, 'provider': 'brain'}, 'VX2418C': {'PriceUSD': 155.5, 'provider': 'brain'}, '66BEKAC2UA': {'PriceUSD': 140.0, 'provider': 'brain'}, 'PRO MP273': {'PriceUSD': 126.8, 'provider': 'brain'}, 'VA2715-H': {'PriceUSD': 124.0, 'provider': 'brain'}, 'PRO MP242A': {'PriceUSD': 117.8, 'provider': 'brain'}, '66BDKAC2UA': {'PriceUSD': 112.9, 'provider': 'brain'}}}
>>> 