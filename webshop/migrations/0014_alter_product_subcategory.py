# Generated by Django 5.0.1 on 2024-09-08 21:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webshop', '0013_alter_product_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='subcategory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webshop.subcategory'),
        ),
    ]
