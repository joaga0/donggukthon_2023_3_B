# Generated by Django 5.0 on 2023-12-19 16:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fishbread', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fishbread',
            name='user_id',
        ),
    ]
