# Generated by Django 5.0.4 on 2024-05-06 06:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0002_alter_orderinfos_created_by_alter_userinfos_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userinfos',
            name='last_login',
        ),
        migrations.RemoveField(
            model_name='userinfos',
            name='password',
        ),
    ]