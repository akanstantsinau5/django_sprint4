# Generated by Django 3.2.16 on 2024-07-11 14:21

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20240709_1306'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-pub_date'], 'verbose_name': 'публикация', 'verbose_name_plural': 'Публикации'},
        ),
        migrations.AlterModelManagers(
            name='post',
            managers=[
                ('manager', django.db.models.manager.Manager()),
            ],
        ),
    ]
