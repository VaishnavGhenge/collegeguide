# Generated by Django 3.1.7 on 2021-05-22 22:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collegeapp', '0030_auto_20210522_1924'),
    ]

    operations = [
        migrations.AlterField(
            model_name='platformstatistics',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
