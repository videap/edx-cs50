# Generated by Django 3.0.8 on 2020-07-09 20:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_auto_20200709_1612'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='listing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auctions.Listing'),
        ),
    ]
