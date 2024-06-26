# Generated by Django 5.0.4 on 2024-04-15 14:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.CharField(max_length=50)),
                ('first_name', models.CharField(max_length=50)),
                ('middle_name', models.CharField(max_length=50)),
                ('is_mentor', models.BooleanField(default=False)),
                ('specialization_1', models.CharField(choices=[('Teamlead', 'Teamlead'), ('Backend', 'Backend'), ('Frontend', 'Frontend'), ('Дизайн', 'Дизайн'), ('Аналитика', 'Аналитика')], max_length=20)),
                ('specialization_2', models.CharField(choices=[('Teamlead', 'Teamlead'), ('Backend', 'Backend'), ('Frontend', 'Frontend'), ('Дизайн', 'Дизайн'), ('Аналитика', 'Аналитика')], max_length=20)),
                ('specialization_3', models.CharField(choices=[('Teamlead', 'Teamlead'), ('Backend', 'Backend'), ('Frontend', 'Frontend'), ('Дизайн', 'Дизайн'), ('Аналитика', 'Аналитика')], max_length=20)),
                ('description', models.TextField(max_length=1000)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Нет комментариев', 'Нет комментариев'), ('Не решён', 'Не решён'), ('Решён', 'Решён')], max_length=20)),
                ('title', models.TextField(max_length=150)),
                ('text', models.TextField(max_length=500)),
                ('likes', models.IntegerField()),
                ('specialization_1', models.CharField(choices=[('Teamlead', 'Teamlead'), ('Backend', 'Backend'), ('Frontend', 'Frontend'), ('Дизайн', 'Дизайн'), ('Аналитика', 'Аналитика')], max_length=20)),
                ('specialization_2', models.CharField(choices=[('Teamlead', 'Teamlead'), ('Backend', 'Backend'), ('Frontend', 'Frontend'), ('Дизайн', 'Дизайн'), ('Аналитика', 'Аналитика')], max_length=20)),
                ('specialization_3', models.CharField(choices=[('Teamlead', 'Teamlead'), ('Backend', 'Backend'), ('Frontend', 'Frontend'), ('Дизайн', 'Дизайн'), ('Аналитика', 'Аналитика')], max_length=20)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Consultation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Отправлен', 'Отправлен'), ('Принят', 'Принят'), ('Отклонён', 'Отклонён')], default='Отправлен', max_length=20)),
                ('join_link', models.CharField(max_length=150)),
                ('author_of_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='backend.userprofile')),
                ('mentor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='backend.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Commentary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('has_parent', models.BooleanField(default=False)),
                ('likes', models.IntegerField()),
                ('is_answer', models.BooleanField(default=False)),
                ('text', models.TextField(max_length=500)),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.commentary')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.question')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.userprofile')),
            ],
        ),
    ]
