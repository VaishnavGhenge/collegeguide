# Generated by Django 3.1.7 on 2021-05-17 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collegeapp', '0018_auto_20210516_1624'),
    ]

    operations = [
        migrations.AddField(
            model_name='collegereview',
            name='is_alumni',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='coursereview',
            name='is_alumni',
            field=models.BooleanField(default=False),
        ),
    ]