# Generated by Django 3.1.1 on 2021-11-29 07:04

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bids',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ID', models.CharField(db_index=True, max_length=50, verbose_name='ID')),
                ('site', models.CharField(blank=True, choices=[('versum', 'versum'), ('itblok', 'itblok')], db_index=True, max_length=10, null=True, verbose_name='site')),
                ('status', models.CharField(blank=True, choices=[('Отправлен', 'Отправлен'), ('Подтверждён', 'Подтверждён'), ('Ожидает деталь', 'Ожидает деталь'), ('Идёт диалог', 'Идёт диалог'), ('Ожидаем оплату', 'Ожидаем оплату'), ('Заказ товара', 'Заказ товара'), ('Идёт сборка', 'Идёт сборка'), ('Дубль', 'Дубль'), ('Выкуплен', 'Выкуплен'), ('Неактуально', 'Неактуально'), ('Ремонт ПК', 'Ремонт ПК'), ('Удален', 'Удален'), ('Отказ', 'Отказ')], db_index=True, max_length=50, null=True, verbose_name='status')),
                ('sposobOplaty', models.CharField(blank=True, choices=[('Другой способ оплаты', 'Другой способ оплаты'), ('Кредит Альфа Банк', 'Кредит Альфа Банк'), ('Оплата на ФОП', 'Оплата на ФОП'), ('Оплата картой Visa/MasterCard', 'Оплата картой Visa/MasterCard'), ('Оплата онлайн-картой (LiqPay)', 'Оплата онлайн-картой (LiqPay)'), ('Безналичный с НДС', 'Безналичный с НДС'), ('На карту', 'На карту'), ('Кредит Монобанк', 'Кредит Монобанк'), ('Готівкою', 'Готівкою')], db_index=True, max_length=100, null=True, verbose_name='sposobOplaty')),
                ('istocnikZakaza', models.CharField(blank=True, db_index=True, max_length=100, null=True, verbose_name='istocnikZakaza')),
                ('date_ch', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'ID',
                'verbose_name_plural': 'ID+',
                'ordering': ['date_ch'],
            },
        ),
        migrations.CreateModel(
            name='Managers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, default='somebody', max_length=100, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'Name',
                'verbose_name_plural': 'Names',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Statistics_bid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('bid_count', models.PositiveIntegerField(default=0, verbose_name='bid_count')),
                ('idet_dialog_count', models.PositiveIntegerField(default=0, verbose_name='idet_dialog_count')),
                ('ojidaem_oplatu_count', models.PositiveIntegerField(default=0, verbose_name='ojidaem_oplatu_count')),
                ('otkaz_count', models.PositiveIntegerField(default=0, verbose_name='otkaz_count')),
                ('positive_count', models.PositiveIntegerField(default=0, verbose_name='positive_count')),
                ('negative_sum', models.IntegerField(default=0, verbose_name='negative_sum')),
                ('managers', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='money.managers')),
            ],
            options={
                'verbose_name': 'Statistics_bids',
                'verbose_name_plural': 'Statistics_bid',
                'ordering': ['date'],
            },
        ),
        migrations.CreateModel(
            name='Statistics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('site', models.CharField(blank=True, choices=[('versum', 'versum'), ('itblok', 'itblok')], db_index=True, max_length=10, null=True, verbose_name='site')),
                ('sposobOplaty', models.CharField(blank=True, choices=[('Другой способ оплаты', 'Другой способ оплаты'), ('Кредит Альфа Банк', 'Кредит Альфа Банк'), ('Оплата на ФОП', 'Оплата на ФОП'), ('Оплата картой Visa/MasterCard', 'Оплата картой Visa/MasterCard'), ('Оплата онлайн-картой (LiqPay)', 'Оплата онлайн-картой (LiqPay)'), ('Безналичный с НДС', 'Безналичный с НДС'), ('На карту', 'На карту'), ('Кредит Монобанк', 'Кредит Монобанк'), ('Готівкою', 'Готівкою')], db_index=True, max_length=100, null=True, verbose_name='sposobOplaty')),
                ('istocnikZakaza', models.CharField(blank=True, db_index=True, max_length=100, null=True, verbose_name='istocnikZakaza')),
                ('kind', models.CharField(blank=True, choices=[('Системный блок', 'Системный блок'), ('ПО', 'ПО'), ('Комплектующие', 'Комплектующие'), ('Периферия', 'Периферия')], db_index=True, max_length=100, null=True, verbose_name='kind')),
                ('summa', models.PositiveIntegerField(db_index=True, default=0, verbose_name='summa')),
                ('managers', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='money.managers')),
            ],
            options={
                'verbose_name': 'Statistics',
                'verbose_name_plural': 'Statistic',
                'ordering': ['date'],
            },
        ),
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('summa', models.PositiveIntegerField(db_index=True, default=0, verbose_name='summa')),
                ('discr', models.TextField(blank=True, db_index=True, max_length=5000, null=True, verbose_name='discription')),
                ('kind', models.CharField(blank=True, choices=[('Системный блок', 'Системный блок'), ('ПО', 'ПО'), ('Комплектующие', 'Комплектующие'), ('Периферия', 'Периферия')], db_index=True, max_length=100, null=True, verbose_name='kind')),
                ('bids', models.ForeignKey(default='Системный блок', on_delete=django.db.models.deletion.CASCADE, to='money.bids')),
            ],
            options={
                'verbose_name': 'discription',
                'verbose_name_plural': 'Discriptions',
                'ordering': ['summa'],
            },
        ),
        migrations.AddField(
            model_name='bids',
            name='managers',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='money.managers'),
        ),
    ]