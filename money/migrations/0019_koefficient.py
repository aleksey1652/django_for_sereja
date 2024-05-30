# Generated by Django 3.1.1 on 2022-02-19 16:18

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('money', '0018_auto_20220219_1714'),
    ]

    operations = [
        migrations.CreateModel(
            name='Koefficient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('hand', models.FloatField(db_index=True, default=0, verbose_name='Коэффициент')),
            ],
            options={
                'verbose_name': 'Koefficient',
                'verbose_name_plural': 'Koefficientes',
                'ordering': ['date'],
            },
        ),
    ]
