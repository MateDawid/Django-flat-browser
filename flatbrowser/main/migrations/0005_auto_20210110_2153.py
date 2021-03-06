# Generated by Django 3.1.5 on 2021-01-10 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20210110_1912'),
    ]

    operations = [
        migrations.AddField(
            model_name='flat',
            name='city',
            field=models.CharField(default='Jaworzno', max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='flat',
            name='area',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='flat',
            name='price',
            field=models.FloatField(),
        ),
    ]
