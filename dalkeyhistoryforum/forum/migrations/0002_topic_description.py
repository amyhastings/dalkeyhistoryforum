# Generated by Django 4.2.16 on 2025-01-24 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='description',
            field=models.CharField(default='', max_length=1000),
        ),
    ]
