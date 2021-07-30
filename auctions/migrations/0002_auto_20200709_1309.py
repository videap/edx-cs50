# Generated by Django 3.0.8 on 2020-07-09 16:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('image_url', models.URLField()),
                ('description', models.TextField(max_length=2048)),
                ('open_status', models.BooleanField()),
                ('min_bid', models.DecimalField(decimal_places=2, max_digits=11)),
                ('max_bid', models.DecimalField(decimal_places=2, max_digits=11)),
                ('category', models.CharField(choices=[('AUTO', 'Automotive'), ('EL', 'Electronics'), ('ART', 'Arts'), ('SPT', 'Sports'), ('FSH', 'Fashion'), ('HME', 'Home'), ('RE', 'Real Estate'), ('PET', 'Pets'), ('IND', 'Industry')], max_length=24)),
                ('creation_timestamp', models.DateTimeField(auto_now_add=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_listings', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=256)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='auctions.Listing')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_comments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bid_value', models.DecimalField(decimal_places=2, max_digits=11)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bids', to='auctions.Listing')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_bids', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='watchlist',
            field=models.ManyToManyField(related_name='users_watching', to='auctions.Listing'),
        ),
    ]
