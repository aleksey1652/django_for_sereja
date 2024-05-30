# Generated by Django 3.1.1 on 2022-01-12 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cat', '0052_auto_20211223_1312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articles',
            name='article',
            field=models.CharField(db_index=True, max_length=50, unique=True, verbose_name='Partumber_field'),
        ),
        migrations.AlterField(
            model_name='articles',
            name='item_price',
            field=models.CharField(blank=True, choices=[('cool', 'cool'), ('imb', 'imb'), ('amb', 'amb'), ('case', 'case'), ('ssd', 'ssd'), ('hdd', 'hdd'), ('aproc', 'aproc'), ('iproc', 'iproc'), ('video', 'video'), ('ps', 'ps'), ('mem', 'mem'), ('vent', 'vent'), ('mon', 'mon'), ('wifi', 'wifi'), ('km', 'km'), ('soft', 'soft'), ('cables', 'cables')], db_index=True, max_length=50, null=True, verbose_name='Kind'),
        ),
    ]
