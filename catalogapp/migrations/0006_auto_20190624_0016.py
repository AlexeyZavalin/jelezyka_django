# Generated by Django 2.2 on 2019-06-23 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogapp', '0005_remove_product_stock'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Наименование категории'),
        ),
    ]