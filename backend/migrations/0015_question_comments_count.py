# Generated by Django 5.0.4 on 2024-05-14 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0014_question_is_new'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='comments_count',
            field=models.IntegerField(default=0),
        ),
    ]
