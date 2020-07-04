# Generated by Django 2.2.12 on 2020-07-02 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='unti_price',
        ),
        migrations.AddField(
            model_name='option',
            name='unti_price',
            field=models.IntegerField(blank=True, default=1),
            preserve_default=False,
        ),
    ]
