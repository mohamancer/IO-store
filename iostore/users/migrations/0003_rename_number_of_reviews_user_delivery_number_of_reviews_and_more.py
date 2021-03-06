# Generated by Django 4.0.4 on 2022-05-20 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_rating'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='number_of_reviews',
            new_name='delivery_number_of_reviews',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='rating',
            new_name='delivery_rating',
        ),
        migrations.AddField(
            model_name='user',
            name='receiving_number_of_reviews',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='receiving_rating',
            field=models.FloatField(blank=True, default=0),
        ),
    ]
