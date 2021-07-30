# Generated by Django 3.0.8 on 2020-07-10 19:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_auto_20200709_1736'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='listing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listing_bids', to='auctions.Listing'),
        ),
    ]
