# Generated by Django 4.0.5 on 2022-06-11 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0002_ordermodel_city_ordermodel_email_ordermodel_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordermodel',
            name='is_paid',
            field=models.BooleanField(default=False),
        ),
    ]
