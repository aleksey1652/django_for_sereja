# Generated by Django 3.1.1 on 2021-01-28 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cat', '0025_computers_date_computers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parts_short',
            name='computers',
            field=models.ManyToManyField(to='cat.Parts_full'),
        ),
    ]