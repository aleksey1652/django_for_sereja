import re

def mem_from_name_to_filter(name_parts):
    sub_str = 'gb|гб|ddr4|ddr3|ddr5|mhz|kitx'
    sub_name = re.sub(r'' + sub_str, ' ', name_parts.lower())
    return sub_name

def cool_from_name_to_filter(name_parts):
    sub_str = 'amd|intel'
    sub_name = re.sub(r'' + sub_str, ' ', name_parts.lower())
    return sub_name

def mb_from_name_to_filter(name_parts):
    sub_str = 'atx|matx'
    sub_name = re.sub(r'\W|' + sub_str, ' ', name_parts.lower())
    return sub_name

def case_from_name_to_filter(name_parts):
    sub_name = re.sub(r'\W', ' ', name_parts.lower())
    return sub_name

def hdd_ssd_from_name_to_filter(name_parts):
    sub_name = re.sub(r'"|ssd|hdd|2\.5|3\.5', ' ', name_parts.lower())
    return sub_name

def cpu_from_name_to_filter(name_parts):
    sub_name = re.sub(r'\W', ' ', name_parts.lower())
    return sub_name

def video_from_name_to_filter(name_parts):
    sub_name = re.sub(r'\W|intel|amd', ' ', name_parts.lower())
    return ' '.join(re.findall(r'\d{3,4}', sub_name) + re.split(r'\d{3,4}',sub_name))

def ps_from_name_to_filter(name_parts):
    sub_name = re.sub(r'\W', ' ', name_parts.lower())
    return sub_name

dict_name_parts_to_code = {
'iproc':'cpu_from_name_to_filter(name_parts)',
'aproc':'cpu_from_name_to_filter(name_parts)',
'cool':'cool_from_name_to_filter(name_parts)',
'imb':'mb_from_name_to_filter(name_parts)',
'amb':'mb_from_name_to_filter(name_parts)',
'mem':'mem_from_name_to_filter(name_parts)',
'hdd':'hdd_ssd_from_name_to_filter(name_parts)',
'ssd':'hdd_ssd_from_name_to_filter(name_parts)',
'video':'video_from_name_to_filter(name_parts)',
'ps':'ps_from_name_to_filter(name_parts)',
'case':'case_from_name_to_filter(name_parts)',
                        }

def name_parts_to_code(name_parts, kind):
    if kind in dict_name_parts_to_code:
        return eval(dict_name_parts_to_code[kind])
