# Generated by Django 4.0.4 on 2022-05-23 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offer', '0008_alter_offer_post_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='address',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Address'),
        ),
        migrations.AddField(
            model_name='offer',
            name='latitude',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Latitude'),
        ),
        migrations.AddField(
            model_name='offer',
            name='longitude',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Longitude'),
        ),
    ]
