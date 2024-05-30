# Generated by Django 3.1.1 on 2022-01-25 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('money', '0012_bids_advanced'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bids',
            name='few_sborsik',
        ),
        migrations.AddField(
            model_name='bids',
            name='first_sborsik',
            field=models.CharField(db_index=True, default='', max_length=100, verbose_name='first_sborsik'),
        ),
        migrations.AddField(
            model_name='goods',
            name='software_bonus',
            field=models.PositiveIntegerField(db_index=True, default=100, verbose_name='software_bonus'),
        ),
        migrations.AlterField(
            model_name='bids',
            name='status',
            field=models.CharField(choices=[('Отправлен', 'Отправлен'), ('Подтверждён', 'Подтверждён'), ('Идёт диалог', 'Идёт диалог'), ('Ожидаем оплату', 'Ожидаем оплату'), ('Заказ товара', 'Заказ товара'), ('Идёт сборка', 'Идёт сборка'), ('Выкуплен', 'Выкуплен'), ('Сервис', 'Сервис'), ('Отказ', 'Отказ')], db_index=True, default='Идёт диалог', max_length=50, verbose_name='status'),
        ),
    ]
