# Generated by Django 3.1.1 on 2021-01-05 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cat', '0022_compprice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compprice',
            name='case_computers',
            field=models.CharField(blank=True, db_index=True, max_length=300, null=True, verbose_name='Case_computers'),
        ),
        migrations.AlterField(
            model_name='compprice',
            name='cool_computers',
            field=models.CharField(blank=True, db_index=True, max_length=300, null=True, verbose_name='Cool_computers'),
        ),
        migrations.AlterField(
            model_name='compprice',
            name='hdd2_computers',
            field=models.CharField(blank=True, db_index=True, max_length=300, null=True, verbose_name='Hdd_computers'),
        ),
        migrations.AlterField(
            model_name='compprice',
            name='hdd_computers',
            field=models.CharField(blank=True, db_index=True, max_length=300, null=True, verbose_name='Hdd_computers'),
        ),
        migrations.AlterField(
            model_name='compprice',
            name='mb_computers',
            field=models.CharField(blank=True, db_index=True, max_length=300, null=True, verbose_name='Mb_computers'),
        ),
        migrations.AlterField(
            model_name='compprice',
            name='mem_computers',
            field=models.CharField(blank=True, db_index=True, max_length=300, null=True, verbose_name='Mem_computers'),
        ),
        migrations.AlterField(
            model_name='compprice',
            name='price_computers',
            field=models.CharField(blank=True, db_index=True, max_length=300, null=True, verbose_name='Price_computers'),
        ),
        migrations.AlterField(
            model_name='compprice',
            name='proc_computers',
            field=models.CharField(blank=True, db_index=True, max_length=300, null=True, verbose_name='Proc_computers'),
        ),
        migrations.AlterField(
            model_name='compprice',
            name='ps_computers',
            field=models.CharField(blank=True, db_index=True, max_length=300, null=True, verbose_name='Ps_computers'),
        ),
        migrations.AlterField(
            model_name='compprice',
            name='vent_computers',
            field=models.CharField(blank=True, db_index=True, max_length=300, null=True, verbose_name='Url_computers'),
        ),
        migrations.AlterField(
            model_name='compprice',
            name='video_computers',
            field=models.CharField(blank=True, db_index=True, max_length=300, null=True, verbose_name='Video_computers'),
        ),
    ]
