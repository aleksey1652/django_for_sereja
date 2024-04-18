from django.apps import AppConfig


class TechConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tech'

    # Список моделей в желаемом порядке
    models = ['Monitors', 'Mouses', 'Pads',
              'Keyboards', 'KM', 'Headsets',
              'Webcams', 'WiFis', 'Acoustics',
              'Chairs', 'Tables', 'Cabelsplus',
              'Filters', 'Accessories', 'Others',
             ]
