# Generated by Django 3.1.1 on 2022-01-27 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('money', '0013_auto_20220125_1819'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='statistics_service',
            options={'ordering': ['managers__name'], 'permissions': (('only_managers', 'only managers'), ('only_sereja', 'only sereja')), 'verbose_name': 'Statistics_service', 'verbose_name_plural': 'Statistics_services'},
        ),
        migrations.AlterField(
            model_name='statistics_service',
            name='obsluj_count',
            field=models.PositiveIntegerField(default=0, verbose_name='obsluj_count'),
        ),
        migrations.AlterField(
            model_name='statistics_service',
            name='remont_count',
            field=models.PositiveIntegerField(default=0, verbose_name='remont_count'),
        ),
    ]