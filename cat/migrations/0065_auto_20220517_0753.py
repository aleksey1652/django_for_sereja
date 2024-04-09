# Generated by Django 3.1.1 on 2022-05-17 04:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cat', '0064_computer_code'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='computer_code',
            options={'verbose_name': 'Фильтр для сравнения конкурентов', 'verbose_name_plural': 'Фильтры для сравнения конкурентов'},
        ),
        migrations.AlterField(
            model_name='parts_full',
            name='remainder',
            field=models.CharField(blank=True, db_index=True, max_length=50, null=True, verbose_name='Склад'),
        ),
        migrations.AlterField(
            model_name='parts_short',
            name='kind',
            field=models.CharField(blank=True, choices=[('cool', 'cool'), ('imb', 'imb'), ('amb', 'adict_xlsmb'), ('case', 'case'), ('ssd', 'ssd'), ('hdd', 'hdd'), ('aproc', 'aproc'), ('iproc', 'iproc'), ('video', 'video'), ('ps', 'ps'), ('mem', 'mem'), ('vent', 'vent'), ('mon', 'mon'), ('wifi', 'wifi'), ('km', 'km'), ('soft', 'soft'), ('cables', 'cables')], db_index=True, max_length=50, null=True, verbose_name='Вид'),
        ),
    ]
