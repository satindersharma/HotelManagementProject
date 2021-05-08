# Generated by Django 3.2.2 on 2021-05-08 12:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('roomapp', '0002_auto_20210508_1739'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='room',
        ),
        migrations.AddField(
            model_name='booking',
            name='room_category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='roomapp.roomcategory'),
            preserve_default=False,
        ),
    ]
