# Generated by Django 5.0.1 on 2024-09-09 15:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webshop', '0017_remove_product_available_sizes_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productimage',
            name='product',
        ),
    ]
