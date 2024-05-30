from django.apps import AppConfig


class TechConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tech'

    # Список моделей в желаемом порядке
    models = ['00 Monitors', '01 Mouses', '02 Pads',
              '03 Keyboards', '04 KM', '05 Headsets',
              '06 Webcams', '07 WiFis', '08 Acoustics',
              '09 Chairs', 'x10 Tables', 'x11 Cabelsplus',
              'x12 Filters', 'x13 Accessories', 'x14 Others',
             ]
