# Generated by Django 2.2.12 on 2020-07-09 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0029_auto_20200709_1208'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='total',
            field=models.IntegerField(null=True),
        ),
    ]
