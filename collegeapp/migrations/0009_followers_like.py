# Generated by Django 3.1.7 on 2021-05-10 10:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('collegeapp', '0008_auto_20210508_1924'),
    ]

    operations = [
        migrations.CreateModel(
            name='Like',
            fields=[
                ('likeId', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('user1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='onelike', to=settings.AUTH_USER_MODEL)),
                ('user2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='twolike', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Followers',
            fields=[
                ('followId', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('user1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='one', to=settings.AUTH_USER_MODEL)),
                ('user2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='two', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
