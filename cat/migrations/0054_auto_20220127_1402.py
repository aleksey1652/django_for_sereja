# Generated by Django 3.1.1 on 2022-01-27 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cat', '0053_auto_20220112_1235'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parts_short',
            name='kind2',
            field=models.BooleanField(default=False, verbose_name='itlok/versum'),
        ),
    ]
