# Generated by Django 3.1.1 on 2022-09-23 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cat', '0074_auto_20220829_1026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='results',
            name='who_desc',
            field=models.TextField(blank=True, db_index=True, null=True, verbose_name='Who_desc'),
        ),
    ]
