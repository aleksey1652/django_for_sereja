import os,json,pickle,django
os.environ.setdefault('DJANGO_SETTINGS_MODULE','sereja.settings')
django.setup()
from cat.models import *
import pandas as pd

with open("db.json", "r") as write_file:
        db=json.load(write_file)

parts_full_list=[]
parts_short_list=[]
parts_computers_list=[]
sites_list=[]
providers_list=[]
articles_list=[]
pc_assembly_list=[]

for x in db:
    if isinstance(x, dict) and 'model' in x.keys():
        if x['model']=='cat.parts_full':
            parts_full_list.append(x['fields'])

for x in db:
    if isinstance(x, dict) and 'model' in x.keys():
        if x['model']=='cat.parts_short':
            parts_short_list.append(x['fields'])

for x in db:
    if isinstance(x, dict) and 'model' in x.keys():
        if x['model']=='cat.computers':
            parts_computers_list.append(x['fields'])

for x in db:
    if isinstance(x, dict) and 'model' in x.keys():
        if x['model']=='cat.sites':
            sites_list.append(x['fields'])

for x in db:
    if isinstance(x, dict) and 'model' in x.keys():
        if x['model']=='cat.providers':
            providers_list.append(x['fields'])

for x in db:
    if isinstance(x, dict) and 'model' in x.keys():
        if x['model']=='cat.articles':
            articles_list.append(x['fields'])

for x in db:
    if isinstance(x, dict) and 'model' in x.keys():
        if x['model']=='cat.pc_assembly':
            pc_assembly_list.append(x['fields'])



for x in sites_list:
    Sites.objects.create(name_sites=x['name_sites'],more=x['more'])

for x in providers_list:
    p=Providers.objects.create(name_provider=x['name_provider'],more=x['more'])

for x in articles_list:
    a=Articles.objects.create(article=x['article'],item_name=x['item_name'],item_price=x['item_price'])

for x in pc_assembly_list:
    pc=Pc_assembly.objects.create(name_assembly=x['name_assembly'],kind_assembly=x['kind_assembly'],
    sites=Sites.objects.get(pk=x['sites']))

#Parts_short.objects.create(name_parts='empty',partnumber_list='[]',kind='vent')
#Parts_short.objects.create(name_parts='120мм (1 шт.)',partnumber_list='[]',kind='vent')
#Parts_short.objects.create(name_parts='empty video',partnumber_list='[]',kind='video')
#Parts_short.objects.create(name_parts='empty hdd',partnumber_list='[]',kind='hdd')
#Parts_short.objects.create(name_parts='empty ssd',partnumber_list='[]',kind='ssd')
#Parts_short.objects.create(name_parts='empty ps',partnumber_list='[]',kind='ps')


ver_list=[]
it_list=[]

verbasa = pd.read_json('load_form_providers/loads/versum_basa.json')
itbasa = pd.read_json('load_form_providers/loads/it_basa.json')
for x in verbasa.iloc:
    ver_list.append(x['name'])
for x in itbasa.iloc:
    it_list.append(x['name'])

pc_assembly_dict={}
for x in db:
    if isinstance(x, dict) and 'model' in x.keys():
        if x['model']=='cat.pc_assembly':
            pc_assembly_dict[x['pk']]=x['fields']

for x in db:
    if isinstance(x, dict) and 'model' in x.keys():
        if x['model']=='cat.computers' and x['fields']["name_computers"] in ver_list:
            c=Computers(name_computers=x['fields']['name_computers'],url_computers=x['fields']['url_computers'],
                                price_computers=x['fields']['price_computers'],proc_computers=x['fields']['proc_computers'],
                                mb_computers=x['fields']['mb_computers'],mem_computers=x['fields']['mem_computers'],
                                video_computers=x['fields']['video_computers'],hdd_computers=x['fields']['hdd_computers'],
                                ps_computers=x['fields']['ps_computers'],case_computers=x['fields']['case_computers'],
                                cool_computers=x['fields']['cool_computers'],class_computers=x['fields']['class_computers'],
                                warranty_computers=x['fields']['warranty_computers'],vent_computers='empty',
                                vent_num_computers=1,mem_num_computers=1,
                                video_num_computers=1,pc_assembly=Pc_assembly.objects.filter(name_assembly=pc_assembly_dict[x['fields']['pc_assembly']]['name_assembly'],sites__name_sites='versum').first())
            c.save()
cver=Computers.objects.filter(pc_assembly__sites__name_sites='versum')
cver_no=cver.filter(pc_assembly__name_assembly='Other')
for x in cver_no:
    xx=x.delete()

for x in Pc_assembly.objects.filter(name_assembly='Other',sites__name_sites='versum'):
    p=x.delete()

for x in db:
    if isinstance(x, dict) and 'model' in x.keys():
        if x['model']=='cat.computers' and x['fields']["name_computers"] in it_list:
            c=Computers(name_computers=x['fields']['name_computers'],url_computers=x['fields']['url_computers'],
                                price_computers=x['fields']['price_computers'],proc_computers=x['fields']['proc_computers'],
                                mb_computers=x['fields']['mb_computers'],mem_computers=x['fields']['mem_computers'],
                                video_computers=x['fields']['video_computers'],hdd_computers=x['fields']['hdd_computers'],
                                ps_computers=x['fields']['ps_computers'],case_computers=x['fields']['case_computers'],
                                cool_computers=x['fields']['cool_computers'],class_computers=x['fields']['class_computers'],
                                warranty_computers=x['fields']['warranty_computers'],vent_computers='empty',
                                vent_num_computers=1,mem_num_computers=1,
                                video_num_computers=1,pc_assembly=Pc_assembly.objects.filter(name_assembly=pc_assembly_dict[x['fields']['pc_assembly']]['name_assembly'],sites__name_sites='itblok').first())
            c.save()
