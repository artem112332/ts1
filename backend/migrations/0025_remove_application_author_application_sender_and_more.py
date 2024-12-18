# Generated by Django 5.0.4 on 2024-12-09 12:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0024_remove_application_likes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='application',
            name='author',
        ),
        migrations.AddField(
            model_name='application',
            name='sender',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='application_sender', to='backend.userprofile'),
        ),
        migrations.AddField(
            model_name='application',
            name='target',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='application_target', to='backend.userprofile'),
        ),
        migrations.AddField(
            model_name='application',
            name='type',
            field=models.CharField(choices=[('Общая', 'Общая'), ('Прямая', 'Прямая')], default='Общая', max_length=20),
        ),
    ]
