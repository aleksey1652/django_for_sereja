# Generated by Django 3.1.1 on 2020-10-06 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cat', '0013_auto_20201005_1004'),
    ]

    operations = [
        migrations.AddField(
            model_name='parts_short',
            name='kind',
            field=models.CharField(blank=True, db_index=True, max_length=50, null=True, verbose_name='Kind'),
        ),
    ]
