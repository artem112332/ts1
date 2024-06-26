# Generated by Django 5.0.4 on 2024-05-12 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0009_alter_userprofile_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='consultation',
            name='commentary',
            field=models.TextField(blank=True, max_length=500),
        ),
        migrations.AlterField(
            model_name='question',
            name='status',
            field=models.CharField(choices=[('Нет комментариев', 'Нет комментариев'), ('Не решён', 'Не решён'), ('Решён', 'Решён')], default='Нет комментариев', max_length=20),
        ),
    ]
