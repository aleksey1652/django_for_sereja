import os,json,pickle,django
os.environ.setdefault('DJANGO_SETTINGS_MODULE','sereja.settings')
django.setup()
from cat.models import *

with open("it_basa.pickle", "rb") as f:
            it_basa=pickle.load(f)

for x in it_basa.iloc:
    for d in (x.proc,x.mb,x.mem,x.video,x.ps,x.case,x.cool):
        if not isinstance(d,str) and not Parts_short.objects.filter(name_parts=d.Name):
            p=Parts_short(name_parts=d.Name,partnumber_list=f'{d.Partnumbers}')
            p.save()
    for h in x.hdd:
        if not isinstance(h,str) and not Parts_short.objects.filter(name_parts=h.Name):
            p=Parts_short(name_parts=h.Name,partnumber_list=f'{h.Partnumbers}')
            p.save()

Parts_full.objects.filter(partnumber_parts__in=['BX80684G4900','BX80684G5400']).aggregate(a=Min('providerprice_parts'))['a']



with open("dict_msi.json", "r") as write_file:
        dict_msi=json.load(write_file)

s_it=Sites.objects.get(name_sites='itblok')
for x in dict_msi:
    Pc_assembly.objects.create(name_assembly=x,sites=s_it,kind_assembly='msi')

def to_comp(obj):
    dict_comp={}
    dict_comp['name_computers']=obj['name']
    dict_comp['url_computers']=obj.comp_url
    dict_comp['price_computers']=obj.price
    dict_comp['proc_computers']=obj.proc.Name
    dict_comp['mb_computers']=obj.mb.Name
    dict_comp['mem_computers']=obj.mem.Name
    dict_comp['video_computers']=obj.video.Name
    dict_comp['ps_computers']=obj.ps.Name
    dict_comp['case_computers']=obj.case.Name
    dict_comp['cool_computers']=obj.cool.Name
    dict_comp['class_computers']=obj['class']
    dict_comp['warranty_computers']=obj.warranty
    temp=''
    for x in obj.hdd:
        temp+=x.Name+';'
        dict_comp['hdd_computers']=temp[:-1]
    return dict_comp

for x,y in dict_msi.items():
    p=Pc_assembly.objects.get(name_assembly=x)
    for z in y:
        t=to_comp(it_basa.loc[z])
        c=Computers(name_computers=t['name_computers'],url_computers=t['url_computers'],
        price_computers=t['price_computers'],proc_computers=t['proc_computers'],
        mb_computers=t['mb_computers'],mem_computers=t['mem_computers'],
        video_computers=t['video_computers'],hdd_computers=t['hdd_computers'],
        ps_computers=t['ps_computers'],case_computers=t['case_computers'],
        cool_computers=t['cool_computers'],class_computers=t['class_computers'],
        warranty_computers=t['warranty_computers'],pc_assembly=p)
        c.save()

aall=Articles.objects.all()
list_providers = ['dc','itlink','asbis','elko','mti','brain','edg','erc']
for a in aall:
    list_get_providers = []
    #partf = Parts_full.objects.filter(partnumber_parts=a.article)
    try:
        res = r.get_element_panda_partnum(a.article)
    except:
        print(f'false article  {a.article}')
        res={}
    if res:
        for x in list_providers:
            if not res[x].empty:
                list_get_providers.append(x)
    for partf in Parts_full.objects.filter(partnumber_parts=a.article).distinct():
        if partf:
            if partf.providers.name_provider in list_get_providers:
                continue
            else:
                partf.availability_parts = 0
                partf.providerprice_parts = None
                partf.save()
    for p in list_get_providers:
        temp = Parts_full.objects.filter(partnumber_parts=a.article,providers__name_provider=p).distinct()
        if temp:
            temp[0].availability_parts = res[p].Availability
            temp[0].providerprice_parts = res[p].Price
            temp[0].save()
        else:
            prov = Providers.objects.get(name_provider=p)
            Parts_full.objects.create(availability_parts = res[p].Availability,
            providerprice_parts = res[p].Price,name_parts = res[p].Name,
            partnumber_parts = res[p].Partnumber,url_parts = res[p].Url,providers=prov)

#!!!for digitalfury
def to_comp_fury(obj):
    dict_comp={}
    dict_comp['name_computers']=obj['name']
    dict_comp['url_computers']=obj.comp_url
    dict_comp['price_computers']=obj.price
    dict_comp['proc_computers']=obj.proc.Name
    dict_comp['mb_computers']=obj.mb.Name
    dict_comp['mem_computers']=obj.mem.Name
    dict_comp['video_computers']=obj.video.Name
    dict_comp['ps_computers']=obj.ps.Name
    dict_comp['case_computers']=obj.case.Name
    dict_comp['cool_computers']=obj.cool
    dict_comp['class_computers']=obj['class']
    dict_comp['warranty_computers']=obj.warranty
    temp=''
    for x in obj.hdd:
        temp+=x.Name+';'
        dict_comp['hdd_computers']=temp[:-1]
    return dict_comp
for x in fbasa.iloc:
	t=to_comp_fury(x)
	temp=Computers.objects.filter(name_computers=fbasa.iloc[x].name)
	if temp:
		temp[0].name_computers=t['name_computers']
		temp[0].url_computers=t['url_computers']
		temp[0].price_computers=t['price_computers']
		temp[0].proc_computers=t['proc_computers']
		temp[0].mb_computers=t['mb_computers']
		temp[0].mem_computers=t['mem_computers']
		temp[0].video_computers=t['video_computers']
		temp[0].hdd_computers=t['hdd_computers']
		temp[0].ps_computers=t['ps_computers']
		temp[0].case_computers=t['case_computers']
		temp[0].cool_computers=t['cool_computers']
		temp[0].class_computers=t['class_computers']
		temp[0].warranty_computers=t['warranty_computers']
		temp[0].save()
	else:
		c=Computers(name_computers=t['name_computers'],url_computers=t['url_computers'],
        price_computers=t['price_computers'],proc_computers=t['proc_computers'],
        mb_computers=t['mb_computers'],mem_computers=t['mem_computers'],
        video_computers=t['video_computers'],hdd_computers=t['hdd_computers'],
        ps_computers=t['ps_computers'],case_computers=t['case_computers'],
        cool_computers=t['cool_computers'],class_computers=t['class_computers'],
        warranty_computers=t['warranty_computers'],pc_assembly=pcassembly_fury)
		c.save()

replacements = {
                    'Процессор': 'proc', 'Охлаждение процессора': 'cool',
                    'Модель материнской платы': 'mb', 'Оперативная память':'mem',
                    'Видеокарта':'video','Блок питания':'ps','Корпус':'case',
                    'Гарантия':'warranty'
                    }
    def transform(versum_dict):
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
                if ii in replacements:
                    temp_dict[x][replacements[ii]] = versum_dict[x][ii]
            if 'comp_url' in x:
                temp_dict[x]['comp_url'] = versum_dict[x]['comp_url']
            if 'name' in x:
                temp_dict[x]['name'] = versum_dict[x]['name']
            if 'price' in x:
                temp_dict[x]['price'] = versum_dict[x]['price']
        return temp_dict
# for eldorado_get_json(art)
for x,y in art.items():
	for z in ('Модель материнской платы','comp_url','price','Видеокарта','Оперативная память','Корпус','Блок питания','Охлаждение процессора','Гарантия','name','Объем накопителя','Объем второго накопителя','Процессор'):
		if z not in y.keys():
			y[z]=''
