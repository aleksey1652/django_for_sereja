# Generated by Django 3.1.1 on 2020-12-25 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cat', '0019_case_cooler_cpu_fan_gpu_hdd_mb_psu_ram_ssd'),
    ]

    operations = [
        migrations.AlterField(
            model_name='case',
            name='desc_ru',
            field=models.TextField(db_index=True, verbose_name='Desc_ru'),
        ),
        migrations.AlterField(
            model_name='case',
            name='desc_ukr',
            field=models.TextField(db_index=True, verbose_name='Desc_ukr'),
        ),
        migrations.AlterField(
            model_name='cooler',
            name='desc_ru',
            field=models.TextField(db_index=True, verbose_name='Desc_ru'),
        ),
        migrations.AlterField(
            model_name='cooler',
            name='desc_ukr',
            field=models.TextField(db_index=True, verbose_name='Desc_ukr'),
        ),
        migrations.AlterField(
            model_name='cpu',
            name='desc_ru',
            field=models.TextField(db_index=True, verbose_name='Desc_ru'),
        ),
        migrations.AlterField(
            model_name='cpu',
            name='desc_ukr',
            field=models.TextField(db_index=True, verbose_name='Desc_ukr'),
        ),
        migrations.AlterField(
            model_name='fan',
            name='desc_ru',
            field=models.TextField(db_index=True, verbose_name='Desc_ru'),
        ),
        migrations.AlterField(
            model_name='fan',
            name='desc_ukr',
            field=models.TextField(db_index=True, verbose_name='Desc_ukr'),
        ),
        migrations.AlterField(
            model_name='gpu',
            name='desc_ru',
            field=models.TextField(db_index=True, verbose_name='Desc_ru'),
        ),
        migrations.AlterField(
            model_name='gpu',
            name='desc_ukr',
            field=models.TextField(db_index=True, verbose_name='Desc_ukr'),
        ),
        migrations.AlterField(
            model_name='hdd',
            name='desc_ru',
            field=models.TextField(db_index=True, verbose_name='Desc_ru'),
        ),
        migrations.AlterField(
            model_name='hdd',
            name='desc_ukr',
            field=models.TextField(db_index=True, verbose_name='Desc_ukr'),
        ),
        migrations.AlterField(
            model_name='mb',
            name='desc_ru',
            field=models.TextField(db_index=True, verbose_name='Desc_ru'),
        ),
        migrations.AlterField(
            model_name='mb',
            name='desc_ukr',
            field=models.TextField(db_index=True, verbose_name='Desc_ukr'),
        ),
        migrations.AlterField(
            model_name='psu',
            name='desc_ru',
            field=models.TextField(db_index=True, verbose_name='Desc_ru'),
        ),
        migrations.AlterField(
            model_name='psu',
            name='desc_ukr',
            field=models.TextField(db_index=True, verbose_name='Desc_ukr'),
        ),
        migrations.AlterField(
            model_name='ram',
            name='desc_ru',
            field=models.TextField(db_index=True, verbose_name='Desc_ru'),
        ),
        migrations.AlterField(
            model_name='ram',
            name='desc_ukr',
            field=models.TextField(db_index=True, verbose_name='Desc_ukr'),
        ),
        migrations.AlterField(
            model_name='ssd',
            name='desc_ru',
            field=models.TextField(db_index=True, verbose_name='Desc_ru'),
        ),
        migrations.AlterField(
            model_name='ssd',
            name='desc_ukr',
            field=models.TextField(db_index=True, verbose_name='Desc_ukr'),
        ),
    ]
