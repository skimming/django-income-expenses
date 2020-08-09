# Generated by Django 3.1 on 2020-08-09 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taxes', '0002_auto_20200809_1858'),
    ]

    operations = [
        migrations.AddField(
            model_name='tax',
            name='payee',
            field=models.CharField(choices=[('FEDERAL', 'FEDERAL'), ('STATE', 'STATE'), ('LOCAL', 'LOCAL')], default='FEDERAL', max_length=30),
        ),
        migrations.AddField(
            model_name='tax',
            name='taxtype',
            field=models.CharField(choices=[('SALES', 'SALES'), ('PAYROLL', 'PAYROLL'), ('SOCIALSECURITY', 'SOCIALSECURITY')], default='SALES', max_length=30),
        ),
    ]
