# Generated by Django 3.1.1 on 2022-10-03 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('money', '0026_bids_first_sborsik'),
    ]

    operations = [
        migrations.AddField(
            model_name='managers',
            name='site',
            field=models.CharField(choices=[('versum', 'versum'), ('itblok', 'itblok')], db_index=True, default='versum', max_length=20, verbose_name='сайт'),
        ),
        migrations.AddField(
            model_name='service',
            name='cash_rate',
            field=models.PositiveIntegerField(db_index=True, default=0, verbose_name='Ставка'),
        ),
    ]