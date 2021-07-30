# Generated by Django 3.0.8 on 2020-07-14 01:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_user_watchlist'),
    ]

    operations = [
        migrations.CreateModel(
            name='Winners',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bid', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='auctions.Bid')),
                ('listing', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='auctions.Listing')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
