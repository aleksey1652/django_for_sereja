from rest_framework import serializers
from .models import *
from cat.models import Parts_short
#

class SeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Series
        fields = ['series_name']  # Поля, которые нужно вернуть для связанных объектов ITSer

class GrupsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grups
        fields = ['group_name']  # Поля, которые нужно вернуть для связанных объектов ITSer

class ShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parts_short
        fields = ['name_parts']  # Поля, которые нужно вернуть для связанных объектов ITSer


class ITSer(serializers.ModelSerializer):
    # Сериализация компов ItblokComputers

    # Сериализация вычисляемого поля (актуальной цены * нaценку)
    price_parts_new = serializers.FloatField(read_only=True)

    # Сериализация связанных объектов Parts_short
    cpu = ShortSerializer(read_only=True)
    cooler = ShortSerializer(read_only=True)
    mb = ShortSerializer(read_only=True)
    ram = ShortSerializer(read_only=True)
    gpu = ShortSerializer(read_only=True)
    hdd = ShortSerializer(read_only=True)
    ssd = ShortSerializer(read_only=True)
    psu = ShortSerializer(read_only=True)
    case = ShortSerializer(read_only=True)
    fan = ShortSerializer(read_only=True)
    wifi = ShortSerializer(read_only=True)
    cables = ShortSerializer(read_only=True)
    soft = ShortSerializer(read_only=True)

    # Сериализация связанных объектов серий и групп
    series = SeriesSerializer(read_only=True)
    grups = GrupsSerializer(read_only=True)

    class Meta:
        model = ItblokComputers
        fields = ('name_computers', 'name_computers_ua', 'price_parts_new',
            'cpu', 'cooler', 'mb', 'ram', 'gpu',
            'hdd', 'ssd', 'psu', 'case', 'fan', 'wifi',
            'cables', 'soft', 'mem_num_computers',
            'vent_num_computers', 'warr_ua', 'warr_ru',
            'series', 'grups',
            'label',)
