# Generated by Django 5.0.4 on 2024-05-19 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commodity', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commodityinfos',
            name='cost_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=24, verbose_name='商品进价'),
        ),
    ]