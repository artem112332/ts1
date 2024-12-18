# Generated by Django 5.0.4 on 2024-12-05 11:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0019_alter_like_comment_alter_like_question'),
    ]

    operations = [
        migrations.AddField(
            model_name='consultation',
            name='date',
            field=models.DateField(default=datetime.date(2024, 12, 5)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='consultation',
            name='time',
            field=models.CharField(default=1, max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='have_schedule',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='telegram',
            field=models.CharField(default=datetime.date(2024, 12, 5), max_length=50),
            preserve_default=False,
        ),
    ]