# Generated by Django 5.0.1 on 2024-09-12 14:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webshop', '0033_cartitem_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='size',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='webshop.productvariationsize'),
        ),
    ]
