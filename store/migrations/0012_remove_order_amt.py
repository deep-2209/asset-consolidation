# Generated by Django 3.1.13 on 2024-04-14 12:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_auto_20240414_1823'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='amt',
        ),
    ]