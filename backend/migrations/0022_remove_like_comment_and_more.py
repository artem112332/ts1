# Generated by Django 5.0.4 on 2024-12-05 13:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0021_rename_question_consultationrequest_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='like',
            name='comment',
        ),
        migrations.RemoveField(
            model_name='consultationrequest',
            name='author',
        ),
        migrations.RemoveField(
            model_name='like',
            name='ConsultationRequest',
        ),
        migrations.RemoveField(
            model_name='like',
            name='user',
        ),
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Нет комментариев', 'Нет комментариев'), ('Не решён', 'Не решён'), ('Решён', 'Решён')], default='Нет комментариев', max_length=20)),
                ('title', models.TextField(max_length=200)),
                ('description', models.TextField(max_length=1000)),
                ('likes', models.IntegerField(default=0)),
                ('datetime', models.DateTimeField(blank=True)),
                ('is_new', models.BooleanField(default=True)),
                ('comments_count', models.IntegerField(default=0)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.userprofile')),
            ],
        ),
        migrations.DeleteModel(
            name='Commentary',
        ),
        migrations.DeleteModel(
            name='ConsultationRequest',
        ),
        migrations.DeleteModel(
            name='Like',
        ),
    ]
