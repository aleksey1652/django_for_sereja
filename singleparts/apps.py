from django.apps import AppConfig


class SinglepartsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'singleparts'

    # Список моделей в желаемом порядке
    models = ['CPU_OTHER', 'GPU_OTHER', 'MB_OTHER',
              'RAM_OTHER', 'SSD_OTHER', 'HDD_OTHER',
              'PSU_OTHER', 'Cooler_OTHER', 'FAN_OTHER',
              'CASE_OTHER',
             ]
