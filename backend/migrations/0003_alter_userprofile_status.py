# Generated by Django 5.0.4 on 2024-04-23 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_remove_userprofile_is_mentor_userprofile_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='status',
            field=models.CharField(choices=[('Проектант', 'Проектант'), ('Наставник', 'Наставник')], default='PR', max_length=20),
        ),
    ]
