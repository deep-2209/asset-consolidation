# Generated by Django 3.1.13 on 2024-05-01 11:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0017_order_season'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='buyer',
            name='interest',
        ),
        migrations.RemoveField(
            model_name='supplier',
            name='interest',
        ),
    ]
