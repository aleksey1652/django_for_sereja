# Generated by Django 3.1.1 on 2021-11-11 16:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cat', '0045_auto_20211111_1812'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='promotion',
            options={'ordering': ['prom__length']},
        ),
    ]
