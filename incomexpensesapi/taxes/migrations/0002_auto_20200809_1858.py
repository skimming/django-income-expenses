# Generated by Django 3.1 on 2020-08-09 18:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taxes', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tax',
            name='payee',
        ),
        migrations.RemoveField(
            model_name='tax',
            name='taxtype',
        ),
    ]