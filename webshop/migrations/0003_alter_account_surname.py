# Generated by Django 5.0.1 on 2024-08-30 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webshop', '0002_remove_account_gender_account_surname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='surname',
            field=models.CharField(max_length=255),
        ),
    ]
