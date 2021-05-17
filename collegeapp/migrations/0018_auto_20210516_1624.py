# Generated by Django 3.1.7 on 2021-05-16 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collegeapp', '0017_coursereview_collegeid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coursereview',
            name='instrumentsRating',
        ),
        migrations.AddField(
            model_name='coursereview',
            name='helpfulCount',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='coursereview',
            name='inappropriateCount',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='coursereview',
            name='spamCount',
            field=models.IntegerField(default=0),
        ),
    ]
