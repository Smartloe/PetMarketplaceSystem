# Generated by Django 5.0.4 on 2024-05-06 23:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0004_alter_orderinfos_coupon_price_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='orderinfos',
            options={},
        ),
        migrations.AddField(
            model_name='orderinfos',
            name='update_by',
            field=models.CharField(blank=True, max_length=255, verbose_name='更新人'),
        ),
    ]