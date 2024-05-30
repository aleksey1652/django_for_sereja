from cat.models import *
from .load_element import get_min_short, to_article2_1
from pars.ecatalog import dict_name_to_discr

dict_comp_excel = {
            'Процессор AMD': 'proc_computers',
            'Процессор Intel': 'proc_computers',
            'Мать AMD': 'mb_computers',
            'Мать Intel': 'mb_computers',
            'Cpu cooler': 'cool_computers',
            'ОЗУ': 'mem_computers',
            'Видеокарта': 'video_computers',
            'HDD': 'hdd_computers',
            'SSD': 'hdd_computers',
            'Вентилятор': 'vent_computers',
            'Корпус': 'case_computers',
            'Блок питания': 'ps_computers',
            }

def test_price_discrip():
    for short in Parts_short.objects.filter(kind2=False):
        if short.parts_full.first():
            name_ = short.name_parts
            partnumber = short.parts_full.first().partnumber_parts
            discr = eval(dict_name_to_discr[short.kind]).first()
            if discr:
                discr.part_number = partnumber.strip()
                price_ = short.parts_full.first().providerprice_parts
                price_ = price_.replace(',','.') if price_  else '0'
                discr.price = price_
                discr.save()

remainder_old = Parts_full.objects.exclude(remainder=None)
remainder_old.update()

def short_test(k, v):
    if v != 'пусто':
        if k in ('mb_computers', 'proc_computers'):
            amd_intel = to_article2_1(v)
            kind_ = 'a' + k[:-10] if amd_intel == 'aproc' else 'i' + k[:-10]
        elif k == 'hdd_computers':
            hdd_ssd = v.split(';')[0]
            if hdd_ssd != 'пусто':
                kind_ = 'ssd' if hdd_ssd.lower().find('ssd') != -1 else 'hdd'
                short = Parts_short.objects.filter(kind=kind_, kind2=False, name_parts=hdd_ssd)
                if not short.exists():
                    Parts_short.objects.create(kind=kind_, kind2=False, name_parts=hdd_ssd)
            hdd_ssd2 = v.split(';')[1]
            if hdd_ssd2 != 'пусто':
                kind_ = 'ssd' if hdd_ssd2.lower().find('ssd') != -1 else 'hdd'
                short = Parts_short.objects.filter(kind=kind_, kind2=False, name_parts=hdd_ssd2)
                if not short.exists():
                    Parts_short.objects.create(kind=kind_, kind2=False, name_parts=hdd_ssd2)
        else:
            kind_ = k[:-10]
        short = Parts_short.objects.filter(kind=kind_, kind2=False, name_parts=v)
        if not short.exists():
            Parts_short.objects.create(kind=kind_, kind2=False, name_parts=v)

def parts_short_test(dict_):
    for k, v in dict_.items():
        short_test(k, v)



def versum_comp_create(dict_):
    sites_ = Sites.objects.get(name_sites='versum')
    assembly, _ = Pc_assembly.objects.get_or_create(name_assembly=dict_['name_assembly'],
    kind_assembly=dict_['kind_assembly'], sites=sites_)
    comp=Computers(name_computers=dict_['name_computers'],vent_computers=dict_['vent_computers'],
    mem_num_computers='1',proc_computers=dict_['proc_computers'],
    mb_computers=dict_['mb_computers'],mem_computers=dict_['mem_computers'],
    video_computers=dict_['video_computers'],hdd_computers=dict_['hdd_computers'],
    ps_computers=dict_['ps_computers'],case_computers=dict_['case_computers'],
    cool_computers=dict_['cool_computers'],video_num_computers='1',
    vent_num_computers='1',pc_assembly=assembly)
    comp.save()

def versum_com_update(comp, dict_):
    sites_ = Sites.objects.get(name_sites='versum')
    assembly, _ = Pc_assembly.objects.get_or_create(name_assembly=dict_['name_assembly'],
    kind_assembly=dict_['kind_assembly'], sites=sites_)
    comp.name_computers=dict_['name_computers']
    comp.vent_computers=dict_['vent_computers']
    comp.mem_num_computers='1'
    comp.proc_computers=dict_['proc_computers']
    comp.mb_computers=dict_['mb_computers']
    comp.mem_computers=dict_['mem_computers']
    comp.video_computers=dict_['video_computers']
    comp.hdd_computers=dict_['hdd_computers']
    comp.ps_computers=dict_['ps_computers']
    comp.case_computers=dict_['case_computers']
    comp.cool_computers=dict_['cool_computers']
    comp.video_num_computers='1'
    comp.vent_num_computers='1'
    comp.pc_assembly=assembly
    comp.save()

def add_comp_versum(dict_xls):
    versum = Computers.objects.filter(pc_assembly__sites__name_sites='versum')
    for k, comp_xls in dict_xls.items():
        parts_short_test(comp_xls)
        try:
            comp = versum.get(name_computers=k)
            versum_com_update(comp, comp_xls)
        except:
            versum_comp_create(comp_xls)

def for_inactive_comp(dict_xls):
    set_xls = set(dict_xls.keys())
    versum = Computers.objects.filter(pc_assembly__sites__name_sites='versum')
    versum.exclude(name_computers__in=set_xls).update(is_active=False)

def for_inactive_short(): #after create and update versum comps
    versum = Computers.objects.filter(pc_assembly__sites__name_sites='versum')
    set_comp_parts = set(list(dict_comp_excel.values()))
    for part in set_comp_parts:
        if part == 'proc_computers':
            short_versum = Parts_short.objects.filter(kind__in=('aproc','iproc'),kind2=False)
            set_part = set(versum.values_list(part,flat=True))
            set_part.add('пусто')
            short_versum.exclude(name_parts__in=set_part).update(kind2=True)
        elif part == 'mb_computers':
            short_versum = Parts_short.objects.filter(kind__in=('amb','imb'),kind2=False)
            set_part = set(versum.values_list(part,flat=True))
            set_part.add('пусто')
            short_versum.exclude(name_parts__in=set_part).update(kind2=True)
        elif part == 'hdd_computers':
            short_versum = Parts_short.objects.filter(kind__in=('ssd','hdd'),kind2=False)
            set_part = set(versum.values_list(part,flat=True))
            set_ = set()
            for x in set_part:
                k,v = x.split(';')
                set_.add(k)
                set_.add(v)
            short_versum.exclude(name_parts__in=set_).update(kind2=True)
        else:
            kind_ = part[:-10]
            short_versum = Parts_short.objects.filter(kind=kind_,kind2=False)
            set_part = set(versum.values_list(part,flat=True))
            set_part.add('пусто')
            short_versum.exclude(name_parts__in=set_part).update(kind2=True)
