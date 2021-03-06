# Generated by Django 2.2.12 on 2020-07-08 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0016_auto_20200708_1649'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='discounted_price',
            field=models.IntegerField(blank=True, default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='original_price',
            field=models.IntegerField(blank=True, default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='stock',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Option',
        ),
        migrations.DeleteModel(
            name='Size',
        ),
    ]
