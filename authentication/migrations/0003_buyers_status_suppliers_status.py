# Generated by Django 5.0.1 on 2024-01-31 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_ordersreceived_orderssent_delete_orders'),
    ]

    operations = [
        migrations.AddField(
            model_name='buyers',
            name='status',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='suppliers',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]
