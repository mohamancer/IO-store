# Generated by Django 4.0.4 on 2022-05-11 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_user_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, default='users/images/avatar.svg', null=True, upload_to=''),
        ),
    ]