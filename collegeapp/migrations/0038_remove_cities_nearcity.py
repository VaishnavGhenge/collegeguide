# Generated by Django 3.1.7 on 2021-05-30 15:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collegeapp', '0037_auto_20210524_2046'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cities',
            name='nearCity',
        ),
    ]
