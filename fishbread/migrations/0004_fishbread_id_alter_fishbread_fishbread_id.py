# Generated by Django 5.0 on 2023-12-18 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fishbread', '0003_remove_fishbread_foundation_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='fishbread',
            name='id',
            field=models.BigAutoField(auto_created=True, default=0, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='fishbread',
            name='fishbread_id',
            field=models.IntegerField(),
        ),
    ]
