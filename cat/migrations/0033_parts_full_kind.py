# Generated by Django 3.1.1 on 2021-04-20 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cat', '0032_parts_full_is_hot'),
    ]

    operations = [
        migrations.AddField(
            model_name='parts_full',
            name='kind',
            field=models.CharField(blank=True, db_index=True, max_length=50, null=True, verbose_name='kind'),
        ),
    ]
