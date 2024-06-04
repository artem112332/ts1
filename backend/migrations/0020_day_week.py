# Generated by Django 5.0.4 on 2024-06-02 09:14

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0019_alter_like_comment_alter_like_question'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Day',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_9to10', models.CharField(choices=[('Свободно', 'Свободно'), ('Недоступно', 'Недоступно'), ('Занято', 'Занято')], default='Недоступно', max_length=15)),
                ('time_10to11', models.CharField(choices=[('Свободно', 'Свободно'), ('Недоступно', 'Недоступно'), ('Занято', 'Занято')], default='Недоступно', max_length=15)),
                ('time_11to12', models.CharField(choices=[('Свободно', 'Свободно'), ('Недоступно', 'Недоступно'), ('Занято', 'Занято')], default='Недоступно', max_length=15)),
                ('time_12to13', models.CharField(choices=[('Свободно', 'Свободно'), ('Недоступно', 'Недоступно'), ('Занято', 'Занято')], default='Недоступно', max_length=15)),
                ('time_13to14', models.CharField(choices=[('Свободно', 'Свободно'), ('Недоступно', 'Недоступно'), ('Занято', 'Занято')], default='Недоступно', max_length=15)),
                ('time_14to15', models.CharField(choices=[('Свободно', 'Свободно'), ('Недоступно', 'Недоступно'), ('Занято', 'Занято')], default='Недоступно', max_length=15)),
                ('time_15to16', models.CharField(choices=[('Свободно', 'Свободно'), ('Недоступно', 'Недоступно'), ('Занято', 'Занято')], default='Недоступно', max_length=15)),
                ('time_16to17', models.CharField(choices=[('Свободно', 'Свободно'), ('Недоступно', 'Недоступно'), ('Занято', 'Занято')], default='Недоступно', max_length=15)),
                ('time_17to18', models.CharField(choices=[('Свободно', 'Свободно'), ('Недоступно', 'Недоступно'), ('Занято', 'Занято')], default='Недоступно', max_length=15)),
                ('time_18to19', models.CharField(choices=[('Свободно', 'Свободно'), ('Недоступно', 'Недоступно'), ('Занято', 'Занято')], default='Недоступно', max_length=15)),
                ('time_19to20', models.CharField(choices=[('Свободно', 'Свободно'), ('Недоступно', 'Недоступно'), ('Занято', 'Занято')], default='Недоступно', max_length=15)),
                ('time_20to21', models.CharField(choices=[('Свободно', 'Свободно'), ('Недоступно', 'Недоступно'), ('Занято', 'Занято')], default='Недоступно', max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Week',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('friday', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='backend.day')),
                ('monday', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='backend.day')),
                ('saturday', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='backend.day')),
                ('sunday', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='backend.day')),
                ('thursday', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='backend.day')),
                ('tuesday', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='backend.day')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('wednesday', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='backend.day')),
            ],
        ),
    ]