# Generated by Django 5.0.1 on 2024-01-31 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0004_remove_ordersreceived_supplier_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='buyers',
            name='order_count',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='suppliers',
            name='order_count',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]