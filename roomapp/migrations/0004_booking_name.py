# Generated by Django 3.2.2 on 2021-05-08 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roomapp', '0003_auto_20210508_1744'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='name',
            field=models.CharField(default='sharma', max_length=100),
            preserve_default=False,
        ),
    ]
