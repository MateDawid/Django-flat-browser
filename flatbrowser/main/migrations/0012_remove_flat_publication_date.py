# Generated by Django 3.1.5 on 2021-01-24 22:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_auto_20210124_2349'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flat',
            name='publication_date',
        ),
    ]
