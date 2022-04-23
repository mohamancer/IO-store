# Generated by Django 4.0.4 on 2022-04-23 13:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_bid_bidder'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='request',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.request'),
        ),
        migrations.AddField(
            model_name='request',
            name='Host',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='request',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.category'),
        ),
    ]
