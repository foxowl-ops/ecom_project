# Generated by Django 2.2.12 on 2020-07-06 07:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_product_bottom_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='bottom_price',
        ),
    ]
