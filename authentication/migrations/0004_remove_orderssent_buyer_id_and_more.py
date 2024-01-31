# Generated by Django 5.0.1 on 2024-01-31 06:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_buyers_status_suppliers_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderssent',
            name='buyer_id',
        ),
        migrations.RemoveField(
            model_name='ordersreceived',
            name='supplier_id',
        ),
        migrations.DeleteModel(
            name='Buyers',
        ),
        migrations.DeleteModel(
            name='OrdersSent',
        ),
        migrations.DeleteModel(
            name='OrdersReceived',
        ),
        migrations.DeleteModel(
            name='Suppliers',
        ),
    ]
