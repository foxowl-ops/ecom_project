# Generated by Django 2.2.12 on 2020-07-09 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0031_auto_20200709_1607'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='Total_price',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]