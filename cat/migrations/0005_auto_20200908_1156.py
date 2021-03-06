# Generated by Django 3.1.1 on 2020-09-08 08:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cat', '0004_auto_20200907_2027'),
    ]

    operations = [
        migrations.AddField(
            model_name='parts_full',
            name='item_price',
            field=models.CharField(blank=True, db_index=True, max_length=50, null=True, verbose_name='Item_price'),
        ),
        migrations.AddField(
            model_name='parts_full',
            name='partnumber_parts',
            field=models.CharField(blank=True, db_index=True, max_length=50, null=True, unique=True, verbose_name='Partnumber_parts'),
        ),
        migrations.AlterField(
            model_name='parts_full',
            name='availability_parts',
            field=models.CharField(blank=True, db_index=True, max_length=50, null=True, verbose_name='Availability_parts'),
        ),
        migrations.AlterField(
            model_name='parts_full',
            name='providerprice_parts',
            field=models.CharField(blank=True, db_index=True, max_length=50, null=True, verbose_name='price_parts'),
        ),
        migrations.AlterField(
            model_name='parts_full',
            name='providers',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cat.providers'),
        ),
        migrations.AlterField(
            model_name='parts_full',
            name='url_parts',
            field=models.CharField(blank=True, db_index=True, max_length=200, null=True, verbose_name='Url_parts'),
        ),
    ]
