# Generated by Django 5.0.4 on 2024-12-18 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0028_application_mentor_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
    ]
