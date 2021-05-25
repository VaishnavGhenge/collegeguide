# Generated by Django 3.1.7 on 2021-05-24 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collegeapp', '0034_auto_20210523_1837'),
    ]

    operations = [
        migrations.AddField(
            model_name='collegehelpful',
            name='purpose',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='coursehelpful',
            name='purpose',
            field=models.IntegerField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='coursereview',
            name='nothelpfulCount',
            field=models.IntegerField(default=0),
        ),
    ]
