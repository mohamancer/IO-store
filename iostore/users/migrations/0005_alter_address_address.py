# Generated by Django 4.0.4 on 2022-05-21 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='address',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Address'),
        ),
    ]
