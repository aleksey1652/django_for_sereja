# Generated by Django 3.1.1 on 2022-02-10 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cat', '0059_auto_20220201_1523'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promotion',
            name='computers',
            field=models.ManyToManyField(limit_choices_to={'pc_assembly__sites__name_sites': 'versum'}, to='cat.Computers'),
        ),
    ]
