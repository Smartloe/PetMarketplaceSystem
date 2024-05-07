# Generated by Django 5.0.4 on 2024-05-06 18:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commodity', '0006_commodityinfos_types'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commodityinfos',
            name='types',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='commodity.commoditycategories', verbose_name='商品类型'),
        ),
    ]