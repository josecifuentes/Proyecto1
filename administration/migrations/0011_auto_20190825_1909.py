# Generated by Django 2.0.13 on 2019-08-26 01:09

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0010_auto_20190825_1906'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='Create',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 8, 26, 1, 9, 55, 952616, tzinfo=utc), null=True),
        ),
    ]
