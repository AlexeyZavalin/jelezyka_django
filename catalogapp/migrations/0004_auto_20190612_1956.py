# Generated by Django 2.2 on 2019-06-12 09:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalogapp', '0003_auto_20190612_1950'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockproduct',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogapp.Product', verbose_name='Товар'),
        ),
        migrations.AlterField(
            model_name='stockproduct',
            name='stock',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogapp.Stock', verbose_name='Склад'),
        ),
    ]
