# Generated by Django 3.1.1 on 2021-02-13 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ideas', '0041_auto_20210125_1749'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='banking_accept_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='payment_accept_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
