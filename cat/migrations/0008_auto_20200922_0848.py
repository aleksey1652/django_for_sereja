# Generated by Django 3.1.1 on 2020-09-22 05:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cat', '0007_auto_20200921_0949'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='parts_short',
            name='computers',
        ),
        migrations.AlterField(
            model_name='articles',
            name='parts_short',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cat.parts_full'),
        ),
    ]
