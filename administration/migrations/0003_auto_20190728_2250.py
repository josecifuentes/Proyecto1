# Generated by Django 2.0.13 on 2019-07-29 04:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0002_profile_usuario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='State',
            field=models.CharField(choices=[('inactive', 'Inactive'), ('active', 'Active'), ('register', 'register')], default='register', max_length=10),
        ),
    ]
