# Generated by Django 2.2.12 on 2020-07-09 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0023_auto_20200709_1119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='total',
            field=models.IntegerField(blank=True),
        ),
    ]
