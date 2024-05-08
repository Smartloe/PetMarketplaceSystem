# Generated by Django 5.0.4 on 2024-05-08 13:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commodity', '0002_initial'),
        ('trade', '0002_rename_cart_shoppingcart'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shoppingcart',
            name='commodityInfos',
        ),
        migrations.AddField(
            model_name='shoppingcart',
            name='commodity',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to='commodity.commodityinfos', verbose_name='商品'),
        ),
    ]
