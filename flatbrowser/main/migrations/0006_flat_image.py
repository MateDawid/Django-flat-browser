# Generated by Django 3.1.5 on 2021-01-21 22:29

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20210110_2153'),
    ]

    operations = [
        migrations.AddField(
            model_name='flat',
            name='image',
            field=models.URLField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
