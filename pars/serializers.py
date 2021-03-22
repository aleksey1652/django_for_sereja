from rest_framework import serializers

class CompsSerializer(serializers.Serializer):
    name_computers = serializers.CharField(max_length=300)
    url_computers = serializers.CharField(max_length=300)
    price_computers = serializers.CharField(max_length=300)
    proc_computers = serializers.CharField(max_length=300)
    mb_computers = serializers.CharField(max_length=300)
    mem_computers = serializers.CharField(max_length=300)
    video_computers = serializers.CharField(max_length=300)
    hdd_computers = serializers.CharField(max_length=300)
    ps_computers = serializers.CharField(max_length=300)
    case_computers = serializers.CharField(max_length=300)
    cool_computers = serializers.CharField(max_length=300,)
    class_computers = serializers.CharField(max_length=300)
    warranty_computers = serializers.CharField(max_length=300)
    vent_computers = serializers.CharField(max_length=300)
    mem_num_computers = serializers.CharField(max_length=300)
    video_num_computers = serializers.CharField(max_length=300)
    vent_num_computers = serializers.CharField(max_length=300)
    is_active = serializers.BooleanField()
    date_computers = serializers.DateTimeField()
    mon_computers = serializers.CharField(max_length=300)
    wifi_computers = serializers.CharField(max_length=300)
    km_computers = serializers.CharField(max_length=300)

class CoolerSerializer(serializers.Serializer):
    name = serializers.CharField()
    part_number = serializers.CharField()
    vendor = serializers.CharField()
    price = serializers.CharField()
    desc_ukr = serializers.CharField()
    desc_ru = serializers.CharField()
    fan_type_ua = serializers.CharField()
    fan_type_rus = serializers.CharField()
    fan_spd_ua = serializers.CharField()
    fan_spd_rus = serializers.CharField()
    fan_noise_level = serializers.CharField()
    fan_size = serializers.CharField()
    more = serializers.CharField()
    #is_active = models.BooleanField(default=True)

class CpuSerializer(serializers.Serializer):
    name = serializers.CharField()
    part_number = serializers.CharField()
    vendor = serializers.CharField()
    price = serializers.CharField()
    desc_ukr = serializers.CharField()
    desc_ru = serializers.CharField()
    f_name = serializers.CharField()
    cpu_c_t = serializers.CharField()
    f_cpu_c_t = serializers.CharField()
    cpu_b_f = serializers.CharField()
    cpu_cache = serializers.CharField()
    cpu_i_g_ua = serializers.CharField()
    cpu_i_g_rus = serializers.CharField()
    more = serializers.CharField()
    depend_from = serializers.CharField()
    depend_from_type = serializers.CharField()

class MbSerializer(serializers.Serializer):
    name = serializers.CharField()
    part_number = serializers.CharField()
    vendor = serializers.CharField()
    main_category = serializers.CharField()
    price = serializers.CharField()
    desc_ukr = serializers.CharField()
    desc_ru = serializers.CharField()
    mb_chipset = serializers.CharField()
    mb_max_ram = serializers.CharField()
    more = serializers.CharField()
    depend_to = serializers.CharField()
    depend_to_type = serializers.CharField()

class RamSerializer(serializers.Serializer):
    name = serializers.CharField()
    part_number = serializers.CharField()
    vendor = serializers.CharField()
    f_name = serializers.CharField()
    price = serializers.CharField()
    desc_ukr = serializers.CharField()
    desc_ru = serializers.CharField()
    mem_s = serializers.CharField()
    mem_spd = serializers.CharField()
    mem_l = serializers.CharField()
    more = serializers.CharField()

class HddSerializer(serializers.Serializer):
    name = serializers.CharField()
    part_number = serializers.CharField()
    vendor = serializers.CharField()
    f_name = serializers.CharField()
    price = serializers.CharField()
    desc_ukr = serializers.CharField()
    desc_ru = serializers.CharField()
    hdd_s = serializers.CharField()
    hdd_spd_ua = serializers.CharField()
    hdd_spd_rus = serializers.CharField()
    hdd_ca = serializers.CharField()
    more = serializers.CharField()

class PsuSerializer(serializers.Serializer):
    name = serializers.CharField()
    part_number = serializers.CharField()
    vendor = serializers.CharField()
    price = serializers.CharField()
    desc_ukr = serializers.CharField()
    desc_ru = serializers.CharField()
    psu_p = serializers.CharField()
    psu_c = serializers.CharField()
    psu_f = serializers.CharField()
    more = serializers.CharField()

class GpuSerializer(serializers.Serializer):
    name = serializers.CharField()
    part_number = serializers.CharField()
    vendor = serializers.CharField()
    main_category = serializers.CharField()
    f_name = serializers.CharField()
    price = serializers.CharField()
    desc_ukr = serializers.CharField()
    desc_ru = serializers.CharField()
    gpu_fps = serializers.CharField()
    gpu_m_s = serializers.CharField()
    gpu_b = serializers.CharField()
    gpu_cpu_spd = serializers.CharField()
    gpu_mem_spd = serializers.CharField()
    more = serializers.CharField()

class FanSerializer(serializers.Serializer):
    name = serializers.CharField()
    part_number = serializers.CharField()
    vendor = serializers.CharField()
    price = serializers.CharField()
    desc_ukr = serializers.CharField()
    desc_ru = serializers.CharField()
    case_fan_spd_ua = serializers.CharField()
    case_fan_spd_rus = serializers.CharField()
    case_fan_noise_level = serializers.CharField()
    case_fan_size = serializers.CharField()
    more = serializers.CharField()

class CaseSerializer(serializers.Serializer):
    name = serializers.CharField()
    part_number = serializers.CharField()
    vendor = serializers.CharField()
    price = serializers.CharField()
    desc_ukr = serializers.CharField()
    desc_ru = serializers.CharField()
    case_s = serializers.CharField()
    more = serializers.CharField()

class SsdSerializer(serializers.Serializer):
    name = serializers.CharField()
    part_number = serializers.CharField()
    vendor = serializers.CharField()
    f_name = serializers.CharField()
    price = serializers.CharField()
    desc_ukr = serializers.CharField()
    desc_ru = serializers.CharField()
    ssd_s = serializers.CharField()
    ssd_spd = serializers.CharField()
    ssd_r_spd = serializers.CharField()
    ssd_type_cells = serializers.CharField()
    more = serializers.CharField()
