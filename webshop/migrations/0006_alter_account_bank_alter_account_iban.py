# Generated by Django 5.0.1 on 2024-09-04 00:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webshop', '0005_alter_account_bank_alter_account_iban'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='bank',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='iban',
            field=models.CharField(blank=True, max_length=34, null=True),
        ),
    ]
